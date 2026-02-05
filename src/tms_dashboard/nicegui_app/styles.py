#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiceGUI-specific styles and color management - Modern Clean Design"""

from nicegui.elements.label import Label
from typing import Dict


# Modern Color Palette - Clean and Professional
COLORS = {
    'success': '#10b981',      # Green
    'error': '#ef4444',        # Red
    'warning': '#f59e0b',      # Amber
    'info': '#3b82f6',         # Blue
    'neutral': '#6b7280',      # Gray
    'bg_light': '#f9fafb',     # Very light gray
    'bg_card': '#ffffff',      # White
    'border': '#e5e7eb',       # Light gray border
    'text_primary': '#111827', # Almost black
    'text_secondary': '#6b7280' # Gray
}

# Global label registry for updating styles
labels: Dict[str, Label] = {}


def modern_card_style() -> str:
    """Get modern card container style."""
    return (
        'background-color: #ffffff;'
        'border-radius: 12px;'
        'box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);'
        'padding: 24px;'
        'margin-bottom: 16px;'
    )


def status_badge_style(status: str) -> str:
    """Get modern status badge style.
    
    Args:
        status: 'success', 'error', 'warning', 'info', or 'neutral'
        
    Returns:
        CSS style string for badge
    """
    color_map = {
        'success': ('#10b981', '#d1fae5'),
        'error': ('#ef4444', '#fee2e2'),
        'warning': ('#f59e0b', '#fef3c7'),
        'info': ('#3b82f6', '#dbeafe'),
        'neutral': ('#6b7280', '#f3f4f6')
    }
    
    text_color, bg_color = color_map.get(status, color_map['neutral'])
    
    return (
        f'display: inline-flex;'
        f'align-items: center;'
        f'padding: 6px 12px;'
        f'border-radius: 9999px;'
        f'font-size: 0.875rem;'
        f'font-weight: 500;'
        f'background-color: {bg_color};'
        f'color: {text_color};'
        f'border: 1px solid {text_color}33;'
        f'min-width: 100px;'
        f'justify-content: center;'
    )


def section_title_style() -> str:
    """Get section title style."""
    return (
        'font-size: 1.125rem;'
        'font-weight: 600;'
        'color: #111827;'
        'margin-bottom: 12px;'
        'letter-spacing: -0.025em;'
    )


def change_color(ui_state, target_label: str, new_status: str, colors: tuple = None):
    """Change the color of a label and its associated icon.

    Supports labels/icons (original behavior) and the navigation button.

    Args:
        ui_state: DashboardUI instance containing label and icon references
        target_label: Name of the label/button to update
        new_status: Status - 'success' or 'neutral'
        colors: Optional tuple (active_color, inactive_color) for buttons
    """

    # Fallback: original label/icon logic
    if colors is None:
        color = '#10b981' if new_status == 'success' else '#9ca3af'
    else:
        color = colors[0] if new_status == 'success' else colors[1]

    # Update label if exists in ui_state
    label_key = f'label_{target_label.lower().replace(" ", "_")}'
    if hasattr(ui_state, label_key):
        label = getattr(ui_state, label_key)
        if label:
            label.style(f'color: {color};')
            label.update()

    # Update associated icon if exists
    icon_key = f'icon_{target_label.lower().replace(" ", "_")}'
    if hasattr(ui_state, icon_key):
        icon = getattr(ui_state, icon_key)
        if icon:
            icon.style(f'color: {color};')
            icon.update()

def change_icon(ui_state, target_label: str, new_status: str):
    """Change the icon of a label based on status (for Material Icons/Radio Buttons)."""
    icon_key = f'icon_{target_label.lower().replace(" ", "_")}'
    if hasattr(ui_state, icon_key):
        icon = getattr(ui_state, icon_key)
        if icon:
            icon.name = 'radio_button_unchecked' if new_status == 'neutral' else 'radio_button_checked'
            icon.update()

def change_radio_icon(ui_state, target_label: str, new_status: str):
    """Alias for change_icon (compatibility)."""
    change_icon(ui_state, target_label, new_status)

def change_label(ui_state, target_label: str, new_text: str):
    """Change the label text."""
    label_key = f'label_{target_label.lower().replace(" ", "_")}'
    if hasattr(ui_state, label_key):
        label = getattr(ui_state, label_key)
        if label:
            label.text = new_text
            label.update()

def get_status(condition: bool) -> str:
    return 'success' if condition else 'neutral'

def change_button(ui_state, target_label: str, new_status: str, colors: tuple = None):
    # Special handling for the START NAVIGATION button
    if hasattr(ui_state, target_label):
        if colors is None:
            color = '#10b981' if new_status == 'success' else '#9ca3af'
        else:
            color = colors[0] if new_status == 'success' else colors[1]

        button = getattr(ui_state, target_label)
        # Fallback: inline style
        if button:
            button.style(f'background-color: {color} !important;')
            button.update()

def change_image(ui_state, target_label: str, icon_path):
    """Change the source of a ui.image widget."""
    image_key = f'image_{target_label.lower().replace(" ", "_")}'
    if hasattr(ui_state, image_key):
        image = getattr(ui_state, image_key)
        if image and image.source != icon_path:
            image.set_source(icon_path)
            image.force_reload()

def change_progress_ui(ui_state, target_label: str, value):
    """Update value of a circular progress indicator."""
    key = f'{target_label.lower().replace(" ", "_")}'
    if hasattr(ui_state, key):
        progress_ui = getattr(ui_state, key)
        if progress_ui and progress_ui.value != value:
            progress_ui.set_value(value)
