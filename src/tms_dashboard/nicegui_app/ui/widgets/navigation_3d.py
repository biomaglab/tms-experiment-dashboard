#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D Navigation visualization component"""

from nicegui import ui
import math
from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.utils.coordinate_transform import compute_relative_pose
from scipy.spatial.transform import Rotation as R

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

    # Full height scene - fills parent container
    with ui.scene().classes('w-full h-full') as scene:
        # Head model - positioned at origin (head coordinates)
        head_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/head.stl'
        head_stl = scene.stl(head_url).scale(SCALE).material('#f0d5a0', opacity=0.6)
        head_stl.move(0, 0, 0).rotate(0, 0, 0)  # Head at origin in scene
        
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
                # Calculate coil position relative to head using matrix transformations
                # dashboard.*_location format: (x, y, z, rx, ry, rz) - already in Three.js coordinates with radians
                coil_relative = compute_relative_pose(
                    target_pose=list(dashboard.coil_location),
                    reference_pose=list(dashboard.head_location)
                )
                
                #Extract position and rotation
                coil_pos = coil_relative[:3]
                coil_rot = coil_relative[3:]
                
                # Apply scale to position only (NOT rotation)
                # Set absolute position and rotation
                coil_stl.move(
                    coil_pos[0] * SCALE,
                    coil_pos[1] * SCALE,
                    coil_pos[2] * SCALE
                )
                coil_stl.rotate(coil_rot[0], coil_rot[1], coil_rot[2])

                # Calculate target position relative to head
                target_relative = compute_relative_pose(
                    target_pose=list(dashboard.target_location),
                    reference_pose=list(dashboard.head_location)
                )
                
                target_pos = target_relative[:3]
                target_rot = target_relative[3:]
                
                # Set target marker position and rotation
                target_marker_stl.move(
                    target_pos[0] * SCALE,
                    target_pos[1] * SCALE,
                    target_pos[2] * SCALE
                )
                target_marker_stl.rotate(target_rot[0], target_rot[1], target_rot[2])
                target_marker_stl.material(color="yellow", opacity=1)
                
                # Dynamic camera: PERPENDICULAR to target plane
                # Camera should look straight down at target, aligned with target's normal vector
                
                # Calculate camera distance based on displacement
                min_distance = 1.5   # Closest zoom (when at target)
                max_distance = 12.0  # Farthest zoom (when far from target)
                
                displacement_mm = dashboard.module_displacement  # Already in mm
                normalized_displacement = min(1.0, displacement_mm / 150.0)  # Normalize to 0-1
                camera_distance = min_distance + (max_distance - min_distance) * normalized_displacement
                
                # Get target's rotation to calculate normal vector
                # Target rotation defines the plane orientation
                # Testing Y-axis as normal (second column) instead of Z-axis
                target_rotation = R.from_euler('xyz', target_rot, degrees=False)
                target_rot_matrix = target_rotation.as_matrix()
                
                # Normal vector to target plane - Y-axis (index 1)
                # Y-axis is perpendicular to target surface in TMS convention
                # Negate to flip from bottom-up to top-down view
                normal_vector = -target_rot_matrix[:, 1]  # [nx, ny, nz] - NEGATIVE Y-axis
                
                # Position camera along the normal vector at camera_distance from target
                camera_x = target_pos[0] * SCALE + normal_vector[0] * camera_distance
                camera_y = target_pos[1] * SCALE + normal_vector[1] * camera_distance
                camera_z = target_pos[2] * SCALE + normal_vector[2] * camera_distance
                
                # Calculate "up" vector for camera orientation (90° rotation)
                # The up vector defines which direction is "up" in the camera view
                # We want to rotate 90° to the right, so use X-axis of target
                up_vector = target_rot_matrix[:, 0]  # X-axis of target (first column)
                
                scene.move_camera(
                    x=camera_x,
                    y=camera_y,
                    z=camera_z,
                    look_at_x=target_pos[0] * SCALE,
                    look_at_y=target_pos[1] * SCALE,
                    look_at_z=target_pos[2] * SCALE,
                )
            
            else:
                # No target - reset to origin
                coil_stl.move(-4, 0, 0)
                coil_stl.rotate(0,0,0)
                target_marker_stl.material(opacity=0)
                
                # Reset camera to default view
                scene.move_camera(x=0, y=2, z=5, look_at_x=0, look_at_y=0, look_at_z=0)
        
        ui.timer(0.1, update_positions)  # Update at 10 Hz
