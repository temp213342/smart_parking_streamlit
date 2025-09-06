import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Holiday Calendar - Vehicle Vacancy Vault",
    page_icon="📅",
    layout="wide"
)

def main():
    st.title("📅 Holiday Calendar & Rush Hours")
    st.markdown("*View scheduled holidays and rush hour pricing*")
    
    # Load holiday data
    from utils.data_manager import DataManager
    data_manager = DataManager()
    holidays = data_manager.load_holidays()
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(holidays)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df = df.sort_values('date')
    df['date'] = df['date'].dt.strftime('%B %d, %Y')
    
    # Display holidays table
    st.markdown("### 🎉 Holiday Schedule 2025")
    st.dataframe(
        df[['date', 'name', 'rushFrom', 'rushTo']].rename(columns={
            'date': 'Date',
            'name': 'Holiday Name',
            'rushFrom': 'Rush Hours Start',
            'rushTo': 'Rush Hours End'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Regular rush hours
    st.markdown("### ⏰ Regular Rush Hours")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Friday Rush Hours**
        - Time: 5:00 PM - 12:00 AM
        - Surcharge applies to all vehicle types
        - Higher parking rates during peak hours
        """)
    
    with col2:
        st.markdown("""
        **Weekend Rush Hours**
        - Time: 11:00 AM - 12:00 AM (Sat & Sun)
        - Increased demand pricing
        - Plan ahead for weekend visits
        """)
    
    # Night hours info
    st.markdown("### 🌙 Night Hours Discount")
    st.info("""
    **Special Night Rate: ₹100/hour**
    - Time: 11:00 PM - 5:00 AM
    - Applies to all vehicle types
    - Fixed rate regardless of vehicle type
    - No rush hour surcharges during night hours
    """)

if __name__ == "__main__":
    main()
