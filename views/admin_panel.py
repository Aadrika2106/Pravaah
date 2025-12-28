import streamlit as st

def show():
    st.title("⚙️ Admin Panel")
    
    st.info("Admin features coming soon!")
    
    # System stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Users", "24")
    with col2:
        st.metric("Active Sessions", "8")
    with col3:
        st.metric("System Uptime", "99.9%")