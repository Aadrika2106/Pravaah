import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("🔬 Researcher Analysis Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Samples", "1,247")
    with col2:
        st.metric("YOLO Accuracy", "94.2%")
    with col3:
        st.metric("WQI Accuracy", "94.0%")
    with col4:
        st.metric("PINN R²", "0.90")
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2 = st.tabs(["📊 Model Performance", "📈 Data Analysis"])
    
    with tab1:
        st.subheader("Model Comparison")
        
        perf_data = pd.DataFrame({
            'Model': ['YOLO', 'Raman', 'WQI', 'PINN'],
            'Accuracy': [94.2, 91.8, 94.0, 90.0],
            'Precision': [92.5, 90.2, 93.5, 88.5],
            'Recall': [93.8, 92.1, 94.2, 91.2]
        })
        
        fig = px.bar(perf_data, x='Model', y=['Accuracy', 'Precision', 'Recall'],
                    barmode='group', title="Model Performance Metrics")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Dataset Analysis")
        
        try:
            df = pd.read_csv('data/aggregated_results.csv')
            st.dataframe(df.head(10), use_container_width=True)
            
            st.download_button(
                "📥 Download Data",
                df.to_csv(index=False),
                "data.csv",
                "text/csv"
            )
        except:
            st.info("Dataset not loaded yet")