#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Time series panel widget."""

from nicegui import ui
from ....core.dashboard_state import DashboardState


def create_time_series_panel(dashboard: DashboardState):
    """Create time series graphs panel.
    
    Contains two side-by-side graphs:
    - Motor evoked potentials response
    - Distance over time
    
    Args:
        dashboard: DashboardState instance
    """
    with ui.row().style("gap: 0.5rem; width: 100%; height: 100%;"):
        # Motor evoked potentials graph
        with ui.column().style('flex: 1; height: 100%;'):
            ui.label('Motor evoked potentials response').style('font-size: 1rem; font-weight: 600; margin-bottom: 4px;')
            
            # Placeholder for time series plot - fills container
            with ui.column().style('flex: 1; width: 100%; background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 4px;'):
                ui.label('Time Series Graph').style('font-size: 0.875rem; color: #9ca3af;')
                ui.label('(Motor Evoked Potentials)').style('font-size: 0.75rem; color: #d1d5db;')
                # TODO: Add actual plot component here
                # ui.plotly() or ui.matplotlib() or ui.line_plot()
        
        # Displacement graph (x, y, z in same plot)
        with ui.column().style('flex: 1; height: 100%;'):
            ui.label('Displacement (mm)').style('font-size: 1rem; font-weight: 600; margin-bottom: 4px;')
            
            # Create Plotly graph with modern styling
            displacement_plot = ui.plotly({
                'data': [
                    {
                        'x': [],
                        'y': [],
                        'mode': 'lines',
                        'name': 'X axis',
                        'line': {'color': '#ef4444', 'width': 2.5},  # Red
                        'hovertemplate': '<b>X: %{y:.2f} mm</b><br>Time: %{x:.1f}s<extra></extra>'
                    },
                    {
                        'x': [],
                        'y': [],
                        'mode': 'lines',
                        'name': 'Y axis',
                        'line': {'color': '#10b981', 'width': 2.5},  # Green (dashboard success color)
                        'hovertemplate': '<b>Y: %{y:.2f} mm</b><br>Time: %{x:.1f}s<extra></extra>'
                    },
                    {
                        'x': [],
                        'y': [],
                        'mode': 'lines',
                        'name': 'Z axis',
                        'line': {'color': '#3b82f6', 'width': 2.5},  # Blue (dashboard info color)
                        'hovertemplate': '<b>Z: %{y:.2f} mm</b><br>Time: %{x:.1f}s<extra></extra>'
                    }
                ],
                'layout': {
                    'xaxis': {
                        'title': {'text': 'Time (s)', 'font': {'size': 12, 'color': '#6b7280'}},
                        'gridcolor': '#e5e7eb',
                        'showgrid': True,
                        'zeroline': True,
                        'zerolinecolor': '#d1d5db',
                        'zerolinewidth': 1,
                        'fixedrange': False  # Allow zoom/pan
                    },
                    'yaxis': {
                        'title': {'text': 'Displacement (mm)', 'font': {'size': 12, 'color': '#6b7280'}},
                        'gridcolor': '#e5e7eb',
                        'showgrid': True,
                        'zeroline': True,
                        'zerolinecolor': '#d1d5db',
                        'zerolinewidth': 2,
                        'fixedrange': False  # Allow zoom/pan
                    },
                    'autosize': False,  # Disable auto-sizing
                    'width': None,  # Let CSS control width
                    'height': None,  # Let CSS control height
                    'margin': {'l': 50, 'r': 20, 't': 20, 'b': 40},
                    'paper_bgcolor': '#ffffff',
                    'plot_bgcolor': '#fafafa',
                    'hovermode': 'x unified',
                    'legend': {
                        'orientation': 'h',
                        'yanchor': 'bottom',
                        'y': 1.02,
                        'xanchor': 'right',
                        'x': 1,
                        'font': {'size': 11, 'color': '#4b5563'}
                    },
                    'font': {'family': 'system-ui, -apple-system, sans-serif', 'color': '#374151'}
                },
                'config': {
                    'responsive': False,  # Disable responsive mode
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['select2d', 'lasso2d']
                }
            }).style('width: 100%; height: 100%; min-width: 0; min-height: 0; max-width: 100%; border: 1px solid #e5e7eb; border-radius: 8px;')
            
            # Store reference to plot for updates
            dashboard.displacement_plot = displacement_plot
