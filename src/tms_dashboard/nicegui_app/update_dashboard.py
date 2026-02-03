import numpy as np

from tms_dashboard.utils.signal_processing import set_apply_baseline_all, new_indexes_fast_tol
from tms_dashboard.nicegui_app.styles import change_color, change_icon, change_label, get_status, change_button 

class UpdateDashboard:
    def __init__(self, dashboard, emg_connection):
        self.dashboard = dashboard
        self.emg_connection = emg_connection

    def update(self):
        self.update_dashboard_colors()
        self.update_indicators()
        self.update_displacement_plot()
        self.update_buttons()
        if self.dashboard.status_new_mep:
            self.update_mep_plot()

    def update_dashboard_colors(self):
        """Update all dashboard label colors based on state.
        
        Args:
            dashboard: DashboardState instance
        """
        dashboard = self.dashboard
        
        change_color(dashboard, "project", get_status(dashboard.project_set))
        change_color(dashboard, "camera", get_status(dashboard.camera_set))
        change_color(dashboard, "robot", get_status(dashboard.robot_set))
        change_color(dashboard, "tms", get_status(dashboard.tms_set))

        change_color(dashboard, "marker_probe", get_status(dashboard.probe_visible))
        change_color(dashboard, "marker_head", get_status(dashboard.head_visible))
        change_color(dashboard, "marker_coil", get_status(dashboard.coil_visible))

        change_color(dashboard, "nasion", get_status(dashboard.image_NA_set))
        change_icon(dashboard, "nasion", get_status(dashboard.image_NA_set))
        change_color(dashboard, "r_fid", get_status(dashboard.image_RE_set))
        change_icon(dashboard, "r_fid", get_status(dashboard.image_RE_set))
        change_color(dashboard, "l_fid", get_status(dashboard.image_LE_set))
        change_icon(dashboard, "l_fid", get_status(dashboard.image_LE_set))
        change_color(dashboard, "nose", get_status(dashboard.tracker_NA_set))
        change_icon(dashboard, "nose", get_status(dashboard.tracker_NA_set))
        change_color(dashboard, "l_tragus", get_status(dashboard.tracker_LE_set))
        change_icon(dashboard, "l_tragus", get_status(dashboard.tracker_LE_set))
        change_color(dashboard, "r_tragus", get_status(dashboard.tracker_RE_set))
        change_icon(dashboard, "r_tragus", get_status(dashboard.tracker_RE_set))

        change_color(dashboard, "target", get_status(dashboard.target_set))
        change_color(dashboard, "moving", get_status(dashboard.robot_moving))
        change_color(dashboard, "coil", get_status(dashboard.at_target))
        # change_color(dashboard, "trials", get_status(dashboard.trials_started))


    def update_indicators(self):
        """Update all dashboard indicators."""
        dashboard = self.dashboard
        change_label(dashboard, "distance", str(round(dashboard.module_displacement, 2)) + " mm")
        change_label(dashboard, "force", dashboard.force)

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
        
        # Clear and redraw the plot
        ax = dashboard.displacement_ax
        if ax is None:
            return
        ax.clear()
        
        # Plot the three lines
        ax.plot(time_data, x_data, color='#ef4444', linewidth=2.5, label='X axis')
        ax.plot(time_data, y_data, color='#10b981', linewidth=2.5, label='Y axis')
        ax.plot(time_data, z_data, color='#3b82f6', linewidth=2.5, label='Z axis')
        
        # Restore styling
        ax.set_xlabel('Time (s)', fontsize=10)
        ax.set_ylabel('Displacement (mm)', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_facecolor('#fafafa')
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        
        # Update the plot widget
        dashboard.displacement_plot.update()
    
    def update_mep_plot(self, num_windows=5):
        """Update MEP plot with current history data.
        
        Args:
            dashboard: DashboardState instance
        """

        dashboard = self.dashboard
        
        # Aplicar baseline entre 5-20ms
        t_min_ms = self.emg_connection.t_min
        t_max_ms = self.emg_connection.t_max
        
        mep_history = dashboard.mep_history_baseline[-num_windows:]

        ax = dashboard.mep_ax
        ax.clear()

        t_ms = np.linspace(t_min_ms, t_max_ms, len(mep_history[0]))

        ax.set_xlabel('Time (ms)', fontsize=10)
        ax.set_ylabel('MEP amplitude (uV)', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_facecolor('#fafafa')

        for i, mep in enumerate(mep_history[:-1]):
            ax.plot(t_ms, mep, color='gray', alpha=0.5, linewidth=2.5, label='Trial' if i == 0 else None)
        
        ax.plot(t_ms, mep_history[-1], color='#ef4444', alpha=1, linewidth=2.5, label='Last')
        ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
        
        # Update the plot widget
        dashboard.mep_plot.update()

    def update_buttons(self):
        dashboard = self.dashboard
        """Update all dashboard buttons."""
        change_button(dashboard, "navigation_button", get_status(dashboard.navigation_button_pressed))
        change_button(dashboard, "upward_robot_button", get_status(dashboard.move_upward_robot_pressed), ("#5898d46c", "#ffffff00"))
        change_button(dashboard, "active_robot_button", get_status(dashboard.active_robot_pressed), ("#5898d46c", "#ffffff00"))  
        change_button(dashboard, "free_drive_button", get_status(dashboard.free_drive_robot_pressed), ("#5898d46c", "#ffffff00")) 