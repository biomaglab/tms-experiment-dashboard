#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client session management."""

import threading
from typing import Set, List
from .ui_state import DashboardUI

class ClientManager:
    """Manages active client sessions and their UI states.
    
    This class is thread-safe and allows broadcasting updates to all connected clients.
    """
    
    def __init__(self):
        self._clients: Set[DashboardUI] = set()
        self._lock = threading.Lock()
    
    def register(self, ui_state: DashboardUI):
        """Register a new client session."""
        with self._lock:
            self._clients.add(ui_state)
            # print(f"Client registered. Total clients: {len(self._clients)}")
            
    def unregister(self, ui_state: DashboardUI):
        """Unregister a client session."""
        with self._lock:
            if ui_state in self._clients:
                self._clients.remove(ui_state)
                # print(f"Client unregistered. Total clients: {len(self._clients)}")
                
    def get_all_clients(self) -> List[DashboardUI]:
        """Get a list of all active client UI states."""
        with self._lock:
            return list(self._clients)
