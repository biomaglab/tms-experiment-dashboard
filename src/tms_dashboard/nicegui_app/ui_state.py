#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per-client UI state management."""

class DashboardUI:
    """Holds references to UI elements for a single client session.
    
    This class mirrors the UI storage internal to DashboardState but is unique 
    per client connection. It avoids the singleton issue where only the last 
    client's UI elements are stored.
    """
    
    def __init__(self):
        # Connection icons/labels
        self.icon_project = None
        self.label_project = None
        self.icon_robot = None
        self.label_robot = None
        self.icon_camera = None
        self.label_camera = None
        
        # Marker icons/labels
        self.icon_marker_head = None
        self.label_marker_head = None
        self.icon_marker_coil = None
        self.label_marker_coil = None
        self.icon_marker_probe = None
        self.label_marker_probe = None
        
        # Fiducial icons/labels
        self.icon_l_fid = None
        self.label_l_fid = None
        self.icon_nasion = None
        self.label_nasion = None
        self.icon_r_fid = None
        self.label_r_fid = None
        
        self.icon_l_tragus = None
        self.label_l_tragus = None
        self.icon_nose = None
        self.label_nose = None
        self.icon_r_tragus = None
        self.label_r_tragus = None
        
        # Robot status icons/labels
        self.icon_target = None
        self.label_target = None
        self.icon_coil = None
        self.label_coil = None
        self.icon_moving = None
        self.label_moving = None
        
        # Indicators
        self.label_distance = None
        self.label_force = None
        
        # Plots
        self.displacement_plot = None
        self.rotation_plot = None
        self.mep_plot = None
        
        # Navigation Buttons
        self.navigation_button = None
        self.upward_robot_button = None
        self.active_robot_button = None
        self.free_drive_button = None
