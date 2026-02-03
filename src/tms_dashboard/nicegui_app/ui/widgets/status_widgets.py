#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Status widgets panel - consolidates all status displays."""

from nicegui import ui
from tms_dashboard.core.dashboard_state import DashboardState


def create_status_widgets(dashboard: DashboardState):
    """Create consolidated status panel with all status sections.
    
    Contains:
    - Connection: Project, Robot, Camera
    - Markers: Head, Coil, Probe
    - Fiducials: Image & Tracker
    - Status: Target, Coil, Moving Robot
    - Indicators: Distance, Angle, Force
    
    Args:
        dashboard: DashboardState instance
    """
    # Status section - 2x2 grid (horizontal layout)
    with ui.column().style('margin-bottom: 5px;'):
        ui.label('Connection').style('font-size: 1.4rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
        
        with ui.row().style('gap: 2.5rem; flex: 1; align-items: center;'):
            with ui.row().style('gap: 5px;'):
                icon = ui.icon('computer').style('font-size: 22px; color: #9ca3af;')
                label = ui.label('Project').style('font-size: 1.0rem; color: #9ca3af;')
                dashboard.__dict__['icon_project'] = icon
                dashboard.__dict__['label_project'] = label
            with ui.row().style('gap: 5px;'):
                icon = ui.icon('precision_manufacturing').style('font-size: 22px; color: #9ca3af;')
                label = ui.label('Robot').style('font-size: 1.0rem; color: #9ca3af;')
                dashboard.__dict__['icon_robot'] = icon
                dashboard.__dict__['label_robot'] = label
            with ui.row().style('gap: 5px;'):
                icon = ui.icon('videocam').style('font-size: 22px; color: #9ca3af;')
                label = ui.label('Camera').style('font-size: 1.0rem; color: #9ca3af;')
                dashboard.__dict__['icon_camera'] = icon
                dashboard.__dict__['label_camera'] = label
            # with ui.row().style('gap: 5px;'):
            #     icon = ui.icon('offline_bolt').style('font-size: 22px; color: #9ca3af;')               aqui
            #     label = ui.label('TMS').style('font-size: 1.0rem; color: #9ca3af;')
            #     dashboard.__dict__['icon_tms'] = icon
            #     dashboard.__dict__['label_tms'] = label
    
    ui.separator().style('margin: 4px 0;')
    
    # Markers section - horizontal row
    with ui.column().style('margin-bottom: 5px;'):
        ui.label('Markers').style('font-size: 1.4rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
        
        with ui.row().style('gap: 2.5rem; width: 100%;'):
            for label_text, icon in [
                ('Head', 'face'),
                ('Coil', 'sensors'),
                ('Probe', 'sensors'),
            ]:
                with ui.row().style('gap: 4px;'):
                    icon = ui.icon(icon).style('font-size: 22px; color: #9ca3af;')
                    label = ui.label(label_text).style('font-size: 1.1rem; color: #9ca3af;')
                    dashboard.__dict__[f'icon_marker_{label_text.lower()}'] = icon
                    dashboard.__dict__[f'label_marker_{label_text.lower()}'] = label
    
    ui.separator().style('margin: 4px 0;')
    
    # Fiducials section - side by side (Image | Tracker)
    with ui.column().style('margin-bottom: 5px;'):
        ui.label('Fiducials').style('font-size: 1.4rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
        
        with ui.row().style('gap: 2.5rem;'):
            # Image fiducials (left column)
            with ui.column().style('gap: 1px;'):
                ui.label('Image').style('font-size: 1.3rem; color: #6B6B6B; margin-bottom: 1px;')
                for label_text, icon_name in [
                    ('L Fid', 'radio_button_unchecked'),
                    ('Nasion', 'radio_button_unchecked'),
                    ('R Fid', 'radio_button_unchecked'),
                ]:
                    with ui.row().classes('items-center').style('gap: 2px;'):
                        icon = ui.icon(icon_name).style('font-size: 15px; color: #9ca3af;')
                        label = ui.label(label_text).style('font-size: 1rem; color: #9ca3af;')
                        dashboard.__dict__[f'icon_{label_text.lower().replace(" ", "_")}'] = icon
                        dashboard.__dict__[f'label_{label_text.lower().replace(" ", "_")}'] = label
            
            # Tracker fiducials (right column)
            with ui.column().style('gap: 1px;'):
                ui.label('Tracker').style('font-size: 1.3rem; color: #6B6B6B; margin-bottom: 1px;')
                for label_text, icon_name in [
                    ('L Tragus', 'radio_button_unchecked'),
                    ('Nose', 'radio_button_unchecked'),
                    ('R Tragus', 'radio_button_unchecked'),
                ]:
                    with ui.row().classes('items-center').style('gap: 2px;'):
                        icon = ui.icon(icon_name).style('font-size: 15px; color: #9ca3af;')
                        label = ui.label(label_text).style('font-size: 1rem; color: #9ca3af;')
                        dashboard.__dict__[f'icon_{label_text.lower().replace(" ", "_")}'] = icon
                        dashboard.__dict__[f'label_{label_text.lower().replace(" ", "_")}'] = label
    
    ui.separator().style('margin: 4px 0;')
    
    # Robot section - 2x2 grid
    with ui.column().style('gap: 1px;'):
        ui.label('Status').style('font-size: 1.4rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
        
        with ui.row().style('gap: 2.5rem; margin-bottom: 2px; width: 100%;'):
            with ui.row().style('gap: 3px;'):
                icon = ui.icon('gps_fixed').style('font-size: 22px; color: #9ca3af;')
                label = ui.label('Target').style(f'font-size: 1.0rem; color: #9ca3af;')
                dashboard.__dict__['icon_target'] = icon
                dashboard.__dict__['label_target'] = label
            
            with ui.row().style('gap: 3px;'):
                icon = ui.icon('radar').style('font-size: 22px; color: #9ca3af;')
                label = ui.label('Coil at target').style('font-size: 1.0rem; color: #9ca3af;')
                dashboard.__dict__['icon_coil'] = icon
                dashboard.__dict__['label_coil'] = label
        
            with ui.row().style('gap: 3px;'):
                icon = ui.icon('sync').style('font-size: 22px; color: #9ca3af;')
                label = ui.label('Moving Robot').style('font-size: 1.0rem; color: #9ca3af;')
                dashboard.__dict__['icon_moving'] = icon
                dashboard.__dict__['label_moving'] = label
            
            # with ui.row().style('gap: 3px;'):
            #     icon = ui.icon('dataset').style('font-size: 22px; color: #9ca3af;')
            #     label = ui.label('Trials').style('font-size: 1.0rem; color: #9ca3af;')
            #     dashboard.__dict__['icon_trials'] = icon
            #     dashboard.__dict__['label_trials'] = label
    
    ui.separator().style('margin: 4px 0;')
    
    # Indicators section - Distance, Angle, Force
    with ui.column().style('gap: 1px;'):
        ui.label('Indicators').style('font-size: 1.4rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
        with ui.row().style('gap: 2rem;'):
            # Distance
            with ui.row().style('gap: 2px; align-items: center;'):
                ui.label('Distance:').style('font-size: 0.9rem; color: #6B6B6B; font-weight: 600;')
                label = ui.label('0.0 mm').style('font-size: 1.1rem; color: #3b82f6; font-weight: 500;')
                dashboard.__dict__['label_distance'] = label
                       
            # Force Sensor
            with ui.row().style('gap: 2px; align-items: center;'):
                ui.label('Force Sensor:').style('font-size: 0.9rem; color: #6B6B6B; font-weight: 600;')
                label = ui.label('0.0 N').style('font-size: 1.1rem; color: #10b981; font-weight: 500;')
                dashboard.__dict__['label_force'] = label
    