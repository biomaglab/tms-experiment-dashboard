#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Robot configuration state management"""

from dataclasses import dataclass, field
from typing import Tuple

# Available options for select fields
SITE_OPTIONS = ['aalto', 'tubingen', 'usp_coil', 'usp_neurosoft', 'default']
ROBOT_OPTIONS = ['elfin', 'elfin_new_api', 'dobot', 'ur', 'test']
MOVEMENT_ALGORITHM_OPTIONS = ['radially_outward', 'directly_upward', 'directly_PID']


@dataclass
class PIDParams:
    """PID controller parameters for a single axis."""
    kp: float = 1.0
    ki: float = 0.0
    kd: float = 0.0
    
    def to_dict(self) -> dict:
        return {'kp': self.kp, 'ki': self.ki, 'kd': self.kd}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PIDParams':
        return cls(kp=data.get('kp', 1.0), ki=data.get('ki', 0.0), kd=data.get('kd', 0.0))


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
    
    # Site and robot selection
    site: str = 'usp_coil'
    robot: str = 'elfin'
    
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
    
    # PID parameters for position (X, Y, Z)
    pid_x: PIDParams = field(default_factory=PIDParams)
    pid_y: PIDParams = field(default_factory=PIDParams)
    pid_z: PIDParams = field(default_factory=PIDParams)
    
    # PID parameters for rotation (RX, RY, RZ)
    pid_rx: PIDParams = field(default_factory=PIDParams)
    pid_ry: PIDParams = field(default_factory=PIDParams)
    pid_rz: PIDParams = field(default_factory=PIDParams)
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary for serialization/socket transmission."""
        return {
            'site': self.site,
            'robot': self.robot,
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
            'pid_position': {
                'x': self.pid_x.to_dict(),
                'y': self.pid_y.to_dict(),
                'z': self.pid_z.to_dict(),
            },
            'pid_rotation': {
                'rx': self.pid_rx.to_dict(),
                'ry': self.pid_ry.to_dict(),
                'rz': self.pid_rz.to_dict(),
            }
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RobotConfigState':
        """Create configuration from dictionary."""
        pid_pos = data.get('pid_position', {})
        pid_rot = data.get('pid_rotation', {})
        
        return cls(
            site=data.get('site', 'usp_coil'),
            robot=data.get('robot', 'elfin'),
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
            pid_x=PIDParams.from_dict(pid_pos.get('x', {})),
            pid_y=PIDParams.from_dict(pid_pos.get('y', {})),
            pid_z=PIDParams.from_dict(pid_pos.get('z', {})),
            pid_rx=PIDParams.from_dict(pid_rot.get('rx', {})),
            pid_ry=PIDParams.from_dict(pid_rot.get('ry', {})),
            pid_rz=PIDParams.from_dict(pid_rot.get('rz', {})),
        )
    
    def validate(self) -> Tuple[bool, str]:
        """Validate configuration values.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.site not in SITE_OPTIONS:
            return False, f"Invalid site: {self.site}"
        
        if self.robot not in ROBOT_OPTIONS:
            return False, f"Invalid robot: {self.robot}"
        
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
