#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Robot configuration state management"""

from dataclasses import dataclass, field, fields
from typing import Tuple

# Available options for select fields
MOVEMENT_ALGORITHM_OPTIONS = ['radially_outward', 'directly_upward', 'directly_PID']


@dataclass
class PIDParams:
    """PID controller parameters for a single axis.
    
    Includes standard PID gains plus impedance control parameters.
    """
    kp: float = 0.3  # Proportional gain
    ki: float = 0.01  # Integral gain
    kd: float = 0.0   # Derivative gain
    stiffness: float = 0.05  # Impedance stiffness
    damping: float = 0.02    # Impedance damping
    
    def to_dict(self) -> dict:
        return {
            'kp': self.kp, 
            'ki': self.ki, 
            'kd': self.kd,
            'stiffness': self.stiffness,
            'damping': self.damping
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PIDParams':
        return cls(
            kp=data.get('kp', 0.3), 
            ki=data.get('ki', 0.01), 
            kd=data.get('kd', 0.0),
            stiffness=data.get('stiffness', 0.05),
            damping=data.get('damping', 0.02)
        )


@dataclass 
class RobotConfigState:
    """Robot configuration parameters.
    
    Contains all settings needed for robot control including:
    - Site and robot type selection
    - Sensor configuration
    - Movement algorithm and parameters
    - Speed ratios and timing
    - Position and rotation thresholds
    - PID tuning for each axis
    """
    
    # Sensor configuration
    use_force_sensor: bool = False
    use_pressure_sensor: bool = False
    com_port_pressure_sensor: str = ''
    
    # Movement settings
    movement_algorithm: str = 'directly_PID'
    dwell_time: float = 0.0  # seconds
    safe_height: float = 750.0  # mm
    
    # Speed settings
    default_speed_ratio: float = 0.08  # 0.01-1.0
    tuning_speed_ratio: float = 0.1  # 0.01-1.0
    tuning_interval: float = 1.0  # seconds
    
    # Thresholds
    translation_threshold: float = 20.0  # mm
    rotation_threshold: float = 15.0  # degrees
    
    # Safety and debug
    stop_robot_if_head_not_visible: bool = True
    wait_for_keypress_before_movement: bool = False
    verbose: bool = False
    
    # PID parameters for translation (X, Y, Z)
    # X and Y use default PID (Kp=0.3, Ki=0.01, Kd=0.0)
    # Z uses different defaults based on sensor mode (handled in UI)
    pid_x: PIDParams = field(default_factory=lambda: PIDParams(kp=0.3, ki=0.01, kd=0.0))
    pid_y: PIDParams = field(default_factory=lambda: PIDParams(kp=0.3, ki=0.01, kd=0.0))
    pid_z: PIDParams = field(default_factory=lambda: PIDParams(kp=0.1, ki=0.0, kd=0.0, stiffness=0.05, damping=0.02))
    
    # PID parameters for rotation (RX, RY, RZ)
    pid_rx: PIDParams = field(default_factory=lambda: PIDParams(kp=0.3, ki=0.01, kd=0.0))
    pid_ry: PIDParams = field(default_factory=lambda: PIDParams(kp=0.3, ki=0.01, kd=0.0))
    pid_rz: PIDParams = field(default_factory=lambda: PIDParams(kp=0.3, ki=0.01, kd=0.0))
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary for serialization/socket transmission."""
        return {
            'use_force_sensor': self.use_force_sensor,
            'use_pressure_sensor': self.use_pressure_sensor,
            'com_port_pressure_sensor': self.com_port_pressure_sensor,
            'movement_algorithm': self.movement_algorithm,
            'dwell_time': self.dwell_time,
            'safe_height': self.safe_height,
            'default_speed_ratio': self.default_speed_ratio,
            'tuning_speed_ratio': self.tuning_speed_ratio,
            'tuning_interval': self.tuning_interval,
            'translation_threshold': self.translation_threshold,
            'rotation_threshold': self.rotation_threshold,
            'stop_robot_if_head_not_visible': self.stop_robot_if_head_not_visible,
            'wait_for_keypress_before_movement': self.wait_for_keypress_before_movement,
            'verbose': self.verbose,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RobotConfigState':
        """Create configuration from dictionary."""
        pid_trans = data.get('pid_translation', {})
        pid_rot = data.get('pid_rotation', {})
        
        return cls(
            use_force_sensor=data.get('use_force_sensor', False),
            use_pressure_sensor=data.get('use_pressure_sensor', False),
            com_port_pressure_sensor=data.get('com_port_pressure_sensor', ''),
            movement_algorithm=data.get('movement_algorithm', 'directly_PID'),
            dwell_time=data.get('dwell_time', 0.0),
            safe_height=data.get('safe_height', 750.0),
            default_speed_ratio=data.get('default_speed_ratio', 0.08),
            tuning_speed_ratio=data.get('tuning_speed_ratio', 0.1),
            tuning_interval=data.get('tuning_interval', 1.0),
            translation_threshold=data.get('translation_threshold', 20.0),
            rotation_threshold=data.get('rotation_threshold', 15.0),
            stop_robot_if_head_not_visible=data.get('stop_robot_if_head_not_visible', True),
            wait_for_keypress_before_movement=data.get('wait_for_keypress_before_movement', False),
            verbose=data.get('verbose', False),
        )
    
    def validate(self) -> Tuple[bool, str]:
        """Validate configuration values.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.movement_algorithm not in MOVEMENT_ALGORITHM_OPTIONS:
            return False, f"Invalid movement algorithm: {self.movement_algorithm}"
        
        if not (0.01 <= self.default_speed_ratio <= 1.0):
            return False, "Default speed ratio must be between 0.01 and 1.0"
        
        if not (0.01 <= self.tuning_speed_ratio <= 1.0):
            return False, "Tuning speed ratio must be between 0.01 and 1.0"
        
        if self.safe_height < 0:
            return False, "Safe height must be positive"
        
        if self.translation_threshold < 0:
            return False, "Translation threshold must be positive"
        
        if self.rotation_threshold < 0:
            return False, "Rotation threshold must be positive"
        
        return True, ""
    
    def sync_from_embedded(self, data: dict) -> None:
        """Synchronize state from embedded system (no validation)."""
        valid_fields = {f.name for f in fields(self)}

        for key, value in data.items():
            if key in valid_fields:
                setattr(self, key, value)
