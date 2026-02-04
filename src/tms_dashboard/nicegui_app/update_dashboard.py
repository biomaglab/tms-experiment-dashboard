import numpy as np
import plotly.graph_objects as go

from tms_dashboard.nicegui_app.styles import change_color, change_radio_icon, change_label, get_status, change_button, change_icon, change_progress_ui
from tms_dashboard.config import IMAGES_DIR

class UpdateDashboard:
    def __init__(self, dashboard, emg_connection):
        self.dashboard = dashboard
        self.emg_connection = emg_connection

    def update(self):
        self.update_dashboard_colors()
        self.update_indicators()
        self.update_displacement_plot()
        self.update_rotation_plot()
        self.update_buttons()
        if self.dashboard.status_new_mep:
            self.update_mep_plot()

    def update_dashboard_colors(self):
        """Update all dashboard label colors based on state.
        
        Args:
            dashboard: DashboardState instance
        """
        dashboard = self.dashboard
        
        change_color(dashboard, "camera", get_status(dashboard.camera_set))
        change_color(dashboard, "robot", get_status(dashboard.robot_set))
        change_color(dashboard, "emg", get_status(self.emg_connection.get_connection()))

        change_icon(dashboard, "probe", f"{IMAGES_DIR}\icones\stylus_icon_green.png" if dashboard.probe_visible else f"{IMAGES_DIR}\icones\stylus_icon.png")
        change_icon(dashboard, "head", f"{IMAGES_DIR}\icones\head_icon_green.png" if dashboard.head_visible else f"{IMAGES_DIR}\icones\head_icon.png")
        change_icon(dashboard, "coil", f"{IMAGES_DIR}\icones\coil_no_handle_icon_green.png" if dashboard.coil_visible else f"{IMAGES_DIR}\icones\coil_no_handle_icon.png")

        status = get_status(dashboard.image_fiducials)
        change_color(dashboard, "image_fiducials", status)
        change_radio_icon(dashboard, "image_fiducials", status)

        status = get_status(dashboard.tracker_fiducials)
        change_color(dashboard, "tracker_fiducials", status)
        change_radio_icon(dashboard, "tracker_fiducials", status)

        change_color(dashboard, "target", get_status(dashboard.target_set))
        change_color(dashboard, "moving", get_status(dashboard.robot_moving))
        change_color(dashboard, "coil", get_status(dashboard.at_target))

    def update_indicators(self):
        """Update all dashboard indicators."""
        dashboard = self.dashboard
        change_label(dashboard, "distance", str(round(dashboard.module_displacement, 2)) + " mm")
        change_progress_ui(dashboard, "force_indicator", round(dashboard.force, 2))

    def update_displacement_plot(self):
        """Update displacement plot with current history data.
        
        Args:
            dashboard: DashboardState instance
        """

        dashboard = self.dashboard
        
        # Convert deques to lists for plotting
        time_data = list(dashboard.displacement_time_history)
        x_data = list(dashboard.displacement_history_x)
        y_data = list(dashboard.displacement_history_y)
        z_data = list(dashboard.displacement_history_z)
        
        if dashboard.displacement_plot is None:
            return

        # Update existing Plotly traces in-place
        dashboard.displacement_plot.figure.data[0].x = time_data
        dashboard.displacement_plot.figure.data[0].y = x_data
        dashboard.displacement_plot.figure.data[1].x = time_data
        dashboard.displacement_plot.figure.data[1].y = y_data
        dashboard.displacement_plot.figure.data[2].x = time_data
        dashboard.displacement_plot.figure.data[2].y = z_data
        
        # Force auto-range to handle sliding window
        dashboard.displacement_plot.figure.layout.xaxis.autorange = True
        dashboard.displacement_plot.update()
    
    def update_rotation_plot(self):
        """Update rotation plot with current history data (rx, ry, rz in degrees)."""

        dashboard = self.dashboard
        
        # Convert deques to lists for plotting
        time_data = list(dashboard.rotation_time_history)
        rx_data = list(dashboard.rotation_history_rx)
        ry_data = list(dashboard.rotation_history_ry)
        rz_data = list(dashboard.rotation_history_rz)
        
        if dashboard.rotation_plot is None:
            return

        # Update existing Plotly traces in-place
        dashboard.rotation_plot.figure.data[0].x = time_data
        dashboard.rotation_plot.figure.data[0].y = rx_data
        dashboard.rotation_plot.figure.data[1].x = time_data
        dashboard.rotation_plot.figure.data[1].y = ry_data
        dashboard.rotation_plot.figure.data[2].x = time_data
        dashboard.rotation_plot.figure.data[2].y = rz_data
        
        # Force auto-range to handle sliding window
        dashboard.rotation_plot.figure.layout.xaxis.autorange = True
        dashboard.rotation_plot.update()
    
    def update_mep_plot(self, num_windows=5):
        """Update MEP plot with current history data using Plotly."""
        
        dashboard = self.dashboard
        if dashboard.mep_plot is None:
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
        dashboard.mep_plot.figure['data'] = traces
        # Força update
        dashboard.mep_plot.update()

    def update_buttons(self):
        dashboard = self.dashboard
        """Update all dashboard buttons."""
        change_button(dashboard, "navigation_button", get_status(dashboard.navigation_button_pressed))
        change_button(dashboard, "upward_robot_button", get_status(dashboard.move_upward_robot_pressed), ("#5898d46c", "#ffffff00"))
        change_button(dashboard, "active_robot_button", get_status(dashboard.active_robot_pressed), ("#5898d46c", "#ffffff00"))  
        change_button(dashboard, "free_drive_button", get_status(dashboard.free_drive_robot_pressed), ("#5898d46c", "#ffffff00")) 