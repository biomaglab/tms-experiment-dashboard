# tms_dashboard/utils/latency.py

import time
import csv
from pathlib import Path

LOG_FILE = Path("latency_log.csv")

def now():
    # best high-precision monotonic clock (Windows safe)
    return time.perf_counter_ns()

def to_ms(start, end):
    return (end - start) / 1e6

def log_latency(name: str, value: float):
    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow([time.time(), name, value])
