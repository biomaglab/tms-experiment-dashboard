#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard tabs component - 2x2 grid layout with time series graph"""

from nicegui import ui
from tms_dashboard.core.dashboard_state import DashboardState
from .widgets import (
    create_status_widgets,
    create_time_series_panel,
    create_mep_panel,
    create_navigation_controls,
    create_3d_scene_with_models,
)


from tms_dashboard.nicegui_app.ui_state import DashboardUI

def create_dashboard_tabs(dashboard: DashboardState, message_emit, ui_state: DashboardUI):
    """Create 2x2 grid dashboard layout.
    
    Layout (no scrolling):
    Row 1 (65%): 3D Navigation (60%) | Status Items (40%)
    Row 2 (35%): Time Series Graph (60%) | Navigation Controls (40%)
    
    Args:
        dashboard: DashboardState instance
        message_emit: Message emitter instance
        ui_state: DashboardUI instance (per-client UI state)
    """
    # Main container - 2 rows
    with ui.column().classes('w-full').style(
        'height: calc(100vh - 77px); '
        'overflow: hidden; '
        'gap: 0;'
    ):
        
        # ===== ROW 1 (50% height): MEP Graph + Status Items + Controls =====
        with ui.row().classes('w-full').style(
            'flex: 55; '
            'min-height: 0; '
            'align-items: stretch; '
            'gap: 0;'
        ):
            # 3D Navigation (60% width)
            with ui.card().props('flat').style(
                'flex: 45; '
                'padding: 8px; '
                'display: flex; '
                'flex-direction: column; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb;'
            ):
                create_mep_panel(ui_state)
                # ui.label('3D Navigation').style('font-size: 1.1rem; font-weight: 600; margin-bottom: 8px;')
                
                # with ui.column().classes('w-full').style('flex: 1; min-height: 0;'):
                #     create_3d_scene_with_models(dashboard)
            
            # Status Items (40% width)
            with ui.card().props('flat').style(
                'flex: 37; '
                'padding: 8px; '
                'overflow: auto; '
                'height: 100%; '
                'background-color: #f9fafb; '
                'display: flex; '
                'flex-direction: column;'
            ):
                create_status_widgets(ui_state)
            # Status Items (40% width)
            with ui.card().props('flat').style(
                'flex: 18; '
                'padding: 8px; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb; '
                'display: flex; '
                'flex-direction: column;'
            ):
                create_navigation_controls(message_emit, ui_state)
        
        # ===== ROW 2 (50% height): Time Series Graphs + 3D Scene =====
        with ui.row().classes('w-full').style(
            'flex: 45; '
            'min-height: 0; '
            'align-items: stretch; '
            'gap: 0;'
        ):
            # Time Series Graph (60% width)
            with ui.card().props('flat').style(
                'flex: 65; '
                'padding: 8px; '
                'display: flex; '
                'flex-direction: row; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb;'
            ):
                create_time_series_panel(ui_state)
            
            # Navigation Controls (40% width)
            with ui.card().props('flat').style(
                'flex: 35; '
                'padding: 8px 12px 8px 0px; '
                'display: flex; '
                'flex-direction: row; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb;'
                'gap: 1.5rem;'
            ):
                create_3d_scene_with_models(dashboard, message_emit)
