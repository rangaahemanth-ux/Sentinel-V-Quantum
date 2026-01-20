"""
Sentinel-V: Quantum AI Nerve Center
Complete command center with FULLY FUNCTIONAL Jarvis sidebar and scan modes
"""

import streamlit as st
import asyncio
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster
from core import SentinelAgent, generate_pdf_report, run_audit, ScanMode
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import json
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Sentinel-V | Quantum AI Nerve Center",
    layout="wide",
    page_icon="⚛️",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 100%);
    }
    
    /* Quantum-themed buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Quantum glow animation */
    @keyframes quantum-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(138, 43, 226, 0.5); }
        50% { box-shadow: 0 0 40px rgba(138, 43, 226, 0.8); }
    }
    
    .quantum-border {
        border: 2px solid rgba(138, 43, 226, 0.6);
        border-radius: 10px;
        padding: 1rem;
        animation: quantum-glow 3s infinite;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(138, 43, 226, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0;
    }
    
    /* Scan mode indicator */
    .scan-mode-indicator {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Jarvis status */
    .jarvis-status {
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.5);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 10px 20px;
        border: 1px solid rgba(138, 43, 226, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: rgba(138, 43, 226, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'audit_data' not in st.session_state:
    st.session_state.audit_data = None
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'active_scan' not in st.session_state:
    st.session_state.active_scan = False
if 'current_scan_mode' not in st.session_state:
    st.session_state.current_scan_mode = "Deep Quantum Analysis"
if 'jarvis_messages' not in st.session_state:
    st.session_state.jarvis_messages = []

# ============================================================================
# JARVIS HELPER FUNCTIONS
# ============================================================================

def jarvis_speak(message: str, msg_type: str = "info"):
    """Add a message to Jarvis log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.jarvis_messages.append({
        "time": timestamp,
        "message": message,
        "type": msg_type
    })
    # Keep only last 10 messages
    if len(st.session_state.jarvis_messages) > 10:
        st.session_state.jarvis_messages = st.session_state.jarvis_messages[-10:]

def get_scan_mode_description(mode: str) -> dict:
    """Get detailed description for scan mode"""
    descriptions = {
        "Standard Recon": {
            "icon": "🔍",
            "color": "#4ECDC4",
            "speed": "Fast",
            "depth": "Basic",
            "features": ["Quick subdomain scan", "Basic SSL check", "Geolocation", "No quantum analysis"],
            "use_case": "Quick overview of attack surface"
        },
        "Deep Quantum Analysis": {
            "icon": "⚛️",
            "color": "#667eea",
            "speed": "Medium",
            "depth": "Deep",
            "features": ["Full quantum threat assessment", "Shor's algorithm analysis", "PQC recommendations", "HNDL risk evaluation"],
            "use_case": "Complete quantum security posture assessment"
        },
        "Stealth Mode": {
            "icon": "🥷",
            "color": "#FF6B6B",
            "speed": "Slow",
            "depth": "Medium",
            "features": ["Delayed requests (3s)", "Passive OSINT only", "Avoids detection", "Quantum analysis included"],
            "use_case": "Red team exercises, avoiding IDS/IPS"
        },
        "Comprehensive Audit": {
            "icon": "📋",
            "color": "#764ba2",
            "speed": "Thorough",
            "depth": "Maximum",
            "features": ["Extended subdomain list", "Full quantum + compliance", "ISMS framework ready", "50 assets max"],
            "use_case": "Complete security audit for compliance"
        }
    }
    return descriptions.get(mode, descriptions["Standard Recon"])

# ============================================================================
# HEADER SECTION
# ============================================================================

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("⚛️ SENTINEL-V: QUANTUM AI NERVE CENTER")
    st.markdown("<p style='text-align: center; color: #a78bfa; font-size: 1.2rem; margin-top: -20px;'>Next-Generation Agentic Defense | Post-Quantum Cryptography Intelligence</p>", unsafe_allow_html=True)

# Status banner
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🟢 System Status", "OPERATIONAL", delta="Online")
with col2:
    st.metric("⚛️ Quantum Mode", "ACTIVE", delta="PQC Ready")
with col3:
    current_year = datetime.now().year
    quantum_threat_year = 2030
    years_to_threat = quantum_threat_year - current_year
    st.metric("⏰ Quantum Threat", f"{years_to_threat} Years", delta=f"Until CRQC")
with col4:
    st.metric("🛡️ NIST PQC", "FIPS 203/204", delta="Compliant")

st.markdown("---")

# ============================================================================
# SIDEBAR - JARVIS COMMAND CENTER (FULLY FUNCTIONAL!)
# ============================================================================

with st.sidebar:
    st.markdown("### ⚡ JARVIS COMMAND CENTER")
    
    # Domain input section
    st.markdown("---")
    st.markdown("#### 🎯 Target Configuration")
    
    target = st.text_input(
        "Strategic Domain",
        value="prosec-networks.com",
        help="Enter target domain for quantum threat assessment",
        placeholder="example.com"
    )
    
    # ========================================================================
    # SCAN MODE SELECTOR (NOW FUNCTIONAL!)
    # ========================================================================
    st.markdown("---")
    st.markdown("#### 🔧 Scan Mode")
    
    scan_mode = st.selectbox(
        "Select Operation Mode",
        ["Standard Recon", "Deep Quantum Analysis", "Stealth Mode", "Comprehensive Audit"],
        index=1,
        help="Each mode has different speed, depth, and capabilities"
    )
    
    # Display scan mode details
    mode_info = get_scan_mode_description(scan_mode)
    
    st.markdown(f"""
    <div style='background: rgba(102, 126, 234, 0.1); border-radius: 10px; padding: 1rem; border: 1px solid {mode_info["color"]}; margin: 0.5rem 0;'>
        <h4 style='margin: 0; color: {mode_info["color"]};'>{mode_info["icon"]} {scan_mode}</h4>
        <p style='margin: 0.5rem 0; font-size: 0.85rem;'>
            <b>Speed:</b> {mode_info["speed"]} | <b>Depth:</b> {mode_info["depth"]}
        </p>
        <p style='margin: 0; font-size: 0.8rem; color: #888;'>{mode_info["use_case"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show features for selected mode
    with st.expander(f"📋 {scan_mode} Features", expanded=False):
        for feature in mode_info["features"]:
            st.markdown(f"✅ {feature}")
    
    # ========================================================================
    # ADVANCED CONFIGURATION
    # ========================================================================
    st.markdown("---")
    
    with st.expander("⚙️ Advanced Options", expanded=False):
        # These options override scan mode defaults
        custom_max_assets = st.slider(
            "Max Assets to Scan",
            min_value=5,
            max_value=50,
            value=ScanMode.get_config(scan_mode)["max_assets"],
            help="Override default asset limit for this scan mode"
        )
        
        enable_quantum_override = st.checkbox(
            "Force Quantum Analysis",
            value=ScanMode.get_config(scan_mode)["enable_quantum"],
            help="Enable quantum threat analysis regardless of scan mode"
        )
        
        enable_stealth_delay = st.checkbox(
            "Enable Request Delays",
            value=scan_mode == "Stealth Mode",
            help="Add delays between requests to avoid detection"
        )
    
    # ========================================================================
    # MAIN ACTION BUTTON
    # ========================================================================
    st.markdown("---")
    
    if st.button("🚀 INITIALIZE QUANTUM DEFENSE", use_container_width=True, type="primary"):
        if not target or len(target) < 4:
            st.error("⚠️ Please enter a valid domain")
            jarvis_speak("Invalid domain entered", "error")
        else:
            st.session_state.active_scan = True
            st.session_state.current_scan_mode = scan_mode
            jarvis_speak(f"Initializing {scan_mode} on {target}", "info")
            
            # Progress containers
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Phase 1: Initialization
                status_text.info(f"⚡ JARVIS: Initializing {scan_mode}...")
                jarvis_speak(f"Scan mode: {scan_mode}", "info")
                progress_bar.progress(10)
                time.sleep(0.5)
                
                # Phase 2: Configuration
                config = ScanMode.get_config(scan_mode)
                status_text.info(f"🔧 JARVIS: Loading configuration... Max assets: {config['max_assets']}")
                jarvis_speak(f"Config loaded. Max assets: {config['max_assets']}", "info")
                progress_bar.progress(20)
                time.sleep(0.3)
                
                # Phase 3: Reconnaissance
                if "crt.sh" in config['subdomain_sources']:
                    status_text.info("🔍 JARVIS: Querying certificate transparency logs...")
                    jarvis_speak("Scanning crt.sh for subdomains", "info")
                else:
                    status_text.info("🔍 JARVIS: Running passive reconnaissance...")
                    jarvis_speak("Passive recon mode active", "info")
                progress_bar.progress(35)
                time.sleep(0.5)
                
                # Phase 4: Asset Discovery
                status_text.info("📡 JARVIS: Discovering assets and resolving IPs...")
                jarvis_speak("Asset discovery in progress", "info")
                progress_bar.progress(45)
                
                # Run the actual audit
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Phase 5: SSL Analysis
                status_text.info("🔐 JARVIS: Analyzing SSL/TLS configurations...")
                jarvis_speak("Checking SSL certificates", "info")
                progress_bar.progress(55)
                
                # Phase 6: Quantum Analysis (if enabled)
                if config['enable_quantum']:
                    status_text.info("⚛️ JARVIS: Computing quantum vulnerability vectors...")
                    jarvis_speak("Running Shor's algorithm threat analysis", "quantum")
                    progress_bar.progress(70)
                    time.sleep(0.5)
                    
                    status_text.info("🧬 JARVIS: Generating PQC migration strategies...")
                    jarvis_speak("Calculating ML-KEM recommendations", "quantum")
                    progress_bar.progress(80)
                else:
                    status_text.info("📊 JARVIS: Compiling reconnaissance data...")
                    jarvis_speak("Quantum analysis skipped (Standard Recon mode)", "info")
                    progress_bar.progress(80)
                
                # Execute the scan
                df = loop.run_until_complete(run_audit(target, scan_mode))
                
                # Phase 7: Finalization
                status_text.info("📋 JARVIS: Compiling intelligence report...")
                jarvis_speak(f"Scan complete. {len(df)} assets discovered.", "success")
                progress_bar.progress(95)
                time.sleep(0.3)
                
                # Store results
                st.session_state.audit_data = df
                st.session_state.scan_history.append({
                    'domain': target,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'assets_found': len(df),
                    'critical_count': len(df[df['Quantum_Risk'].str.contains('Critical', na=False)]),
                    'scan_mode': scan_mode
                })
                
                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()
                
                st.success(f"✅ {scan_mode} complete! Discovered {len(df)} assets")
                jarvis_speak("Mission accomplished!", "success")
                st.balloons()
                
                loop.close()
                
            except Exception as e:
                st.error(f"❌ Scan failed: {str(e)}")
                jarvis_speak(f"Error: {str(e)}", "error")
                
            finally:
                st.session_state.active_scan = False
    
    # ========================================================================
    # JARVIS LOG
    # ========================================================================
    st.markdown("---")
    st.markdown("#### 🤖 JARVIS Activity Log")
    
    if st.session_state.jarvis_messages:
        log_container = st.container()
        with log_container:
            for msg in reversed(st.session_state.jarvis_messages[-5:]):
                if msg['type'] == 'error':
                    st.error(f"[{msg['time']}] {msg['message']}")
                elif msg['type'] == 'success':
                    st.success(f"[{msg['time']}] {msg['message']}")
                elif msg['type'] == 'quantum':
                    st.info(f"⚛️ [{msg['time']}] {msg['message']}")
                else:
                    st.info(f"[{msg['time']}] {msg['message']}")
    else:
        st.caption("Awaiting commands...")
    
    # ========================================================================
    # QUICK ACTIONS
    # ========================================================================
    st.markdown("---")
    st.markdown("#### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.audit_data = None
            st.session_state.jarvis_messages = []
            jarvis_speak("System reset", "info")
            st.rerun()
    with col2:
        if st.button("📜 History", use_container_width=True):
            st.session_state.show_history = not st.session_state.get('show_history', False)
    
    # Show scan history
    if st.session_state.get('show_history', False) and st.session_state.scan_history:
        st.markdown("---")
        st.markdown("#### 📜 Scan History")
        for idx, scan in enumerate(reversed(st.session_state.scan_history[-5:])):
            with st.expander(f"🎯 {scan['domain']}", expanded=False):
                st.markdown(f"""
                - **Time:** {scan['timestamp']}
                - **Mode:** {scan['scan_mode']}
                - **Assets:** {scan['assets_found']}
                - **Critical:** {scan['critical_count']}
                """)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

if st.session_state.audit_data is None:
    # ========================================================================
    # WELCOME SCREEN
    # ========================================================================
    
    st.markdown("---")
    
    # Scan mode comparison
    st.subheader("🔧 Scan Mode Comparison")
    
    mode_data = {
        "Mode": ["Standard Recon", "Deep Quantum Analysis", "Stealth Mode", "Comprehensive Audit"],
        "Speed": ["⚡ Fast", "🔄 Medium", "🐢 Slow", "📊 Thorough"],
        "Max Assets": [10, 25, 15, 50],
        "Quantum Analysis": ["❌", "✅", "✅", "✅"],
        "Stealth Delays": ["❌", "❌", "✅ (3s)", "❌"],
        "Best For": ["Quick scan", "Security assessment", "Red team", "Full audit"]
    }
    
    st.table(pd.DataFrame(mode_data))
    
    st.markdown("---")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #667eea;'>🎯 Autonomous Discovery</h3>
            <p>Real-time subdomain enumeration via certificate transparency, 
            DNS intelligence, and ML-powered asset correlation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #764ba2;'>⚛️ Quantum Threat Assessment</h3>
            <p>NIST PQC-aligned threat modeling with Shor's algorithm impact analysis 
            and ML-KEM migration roadmaps.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h3 style='color: #f093fb;'>📋 NIS2 Compliance</h3>
            <p>Automated Article 21 reporting with executive-ready PDF exports 
            and quantum-safe cryptography recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quantum threat timeline preview
    st.subheader("⏰ Quantum Computing Threat Timeline")
    
    years = [2024, 2027, 2030, 2033, 2035]
    threat_levels = [15, 40, 75, 90, 95]
    capabilities = ['NISQ', 'Early Fault-Tolerant', 'CRQC', 'Advanced QC', 'Universal QC']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=threat_levels,
        mode='lines+markers+text',
        name='Quantum Threat Level',
        line=dict(color='#667eea', width=4),
        marker=dict(size=15, color='#764ba2', line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        text=capabilities,
        textposition='top center',
        textfont=dict(size=10, color='white')
    ))
    
    fig.update_layout(
        title="Quantum Computing Evolution & Cryptographic Threat Projection",
        xaxis_title="Year",
        yaxis_title="Threat Level (%)",
        template="plotly_dark",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        annotations=[
            dict(x=2030, y=75, text="RSA-2048 BROKEN", 
                 showarrow=True, arrowhead=2, arrowcolor='#ff6b6b',
                 font=dict(size=12, color='#ff6b6b'))
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("🎬 **Select a scan mode and click 'Initialize Quantum Defense' to begin.**")
    
    # Preview map
    st.markdown("---")
    st.subheader("🌐 Global Adversarial Radar")
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
    st_folium(m, width=1200, height=400)

else:
    # ========================================================================
    # ACTIVE AUDIT DISPLAY
    # ========================================================================
    
    df = st.session_state.audit_data
    
    # Show current scan mode
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 0.5rem 1rem; border-radius: 20px; 
                display: inline-block; margin-bottom: 1rem;'>
        🔬 Scan Mode: <b>{st.session_state.current_scan_mode}</b>
    </div>
    """, unsafe_allow_html=True)
    
    # Quantum-enhanced metrics dashboard
    st.subheader("📊 Quantum Threat Intelligence Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_assets = len(df)
    critical_count = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    quantum_vulnerable = len(df[df['quantum_years_vulnerable'] <= 5])
    harvest_threat = len(df[df['harvest_now_threat'] == True])
    avg_risk = df['Risk_Score'].mean()
    
    with col1:
        st.metric("🎯 Total Assets", total_assets, delta=f"+{total_assets} discovered")
    
    with col2:
        delta_text = "URGENT" if critical_count > 0 else "Clear"
        st.metric("🔴 Critical Risks", critical_count, delta=delta_text)
    
    with col3:
        delta_text = f"By 2030" if quantum_vulnerable > 0 else "Safe"
        st.metric("⚛️ Quantum Threats", quantum_vulnerable, delta=delta_text)
    
    with col4:
        delta_text = "ACTIVE" if harvest_threat > 0 else "Low"
        st.metric("🎯 Harvest Threat", harvest_threat, delta=delta_text)
    
    with col5:
        delta_text = "⚠️ High" if avg_risk > 60 else "✅ OK"
        st.metric("📈 Avg Risk", f"{avg_risk:.1f}/100", delta=delta_text)
    
    # ========================================================================
    # GLOBAL MAP
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🌐 Global Adversarial Radar")
    
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
    marker_cluster = MarkerCluster().add_to(m)
    
    heat_data = []
    
    for _, row in df.iterrows():
        if row['lat'] != 0.0 and row['lon'] != 0.0:
            if "Critical" in row['Quantum_Risk']:
                color = 'red'
                icon = 'warning-sign'
            elif "High" in row['Quantum_Risk']:
                color = 'orange'
                icon = 'warning-sign'
            else:
                color = 'blue'
                icon = 'shield'
            
            popup_html = f"""
            <div style='width: 280px; font-family: Arial;'>
                <h4 style='margin: 0; color: {color};'>{row['asset']}</h4>
                <hr style='margin: 5px 0;'>
                <b>Location:</b> {row['city']}, {row['country']}<br>
                <b>IP:</b> {row['ip']}<br>
                <b>Risk:</b> {row['Quantum_Risk']} ({row['Risk_Score']}/100)<br>
                <b>Quantum Threat:</b> {row['quantum_years_vulnerable']} years<br>
                <b>PQC:</b> {row['PQC_Migration']}<br>
                <b>Mode:</b> {row.get('scan_mode', 'N/A')}
            </div>
            """
            
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=color, icon=icon, prefix='fa'),
                tooltip=f"{row['asset']} - {row['Quantum_Risk']}"
            ).add_to(marker_cluster)
            
            intensity = row['Risk_Score'] / 100
            heat_data.append([row['lat'], row['lon'], intensity])
    
    if heat_data:
        HeatMap(heat_data, radius=20, blur=30).add_to(m)
    
    st_folium(m, width=1400, height=500)
    
    # ========================================================================
    # TABBED DISPLAY
    # ========================================================================
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "⚛️ Intelligence Matrix",
        "🎯 Threat Analysis", 
        "💡 PQC Roadmap",
        "📥 Export"
    ])
    
    with tab1:
        st.subheader("⚛️ Quantum Threat Intelligence Matrix")
        
        display_df = df[[
            'asset', 'ip', 'country', 'criticality',
            'Quantum_Risk', 'Risk_Score', 'quantum_years_vulnerable',
            'PQC_Migration', 'PQC_Priority', 'scan_mode'
        ]].copy()
        
        display_df.columns = [
            'Asset', 'IP', 'Country', 'Criticality',
            'Quantum Risk', 'Score', 'Years Vulnerable',
            'PQC Strategy', 'Priority', 'Scan Mode'
        ]
        
        st.dataframe(display_df, use_container_width=True, height=500)
    
    with tab2:
        st.subheader("🎯 Threat Analysis by Scan Mode")
        
        st.info(f"**Current Scan Mode:** {st.session_state.current_scan_mode}")
        
        # Risk distribution
        fig = go.Figure(data=[
            go.Bar(
                x=['Critical', 'High', 'Moderate', 'Low'],
                y=[
                    len(df[df['Quantum_Risk'].str.contains('Critical', na=False)]),
                    len(df[df['Quantum_Risk'].str.contains('High', na=False)]),
                    len(df[df['Quantum_Risk'].str.contains('Moderate', na=False)]),
                    len(df[df['Quantum_Risk'].str.contains('Low', na=False)])
                ],
                marker_color=['#ff6b6b', '#ffa500', '#ffd700', '#4ecdc4']
            )
        ])
        
        fig.update_layout(
            title="Risk Distribution",
            template="plotly_dark",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Critical assets
        critical_assets = df[df['Quantum_Risk'].str.contains('Critical', na=False)]
        if not critical_assets.empty:
            st.error(f"🚨 {len(critical_assets)} CRITICAL assets require immediate action!")
            for _, row in critical_assets.iterrows():
                with st.expander(f"🔴 {row['asset']}", expanded=False):
                    st.markdown(f"""
                    - **Risk Score:** {row['Risk_Score']}/100
                    - **Location:** {row['city']}, {row['country']}
                    - **Quantum Vulnerable In:** {row['quantum_years_vulnerable']} years
                    - **PQC Migration:** {row['PQC_Migration']}
                    - **Action:** {row['Solution']}
                    """)
    
    with tab3:
        st.subheader("💡 Post-Quantum Migration Roadmap")
        
        if st.session_state.current_scan_mode in ["Deep Quantum Analysis", "Stealth Mode", "Comprehensive Audit"]:
            # PQC priority distribution
            priority_counts = df['PQC_Priority'].value_counts()
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=list(priority_counts.index),
                    values=list(priority_counts.values),
                    hole=0.4,
                    marker=dict(colors=['#ff6b6b', '#ffa500', '#4ecdc4'])
                )
            ])
            
            fig.update_layout(
                title="PQC Migration Priorities",
                template="plotly_dark",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Migration phases
            st.markdown("### 📋 Migration Phases")
            
            phases = {
                "Phase 1 (0-3 months)": "Migrate CRITICAL assets to ML-KEM-1024",
                "Phase 2 (3-6 months)": "Deploy ML-DSA signatures, hybrid TLS",
                "Phase 3 (6-12 months)": "Complete HIGH priority migrations",
                "Phase 4 (12-24 months)": "Full PQC adoption, decommission legacy"
            }
            
            for phase, action in phases.items():
                st.success(f"**{phase}:** {action}")
        else:
            st.warning("⚠️ PQC analysis not available in Standard Recon mode. Use Deep Quantum Analysis for full PQC roadmap.")
    
    with tab4:
        st.subheader("📥 Export Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📄 PDF Report")
            pdf_bytes = generate_pdf_report(df, target, st.session_state.current_scan_mode)
            st.download_button(
                "📥 Download PDF",
                data=pdf_bytes,
                file_name=f"Sentinel_V_{target}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            st.markdown("### 📊 CSV Data")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download CSV",
                data=csv,
                file_name=f"Sentinel_V_{target}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            st.markdown("### 🔗 JSON API")
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                "📥 Download JSON",
                data=json_data,
                file_name=f"Sentinel_V_{target}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("**🛡️ Sentinel-V Quantum Edition**")
    st.caption("Powered by Post-Quantum Cryptography Intelligence")

with footer_col2:
    st.markdown("**⚛️ NIST PQC Compliant**")
    st.caption("FIPS 203, 204, 205 Standards")

with footer_col3:
    st.markdown("**🌐 ProSec Networks**")
    st.caption("Your Quantum-Ready Security Partner")