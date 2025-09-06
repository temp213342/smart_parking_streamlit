import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Reports - Vehicle Vacancy Vault",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("📊 Parking Reports & Analytics")
    st.markdown("*Comprehensive parking statistics and insights*")
    
    # Load parking data
    if 'parking_data' not in st.session_state:
        from utils.data_manager import DataManager
        data_manager = DataManager()
        st.session_state.parking_data = data_manager.load_parking_data()
    
    # Generate reports
    show_summary_stats()
    show_occupancy_charts()
    show_revenue_analysis()
    show_vehicle_type_breakdown()
    show_detailed_table()

def show_summary_stats():
    """Display summary statistics"""
    st.markdown("### 📈 Summary Statistics")
    
    parking_data = st.session_state.parking_data
    
    # Calculate stats
    total_slots = len(parking_data)
    available = sum(1 for slot in parking_data if slot['vehicleType'] is None and not slot['isReserved'])
    occupied = sum(1 for slot in parking_data if slot['vehicleType'] is not None)
    reserved = sum(1 for slot in parking_data if slot['isReserved'])
    total_revenue = sum(slot['charge'] for slot in parking_data if slot['charge'])
    
    # Occupancy rate
    occupancy_rate = (occupied / total_slots) * 100 if total_slots > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Slots", total_slots)
    
    with col2:
        st.metric("Available", available, delta=None)
    
    with col3:
        st.metric("Occupied", occupied, delta=None)
    
    with col4:
        st.metric("Reserved", reserved, delta=None)
    
    with col5:
        st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")
    
    # Revenue metrics
    st.markdown("#### 💰 Revenue Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"₹{total_revenue:.2f}")
    
    with col2:
        avg_revenue_per_slot = total_revenue / occupied if occupied > 0 else 0
        st.metric("Avg Revenue/Vehicle", f"₹{avg_revenue_per_slot:.2f}")
    
    with col3:
        # Estimate hourly revenue
        avg_hours_per_vehicle = 4  # Assume average 4 hours
        hourly_revenue = total_revenue / (occupied * avg_hours_per_vehicle) if occupied > 0 else 0
        st.metric("Est. Revenue/Hour", f"₹{hourly_revenue:.2f}")
    
    with col4:
        # Daily projection
        daily_projection = total_revenue * 3  # Assuming 3 turnovers per day
        st.metric("Daily Projection", f"₹{daily_projection:.2f}")

def show_occupancy_charts():
    """Display occupancy charts"""
    st.markdown("### 📊 Occupancy Analysis")
    
    parking_data = st.session_state.parking_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for slot status
        status_counts = {
            'Available': sum(1 for slot in parking_data if slot['vehicleType'] is None and not slot['isReserved']),
            'Occupied': sum(1 for slot in parking_data if slot['vehicleType'] is not None),
            'Reserved': sum(1 for slot in parking_data if slot['isReserved'])
        }
        
        fig_pie = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Slot Status Distribution",
            color_discrete_map={
                'Available': '#10b981',
                'Occupied': '#ef4444',
                'Reserved': '#f59e0b'
            }
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart for slot occupancy
        slot_numbers = [slot['slot'] for slot in parking_data]
        slot_status = []
        
        for slot in parking_data:
            if slot['vehicleType'] is not None:
                slot_status.append('Occupied')
            elif slot['isReserved']:
                slot_status.append('Reserved')
            else:
                slot_status.append('Available')
        
        fig_bar = px.bar(
            x=slot_numbers,
            y=[1] * len(slot_numbers),
            color=slot_status,
            title="Slot-wise Occupancy Status",
            labels={'x': 'Slot Number', 'y': 'Status'},
            color_discrete_map={
                'Available': '#10b981',
                'Occupied': '#ef4444',
                'Reserved': '#f59e0b'
            }
        )
        fig_bar.update_layout(showlegend=True, yaxis_title="Occupancy")
        st.plotly_chart(fig_bar, use_container_width=True)

def show_revenue_analysis():
    """Display revenue analysis"""
    st.markdown("### 💰 Revenue Analysis")
    
    parking_data = st.session_state.parking_data
    occupied_slots = [slot for slot in parking_data if slot['vehicleType'] is not None]
    
    if not occupied_slots:
        st.info("No occupied slots available for revenue analysis")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by vehicle type
        vehicle_revenue = {}
        for slot in occupied_slots:
            vehicle_type = slot['vehicleType']
            if vehicle_type not in vehicle_revenue:
                vehicle_revenue[vehicle_type] = 0
            vehicle_revenue[vehicle_type] += slot['charge']
        
        fig_revenue = px.bar(
            x=list(vehicle_revenue.keys()),
            y=list(vehicle_revenue.values()),
            title="Revenue by Vehicle Type",
            labels={'x': 'Vehicle Type', 'y': 'Revenue (₹)'},
            color=list(vehicle_revenue.values()),
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Revenue distribution
        charges = [slot['charge'] for slot in occupied_slots]
        
        fig_hist = px.histogram(
            charges,
            nbins=10,
            title="Revenue Distribution",
            labels={'value': 'Charge Amount (₹)', 'count': 'Number of Vehicles'},
            color_discrete_sequence=['#6366f1']
        )
        st.plotly_chart(fig_hist, use_container_width=True)

def show_vehicle_type_breakdown():
    """Display vehicle type breakdown"""
    st.markdown("### 🚗 Vehicle Type Analysis")
    
    parking_data = st.session_state.parking_data
    occupied_slots = [slot for slot in parking_data if slot['vehicleType'] is not None]
    
    if not occupied_slots:
        st.info("No occupied slots available for vehicle type analysis")
        return
    
    # Count vehicle types
    vehicle_counts = {}
    for slot in occupied_slots:
        vehicle_type = slot['vehicleType']
        if vehicle_type not in vehicle_counts:
            vehicle_counts[vehicle_type] = 0
        vehicle_counts[vehicle_type] += 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Vehicle type distribution
        fig_vehicle = px.pie(
            values=list(vehicle_counts.values()),
            names=list(vehicle_counts.keys()),
            title="Vehicle Type Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_vehicle, use_container_width=True)
    
    with col2:
        # Average charge by vehicle type
        vehicle_avg_charge = {}
        vehicle_charge_counts = {}
        
        for slot in occupied_slots:
            vehicle_type = slot['vehicleType']
            if vehicle_type not in vehicle_avg_charge:
                vehicle_avg_charge[vehicle_type] = 0
                vehicle_charge_counts[vehicle_type] = 0
            
            vehicle_avg_charge[vehicle_type] += slot['charge']
            vehicle_charge_counts[vehicle_type] += 1
        
        # Calculate averages
        for vehicle_type in vehicle_avg_charge:
            vehicle_avg_charge[vehicle_type] /= vehicle_charge_counts[vehicle_type]
        
        fig_avg = px.bar(
            x=list(vehicle_avg_charge.keys()),
            y=list(vehicle_avg_charge.values()),
            title="Average Charge by Vehicle Type",
            labels={'x': 'Vehicle Type', 'y': 'Average Charge (₹)'},
            color=list(vehicle_avg_charge.values()),
            color_continuous_scale='blues'
        )
        st.plotly_chart(fig_avg, use_container_width=True)

def show_detailed_table():
    """Display detailed parking data table"""
    st.markdown("### 📋 Detailed Parking Data")
    
    parking_data = st.session_state.parking_data
    
    # Prepare data for table
    table_data = []
    for slot in parking_data:
        if slot['vehicleType'] is not None:
            table_data.append({
                'Slot': slot['slot'],
                'Vehicle Type': slot['vehicleType'],
                'Vehicle Number': slot['vehicleNumber'],
                'Arrival Date': slot['arrivalDate'],
                'Arrival Time': slot['arrivalTime'],
                'Expected Pickup': f"{slot['expectedPickupDate']} {slot['expectedPickupTime']}",
                'Weekday': slot['weekday'],
                'Charge (₹)': slot['charge']
            })
        elif slot['isReserved']:
            reservation = slot['reservationData']
            table_data.append({
                'Slot': slot['slot'],
                'Vehicle Type': f"Reserved - {reservation['vehicleType']}",
                'Vehicle Number': reservation['vehicleNumber'],
                'Arrival Date': reservation['date'],
                'Arrival Time': reservation['time'],
                'Expected Pickup': f"Duration: {reservation['duration']} hours",
                'Weekday': 'Reserved',
                'Charge (₹)': 'TBD'
            })
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"parking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name=f"parking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    else:
        st.info("No parking data available for detailed view")

if __name__ == "__main__":
    main()
