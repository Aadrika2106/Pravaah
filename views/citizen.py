import streamlit as st
from models.yolo.infer import predict_image_with_viz
from apis.weather import get_weather_data
from apis.pollution import get_pollution_data
from maps.hotspot import create_hotspot_map

def show():
    st.title("👥 Public Awareness Dashboard")
    
    # Simple metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Water Quality", "Moderate")
    with col2:
        st.metric("Safety Level", "6.5/10")
    with col3:
        st.metric("Nearby Alerts", "2")
    
    st.markdown("---")
    
    # Map
    st.subheader("🗺️ Pollution Hotspots")
    try:
        weather = get_weather_data()
        pollution = get_pollution_data()
        river = {'flow': 1250, 'level': 3.2, 'ph': 7.3, 'water_temp': 22.5}
        user_data = {'turbidity': 25.0, 'conductivity': 450.0, 'dissolved_oxygen': 7.5, 'sampling_depth': 2.0}
        
        hotspot_map = create_hotspot_map(weather, pollution, river, user_data)
        st.components.v1.html(hotspot_map._repr_html_(), height=400)
    except Exception as e:
        st.error(f"Map error: {e}")
    
    st.markdown("---")
    
    # Image upload
    st.subheader("📸 Microplastic Detection")
    uploaded = st.file_uploader("Upload water sample", type=['jpg', 'png', 'jpeg'])
    
    if uploaded:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded, caption="Original", use_container_width=True)
        
        if st.button("🔍 Analyze", type="primary"):
            with st.spinner("Analyzing..."):
                try:
                    result = predict_image_with_viz(uploaded, 0.50, "Public")
                    
                    with col2:
                        st.image(result['annotated_image'], caption="Detected", use_container_width=True)
                    
                    st.success(f"Found {result['count']} microplastics!")
                    
                    if result.get('particle_types'):
                        st.write("**Types:**")
                        for ptype, count in result['particle_types'].items():
                            st.write(f"- {ptype.title()}: {count}")
                
                except Exception as e:
                    st.error(f"Detection error: {e}")