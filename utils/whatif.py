import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show_whatif_simulation():
    """What-If Scenario Simulation"""
    st.subheader("🎮 What-If Scenario Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Adjust Parameters:**")
        
        rainfall = st.slider("Rainfall (mm/day)", 0, 100, 50)
        flow = st.slider("Flow Rate (m³/s)", 500, 3000, 1200)
        temp = st.slider("Temperature (°C)", 10, 35, 25)
        
        if st.button("🚀 Run Simulation", type="primary"):
            st.session_state['sim_run'] = True
    
    with col2:
        if st.session_state.get('sim_run'):
            st.markdown("**Predicted Impacts:**")
            
            # Simple calculation
            wqi = 50 + (flow - 1200) / 100 - (temp - 25) * 2
            wqi = np.clip(wqi, 0, 100)
            
            do = 7 - (temp - 25) * 0.2
            do = np.clip(do, 0, 15)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("WQI", f"{wqi:.1f}")
            with col_b:
                st.metric("DO", f"{do:.1f} mg/L")
            
            # Simple chart
            days = list(range(30))
            wqi_series = [wqi + np.random.normal(0, 3) for _ in days]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=days, y=wqi_series, mode='lines', name='WQI'))
            fig.update_layout(title="30-Day Projection", xaxis_title="Days", yaxis_title="WQI")
            
            st.plotly_chart(fig, use_container_width=True)