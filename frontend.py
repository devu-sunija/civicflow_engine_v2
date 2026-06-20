import streamlit as st
import pandas as pd
import numpy as np
import os
import folium
from streamlit_folium import st_folium

# --- 1. DATA INGESTION ---
DATA_FILENAME = "traffic_data.csv"
if os.path.exists(DATA_FILENAME):
    df = pd.read_csv(DATA_FILENAME)
    df.columns = df.columns.str.strip().str.lower()
else:
    # Fallback data if file missing
    data = {'geohash': ["tdr1w2", "tdr1w4", "tdr1w9", "tdr1w1", "tdr34e", "tdr45g"], 
            'demand': [0.5, 0.4, 0.6, 0.3, 0.7, 0.4]}
    df = pd.DataFrame(data)

# --- 2. LOGIC (Formerly Backend) ---
def extract_geohash(lat, lon):
    lat_idx = int((lat - 12.9) * 100) % 3
    lon_idx = int((lon - 77.5) * 100) % 2
    matrix = [["tdr1w2", "tdr1w4"], ["tdr1w9", "tdr1w1"], ["tdr34e", "tdr45g"]]
    return matrix[lat_idx][lon_idx]

def calculate_resources(event_type, footfall, lat, lon, weather):
    target_hash = extract_geohash(lat, lon)
    base_demand = df[df['geohash'] == target_hash]['demand'].mean() if 'geohash' in df.columns else 0.38
    
    # Non-linear equation
    impact = 0.50 * (1 - np.exp(-footfall / 22000))
    weather_scalar = 1.25 if "rain" in weather.lower() else 1.00
    final_congestion = min(1.00, (base_demand + impact) * weather_scalar)
    
    profiles = {
        "Political Rally": {"o": 0.0015, "b": 0.0045},
        "Cricket Match": {"o": 0.0011, "b": 0.0038},
        "Festival": {"o": 0.0018, "b": 0.0052}
    }
    config = profiles.get(event_type, {"o": 0.0010, "b": 0.0035})
    
    officers = max(8, int((footfall * config["o"]) * (1.0 + final_congestion)))
    barricades = max(15, int((footfall * config["b"]) * (1.0 + final_congestion)))
    
    return final_congestion, officers, barricades, target_hash

# --- 3. UI (Frontend) ---
st.set_page_config(layout="wide")
st.title("CivicFlow AI: Event-Driven Congestion Control Room")

col1, col2 = st.columns(2)

with col1:
    e_type = st.selectbox("Event Type", ["Cricket Match", "Political Rally", "Festival", "Construction"])
    footfall = st.number_input("Expected Footfall", value=32500)
    lat = st.number_input("Latitude", value=12.97, format="%.4f")
    lon = st.number_input("Longitude", value=77.59, format="%.4f")
    weather = st.radio("Weather", ["Clear", "Heavy Rain"])
    
    if st.button("Analyze Traffic Impact"):
        st.session_state['res'] = calculate_resources(e_type, footfall, lat, lon, weather)

with col2:
    if 'res' in st.session_state:
        cong, off, bar, gh = st.session_state['res']
        st.metric("Predicted Congestion", f"{cong*100:.1f}%")
        st.metric("Officers Required", f"{off} Pers.")
        st.metric("Barricades Needed", f"{bar} Units")
        
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.Marker([lat, lon], popup=gh, icon=folium.Icon(color="red")).add_to(m)
        st_folium(m, width=700)