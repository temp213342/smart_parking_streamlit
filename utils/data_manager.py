import json
import os
from pathlib import Path
from typing import Dict, List, Any
import datetime

class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.parking_file = self.data_dir / "parking_data.json"
        self.holidays_file = self.data_dir / "holidays.json"
    
    def load_parking_data(self) -> List[Dict[str, Any]]:
        """Load parking data from JSON file or initialize with sample data"""
        if self.parking_file.exists():
            with open(self.parking_file, 'r') as f:
                return json.load(f)
        else:
            return self._initialize_parking_data()
    
    def save_parking_data(self, data: List[Dict[str, Any]]) -> None:
        """Save parking data to JSON file"""
        with open(self.parking_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_holidays(self) -> List[Dict[str, Any]]:
        """Load holiday data from JSON file"""
        if self.holidays_file.exists():
            with open(self.holidays_file, 'r') as f:
                return json.load(f)
        else:
            return self._initialize_holidays()
    
    def _initialize_parking_data(self) -> List[Dict[str, Any]]:
        """Initialize parking data with 20 empty slots and sample occupied slots"""
        parking_data = []
        
        # Initialize 20 empty slots
        for i in range(1, 21):
            parking_data.append({
                "slot": i,
                "vehicleType": None,
                "vehicleNumber": None,
                "arrivalDate": None,
                "arrivalTime": None,
                "expectedPickupDate": None,
                "expectedPickupTime": None,
                "weekday": None,
                "charge": 0,
                "isReserved": False,
                "reservationData": None
            })
        
        # Add sample data (from your original JavaScript)
        sample_data = [
            {"slot": 2, "vehicleType": "Bike", "vehicleNumber": "WB02B5678", "arrivalDate": "01-02-25", "arrivalTime": "09:30", "expectedPickupDate": "01-02-25", "expectedPickupTime": "12:00", "weekday": "Mon", "charge": 450.0},
            {"slot": 4, "vehicleType": "Car", "vehicleNumber": "WB01A1234", "arrivalDate": "01-02-25", "arrivalTime": "10:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "14:00", "weekday": "Mon", "charge": 800.0},
            {"slot": 6, "vehicleType": "Truck", "vehicleNumber": "WB03C9101", "arrivalDate": "01-02-25", "arrivalTime": "08:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "16:00", "weekday": "Mon", "charge": 2400.0},
            {"slot": 8, "vehicleType": "Car", "vehicleNumber": "WB04D1121", "arrivalDate": "31-01-25", "arrivalTime": "22:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "06:00", "weekday": "Tue", "charge": 1600.0},
            {"slot": 9, "vehicleType": "Bike", "vehicleNumber": "WB05E3141", "arrivalDate": "01-02-25", "arrivalTime": "15:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "18:00", "weekday": "Mon", "charge": 510.0},
            {"slot": 11, "vehicleType": "Truck", "vehicleNumber": "WB06F7171", "arrivalDate": "01-02-25", "arrivalTime": "19:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "23:00", "weekday": "Mon", "charge": 1200.0},
            {"slot": 13, "vehicleType": "Car", "vehicleNumber": "WB07G8181", "arrivalDate": "01-02-25", "arrivalTime": "07:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "11:00", "weekday": "Mon", "charge": 1000.0},
            {"slot": 15, "vehicleType": "Bike", "vehicleNumber": "WB08H9191", "arrivalDate": "01-02-25", "arrivalTime": "21:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "23:00", "weekday": "Mon", "charge": 400.0},
            {"slot": 17, "vehicleType": "Truck", "vehicleNumber": "WB09I2121", "arrivalDate": "01-02-25", "arrivalTime": "12:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "18:00", "weekday": "Mon", "charge": 1800.0},
            {"slot": 19, "vehicleType": "Car", "vehicleNumber": "WB10J3131", "arrivalDate": "01-02-25", "arrivalTime": "20:00", "expectedPickupDate": "01-02-25", "expectedPickupTime": "22:00", "weekday": "Mon", "charge": 400.0}
        ]
        
        # Apply sample data
        for data in sample_data:
            parking_data[data["slot"] - 1].update(data)
        
        # Add sample reservation to slot 3
        parking_data[2].update({
            "isReserved": True,
            "reservationData": {
                "customerName": "John Doe",
                "vehicleType": "Car",
                "vehicleNumber": "WB11X1234",
                "date": "01-02-25",
                "time": "14:00",
                "duration": 3
            }
        })
        
        self.save_parking_data(parking_data)
        return parking_data
    
    def _initialize_holidays(self) -> List[Dict[str, Any]]:
        """Initialize holiday data"""
        holidays = [
            {"date": "01-01-2025", "name": "New Year's Day", "rushFrom": "00:00", "rushTo": "23:59"},
            {"date": "26-01-2025", "name": "Republic Day", "rushFrom": "08:00", "rushTo": "14:00"},
            {"date": "02-02-2025", "name": "Vasant Panchami", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "26-02-2025", "name": "Maha Shivaratri", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "13-03-2025", "name": "Holika Dahana", "rushFrom": "09:00", "rushTo": "22:00"},
            {"date": "14-03-2025", "name": "Holi", "rushFrom": "09:00", "rushTo": "20:00"},
            {"date": "28-03-2025", "name": "Jamat Ul-Vida", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "30-03-2025", "name": "Chaitra Sukhladi / Ugadi / Gudi Padwa", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "31-03-2025", "name": "Eid-ul-Fitr", "rushFrom": "08:00", "rushTo": "21:00"},
            {"date": "06-04-2025", "name": "Rama Navami", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "10-04-2025", "name": "Mahavir Jayanti", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "18-04-2025", "name": "Good Friday", "rushFrom": "08:00", "rushTo": "16:00"},
            {"date": "12-05-2025", "name": "Buddha Purnima", "rushFrom": "09:00", "rushTo": "18:00"},
            {"date": "07-06-2025", "name": "Eid ul-Adha (Bakrid)", "rushFrom": "08:00", "rushTo": "21:00"},
            {"date": "06-07-2025", "name": "Muharram", "rushFrom": "07:00", "rushTo": "19:00"},
            {"date": "09-08-2025", "name": "Raksha Bandhan", "rushFrom": "10:00", "rushTo": "18:00"},
            {"date": "15-08-2025", "name": "Independence Day", "rushFrom": "08:00", "rushTo": "14:00"},
            {"date": "16-08-2025", "name": "Janmashtami", "rushFrom": "08:00", "rushTo": "23:00"},
            {"date": "27-08-2025", "name": "Ganesh Chaturthi", "rushFrom": "08:00", "rushTo": "21:00"},
            {"date": "05-09-2025", "name": "Milad-un-Nabi / Onam", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "29-09-2025", "name": "Maha Saptami", "rushFrom": "06:00", "rushTo": "23:59"},
            {"date": "30-09-2025", "name": "Maha Ashtami", "rushFrom": "06:00", "rushTo": "23:59"},
            {"date": "01-10-2025", "name": "Maha Navami", "rushFrom": "06:00", "rushTo": "23:59"},
            {"date": "02-10-2025", "name": "Mahatma Gandhi Jayanti / Dussehra", "rushFrom": "08:00", "rushTo": "17:00"},
            {"date": "07-10-2025", "name": "Maharishi Valmiki Jayanti", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "20-10-2025", "name": "Diwali", "rushFrom": "10:00", "rushTo": "23:59"},
            {"date": "22-10-2025", "name": "Govardhan Puja", "rushFrom": "09:00", "rushTo": "18:00"},
            {"date": "23-10-2025", "name": "Bhai Duj", "rushFrom": "10:00", "rushTo": "18:00"},
            {"date": "05-11-2025", "name": "Guru Nanak Jayanti", "rushFrom": "09:00", "rushTo": "19:00"},
            {"date": "24-11-2025", "name": "Guru Tegh Bahadur's Martyrdom Day", "rushFrom": "09:00", "rushTo": "17:00"},
            {"date": "25-12-2025", "name": "Christmas Day", "rushFrom": "09:00", "rushTo": "22:00"},
            {"date": "31-12-2025", "name": "New Year's Eve", "rushFrom": "00:00", "rushTo": "23:59"}
        ]
        
        with open(self.holidays_file, 'w') as f:
            json.dump(holidays, f, indent=2)
        
        return holidays
