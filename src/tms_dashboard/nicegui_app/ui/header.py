#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Header component for NiceGUI app - Alternative Modal Approach"""

from nicegui import ui

from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.core.robot_config_state import RobotConfigState
from tms_dashboard.config import IMAGES_DIR

from tms_dashboard.nicegui_app.ui.widgets.robot_dialog import open_robot_config
from tms_dashboard.nicegui_app.ui.experiment_form import create_experiment_form
from tms_dashboard.nicegui_app.ui.checklist_tab import create_checklist_tab

def create_header(dashboard: DashboardState, robot_config: RobotConfigState, message_emit=None):
    """Create clean minimal header with working experiment config dialog.
    
    Args:
        dashboard: DashboardState instance
    """
    
    # Header row
    with ui.row().classes('w-full items-center justify-between').style(
        'background-color: #ffffff;'
        'padding: 10px 32px;'
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
        
        # Right side: Experiment Description button and Checklist button (grouped)
        with ui.row().classes('items-center gap-2'):

            ui.button('Configure Robot', on_click=lambda: open_robot_config(robot_config, message_emit, dashboard), icon='settings').props('flat').style(
                'font-weight: 500; color: #6b7280;'
            )
            # Experiment Description opens the experiment form dialog (renamed from 'Configure Experiment')
            exp_btn = create_experiment_form(dashboard, button_label='Experiment Description', header_mode=True)
            exp_btn.style('min-height: 40px; padding: 6px 14px; display: inline-flex; align-items: center;')

            # Checklist button: opens the checklist in a modal dialog (reuses create_checklist_tab)
            def show_checklist_dialog():
                with ui.dialog() as dialog, ui.card().style('min-width: 480px; max-width: 900px; max-height: 85vh;'):
                    # Dialog header
                    with ui.row().classes('w-full items-center justify-between mb-4'):
                        ui.label('Experiment Checklist').style(
                            'font-size: 1.25rem; font-weight: 600; color: #111827;'
                        )
                        ui.button(icon='close', on_click=dialog.close).props('flat round dense')

                    ui.separator()

                    with ui.column().classes('w-full'):
                        create_checklist_tab(dashboard)

                    # Footer actions
                    with ui.row().classes('w-full justify-end gap-2 mt-4'):
                        ui.button('Close', on_click=dialog.close).props('outline')

                dialog.open()

            checklist_btn = ui.button('Checklist', on_click=show_checklist_dialog, icon='checklist').props('flat')
            checklist_btn.style('min-height: 40px; padding: 6px 12px; display: inline-flex; align-items: center; margin-left: 8px;')
