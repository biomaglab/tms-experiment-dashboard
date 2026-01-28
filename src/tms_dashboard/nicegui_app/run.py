#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiceGUI web application main entry point - Versão simplificada"""

import threading
import time
from nicegui import ui

from ..config import DEFAULT_HOST, DEFAULT_PORT, NICEGUI_PORT
from ..core.dashboard_state import DashboardState
from ..core.components.socket_client import SocketClient
from ..core.message_handler import MessageHandler
from .update_dashboard import UpdateDashboard
from .components import create_header, create_dashboard_tabs, create_checklist_tab
# Global shared instances (persist across all sessions)
dashboard = DashboardState()
socket_client = SocketClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
message_handler = MessageHandler(socket_client, dashboard)
update_dashboard = UpdateDashboard(dashboard)


# Flag to ensure background thread starts only once
_background_thread_started = False


def start_background_services():
    """Start background services (socket client and message processing thread).
    
    This function is called only once, regardless of how many sessions are created.
    """
    global _background_thread_started
    
    if _background_thread_started:
        return
    
    _background_thread_started = True
    
    # Background thread for message processing
    def process_messages_loop():
        """Continuously process messages and update dashboard."""
        while True:
            try:
                time.sleep(0.1)
                message_handler.process_messages()
                update_dashboard.update()
            except Exception:
                pass
    
    # Start message processing thread
    threading.Thread(target=process_messages_loop, daemon=True, name="MessageProcessor").start()
    
    # Start socket client
    socket_client.connect()
    
    print("✅ Background services started (socket client + message processor)")


@ui.page('/')
def index():
    """Main page builder - called for each new session/reload.
    
    Uses shared global dashboard instance, so state persists across reloads.
    """
    # Remove default body margins/padding and set gap to 0
    ui.add_head_html('''
        <style>
            :root {
                --nicegui-default-gap: 0;
            }
            body {
                margin: 0 !important;
                padding: 0 !important;
            }
        </style>
    ''')
    
    # Build UI using shared dashboard instance
    create_header(dashboard)
    
    # Main tabs
    with ui.tabs().classes('w-full') as tabs:
        dashboard_tab = ui.tab('Dashboard')
        checklist_tab = ui.tab('Checklist')
    
    with ui.tab_panels(tabs, value=dashboard_tab).classes('w-full').style('height: calc(100vh - 110px);'):
        with ui.tab_panel(dashboard_tab):
            create_dashboard_tabs(dashboard)
        
        with ui.tab_panel(checklist_tab):
            create_checklist_tab(dashboard)


def main():
    """Main entry point for NiceGUI application."""
    
    # Start background services once
    start_background_services()
    
    # Run NiceGUI server
    ui.run(
        port=NICEGUI_PORT,
        reload=False,
        show=False,
        title="TMS Dashboard",
        favicon="🧠"
    )


if __name__ == "__main__":
    print("🚀 Starting TMS Dashboard with NiceGUI...")
    print(f"📡 Acess: http://localhost:{NICEGUI_PORT}")
    main()
