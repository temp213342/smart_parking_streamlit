import streamlit as st
import time
from utils.detection_api import DetectionAPI
from utils.parking_logic import ParkingLogic
import datetime
def main():
    st.title("🤖 AI Auto Detection Mode")
    st.markdown("*Automated vehicle detection using computer vision*")
    
    detection_api = init_detection_api()
    
    # Check if running in cloud
    if detection_api.is_cloud_deployment:
        show_cloud_deployment_message()
        return
    
    # ... rest of your existing code

def show_cloud_deployment_message():
    """Show message for cloud deployment users"""
    st.info("🌐 **Cloud Deployment Detected**")
    
    st.markdown("""
    The AI Auto Detection Mode requires a local AI detection server running on your machine, 
    which is not available in this cloud deployment.
    
    ### To use AI Auto Detection:
    
    1. **Download the application** to your local machine
    2. **Install dependencies**: `pip install -r requirements.txt`
    3. **Download YOLO models**:
       - `yolo11n.pt` for vehicle detection
       - `best.pt` for license plate detection
    4. **Start the detection server**: `python server.py`
    5. **Run locally**: `streamlit run app.py`
    
    ### For now, please use **Manual Mode**:
    - Go back to the main page
    - Use the "🎛️ Controls" panel to manually park vehicles
    - Fill in vehicle details manually
    """)
    
    if st.button("🏠 Return to Main Page"):
        st.switch_page("app.py")

st.set_page_config(
    page_title="Auto Mode - Vehicle Vacancy Vault",
    page_icon="🤖",
    layout="wide"
)

# Initialize API
@st.cache_resource
def init_detection_api():
    return DetectionAPI()

@st.cache_resource
def init_parking_logic():
    return ParkingLogic()

def main():
    st.title("🤖 AI Auto Detection Mode")
    st.markdown("*Automated vehicle detection using computer vision*")
    
    # Initialize session state
    if 'detection_active' not in st.session_state:
        st.session_state.detection_active = False
    if 'detection_results' not in st.session_state:
        st.session_state.detection_results = {}
    if 'detection_status' not in st.session_state:
        st.session_state.detection_status = 'idle'
    
    detection_api = init_detection_api()
    
    # Server status check
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Detection Server Status")
        
        with st.spinner("Checking server status..."):
            health = detection_api.health_check()
        
        if health.get('status') == 'healthy':
            st.success("✅ Detection server is running and ready")
        else:
            st.error(f"❌ Detection server unavailable: {health.get('message', 'Unknown error')}")
            st.info("Please make sure to run `python server.py` before using Auto Mode")
    
    with col2:
        if st.button("🔄 Refresh Status"):
            st.rerun()
    
    st.markdown("---")
    
    # Detection process
    if health.get('status') == 'healthy':
        show_detection_interface(detection_api)
    else:
        show_server_instructions()

