#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Socket.IO client isolado em thread - Versão simplificada"""

import time
import socketio
import threading
from queue import Queue
from typing import Optional
import logging

# Suppress verbose socketio logs
logging.getLogger('socketio').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)


class SocketClient:
    """Socket.IO client que roda em thread dedicada para não bloquear NiceGUI."""
    
    def __init__(self, remote_host: str):
        """Initialize socket client.
        
        Args:
            remote_host: URL do relay server (ex: 'http://127.0.0.1:5000')
        """
        self.__remote_host = remote_host
        self.__buffer: Queue = Queue()
        self.__connected = False
        self.__thread: Optional[threading.Thread] = None
        self.__stop_event = threading.Event()
        self.__sio: Optional[socketio.Client] = None
    
    def __run_in_thread(self):
        """Executa Socket.IO client em thread isolada."""
        # Criar novo cliente Socket.IO nesta thread
        self.__sio = socketio.Client(
            logger=False,
            engineio_logger=False,
            reconnection=True,
            reconnection_attempts=0,  # Infinite retries
            reconnection_delay=1,
            reconnection_delay_max=5
        )
        
        # Registrar callbacks
        @self.__sio.event
        def connect():
            print(f"✓ Socket.IO connected to {self.__remote_host}")
            self.__connected = True
        
        @self.__sio.event
        def disconnect():
            print("⚠ Socket.IO disconnected (will auto-reconnect)")
            self.__connected = False
        
        @self.__sio.event
        def connect_error(data):
            self.__connected = False
        
        @self.__sio.on('to_robot')
        def on_to_robot(msg):
            """Recebe mensagens do canal to_robot."""
            self.__buffer.put(msg)
        
        @self.__sio.on('to_neuronavigation')
        def on_to_neuronavigation(msg):
            """Recebe mensagens do canal to_neuronavigation."""
            self.__buffer.put(msg)
        
        # Loop de conexão com retry
        while not self.__stop_event.is_set():
            try:
                if not self.__sio.connected:
                    print(f"Connecting to {self.__remote_host}...")
                    self.__sio.connect(
                        self.__remote_host,
                        wait_timeout=5,
                        transports=['websocket', 'polling']
                    )
                    # Manter conexão viva
                    while self.__sio.connected and not self.__stop_event.is_set():
                        time.sleep(1)
                        
            except Exception as e:
                if not self.__stop_event.is_set():
                    print(f"Connection error: {e}, retrying in 2s...")
                    time.sleep(2)
        
        # Cleanup
        if self.__sio and self.__sio.connected:
            self.__sio.disconnect()
    
    def connect(self):
        """Inicia Socket.IO client em thread isolada (não bloqueia)."""
        if self.__thread is None or not self.__thread.is_alive():
            self.__stop_event.clear()
            self.__thread = threading.Thread(
                target=self.__run_in_thread,
                daemon=True,
                name="SocketIO-IsolatedThread"
            )
            self.__thread.start()
            print("✓ Socket.IO client started in isolated thread")
    
    def disconnect(self):
        """Para o Socket.IO client."""
        self.__stop_event.set()
        if self.__thread and self.__thread.is_alive():
            self.__thread.join(timeout=5)

    def emit_event(self, event: str, msg):
        """Emit an event to the relay server if connected.

        Args:
            event: Socket.IO event name (e.g., 'from_robot')
            msg: Any JSON-serializable payload
        """
        if self.__sio is None:
            print(f"[SocketClient] Cannot emit, client not initialized (event={event})")
            return False
        try:
            # emit is thread-safe in python-socketio
            self.__sio.emit(event, msg)
            return True
        except Exception as e:
            print(f"[SocketClient] Error emitting event '{event}': {e}")
            return False
    
    def get_buffer(self) -> list:
        """Retorna todas as mensagens do buffer (não bloqueia).
        
        Returns:
            Lista de mensagens recebidas desde a última chamada
        """
        messages = []
        while not self.__buffer.empty():
            try:
                messages.append(self.__buffer.get_nowait())
            except:
                break
        return messages
    
    @property
    def is_connected(self) -> bool:
        """Verifica se está conectado ao servidor."""
        return self.__connected
