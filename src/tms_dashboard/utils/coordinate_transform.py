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
from scipy.spatial.transform import Rotation as R


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


# ============================================================================
# Matrix Transformation Utilities
# ============================================================================

def pose_to_matrix(pose: List[float]) -> np.ndarray:
    """
    Convert pose (x, y, z, rx, ry, rz) to 4x4 transformation matrix.
    
    Args:
        pose: [x, y, z, rx, ry, rz] where rotations are in radians
    
    Returns:
        4x4 transformation matrix
    """
    x, y, z, rx, ry, rz = pose
    
    # Create rotation matrix from Euler angles (XYZ order, extrinsic)
    rot = R.from_euler('xyz', [rx, ry, rz], degrees=False)
    
    # Build 4x4 transformation matrix
    mat = np.eye(4)
    mat[:3, :3] = rot.as_matrix()
    mat[:3, 3] = [x, y, z]
    
    return mat


def matrix_to_pose(matrix: np.ndarray) -> Tuple[List[float], List[float]]:
    """
    Extract pose from 4x4 transformation matrix.
    
    Args:
        matrix: 4x4 transformation matrix
    
    Returns:
        (position, rotation) where:
            - position: [x, y, z]
            - rotation: [rx, ry, rz] in radians
    """
    # Extract position
    position = matrix[:3, 3].tolist()
    
    # Extract rotation
    rot = R.from_matrix(matrix[:3, :3])
    rotation = rot.as_euler('xyz', degrees=False).tolist()
    
    return position, rotation


def rotation_matrix_to_euler_angles(R_mat: List[List[float]]) -> List[float]:
    """
    Convert 3x3 rotation matrix to Euler angles.
    
    Args:
        R_mat: 3x3 rotation matrix (list of lists or numpy array)
    
    Returns:
        [rx, ry, rz] Euler angles in radians (XYZ order, extrinsic)
    """
    R_mat_np = np.array(R_mat)
    rot = R.from_matrix(R_mat_np)
    return rot.as_euler('xyz', degrees=False).tolist()


def compute_relative_pose(target_pose: List[float], reference_pose: List[float]) -> List[float]:
    """
    Compute target pose relative to reference frame.
    
    This calculates: pose_relative = inv(reference) @ target
    
    Args:
        target_pose: [x, y, z, rx, ry, rz] in global frame (radians)
        reference_pose: [x, y, z, rx, ry, rz] defining new frame origin (radians)
    
    Returns:
        target pose in reference frame coordinates [x, y, z, rx, ry, rz] (radians)
    
    Example:
        If head is at (10, 5, 0, 0, 0, 0) and coil is at (12, 6, 1, 0.1, 0, 0):
        Coil relative to head = (2, 1, 1, 0.1, 0, 0)
    """
    # Convert poses to transformation matrices
    m_ref = pose_to_matrix(reference_pose)
    m_target = pose_to_matrix(target_pose)
    
    # Compute relative transformation: inv(m_ref) @ m_target
    m_relative = np.linalg.inv(m_ref) @ m_target
    
    # Extract position and rotation
    position, rotation = matrix_to_pose(m_relative)
    
    return position + rotation
