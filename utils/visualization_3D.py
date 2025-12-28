"""
3D River Visualization
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_3d_river_visualization():
    """
    Create 3D visualization of river with pollution data
    """
    st.subheader("🌊 3D River Model")
    st.markdown("*Interactive 3D visualization of river bathymetry and pollution distribution*")
    
    # Generate synthetic river bathymetry
    x = np.linspace(0, 10, 50)
    y = np.linspace(0, 5, 30)
    X, Y = np.meshgrid(x, y)
    
    # River depth (bathymetry)
    Z = -5 + 3 * np.sin(X / 2) - 2 * np.exp(-((Y - 2.5)**2) / 2)
    
    # Pollution concentration (volumetric)
    pollution = 100 * np.exp(-((X - 5)**2 + (Y - 2.5)**2) / 5)
    
    fig = go.Figure()
    
    # River bed surface
    fig.add_trace(go.Surface(
        x=X,
        y=Y,
        z=Z,
        surfacecolor=pollution,
        colorscale='Reds',
        showscale=True,
        colorbar=dict(title="Pollution<br>Concentration<br>(particles/L)", x=1.1),
        name='River Bed'
    ))
    
    # Add pollution hotspots as scatter
    hotspot_x = [3, 7, 5]
    hotspot_y = [2.5, 2.5, 2.5]
    hotspot_z = [-5 + 3 * np.sin(np.array(hotspot_x) / 2) - 2 * np.exp(-((np.array(hotspot_y) - 2.5)**2) / 2) + 1]
    
    fig.add_trace(go.Scatter3d(
        x=hotspot_x,
        y=hotspot_y,
        z=hotspot_z,
        mode='markers',
        marker=dict(
            size=15,
            color='red',
            symbol='diamond',
            line=dict(color='darkred', width=2)
        ),
        name='Pollution Hotspots'
    ))
    
    # Water surface
    water_surface_z = np.zeros_like(Z)
    fig.add_trace(go.Surface(
        x=X,
        y=Y,
        z=water_surface_z,
        opacity=0.3,
        showscale=False,
        colorscale=[[0, 'lightblue'], [1, 'lightblue']],
        name='Water Surface'
    ))
    
    fig.update_layout(
        title="3D River Model with Pollution Distribution",
        scene=dict(
            xaxis_title="River Length (km)",
            yaxis_title="River Width (km)",
            zaxis_title="Depth (m)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Controls
    st.markdown("---")
    st.markdown("### 🎮 Visualization Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        view_angle = st.selectbox("View Angle", ["Top", "Side", "Isometric"])
    
    with col2:
        show_grid = st.checkbox("Show Grid", value=True)
    
    with col3:
        animate = st.checkbox("Animate Flow", value=False)
    
    if animate:
        st.info("🌊 Animation mode: Simulating water flow dynamics")