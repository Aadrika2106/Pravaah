"""
Advanced Analytics Module
- Multi-location comparison
- Historical trend analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

def show_comparison_mode():
    """
    Compare multiple locations simultaneously
    """
    st.subheader("📍 Multi-Location Comparison")
    st.markdown("*Compare water quality across different monitoring sites*")
    
    # Sample locations data
    locations_data = {
        'Delhi - Yamuna': {'wqi': 32.5, 'do': 3.8, 'mp': 185, 'turbidity': 68, 'lat': 28.6139, 'lon': 77.2090},
        'Mumbai - Mithi': {'wqi': 45.2, 'do': 5.2, 'mp': 120, 'turbidity': 52, 'lat': 19.0760, 'lon': 72.8777},
        'Chennai - Cooum': {'wqi': 38.7, 'do': 4.5, 'mp': 145, 'turbidity': 58, 'lat': 13.0827, 'lon': 80.2707},
        'Kolkata - Hooghly': {'wqi': 28.3, 'do': 3.2, 'mp': 215, 'turbidity': 75, 'lat': 22.5726, 'lon': 88.3639},
        'Bangalore - Vrishabhavathi': {'wqi': 52.8, 'do': 6.1, 'mp': 95, 'turbidity': 42, 'lat': 12.9716, 'lon': 77.5946},
        'Hyderabad - Musi': {'wqi': 41.5, 'do': 4.8, 'mp': 132, 'turbidity': 55, 'lat': 17.3850, 'lon': 78.4867}
    }
    
    # Location selector
    selected_locations = st.multiselect(
        "Select locations to compare (2-5 recommended)",
        list(locations_data.keys()),
        default=list(locations_data.keys())[:3]
    )
    
    if len(selected_locations) < 2:
        st.warning("⚠️ Please select at least 2 locations for comparison")
        return
    
    # Filter data for selected locations
    comparison_data = {loc: locations_data[loc] for loc in selected_locations}
    
    # Create comparison DataFrame
    df_comparison = pd.DataFrame(comparison_data).T
    df_comparison['Location'] = df_comparison.index
    
    st.markdown("---")
    
    # Metrics comparison
    st.markdown("### 📊 Key Metrics Comparison")
    
    # Grouped bar chart
    fig_metrics = go.Figure()
    
    metrics = ['wqi', 'do', 'mp', 'turbidity']
    metric_names = ['WQI', 'DO (mg/L)', 'Microplastic (p/L)', 'Turbidity (NTU)']
    
    for metric, name in zip(metrics, metric_names):
        fig_metrics.add_trace(go.Bar(
            name=name,
            x=selected_locations,
            y=df_comparison[metric],
            text=df_comparison[metric].round(1),
            textposition='auto',
        ))
    
    fig_metrics.update_layout(
        title="Multi-Parameter Comparison",
        xaxis_title="Location",
        yaxis_title="Value",
        barmode='group',
        plot_bgcolor='white',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_metrics, use_container_width=True)
    
    st.markdown("---")
    
    # Radar chart for multi-dimensional comparison
    st.markdown("### 🎯 Multi-Dimensional Performance")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Normalize values for radar chart (0-100 scale)
        df_normalized = df_comparison.copy()
        df_normalized['wqi_norm'] = df_normalized['wqi']
        df_normalized['do_norm'] = (df_normalized['do'] / 15) * 100
        df_normalized['mp_norm'] = 100 - (df_normalized['mp'] / 300) * 100  # Inverse
        df_normalized['turbidity_norm'] = 100 - (df_normalized['turbidity'] / 100) * 100  # Inverse
        
        fig_radar = go.Figure()
        
        categories = ['WQI', 'DO', 'Microplastic<br>(lower better)', 'Turbidity<br>(lower better)']
        
        colors = px.colors.qualitative.Set1
        
        for idx, location in enumerate(selected_locations):
            values = [
                df_normalized.loc[location, 'wqi_norm'],
                df_normalized.loc[location, 'do_norm'],
                df_normalized.loc[location, 'mp_norm'],
                df_normalized.loc[location, 'turbidity_norm']
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=location.split(' - ')[0],
                line=dict(color=colors[idx % len(colors)])
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Normalized Performance Comparison",
            height=450
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("**📊 Rankings**")
        
        # Rank locations
        rankings = {}
        for metric in ['wqi', 'do']:
            rankings[metric] = df_comparison[metric].rank(ascending=False)
        for metric in ['mp', 'turbidity']:
            rankings[metric] = df_comparison[metric].rank(ascending=True)
        
        df_rankings = pd.DataFrame(rankings)
        df_rankings['Overall'] = df_rankings.mean(axis=1)
        df_rankings = df_rankings.sort_values('Overall')
        
        st.markdown("**Overall Ranking:**")
        for idx, (location, row) in enumerate(df_rankings.iterrows(), 1):
            medal = ['🥇', '🥈', '🥉'][idx-1] if idx <= 3 else f"{idx}."
            st.markdown(f"{medal} **{location.split(' - ')[0]}**")
            st.caption(f"Score: {row['Overall']:.2f}")
        
        st.markdown("---")
        
        # Best practices
        st.markdown("**✅ Best Performer:**")
        best_location = df_rankings.index[0]
        best_data = df_comparison.loc[best_location]
        
        st.success(f"**{best_location}**")
        st.write(f"WQI: {best_data['wqi']:.1f}")
        st.write(f"DO: {best_data['do']:.1f} mg/L")
    
    st.markdown("---")
    
    # Time series comparison (simulated)
    st.markdown("### 📅 Temporal Comparison (Last 30 Days)")
    
    # Generate synthetic time series
    days = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    fig_timeseries = go.Figure()
    
    for location in selected_locations:
        # Simulate time series around current WQI
        base_wqi = df_comparison.loc[location, 'wqi']
        trend = np.linspace(base_wqi - 5, base_wqi + 5, 30)
        seasonal = 3 * np.sin(np.linspace(0, 2*np.pi, 30))
        noise = np.random.normal(0, 2, 30)
        
        wqi_series = trend + seasonal + noise
        wqi_series = np.clip(wqi_series, 0, 100)
        
        fig_timeseries.add_trace(go.Scatter(
            x=days,
            y=wqi_series,
            mode='lines+markers',
            name=location.split(' - ')[0],
            line=dict(width=2)
        ))
    
    fig_timeseries.update_layout(
        title="WQI Trends Over Time",
        xaxis_title="Date",
        yaxis_title="WQI",
        hovermode='x unified',
        plot_bgcolor='white',
        height=400
    )
    
    st.plotly_chart(fig_timeseries, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed comparison table
    st.markdown("### 📋 Detailed Comparison Table")
    
    # Add classification
    df_display = df_comparison.copy()
    df_display['WQI Class'] = df_display['wqi'].apply(lambda x: 
        'Excellent' if x > 75 else 'Good' if x > 50 else 'Fair' if x > 25 else 'Poor')
    
    df_display['DO Status'] = df_display['do'].apply(lambda x:
        '✅ Good' if x > 6 else '⚠️ Low' if x > 4 else '🔴 Critical')
    
    st.dataframe(
        df_display[['wqi', 'WQI Class', 'do', 'DO Status', 'mp', 'turbidity']].style.background_gradient(
            subset=['wqi', 'do'], cmap='RdYlGn'
        ).background_gradient(
            subset=['mp', 'turbidity'], cmap='RdYlGn_r'
        ),
        use_container_width=True
    )
    
    # Export
    csv = df_display.to_csv(index=True)
    st.download_button(
        "📥 Download Comparison Data",
        csv,
        "location_comparison.csv",
        "text/csv"
    )


def show_historical_trends():
    """
    Historical trend analysis with decomposition
    """
    st.subheader("📈 Historical Trend Analysis")
    st.markdown("*Analyze long-term patterns and seasonality*")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Generate synthetic historical data
    days = pd.date_range(start=start_date, end=end_date, freq='D')
    n_days = len(days)
    
    # WQI time series with trend, seasonality, and noise
    trend = np.linspace(45, 55, n_days)  # Slight improvement trend
    seasonal = 8 * np.sin(2 * np.pi * np.arange(n_days) / 365)  # Annual cycle
    weekly = 3 * np.sin(2 * np.pi * np.arange(n_days) / 7)  # Weekly pattern
    noise = np.random.normal(0, 3, n_days)
    
    wqi_series = trend + seasonal + weekly + noise
    wqi_series = np.clip(wqi_series, 0, 100)
    
    df_hist = pd.DataFrame({
        'Date': days,
        'WQI': wqi_series,
        'DO': 6 + seasonal/4 + np.random.normal(0, 0.5, n_days),
        'Microplastic': 120 - trend/2 + np.random.normal(0, 10, n_days)
    })
    
    st.markdown("---")
    
    # Main time series plot
    st.markdown("### 📊 Time Series Overview")
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Water Quality Index', 'Dissolved Oxygen', 'Microplastic Concentration'),
        vertical_spacing=0.08
    )
    
    fig.add_trace(
        go.Scatter(x=df_hist['Date'], y=df_hist['WQI'], name='WQI',
                  line=dict(color='#3498db', width=1.5),
                  fill='tozeroy', fillcolor='rgba(52, 152, 219, 0.2)'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df_hist['Date'], y=df_hist['DO'], name='DO',
                  line=dict(color='#2ecc71', width=1.5),
                  fill='tozeroy', fillcolor='rgba(46, 204, 113, 0.2)'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=df_hist['Date'], y=df_hist['Microplastic'], name='Microplastic',
                  line=dict(color='#e74c3c', width=1.5),
                  fill='tozeroy', fillcolor='rgba(231, 76, 60, 0.2)'),
        row=3, col=1
    )
    
    # Add trend lines
    from scipy.signal import savgol_filter
    wqi_smooth = savgol_filter(df_hist['WQI'], 51, 3)
    
    fig.add_trace(
        go.Scatter(x=df_hist['Date'], y=wqi_smooth, name='Trend',
                  line=dict(color='darkblue', width=3, dash='dash')),
        row=1, col=1
    )
    
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="WQI", row=1, col=1)
    fig.update_yaxes(title_text="DO (mg/L)", row=2, col=1)
    fig.update_yaxes(title_text="Particles/L", row=3, col=1)
    
    fig.update_layout(height=800, showlegend=False, plot_bgcolor='white')
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Statistical summary
    st.markdown("### 📊 Statistical Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean WQI", f"{df_hist['WQI'].mean():.1f}")
        st.caption(f"Std: {df_hist['WQI'].std():.1f}")
    
    with col2:
        st.metric("Min WQI", f"{df_hist['WQI'].min():.1f}")
        st.caption(f"Date: {df_hist.loc[df_hist['WQI'].idxmin(), 'Date'].strftime('%Y-%m-%d')}")
    
    with col3:
        st.metric("Max WQI", f"{df_hist['WQI'].max():.1f}")
        st.caption(f"Date: {df_hist.loc[df_hist['WQI'].idxmax(), 'Date'].strftime('%Y-%m-%d')}")
    
    with col4:
        # Calculate trend
        from scipy.stats import linregress
        slope, _, _, _, _ = linregress(range(len(df_hist)), df_hist['WQI'])
        trend_direction = "📈 Improving" if slope > 0 else "📉 Declining"
        st.metric("Trend", trend_direction)
        st.caption(f"Rate: {slope*365:.1f}/year")
    
    st.markdown("---")
    
    # Year-over-year comparison
    st.markdown("### 📅 Year-over-Year Comparison")
    
    if n_days >= 365:
        # Extract years
        df_hist['Year'] = df_hist['Date'].dt.year
        df_hist['DayOfYear'] = df_hist['Date'].dt.dayofyear
        
        fig_yoy = go.Figure()
        
        for year in df_hist['Year'].unique():
            year_data = df_hist[df_hist['Year'] == year]
            fig_yoy.add_trace(go.Scatter(
                x=year_data['DayOfYear'],
                y=year_data['WQI'],
                mode='lines',
                name=str(year),
                line=dict(width=2)
            ))
        
        fig_yoy.update_layout(
            title="Year-over-Year WQI Comparison",
            xaxis_title="Day of Year",
            yaxis_title="WQI",
            hovermode='x unified',
            plot_bgcolor='white',
            height=400
        )
        
        st.plotly_chart(fig_yoy, use_container_width=True)
    
    st.markdown("---")
    
    # Anomaly detection
    st.markdown("### 🔍 Anomaly Detection")
    
    # Simple anomaly detection using z-score
    from scipy.stats import zscore
    df_hist['z_score'] = zscore(df_hist['WQI'])
    anomalies = df_hist[abs(df_hist['z_score']) > 2]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_anomaly = go.Figure()
        
        fig_anomaly.add_trace(go.Scatter(
            x=df_hist['Date'],
            y=df_hist['WQI'],
            mode='lines',
            name='WQI',
            line=dict(color='lightblue')
        ))
        
        fig_anomaly.add_trace(go.Scatter(
            x=anomalies['Date'],
            y=anomalies['WQI'],
            mode='markers',
            name='Anomalies',
            marker=dict(color='red', size=10, symbol='x')
        ))
        
        fig_anomaly.update_layout(
            title="Anomaly Detection (|Z-score| > 2)",
            xaxis_title="Date",
            yaxis_title="WQI",
            plot_bgcolor='white',
            height=400
        )
        
        st.plotly_chart(fig_anomaly, use_container_width=True)
    
    with col2:
        st.markdown(f"**Detected Anomalies:** {len(anomalies)}")
        
        if len(anomalies) > 0:
            st.markdown("**Recent Anomalies:**")
            for idx, row in anomalies.tail(5).iterrows():
                st.write(f"📍 {row['Date'].strftime('%Y-%m-%d')}: WQI {row['WQI']:.1f}")
        else:
            st.success("No significant anomalies detected")
    
    # Export
    st.markdown("---")
    csv = df_hist.to_csv(index=False)
    st.download_button(
        "📥 Download Historical Data",
        csv,
        "historical_data.csv",
        "text/csv"
    )