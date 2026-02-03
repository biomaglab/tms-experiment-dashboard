#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Header component for NiceGUI app - Alternative Modal Approach"""

from nicegui import ui

from tms_dashboard.nicegui_app.ui.widgets.exp_logger_dialog import open_config
from tms_dashboard.nicegui_app.ui.widgets.robot_dialog import open_robot_config
from tms_dashboard.config import IMAGES_DIR
from tms_dashboard.core.dashboard_state import DashboardState

def create_header(dashboard: DashboardState, message_emit=None):
    """Create clean minimal header with working experiment config dialog.
    
    Args:
        dashboard: DashboardState instance
        message_emit: Message2Server instance for sending config to robot
    """
    
    # Header row
    with ui.row().classes('w-full items-center justify-between').style(
        'background-color: #ffffff;'
        'padding: 16px 32px;'
        'border-bottom: 1px solid #e5e7eb;'
        'box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);'
    ):
        # Left side: Logo + Title
        with ui.row().classes('items-center gap-4'):
            ui.image(str(IMAGES_DIR / 'biomag_logo.jpg')).classes('rounded').style(
                'width: 45px; height: 45px; object-fit: cover;'
            )
            ui.label('Biomag TMS Dashboard').style(
                'font-size: 1.5rem; font-weight: 600; color: #111827;'
                'letter-spacing: -0.025em;'
            )
        
        with ui.row().style(
            'gap: 5px;'
        ):

            ui.button('Configure Robot', on_click=lambda: open_robot_config(dashboard, message_emit), icon='settings').props('flat').style(
                'font-weight: 500; color: #6b7280;'
            )
            
            ui.button('Configure Experiment', on_click=lambda: open_config(dashboard), icon='settings').props('flat').style(
                'font-weight: 500; color: #6b7280;'
            )

