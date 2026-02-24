#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Message handler for processing navigation status updates"""
import threading
import numpy as np
from typing import Optional
import time

from src.tms_dashboard.core.dashboard_state import DashboardState
from src.tms_dashboard.core.modules.socket_client import SocketClient
from src.tms_dashboard.core.message_emit import Message2Server
from src.tms_dashboard.core.robot_config_state import RobotConfigState

class MessageHandler:
    """Processes messages from socket client and updates dashboard state."""
    
    def __init__(self, socket_client: SocketClient, dashboard_state: DashboardState, robot_state: RobotConfigState, message_emit: Message2Server):
        """Initializes message handler.
        
        Args:
            socket_client: SocketClient instance to get messages from
            dashboard_state: DashboardState instance to update
        """
        self.socket_client = socket_client
        self.dashboard = dashboard_state
        self.message_emit = message_emit

        self.robot_state = robot_state 

        self.target_status = None
        self.neuronaviagator_status: bool = True

        # Inactivity timeout: reset dashboard if no messages for 120s
        self._last_message_time = time.time()
        self._timeout_seconds = 120.0
        self._timed_out = False

        self._debounce_seconds = 10
        self._surface_debounce_timer = None
    
    def process_messages(self) -> Optional[dict]:
        """Process all messages in buffer and update dashboard state.
        
        Returns:
            Last processed message or None if no messages
        """
        buf = self.socket_client.get_buffer()
        
        if len(buf) == 0:
            # Check for inactivity timeout
            if not self._timed_out and (time.time() - self._last_message_time) > self._timeout_seconds:
                self.dashboard.reset_state()
                self._timed_out = True
            return None
        
        # Messages received — update timestamp and clear timeout flag
        self._last_message_time = time.time()
        self._timed_out = False

        for message in buf:
            topic, data = message['topic'], message['data']
            self._handle_message(topic, data)
        
        return self.target_status
    
    def _handle_message(self, topic: str, data):
        """Handles individual message based on topic.
        
        Args:
            topic: Message topic string
            data: Message data payload
        """

        if self.neuronaviagator_status:

            match topic:

                #IMPORTANT: THIS TOPIC MUST BE THE FIRST
                case 'Exit':
                    self.neuronaviagator_status = False
                    self.dashboard.reset_state()
                    time.sleep(3)
                    self.socket_client.clear_buffer()
                    self.neuronaviagator_status = True

                case 'Set image fiducial':
                    self._handle_image_fiducial(data)
                
                case 'Reset image fiducials':
                    self.dashboard.image_fiducials = False
                
                case 'Project loaded successfully':
                    self.dashboard.project_set = True
                
                case 'Close Project':
                    self.dashboard.project_set = False

                case 'From Neuronavigation: Send coil pose':
                    self._handle_coil_poses(data)

                case 'From Neuronavigation: Update tracker poses':
                    self._handle_tracker_poses(data)

                    if any(data['visibilities']):
                        self.dashboard.camera_set = True

                        self.dashboard.probe_visible = data['visibilities'][0]
                        self.dashboard.head_visible = data['visibilities'][1]
                        self.dashboard.coil_visible = data['visibilities'][2]

                    else:
                        self.dashboard.camera_set = False
                        self.dashboard.probe_visible = False
                        self.dashboard.head_visible = False
                        self.dashboard.coil_visible = False
                    
                case 'Neuronavigation to Robot: Update displacement to target':
                    self._handle_displacement(data)

                    self.dashboard.navigation_button_pressed = True
                    self.dashboard.target_set = True
                    self.dashboard.image_fiducials = True
                    self.dashboard.tracker_fiducials = True
                
                case 'Tracker fiducials set':
                    self.dashboard.tracker_fiducials = True
                
                case 'Reset tracker fiducials':
                    self.dashboard.tracker_fiducials = False
                
                case "Robot to Neuronavigation: Robot connection status":
                    self.dashboard.robot_set = True if data['data'] == 'Connected' else False
                
                case 'Open navigation menu':
                    self.dashboard.matrix_set = True
                
                case "From Neuronavigation: Send target":
                    self.dashboard.target_set = True
                    
                    # Extract target position from transformation matrix
                    if 'target' in data:
                        target = np.array(data['target'])
                        self._handle_target_position(target)

                case "Neuronavigation to Robot: Unset target":
                    self.dashboard.target_set = False
                    self.dashboard.target_location = (0, 0, 0, 0, 0, 0)

                case "Robot to Neuronavigation: Set objective":
                    self.dashboard.robot_moving = False if data["objective"] == 0 else True

                    if not self.dashboard.robot_set and self.dashboard.robot_moving:
                        self.message_emit.check_robot_connection()
                
                case 'Coil at target':
                    if data['state'] == True:
                        self.dashboard.at_target = True
                    else:
                        self.dashboard.at_target = False

                case "Press navigation button":
                    self.dashboard.navigation_button_pressed = data["cond"]
                
                case "Robot to Neuronavigation: Send force sensor data":
                    self.dashboard.force = data["force_feedback"]
                    if not self.dashboard.robot_set:
                        self.message_emit.check_robot_connection()
        
                case "Start navigation":
                    self.dashboard.navigation_button_pressed = True

                case "Stop navigation":
                    self.dashboard.navigation_button_pressed = False

                case "Neuronavigation to Robot: Set free drive":
                    pressed = data["set"]
                    self.dashboard.free_drive_robot_pressed = pressed
                
                case 'Press move away button':
                    pressed = data['pressed']
                    self.dashboard.move_upward_robot_pressed = pressed

                case "Press robot button":
                    pressed = data['pressed']
                    self.dashboard.active_robot_pressed = pressed

                case "Robot to Neuronavigation: Initial config":
                    self.robot_state.sync_from_embedded(data['config'])
                
                case "Robot to Dashboard: PID factors":
                    if 'pid_factors' in data:
                        self.robot_state._sync_pids(data['pid_factors'])

                case "Neuronavigation to Dashboard: Send surface":
                    self._handle_surface_stl(data)
                    self.dashboard.wait_for_stl = False

                case "Fold surface task":
                    self._debounce_surface_request()
                
                case "Set surface colour" | "Set surface transparency":
                    self._handle_material_surface(data)
                
                case "Remove surfaces":
                    surface_indexes = data.get("surface_indexes", None)
                    if surface_indexes:
                        for index in surface_indexes:
                            self.dashboard.stl_urls.pop(index, None)

    def _debounce_surface_request(self):
        """Debounce surface requests to avoid overloading the socket."""
        if self._surface_debounce_timer is not None:
            self._surface_debounce_timer.cancel()
        self._surface_debounce_timer = threading.Timer(
            self._debounce_seconds,
            self.message_emit.request_invesalius_mesh
        )
        self._surface_debounce_timer.start()

                    
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
            self.dashboard.image_fiducials= False
        else:
            match data['fiducial_name']:
                case 'NA':
                    print("Sim")
                    self.dashboard.image_NA_set = True
                case 'RE':
                    self.dashboard.image_RE_set = True
                case 'LE':
                    self.dashboard.image_LE_set = True
            
            if self.dashboard.image_NA_set and self.dashboard.image_RE_set and self.dashboard.image_LE_set:
                self.dashboard.image_fiducials= True
    
    def _handle_coil_poses(self, data):
        poses = data['coord']
        self.dashboard.coil_location = (
            poses[0], -poses[1], poses[2],
            np.radians(poses[4]), -np.radians(poses[3]), np.radians(poses[5])+1.5708
        )

    def _handle_tracker_poses(self, data):
        """Handle tracker pose updates."""
        poses = data['poses']
        # Convert angles to degrees
        self.dashboard.probe_location = (
            poses[0][0], poses[0][1], poses[0][2],
            np.radians(poses[0][3]), np.radians(poses[0][4]), np.radians(poses[0][5])
        )
        self.dashboard.head_location = (
            poses[1][0], poses[1][1], poses[1][2],
            np.radians(poses[1][3]), np.radians(poses[1][4]), np.radians(poses[1][5])
        )

    def _handle_displacement(self, data):
        """Handle displacement to target update."""
        displacement = list(map(lambda x: data['displacement'][x], range(6)))
        self.dashboard.displacement = displacement
        self.dashboard.module_displacement = round(np.linalg.norm(displacement[:3]), 2)

        # Update displacement history for plotting
        self.dashboard.add_displacement_sample()
    
    def _handle_target_position(self, target):
        # Stores in InVesalius coordinate system (same as displacement)
        self.dashboard.target_location = (
            target[0], -target[1], target[2],
            np.radians(target[4]), -np.radians(target[3]), np.radians(target[5])+1.5708
        )

    def _handle_surface_stl(self, data):
        """Handle incoming STL surface (base64) from InVesalius."""
        try:
            name = data.get('model_name')
            stl_b64 = data.get('stl_b64')
            rgb_normalized = data.get('color')
            surface_index = data.get('surface_index')
            transparency = 1 - data.get("transparency")

            if not (name and stl_b64):
                print("Error: Missing model name or STL data.")
                return

            print(f"Processing surface for model: {name}")

            rgb_255 = [int(x * 255) for x in rgb_normalized]
            hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_255)

            # Generate data URL
            # NOTE: If using data URLs directly for binary STL, you'd handle differently.
            data_url = f'data:model/stl;base64,{stl_b64}'

            # Update dashboard
            self.dashboard.stl_urls[surface_index] = {
                "name": name,
                "url": data_url,
                "color": hex_color,
                "transparency": transparency
            }
            self.dashboard.stl_version += 1
            print(f"Updated dashboard for model: {name}")

        except Exception as e:
            print(f"Unhandled exception in processing surface: {e}")

    def _handle_material_surface(self, data):
        if "surface_index" in data:
            surface_index = data["surface_index"]
            if surface_index in self.dashboard.stl_urls:
                if "transparency" in data:
                    prop_material, key = 1 - data["transparency"], "transparency"
                elif "colour" in data:
                    color, key = data["colour"], "color"
                    rgb_255 = [int(x * 255) for x in color]
                    prop_material = "#{:02x}{:02x}{:02x}".format(*rgb_255)
                else:
                    return
                self.dashboard.stl_urls[surface_index][key] = prop_material
                self.dashboard.stl_version += 1

            else:
                self.message_emit.request_invesalius_mesh()

