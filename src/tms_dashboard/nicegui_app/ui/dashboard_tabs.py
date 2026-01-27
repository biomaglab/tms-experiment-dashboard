#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard tabs component - 2x2 grid layout with time series graph"""

from nicegui import ui
from tms_dashboard.core.dashboard_state import DashboardState
from .widgets import (
    create_status_widgets,
    create_time_series_panel,
    create_navigation_controls,
    create_3d_scene_with_models,

)


def create_dashboard_tabs(dashboard: DashboardState):
    """Create 2x2 grid dashboard layout.
    
    Layout (no scrolling):
    Row 1 (65%): 3D Navigation (60%) | Status Items (40%)
    Row 2 (35%): Time Series Graph (60%) | Navigation Controls (40%)
    
    Args:
        dashboard: DashboardState instance
    """
    # Main container - 2 rows
    with ui.column().classes('w-full').style(
        'height: calc(100vh - 110px); '
        'overflow: hidden; '
        'gap: 0;'
    ):
        
        # ===== ROW 1 (65% height): 3D Navigation + Status Items =====
        with ui.row().classes('w-full').style(
            'flex: 65; '
            'min-height: 0; '
            'align-items: stretch; '
            'gap: 0;'
        ):
            # 3D Navigation (60% width)
            with ui.card().props('flat').style(
                'flex: 60; '
                'padding: 12px; '
                'display: flex; '
                'flex-direction: column; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb;'
            ):
                ui.label('3D Navigation').style('font-size: 1.1rem; font-weight: 600; margin-bottom: 8px;')
                
                with ui.column().classes('w-full').style('flex: 1; min-height: 0;'):
                    create_3d_scene_with_models(dashboard)
            
            # Status Items (40% width)
            with ui.card().props('flat').style(
                'flex: 40; '
                'padding: 8px; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb; '
                'display: flex; '
                'flex-direction: column;'
            ):
                create_status_widgets(dashboard)
        
        # ===== ROW 2 (35% height): Time Series Graph + Navigation Controls =====
        with ui.row().classes('w-full').style(
            'flex: 35; '
            'min-height: 0; '
            'align-items: stretch; '
            'gap: 0;'
        ):
            # Time Series Graph (60% width)
            with ui.card().props('flat').style(
                'flex: 60; '
                'padding: 12px; '
                'display: flex; '
                'flex-direction: row; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb;'
            ):
                create_time_series_panel(dashboard)
            
            # Navigation Controls (40% width)
            with ui.card().props('flat').style(
                'flex: 40; '
                'padding: 12px; '
                'display: flex; '
                'flex-direction: row; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb;'
                'gap: 1.5rem;'
            ):
                create_navigation_controls(dashboard)
