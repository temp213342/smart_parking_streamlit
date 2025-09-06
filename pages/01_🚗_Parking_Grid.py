import streamlit as st

st.set_page_config(
    page_title="Parking Grid - Vehicle Vacancy Vault",
    page_icon="🚗",
    layout="wide"
)

# This will redirect to main page as parking grid is the main functionality
st.switch_page("app.py")
