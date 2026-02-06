#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checklist tab component for NiceGUI app"""

import json
import os
from nicegui import ui
from ...core.dashboard_state import DashboardState
from ...config import DATA_DIR


TEMPLATES_FILE = DATA_DIR / 'checklist_templates.json'


@ui.refreshable
def create_checklist_tab(dashboard: DashboardState):
    """Create the checklist tab content.
    
    Args:
        dashboard: DashboardState instance
    """
    with ui.column().classes('w-full p-4 gap-4'):
        ui.label('Experiment Checklist').style('font-size: 1.25rem; font-weight: 600;')
        
        # Template loading
        with ui.row().classes('w-full items-center gap-2'):
            templates = load_templates()
            template_select = ui.select(options=list(templates.keys()), label='Load Template').classes('flex-grow')
            ui.button('Load Template', icon='folder_open', on_click=lambda: load_template(dashboard, template_select.value)).props('flat')
        
        if not templates:
            ui.label('No templates saved yet.').style('color: gray; font-style: italic;')
        
        ui.separator()
        
        # Display checklist items
        for i, item in enumerate(dashboard.experiment_checklist):
            with ui.row().classes('w-full items-center gap-2'):
                with ui.element('div').style('width: 2.25rem; display: flex; align-items: center; justify-content: center;'):
                    ui.checkbox('').bind_value(dashboard.checklist_checked, str(i)).classes('self-center').style('width: 1.25rem; height: 1.25rem;')

                ui.input(value=item).props('debounce=300').on_value_change(lambda e, idx=i: update_checklist_item(dashboard, idx, e.value)).classes('flex-grow')
                ui.button(icon='delete', on_click=lambda idx=i: delete_checklist_item(dashboard, idx)).props('flat dense')
        
        ui.button('Add Step', icon='add', on_click=lambda: add_checklist_item(dashboard)).classes('mt-4')
        
        # Template saving at the end
        ui.separator()
        with ui.row().classes('w-full items-center gap-2'):
            template_name_input = ui.input('Template Name', placeholder='Enter template name').classes('flex-grow')
            ui.button('Save as Template', icon='save', on_click=lambda: save_template(dashboard, template_name_input.value)).props('flat')


def update_checklist_item(dashboard: DashboardState, idx: int, new_value: str):
    """Update a checklist item."""
    dashboard.experiment_checklist[idx] = new_value


def delete_checklist_item(dashboard: DashboardState, idx: int):
    """Delete a checklist item."""
    del dashboard.experiment_checklist[idx]
    # Reindex the checked dict
    new_checked = {}
    for j in range(len(dashboard.experiment_checklist) + 1):
        key = str(j)
        if key in dashboard.checklist_checked:
            if j < idx:
                new_checked[str(j)] = dashboard.checklist_checked[key]
            elif j > idx:
                new_checked[str(j - 1)] = dashboard.checklist_checked[key]
    dashboard.checklist_checked = new_checked
    create_checklist_tab.refresh()


def add_checklist_item(dashboard: DashboardState):
    """Add a new checklist item."""
    dashboard.experiment_checklist.append('New step')
    dashboard.checklist_checked[str(len(dashboard.experiment_checklist) - 1)] = False
    create_checklist_tab.refresh()


def save_template(dashboard: DashboardState, name: str):
    """Save the current checklist as a template."""
    if not name:
        ui.notify('Please enter a template name.', type='warning')
        return
    templates = load_templates()
    templates[name] = {
        'checklist': dashboard.experiment_checklist.copy(),
        'checked': dashboard.checklist_checked.copy()
    }
    save_templates(templates)
    ui.notify(f'Template "{name}" saved.', type='positive')


def load_template(dashboard: DashboardState, name: str):
    """Load a template into the checklist."""
    if not name:
        ui.notify('Please select a template.', type='warning')
        return
    templates = load_templates()
    if name not in templates:
        ui.notify('Template not found.', type='negative')
        return
    template = templates[name]
    dashboard.experiment_checklist = template['checklist'].copy()
    dashboard.checklist_checked = template['checked'].copy()
    create_checklist_tab.refresh()
    ui.notify(f'Template "{name}" loaded.', type='positive')


def load_templates():
    """Load templates from file."""
    if not TEMPLATES_FILE.exists():
        return {}
    with open(TEMPLATES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_templates(templates):
    """Save templates to file."""
    with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=2)