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

    def update_single(self, ui_state):
        """Update a single client's UI. Called by per-client ui.timer on event loop."""
        self.update_dashboard_colors(ui_state)
        self.update_indicators(ui_state)
        self.update_buttons(ui_state)
        self.update_displacement_plot(ui_state)
        self.update_rotation_plot(ui_state)
        if self.dashboard.status_new_mep:
            self.update_mep_plot(ui_state)

    def update(self):
        """Update all clients (legacy — kept for compatibility)."""
        ui_states = self.client_manager.get_all_clients()
        for ui_state in ui_states:
            try:
                self.update_single(ui_state)
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
            path_probe = str(IMAGES_DIR / 'visibilities_markers_icon/stylus_icon_green.png') 
        else:
            path_probe = str(IMAGES_DIR / 'visibilities_markers_icon/stylus_icon.png')
        change_image(ui_state, "probe", path_probe)

        if dashboard.head_visible:
            path_head = str(IMAGES_DIR / 'visibilities_markers_icon/head_icon_green.png') 
        else:
            path_head = str(IMAGES_DIR / 'visibilities_markers_icon/head_icon.png')
        change_image(ui_state, "head", path_head)

        if dashboard.coil_visible:
            path_coil = str(IMAGES_DIR / 'visibilities_markers_icon/coil_no_handle_icon_green.png') 
        else:
            path_coil = str(IMAGES_DIR / 'visibilities_markers_icon/coil_no_handle_icon.png')
        change_image(ui_state, "coil", path_coil)

        status = get_status(dashboard.image_fiducials)
        change_color(ui_state, "image_fiducials", status)
        change_radio_icon(ui_state, "image_fiducials", status)

        status = get_status(dashboard.tracker_fiducials)
        change_color(ui_state, "tracker_fiducials", status)
        change_radio_icon(ui_state, "tracker_fiducials", status)

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
        time_trigger = list(dashboard.trigged_times)
        x_data = list(dashboard.displacement_history_x)
        y_data = list(dashboard.displacement_history_y)
        z_data = list(dashboard.displacement_history_z)
        
        if ui_state.displacement_plot is None:
            return

        # Skip if no new data since last update
        if dashboard.displacement_time_history:
            last_time = dashboard.displacement_time_history[-1]
            cache_key = '_cache_last_displacement_time'
            if getattr(ui_state, cache_key, None) == last_time:
                return
            setattr(ui_state, cache_key, last_time)

        # Update existing Plotly traces in-place
        ui_state.displacement_plot.figure.data[0].x = time_data
        ui_state.displacement_plot.figure.data[0].y = x_data
        ui_state.displacement_plot.figure.data[1].x = time_data
        ui_state.displacement_plot.figure.data[1].y = y_data
        ui_state.displacement_plot.figure.data[2].x = time_data
        ui_state.displacement_plot.figure.data[2].y = z_data

        ui_state.displacement_plot.figure.layout.shapes = []
        for trigger in time_trigger:
            if trigger in time_data:
                ui_state.displacement_plot.figure.add_vline(
                x=trigger,
                line=dict(color="red", width=2, dash="dash"),
                opacity=0.8
            )
        
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
        time_trigger = list(dashboard.trigged_times)
        
        if ui_state.rotation_plot is None:
            return

        # Skip if no new data since last update
        if dashboard.rotation_time_history:
            last_time = dashboard.rotation_time_history[-1]
            cache_key = '_cache_last_rotation_time'
            if getattr(ui_state, cache_key, None) == last_time:
                return
            setattr(ui_state, cache_key, last_time)

        # Update existing Plotly traces in-place
        ui_state.rotation_plot.figure.data[0].x = time_data
        ui_state.rotation_plot.figure.data[0].y = rx_data
        ui_state.rotation_plot.figure.data[1].x = time_data
        ui_state.rotation_plot.figure.data[1].y = ry_data
        ui_state.rotation_plot.figure.data[2].x = time_data
        ui_state.rotation_plot.figure.data[2].y = rz_data
        
        ui_state.displacement_plot.figure.layout.shapes = []
        for trigger in time_trigger:
            if trigger in time_data:
                ui_state.displacement_plot.figure.add_vline(
                x=trigger,
                line=dict(color="red", width=2, dash="dash"),
                opacity=0.8
            )

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
        mep_p2p_history = list(dashboard.mep_p2p_history_baseline)[-num_windows:]
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
            # Annotation for history (optional, keeps it cleaner if only on last? User asked for "on the curve")
            if i < len(mep_p2p_history):
                peak_idx = np.argmax(mep)
                traces.append(go.Scatter(
                    x=[t_ms[peak_idx]], y=[mep[peak_idx]],
                    mode='text',
                    text=[f'{mep_p2p_history[i]:.0f} uV'],
                    textposition='top center',
                    textfont=dict(color='gray', size=18),
                    showlegend=False,
                    hoverinfo='skip'
                ))
            
        # Último (vermelho destaque)
        if len(mep_history) > 0:
            last_mep = mep_history[-1]
            traces.append(go.Scatter(
                x=t_ms, y=last_mep,
                mode='lines',
                line=dict(color='#dc2626', width=3),
                name='Last Response',
                showlegend=False 
            ))
            if len(mep_p2p_history) > 0:
                peak_idx = np.argmax(last_mep)
                traces.append(go.Scatter(
                    x=[t_ms[peak_idx]], y=[last_mep[peak_idx]],
                    mode='text',
                    text=[f'{mep_p2p_history[-1]:.0f} µV'],
                    textposition='top center',
                    textfont=dict(color='#dc2626', size=24, weight='bold'),
                    showlegend=False,
                    hoverinfo='skip'
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