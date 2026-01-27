#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TMS Dashboard - Intelligent Framework Auto-detection Entry Point

This script automatically detects and launches the appropriate dashboard framework.
Priority: NiceGUI → Streamlit
"""

import sys
from pathlib import Path
import traceback

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))


def main():
    """Main entry point with framework auto-detection."""
    
    # Mensagem de inicialização (apenas uma vez)
    print("Iniciando TMS Dashboard com NiceGUI...")
    print(f"Acesse: http://localhost:8084")
    
    # Try NiceGUI first
    try:
        from tms_dashboard.nicegui_app.run import main as nicegui_run
        nicegui_run()
        return
        
    except ImportError as e:
        traceback.print_exc()


if __name__ == "__main__":
    main()