def show_detection_interface(detection_api):
    st.markdown("### 🎯 Auto Detection Process")
    
    # Detection phases info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Phase 1: Vehicle Detection**
        - Point camera at vehicle
        - AI identifies vehicle type
        - Supports cars, bikes, trucks
        """)
    
    with col2:
        st.markdown("""
        **Phase 2: License Plate**
        - Point camera at license plate
        - OCR extracts plate number
        - Indian plate format support
        """)
    
    with col3:
        st.markdown("""
        **Phase 3: Duration Input**
        - Show fingers for parking hours
        - 1-10 hours supported
        - Confirm with OK gesture
        """)
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Auto Detection", disabled=st.session_state.detection_active):
            start_detection(detection_api)
    
    with col2:
        if st.button("⏹️ Stop Detection", disabled=not st.session_state.detection_active):
            stop_detection(detection_api)
    
    with col3:
        if st.button("🔄 Reset System"):
            reset_detection(detection_api)
    
    # Detection status display
    if st.session_state.detection_active:
        show_detection_status(detection_api)
    
    # Results display
    if st.session_state.detection_results:
        show_detection_results()

def start_detection(detection_api):
    """Start the detection process"""
    result = detection_api.start_detection()
    
    if result.get('status') == 'started':
        st.session_state.detection_active = True
        st.session_state.detection_status = 'running'
        st.success("🚀 Detection started! Follow the camera instructions.")
        st.rerun()
    else:
        st.error(f"Failed to start detection: {result.get('message', 'Unknown error')}")

def stop_detection(detection_api):
    """Stop the detection process"""
    st.session_state.detection_active = False
    st.session_state.detection_status = 'stopped'
    st.info("Detection stopped")
    st.rerun()

def reset_detection(detection_api):
    """Reset the detection system"""
    result = detection_api.reset_detection()
    
    st.session_state.detection_active = False
    st.session_state.detection_results = {}
    st.session_state.detection_status = 'idle'
    
    if result.get('status') == 'reset':
        st.success("🔄 Detection system reset")
    else:
        st.warning("Reset may have failed, but local state cleared")
    
    st.rerun()

def show_detection_status(detection_api):
    """Display real-time detection status"""
    st.markdown("### 📊 Detection Status")
    
    # Create placeholder for real-time updates
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    # Auto-refresh every 2 seconds
    if st.session_state.detection_active:
        result = detection_api.get_results()
        
        current_phase = result.get('current_phase', 'Starting...')
        message = result.get('message', '')
        status = result.get('status', 'running')
        
        with status_placeholder.container():
            if status == 'running':
                st.info(f"🔄 {current_phase}")
                if message:
                    st.write(f"💡 {message}")
            elif status == 'completed':
                st.success(f"✅ {current_phase}")
                st.session_state.detection_active = False
                st.session_state.detection_results = result.get('results', {})
                st.rerun()
            elif status == 'error':
                st.error(f"❌ Error: {message}")
                st.session_state.detection_active = False
                st.rerun()
        
        # Progress indicator
        with progress_placeholder.container():
            phases = ['Vehicle Detection', 'License Plate', 'Hand Gesture']
            progress_value = 0
            
            if 'vehicle' in current_phase.lower():
                progress_value = 33
            elif 'license' in current_phase.lower() or 'plate' in current_phase.lower():
                progress_value = 66
            elif 'hand' in current_phase.lower() or 'gesture' in current_phase.lower():
                progress_value = 100
            
            st.progress(progress_value / 100)
            st.write(f"Progress: {progress_value}%")
        
        # Auto-refresh
        time.sleep(2)
        st.rerun()

def show_detection_results():
    """Display detection results and allow parking"""
    st.markdown("### 🎉 Detection Results")
    
    results = st.session_state.detection_results
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        vehicle_type = results.get('vehicle_type', 'Not detected')
        st.metric("Vehicle Type", vehicle_type)
    
    with col2:
        license_plate = results.get('license_plate', 'Not detected')
        st.metric("License Plate", license_plate)
    
    with col3:
        parking_hours = results.get('parking_hours', 'Not detected')
        st.metric("Parking Hours", f"{parking_hours} hours" if parking_hours else "Not detected")
    
    # Manual override options
    st.markdown("### ✏️ Edit Results (Optional)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        manual_vehicle_type = st.selectbox(
            "Vehicle Type Override",
            ["Use Detected", "Bike", "Car", "Truck"],
            key="manual_vehicle_override"
        )
    
    with col2:
        manual_license = st.text_input(
            "License Plate Override",
            value=license_plate if license_plate != 'Not detected' else '',
            key="manual_license_override"
        )
    
    with col3:
        manual_hours = st.number_input(
            "Hours Override",
            min_value=1,
            max_value=24,
            value=int(parking_hours) if parking_hours and parking_hours != 'Not detected' else 2,
            key="manual_hours_override"
        )
    
    # Park vehicle button
    if st.button("🅿️ Park Vehicle with These Details", type="primary"):
        park_detected_vehicle(results, manual_vehicle_type, manual_license, manual_hours)

def park_detected_vehicle(results, manual_vehicle_type, manual_license, manual_hours):
    """Park vehicle using detection results"""
    # Determine final values
    final_vehicle_type = manual_vehicle_type if manual_vehicle_type != "Use Detected" else results.get('vehicle_type')
    final_license = manual_license if manual_license else results.get('license_plate')
    final_hours = manual_hours
    
    # Validate inputs
    if not final_vehicle_type or final_vehicle_type == 'Not detected':
        st.error("Please specify vehicle type")
        return
    
    if not final_license or final_license == 'Not detected':
        st.error("Please specify license plate number")
        return
    
    # Map vehicle type names
    vehicle_type_mapping = {
        "Two Wheeler (Bike)": "Bike",
        "4 Wheeler (Car)": "Car",
        "Heavy Vehicle (Bus/Truck)": "Truck",
        "Heavy Vehicle (Truck)": "Truck"
    }
    
    mapped_vehicle_type = vehicle_type_mapping.get(final_vehicle_type, final_vehicle_type)
    
    # Park the vehicle
    parking_logic = init_parking_logic()
    
    # Load current parking data
    if 'parking_data' not in st.session_state:
        from utils.data_manager import DataManager
        data_manager = DataManager()
        st.session_state.parking_data = data_manager.load_parking_data()
    
    result = parking_logic.park_vehicle(
        st.session_state.parking_data,
        mapped_vehicle_type,
        final_license,
        final_hours
    )
    
    if result['success']:
        st.success(f"🎉 Vehicle successfully parked in Slot {result['slot']}!")
        
        # Show parking details
        charge_info = result['charge']
        st.info(f"""
        **Parking Confirmation**
        - Slot: {result['slot']}
        - Vehicle: {mapped_vehicle_type} - {final_license}
        - Duration: {final_hours} hours
        - Charge: ₹{charge_info['total']}
        - Rush Hours: {'Yes' if charge_info['rushHours'] else 'No'}
        - Night Rate: {'Yes' if charge_info['nightRate'] else 'No'}
        """)
        
        # Save data
        from utils.data_manager import DataManager
        data_manager = DataManager()
        data_manager.save_parking_data(st.session_state.parking_data)
        
        # Clear results
        st.session_state.detection_results = {}
        
        # Option to return to main page
        if st.button("🏠 Return to Main Page"):
            st.switch_page("app.py")
    else:
        st.error(f"Failed to park vehicle: {result['message']}")

def show_server_instructions():
    """Show instructions for starting the detection server"""
    st.markdown("### 🛠️ Setup Instructions")
    
    st.markdown("""
    To use Auto Mode, you need to start the AI detection server:
    
    1. **Install Dependencies**
       ```
       pip install -r requirements.txt
       ```
    
    2. **Download YOLO Models**
       - Download `yolo11n.pt` from [Ultralytics](https://github.com/ultralytics/ultralytics)
       - Place your license plate detection model as `best.pt`
       - Both files should be in the project directory
    
    3. **Start Detection Server**
       ```
       python server.py
       ```
       
    4. **Verify Camera Access**
       - Make sure your webcam is connected and working
       - Allow camera permissions when prompted
    
    5. **Return to this page** and click "Refresh Status"
    """)
    
    st.markdown("### 🔧 Troubleshooting")
    
    with st.expander("Common Issues"):
        st.markdown("""
        **Server won't start:**
        - Check Python version (3.8+)
        - Install all dependencies: `pip install -r requirements.txt`
        - Verify camera is not used by another application
        
        **Detection fails:**
        - Ensure good lighting conditions
        - Hold camera steady during detection phases
        - Make sure license plates are clearly visible
        
        **Model errors:**
        - Download `yolo11n.pt` from Ultralytics
        - Update file paths in `server.py` if needed
        - Check model files are in correct directory
        """)

if __name__ == "__main__":
    main()

