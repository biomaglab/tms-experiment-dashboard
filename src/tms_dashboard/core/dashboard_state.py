#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard state management - framework agnostic"""

from dataclasses import dataclass
from collections import deque
import time
import numpy as np

from tms_dashboard.utils.signal_processing import set_apply_baseline_all, new_indexes_fast_tol


@dataclass
class DashboardState:
    """Central state object for the TMS experiment dashboard.
    
    This class holds all state information including:
    - Connection status (project, camera, robot)
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
        self.emg_connection_set = False
        
        # Image fiducials (set in software)
        self.image_fiducials = False
        self.image_NA_set = False
        self.image_RE_set = False
        self.image_LE_set = False
        
        # Tracker fiducials (real world landmarks)
        self.tracker_fiducials = False

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

        # Rotation history for time series plotting (rx, ry, rz in degrees)
        self.rotation_ax = None
        self.rotation_plot = None
        self.rotation_history_rx = deque(maxlen=self.max_history_length)
        self.rotation_history_ry = deque(maxlen=self.max_history_length)
        self.rotation_history_rz = deque(maxlen=self.max_history_length)
        self.rotation_time_history = deque(maxlen=self.max_history_length)

        # Motor evoked potentials plots and history
        self.mep_ax = None
        self.mep_plot = None
        self.mep_history = []
        self.mep_history_baseline = []
        self.mep_sampling_rate = None
        self.status_new_mep = False
        self.new_meps_index = []
        
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
        """Add current displacement and rotation values to history for time series plotting.
        
        This method is called whenever new displacement data is received.
        It automatically maintains a rolling window of the last max_history_length samples.
        """
        # Calculate elapsed time in seconds
        elapsed_time = time.time() - self._start_time
        
        # Add current displacement values (x, y, z)
        self.displacement_history_x.append(float(self.displacement[0]))
        self.displacement_history_y.append(float(self.displacement[1]))
        self.displacement_history_z.append(float(self.displacement[2]))
        self.displacement_time_history.append(elapsed_time)
        
        # Add current rotation values (rx, ry, rz - indices 3, 4, 5)
        self.rotation_history_rx.append(float(self.displacement[3]))
        self.rotation_history_ry.append(float(self.displacement[4]))
        self.rotation_history_rz.append(float(self.displacement[5]))
        self.rotation_time_history.append(elapsed_time)

    def update_mep_history(self, new_mep_history, t_min, t_max, sampling_rate):
        if len(new_mep_history) == 0:
            return
        if np.array_equal(new_mep_history, self.mep_history):
            return
        
        self.new_meps_index = new_indexes_fast_tol(self.mep_history, new_mep_history)

        self.mep_history = new_mep_history
        self.mep_history_baseline = set_apply_baseline_all(
                                baseline_start_ms=5,      # Início do baseline em 5ms
                                baseline_end_ms=20,        # Fim do baseline em 20ms
                                signal_start_ms= t_min,  # Sinal começa em -10ms
                                signal_end_ms= t_max,    # Sinal termina em 40ms
                                data_windows=new_mep_history, 
                                sampling_rate=sampling_rate
                            )
        self.status_new_mep = True
    
    def get_all_state_mep(self):
        if self.mep_history == [] and self.mep_history_baseline == [] and self.mep_sampling_rate == None and self.status_new_mep == False and self.new_meps_index == []:
            return False
        else:
            return True
        
    def reset_all_state_mep(self):
        self.mep_history = []
        self.mep_history_baseline = []
        self.mep_sampling_rate = None
        self.status_new_mep = False
        self.new_meps_index = []
