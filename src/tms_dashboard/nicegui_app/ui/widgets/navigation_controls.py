#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Navigation controls widget."""

from nicegui import ui
from tms_dashboard.core.dashboard_state import DashboardState
from src.tms_dashboard.utils.latency import now


from tms_dashboard.nicegui_app.ui_state import DashboardUI

def create_navigation_controls(message_emit, ui_state: DashboardUI):
    """Creates navigation and robot control buttons.
    
    Contains two columns:
    - Navigation Controls: START NAVIGATION, Create Target
    - Robot Control: Free Drive, Active Robot, Move Upward
    
    Args:
        dashboard: DashboardState instance
    """
    # Navigation Controls column
    with ui.column().style('gap: 10px; flex: 1; height: 100%; gap: 10px; flex: 1; width: 100%;'):
        ui.label('Navigation Controls').style('font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; color: #374151;')
        
        # Main control button - Start/Stop (highlighted)
        nav_button = ui.button('NAVIGATION STATUS', icon='play_arrow').props('color=positive size=lg').classes('w-full').style(
            'font-size: 1rem; '
            'font-weight: 600; '
            'padding: 16px; '
            'min-height: 60px;'
        )
        # Save UI reference so the updater can change its color
        ui_state.navigation_button = nav_button

        ui.separator().style('margin: 4px 0;')
        
        # Create Target button
        def _create_target_click(e):
            timestamp_ns = int(float(e.args['timeStamp']) * 1_000_000)
            message_emit.last_command_time_2 = timestamp_ns + ui_state.client_clock_offset_ns
            success = message_emit.create_marker()

            if success:
                ui.notify('Create target sent', position='top')
            else:
                ui.notify('Failed to send Create marker', position='top')

        ui.button('Create Target', icon='add_location_alt').props('outlined color=primary').classes('w-full').style(
            'font-size: 0.95rem; '
            'min-height: 50px;'
        ).on('click', _create_target_click, args=['timeStamp'])
    
    # Robot Control column
    with ui.column().style('gap: 5px; flex: 1; height: 100%; width: 100%;'):
        ui.label('Robot Control').style('font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; color: #374151;')

        def _free_drive_click(e):
            timestamp_ns = int(float(e.args['timeStamp']) * 1_000_000)
            message_emit.last_command_time_1 = timestamp_ns + ui_state.client_clock_offset_ns
            success = message_emit.free_drive_robot()

            if success:
                ui.notify('Free drive activated', position='top')
            else:
                ui.notify('Failed to activate free drive', position='top')
        
        button = ui.button('Free Drive Robot', icon='gesture').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        ).on('click', _free_drive_click, args=['timeStamp'])

        ui_state.free_drive_button =  button

        ui.separator().style('margin: 4px 0;')

        def _active_robot_click(e):
            timestamp_ns = int(float(e.args['timeStamp']) * 1_000_000)
            message_emit.last_command_time_1 = timestamp_ns + ui_state.client_clock_offset_ns
            success = message_emit.active_robot()

            if success:
                ui.notify('Create target sent', position='top')
            else:
                ui.notify('Failed to send Create marker', position='top')
        
        button = ui.button('Active Robot', icon='settings_remote').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        ).on('click', _active_robot_click, args=['timeStamp'])

        ui_state.active_robot_button =  button
        
        ui.separator().style('margin: 4px 0;')

        def _upward_click(e):
            timestamp_ns = int(float(e.args['timeStamp']) * 1_000_000)
            message_emit.last_command_time_1 = timestamp_ns + ui_state.client_clock_offset_ns
            success = message_emit.move_upward_robot()

            if success:
                ui.notify('Moving robot upward', position='top')
            else:
                ui.notify('Failed to move robot upward', position='top')

        button = ui.button('Move Upward Robot', icon='arrow_upward').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        ).on('click', _upward_click, args=['timeStamp'])

        ui_state.upward_robot_button =  button
