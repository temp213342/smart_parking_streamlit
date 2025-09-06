import requests
from typing import Dict, Any, Optional
import time
import streamlit as st

class DetectionAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def start_detection(self) -> Dict[str, Any]:
        """Start the AI detection process"""
        try:
            response = requests.post(f"{self.base_url}/start_detection", timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Connection error: {str(e)}"}
    
    def get_results(self) -> Dict[str, Any]:
        """Get current detection results"""
        try:
            response = requests.get(f"{self.base_url}/get_results", timeout=5)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Connection error: {str(e)}"}
    
    def reset_detection(self) -> Dict[str, Any]:
        """Reset the detection system"""
        try:
            response = requests.post(f"{self.base_url}/reset", timeout=5)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Connection error: {str(e)}"}
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the detection server is running"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Server not available: {str(e)}"}
