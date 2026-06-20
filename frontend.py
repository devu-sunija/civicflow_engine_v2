import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- YOUR MOVED BACKEND LOGIC ---
def calculate_traffic_impact(event_type, footfall, weather):
    # This is your math logic from backend.py
    base_congestion = 0.5
    if event_type == "Cricket Match": base_congestion += 0.2
    if weather == "Heavy Rain": base_congestion += 0.25
    
    congestion = min(base_congestion + (footfall / 100000), 1.0)
    officers = int(congestion * 100)
    barricades = int(congestion * 300)
    return congestion * 100, officers, barricades

# --- YOUR STREAMLIT FRONTEND UI ---
st.set_page_config(layout="wide")
st.title("CivicFlow AI: Event-Driven Congestion Control Room")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Schedule New Event")
    e_type = st.selectbox("Event Type", ["Cricket Match", "Concert", "Rally"])
    footfall = st.number_input("Expected Footfall", value=32500)
    weather = st.radio("Weather Condition", ["Clear", "Heavy Rain"])
    
    if st.button("Analyze Traffic Impact"):
        # DIRECT FUNCTION CALL (No more "Link Broken" errors!)
        cong, off, bar = calculate_traffic_impact(e_type, footfall, weather)
        st.session_state['result'] = (cong, off, bar)

with col2:
    st.subheader("Live Predictive Analytics")
    if 'result' in st.session_state:
        c, o, b = st.session_state['result']
        st.metric("Predicted Congestion", f"{c:.1f}%")
        st.metric("Officers Required", f"{o} Pers.")
        st.metric("Barricades Needed", f"{b} Units")
        
        # Map
        m = folium.Map(location=[12.9812, 77.6412], zoom_start=14)
        folium.Circle([12.9812, 77.6412], radius=500, color="red").add_to(m)
        st_folium(m, width=700)