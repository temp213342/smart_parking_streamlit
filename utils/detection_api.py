import requests
from typing import Dict, Any, Optional
import time
import streamlit as st

import requests
from typing import Dict, Any, Optional
import streamlit as st
import os

class DetectionAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.is_cloud_deployment = self._check_if_cloud_deployment()
    
    def _check_if_cloud_deployment(self) -> bool:
        """Check if running in Streamlit Cloud or other remote environment"""
        # Streamlit Cloud sets these environment variables
        return (
            os.getenv('STREAMLIT_SHARING_MODE') is not None or
            os.getenv('STREAMLIT_SERVER_HEADLESS') == 'true' or
            'streamlit.app' in os.getenv('HOSTNAME', '') or
            'streamlit.app' in os.getenv('SERVER_NAME', '')
        )
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the detection server is running"""
        if self.is_cloud_deployment:
            return {
                "status": "cloud_deployment",
                "message": "AI detection is not available in cloud deployment. Please use manual mode."
            }
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Server not available: {str(e)}"}
    
    def start_detection(self) -> Dict[str, Any]:
        """Start the AI detection process"""
        if self.is_cloud_deployment:
            return {
                "status": "cloud_deployment",
                "message": "AI detection is not available in cloud deployment"
            }
        
        try:
            response = requests.post(f"{self.base_url}/start_detection", timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Connection error: {str(e)}"}
    
    # ... other methods with similar cloud deployment checks

    
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

