#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared constants for TMS Experiment Dashboard"""

# Robot messages set - topics that trigger state updates
robot_messages = {
    'Neuronavigation to Robot: Set target',
    'Start navigation',
    'Open navigation menu',
    'Close Project',
    'Project loaded successfully',
    'Set image fiducial',
    'Reset image fiducials',
    'Set robot transformation matrix',
    'Set target',
    'Tracker fiducials set',
    'Set objective',
    'Unset target',
    'Remove sensors ID',
    'Reset tracker fiducials',
    'Robot connection status',
    'Disconnect tracker',
    'Tracker changed',
    'From Neuronavigation: Update tracker poses',
    'Coil at target',
    'Neuronavigation to Robot: Update displacement to target',
    'Trials started',
    'Trial triggered',
    'Stop navigation',
    'Set objective',
    'Set trial objective',
}

# UI label texts
UI_LABELS = [
    'Project', 'Robot', 'Camera', 'TMS',
    'Left Fiducial', 'Nasion', 'Right Fiducial',
    'Left Tragus', 'Nose', 'Right Tragus',
    'Target', 'Coil', 'Moving', 'Trials',
    'Navigation stopped'
]
