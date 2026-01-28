#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Experiment form component for NiceGUI app - Modal Dialog"""

from nicegui import ui
from pathlib import Path
from ...core.dashboard_state import DashboardState
from ...core.data_logger import DataLogger
from ...config import CSV_PATH


def create_experiment_form(dashboard: DashboardState):
    """Create experiment details button that opens a modal dialog.
    
    Args:
        dashboard: DashboardState instance
    """
    # Store selected folder path
    selected_folder = {'path': str(CSV_PATH.parent)}
    
    def show_experiment_dialog():
        """Show experiment details dialog with tabbed interface."""
        with ui.dialog() as dialog, ui.card().style('min-width: 800px; max-width: 1000px; max-height: 85vh;'):
            # Dialog header
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label('Experiment Configuration').style(
                    'font-size: 1.25rem; font-weight: 600; color: #111827;'
                )
                ui.button(icon='close', on_click=dialog.close).props('flat round dense')
            
            ui.separator()
            
            # Save location section
            with ui.row().classes('w-full items-center gap-2 mb-4'):
                ui.label('Save Location:').style('font-weight: 500;')
                folder_input = ui.input(value=selected_folder['path']).classes('flex-1').props('outlined dense')
                folder_input.on_value_change(lambda e: selected_folder.update({'path': e.value}))
                
                def validate_and_update():
                    path = Path(folder_input.value)
                    if path.exists() and path.is_dir():
                        selected_folder['path'] = str(path)
                        ui.notify(f'Path set to: {path}', type='info', position='top')
                    else:
                        ui.notify(f'Invalid path: {folder_input.value}', type='warning', position='top')
                
                ui.button('Update', on_click=validate_and_update).props('outline dense')
            
            # Create tabs
            with ui.tabs().classes('w-full') as tabs:
                tab1 = ui.tab('Basic Information')
                tab2 = ui.tab('Stimulation Parameters')
                tab3 = ui.tab('Technical Details')
            
            with ui.tab_panels(tabs).classes('w-full'):
                # ==================== TAB 1: Basic Information ====================
                with ui.tab_panel(tab1):
                    with ui.column().classes('w-full gap-3 p-4'):
                        ui.label('Basic Information').style('font-weight: 600; font-size: 1rem;')
                        
                        name_input = ui.input('Experiment Name', value=dashboard.experiment_name).classes('w-full').props('outlined dense')
                        
                        ui.label('Start Date and Time').style('font-weight: 500; font-size: 0.9rem; margin-top: 8px;')
                        datetime_input = ui.input('Date and Time', value=dashboard.start_datetime).classes('w-full').props('outlined dense type=datetime-local')
                        
                        desc_input = ui.textarea('General Description', value=dashboard.experiment_description).classes('w-full').props('outlined dense rows=3')
                        
                        objective_input = ui.textarea('Experiment Objective', value=dashboard.experiment_objective).classes('w-full').props('outlined dense rows=2')
                        
                        protocol_input = ui.textarea('Experimental Protocol Description', value=dashboard.protocol_description).classes('w-full').props('outlined dense rows=3')
                
                # ==================== TAB 2: Stimulation Parameters ====================
                with ui.tab_panel(tab2):
                    with ui.column().classes('w-full gap-3 p-4 overflow-y-auto'):
                        ui.label('Stimulation Parameters').style('font-weight: 600; font-size: 1rem;')
                        
                        with ui.grid(columns=2).classes('w-full gap-3'):
                            intensity_input = ui.input('Stimulus Intensity (e.g., 120% RMT)', value=dashboard.stimulus_intensity).classes('w-full').props('outlined dense')
                            isi_input = ui.input('ISI - Interstimulus Interval (ms)', value=dashboard.isi_value).classes('w-full').props('outlined dense')
                            
                            pulses_input = ui.input('Number of Pulses', value=dashboard.number_pulses).classes('w-full').props('outlined dense')
                            frequency_input = ui.input('Stimulation Frequency (Hz)', value=dashboard.stimulation_frequency).classes('w-full').props('outlined dense')
                            
                            duration_input = ui.input('Stimulation Duration (minutes)', value=dashboard.stimulation_duration).classes('w-full').props('outlined dense')
                
                # ==================== TAB 3: Technical Details ====================
                with ui.tab_panel(tab3):
                    with ui.column().classes('w-full gap-4 p-4 overflow-y-auto'):
                        
                        # TMS Equipment Section
                        ui.label('TMS Equipment').style('font-weight: 600; font-size: 0.95rem; margin-top: 8px;')
                        with ui.grid(columns=2).classes('w-full gap-3'):
                            tms_brand_input = ui.input('TMS Brand', value=dashboard.tms_equipment_brand).classes('w-full').props('outlined dense')
                            tms_model_input = ui.input('TMS Model', value=dashboard.tms_equipment_model).classes('w-full').props('outlined dense')
                            
                            coil_type_input = ui.input('Coil Type (e.g., figure-of-8, circular)', value=dashboard.coil_type).classes('w-full').props('outlined dense')
                            coil_orientation_input = ui.input('Coil Orientation', value=dashboard.coil_orientation).classes('w-full').props('outlined dense')
                            
                            coil_position_input = ui.input('Scalp Position', value=dashboard.coil_position).classes('w-full').props('outlined dense')
                        
                        # EMG Equipment Section
                        ui.label('Electromyograph (EMG)').style('font-weight: 600; font-size: 0.95rem; margin-top: 12px;')
                        with ui.grid(columns=2).classes('w-full gap-3'):
                            emg_model_input = ui.input('EMG Model', value=dashboard.emg_equipment_model).classes('w-full').props('outlined dense')
                            
                            sampling_input = ui.input('Sampling Rate (Hz)', value=dashboard.emg_sampling_rate).classes('w-full').props('outlined dense')
                            muscle_input = ui.input('Recorded Muscle', value=dashboard.muscle_recorded).classes('w-full').props('outlined dense')
                            electrode_input = ui.input('Electrode Positioning', value=dashboard.electrode_position).classes('w-full').props('outlined dense')
            
            def save_data():
                """Save experiment data to CSV in selected folder."""
                data = {
                    'experiment_name': name_input.value,
                    'experiment_description': desc_input.value,
                    'start_datetime': datetime_input.value,
                    'experiment_objective': objective_input.value,
                    'protocol_description': protocol_input.value,
                    'stimulus_intensity': intensity_input.value,
                    'isi_value': isi_input.value,
                    'number_pulses': pulses_input.value,
                    'stimulation_frequency': frequency_input.value,
                    'stimulation_duration': duration_input.value,
                    'tms_equipment_brand': tms_brand_input.value,
                    'tms_equipment_model': tms_model_input.value,
                    'coil_type': coil_type_input.value,
                    'coil_orientation': coil_orientation_input.value,
                    'coil_position': coil_position_input.value,
                    'emg_equipment_model': emg_model_input.value,
                    'emg_sampling_rate': sampling_input.value,
                    'muscle_recorded': muscle_input.value,
                    'electrode_position': electrode_input.value
                }
                
                # Update dashboard state
                dashboard.experiment_name = name_input.value
                dashboard.experiment_description = desc_input.value
                dashboard.start_datetime = datetime_input.value
                dashboard.experiment_objective = objective_input.value
                dashboard.protocol_description = protocol_input.value
                dashboard.stimulus_intensity = intensity_input.value
                dashboard.isi_value = isi_input.value
                dashboard.number_pulses = pulses_input.value
                dashboard.stimulation_frequency = frequency_input.value
                dashboard.stimulation_duration = duration_input.value
                dashboard.tms_equipment_brand = tms_brand_input.value
                dashboard.tms_equipment_model = tms_model_input.value
                dashboard.coil_type = coil_type_input.value
                dashboard.coil_orientation = coil_orientation_input.value
                dashboard.coil_position = coil_position_input.value
                dashboard.emg_equipment_model = emg_model_input.value
                dashboard.emg_sampling_rate = sampling_input.value
                dashboard.muscle_recorded = muscle_input.value
                dashboard.electrode_position = electrode_input.value
                
                # Create logger with selected folder
                csv_file_path = Path(selected_folder['path']) / 'experiment_details.csv'
                logger = DataLogger(csv_file_path)
                
                if logger.save_experiment_data(data):
                    ui.notify(f'Data saved to: {csv_file_path}', type='positive', position='top')
                    dialog.close()
                else:
                    ui.notify('Error saving data', type='negative', position='top')
            
            # Action buttons
            with ui.row().classes('w-full justify-end gap-2 mt-4'):
                ui.button('Cancel', on_click=dialog.close).props('outline')
                ui.button('Save', on_click=save_data, icon='save').props('color=primary')
        
        dialog.open()
    
    # Simple button to open dialog
    ui.button('Configure Experiment', on_click=show_experiment_dialog, icon='settings').props('outline').style(
        'margin-bottom: 16px;'
    )
