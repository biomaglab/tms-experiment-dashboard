#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard state management - framework agnostic"""

from dataclasses import dataclass
from collections import deque
import time
import numpy as np


@dataclass
class DashboardState:
    """Central state object for the TMS experiment dashboard.
    
    This class holds all state information including:
    - Connection status (project, camera, robot, TMS)
    - Image and tracker fiducials
    - Navigation data (locations, displacements)
    - Experiment metadata
    """
    
    def __init__(self):
        # Navigation button status
        self.navigation_button_pressed = False
        self.free_drive_robot_pressed = False
        self.move_upward_robot_pressed = False
        self.active_robot_pressed = False

        # Connection and setup status
        self.project_set = False
        self.camera_set = False
        self.robot_set = False
        self.tms_set = False
        
        # Image fiducials (set in software)
        self.image_NA_set = False  # Nasion
        self.image_RE_set = False  # Right ear
        self.image_LE_set = False  # Left ear
        
        # Tracker fiducials (real world landmarks)
        self.tracker_NA_set = False  # Nose
        self.tracker_RE_set = False  # Right tragus
        self.tracker_LE_set = False  # Left tragus

        # Makers Visibilities
        self.probe_visible = False
        self.head_visible = False
        self.coil_visible = False
        
        # Robot and navigation status
        self.matrix_set = False
        self.target_set = False
        self.robot_moving = False
        self.at_target = False
        self.trials_started = False
        
        # Navigation position/orientation data (x, y, z, rx, ry, rz)
        self.displacement = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.module_displacement = 0.0
        self.probe_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.head_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.coil_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.target_location = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)
        self.force = 0.0
        
        # Displacement history for time series plotting (x, y, z only)
        self.displacement_ax = None
        self.displacement_plot = None
        self.max_history_length = 100  # Maximum number of samples to keep
        self.displacement_history_x = deque(maxlen=self.max_history_length)
        self.displacement_history_y = deque(maxlen=self.max_history_length)
        self.displacement_history_z = deque(maxlen=self.max_history_length)
        self.displacement_time_history = deque(maxlen=self.max_history_length)
        self._start_time = time.time()  # Reference time for plotting

        # Motor evoked potentials plots and history
        self.mep_ax = None
        self.mep_plot = None
        self.mep_history = []
        self.mep_sampling_rate = None
        
        # Experiment metadata with default values
        self.experiment_name = 'Paired pulse, dual site, bilateral, leftM1-rightPMv'
        self.experiment_description = 'Dual site paired bilateral TMS stimulation, with 2 channel EMG acquisition. 80 trials, 4 experimental conditions, 200 pulses'
        self.start_date = '2025-01-31'
        self.end_date = '2024-02-01'
        self.experiment_details = 'Paired pulse contralateral conditioning. Paradigm with motor mapping totaling 80 trials with 20 pulses/condition. Target muscle: APB. Inter-pulse interval: 7 to 10 s.'
        
        # Stimulation parameters
        self.conditioning_stimulus = 'right ventral premotor cortex (rPMv)'
        self.test_stimulus = 'left M1'
        self.number_intervals = '30'
        self.interval_step = '15'  # ms
        self.number_trials = '120'
        self.number_conditions = '4'
        self.trials_per_condition = '30'
        self.intertrial_interval = '12'  # ms
    
    def add_displacement_sample(self):
        """Add current displacement values to history for time series plotting.
        
        This method is called whenever new displacement data is received.
        It automatically maintains a rolling window of the last max_history_length samples.
        """
        # Calculate elapsed time in seconds
        elapsed_time = time.time() - self._start_time
        
        # Add current displacement values (x, y, z only)
        self.displacement_history_x.append(float(self.displacement[0]))
        self.displacement_history_y.append(float(self.displacement[1]))
        self.displacement_history_z.append(float(self.displacement[2]))
        self.displacement_time_history.append(elapsed_time)
