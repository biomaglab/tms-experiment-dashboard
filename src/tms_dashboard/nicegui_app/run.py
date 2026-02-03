#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NiceGUI web application main entry point - Versão simplificada"""

import threading
import time
from nicegui import ui
import traceback
import numpy as np

from tms_dashboard.config import DEFAULT_HOST, DEFAULT_PORT, NICEGUI_PORT
from tms_dashboard.constants import TriggerType
from tms_dashboard.core.dashboard_state import DashboardState
from tms_dashboard.core.modules.socket_client import SocketClient
from tms_dashboard.core.modules.emg_connection import neuroOne
from tms_dashboard.core.message_handler import MessageHandler
from tms_dashboard.core.message_emit import Message2Server
from tms_dashboard.nicegui_app.update_dashboard import UpdateDashboard
from tms_dashboard.nicegui_app.ui import create_header, create_dashboard_tabs

# Global shared instances (persist across all sessions)
dashboard = DashboardState()
socket_client = SocketClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
message_handler = MessageHandler(socket_client, dashboard)
neuroone_connection = neuroOne(num_trial=20, t_min=-5, t_max=40, ch=33, trigger_type_interest=TriggerType.STIMULUS)
update_dashboard = UpdateDashboard(dashboard, neuroone_connection)
message_emit = Message2Server(socket_client, dashboard)

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

                if neuroone_connection.get_connection() and neuroone_connection.get_status():
                    dashboard.mep_sampling_rate = neuroone_connection.get_sampling_rate()
                    mep_history = list(neuroone_connection.get_triggered_window())
                    dashboard.update_mep_history(mep_history,
                                                neuroone_connection.t_min,
                                                neuroone_connection.t_max,
                                                dashboard.mep_sampling_rate)
                else:
                    if dashboard.get_all_state_mep():
                        dashboard.reset_all_state_mep()
                
                update_dashboard.update()
                if dashboard.status_new_mep:
                    new_meps_only = [dashboard.mep_history_baseline[i] for i in dashboard.new_meps_index]
                    message_emit.send_mep_value(new_meps_only)

                    
            except Exception as e:
                print("Error processing messages", e)
                traceback.print_exc()

    # Start socket client
    socket_client.connect()
    neuroone_connection.start()
    
    # Start message processing thread
    threading.Thread(target=process_messages_loop, daemon=True, name="MessageProcessor").start()
    
    
    print("Background services started (socket client + message processor)")


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
    create_dashboard_tabs(dashboard, message_emit)


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
