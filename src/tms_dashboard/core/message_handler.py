#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Message handler for processing navigation status updates"""

import numpy as np
from typing import Optional
from .dashboard_state import DashboardState
from .socket_client import SocketClient
from ..utils.constants import robot_messages


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
            
            case 'Neuronavigation to Robot: Update displacement to target':
                self._handle_displacement(data)
            
            case "Sensors ID":
                self.dashboard.camera_set = True

                self.dashboard.probe_visible = data[0]
                self.dashboard.head_visible = data[1]
                self.dashboard.coil_visible = all(data[2:])
            
            case 'Remove sensors ID':
                self.dashboard.camera_set = False

                self.dashboard.probe_visible = False
                self.dashboard.head_visible = False
                self.dashboard.coil_visible = False
            
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
            
            case "Set target":
                print("Set target")
                self.dashboard.target_set = True
            
            case 'Unset target':
                self.dashboard.target_set = False

            case "Robot to Neuronavigation: Set objective":
                self.dashboard.robot_moving = False if data["objective"] == 0 else True
            
            case 'Coil at target':
                if data['state'] == True:
                    self.dashboard.at_target = True
                else:
                    self.dashboard.at_target = False
            
            case "Press navigation button":
                self.dashboard.navigation_button_pressed = data["cond"]
                print(data["cond"])
    
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
            poses[0][0], poses[0][1], poses[0][2],
            np.degrees(poses[0][3]), np.degrees(poses[0][4]), np.degrees(poses[0][5])
        )
        self.dashboard.head_location = (
            poses[1][0], poses[1][1], poses[1][2],
            np.degrees(poses[1][3]), np.degrees(poses[1][4]), np.degrees(poses[1][5])
        )
        self.dashboard.coil_location = (
            poses[2][0], poses[2][1], poses[2][2],
            np.degrees(poses[2][3]), np.degrees(poses[2][4]), np.degrees(poses[2][5])
        )
        self.dashboard.target_location = (
            poses[3][0], poses[3][1], poses[3][2],
            np.degrees(poses[3][3]), np.degrees(poses[3][4]), np.degrees(poses[3][5])
        )
    
    def _handle_displacement(self, data):
        """Handle displacement to target update."""
        self.dashboard.displacement = list(map(lambda x: data['displacement'][x], range(6)))
        self.dashboard.module_distance = np.linalg.norm(self.dashboard.displacement[:3])
        self.dashboard.module_distance = str(round(self.dashboard.module_distance, 2)) + " mm"

        # Update displacement history for plotting
        self.dashboard.add_displacement_sample()

