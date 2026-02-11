#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D Navigation visualization component"""

from scipy.spatial.transform import Rotation as R
from nicegui import ui
import math

from tms_dashboard.core.message_emit import Message2Server
from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.config import OBJECTS_DIR

from tms_dashboard.utils.coordinate_transform import compute_relative_pose

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

def create_3d_scene_with_models(dashboard: DashboardState, message_emit: Message2Server):
    """Create detailed 3D scene with STL models of probe, head, coil, and target.
    
    Args:
        dashboard: DashboardState instance for accessing object positions
    """

    SCALE = 1

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
                with ui.scene(grid=(0.1, 0.1)).classes('w-full h-full') as scene:
                    stl_version_seen = dashboard.stl_version
                    # scene.run_method('cameraControls.enabled = false')
                    # Head model - positioned at origin (head coordinates)
                    # Static reference - doesn't move, just for visual context
                    #head_url = '/static/objects/head.stl'
                    #head_stl = scene.stl(head_url).scale(SCALE * 2.9).material("#949494", opacity=1)
                    # Rotate head to stand upright: X rotation of -90° (occipital was facing ground)
                    #head_stl.move(0, 0, 1).rotate(math.pi/2, 0, -math.pi/10)
                    #-math.pi/2
                    
                    # Coil model - will move based on displacement
                    coil_path = '/static/objects/magstim_fig8_coil.stl'
                    coil_stl = scene.stl(coil_path).scale(SCALE).material('gray', opacity=0.5)
            
                    # Target marker - visual indicator of target position
                    # This will be positioned when target is set
                    coil_path = '/static/objects/aim.stl'
                    target_marker_stl = scene.stl(coil_path).scale(SCALE).material('red', opacity=0)

                    def refresh_surfaces():
                        nonlocal stl_version_seen

                        if not dashboard.stl_urls:
                            message_emit.request_invesalius_mesh()

                        if dashboard.stl_version == stl_version_seen:
                            return

                        stl_version_seen = dashboard.stl_version
                        for name, url in dashboard.stl_urls.items():
                            if name in dashboard.stl_objects:
                                continue

                            obj = scene.stl(url)
                            obj.scale(SCALE).material('orange', opacity=0.4)

                            dashboard.stl_objects[name] = obj

                    # Timer to update object positions from dashboard state
                    def update_positions():
                        refresh_surfaces()
                        if dashboard.target_set:
                            distance_label.set_text(f'Distance: {dashboard.module_displacement} mm')
                            # Get target location: (x, y, z, rx, ry, rz) in InVesalius coords
                            target = dashboard.target_location
                            displacement = dashboard.displacement
                            
                            # Convert InVesalius Z-up to Three.js Y-up:
                            # InVesalius: X=right, Y=front, Z=up
                            # Three.js:   X=right, Y=up, Z=front
                            # Mapping: X_threejs = X_inv, Y_threejs = Z_inv, Z_threejs = -Y_inv

                            # Position and rotate target
                            target_marker_stl.move(target[0], target[1], target[2])
                            target_marker_stl.rotate(target[3], target[4], target[5])
                            target_marker_stl.material(color="yellow", opacity=1)

                            coil_stl.move(dashboard.coil_location[0], dashboard.coil_location[1], dashboard.coil_location[2])
                            # needs to add 90deg in Z (1.5708 rad), only for tms model
                            coil_stl.rotate(dashboard.coil_location[3], dashboard.coil_location[4], dashboard.coil_location[5])
                            
                            # Dynamic camera: perpendicular to target plane (like InVesalius)
                            min_distance = 1
                            max_distance = 2.5
                            displacement_mm = dashboard.module_displacement
                            normalized_displacement = min(1.0, displacement_mm / 140)
                            camera_distance = min_distance + (max_distance - min_distance) * normalized_displacement
                            
                            # Get target's rotation matrix to calculate normal and handle direction
                            target_rotation = R.from_euler('xyz', [target[3], target[4], target[5]], degrees=False)
                            target_rot_matrix = target_rotation.as_matrix()
                            
                            # Normal vector = target's Z-axis (direction coil faces)
                            normal_vector = target_rot_matrix[:, 2]  # Z-axis column
                            
                            # Handle direction = target's Y-axis
                            # Rotate camera position 90° around normal so handle appears vertical
                            handle_vector = target_rot_matrix[:, 1]  # Y-axis column (handle direction)
                            
                            # Position camera along normal vector, looking back at target
                            camera_x = target[3] + normal_vector[0] * camera_distance
                            camera_y = target[4] + normal_vector[1] * camera_distance
                            camera_z = target[5] + normal_vector[2] * camera_distance
                            #TODO fix camera
                            # if dashboard.navigation_button_pressed:
                            #     scene.move_camera(
                            #         x=camera_x,
                            #         y=camera_y,
                            #         z=camera_z,
                            #         look_at_x=target[0],
                            #         look_at_y=target[1],
                            #         look_at_z=target[2],
                            #         up_x=-handle_vector[0],
                            #         up_y=-handle_vector[1],
                            #         up_z=-handle_vector[2],
                            #     )
                        
                        else:
                            # No target - reset to origin
                            coil_stl.move(-4, 0, 0)
                            coil_stl.rotate(0,0,0)
                            target_marker_stl.material(opacity=0)
                            
                            # Reset camera to default view
                            scene.move_camera(x=0, y=2, z=5, look_at_x=0, look_at_y=0, look_at_z=0)
                    
                    ui.timer(0.1, update_positions)  # Update at 10 Hz
