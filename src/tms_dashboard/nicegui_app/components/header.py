#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Header component for NiceGUI app - Alternative Modal Approach"""

from nicegui import ui
from ...config import IMAGES_DIR
from ...core.dashboard_state import DashboardState
from .experiment_form import create_experiment_form


def create_header(dashboard: DashboardState):
    """Create clean minimal header with working experiment config dialog.
    
    Args:
        dashboard: DashboardState instance
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
                'width: 40px; height: 40px; object-fit: cover;'
            )
            ui.label('Biomag TMS Dashboard').style(
                'font-size: 1.5rem; font-weight: 600; color: #111827;'
                'letter-spacing: -0.025em;'
            )
        
        # Right side: Config button - use the experiment_form component
        create_experiment_form(dashboard)
