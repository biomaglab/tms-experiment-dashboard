#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3D Navigation visualization component"""

import math
from nicegui import ui
from ...core.dashboard_state import DashboardState


def create_coordinate_system(name: str, length: float = 1.0):
    """Create 3D coordinate system with X, Y, Z axes.
    
    Args:
        name: Name label for the coordinate system
        length: Length multiplier for axes
        
    Returns:
        ui.scene.group with coordinate axes
    """
    class CoordinateSystem(ui.scene.group):
        def __init__(self, name: str, *, length: float = 1.0) -> None:
            super().__init__()
            
            with self:
                # Create X, Y, Z axes with colored cylinders and cones
                for label, color, rx, ry, rz in [
                    ('x', '#ff0000', 0, 0, -math.pi / 2),      # Red X
                    ('y', '#00ff00', 0, 0, 0),                  # Green Y
                    ('z', '#0000ff', math.pi / 2, 0, 0),        # Blue Z
                ]:
                    with ui.scene.group().rotate(rx, ry, rz):
                        # Cylinder for axis shaft
                        ui.scene.cylinder(0.02 * length, 0.02 * length, 0.8 * length) \
                            .move(y=0.4 * length).material(color)
                        # Cone for arrow head
                        ui.scene.cylinder(0, 0.1 * length, 0.2 * length) \
                            .move(y=0.9 * length).material(color)
                        # Label
                        ui.scene.text(label, style=f'color: {color}') \
                            .move(y=1.1 * length)
                
                # Coordinate system name
                ui.scene.text(name, style='color: #808080')
    
    return CoordinateSystem(name, length=length)


def create_navigation_3d(dashboard: DashboardState):
    """Create 3D navigation visualization with real-time updates.
    
    Args:
        dashboard: DashboardState instance for accessing navigation data
    """
    # Main scene with coordinate systems and coil tracking
    with ui.scene().classes('w-full').style('height: 400px;') as scene:
        scene.axes_helper()
        
        # Target coordinate system (origin)
        origin = create_coordinate_system('Target')
        
        # TMS coil coordinate system (moves relative to target)
        custom_frame = create_coordinate_system('TMS coil')
        
        # Timer to update coil position/rotation from displacement
        def update_frame():
            # Get linear displacement (x, y, z)
            distance_x = dashboard.displacement[0]
            distance_y = dashboard.displacement[1]
            distance_z = dashboard.displacement[2]
            
            # Get angular displacement (rx, ry, rz) in radians
            rotation_x = dashboard.displacement[3]
            rotation_y = dashboard.displacement[4]
            rotation_z = dashboard.displacement[5]
            
            # Update coil frame position and rotation
            custom_frame.move(distance_x, distance_y, distance_z)
            custom_frame.rotate(rotation_x, rotation_y, rotation_z)
        
        ui.timer(0.05, update_frame)  # Update at 20 Hz


def create_3d_scene_with_models(dashboard: DashboardState):
    """Create detailed 3D scene with STL models of probe, head, coil, and target.
    
    Args:
        dashboard: DashboardState instance for accessing object positions
    """
    # Full height scene - fills parent container
    with ui.scene().classes('w-full h-full') as scene:
        # Load STL models from InVesalius3 GitHub repository
        probe_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/stylus.stl'
        probe = scene.stl(probe_url).scale(0.02).move(-2, -3, 0.5)
        
        head_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/head.stl'
        head = scene.stl(head_url).scale(0.02).move(-3, 4, 1).rotate(1.57, 0, 0)
        
        coil_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/magstim_fig8_coil.stl'
        coil = scene.stl(coil_url).scale(0.02).move(-2, -3, 0.5)
        
        target_url = 'https://raw.githubusercontent.com/invesalius/invesalius3/master/navigation/objects/aim.stl'
        target = scene.stl(target_url).scale(0.2).move(-2, -3, 0.5)
        
        # Timer to update object positions from dashboard state
        def update_positions():
            # Get positions (first 3 elements) and rotations (last 3 elements)
            probe_position = dashboard.probe_location[:3]
            probe_rotation = dashboard.probe_location[3:]
            
            head_position = dashboard.head_location[:3]
            head_rotation = dashboard.head_location[3:]
            
            coil_position = dashboard.coil_location[:3]
            coil_rotation = dashboard.coil_location[3:]
            
            target_position = dashboard.target_location[:3]
            
            # Update probe
            probe.move(int(probe_position[0]), int(probe_position[1]), int(probe_position[2]))
            probe.rotate(int(probe_rotation[0]), int(probe_rotation[1]), int(probe_rotation[2]))
            
            # Update head
            head.move(int(head_position[0]), int(head_position[1]), int(head_position[2]))
            head.rotate(int(head_rotation[0]), int(head_rotation[1]), int(head_rotation[2]))
            
            # Update coil (using displacement for real-time tracking)
            coil.move(int(dashboard.displacement[0]), int(dashboard.displacement[1]), int(dashboard.displacement[2]))
            coil.rotate(int(dashboard.displacement[3]), int(dashboard.displacement[4]), int(dashboard.displacement[5]))
            
            # Update target
            target.move(int(target_position[0]), int(target_position[1]), int(target_position[2]))
        
        ui.timer(0.1, update_positions)  # Update at 10 Hz
