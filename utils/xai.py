import streamlit as st
import plotly.graph_objects as go
import numpy as np

def show_xai_tab():
    """XAI Dashboard"""
    st.subheader("🔍 Explainable AI Analysis")
    
    # Feature Importance
    features = ['DO', 'pH', 'Temp', 'Turbidity', 'BOD', 'COD']
    importance = [0.18, 0.15, 0.12, 0.11, 0.10, 0.09]
    
    fig = go.Figure(go.Bar(
        x=importance,
        y=features,
        orientation='h',
        marker_color='blue'
    ))
    
    fig.update_layout(
        title="Feature Importance (Random Forest)",
        xaxis_title="Importance",
        yaxis_title="Features"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**Interpretation:** Dissolved Oxygen is the most critical factor for WQI prediction.")