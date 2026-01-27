#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Header component for NiceGUI app - Alternative Modal Approach"""

from nicegui import ui
from tms_dashboard.config import IMAGES_DIR, CSV_PATH
from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.core.data_logger import DataLogger


def create_header(dashboard: DashboardState):
    """Create clean minimal header with working experiment config dialog.
    
    Args:
        dashboard: DashboardState instance
    """
    logger = DataLogger(CSV_PATH)
    
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
        
        # Right side: Config button
        async def open_config():
            """Open configuration dialog."""
            with ui.dialog().props('persistent') as dialog:
                with ui.card().style('min-width: 600px; max-width: 800px;'):
                    # Dialog header
                    with ui.row().classes('w-full items-center justify-between mb-4'):
                        ui.label('Experiment Configuration').style(
                            'font-size: 1.25rem; font-weight: 600; color: #111827;'
                        )
                        ui.button(icon='close', on_click=dialog.close).props('flat round dense')
                    
                    ui.separator()
                    
                    # Form fields in a grid
                    with ui.grid(columns=2).classes('w-full gap-4 mt-4'):
                        # Left column
                        with ui.column().classes('gap-3'):
                            ui.label('Basic Information').style('font-weight: 600; font-size: 0.9375rem;')
                            name_input = ui.input('Experiment Name', value=dashboard.experiment_name).classes('w-full').props('outlined dense')
                            desc_input = ui.textarea('Description', value=dashboard.experiment_description).classes('w-full').props('outlined dense rows=3')
                        
                        # Right column  
                        with ui.column().classes('gap-3'):
                            ui.label('Timeline').style('font-weight: 600; font-size: 0.9375rem;')
                            start_input = ui.input('Start Date', value=dashboard.start_date).classes('w-full').props('outlined dense type=date')
                            end_input = ui.input('End Date', value=dashboard.end_date).classes('w-full').props('outlined dense type=date')
                    
                    # Details (full width)
                    details_input = ui.textarea('Details', value=dashboard.experiment_details).classes('w-full mt-3').props('outlined dense rows=3')
                    
                    def save_data():
                        """Save experiment data to CSV."""
                        data = DataLogger.create_experiment_dict(
                            experiment_name=name_input.value,
                            experiment_description=desc_input.value,
                            start_date=start_input.value,
                            end_date=end_input.value,
                            experiment_details=details_input.value
                        )
                        if logger.save_experiment_data(data):
                            ui.notify('Data saved successfully', type='positive', position='top')
                            dialog.close()
                        else:
                            ui.notify('Error saving data', type='negative', position='top')
                    
                    # Action buttons
                    with ui.row().classes('w-full justify-end gap-2 mt-4'):
                        ui.button('Cancel', on_click=dialog.close).props('outline')
                        ui.button('Save', on_click=save_data, icon='save').props('color=primary')
            
            await dialog
        
        ui.button('Configure Experiment', on_click=open_config, icon='settings').props('flat').style(
            'font-weight: 500; color: #6b7280;'
        )
