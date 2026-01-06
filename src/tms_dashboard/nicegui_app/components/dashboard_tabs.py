#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dashboard tabs component - 2x2 grid layout with time series graph"""

from nicegui import ui
from ...core.dashboard_state import DashboardState
from .navigation_3d import create_3d_scene_with_models


def create_dashboard_tabs(dashboard: DashboardState):
    """Create 2x2 grid dashboard layout.
    
    Layout (no scrolling):
    Row 1 (65%): 3D Navigation (70%) | Status Items (30%)
    Row 2 (35%): Time Series Graph (70%) | Navigation Controls (30%)
    
    Args:
        dashboard: DashboardState instance
    """
    # Main container - 2 rows
    with ui.column().classes('w-full').style(
        'height: calc(100vh - 110px); '
        'overflow: hidden; '
        'gap: 0;'
    ):
        
        # ROW 1 (60% height): 3D + Status
        with ui.row().classes('w-full').style(
            'flex: 65; '
            'min-height: 0; '
            'align-items: stretch; '
            'gap: 0;'
        ):
            # 3D Navigation (65%)
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
            
            # Status Items (35%) - NO SCROLLBAR, ultra compact
            with ui.card().props('flat').style(
                'flex: 40; '
                'padding: 8px; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb; '
                'display: flex; '
                'flex-direction: column;'
            ):
                # Status section - 2x2 grid (horizontal layout)
                with ui.column().style('margin-bottom: 5px;'):
                    ui.label('Status').style('font-size: 1.3rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
                    
                    with ui.row().style('gap: 2.5rem; flex: 1; align-items: center;'):
                        with ui.row().style('gap: 5px;'):
                            ui.icon('computer').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('Project').style('font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_project'] = label
                        with ui.row().style('gap: 5px;'):
                            ui.icon('precision_manufacturing').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('Robot').style('font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_robot'] = label
                        with ui.row().style('gap: 5px;'):
                            ui.icon('videocam').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('Camera').style('font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_camera'] = label
                        with ui.row().style('gap: 5px;'):
                            ui.icon('offline_bolt').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('TMS').style('font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_tms'] = label
                
                ui.separator().style('margin: 4px 0;')
                
                # Markers section - horizontal row
                with ui.column().style('margin-bottom: 5px;'):
                    ui.label('Markers').style('font-size: 1.3rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
                    
                    with ui.row().style('gap: 2.5rem; width: 100%;'):
                        for label_text, icon in [
                            ('Head', 'face'),
                            ('Coil', 'sensors'),
                            ('Probe', 'stylus'),
                        ]:
                            with ui.row().style('gap: 4px;'):
                                ui.icon(icon).style('font-size: 22px; color: #9ca3af;')
                                label = ui.label(label_text).style('font-size: 1.0rem; color: #9ca3af;')
                                dashboard.__dict__[f'label_marker_{label_text.lower()}'] = label
                
                ui.separator().style('margin: 4px 0;')
                
                # Fiducials section - side by side (Image | Tracker)
                with ui.column().style('margin-bottom: 5px;'):
                    ui.label('Fiducials').style('font-size: 1.3rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
                    
                    with ui.row().style('gap: 2.5rem;'):
                        # Image fiducials (left column)
                        with ui.column().style('gap: 1px;'):
                            ui.label('Image').style('font-size: 1.2rem; color: #6B6B6B; margin-bottom: 1px;')
                            for label_text, icon in [
                                ('L Fid', 'radio_button_unchecked'),
                                ('Nasion', 'radio_button_unchecked'),
                                ('R Fid', 'radio_button_unchecked'),
                            ]:
                                with ui.row().classes('items-center').style('gap: 2px;'):
                                    ui.icon(icon).style('font-size: 15px; color: #9ca3af;')
                                    label = ui.label(label_text).style('font-size: 1rem; color: #9ca3af;')
                                    dashboard.__dict__[f'label_{label_text.lower().replace(" ", "_")}'] = label
                        
                        # Tracker fiducials (right column)
                        with ui.column().style('gap: 1px;'):
                            ui.label('Tracker').style('font-size: 1.2rem; color: #6B6B6B; margin-bottom: 1px;')
                            for label_text, icon in [
                                ('L Tragus', 'radio_button_unchecked'),
                                ('Nose', 'radio_button_unchecked'),
                                ('R Tragus', 'radio_button_unchecked'),
                            ]:
                                with ui.row().classes('items-center').style('gap: 2px;'):
                                    ui.icon(icon).style('font-size: 15px; color: #9ca3af;')
                                    label = ui.label(label_text).style('font-size: 0.85rem; color: #9ca3af;')
                                    dashboard.__dict__[f'label_{label_text.lower().replace(" ", "_")}'] = label
                
                ui.separator().style('margin: 4px 0;')
                
                # Robot section - 2x2 grid
                with ui.column().style('gap: 1px;'):
                    ui.label('Robot').style('font-size: 1.3rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
                    
                    with ui.row().style('gap: 2.5rem; margin-bottom: 2px; width: 100%;'):
                        with ui.row().style('gap: 3px;'):
                            ui.icon('gps_fixed').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('Target').style(f'font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_target'] = label
                        
                        with ui.row().style('gap: 3px;'):
                            ui.icon('radar').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('Coil').style('font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_coil'] = label
                    
                        with ui.row().style('gap: 3px;'):
                            ui.icon('sync').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('Moving').style('font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_moving'] = label
                        
                        with ui.row().style('gap: 3px;'):
                            ui.icon('dataset').style('font-size: 22px; color: #9ca3af;')
                            label = ui.label('Trials').style('font-size: 1.0rem; color: #9ca3af;')
                            dashboard.__dict__['label_trials'] = label
                
                ui.separator().style('margin: 4px 0;')
                
                # Indicators section - Distance, Angle, Force
                with ui.column().style('gap: 1px;'):
                    ui.label('Indicators').style('font-size: 1.3rem; font-weight: 600; color: #6B6B6B; margin-bottom: 2px;')
                    with ui.row().style('gap: 2rem;'):
                        # Distance
                        with ui.row().style('gap: 2px; align-items: center;'):
                            ui.label('Distance:').style('font-size: 0.85rem; color: #6B6B6B; font-weight: 600;')
                            ui.label('0.0 mm').style('font-size: 1.1rem; color: #3b82f6; font-weight: 500;')
                        
                        # Angle
                        with ui.row().style('gap: 2px; align-items: center;'):
                            ui.label('Angle:').style('font-size: 0.85rem; color: #6B6B6B; font-weight: 600;')
                            ui.label('0.0°').style('font-size: 1.1rem; color: #3b82f6; font-weight: 500;')
                        
                        # Force Sensor
                        with ui.row().style('gap: 2px; align-items: center;'):
                            ui.label('Force Sensor:').style('font-size: 0.85rem; color: #6B6B6B; font-weight: 600;')
                            ui.label('0.0 N').style('font-size: 1.1rem; color: #10b981; font-weight: 500;')
            
        # ROW 2 (40% height): Time Series Graph + Navigation Controls
        with ui.row().classes('w-full').style(
            'flex: 35; '
            'min-height: 0; '
            'align-items: stretch; '
            'gap: 0;'
        ):
            # Time Series Graph (65%)
            with ui.card().props('flat').style(
                'flex: 60; '
                'padding: 12px; '
                'display: flex; '
                'flex-direction: row; '
                'overflow: hidden; '
                'height: 100%; '
                'background-color: #f9fafb;'
            ):
                with ui.row().style("gap: 0.5rem; width: 100%; height: 100%;"):
                    with ui.column().style('flex: 1; height: 100%;'):
                        ui.label('Motor evoked potentials response').style('font-size: 1rem; font-weight: 600; margin-bottom: 4px;')
                        
                        # Placeholder for time series plot - fills container
                        with ui.column().style('flex: 1; width: 100%; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 4px;'):
                            ui.label('Time Series Graph').style('font-size: 0.875rem; color: #9ca3af;')
                            ui.label('(Motor Evoked Potentials)').style('font-size: 0.75rem; color: #d1d5db;')
                            # TODO: Add actual plot component here
                            # ui.plotly() or ui.matplotlib() or ui.line_plot()
                    
                    with ui.column().style('flex: 1; height: 100%;'):
                        ui.label('Distance').style('font-size: 1rem; font-weight: 600; margin-bottom: 4px;')
                        
                        # Placeholder for distance graph - fills container
                        with ui.column().style('flex: 1; width: 100%; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 4px;'):
                            ui.label('Time Series Graph').style('font-size: 0.875rem; color: #9ca3af;')
                            ui.label('(Distance over Time)').style('font-size: 0.75rem; color: #d1d5db;')
                            # TODO: Add actual plot component here
                            # ui.plotly() or ui.matplotlib() or ui.line_plot()
            
            # Navigation Controls (40%)
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
                with ui.column().style('gap: 10px; flex: 1; height: 100%;'):
                
                    with ui.column().classes('w-full').style('gap: 10px; flex: 1;'):

                        ui.label('Navigation Controls').style('font-size: 1rem; font-weight: 600; margin-bottom: 8px;')
                        # Main control button - Start/Stop (highlighted)
                        ui.button('START NAVIGATION', icon='play_arrow').props('color=positive size=lg').classes('w-full').style(
                            'font-size: 1rem; '
                            'font-weight: 600; '
                            'padding: 16px; '
                            'min-height: 60px;'
                        )
                        
                        ui.separator().style('margin: 4px 0;')
                        
                        # Create Target button
                        ui.button('Create Target', icon='add_location_alt').props('outlined color=primary').classes('w-full').style(
                            'font-size: 0.95rem; '
                            'min-height: 50px;'
                        )
                        

                with ui.column().style('gap: 5px; flex: 1; height: 100%;'):
                    # Robot control buttons
                        ui.label('Robot Control').style('font-size: 1rem; font-weight: 600; margin-bottom: 8px;')
                        
                        ui.button('Free Drive Robot', icon='gesture').props('flat outlined').classes('w-full').style(
                            'font-size: 0.9rem; '
                            'min-height: 50px;'
                        )

                        ui.separator().style('margin: 4px 0;')
                        
                        ui.button('Active Robot', icon='settings_remote').props('flat outlined').classes('w-full').style(
                            'font-size: 0.9rem; '
                            'min-height: 50px;'
                        )
                        
                        ui.separator().style('margin: 4px 0;')

                        ui.button('Move Upward Robot', icon='arrow_upward').props('flat outlined').classes('w-full').style(
                            'font-size: 0.9rem; '
                            'min-height: 50px;'
                        )
