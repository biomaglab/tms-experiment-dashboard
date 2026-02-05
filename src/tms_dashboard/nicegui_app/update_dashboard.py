#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update dashboard module - manages real-time UI updates."""

import numpy as np
import plotly.graph_objects as go

from tms_dashboard.nicegui_app.styles import change_color, change_radio_icon, change_label, get_status, change_button, change_icon, change_progress_ui, change_image
from tms_dashboard.config import IMAGES_DIR

class UpdateDashboard:
    def __init__(self, dashboard, emg_connection, client_manager):
        self.dashboard = dashboard
        self.emg_connection = emg_connection
        self.client_manager = client_manager

    def update(self):
        ui_states = self.client_manager.get_all_clients()
        for ui_state in ui_states:
            try:
                self.update_dashboard_colors(ui_state)
                self.update_indicators(ui_state)
                self.update_buttons(ui_state)
                # Plots need special handling because they might be heavy to update in loop if not careful,
                # but for now we just update them all.
                # Ideally, NiceGUI handles this efficiently.
                self.update_displacement_plot(ui_state)
                self.update_rotation_plot(ui_state)
                if self.dashboard.status_new_mep:
                    self.update_mep_plot(ui_state)
            except Exception as e:
                print(f"Error updating client: {e}")

    def update_dashboard_colors(self, ui_state):
        """Update all dashboard label colors based on state.
        
        Args:
            ui_state: DashboardUI instance
        """
        dashboard = self.dashboard
        
        change_color(ui_state, "camera", get_status(dashboard.camera_set))
        change_color(ui_state, "robot", get_status(dashboard.robot_set))
        change_color(ui_state, "emg", get_status(self.emg_connection.get_connection()))

        if dashboard.probe_visible:
            path_probe = str(IMAGES_DIR / 'icones/stylus_icon_green.png') 
        else:
            path_probe = str(IMAGES_DIR / 'icones/stylus_icon.png')
        change_image(ui_state, "probe", path_probe)

        if dashboard.head_visible:
            path_head = str(IMAGES_DIR / 'icones/head_icon_green.png') 
        else:
            path_head = str(IMAGES_DIR / 'icones/head_icon.png')
        change_image(ui_state, "head", path_head)

        if dashboard.coil_visible:
            path_coil = str(IMAGES_DIR / 'icones/coil_no_handle_icon_green.png') 
        else:
            path_coil = str(IMAGES_DIR / 'icones/coil_no_handle_icon.png')
        change_image(ui_state, "coil", path_coil)

        status = get_status(dashboard.image_fiducials)
        change_color(dashboard, "image_fiducials", status)
        change_radio_icon(dashboard, "image_fiducials", status)

        status = get_status(dashboard.tracker_fiducials)
        change_color(dashboard, "tracker_fiducials", status)
        change_radio_icon(dashboard, "tracker_fiducials", status)


        change_color(ui_state, "target", get_status(dashboard.target_set))
        change_color(ui_state, "moving", get_status(dashboard.robot_moving))
        change_color(ui_state, "coil", get_status(dashboard.at_target))

    def update_indicators(self, ui_state):
        """Update all dashboard indicators."""
        dashboard = self.dashboard
        change_label(ui_state, "distance", str(round(dashboard.module_displacement, 2)) + " mm")
        change_progress_ui(ui_state, "force_indicator", round(dashboard.force, 2))

    def update_displacement_plot(self, ui_state):
        """Update displacement plot with current history data.
        
        Args:
            ui_state: DashboardUI instance
        """

        dashboard = self.dashboard
        
        # Convert deques to lists for plotting
        time_data = list(dashboard.displacement_time_history)
        x_data = list(dashboard.displacement_history_x)
        y_data = list(dashboard.displacement_history_y)
        z_data = list(dashboard.displacement_history_z)
        
        if ui_state.displacement_plot is None:
            return

        # Update existing Plotly traces in-place
        ui_state.displacement_plot.figure.data[0].x = time_data
        ui_state.displacement_plot.figure.data[0].y = x_data
        ui_state.displacement_plot.figure.data[1].x = time_data
        ui_state.displacement_plot.figure.data[1].y = y_data
        ui_state.displacement_plot.figure.data[2].x = time_data
        ui_state.displacement_plot.figure.data[2].y = z_data
        
        # Force auto-range to handle sliding window
        ui_state.displacement_plot.figure.layout.xaxis.autorange = True
        ui_state.displacement_plot.update()
    
    def update_rotation_plot(self, ui_state):
        """Update rotation plot with current history data (rx, ry, rz in degrees)."""

        dashboard = self.dashboard
        
        # Convert deques to lists for plotting
        time_data = list(dashboard.rotation_time_history)
        rx_data = list(dashboard.rotation_history_rx)
        ry_data = list(dashboard.rotation_history_ry)
        rz_data = list(dashboard.rotation_history_rz)
        
        if ui_state.rotation_plot is None:
            return

        # Update existing Plotly traces in-place
        ui_state.rotation_plot.figure.data[0].x = time_data
        ui_state.rotation_plot.figure.data[0].y = rx_data
        ui_state.rotation_plot.figure.data[1].x = time_data
        ui_state.rotation_plot.figure.data[1].y = ry_data
        ui_state.rotation_plot.figure.data[2].x = time_data
        ui_state.rotation_plot.figure.data[2].y = rz_data
        
        # Force auto-range to handle sliding window
        ui_state.rotation_plot.figure.layout.xaxis.autorange = True
        ui_state.rotation_plot.update()
    
    def update_mep_plot(self, ui_state, num_windows=5):
        """Update MEP plot with current history data using Plotly."""
        
        dashboard = self.dashboard
        if ui_state.mep_plot is None:
            return
            
        # Obter dados
        t_min_ms = self.emg_connection.t_min * 1000
        t_max_ms = self.emg_connection.t_max * 1000
        
        # Se não houver dados, não faz nada
        if not dashboard.mep_history_baseline:
            return
            
        mep_history = list(dashboard.mep_history_baseline)[-num_windows:]
        if not mep_history:
            return

        # Eixo X
        t_ms = np.linspace(t_min_ms, t_max_ms, len(mep_history[0]))
        
        traces = []
        
        # Histórico (cinza)
        for i, mep in enumerate(mep_history[:-1]):
            traces.append(go.Scatter(
                x=t_ms, y=mep,
                mode='lines',
                line=dict(color='rgba(128, 128, 128, 0.5)', width=1.5),
                showlegend=False,
                hoverinfo='skip', # Otimização: ignora hover no histórico
                name=f'Trial {i}'
            ))
            
        # Último (vermelho destaque)
        if len(mep_history) > 0:
            traces.append(go.Scatter(
                x=t_ms, y=mep_history[-1],
                mode='lines',
                line=dict(color='#dc2626', width=3),
                name='Last Response',
                showlegend=False # Sem legenda para manter limpo, ou True se quiser
            ))
            
        # Atualiza figura
        # Substituímos a figura inteira para evitar o erro de validação do Plotly
        # "The data property of a figure may only be assigned..."
        # Mantemos o layout original
        ui_state.mep_plot.figure = go.Figure(data=traces, layout=ui_state.mep_plot.figure.layout)
        # Força update
        ui_state.mep_plot.update()

    def update_buttons(self, ui_state):
        dashboard = self.dashboard
        """Update all dashboard buttons."""
        change_button(ui_state, "navigation_button", get_status(dashboard.navigation_button_pressed))
        change_button(ui_state, "upward_robot_button", get_status(dashboard.move_upward_robot_pressed), ("#5898d46c", "#ffffff00"))
        change_button(ui_state, "active_robot_button", get_status(dashboard.active_robot_pressed), ("#5898d46c", "#ffffff00"))  
        change_button(ui_state, "free_drive_button", get_status(dashboard.free_drive_robot_pressed), ("#5898d46c", "#ffffff00")) 