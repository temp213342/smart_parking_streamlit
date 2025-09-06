import streamlit as st
import json
import datetime
from pathlib import Path
import pandas as pd
from utils.data_manager import DataManager
from utils.parking_logic import ParkingLogic

# Page config
st.set_page_config(
    page_title="Vehicle Vacancy Vault",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data manager
@st.cache_resource
def init_data_manager():
    return DataManager()

@st.cache_resource
def init_parking_logic():
    return ParkingLogic()

# Load custom CSS
def load_css():
    css_file = Path("styles/main.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main page
def main():
    load_css()
    
    # Initialize session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    if 'parking_data' not in st.session_state:
        data_manager = init_data_manager()
        st.session_state.parking_data = data_manager.load_parking_data()
    
    if 'selected_slot' not in st.session_state:
        st.session_state.selected_slot = None
    
    # Header with theme toggle
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown("# 🚗 Vehicle Vacancy Vault")
        st.markdown("*Smart Parking Management System*")
    
    with col2:
        # Real-time stats
        parking_logic = init_parking_logic()
        stats = parking_logic.get_parking_stats(st.session_state.parking_data)
        
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        with stat_col1:
            st.metric("Available", stats['available'], delta=None)
        with stat_col2:
            st.metric("Occupied", stats['occupied'], delta=None)
        with stat_col3:
            st.metric("Reserved", stats['reserved'], delta=None)
        with stat_col4:
            st.metric("Revenue Today", f"₹{stats['revenue']}")
    
    with col3:
        # Theme toggle
        theme_options = {"🌙 Dark": "dark", "☀️ Light": "light"}
        selected_theme = st.selectbox(
            "Theme",
            options=list(theme_options.keys()),
            index=0 if st.session_state.theme == 'dark' else 1,
            key="theme_selector"
        )
        st.session_state.theme = theme_options[selected_theme]
    
    # Current time
    current_time = datetime.datetime.now()
    st.markdown(f"**Current Time:** {current_time.strftime('%A, %B %d, %Y - %I:%M:%S %p')}")
    
    # Pricing information
    show_pricing_info()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_parking_grid()
    
    with col2:
        show_control_panel()

def show_pricing_info():
    st.markdown("### 💰 Pricing Information")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="price-card">
            <h4>🏍️ Bikes</h4>
            <p>₹200/hour</p>
            <small>+₹50 rush hour surcharge</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="price-card">
            <h4>🚗 Cars</h4>
            <p>₹150/hour</p>
            <small>+₹30 rush hour surcharge</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="price-card">
            <h4>🚛 Trucks</h4>
            <p>₹300/hour</p>
            <small>+₹70 rush hour surcharge</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="price-card">
            <h4>🌙 Night Rate</h4>
            <p>₹100/hour</p>
            <small>11 PM - 5 AM (All vehicles)</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("**Rush hours:** Fridays 5PM-12AM, Weekends 11AM-12AM, Holidays as scheduled")

def show_parking_grid():
    st.markdown("### 🅿️ Parking Layout")
    
    # Create 5x4 grid for 20 slots
    for row in range(5):
        cols = st.columns(4)
        for col_idx, col in enumerate(cols):
            slot_num = row * 4 + col_idx + 1
            slot_data = st.session_state.parking_data[slot_num - 1]
            
            with col:
                if slot_data['vehicleType'] is None and not slot_data['isReserved']:
                    # Available slot
                    if st.button(f"🟢 Slot {slot_num}\nAvailable", 
                               key=f"slot_{slot_num}",
                               help="Click to park a vehicle"):
                        st.session_state.selected_slot = slot_num
                        st.rerun()
                
                elif slot_data['isReserved']:
                    # Reserved slot
                    reservation = slot_data['reservationData']
                    if st.button(f"🟡 Slot {slot_num}\nReserved\n{reservation['vehicleType']}", 
                               key=f"slot_{slot_num}",
                               help=f"Reserved for {reservation['customerName']}"):
                        show_reservation_details(slot_data)
                
                else:
                    # Occupied slot
                    if st.button(f"🔴 Slot {slot_num}\nOccupied\n{slot_data['vehicleType']}\n{slot_data['vehicleNumber']}", 
                               key=f"slot_{slot_num}",
                               help="Click to remove vehicle or view details"):
                        show_vehicle_details(slot_data)
    
    # Legend
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🟢 **Available** - Ready for parking")
    with col2:
        st.markdown("🔴 **Occupied** - Vehicle parked")
    with col3:
        st.markdown("🟡 **Reserved** - Slot reserved")

def show_control_panel():
    st.markdown("### 🎛️ Controls")
    
    # Auto Mode Button
    if st.button("🤖 Auto Mode", help="AI-powered automatic vehicle detection"):
        st.switch_page("pages/04_🤖_Auto_Mode.py")
    
    st.markdown("---")
    
    # Manual parking form
    st.markdown("#### 🚗 Park Vehicle")
    
    with st.form("park_vehicle_form"):
        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["Bike", "Car", "Truck"],
            key="manual_vehicle_type"
        )
        
        vehicle_number = st.text_input(
            "Vehicle Number",
            placeholder="e.g., MH01AB1234",
            key="manual_vehicle_number"
        ).upper()
        
        duration = st.number_input(
            "Parking Duration (hours)",
            min_value=1,
            max_value=24,
            value=2,
            key="manual_duration"
        )
        
        submitted = st.form_submit_button("🅿️ Park Vehicle")
        
        if submitted:
            if vehicle_number:
                parking_logic = init_parking_logic()
                result = parking_logic.park_vehicle(
                    st.session_state.parking_data,
                    vehicle_type,
                    vehicle_number,
                    duration
                )
                
                if result['success']:
                    st.success(f"Vehicle parked in slot {result['slot']}!")
                    st.session_state.parking_data = result['data']
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.error("Please enter vehicle number")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("#### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Search Vehicle"):
            show_search_dialog()
        
        if st.button("📊 Generate Report"):
            st.switch_page("pages/02_📊_Reports.py")
    
    with col2:
        if st.button("🎯 Reserve Slot"):
            show_reservation_dialog()
        
        if st.button("📅 Holiday Calendar"):
            st.switch_page("pages/03_📅_Holiday_Calendar.py")

def show_vehicle_details(slot_data):
    with st.expander(f"Vehicle Details - Slot {slot_data['slot']}", expanded=True):
        st.write(f"**Vehicle Type:** {slot_data['vehicleType']}")
        st.write(f"**Vehicle Number:** {slot_data['vehicleNumber']}")
        st.write(f"**Arrival:** {slot_data['arrivalDate']} at {slot_data['arrivalTime']}")
        st.write(f"**Expected Departure:** {slot_data['expectedPickupDate']} at {slot_data['expectedPickupTime']}")
        st.write(f"**Current Charge:** ₹{slot_data['charge']}")
        
        if st.button(f"🚗 Remove Vehicle from Slot {slot_data['slot']}", key=f"remove_{slot_data['slot']}"):
            remove_vehicle(slot_data['slot'])

def remove_vehicle(slot_num):
    parking_logic = init_parking_logic()
    result = parking_logic.remove_vehicle(st.session_state.parking_data, slot_num)
    
    if result['success']:
        st.success(f"Vehicle removed from slot {slot_num}")
        st.session_state.parking_data = result['data']
        
        # Show bill
        show_bill(result['bill'])
        st.rerun()
    else:
        st.error(result['message'])

def show_bill(bill_data):
    st.markdown("### 🧾 Parking Bill")
    
    st.markdown(f"""
    <div class="bill">
        <div class="bill-header">
            <h3>Vehicle Vacancy Vault</h3>
            <p>Smart Parking Management System</p>
            <p>{datetime.datetime.now().strftime('%B %d, %Y - %I:%M:%S %p')}</p>
        </div>
        
        <div class="bill-details">
            <div class="bill-row">
                <span>Vehicle Type:</span>
                <span>{bill_data['vehicleType']}</span>
            </div>
            <div class="bill-row">
                <span>Vehicle Number:</span>
                <span>{bill_data['vehicleNumber']}</span>
            </div>
            <div class="bill-row">
                <span>Slot Number:</span>
                <span>{bill_data['slot']}</span>
            </div>
            <div class="bill-row">
                <span>Parking Duration:</span>
                <span>{bill_data['duration']} hours</span>
            </div>
            <div class="bill-row">
                <span>Base Rate:</span>
                <span>₹{bill_data['baseRate']}/hour</span>
            </div>
            <div class="bill-row">
                <span>Rush Hour Surcharge:</span>
                <span>₹{bill_data['surcharge']}</span>
            </div>
            <div class="bill-total">
                <div class="bill-row">
                    <span><strong>Total Amount:</strong></span>
                    <span><strong>₹{bill_data['total']}</strong></span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_search_dialog():
    st.markdown("### 🔍 Search Vehicle")
    search_term = st.text_input("Enter vehicle number to search:", key="search_input")
    
    if search_term:
        results = []
        for slot_data in st.session_state.parking_data:
            if slot_data['vehicleNumber'] and search_term.upper() in slot_data['vehicleNumber'].upper():
                results.append(slot_data)
        
        if results:
            for result in results:
                st.success(f"Found in Slot {result['slot']}: {result['vehicleType']} - {result['vehicleNumber']}")
        else:
            st.warning("Vehicle not found")

def show_reservation_dialog():
    st.markdown("### 🎯 Reserve Slot")
    
    with st.form("reservation_form"):
        customer_name = st.text_input("Customer Name")
        vehicle_type = st.selectbox("Vehicle Type", ["Bike", "Car", "Truck"])
        vehicle_number = st.text_input("Vehicle Number").upper()
        
        col1, col2 = st.columns(2)
        with col1:
            arrival_date = st.date_input("Expected Arrival Date")
        with col2:
            arrival_time = st.time_input("Expected Arrival Time")
        
        duration = st.number_input("Expected Duration (hours)", min_value=1, max_value=24, value=2)
        
        if st.form_submit_button("Reserve Slot"):
            if customer_name and vehicle_number:
                parking_logic = init_parking_logic()
                result = parking_logic.reserve_slot(
                    st.session_state.parking_data,
                    customer_name,
                    vehicle_type,
                    vehicle_number,
                    arrival_date.strftime('%d-%m-%y'),
                    arrival_time.strftime('%H:%M'),
                    duration
                )
                
                if result['success']:
                    st.success(f"Slot {result['slot']} reserved successfully!")
                    st.session_state.parking_data = result['data']
                    st.rerun()
                else:
                    st.error(result['message'])
            else:
                st.error("Please fill all required fields")

def show_reservation_details(slot_data):
    reservation = slot_data['reservationData']
    st.info(f"""
    **Reserved Slot {slot_data['slot']}**
    
    Customer: {reservation['customerName']}
    Vehicle: {reservation['vehicleType']} - {reservation['vehicleNumber']}
    Expected Arrival: {reservation['date']} at {reservation['time']}
    Duration: {reservation['duration']} hours
    """)

if __name__ == "__main__":
    main()
