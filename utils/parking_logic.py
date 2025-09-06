import datetime
from typing import Dict, List, Any, Tuple
import json

class ParkingLogic:
    def __init__(self):
        self.base_rates = {
            "Bike": 200,
            "Car": 150,
            "Truck": 300
        }
        
        self.surcharges = {
            "Bike": 50,
            "Car": 30,
            "Truck": 70
        }
        
        self.night_rate = 100
    
    def get_parking_stats(self, parking_data: List[Dict]) -> Dict[str, Any]:
        """Calculate parking statistics"""
        available = sum(1 for slot in parking_data if slot['vehicleType'] is None and not slot['isReserved'])
        occupied = sum(1 for slot in parking_data if slot['vehicleType'] is not None)
        reserved = sum(1 for slot in parking_data if slot['isReserved'])
        total_revenue = sum(slot['charge'] for slot in parking_data if slot['charge'])
        
        return {
            'available': available,
            'occupied': occupied,
            'reserved': reserved,
            'revenue': total_revenue,
            'total': len(parking_data)
        }
    
    def calculate_charge(self, vehicle_type: str, duration: int, arrival_time: str = None) -> Dict[str, Any]:
        """Calculate parking charge based on vehicle type, duration, and time"""
        if arrival_time is None:
            arrival_time = datetime.datetime.now().strftime('%H:%M')
        
        current_time = datetime.datetime.now()
        current_day = current_time.strftime('%A')
        
        base_rate = self.base_rates.get(vehicle_type, 150)
        surcharge = self.surcharges.get(vehicle_type, 30)
        
        # Check if it's night time (11 PM - 5 AM)
        hour = int(arrival_time.split(':')[0])
        is_night = hour >= 23 or hour < 5
        
        if is_night:
            rate_per_hour = self.night_rate
            total_surcharge = 0
            rush_hours = False
        else:
            # Check for rush hours
            is_friday_rush = current_day == 'Friday' and 17 <= hour <= 23
            is_weekend_rush = current_day in ['Saturday', 'Sunday'] and 11 <= hour <= 23
            
            rush_hours = is_friday_rush or is_weekend_rush
            
            if rush_hours:
                rate_per_hour = base_rate + surcharge
                total_surcharge = surcharge * duration
            else:
                rate_per_hour = base_rate
                total_surcharge = 0
        
        total_charge = rate_per_hour * duration
        
        return {
            'baseRate': base_rate,
            'surcharge': total_surcharge,
            'ratePerHour': rate_per_hour,
            'duration': duration,
            'total': total_charge,
            'rushHours': rush_hours,
            'nightRate': is_night
        }
    
    def park_vehicle(self, parking_data: List[Dict], vehicle_type: str, vehicle_number: str, duration: int) -> Dict[str, Any]:
        """Park a vehicle in the first available slot"""
        # Find first available slot
        for slot in parking_data:
            if slot['vehicleType'] is None and not slot['isReserved']:
                current_time = datetime.datetime.now()
                arrival_time = current_time.strftime('%H:%M')
                arrival_date = current_time.strftime('%d-%m-%y')
                weekday = current_time.strftime('%a')
                
                # Calculate expected pickup time
                pickup_time = current_time + datetime.timedelta(hours=duration)
                expected_pickup_date = pickup_time.strftime('%d-%m-%y')
                expected_pickup_time = pickup_time.strftime('%H:%M')
                
                # Calculate charge
                charge_info = self.calculate_charge(vehicle_type, duration, arrival_time)
                
                # Update slot
                slot.update({
                    'vehicleType': vehicle_type,
                    'vehicleNumber': vehicle_number,
                    'arrivalDate': arrival_date,
                    'arrivalTime': arrival_time,
                    'expectedPickupDate': expected_pickup_date,
                    'expectedPickupTime': expected_pickup_time,
                    'weekday': weekday,
                    'charge': charge_info['total']
                })
                
                return {
                    'success': True,
                    'slot': slot['slot'],
                    'data': parking_data,
                    'charge': charge_info
                }
        
        return {
            'success': False,
            'message': 'No available slots'
        }
    
    def remove_vehicle(self, parking_data: List[Dict], slot_number: int) -> Dict[str, Any]:
        """Remove vehicle from slot and generate bill"""
        slot = parking_data[slot_number - 1]
        
        if slot['vehicleType'] is None:
            return {
                'success': False,
                'message': 'Slot is already empty'
            }
        
        # Generate bill
        bill = {
            'slot': slot_number,
            'vehicleType': slot['vehicleType'],
            'vehicleNumber': slot['vehicleNumber'],
            'arrivalDate': slot['arrivalDate'],
            'arrivalTime': slot['arrivalTime'],
            'departureDate': datetime.datetime.now().strftime('%d-%m-%y'),
            'departureTime': datetime.datetime.now().strftime('%H:%M'),
            'duration': self._calculate_actual_duration(slot['arrivalDate'], slot['arrivalTime']),
            'baseRate': self._get_base_rate_from_charge(slot),
            'surcharge': self._get_surcharge_from_charge(slot),
            'total': slot['charge']
        }
        
        # Clear slot
        slot.update({
            'vehicleType': None,
            'vehicleNumber': None,
            'arrivalDate': None,
            'arrivalTime': None,
            'expectedPickupDate': None,
            'expectedPickupTime': None,
            'weekday': None,
            'charge': 0
        })
        
        return {
            'success': True,
            'data': parking_data,
            'bill': bill
        }
    
    def reserve_slot(self, parking_data: List[Dict], customer_name: str, vehicle_type: str, 
                    vehicle_number: str, date: str, time: str, duration: int) -> Dict[str, Any]:
        """Reserve the first available slot"""
        for slot in parking_data:
            if slot['vehicleType'] is None and not slot['isReserved']:
                slot.update({
                    'isReserved': True,
                    'reservationData': {
                        'customerName': customer_name,
                        'vehicleType': vehicle_type,
                        'vehicleNumber': vehicle_number,
                        'date': date,
                        'time': time,
                        'duration': duration
                    }
                })
                
                return {
                    'success': True,
                    'slot': slot['slot'],
                    'data': parking_data
                }
        
        return {
            'success': False,
            'message': 'No available slots for reservation'
        }
    
    def _calculate_actual_duration(self, arrival_date: str, arrival_time: str) -> int:
        """Calculate actual parking duration"""
        try:
            arrival_datetime = datetime.datetime.strptime(f"{arrival_date} {arrival_time}", '%d-%m-%y %H:%M')
            current_datetime = datetime.datetime.now()
            duration = (current_datetime - arrival_datetime).total_seconds() / 3600
            return max(1, int(duration))
        except:
            return 1
    
    def _get_base_rate_from_charge(self, slot: Dict) -> int:
        """Extract base rate from slot data"""
        vehicle_type = slot['vehicleType']
        return self.base_rates.get(vehicle_type, 150)
    
    def _get_surcharge_from_charge(self, slot: Dict) -> int:
        """Calculate surcharge from slot data"""
        # This is a simplified calculation
        # In a real implementation, you'd store more detailed pricing info
        return 0
