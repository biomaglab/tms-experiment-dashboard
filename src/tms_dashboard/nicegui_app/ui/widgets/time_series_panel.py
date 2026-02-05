#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Time series panel widget using Plotly for responsive layout."""

from nicegui import ui
import plotly.graph_objects as go
from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.nicegui_app.ui_state import DashboardUI

def create_mep_panel(ui_state: DashboardUI):
    """Create MEP panel using Plotly with distinct styling.
    
    Args:
        dashboard: DashboardState instance
        ui_state: DashboardUI instance (per-client UI state)
    """
    with ui.column().style('flex: 1; width: 100%; height: 100%; min-width: 0; display: flex; flex-direction: column;'):
        ui.label('Motor Evoked Potentials').style(
            'font-size: 1.1rem; font-weight: 600; margin-bottom: 4px; color: #4b5563;'
        )
        
        # Container for Plotly
        with ui.card().props('flat').style('flex: 1; width: 100%; min-height: 0; padding: 0; overflow: hidden; border: 1px solid #e5e7eb; border-radius: 8px;'):
            fig_mep = go.Figure()
            
            # Clinical style trace - thicker line
            fig_mep.add_trace(go.Scatter(
                x=[], y=[], 
                mode='lines', 
                line=dict(color='#dc2626', width=2.5), # Slightly darker red
                name='MEP'
            ))
            
            fig_mep.update_layout(
                margin=dict(l=60, r=20, t=20, b=40), # Increased margins
                font=dict(family="Roboto, sans-serif", size=12, color="#6b7280"), # Matched font
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='#f3f4f6', 
                showlegend=False,
                xaxis=dict(
                    title='Time (ms)', 
                    showgrid=True, 
                    gridcolor='#d1d5db', 
                    zeroline=True,
                    zerolinecolor='#9ca3af',
                    range=[-5, 40] 
                ),
                yaxis=dict(
                    title='Amplitude (µV)', 
                    showgrid=True, 
                    gridcolor='#d1d5db',
                    zeroline=True,
                    zerolinecolor='#9ca3af',
                    automargin=True,
                ),
                autosize=True,
                dragmode=False
            )
            
            # Store reference in UI state
            ui_state.mep_plot = ui.plotly(fig_mep).classes('w-full h-full').props('config="{displayModeBar: false}"')
            ui_state.mep_ax = None # No longer used


def create_time_series_panel(ui_state: DashboardUI):
    """Create time series graphs using Plotly.
    
    Args:
        dashboard: DashboardState instance
        ui_state: DashboardUI instance (per-client UI state)
    """
    
    # Global CSS to hide Plotly toolbar safely
    ui.add_head_html('<style>.js-plotly-plot .plotly .modebar { display: none !important; }</style>')
    
    with ui.row().style("gap: 1rem; width: 100%; height: 100%;"):
        
        # --- Graph 1: Displacement ---
        with ui.column().style('flex: 1; height: 100%; min-width: 0; display: flex; flex-direction: column;'):
            with ui.row().style('align-items: center; gap: 6px; margin-bottom: 4px; flex-shrink: 0;'):
                # ui.icon('trending_up', size='xs').style('color: #3b82f6;')
                ui.label('Displacement (mm)').style('font-size: 1.1rem; font-weight: 600; color: #374151;')
            
            # Container for Plotly
            with ui.card().props('flat').style('flex: 1; width: 100%; min-height: 0; padding: 0; overflow: hidden; border: 1px solid #e5e7eb; border-radius: 8px;'):
                fig_disp = go.Figure()
                
                # Add traces (initially empty)
                fig_disp.add_trace(go.Scatter(x=[], y=[], name='X', mode='lines', line=dict(color='#ef4444', width=2)))
                fig_disp.add_trace(go.Scatter(x=[], y=[], name='Y', mode='lines', line=dict(color='#10b981', width=2)))
                fig_disp.add_trace(go.Scatter(x=[], y=[], name='Z', mode='lines', line=dict(color='#3b82f6', width=2)))
                
                fig_disp.update_layout(
                    margin=dict(l=60, r=20, t=20, b=40),  # Increased margins
                    font=dict(family="Roboto, sans-serif", size=12, color="#6b7280"), # Matched font
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='#fafbfc',
                    showlegend=True,
                    legend=dict(x=1, y=1, xanchor='right', yanchor='top', bgcolor='rgba(255,255,255,0.8)'),
                    xaxis=dict(title='Time (s)', showgrid=True, gridcolor='#e5e7eb'),
                    yaxis=dict(title='Displacement (mm)', showgrid=True, gridcolor='#e5e7eb', automargin=True),
                    autosize=True,
                    dragmode=False  # Disable drag interactions naturally
                )
                
                # Create Plotly element - hide toolbar
                ui_state.displacement_plot = ui.plotly(fig_disp).classes('w-full h-full').props('config="{displayModeBar: false}"')

        # --- Graph 2: Rotation ---
        with ui.column().style('flex: 1; height: 100%; min-width: 0; display: flex; flex-direction: column;'):
            with ui.row().style('align-items: center; gap: 6px; margin-bottom: 4px; flex-shrink: 0;'):
                # ui.icon('rotate_right', size='xs').style('color: #10b981;')
                ui.label('Rotation (°)').style('font-size: 1.1rem; font-weight: 600; color: #374151;')
            
            # Container for Plotly
            with ui.card().props('flat').style('flex: 1; width: 100%; min-height: 0; padding: 0; overflow: hidden; border: 1px solid #e5e7eb; border-radius: 8px;'):
                fig_rot = go.Figure()
                
                # Add traces (initially empty)
                fig_rot.add_trace(go.Scatter(x=[], y=[], name='RX', mode='lines', line=dict(color='#ef4444', width=2)))
                fig_rot.add_trace(go.Scatter(x=[], y=[], name='RY', mode='lines', line=dict(color='#10b981', width=2)))
                fig_rot.add_trace(go.Scatter(x=[], y=[], name='RZ', mode='lines', line=dict(color='#3b82f6', width=2)))
                
                fig_rot.update_layout(
                    margin=dict(l=60, r=20, t=20, b=40), # Increased margins
                    font=dict(family="Roboto, sans-serif", size=12, color="#6b7280"), # Matched font
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='#fafbfc',
                    showlegend=True,
                    legend=dict(x=1, y=1, xanchor='right', yanchor='top', bgcolor='rgba(255,255,255,0.8)'),
                    xaxis=dict(title='Time (s)', showgrid=True, gridcolor='#e5e7eb'),
                    yaxis=dict(title='Rotation (deg)', showgrid=True, gridcolor='#e5e7eb', automargin=True),
                    autosize=True,
                    dragmode=False  # Disable drag interactions naturally
                )
                
                # Create Plotly element - hide toolbar
                ui_state.rotation_plot = ui.plotly(fig_rot).classes('w-full h-full').props('config="{displayModeBar: false}"')
