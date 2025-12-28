import streamlit as st
import plotly.graph_objects as go
from utils.xai import show_xai_tab
from utils.whatif import show_whatif_simulation
from models.wqi.predict import predict_wqi
from apis.weather import get_weather_data
from apis.pollution import get_pollution_data
from apis.rivers import get_river_data

def show():
    st.title("🏛️ Government Policy Dashboard")
    
    # Get live data
    weather = get_weather_data()
    pollution = get_pollution_data()
    river = get_river_data()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("WQI Score", "52.3")
    with col2:
        st.metric("Critical Zones", "12")
    with col3:
        st.metric("Active Alerts", "3")
    with col4:
        st.metric("Monitored Sites", "24")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Monitoring", 
        "🔍 XAI Analysis", 
        "🎮 What-If Simulation",
        "📊 Reports"
    ])
    
    with tab1:
        st.subheader("Real-time Monitoring")
        
        # Map
        try:
            from maps.hotspot import create_hotspot_map
            user_data = {'turbidity': 25.0, 'conductivity': 450.0, 'dissolved_oxygen': 7.5, 'sampling_depth': 2.0}
            hotspot_map = create_hotspot_map(weather, pollution, river, user_data)
            st.components.v1.html(hotspot_map._repr_html_(), height=450)
        except Exception as e:
            st.error(f"Map error: {e}")
        
        # WQI Gauge
        st.markdown("---")
        st.subheader("Water Quality Index")
        
        try:
            wqi_features = {
                'temperature': weather['temp'],
                'ph': river['ph'],
                'dissolved_oxygen': 7.5,
                'conductivity': 450,
                'turbidity': 25,
                'tds': 300,
                'bod': 10,
                'cod': 35,
                'nitrate': 8.5,
                'phosphate': 2.1,
                'fecal_coliform': 150,
                'total_coliform': 1200,
                'chloride': 85,
                'fluoride': 0.8,
                'hardness': 180,
                'alkalinity': 120
            }
            
            wqi_result = predict_wqi(wqi_features)
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=wqi_result['wqi_score'],
                title={'text': f"WQI: {wqi_result['classification']}"},
                gauge={'axis': {'range': [0, 100]},
                      'bar': {'color': "darkblue"}}
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        except Exception as e:
            st.warning("WQI calculation in progress...")
    
    with tab2:
        try:
            show_xai_tab()
        except Exception as e:
            st.error(f"XAI error: {e}")
            st.info("XAI features loading...")
    
    with tab3:
        try:
            show_whatif_simulation()
        except Exception as e:
            st.error(f"Simulation error: {e}")
            st.info("Simulation features loading...")
    
    with tab4:
        st.subheader("📄 Generate Reports")
        
        if st.button("Generate PDF Report", type="primary"):
            st.success("Report generated! (Feature in development)")