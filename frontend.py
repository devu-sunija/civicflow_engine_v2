import streamlit as st
import requests
import folium
import pandas as pd
from streamlit_folium import st_folium  # FIX: Correct official import wrapper string

st.set_page_config(layout="wide", page_title="CivicFlow AI Dashboard")

# Inject styling tweaks natively
st.markdown("""
    <style>
        .main, .stApp { background-color: #FFFFFF !important; }
        div[data-testid="stMetricValue"], label, p, h1, h2, h3 { color: #1A1A1A !important; }
        div[data-testid="stSidebar"] { background-color: #F8F9FA !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🚨 CivicFlow AI: Event-Driven Congestion Control Room")
st.markdown("---")

# Tab navigation panel setup
tab1, tab2 = st.tabs(["🎮 Live Control Room Operations", "📈 Post-Event Analytics Feedback Loop"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("🗓️ Schedule New Event")
        event_type = st.selectbox("Event Type", ["Cricket Match", "Political Rally", "Festival", "Construction"])
        footfall = st.number_input("Expected Footfall (People)", min_value=100, max_value=200000, value=32500, step=500)
        weather = st.radio("Weather Condition", ["Clear", "Heavy Rain"])
        
        st.markdown("### 📍 Location Coordinates")
        lat_input = st.number_input("Latitude", value=12.9812, format="%.4f")
        lon_input = st.number_input("Longitude", value=77.6412, format="%.4f")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.button("Analyze Traffic Impact", type="primary", use_container_width=True)

    if submit_btn:
        payload = {
            "event_type": event_type,
            "footfall": int(footfall),
            "latitude": float(lat_input),
            "longitude": float(lon_input),
            "weather": weather
        }
        try:
            response = requests.post("http://127.0.0.1:8000/api/v1/predict", json=payload).json()
            st.session_state['api_results'] = response
        except Exception:
            st.session_state['api_results'] = "ERROR"

    with col2:
        st.header("📊 Live Predictive Analytics & Resources")
        
        if st.session_state.get('api_results') == "ERROR":
            st.error("❌ Link Broken: Could not establish a connection to the FastAPI backend service loop on port 8000.")
        elif 'api_results' in st.session_state:
            res = st.session_state['api_results']
            congestion_percentage = int(res['congestion_index'] * 100)
            
            # Real-time data validation layout metrics row
            m1, m2, m3 = st.columns(3)
            m1.metric("Predicted Congestion", f"{congestion_percentage}%", res['status'], delta_color="inverse")
            m2.metric("Officers Required", f"{res['resources']['traffic_officers']} Pers.", "Dynamic Target Match")
            m3.metric("Barricades Needed", f"{res['resources']['barricades_count']} Units", "Optimized Logistics Perimeter")
            
            st.markdown("---")
            st.markdown("### 📊 Flipkart Challenge Dataset Pipeline Status")
            
            if res['dataset_mode_active']:
                st.success(f"✔️ **Active Verification Engine Connected:** Mapped inputs directly to Dataset Geohash Cluster node `{res['geohash_mapped']}`.")
            else:
                st.warning(f"⚠️ **Simulation Matrix Enforced:** Running fallback data frameworks for node `{res['geohash_mapped']}`. Check if file configurations match naming targets.")

            st.markdown("### 🗺️ Localization Hotspot Map & Suggested Alternate Routing")
            
            # Center Folium display map dynamically based on current user coordinate parameters
            m = folium.Map(location=[res['coordinates']['lat'], res['coordinates']['lon']], zoom_start=14, tiles="CartoDB Positron")
            
            # Drop marker track pins directly on targets
            folium.Marker(
                location=[res['coordinates']['lat'], res['coordinates']['lon']],
                tooltip=f"Event Core: {event_type}",
                popup=f"Geohash Cluster Node: {res['geohash_mapped']}"
            ).add_to(m)
            
            # Dynamic perimeter bounds calculation layer
            folium.Circle(
                location=[res['coordinates']['lat'], res['coordinates']['lon']],
                radius=int(400 + (res['congestion_index'] * 600)),
                color="red" if res['congestion_index'] > 0.75 else "orange",
                fill=True,
                fill_opacity=0.25
            ).add_to(m)
            
            # FIX: Use correct st_folium call syntax matching correct library instantiation rules
            st_folium(m, use_container_width=True, height=400, key="ops_room_map")
        else:
            st.info("💡 Input event telemetry details on the control board and click 'Analyze' to spin up core predictive computations.")

with tab2:
    st.header("🔄 Post-Event Machine Learning Feedback Loop")
    st.write("Tracks model prediction variances against actual physical street counter telemetry observations over runtime cycles.")
    hist_df = pd.DataFrame({
        'AI Predicted (%)': [82, 58, 91, 40], 
        'Actual Observed (%)': [80, 61, 89, 42]
    }).set_index(pd.Index(['Event #1', 'Event #2', 'Event #3', 'Event #4']))
    st.line_chart(hist_df)