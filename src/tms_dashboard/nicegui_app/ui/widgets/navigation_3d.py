#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D Navigation visualization component"""

from scipy.spatial.transform import Rotation as R
from nicegui import ui
import math

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

def create_3d_scene_with_models(dashboard: DashboardState):
    """Create detailed 3D scene with STL models of probe, head, coil, and target.
    
    Args:
        dashboard: DashboardState instance for accessing object positions
    """

    SCALE = 0.012

    # Full height scene - fills parent container
    with ui.scene().classes('w-full h-full') as scene:
        # Head model - positioned at origin (head coordinates)
        # Static reference - doesn't move, just for visual context
        head_url = '/static/objects/head.stl'
        head_stl = scene.stl(head_url).scale(SCALE * 0.8).material('#f0d5a0', opacity=0.4)
        # Rotate head to stand upright: X rotation of -90° (occipital was facing ground)
        head_stl.move(0, 0, 0).rotate(-math.pi/2, 0, 0)
        
        # Coil model - will move based on displacement
        coil_path = '/static/objects/magstim_fig8_coil.stl'
        coil_stl = scene.stl(coil_path).scale(SCALE).material('gray', opacity=0.5)
  
        # Target marker - visual indicator of target position
        # This will be positioned when target is set
        coil_path = '/static/objects/aim.stl'
        target_marker_stl = scene.stl(coil_path).scale(SCALE).material('#ff0000', opacity=0.5)

        CoordinateSystem('origin')
        
        # Timer to update object positions from dashboard state
        def update_positions():
            if dashboard.target_set:
                # Get target location: (x, y, z, rx, ry, rz) in InVesalius coords
                target = dashboard.target_location
                displacement = dashboard.displacement
                
                # Convert InVesalius Z-up to Three.js Y-up:
                # InVesalius: X=right, Y=front, Z=up
                # Three.js:   X=right, Y=up, Z=front
                # Mapping: X_threejs = X_inv, Y_threejs = Z_inv, Z_threejs = -Y_inv
                
                # Target position (convert coords and scale)
                target_x = target[0] * SCALE
                target_y = target[2] * SCALE        # Z becomes Y (up)
                target_z = -target[1] * SCALE       # -Y becomes Z
                
                # Target rotation (axis swap)
                target_rx = target[3]               # X rotation (already radians)
                target_ry = target[5]               # Z rotation becomes Y
                target_rz = -target[4]              # -Y rotation becomes Z
                
                # Position and rotate target
                target_marker_stl.move(target_x, target_y, target_z)
                target_marker_stl.rotate(target_rx, target_ry, target_rz)
                target_marker_stl.material(color="yellow", opacity=1)
                
                # Coil position = target position + displacement (with same conversion)
                # Displacement is (dx, dy, dz) in mm, (drx, dry, drz) in degrees
                coil_x = target_x + displacement[0] * SCALE
                coil_y = target_y + displacement[2] * SCALE        # Z becomes Y
                coil_z = target_z + (-displacement[1]) * SCALE     # -Y becomes Z
                
                # Coil rotation = target rotation + displacement rotation
                coil_rx = target_rx + math.radians(displacement[3])
                coil_ry = target_ry + math.radians(displacement[5])  # Z becomes Y
                coil_rz = target_rz + (-math.radians(displacement[4]))  # -Y becomes Z
                
                coil_stl.move(coil_x, coil_y, coil_z)
                coil_stl.rotate(coil_rx, coil_ry, coil_rz)
                
                # Dynamic camera: perpendicular to target plane (like InVesalius)
                min_distance = 1.5
                max_distance = 12.0
                displacement_mm = dashboard.module_displacement
                normalized_displacement = min(1.0, displacement_mm / 150.0)
                camera_distance = min_distance + (max_distance - min_distance) * normalized_displacement
                
                # Get target's rotation matrix to calculate normal vector
                # The target's Z-axis points outward from brain (coil direction)
                target_rotation = R.from_euler('xyz', [target_rx, target_ry, target_rz], degrees=False)
                target_rot_matrix = target_rotation.as_matrix()
                
                # Normal vector = target's Z-axis (direction coil faces)
                # In Three.js Y-up, this is the direction we want to position camera
                normal_vector = target_rot_matrix[:, 2]  # Z-axis column
                
                # Position camera along normal vector, looking back at target
                camera_x = target_x + normal_vector[0] * camera_distance
                camera_y = target_y + normal_vector[1] * camera_distance
                camera_z = target_z + normal_vector[2] * camera_distance
                
                scene.move_camera(
                    x=camera_x,
                    y=camera_y,
                    z=camera_z,
                    look_at_x=target_x,
                    look_at_y=target_y,
                    look_at_z=target_z,
                )
            
            else:
                # No target - reset to origin
                coil_stl.move(-4, 0, 0)
                coil_stl.rotate(0,0,0)
                target_marker_stl.material(opacity=0)
                
                # Reset camera to default view
                scene.move_camera(x=0, y=2, z=5, look_at_x=0, look_at_y=0, look_at_z=0)
        
        ui.timer(0.1, update_positions)  # Update at 10 Hz
