#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D Navigation visualization component"""

from nicegui import ui
import math
from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.utils.coordinate_transform import InVesaliusToThreeJS

class CoordinateSystem(ui.scene.group):

    def __init__(self, name: str, *, length: float = 1.0) -> None:
        super().__init__()

        with self:
            for label, color, rx, ry, rz in [
                ('x', '#ff0000', 0, 0, -math.pi / 2),
                ('y', '#00ff00', 0, 0, 0),
                ('z', '#0000ff', math.pi / 2, 0, 0),
            ]:
                with ui.scene.group().rotate(rx, ry, rz):
                    ui.scene.cylinder(0.02 * length, 0.02 * length, 0.8 * length) \
                        .move(y=0.4 * length).material(color)
                    ui.scene.cylinder(0, 0.1 * length, 0.2 * length) \
                        .move(y=0.9 * length).material(color)
                    ui.scene.text(label, style=f'color: {color}') \
                        .move(y=1.1 * length)
            ui.scene.text(name, style='color: #808080')

def create_3d_scene_with_models(dashboard: DashboardState):
    """Create detailed 3D scene with STL models of probe, head, coil, and target.
    
    Args:
        dashboard: DashboardState instance for accessing object positions
    """

    SCALE = 0.012

    # Full height scene - fills    # Create container for 3D scene
    with ui.column().classes('w-full h-full').style('position: relative; overflow: hidden; display: flex; flex-direction: column; flex: 1;'):
        ui.label('Navigation').style('font-size: 1.1rem; font-weight: 600; margin-bottom: 4px; color: #4b5563;')
        with ui.column().style("position: relative; width: 100%; height: calc(100% - 24px); border: 1px solid #e5e7eb; border-radius: 8px; background-color: white; overflow: hidden;"):
            # Static Overlay Label example
            distance_label = ui.label(f'Distance: {dashboard.module_displacement} mm').style(
                'position: absolute; top: 10px; left: 10px; z-index: 10; '
                'background-color: transparent; padding: 8px 12px; '
                'font-size: 1.1rem; font-weight: 450; color: #374151;'
            )
            
            with ui.row().style("width: calc(100% - 30px); height: calc(100% - 30px); margin: 15px;"):
                with ui.scene().classes('w-full h-full') as scene:
                    # Head model - static in scene
                    head_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/head.stl'
                    # head = scene.stl(head_url).scale(0.17).move(0, 0, 9).rotate(1.57, 0, -0.3)
            
                    # Coil model - will move based on displacement
                    coil_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/magstim_fig8_coil.stl'
                    coil_stl = scene.stl(coil_url).scale(SCALE).material('gray', opacity=0.5)
            
                    # Target marker - visual indicator of target position
                    # This will be positioned when target is set
                    target_marker_stl = scene.sphere(0.2).material('#ff0000', opacity=0.5)

                    CoordinateSystem('origin')
                    
                    # Timer to update object positions from dashboard state
                    def update_positions():
                        if dashboard.target_set:
                            distance_label.set_text(f'Distance: {dashboard.module_displacement} mm')
                            # Calculate relative positions (coil and target relative to head)

                            target_marker_stl.material(color= "yellow", opacity=1)
                            coil_stl.move(
                                (dashboard.coil_location[0] - dashboard.head_location[0]) * SCALE,
                                (dashboard.coil_location[1] - dashboard.head_location[1]) * SCALE,
                                (dashboard.coil_location[2] - dashboard.head_location[2]) * SCALE)
                            coil_stl.rotate(
                                (dashboard.coil_location[3] - dashboard.head_location[3]),
                                (dashboard.coil_location[4] - dashboard.head_location[4]),
                                (dashboard.coil_location[5] - dashboard.head_location[5])
                            )

                            target_x = (dashboard.target_location[0] - dashboard.head_location[0]) * SCALE
                            target_y = (dashboard.target_location[1] - dashboard.head_location[1]) * SCALE
                            target_z = (dashboard.target_location[2] - dashboard.head_location[2]) * SCALE
                            
                            target_marker_stl.move(target_x, target_y, target_z)

                            target_aplha = (dashboard.target_location[3] - dashboard.head_location[3])
                            target_beta = (dashboard.target_location[3] - dashboard.head_location[3])
                            target_gamma = (dashboard.target_location[5] - dashboard.head_location[5])

                            target_marker_stl.rotate(target_aplha, target_beta, target_gamma)
                            
                            # Update camera position: centered on target, looking down from above
                            # Camera height based on module_distance (larger distance = zoom out)
                            camera_height = dashboard.module_displacement * SCALE * 2  # Scale factor for visual comfort
                            
                            # Position camera above target
                            # scene.move_camera(
                            #     x=target_x  + camera_height,
                            #     y=target_y + camera_height, # Above target
                            #     z=target_z  + camera_height,
                            #     look_at_x=target_x,  # Look at target
                            #     look_at_y=target_y,
                            #     look_at_z=target_z
                            # )
                        
                        else:
                            # No target - reset to origin
                            coil_stl.move(-4, 0, 0)
                            coil_stl.rotate(0,0,0)
                            target_marker_stl.material(opacity=0)
                            
                            # Reset camera to default view
                            scene.move_camera(x=0, y=2, z=5, look_at_x=0, look_at_y=0, look_at_z=0)
                    
                    ui.timer(0.1, update_positions)  # Update at 10 Hz
