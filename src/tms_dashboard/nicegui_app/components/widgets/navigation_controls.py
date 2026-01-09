#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Navigation controls widget."""

from nicegui import ui
from ....core.dashboard_state import DashboardState


def create_navigation_controls(dashboard: DashboardState):
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
            ui.button('START NAVIGATION', icon='play_arrow').props('color=positive size=lg').classes('w-full').style(
                'font-size: 1rem; '
                'font-weight: 600; '
                'padding: 16px; '
                'min-height: 60px;'
            )
            
            ui.separator().style('margin: 4px 0;')
            
            # Create Target button
            ui.button('Create Target', icon='add_location_alt').props('outlined color=primary').classes('w-full').style(
                'font-size: 0.95rem; '
                'min-height: 50px;'
            )
    
    # Robot Control column
    with ui.column().style('gap: 5px; flex: 1; height: 100%;'):
        ui.label('Robot Control').style('font-size: 1rem; font-weight: 600; margin-bottom: 8px;')
        
        ui.button('Free Drive Robot', icon='gesture').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )

        ui.separator().style('margin: 4px 0;')
        
        ui.button('Active Robot', icon='settings_remote').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )
        
        ui.separator().style('margin: 4px 0;')

        ui.button('Move Upward Robot', icon='arrow_upward').props('flat outlined').classes('w-full').style(
            'font-size: 0.9rem; '
            'min-height: 50px;'
        )
