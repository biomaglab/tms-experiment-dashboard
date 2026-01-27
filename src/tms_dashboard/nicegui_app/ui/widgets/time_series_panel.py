#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Time series panel widget."""

from nicegui import ui
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tms_dashboard.core.dashboard_state import DashboardState


def create_time_series_panel(dashboard: DashboardState):
    """Create time series graphs panel using the documentation pattern."""
    
    with ui.row().style("gap: 0.5rem; width: 100%; height: 100%;"):
        
        # --- Gráfico 1: Motor evoked potentials ---
        with ui.column().style('flex: 1; height: 100%; min-width: 0; max-width: 50%;'):
            ui.label('Motor evoked potentials response').style('font-size: 1rem; font-weight: 600; margin-bottom: 4px;')
            
            # Criamos o widget usando a sintaxe da documentação
            with ui.matplotlib(figsize=(6, 3)).style('width: 100%; height: 100%; border: 1px solid #e5e7eb; border-radius: 8px;') as mep_plot:
                # Acessamos a figura criada automaticamente
                fig_mep = mep_plot.figure
                ax_mep = fig_mep.gca() # Pega o eixo atual
                
                # Inicializar com plot vazio para exibir eixos e labels
                ax_mep.plot([], [], color='#ef4444', linewidth=2.5)
                
                ax_mep.set_xlabel('Time (ms)', fontsize=10)
                ax_mep.set_ylabel('MEP amplitude (uV)', fontsize=10)
                ax_mep.set_xlim(-10, 40)  # Escala fixa de -10 a 40 ms
                ax_mep.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
                ax_mep.set_facecolor('#fafafa')
                fig_mep.patch.set_facecolor('#ffffff')
                fig_mep.tight_layout()
                mep_plot.update()
            
            # Guardamos as referências para atualizar depois
            dashboard.mep_plot = mep_plot
            dashboard.mep_ax = ax_mep

        # --- Gráfico 2: Displacement ---
        with ui.column().style('flex: 1; height: 100%; min-width: 0; max-width: 50%;'):
            ui.label('Displacement (mm)').style('font-size: 1rem; font-weight: 600; margin-bottom: 4px;')
            
            with ui.matplotlib(figsize=(6, 3)).style('width: 100%; height: 100%; border: 1px solid #e5e7eb; border-radius: 8px;') as displacement_plot:
                fig_disp = displacement_plot.figure
                ax_disp = fig_disp.gca()
                
                ax_disp.set_xlabel('Time (s)', fontsize=10)
                ax_disp.set_ylabel('Displacement (mm)', fontsize=10)
                ax_disp.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
                ax_disp.set_facecolor('#fafafa')
                fig_disp.patch.set_facecolor('#ffffff')
                fig_disp.tight_layout()

            # Guardamos as referências
            dashboard.displacement_plot = displacement_plot
            dashboard.displacement_ax = ax_disp