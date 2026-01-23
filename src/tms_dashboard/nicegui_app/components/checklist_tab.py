#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checklist tab component for NiceGUI app"""

from nicegui import ui
from ...core.dashboard_state import DashboardState


def create_checklist_tab(dashboard: DashboardState):
    """Create the checklist tab content.
    
    Args:
        dashboard: DashboardState instance
    """
    with ui.column().classes('w-full p-4 gap-4'):
        ui.label('Experiment Checklist').style('font-size: 1.25rem; font-weight: 600;')
        
        # Display checklist items
        for item in dashboard.experiment_checklist:
            ui.label(f'• {item}').classes('w-full')