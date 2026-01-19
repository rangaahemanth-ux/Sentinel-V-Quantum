"""
Sentinel-V: Quantum AI Nerve Center
Complete command center with quantum threat intelligence integration
"""

import streamlit as st
import asyncio
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster
from core import SentinelAgent, generate_pdf_report, run_audit
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
    
    /* Quantum particle effect */
    .quantum-particles {
        background-image: radial-gradient(circle, rgba(138, 43, 226, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
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
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(138, 43, 226, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(138, 43, 226, 0.3);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(138, 43, 226, 0.3);
        border-radius: 8px;
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
if 'quantum_demo_active' not in st.session_state:
    st.session_state.quantum_demo_active = False

# ============================================================================
# HEADER SECTION
# ============================================================================

# Animated header with quantum theme
st.markdown("<div class='quantum-particles'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("⚛️ SENTINEL-V: QUANTUM AI NERVE CENTER")
    st.markdown("<p style='text-align: center; color: #a78bfa; font-size: 1.2rem; margin-top: -20px;'>Next-Generation Agentic Defense | Post-Quantum Cryptography Intelligence</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

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
# SIDEBAR - COMMAND INTERFACE
# ============================================================================

with st.sidebar:
    st.markdown("### ⚡ JARVIS COMMAND CENTER")
    st.markdown("<div class='quantum-border'>", unsafe_allow_html=True)
    
    # Domain input
    target = st.text_input(
        "🎯 Strategic Domain",
        value="prosec-networks.com",
        help="Enter target domain for quantum threat assessment",
        placeholder="example.com"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Advanced options
    with st.expander("🔧 Advanced Configuration"):
        scan_mode = st.selectbox(
            "Scan Mode",
            ["Standard Recon", "Deep Quantum Analysis", "Stealth Mode", "Comprehensive Audit"],
            index=1
        )
        
        enable_quantum_sim = st.checkbox("Enable Quantum Simulations", value=True)
        enable_threat_timeline = st.checkbox("Generate Threat Timeline", value=True)
        enable_pqc_roadmap = st.checkbox("PQC Migration Roadmap", value=True)
        
        max_assets = st.slider("Max Assets to Scan", 10, 50, 20)
    
    st.markdown("---")
    
    # Main action button
    if st.button("🚀 INITIALIZE QUANTUM DEFENSE", use_container_width=True, type="primary"):
        if not target or len(target) < 4:
            st.error("⚠️ Please enter a valid domain")
        else:
            st.session_state.active_scan = True
            
            with st.spinner("⚛️ Deploying Quantum-Aware Sentinel Agents..."):
                try:
                    # Progress tracking
                    progress_container = st.empty()
                    status_container = st.empty()
                    
                    def update_progress(percent, message):
                        progress_container.progress(percent / 100)
                        status_container.info(f"🔬 {message}")
                    
                    update_progress(10, "Initializing quantum threat analyzer...")
                    time.sleep(0.5)
                    
                    update_progress(25, "Scanning certificate transparency logs...")
                    time.sleep(0.5)
                    
                    # Run async audit
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    update_progress(40, "Resolving IP addresses & geolocations...")
                    time.sleep(0.5)
                    
                    update_progress(55, "Analyzing SSL/TLS configurations...")
                    df = loop.run_until_complete(run_audit(target))
                    
                    update_progress(70, "Computing quantum vulnerability vectors...")
                    time.sleep(0.5)
                    
                    update_progress(85, "Generating PQC migration strategies...")
                    time.sleep(0.5)
                    
                    update_progress(100, "Compiling quantum intelligence report...")
                    time.sleep(0.5)
                    
                    # Store results
                    st.session_state.audit_data = df
                    st.session_state.scan_history.append({
                        'domain': target,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'assets_found': len(df),
                        'quantum_vulnerable': len(df[df['quantum_years_vulnerable'] <= 5]),
                        'scan_mode': scan_mode
                    })
                    
                    st.session_state.active_scan = False
                    
                    progress_container.empty()
                    status_container.empty()
                    
                    st.success(f"✅ Quantum audit complete! Discovered {len(df)} assets")
                    st.balloons()
                    
                    loop.close()
                    
                except Exception as e:
                    st.error(f"❌ Scan failed: {str(e)}")
                    st.session_state.active_scan = False
    
    # Quick actions
    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.audit_data = None
            st.rerun()
    with col2:
        if st.button("📊 Demo", use_container_width=True):
            st.session_state.quantum_demo_active = True
    
    # Scan history
    if st.session_state.scan_history:
        st.markdown("---")
        st.markdown("### 📜 Scan History")
        for idx, scan in enumerate(reversed(st.session_state.scan_history[-5:])):
            with st.expander(f"🎯 {scan['domain']}", expanded=False):
                st.text(f"⏰ {scan['timestamp']}")
                st.text(f"📦 {scan['assets_found']} assets")
                st.text(f"⚛️ {scan['quantum_vulnerable']} quantum-vulnerable")
                st.text(f"🔬 Mode: {scan['scan_mode']}")

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

if st.session_state.audit_data is None:
    # ========================================================================
    # WELCOME SCREEN
    # ========================================================================
    
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
    
    st.info("🎬 **Initialize the Sentinel Agent to begin quantum threat assessment.** Click 'Initialize Quantum Defense' in the sidebar.")
    
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
    
    # Quantum-enhanced metrics dashboard
    st.markdown("---")
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
        delta_text = f"Vulnerable by 2030" if quantum_vulnerable > 0 else "Safe"
        st.metric("⚛️ Quantum Threats", quantum_vulnerable, delta=delta_text)
    
    with col4:
        delta_text = "ACTIVE" if harvest_threat > 0 else "Low"
        st.metric("🎯 Harvest Threat", harvest_threat, delta=delta_text)
    
    with col5:
        delta_text = "⚠️ High" if avg_risk > 60 else "✅ Acceptable"
        st.metric("📈 Avg Risk Score", f"{avg_risk:.1f}/100", delta=delta_text)
    
    # ========================================================================
    # GLOBAL MAP WITH QUANTUM OVERLAY
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🌐 Global Adversarial Radar with Quantum Threat Overlay")
    
    # Create sophisticated map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
    marker_cluster = MarkerCluster().add_to(m)
    
    # Prepare heatmap data
    heat_data = []
    
    for _, row in df.iterrows():
        if row['lat'] != 0.0 and row['lon'] != 0.0:
            # Determine marker properties based on quantum risk
            if "Critical" in row['Quantum_Risk']:
                color = 'red'
                icon = 'radiation'
            elif "High" in row['Quantum_Risk'] or "Quantum Vulnerable" in row['Quantum_Risk']:
                color = 'orange'
                icon = 'warning-sign'
            else:
                color = 'blue'
                icon = 'shield'
            
            # Create quantum-aware popup
            quantum_status = "⚛️ QUANTUM-SAFE" if row['quantum_safe_crypto'] else "⚠️ QUANTUM-VULNERABLE"
            harvest_status = "🎯 HARVEST THREAT" if row['harvest_now_threat'] else "✓ Low Risk"
            
            popup_html = f"""
            <div style='width: 300px; font-family: Arial;'>
                <h3 style='margin: 0; color: {color}; border-bottom: 2px solid {color};'>
                    {row['asset']}
                </h3>
                <div style='margin-top: 10px;'>
                    <b>🌍 Location:</b> {row['city']}, {row['country']}<br>
                    <b>🔗 IP:</b> {row['ip']}<br>
                    <b>🏢 ISP:</b> {row['isp'][:40]}<br>
                    <hr style='margin: 8px 0;'>
                    <b>🛡️ Risk Level:</b> {row['Quantum_Risk']}<br>
                    <b>📊 Risk Score:</b> {row['Risk_Score']}/100<br>
                    <b>🎯 Criticality:</b> {row['criticality']}<br>
                    <hr style='margin: 8px 0;'>
                    <b>⚛️ Quantum Status:</b> {quantum_status}<br>
                    <b>🔐 Current Crypto:</b> {row['ssl_cipher'][:30]}<br>
                    <b>⏰ Vulnerable In:</b> {row['quantum_years_vulnerable']} years<br>
                    <b>🎯 Threat Type:</b> {row['quantum_threat_algorithm']}'s Algorithm<br>
                    <b>{harvest_status}</b><br>
                    <hr style='margin: 8px 0;'>
                    <b>💡 PQC Migration:</b> {row['PQC_Migration']}<br>
                    <b>⏱️ Timeline:</b> {row['PQC_Timeline']}<br>
                    <b>🚨 Priority:</b> {row['PQC_Priority']}<br>
                    <hr style='margin: 8px 0;'>
                    <b>📋 Action:</b><br>{row['Solution'][:100]}...
                </div>
            </div>
            """
            
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=folium.Popup(popup_html, max_width=350),
                icon=folium.Icon(color=color, icon=icon, prefix='fa'),
                tooltip=f"{row['asset']} - {row['Quantum_Risk']}"
            ).add_to(marker_cluster)
            
            # Add to heatmap with quantum risk intensity
            intensity = row['Risk_Score'] / 100
            heat_data.append([row['lat'], row['lon'], intensity])
    
    # Add heatmap layer
    if heat_data:
        HeatMap(
            heat_data,
            radius=20,
            blur=30,
            max_zoom=13,
            gradient={0.4: 'blue', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}
        ).add_to(m)
    
    st_folium(m, width=1400, height=500)
    
    # ========================================================================
    # TABBED INTELLIGENCE DISPLAY
    # ========================================================================
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚛️ Quantum Intelligence",
        "🎯 Threat Analysis",
        "💡 PQC Migration",
        "📊 Analytics & Insights",
        "📥 Export & Reporting"
    ])
    
    # TAB 1: Quantum Intelligence Matrix
    with tab1:
        st.subheader("⚛️ Quantum Threat Intelligence Matrix")
        
        st.markdown("""
        **Understanding the Data:**
        - **Quantum Risk:** Overall threat level combining classical and quantum vulnerabilities
        - **Quantum Years Vulnerable:** Time until quantum computers can break current encryption
        - **Harvest Threat:** Data encrypted today could be decrypted in the future
        - **PQC Migration:** Recommended NIST-approved post-quantum algorithms
        """)
        
        # Display comprehensive dataframe
        display_df = df[[
            'asset', 'ip', 'country', 'criticality',
            'Quantum_Risk', 'Risk_Score', 'quantum_years_vulnerable',
            'quantum_threat_algorithm', 'PQC_Migration', 'PQC_Priority',
            'harvest_now_threat', 'quantum_safe_crypto'
        ]].copy()
        
        display_df.columns = [
            'Asset', 'IP Address', 'Country', 'Criticality',
            'Quantum Risk', 'Risk Score', 'Years Vulnerable',
            'Threat Algorithm', 'PQC Strategy', 'Priority',
            'Harvest Threat', 'Quantum-Safe'
        ]
        
        # Color-code the dataframe
        def highlight_risk(val):
            if isinstance(val, str):
                if 'Critical' in val or 'CRITICAL' in val or 'P0' in val:
                    return 'background-color: #ff6b6b'
                elif 'High' in val or 'HIGH' in val or 'P1' in val:
                    return 'background-color: #ffa500'
                elif val == True or val == 'True':
                    return 'background-color: #ff6b6b'
            return ''
        
        st.dataframe(
            display_df.style.applymap(highlight_risk),
            use_container_width=True,
            height=500
        )
        
        # Download quantum intelligence as JSON
        if st.button("📥 Download Quantum Intelligence (JSON)"):
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                "Download JSON",
                data=json_data,
                file_name=f"quantum_intelligence_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # TAB 2: Threat Analysis
    with tab2:
        st.subheader("🎯 Prioritized Threat Analysis")
        
        # Quantum threat timeline for assets
        st.markdown("### ⏰ Quantum Vulnerability Timeline")
        
        vulnerability_years = df['quantum_years_vulnerable'].value_counts().sort_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(vulnerability_years.index),
                y=list(vulnerability_years.values),
                marker=dict(
                    color=list(vulnerability_years.values),
                    colorscale='Reds',
                    showscale=True
                ),
                text=list(vulnerability_years.values),
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Asset Distribution by Years Until Quantum Vulnerability",
            xaxis_title="Years Until Vulnerable",
            yaxis_title="Number of Assets",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Threat breakdown
        st.markdown("---")
        st.markdown("### 🔍 Detailed Threat Breakdown")
        
        # Critical assets requiring immediate action
        critical_assets = df[df['Quantum_Risk'].str.contains('Critical', na=False)]
        high_assets = df[df['Quantum_Risk'].str.contains('High', na=False)]
        moderate_assets = df[~df['Quantum_Risk'].str.contains('Critical|High', na=False)]
        
        if not critical_assets.empty:
            st.error(f"🚨 **CRITICAL PRIORITY** - {len(critical_assets)} Assets Require Immediate Action")
            for _, row in critical_assets.iterrows():
                with st.expander(f"🔴 {row['asset']} - Risk Score: {row['Risk_Score']}/100", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **📍 Asset Details:**
                        - Location: {row['city']}, {row['country']}
                        - IP: {row['ip']}
                        - ISP: {row['isp']}
                        - Criticality: {row['criticality']}
                        
                        **⚛️ Quantum Threat:**
                        - Algorithm: {row['quantum_threat_algorithm']}'s
                        - Years Vulnerable: {row['quantum_years_vulnerable']}
                        - Harvest Threat: {'🎯 ACTIVE' if row['harvest_now_threat'] else '✓ Low'}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **🛡️ Current Security:**
                        - SSL: {row['ssl_version']}
                        - Cipher: {row['ssl_cipher'][:40]}
                        - Quantum-Safe: {'✅ Yes' if row['quantum_safe_crypto'] else '❌ No'}
                        
                        **💡 PQC Migration:**
                        - Recommended: {row['PQC_Migration']}
                        - Signature: {row['PQC_Signature']}
                        - Priority: {row['PQC_Priority']}
                        - Timeline: {row['PQC_Timeline']}
                        """)
                    
                    st.warning(f"**🚨 REQUIRED ACTION:** {row['Solution']}")
        
        if not high_assets.empty:
            st.warning(f"⚠️ **HIGH PRIORITY** - {len(high_assets)} Assets Need Migration Planning")
            for _, row in high_assets.iterrows():
                with st.expander(f"🟠 {row['asset']} - Risk Score: {row['Risk_Score']}/100"):
                    st.markdown(f"""
                    **Quantum Threat:** {row['quantum_threat_algorithm']}'s algorithm breaks this in {row['quantum_years_vulnerable']} years  
                    **Recommendation:** {row['Solution']}  
                    **PQC Strategy:** Migrate to {row['PQC_Migration']} within {row['PQC_Timeline']}
                    """)
        
        if not moderate_assets.empty:
            st.success(f"✅ **STANDARD MONITORING** - {len(moderate_assets)} Assets Under Normal Security Posture")
            st.caption("These assets have acceptable risk levels but should be reviewed quarterly.")
    
    # TAB 3: PQC Migration Roadmap
    with tab3:
        st.subheader("💡 Post-Quantum Cryptography Migration Roadmap")
        
        st.markdown("""
        ### 🎯 NIST Post-Quantum Cryptography Standards
        
        In 2024, NIST finalized the following quantum-resistant algorithms:
        
        - **FIPS 203 (ML-KEM):** Module-Lattice-Based Key-Encapsulation Mechanism
        - **FIPS 204 (ML-DSA):** Module-Lattice-Based Digital Signature Algorithm
        - **FIPS 205 (SLH-DSA):** Stateless Hash-Based Digital Signature Algorithm
        """)
        
        # Migration priority breakdown
        st.markdown("---")
        st.markdown("### 📊 Migration Priority Distribution")
        
        priority_counts = df['PQC_Priority'].value_counts()
        
        fig = go.Figure(data=[
            go.Pie(
                labels=list(priority_counts.index),
                values=list(priority_counts.values),
                hole=0.4,
                marker=dict(colors=['#ff6b6b', '#ffa500', '#4ecdc4']),
                textinfo='label+percent+value'
            )
        ])
        
        fig.update_layout(
            title="PQC Migration Priorities",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed migration roadmap
        st.markdown("---")
        st.markdown("### 🗓️ Phased Migration Timeline")
        
        phases = {
            "Phase 1: Assessment & Planning (Weeks 1-4)": [
                "Inventory all cryptographic assets and dependencies",
                "Identify critical systems requiring immediate PQC migration",
                "Select appropriate NIST-approved PQC algorithms",
                "Design hybrid classical-PQC architecture",
                "Assess performance impacts and compatibility"
            ],
            "Phase 2: Pilot Deployment (Weeks 5-12)": [
                "Deploy PQC to isolated test environment",
                "Conduct performance benchmarking",
                "Test interoperability with existing systems",
                "Train technical teams on PQC implementation",
                "Document lessons learned and optimize"
            ],
            "Phase 3: Production Rollout (Months 3-6)": [
                "Begin with P0 critical assets",
                "Implement hybrid mode for backwards compatibility",
                "Monitor system performance and stability",
                "Gradual expansion to P1 and P2 assets",
                "Continuous security testing and validation"
            ],
            "Phase 4: Full Migration (Months 6-12)": [
                "Complete migration of all production systems",
                "Decommission legacy classical-only crypto",
                "Implement cryptographic agility framework",
                "Establish ongoing quantum threat monitoring",
                "Regular compliance audits and updates"
            ]
        }
        
        for phase, tasks in phases.items():
            with st.expander(phase, expanded=True):
                for task in tasks:
                    st.markdown(f"- {task}")
        
        # Asset-specific recommendations
        st.markdown("---")
        st.markdown("### 🎯 Asset-Specific PQC Recommendations")
        
        for _, row in df.iterrows():
            if row['quantum_years_vulnerable'] <= 5:  # Show only urgent ones
                with st.expander(f"⚛️ {row['asset']}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Current State:**
                        - Cipher: {row['ssl_cipher']}
                        - Vulnerable: {row['quantum_years_vulnerable']} years
                        - Threat: {row['quantum_threat_algorithm']}'s Algorithm
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Migration Plan:**
                        - KEM: {row['PQC_Migration']}
                        - Signature: {row['PQC_Signature']}
                        - Timeline: {row['PQC_Timeline']}
                        - Priority: {row['PQC_Priority']}
                        """)
    
    # TAB 4: Analytics & Insights
    with tab4:
        st.subheader("📊 Quantum Threat Analytics & Insights")
        
        # Risk distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Risk Score Distribution")
            risk_bins = pd.cut(df['Risk_Score'], bins=[0, 40, 60, 80, 100], labels=['Low', 'Moderate', 'High', 'Critical'])
            risk_dist = risk_bins.value_counts()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(risk_dist.index),
                    y=list(risk_dist.values),
                    marker=dict(color=['#4ecdc4', '#ffa500', '#ff9800', '#ff6b6b']),
                    text=list(risk_dist.values),
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                xaxis_title="Risk Level",
                yaxis_title="Number of Assets",
                template="plotly_dark",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🌍 Geographic Distribution")
            geo_dist = df['country'].value_counts().head(10)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(geo_dist.values),
                    y=list(geo_dist.index),
                    orientation='h',
                    marker=dict(
                        color=list(geo_dist.values),
                        colorscale='Viridis'
                    ),
                    text=list(geo_dist.values),
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                xaxis_title="Number of Assets",
                yaxis_title="Country",
                template="plotly_dark",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Quantum vulnerability timeline
        st.markdown("---")
        st.markdown("### ⏰ Quantum Threat Progression Analysis")
        
        # Calculate assets vulnerable by year
        vulnerability_by_year = {}
        current_year = datetime.now().year
        
        for year in range(current_year, 2040):
            vulnerable_count = len(df[df['quantum_years_vulnerable'] <= (year - current_year)])
            vulnerability_by_year[year] = vulnerable_count
        
        years = list(vulnerability_by_year.keys())
        vulnerable_assets = list(vulnerability_by_year.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years,
            y=vulnerable_assets,
            mode='lines+markers',
            name='Vulnerable Assets',
            fill='tozeroy',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8)
        ))
        
        # Add critical year markers
        fig.add_vline(x=2030, line_dash="dash", line_color="#ffa500", 
                      annotation_text="CRQC Expected", annotation_position="top")
        
        fig.update_layout(
            title="Asset Vulnerability Projection Over Time",
            xaxis_title="Year",
            yaxis_title="Cumulative Vulnerable Assets",
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.markdown("---")
        st.markdown("### 💡 Key Insights & Recommendations")
        
        insights = []
        
        # Insight 1: Immediate threats
        immediate_threats = len(df[df['quantum_years_vulnerable'] <= 3])
        if immediate_threats > 0:
            insights.append(f"🚨 **URGENT:** {immediate_threats} assets will be vulnerable to quantum attacks within 3 years")
        
        # Insight 2: Harvest threat
        harvest_count = len(df[df['harvest_now_threat'] == True])
        if harvest_count > 0:
            insights.append(f"🎯 **HARVEST THREAT:** {harvest_count} assets contain long-lived data vulnerable to 'Harvest Now, Decrypt Later' attacks")
        
        # Insight 3: Non-quantum-safe
        non_quantum_safe = len(df[df['quantum_safe_crypto'] == False])
        insights.append(f"⚛️ **PQC MIGRATION:** {non_quantum_safe} assets require post-quantum cryptography implementation")
        
        # Insight 4: Geographic concentration
        top_country = df['country'].value_counts().index[0]
        top_country_count = df['country'].value_counts().values[0]
        insights.append(f"🌍 **GEOGRAPHIC RISK:** {top_country_count} assets concentrated in {top_country}")
        
        # Insight 5: Average risk
        if avg_risk >= 70:
            insights.append(f"📊 **HIGH RISK ENVIRONMENT:** Average risk score of {avg_risk:.1f}/100 indicates immediate action required")
        
        for insight in insights:
            st.warning(insight)
    
    # TAB 5: Export & Reporting
    with tab5:
        st.subheader("📥 Export & Reporting Center")
        
        st.markdown("""
        Generate comprehensive reports for stakeholders, compliance teams, and technical staff.
        All exports include quantum threat intelligence and PQC migration roadmaps.
        """)
        
        col1, col2, col3 = st.columns(3)
        
        # PDF Report
        with col1:
            st.markdown("### 📄 Executive PDF Report")
            st.markdown("""
            **Includes:**
            - Executive summary
            - Quantum threat timeline
            - Asset intelligence matrix
            - PQC migration roadmap
            - Risk prioritization
            - NIS2 compliance status
            """)
            
            pdf_bytes = generate_pdf_report(df, target)
            
            st.download_button(
                "📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"Sentinel_V_Quantum_Audit_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        
        # CSV Export
        with col2:
            st.markdown("### 📊 Technical CSV Data")
            st.markdown("""
            **Includes:**
            - All asset details
            - Quantum risk metrics
            - PQC recommendations
            - Timeline data
            - SIEM-compatible format
            """)
            
            csv = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "📥 Download CSV Data",
                data=csv,
                file_name=f"Sentinel_V_Data_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # JSON Export
        with col3:
            st.markdown("### 🔗 API JSON Format")
            st.markdown("""
            **Includes:**
            - Structured JSON
            - API-compatible
            - Automation-ready
            - Complete metadata
            - Quantum intelligence
            """)
            
            json_data = df.to_json(orient='records', indent=2)
            
            st.download_button(
                "📥 Download JSON Data",
                data=json_data,
                file_name=f"Sentinel_V_API_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Custom report builder
        st.markdown("---")
        st.markdown("### 🛠️ Custom Report Builder")
        
        with st.expander("Build Custom Report", expanded=False):
            report_name = st.text_input("Report Name", value=f"Custom_Report_{target}")
            
            include_options = st.multiselect(
                "Include Sections",
                ["Executive Summary", "Quantum Threat Timeline", "Asset Details", 
                 "Risk Analysis", "PQC Roadmap", "Geographic Distribution", "Recommendations"],
                default=["Executive Summary", "Asset Details", "PQC Roadmap"]
            )
            
            filter_by_risk = st.multiselect(
                "Filter by Risk Level",
                ["Critical (HNDL)", "High - Quantum Vulnerable", "Moderate", "Low"],
                default=[]
            )
            
            if st.button("Generate Custom Report", use_container_width=True):
                filtered_df = df if not filter_by_risk else df[df['Quantum_Risk'].isin(filter_by_risk)]
                st.success(f"Custom report '{report_name}' generated with {len(filtered_df)} assets!")
                st.dataframe(filtered_df, use_container_width=True)

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

st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem; margin-top: 20px;'>
    Built with ⚛️ by the Sentinel-V Team | Quantum Intelligence Engine v2.0<br>
    Protecting Today's Data from Tomorrow's Threats
</div>
""", unsafe_allow_html=True)