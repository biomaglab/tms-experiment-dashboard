#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coordinate transformation utilities for InVesalius → NiceGUI/Three.js

InVesalius uses RAS+ coordinate system:
    X: Right
    Y: Anterior (front)
    Z: Superior (up)

Three.js (NiceGUI scene) uses Y-up coordinate system:
    X: Right
    Y: Up
    Z: Forward (toward viewer)

Transformation mapping:
    threejs_x =  invesalius_x   (Right → Right)
    threejs_y =  invesalius_z   (Superior → Up)
    threejs_z = -invesalius_y   (Anterior → -Forward)
"""

from typing import List, Tuple
import numpy as np


class InVesaliusToThreeJS:
    """Transforms coordinates from InVesalius RAS+ to Three.js Y-up system."""
    
    @staticmethod
    def transform_position(inv_pos: List[float]) -> List[float]:
        """
        Transform linear position from InVesalius to Three.js.
        
        Args:
            inv_pos: [x, y, z] in InVesalius RAS+ (mm)
        
        Returns:
            [x, y, z] in Three.js Y-up (mm)
        """
        x, y, z = inv_pos
        return [
            x,   # Right → Right
            z,   # Superior → Up
            -y   # Anterior → -Forward
        ]
    
    @staticmethod
    def transform_rotation(inv_rot: List[float]) -> List[float]:
        """
        Transform rotation from InVesalius to Three.js.
        
        Args:
            inv_rot: [rx, ry, rz] in InVesalius RAS+ (degrees)
        
        Returns:
            [rx, ry, rz] in Three.js Y-up (degrees)
        """
        rx, ry, rz = inv_rot
        return [
            rx,   # Rotation around X
            rz,   # Rotation around Z → Y
            -ry   # Rotation around Y → -Z
        ]
    
    @staticmethod
    def transform_pose(inv_pose: List[float]) -> Tuple[List[float], List[float]]:
        """
        Transform complete pose (position + rotation).
        
        Args:
            inv_pose: [x, y, z, rx, ry, rz] in InVesalius
        
        Returns:
            (position, rotation) in Three.js
        """
        position = InVesaliusToThreeJS.transform_position(inv_pose[:3])
        rotation = InVesaliusToThreeJS.transform_rotation(inv_pose[3:])
        return position, rotation


def transform_displacement(displacement: List[float]) -> Tuple[List[float], List[float]]:
    """
    Transform displacement data from InVesalius to Three.js.
    
    This is a convenience function that uses InVesaliusToThreeJS internally.
    
    Args:
        displacement: [dx, dy, dz, drx, dry, drz] from InVesalius
            - Linear displacement in mm
            - Angular displacement in degrees
    
    Returns:
        (linear_disp, angular_disp) transformed for Three.js
    """
    linear = InVesaliusToThreeJS.transform_position(displacement[:3])
    angular = InVesaliusToThreeJS.transform_rotation(displacement[3:])
    return linear, angular


def scale_position(position: List[float], scale: float = 1.0) -> List[float]:
    """
    Apply uniform scaling to position.
    
    Useful if you need to convert units or adjust visual scale.
    
    Args:
        position: [x, y, z]
        scale: Scaling factor (default 1.0 = no scaling)
    
    Returns:
        Scaled position
    """
    return [p * scale for p in position]
