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

def create_3d_scene_with_models(dashboard: DashboardState, message_emit: Message2Server):
    """Create detailed 3D scene with STL models of probe, head, coil, and target.
    
    Args:
        dashboard: DashboardState instance for accessing object positions
    """

    SCALE = 0.65

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
                    
                    # Coil model - will move based on displacement
                    coil_path = '/static/objects/magstim_fig8_coil.stl'
                    coil_stl = scene.stl(coil_path).scale(SCALE).material('gray', opacity=0.4)
            
                    # Target marker - visual indicator of target position
                    # This will be positioned when target is set
                    coil_path = '/static/objects/aim.stl'
                    target_marker_stl = scene.stl(coil_path).scale(SCALE).material('red', opacity=0)

                    scene.move_camera(x=0, y=80, z=200, look_at_x=0, look_at_y=0, look_at_z=0)

                    # Per-scene storage for STL objects (NOT shared across clients)
                    local_stl_objects: dict = {}

                    def refresh_surfaces():
                        nonlocal stl_version_seen

                        if (
                            not dashboard.stl_urls
                            and dashboard.stl_version == 0
                            and dashboard.navigation_button_pressed
                        ):
                            message_emit.request_invesalius_mesh()
                            return

                        if dashboard.stl_version == stl_version_seen:
                            first_object = next(iter(local_stl_objects.values()), None)
                            if first_object is not None and first_object.id in scene.objects:
                                return

                        stl_version_seen = dashboard.stl_version

                        # Snapshot copy: safe to iterate even if message handler modifies the original
                        stl_urls_snapshot = dict(dashboard.stl_urls)

                        # Clean up local objects that were removed from stl_urls
                        removed_keys = set(local_stl_objects) - set(stl_urls_snapshot)
                        for key in removed_keys:
                            obj = local_stl_objects.pop(key)
                            obj.delete()

                        for surface_index, stl_info in stl_urls_snapshot.items():
                            color = stl_info.get("color", "gray")
                            opacity = stl_info.get("transparency", 0.4)

                            obj = local_stl_objects.get(surface_index)

                            if obj is not None and obj.id in scene.objects:
                                obj.material(color, opacity=opacity, side='both')
                                continue

                            obj = scene.stl(stl_info["url"])
                            obj.material(color, opacity=opacity, side='both')
                            # Disable depthWrite so inner objects (brain) show through
                            # outer transparent objects (head).
                            try:
                                ui.run_javascript(f'''
                                    setTimeout(() => {{
                                        for (const [key, el] of Object.entries(window)) {{
                                            if (key.startsWith("scene_")) {{
                                                el.traverse((child) => {{
                                                    if (child.object_id === "{obj.id}" && child.material) {{
                                                        child.material.depthWrite = false;
                                                    }}
                                                }});
                                            }}
                                        }}
                                    }}, 500);
                                ''')
                            except Exception:
                                pass
                            local_stl_objects[surface_index] = obj

                    # Timer to update object positions from dashboard state
                    def update_positions():

                        refresh_surfaces()
                        coil_stl.move(dashboard.coil_location[0], dashboard.coil_location[1], dashboard.coil_location[2])
                        # needs to add 90deg in Z (1.5708 rad), only for tms model
                        coil_stl.rotate(dashboard.coil_location[3], dashboard.coil_location[4], dashboard.coil_location[5])

                        if dashboard.target_set:
                            distance_label.set_text(f'Distance: {dashboard.module_displacement} mm')
                            # Get target location: (x, y, z, rx, ry, rz) in InVesalius coords
                            target = dashboard.target_location
                            
                            # Convert InVesalius Z-up to Three.js Y-up:
                            # InVesalius: X=right, Y=front, Z=up
                            # Three.js:   X=right, Y=up, Z=front
                            # Mapping: X_threejs = X_inv, Y_threejs = Z_inv, Z_threejs = -Y_inv

                            # Position and rotate target
                            target_marker_stl.move(target[0], target[1], target[2])
                            target_marker_stl.rotate(target[3], target[4], target[5])
                            target_marker_stl.material(color="yellow", opacity=1)

                            if dashboard.navigation_button_pressed:
                                # Dynamic camera: perpendicular to target plane (like InVesalius)
                                min_distance = 30
                                max_distance = 200
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
                                camera_x = target[0] + normal_vector[0] * camera_distance
                                camera_y = target[1] + normal_vector[1] * camera_distance
                                camera_z = target[2] + normal_vector[2] * camera_distance

                                scene.move_camera(
                                    x=camera_x,
                                    y=camera_y,
                                    z=camera_z,
                                    look_at_x=target[0],
                                    look_at_y=target[1],
                                    look_at_z=target[2],
                                    up_x=-handle_vector[0],
                                    up_y=-handle_vector[1],
                                    up_z=-handle_vector[2],
                                )
                        else:
                            target_marker_stl.material(opacity=0)
                    
                    ui.timer(0.1, update_positions)  # Update at 10 Hz
