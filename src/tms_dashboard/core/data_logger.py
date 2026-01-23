#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data logger for experiment data"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class DataLogger:
    """Handles logging of experiment data to CSV files."""
    
    def __init__(self, output_path: Path):
        """Initialize data logger.
        
        Args:
            output_path: Path to CSV file for logging
        """
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def save_experiment_data(self, data: Dict[str, Any]) -> bool:
        """Save experiment data to CSV file.
        
        Args:
            data: Dictionary with experiment data fields
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file_exists = self.output_path.exists()
            
            with open(self.output_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header if file doesn't exist
                if not file_exists:
                    headers = ["Timestamp"] + list(data.keys())
                    writer.writerow(headers)
                
                # Write data row
                row = [timestamp] + list(data.values())
                writer.writerow(row)
            
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    @staticmethod
    def create_experiment_dict(
        experiment_name: str = "",
        experiment_description: str = "",
        start_date: str = "",
        end_date: str = "",
        experiment_details: str = "",
        experiment_checklist: list = None,
        conditioning_stimulus: str = "",
        test_stimulus: str = "",
        number_intervals: str = "",
        interval_step: str = "",
        number_trials: str = "",
        number_conditions: str = "",
        trials_per_condition: str = "",
        intertrial_interval: str = ""
    ) -> Dict[str, str]:
        """Create a dictionary with experiment data for logging.
        
        Args:
            All experiment parameters as strings
            
        Returns:
            Dictionary with labeled experiment data
        """
        if experiment_checklist is None:
            experiment_checklist = []
        
        return {
            "Experiment Name": experiment_name,
            "Experiment Description": experiment_description,
            "Start Date": start_date,
            "End Date": end_date,
            "Experiment Details": experiment_details,
            "Experiment Checklist": "; ".join(experiment_checklist),  # Join list into string for CSV
            "Conditioning Stimulus": conditioning_stimulus,
            "Test Stimulus": test_stimulus,
            "Number of Intervals": number_intervals,
            "Interval Step (ms)": interval_step,
            "Number of Trials": number_trials,
            "Number of Conditions": number_conditions,
            "Trials per Condition": trials_per_condition,
            "Inter-trial Interval (ms)": intertrial_interval
        }
