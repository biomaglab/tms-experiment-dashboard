#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Status widgets panel - consolidates all status displays."""

from nicegui import ui

from tms_dashboard.config import IMAGES_DIR
from tms_dashboard.core.dashboard_state import DashboardState
   

def create_status_widgets(dashboard: DashboardState):
    with ui.row().classes('w-full h-full').style('gap: 0;'):
        with ui.column().classes('h-full').style('flex: 30;align-items: center;'):
            image = ui.image(str(IMAGES_DIR / 'icones/stylus_icon.png')).classes('rounded').style(
                'width: 140px; height: 140px; object-fit: cover'
            )
            ui.label('Probe').style('font-size: 1.2rem; color: #9ca3af; font-weight: 500;')
            dashboard.__dict__['image_probe'] = image

            image = ui.image(str(IMAGES_DIR / 'icones/head_icon.png')).classes('rounded').style(
                'width: 140px; height: 140px; object-fit: cover;'
            )
            ui.label('Head').style('font-size: 1.2rem; color: #9ca3af; font-weight: 500;')
            dashboard.__dict__['image_head'] = image

            image = ui.image(str(IMAGES_DIR / 'icones/coil_no_handle_icon.png')).classes('rounded').style(
                'width: 140px; height: 140px; object-fit: cover;'
            )
            ui.label('Coil').style('font-size: 1.2rem; color: #9ca3af; font-weight: 500;')
            dashboard.__dict__['image_coil'] = image
        
        with ui.column().classes('h-full').style('flex: 70;'):
            with ui.row().classes('w-full').style('gap: 2px; flex: 15; flex-direction:column;'):
                ui.label('Connections').style('font-size: 1.1rem; font-weight: 600; color: #4b5563; margin-bottom: 5px;')

                with ui.row().style('gap: 2.5rem; flex: 1;'):
                    with ui.row().style('gap: 5px;'):
                        icon = ui.icon('computer').style('font-size: 22px; color: #9ca3af;')
                        label = ui.label('EMG').style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__['icon_emg'] = icon
                        dashboard.__dict__['label_emg'] = label
                    with ui.row().style('gap: 5px;'):
                        icon = ui.icon('precision_manufacturing').style('font-size: 22px; color: #9ca3af;')
                        label = ui.label('Robot').style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__['icon_robot'] = icon
                        dashboard.__dict__['label_robot'] = label
                    with ui.row().style('gap: 5px;'):
                        icon = ui.icon('videocam').style('font-size: 22px; color: #9ca3af;')
                        label = ui.label('Camera').style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__['icon_camera'] = icon
                        dashboard.__dict__['label_camera'] = label

            ui.separator()
            ui.label('Status').style('font-size: 1.1rem; font-weight: 600; color: #4b5563; margin-bottom: 5px;')
            with ui.row().classes('w-full').style('gap: 2px; flex: 70;'):
                with ui.column().classes('h-full').style('flex: 50; justify-content: center;'):
                    with ui.column().classes('w-full').style('gap: 2px; justify-content: center; align-items: center; flex: 1;'):
                        force = ui.circular_progress(size='80px',min=0, max=10, value=0).classes('force-progress').style('color: #9ca3af;')
                        dashboard.__dict__['force_indicator'] = force
                        ui.label('Force (N)').style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        ui.add_head_html("<style>.q-circular-progress__text .text-xs {font-size: 1.2rem}</style>")

                    with ui.column().classes('w-full').style('gap: 2px; justify-content: center; align-items: center; flex: 1;'):
                        icon = ui.icon('precision_manufacturing').style('font-size: 80px; color: #9ca3af;')
                        label = ui.label('Moving Robot').style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__['icon_moving'] = icon
                        dashboard.__dict__['label_moving'] = label

                with ui.column().classes('h-full').style('flex: 50; justify-content: center;'):
                    with ui.column().classes('w-full').style('gap: 2px; justify-content: center; align-items: center; flex: 1;'):
                        icon = ui.icon('radar').style('font-size: 80px; color: #9ca3af;')
                        label = ui.label('Coil at target').style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__['icon_coil'] = icon
                        dashboard.__dict__['label_coil'] = label
                    with ui.column().classes('w-full').style('gap: 2px; justify-content: center; align-items: center; flex: 1;'):
                        icon = ui.icon('gps_fixed').style('font-size: 80px; color: #9ca3af;')
                        label = ui.label('Target').style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__['icon_target'] = icon
                        dashboard.__dict__['label_target'] = label
            
            ui.separator()
            with ui.row().classes('w-full').style('gap: 2px; flex: 15; flex-direction:column;'):
                ui.label('Fiducials').style('font-size: 1.1rem; font-weight: 600; color: #4b5563; margin-bottom: 5px;')
                with ui.row().style('gap: 2.5rem; flex: 1;'):
                    with ui.row().style('gap: 5px; align-items: center;'):
                        label_text = "Image Fiducials"
                        icon = ui.icon('radio_button_unchecked').style('font-size: 15px; color: #9ca3af;')
                        label = ui.label(label_text).style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__[f'icon_{label_text.lower().replace(" ", "_")}'] = icon
                        dashboard.__dict__[f'label_{label_text.lower().replace(" ", "_")}'] = label
                    with ui.row().style('gap: 5px; align-items: center;'):
                        label_text = "Tracker Fiducials"
                        icon = ui.icon('radio_button_unchecked').style('font-size: 15px; color: #9ca3af;')
                        label = ui.label(label_text).style('font-size: 1.15rem; color: #9ca3af; font-weight: 500;')
                        dashboard.__dict__[f'icon_{label_text.lower().replace(" ", "_")}'] = icon
                        dashboard.__dict__[f'label_{label_text.lower().replace(" ", "_")}'] = label