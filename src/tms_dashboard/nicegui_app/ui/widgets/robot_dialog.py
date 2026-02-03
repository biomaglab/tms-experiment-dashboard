#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Robot configuration dialog widget."""

from nicegui import ui
from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.core.robot_config_state import (
    RobotConfigState, 
    PIDParams,
    SITE_OPTIONS, 
    ROBOT_OPTIONS, 
    MOVEMENT_ALGORITHM_OPTIONS
)


# Global robot config instance
robot_config = RobotConfigState()


async def open_robot_config(dashboard: DashboardState, message_emit=None):
    """Open robot configuration dialog.
    
    Args:
        dashboard: DashboardState instance
        message_emit: Message2Server instance for sending config to neuronavigation
    """
    global robot_config
    
    with ui.dialog().props('persistent maximized') as dialog:
        with ui.card().style('width: 900px; max-width: 95vw; max-height: 90vh; overflow-y: auto;'):
            # Dialog header
            with ui.row().classes('w-full items-center justify-between mb-2 sticky top-0 bg-white z-10 pb-2'):
                ui.label('Robot Configuration').style(
                    'font-size: 1.5rem; font-weight: 700; color: #111827;'
                )
                ui.button(icon='close', on_click=dialog.close).props('flat round dense')
            
            ui.separator()
            
            # Store input references for saving
            inputs = {}
            
            # ===== SECTION 1: Site & Robot Selection =====
            with ui.expansion('Site & Robot', icon='precision_manufacturing', value=True).classes('w-full').style('margin-top: 8px;'):
                with ui.grid(columns=2).classes('w-full gap-4'):
                    inputs['site'] = ui.select(
                        label='Site', 
                        options=SITE_OPTIONS, 
                        value=robot_config.site
                    ).classes('w-full').props('outlined dense')
                    
                    inputs['robot'] = ui.select(
                        label='Robot Type', 
                        options=ROBOT_OPTIONS, 
                        value=robot_config.robot
                    ).classes('w-full').props('outlined dense')
            
            # ===== SECTION 2: Sensors =====
            with ui.expansion('Sensors', icon='sensors').classes('w-full'):
                with ui.grid(columns=3).classes('w-full gap-4 items-center'):
                    inputs['use_force_sensor'] = ui.switch(
                        'Use Force Sensor', 
                        value=robot_config.use_force_sensor
                    )
                    
                    inputs['use_pressure_sensor'] = ui.switch(
                        'Use Pressure Sensor', 
                        value=robot_config.use_pressure_sensor
                    )
                    
                    inputs['com_port_pressure_sensor'] = ui.input(
                        label='COM Port', 
                        value=robot_config.com_port_pressure_sensor,
                        placeholder='e.g., COM1 or /dev/ttyUSB0'
                    ).classes('w-full').props('outlined dense')
            
            # ===== SECTION 3: Movement Algorithm =====
            with ui.expansion('Movement Settings', icon='route', value=True).classes('w-full'):
                with ui.grid(columns=3).classes('w-full gap-4'):
                    inputs['movement_algorithm'] = ui.select(
                        label='Movement Algorithm', 
                        options=MOVEMENT_ALGORITHM_OPTIONS, 
                        value=robot_config.movement_algorithm
                    ).classes('w-full').props('outlined dense')
                    
                    inputs['dwell_time'] = ui.number(
                        label='Dwell Time (s)', 
                        value=robot_config.dwell_time,
                        min=0, max=10, step=0.1,
                        format='%.1f'
                    ).classes('w-full').props('outlined dense')
                    
                    inputs['safe_height'] = ui.number(
                        label='Safe Height (mm)', 
                        value=robot_config.safe_height,
                        min=0, max=2000, step=10,
                        format='%.0f'
                    ).classes('w-full').props('outlined dense')
            
            # ===== SECTION 4: Speed Settings =====
            with ui.expansion('Speed & Timing', icon='speed', value=True).classes('w-full'):
                with ui.grid(columns=3).classes('w-full gap-4'):
                    inputs['default_speed_ratio'] = ui.number(
                        label='Default Speed Ratio', 
                        value=robot_config.default_speed_ratio,
                        min=0.01, max=1.0, step=0.01,
                        format='%.2f'
                    ).classes('w-full').props('outlined dense')
                    
                    inputs['tuning_speed_ratio'] = ui.number(
                        label='Tuning Speed Ratio', 
                        value=robot_config.tuning_speed_ratio,
                        min=0.01, max=1.0, step=0.01,
                        format='%.2f'
                    ).classes('w-full').props('outlined dense')
                    
                    inputs['tuning_interval'] = ui.number(
                        label='Tuning Interval (s)', 
                        value=robot_config.tuning_interval,
                        min=0, max=10, step=0.1,
                        format='%.1f'
                    ).classes('w-full').props('outlined dense')
            
            # ===== SECTION 5: Thresholds =====
            with ui.expansion('Thresholds', icon='straighten', value=True).classes('w-full'):
                with ui.grid(columns=2).classes('w-full gap-4'):
                    inputs['translation_threshold'] = ui.number(
                        label='Translation Threshold (mm)', 
                        value=robot_config.translation_threshold,
                        min=1, max=100, step=1,
                        format='%.0f'
                    ).classes('w-full').props('outlined dense')
                    
                    inputs['rotation_threshold'] = ui.number(
                        label='Rotation Threshold (°)', 
                        value=robot_config.rotation_threshold,
                        min=1, max=90, step=1,
                        format='%.0f'
                    ).classes('w-full').props('outlined dense')
            
            # ===== SECTION 6: PID Tuning =====
            with ui.expansion('PID Tuning', icon='tune', value=False).classes('w-full'):
                # Position PID (X, Y, Z)
                ui.label('Position Control').style('font-weight: 600; font-size: 0.95rem; margin-bottom: 8px;')
                
                pid_inputs = {}
                
                with ui.grid(columns=4).classes('w-full gap-2 mb-4'):
                    ui.label('Axis').style('font-weight: 600; color: #6b7280;')
                    ui.label('Kp').style('font-weight: 600; color: #6b7280;')
                    ui.label('Ki').style('font-weight: 600; color: #6b7280;')
                    ui.label('Kd').style('font-weight: 600; color: #6b7280;')
                    
                    for axis, pid in [('X', robot_config.pid_x), ('Y', robot_config.pid_y), ('Z', robot_config.pid_z)]:
                        ui.label(axis).style('font-weight: 600; color: #10b981; align-self: center;')
                        pid_inputs[f'{axis.lower()}_kp'] = ui.number(value=pid.kp, min=0, max=100, step=0.1, format='%.2f').props('outlined dense').classes('w-full')
                        pid_inputs[f'{axis.lower()}_ki'] = ui.number(value=pid.ki, min=0, max=100, step=0.01, format='%.3f').props('outlined dense').classes('w-full')
                        pid_inputs[f'{axis.lower()}_kd'] = ui.number(value=pid.kd, min=0, max=100, step=0.01, format='%.3f').props('outlined dense').classes('w-full')
                
                ui.separator().classes('my-2')
                
                # Rotation PID (RX, RY, RZ)
                ui.label('Rotation Control').style('font-weight: 600; font-size: 0.95rem; margin-bottom: 8px;')
                
                with ui.grid(columns=4).classes('w-full gap-2'):
                    ui.label('Axis').style('font-weight: 600; color: #6b7280;')
                    ui.label('Kp').style('font-weight: 600; color: #6b7280;')
                    ui.label('Ki').style('font-weight: 600; color: #6b7280;')
                    ui.label('Kd').style('font-weight: 600; color: #6b7280;')
                    
                    for axis, pid in [('RX', robot_config.pid_rx), ('RY', robot_config.pid_ry), ('RZ', robot_config.pid_rz)]:
                        ui.label(axis).style('font-weight: 600; color: #f59e0b; align-self: center;')
                        pid_inputs[f'{axis.lower()}_kp'] = ui.number(value=pid.kp, min=0, max=100, step=0.1, format='%.2f').props('outlined dense').classes('w-full')
                        pid_inputs[f'{axis.lower()}_ki'] = ui.number(value=pid.ki, min=0, max=100, step=0.01, format='%.3f').props('outlined dense').classes('w-full')
                        pid_inputs[f'{axis.lower()}_kd'] = ui.number(value=pid.kd, min=0, max=100, step=0.01, format='%.3f').props('outlined dense').classes('w-full')
                
                inputs['pid'] = pid_inputs
            
            # ===== SECTION 7: Safety & Debug =====
            with ui.expansion('Safety & Debug', icon='bug_report').classes('w-full'):
                with ui.column().classes('w-full gap-2'):
                    inputs['stop_robot_if_head_not_visible'] = ui.switch(
                        'Stop Robot if Head Not Visible', 
                        value=robot_config.stop_robot_if_head_not_visible
                    )
                    
                    inputs['wait_for_keypress_before_movement'] = ui.switch(
                        'Wait for Keypress Before Movement (Debug)', 
                        value=robot_config.wait_for_keypress_before_movement
                    )
                    
                    inputs['verbose'] = ui.switch(
                        'Verbose Logging', 
                        value=robot_config.verbose
                    )
            
            ui.separator().classes('my-2')
            
            # ===== Action Buttons =====
            def save_config():
                """Save configuration and optionally send to neuronavigation."""
                global robot_config
                
                # Update robot_config from inputs
                robot_config.site = inputs['site'].value
                robot_config.robot = inputs['robot'].value
                robot_config.use_force_sensor = inputs['use_force_sensor'].value
                robot_config.use_pressure_sensor = inputs['use_pressure_sensor'].value
                robot_config.com_port_pressure_sensor = inputs['com_port_pressure_sensor'].value
                robot_config.movement_algorithm = inputs['movement_algorithm'].value
                robot_config.dwell_time = inputs['dwell_time'].value
                robot_config.safe_height = inputs['safe_height'].value
                robot_config.default_speed_ratio = inputs['default_speed_ratio'].value
                robot_config.tuning_speed_ratio = inputs['tuning_speed_ratio'].value
                robot_config.tuning_interval = inputs['tuning_interval'].value
                robot_config.translation_threshold = inputs['translation_threshold'].value
                robot_config.rotation_threshold = inputs['rotation_threshold'].value
                robot_config.stop_robot_if_head_not_visible = inputs['stop_robot_if_head_not_visible'].value
                robot_config.wait_for_keypress_before_movement = inputs['wait_for_keypress_before_movement'].value
                robot_config.verbose = inputs['verbose'].value
                
                # Update PID params
                pid = inputs['pid']
                robot_config.pid_x = PIDParams(kp=pid['x_kp'].value, ki=pid['x_ki'].value, kd=pid['x_kd'].value)
                robot_config.pid_y = PIDParams(kp=pid['y_kp'].value, ki=pid['y_ki'].value, kd=pid['y_kd'].value)
                robot_config.pid_z = PIDParams(kp=pid['z_kp'].value, ki=pid['z_ki'].value, kd=pid['z_kd'].value)
                robot_config.pid_rx = PIDParams(kp=pid['rx_kp'].value, ki=pid['rx_ki'].value, kd=pid['rx_kd'].value)
                robot_config.pid_ry = PIDParams(kp=pid['ry_kp'].value, ki=pid['ry_ki'].value, kd=pid['ry_kd'].value)
                robot_config.pid_rz = PIDParams(kp=pid['rz_kp'].value, ki=pid['rz_ki'].value, kd=pid['rz_kd'].value)
                
                # Validate
                is_valid, error_msg = robot_config.validate()
                if not is_valid:
                    ui.notify(f'Validation error: {error_msg}', type='negative', position='top')
                    return
                
                # Send to neuronavigation if message_emit available
                if message_emit is not None:
                    success = message_emit.send_robot_config(robot_config)
                    if success:
                        ui.notify('Configuration saved and sent to robot', type='positive', position='top')
                    else:
                        ui.notify('Configuration saved but failed to send', type='warning', position='top')
                else:
                    ui.notify('Configuration saved locally', type='positive', position='top')
                
                dialog.close()
            
            with ui.row().classes('w-full justify-end gap-2 sticky bottom-0 bg-white pt-2'):
                ui.button('Cancel', on_click=dialog.close).props('outline')
                ui.button('Save & Apply', on_click=save_config, icon='save').props('color=primary')
    
    await dialog