#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Message handler for processing navigation status updates"""

import numpy as np
from scipy.spatial.transform import Rotation as R
from typing import Optional
from .dashboard_state import DashboardState
from .modules.socket_client import SocketClient
from tms_dashboard.utils.constants import robot_messages


class MessageHandler:
    """Processes messages from socket client and updates dashboard state."""
    
    def __init__(self, socket_client: SocketClient, dashboard_state: DashboardState):
        """Initialize message handler.
        
        Args:
            socket_client: SocketClient instance to get messages from
            dashboard_state: DashboardState instance to update
        """
        self.socket_client = socket_client
        self.dashboard = dashboard_state
        self.target_status = None
        self.distance_0 = 0
        self.distance_x = 0
        self.distance_y = 0
        self.distance_z = 0
    
    def process_messages(self) -> Optional[dict]:
        """Process all messages in buffer and update dashboard state.
        
        Returns:
            Last processed message or None if no messages
        """
        buf = self.socket_client.get_buffer()
        
        if len(buf) == 0:
            return None
        
        for message in buf:
            topic, data = message['topic'], message['data']
            self._handle_message(topic, data)
        
        return self.target_status
    
    def _handle_message(self, topic: str, data):
        """Handle individual message based on topic.
        
        Args:
            topic: Message topic string
            data: Message data payload
        """
        match topic:
            case 'Set image fiducial':
                self._handle_image_fiducial(data)
            
            case 'Reset image fiducials':
                self.dashboard.image_NA_set = False
                self.dashboard.image_RE_set = False
                self.dashboard.image_LE_set = False
            
            case 'Project loaded successfully':
                self.dashboard.project_set = True
            
            case 'Close Project':
                self.dashboard.project_set = False
            
            case 'From Neuronavigation: Update tracker poses':
                self._handle_tracker_poses(data)

                if any(data['visibilities']):
                    self.dashboard.camera_set = True

                    self.dashboard.probe_visible = data['visibilities'][0]
                    self.dashboard.head_visible = data['visibilities'][1]
                    self.dashboard.coil_visible = all(data['visibilities'][2:])

                else:
                    self.dashboard.camera_set = False
                    self.dashboard.probe_visible = False
                    self.dashboard.head_visible = False
                    self.dashboard.coil_visible = False
                
            case 'Neuronavigation to Robot: Update displacement to target':
                self._handle_displacement(data)
            
            case 'Tracker fiducials set':
                self.dashboard.tracker_LE_set = True
                self.dashboard.tracker_RE_set = True
                self.dashboard.tracker_NA_set = True
            
            case 'Reset tracker fiducials':
                self.dashboard.tracker_NA_set = False
                self.dashboard.tracker_RE_set = False
                self.dashboard.tracker_LE_set = False
            
            case "Robot to Neuronavigation: Robot connection status":
                self.dashboard.robot_set = True if data['state'] == 'Connected' else False
            
            case 'Open navigation menu':
                self.dashboard.matrix_set = True
            
            case "Neuronavigation to Robot: Set target":
                self.dashboard.target_set = True
                
                # Extract target position from transformation matrix
                if 'target' in data:
                    target_matrix = np.array(data['target'])
                    
                    # Check if it's a 4x4 transformation matrix
                    if target_matrix.shape == (4, 4):

                        R_mat = target_matrix[:3, :3]

                        rot = R.from_matrix(R_mat)

                        # alpha (X), beta (Y), gamma (Z)
                        alpha, beta, gamma = rot.as_euler('xyz', degrees=True)
                        
                        # Store as tuple [x, y, z, rx, ry, rz]
                        self.dashboard.target_location = (
                            target_matrix[1][3], -target_matrix[2][3], -target_matrix[0][3],
                            alpha,beta,gamma
                        )

            case "Neuronavigation to Robot: Unset target":
                self.dashboard.target_set = False
                self.dashboard.target_location = (0, 0, 0, 0, 0, 0)

            case "Robot to Neuronavigation: Set objective":
                self.dashboard.robot_moving = False if data["objective"] == 0 else True
            
            case 'Coil at target':
                if data['state'] == True:
                    self.dashboard.at_target = True
                else:
                    self.dashboard.at_target = False
            
            case "Start navigation":
                self.dashboard.navigation_button_pressed = True

            case "Stop navigation":
                self.dashboard.navigation_button_pressed = False
              
    def _handle_image_fiducial(self, data):
        """Handle image fiducial setting/unsetting."""
        if data == "":
            return
        
        if str(data['position']) == "nan":
            match data['fiducial_name']:
                case 'NA':
                    self.dashboard.image_NA_set = False
                case 'RE':
                    self.dashboard.image_RE_set = False
                case 'LE':
                    self.dashboard.image_LE_set = False
        else:
            match data['fiducial_name']:
                case 'NA':
                    self.dashboard.image_NA_set = True
                case 'RE':
                    self.dashboard.image_RE_set = True
                case 'LE':
                    self.dashboard.image_LE_set = True
    
    def _handle_tracker_poses(self, data):
        """Handle tracker pose updates."""
        poses = data['poses']
        # Convert angles to degrees
        self.dashboard.probe_location = (
            poses[0][1], -poses[0][2], -poses[0][0],
            np.radians(poses[0][4]), -np.radians(poses[0][5]), np.radians(poses[0][3])
        )
        self.dashboard.head_location = (
            poses[1][1], -poses[1][2], -poses[1][0],
            np.radians(poses[1][4]), -np.radians(poses[1][5]), np.radians(poses[1][3])
        )
        self.dashboard.coil_location = (
            poses[2][1], -poses[2][2], -poses[2][0],
            np.radians(poses[2][4]), -np.radians(poses[2][5]), np.radians(poses[2][3])
        )

    def _handle_displacement(self, data):
        """Handle displacement to target update."""
        self.dashboard.displacement = list(map(lambda x: data['displacement'][x], range(6)))
        self.dashboard.module_displacement = np.linalg.norm(self.dashboard.displacement[:3])

        # Update displacement history for plotting
        self.dashboard.add_displacement_sample()

