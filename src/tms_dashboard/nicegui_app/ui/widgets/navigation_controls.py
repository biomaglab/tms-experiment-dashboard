#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Navigation controls widget."""

from nicegui import ui
from tms_dashboard.core.dashboard_state import DashboardState


def create_navigation_controls(dashboard: DashboardState, message_emit):
    """Create navigation and robot control buttons.
    
    Contains two columns:
    - Navigation Controls: START NAVIGATION, Create Target
    - Robot Control: Free Drive, Active Robot, Move Upward
    
    Args:
        dashboard: DashboardState instance
    """
    # Navigation Controls column
    with ui.column().style('gap: 10px; flex: 1; height: 100%;'):
        with ui.column().classes('w-full').style('gap: 10px; flex: 1;'):
            ui.label('Navigation Controls').style('font-size: 1rem; font-weight: 600; margin-bottom: 8px;')
            
            # Main control button - Start/Stop (highlighted)
            nav_button = ui.button('NAVIGATION STATUS', icon='play_arrow').props('color=positive size=lg').classes('w-full').style(
                'font-size: 1rem; '
                'font-weight: 600; '
                'padding: 16px; '
                'min-height: 60px;'
            )
            # Save UI reference so the updater can change its color
            dashboard.__dict__['navigation_button'] = nav_button

            ui.separator().style('margin: 4px 0;')
            
            # Create Target button
            def _create_target_click(e=None):
                success = message_emit.create_marker()

                if success:
                    ui.notify('Create target sent', position='top')
                else:
                    ui.notify('Failed to send Create marker', position='top')

            ui.button('Create Target', icon='add_location_alt', on_click=_create_target_click).props('outlined color=primary').classes('w-full').style(
                'font-size: 0.95rem; '
                'min-height: 50px;'
            )
    
    # Robot Control column
    with ui.column().style('gap: 5px; flex: 1; height: 100%;'):
        ui.label('Robot Control').style('font-size: 1rem; font-weight: 600; margin-bottom: 8px;')

        def _free_drive_click(e=None):
            success = message_emit.free_drive_robot()

            if success:
                ui.notify('Create target sent', position='top')
            else:
                ui.notify('Failed to send Create marker', position='top')
        
        button = ui.button('Free Drive Robot', icon='gesture', on_click=_free_drive_click).props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )

        dashboard.__dict__["free_drive_button"] =  button

        ui.separator().style('margin: 4px 0;')

        def _active_robot_click(e=None):
            success = message_emit.active_robot()

            if success:
                ui.notify('Create target sent', position='top')
            else:
                ui.notify('Failed to send Create marker', position='top')
        
        button = ui.button('Active Robot', icon='settings_remote', on_click=_active_robot_click).props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )

        dashboard.__dict__["active_robot_button"] =  button
        
        ui.separator().style('margin: 4px 0;')

        def _upward_click(e=None):
            success = message_emit.move_upward_robot()

            if success:
                ui.notify('Create target sent', position='top')
            else:
                ui.notify('Failed to send Create marker', position='top')

        button = ui.button('Move Upward Robot', icon='arrow_upward', on_click=_upward_click).props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )

        dashboard.__dict__["upward_robot_button"] =  button
