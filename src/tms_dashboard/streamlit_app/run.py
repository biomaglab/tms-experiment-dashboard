#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Streamlit web application main entry point"""

import streamlit as st
import threading
import time

from ..config import DEFAULT_HOST, DEFAULT_PORT
from ..core.dashboard_state import DashboardState
from ..core.socket_client import SocketClient
from ..core.message_handler import MessageHandler


def main():
    """Main entry point for Streamlit application."""
    
    st.set_page_config(
        page_title="TMS Experiment Dashboard",
        page_icon="🧠",
        layout="wide"
    )
    
    # Initialize session state
    if 'dashboard' not in st.session_state:
        st.session_state.dashboard = DashboardState()
        st.session_state.socket_client = SocketClient(f"http://{DEFAULT_HOST}:{DEFAULT_PORT}")
        st.session_state.message_handler = MessageHandler(
            st.session_state.socket_client,
            st.session_state.dashboard
        )
        
        # Connect to relay server
        st.session_state.socket_client.connect()
        
        # Start background message processing
        def process_messages_loop():
            while True:
                time.sleep(0.5)
                st.session_state.message_handler.process_messages()
        
        threading.Thread(target=process_messages_loop, daemon=True).start()
    
    # Header
    st.title("🧠 Biomag TMS Dashboard")
    st.markdown("---")
    
    # Main content
    st.header("Streamlit Implementation")
    st.info("""
    This is a placeholder Streamlit implementation.
    
    Full UI will be migrated from the existing streamlit/ folder files,
    using the shared core modules (DashboardState, SocketClient, MessageHandler).
    
    The modular structure allows both NiceGUI and Streamlit to coexist,
    sharing the same business logic while having framework-specific UIs.
    """)
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    dashboard = st.session_state.dashboard
    
    with col1:
        st.metric("Project", "✅" if dashboard.project_set else "❌")
    with col2:
        st.metric("Camera", "✅" if dashboard.camera_set else "❌")
    with col3:
        st.metric("Robot", "✅" if dashboard.robot_set else "❌")
    with col4:
        st.metric("TMS", "✅" if dashboard.tms_set else "❌")
    
    # Auto refresh
    if st.button("🔄 Refresh Status"):
        st.rerun()


if __name__ == "__main__":
    main()
