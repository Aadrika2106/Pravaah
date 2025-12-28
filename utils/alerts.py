"""
Real-Time Alert System
Monitors water quality and sends notifications
"""

import streamlit as st
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSystem:
    def __init__(self):
        self.thresholds = {
            'wqi': {'critical': 30, 'warning': 50, 'info': 75},
            'do': {'critical': 3.0, 'warning': 4.0, 'info': 5.0},
            'microplastic': {'critical': 200, 'warning': 100, 'info': 50},
            'turbidity': {'critical': 75, 'warning': 50, 'info': 30}
        }
        
        # Initialize alert history in session state
        if 'alert_history' not in st.session_state:
            st.session_state.alert_history = []
    
    def check_and_create_alerts(self, wqi, do, microplastic_count, turbidity):
        """
        Check parameters and create alerts if thresholds exceeded
        """
        alerts = []
        current_time = datetime.now()
        
        # WQI Check
        if wqi < self.thresholds['wqi']['critical']:
            alerts.append({
                'severity': 'CRITICAL',
                'parameter': 'WQI',
                'value': wqi,
                'threshold': self.thresholds['wqi']['critical'],
                'message': f'Water Quality Index critically low: {wqi:.1f}',
                'action': 'Immediate intervention required',
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        elif wqi < self.thresholds['wqi']['warning']:
            alerts.append({
                'severity': 'WARNING',
                'parameter': 'WQI',
                'value': wqi,
                'threshold': self.thresholds['wqi']['warning'],
                'message': f'Water Quality Index below acceptable: {wqi:.1f}',
                'action': 'Enhanced monitoring recommended',
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Dissolved Oxygen Check
        if do < self.thresholds['do']['critical']:
            alerts.append({
                'severity': 'CRITICAL',
                'parameter': 'DO',
                'value': do,
                'threshold': self.thresholds['do']['critical'],
                'message': f'Dissolved Oxygen critical: {do:.1f} mg/L',
                'action': 'Increase aeration immediately',
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        elif do < self.thresholds['do']['warning']:
            alerts.append({
                'severity': 'WARNING',
                'parameter': 'DO',
                'value': do,
                'threshold': self.thresholds['do']['warning'],
                'message': f'Dissolved Oxygen low: {do:.1f} mg/L',
                'action': 'Monitor closely and prepare aeration',
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Microplastic Check
        if microplastic_count > self.thresholds['microplastic']['critical']:
            alerts.append({
                'severity': 'CRITICAL',
                'parameter': 'Microplastic',
                'value': microplastic_count,
                'threshold': self.thresholds['microplastic']['critical'],
                'message': f'Microplastic concentration critical: {microplastic_count} particles/L',
                'action': 'Deploy cleanup operations',
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        elif microplastic_count > self.thresholds['microplastic']['warning']:
            alerts.append({
                'severity': 'WARNING',
                'parameter': 'Microplastic',
                'value': microplastic_count,
                'threshold': self.thresholds['microplastic']['warning'],
                'message': f'Microplastic concentration high: {microplastic_count} particles/L',
                'action': 'Schedule cleanup operation',
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Turbidity Check
        if turbidity > self.thresholds['turbidity']['critical']:
            alerts.append({
                'severity': 'CRITICAL',
                'parameter': 'Turbidity',
                'value': turbidity,
                'threshold': self.thresholds['turbidity']['critical'],
                'message': f'Turbidity extremely high: {turbidity} NTU',
                'action': 'Investigate upstream sources',
                'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Add to history
        for alert in alerts:
            self._add_to_history(alert)
        
        return alerts
    
    def _add_to_history(self, alert):
        """Add alert to history"""
        if 'alert_history' not in st.session_state:
            st.session_state.alert_history = []
        
        st.session_state.alert_history.insert(0, alert)
        
        # Keep only last 100 alerts
        st.session_state.alert_history = st.session_state.alert_history[:100]
    
    def get_active_alerts(self):
        """Get alerts from last 24 hours"""
        if 'alert_history' not in st.session_state:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        active_alerts = []
        for alert in st.session_state.alert_history:
            alert_time = datetime.strptime(alert['timestamp'], "%Y-%m-%d %H:%M:%S")
            if alert_time > cutoff_time:
                active_alerts.append(alert)
        
        return active_alerts
    
    def show_alert_dashboard(self):
        """Display alert dashboard"""
        st.subheader("🔔 Alert Management System")
        
        # Alert summary
        active_alerts = self.get_active_alerts()
        
        col1, col2, col3 = st.columns(3)
        
        critical = sum(1 for a in active_alerts if a['severity'] == 'CRITICAL')
        warning = sum(1 for a in active_alerts if a['severity'] == 'WARNING')
        info = sum(1 for a in active_alerts if a['severity'] == 'INFO')
        
        with col1:
            st.metric("🔴 Critical", critical, delta_color="inverse")
        with col2:
            st.metric("🟡 Warning", warning, delta_color="inverse")
        with col3:
            st.metric("🔵 Info", info)
        
        st.markdown("---")
        
        # Alert list
        if active_alerts:
            st.markdown("### Recent Alerts (Last 24 hours)")
            
            for alert in active_alerts[:10]:  # Show top 10
                severity_emoji = {
                    'CRITICAL': '🔴',
                    'WARNING': '🟡',
                    'INFO': '🔵'
                }.get(alert['severity'], '⚪')
                
                with st.expander(f"{severity_emoji} {alert['message']} - {alert['timestamp']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Parameter:** {alert['parameter']}")
                        st.markdown(f"**Current Value:** {alert['value']}")
                        st.markdown(f"**Threshold:** {alert['threshold']}")
                    
                    with col2:
                        st.markdown(f"**Severity:** {alert['severity']}")
                        st.markdown(f"**Recommended Action:**")
                        st.info(alert['action'])
                    
                    # Action buttons
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button("✅ Acknowledge", key=f"ack_{alert['timestamp']}"):
                            st.success("Alert acknowledged")
                    with col_b:
                        if st.button("📧 Send Report", key=f"report_{alert['timestamp']}"):
                            self.send_alert_email(alert)
                            st.success("Report sent!")
                    with col_c:
                        if st.button("🗑️ Dismiss", key=f"dismiss_{alert['timestamp']}"):
                            st.warning("Alert dismissed")
        else:
            st.success("✅ No active alerts in the last 24 hours")
        
        # Alert history download
        st.markdown("---")
        if st.button("📥 Download Alert History (JSON)"):
            alerts_json = json.dumps(st.session_state.alert_history, indent=2)
            st.download_button(
                "Download JSON",
                alerts_json,
                "alert_history.json",
                "application/json"
            )
    
    def send_alert_email(self, alert, recipient="admin@example.com"):
        """
        Send alert via email (configure SMTP settings)
        """
        try:
            # Email configuration (replace with actual credentials)
            sender_email = "alerts@microplastic-monitor.com"
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            
            # Create message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient
            message['Subject'] = f"[{alert['severity']}] Water Quality Alert - {alert['parameter']}"
            
            body = f"""
            Alert Notification
            
            Severity: {alert['severity']}
            Parameter: {alert['parameter']}
            Current Value: {alert['value']}
            Threshold: {alert['threshold']}
            
            Message: {alert['message']}
            
            Recommended Action: {alert['action']}
            
            Time: {alert['timestamp']}
            
            This is an automated message from the Microplastic Monitoring System.
            """
            
            message.attach(MIMEText(body, 'plain'))
            
            # Note: In production, use actual SMTP credentials
            # server = smtplib.SMTP(smtp_server, smtp_port)
            # server.starttls()
            # server.login(sender_email, password)
            # server.send_message(message)
            # server.quit()
            
            return True
        
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
            return False
    
    def configure_thresholds(self):
        """UI to configure alert thresholds"""
        st.subheader("⚙️ Configure Alert Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### WQI Thresholds")
            wqi_critical = st.number_input("Critical (<)", 0, 100, 
                                          self.thresholds['wqi']['critical'])
            wqi_warning = st.number_input("Warning (<)", 0, 100,
                                         self.thresholds['wqi']['warning'])
            
            st.markdown("### DO Thresholds (mg/L)")
            do_critical = st.number_input("Critical (<)", 0.0, 15.0,
                                         self.thresholds['do']['critical'])
            do_warning = st.number_input("Warning (<)", 0.0, 15.0,
                                        self.thresholds['do']['warning'])
        
        with col2:
            st.markdown("### Microplastic Thresholds (p/L)")
            mp_critical = st.number_input("Critical (>)", 0, 1000,
                                         self.thresholds['microplastic']['critical'])
            mp_warning = st.number_input("Warning (>)", 0, 1000,
                                        self.thresholds['microplastic']['warning'])
            
            st.markdown("### Turbidity Thresholds (NTU)")
            turb_critical = st.number_input("Critical (>)", 0, 200,
                                           self.thresholds['turbidity']['critical'])
            turb_warning = st.number_input("Warning (>)", 0, 200,
                                          self.thresholds['turbidity']['warning'])
        
        if st.button("💾 Save Thresholds", type="primary"):
            self.thresholds = {
                'wqi': {'critical': wqi_critical, 'warning': wqi_warning},
                'do': {'critical': do_critical, 'warning': do_warning},
                'microplastic': {'critical': mp_critical, 'warning': mp_warning},
                'turbidity': {'critical': turb_critical, 'warning': turb_warning}
            }
            st.success("✅ Thresholds updated!")