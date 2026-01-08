#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TMS Dashboard - Intelligent Framework Auto-detection Entry Point

This script automatically detects and launches the appropriate dashboard framework.
Priority: NiceGUI → Streamlit
"""

import sys


def main():
    """Main entry point with framework auto-detection."""
    
    # Mensagem de inicialização (apenas uma vez)
    print("🚀 Iniciando TMS Dashboard com NiceGUI...")
    print(f"📡 Acesse: http://localhost:8084")
    
    # Try NiceGUI first
    try:
        from src.tms_dashboard.nicegui_app.run import main as nicegui_run
        nicegui_run()
        return
        
    except ImportError as e:
        print(f"\n⚠️  NiceGUI not available: {e}")
        print("Trying Streamlit...")
    
    # Fallback to Streamlit
    try:
        from src.tms_dashboard.streamlit_app.run import main as streamlit_run
        streamlit_run()
        return
        
    except ImportError:
        print("\n❌ Error: No framework available!")
        print("\nPlease install a framework:")
        print("  For NiceGUI: uv sync --extra nicegui")
        print("  For Streamlit: uv sync --extra streamlit")
        print("  For both: uv sync --extra all")
        sys.exit(1)


if __name__ == "__main__":
    main()
