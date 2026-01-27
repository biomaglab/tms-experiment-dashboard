#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuration settings for TMS Experiment Dashboard"""

from enum import Enum
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
STATIC_DIR = PROJECT_ROOT / "src" / "tms_dashboard" / "static"
IMAGES_DIR = STATIC_DIR / "images"

# Socket connection settings
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 5000

# Alternative hosts (commented out for reference)
# HOST_IP_1 = '169.254.128.134'
# HOST_IP_2 = '169.254.52.180'
# HOST_IP_3 = '192.168.200.202'

# NiceGUI settings
NICEGUI_PORT = 8084
NICEGUI_RELOAD = False

# CSV output settings
CSV_FILE = 'nice_details.csv'
CSV_PATH = DATA_DIR / CSV_FILE

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

class TriggerType(Enum):
    DISABLED = 0
    STIMULUS = 1
    VIDEO = 2
    MUTE = 3
    PARALLEL = 4



