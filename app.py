"""
Sentinel-V: Quantum AI Nerve Center
🔥 ULTIMATE EDITION - Custom Mode Buttons, Shor's Algorithm, ISMS Framework
Built by SORAA for Thokio
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
import numpy as np
import json
import time
from fpdf import FPDF

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
# 🔥 ULTIMATE CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    /* === DARK QUANTUM THEME === */
    .main {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* === QUANTUM TITLE === */
    .quantum-title {
        background: linear-gradient(135deg, #00f5d4 0%, #7b2cbf 50%, #f72585 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 3.5rem;
        text-shadow: 0 0 30px rgba(123, 44, 191, 0.5);
        animation: quantum-pulse 3s infinite;
    }
    
    @keyframes quantum-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* === MODE BUTTONS - EACH UNIQUE === */
    
    /* Standard Recon - Cyber Green */
    .mode-standard {
        background: linear-gradient(135deg, #00f5d4 0%, #00bbf9 100%) !important;
        color: #000 !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 30px rgba(0, 245, 212, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .mode-standard:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 50px rgba(0, 245, 212, 0.8) !important;
    }
    
    /* Deep Quantum - Purple Quantum */
    .mode-quantum {
        background: linear-gradient(135deg, #7b2cbf 0%, #9d4edd 50%, #c77dff 100%) !important;
        color: #fff !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 30px rgba(123, 44, 191, 0.5) !important;
        animation: quantum-glow 2s infinite !important;
    }
    
    /* Stealth Mode - Dark Red */
    .mode-stealth {
        background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 50%, #0d0d0d 100%) !important;
        color: #ff4444 !important;
        border: 2px solid #ff4444 !important;
        padding: 1rem 2rem !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 20px rgba(255, 68, 68, 0.3) !important;
    }
    .mode-stealth:hover {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%) !important;
        color: #fff !important;
    }
    
    /* Comprehensive - Gold Premium */
    .mode-comprehensive {
        background: linear-gradient(135deg, #f9a825 0%, #ff8f00 50%, #e65100 100%) !important;
        color: #000 !important;
        border: none !important;
        padding: 1rem 2rem !important;
        border-radius: 15px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 0 30px rgba(249, 168, 37, 0.5) !important;
    }
    
    @keyframes quantum-glow {
        0%, 100% { box-shadow: 0 0 30px rgba(123, 44, 191, 0.5); }
        50% { box-shadow: 0 0 60px rgba(157, 78, 221, 0.8); }
    }
    
    /* === METRIC CARDS === */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(123, 44, 191, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: rgba(123, 44, 191, 0.8);
        transform: translateY(-5px);
    }
    
    /* === JARVIS TERMINAL === */
    .jarvis-terminal {
        background: #0a0a0a;
        border: 1px solid #00ff00;
        border-radius: 10px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        max-height: 200px;
        overflow-y: auto;
    }
    
    .jarvis-line {
        margin: 0.3rem 0;
        font-size: 0.85rem;
    }
    
    .jarvis-prompt {
        color: #00ffff;
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(123, 44, 191, 0.1);
        border-radius: 10px;
        padding: 12px 24px;
        border: 1px solid rgba(123, 44, 191, 0.3);
        color: #fff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7b2cbf 0%, #9d4edd 100%);
        border-color: #c77dff;
    }
    
    /* === SHOR'S ALGORITHM VISUAL === */
    .shor-container {
        background: linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #7b2cbf;
        margin: 1rem 0;
    }
    
    /* === SCAN PROGRESS === */
    .scan-progress {
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid #7b2cbf;
        margin: 1rem 0;
    }
    
    /* === HIDE STREAMLIT DEFAULTS === */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* === CUSTOM SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    ::-webkit-scrollbar-thumb {
        background: #7b2cbf;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if 'audit_data' not in st.session_state:
    st.session_state.audit_data = None
if 'scan_history' not in st.session_state:
    st.session_state.scan_history = []
if 'current_scan_mode' not in st.session_state:
    st.session_state.current_scan_mode = "Deep Quantum Analysis"
if 'jarvis_log' not in st.session_state:
    st.session_state.jarvis_log = []
if 'current_target' not in st.session_state:
    st.session_state.current_target = ""
if 'scan_complete' not in st.session_state:
    st.session_state.scan_complete = False

# ============================================================================
# JARVIS SYSTEM
# ============================================================================

def jarvis_log(message: str, level: str = "INFO"):
    """Add message to JARVIS terminal"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "INFO": "#00ff00",
        "WARN": "#ffff00",
        "ERROR": "#ff4444",
        "QUANTUM": "#c77dff",
        "SUCCESS": "#00f5d4",
        "STEALTH": "#ff4444"
    }
    color = colors.get(level, "#00ff00")
    st.session_state.jarvis_log.append({
        "time": timestamp,
        "message": message,
        "level": level,
        "color": color
    })
    # Keep last 20 messages
    if len(st.session_state.jarvis_log) > 20:
        st.session_state.jarvis_log = st.session_state.jarvis_log[-20:]

def render_jarvis_terminal():
    """Render JARVIS terminal with logs"""
    terminal_html = "<div class='jarvis-terminal'>"
    terminal_html += "<div class='jarvis-line'><span style='color: #00ffff;'>JARVIS v2.0</span> | Quantum Intelligence System</div>"
    terminal_html += "<div class='jarvis-line'>─────────────────────────────────</div>"
    
    for log in st.session_state.jarvis_log[-8:]:
        terminal_html += f"<div class='jarvis-line'><span style='color: #888;'>[{log['time']}]</span> <span style='color: {log['color']};'>[{log['level']}]</span> {log['message']}</div>"
    
    if not st.session_state.jarvis_log:
        terminal_html += "<div class='jarvis-line'><span class='jarvis-prompt'>></span> Awaiting commands...</div>"
    
    terminal_html += "</div>"
    return terminal_html

# ============================================================================
# SHOR'S ALGORITHM VISUALIZATION
# ============================================================================

def render_shors_algorithm_analysis(df: pd.DataFrame):
    """Render Shor's Algorithm threat analysis with visualization"""
    
    st.markdown("### ⚛️ Shor's Algorithm Threat Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Quantum threat progression
        years = list(range(2024, 2036))
        
        # RSA-2048 vulnerability curve
        rsa_2048_threat = [5, 10, 20, 35, 55, 75, 90, 95, 98, 99, 100, 100]
        
        # ECC-256 vulnerability curve (breaks faster)
        ecc_256_threat = [8, 15, 30, 50, 70, 85, 95, 98, 99, 100, 100, 100]
        
        # AES-256 (Grover - quadratic speedup only)
        aes_256_threat = [1, 2, 3, 5, 8, 12, 18, 25, 35, 45, 55, 65]
        
        fig = go.Figure()
        
        # RSA-2048
        fig.add_trace(go.Scatter(
            x=years, y=rsa_2048_threat,
            mode='lines+markers',
            name='RSA-2048 (Shor)',
            line=dict(color='#ff4444', width=3),
            marker=dict(size=8),
            fill='tonexty',
            fillcolor='rgba(255, 68, 68, 0.1)'
        ))
        
        # ECC-256
        fig.add_trace(go.Scatter(
            x=years, y=ecc_256_threat,
            mode='lines+markers',
            name='ECC-256 (Shor)',
            line=dict(color='#ff8c00', width=3),
            marker=dict(size=8)
        ))
        
        # AES-256
        fig.add_trace(go.Scatter(
            x=years, y=aes_256_threat,
            mode='lines+markers',
            name='AES-256 (Grover)',
            line=dict(color='#00f5d4', width=3, dash='dash'),
            marker=dict(size=8)
        ))
        
        # CRQC line
        fig.add_vline(x=2030, line_dash="dash", line_color="#c77dff",
                      annotation_text="CRQC Expected", annotation_position="top")
        
        fig.update_layout(
            title="Quantum Algorithm Threat Progression",
            xaxis_title="Year",
            yaxis_title="Vulnerability (%)",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            legend=dict(x=0.02, y=0.98),
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🧬 Shor's Algorithm")
        st.markdown("""
        **How it breaks RSA/ECC:**
        
        1. **Quantum Superposition**
           - Evaluates all values simultaneously
        
        2. **Period Finding**
           - Uses QFT to find period of f(x) = aˣ mod N
        
        3. **Factor Extraction**
           - GCD reveals prime factors
        
        **Complexity:**
        - Classical: O(e^(n^⅓))
        - Quantum: O(n³)
        
        **Time to break RSA-2048:**
        - Classical: ~300 trillion years
        - Quantum: ~8 hours (with 4000 qubits)
        """)
        
        # Threat countdown
        current_year = datetime.now().year
        years_left = 2030 - current_year
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%); 
                    padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;'>
            <h2 style='margin: 0; color: white;'>⏰ {years_left} YEARS</h2>
            <p style='margin: 0; color: rgba(255,255,255,0.8);'>Until CRQC threatens RSA-2048</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ISMS FRAMEWORK PDF GENERATOR
# ============================================================================

def generate_isms_framework_pdf(df: pd.DataFrame, target: str, scan_mode: str) -> bytes:
    """Generate comprehensive ISMS Framework PDF"""
    pdf = FPDF()
    
    # Cover Page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 32)
    pdf.set_text_color(123, 44, 191)
    pdf.ln(50)
    pdf.cell(0, 20, txt="ISMS FRAMEWORK", ln=True, align='C')
    pdf.cell(0, 20, txt="REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(20)
    pdf.cell(0, 10, txt=f"Target: {target}", ln=True, align='C')
    pdf.cell(0, 10, txt=f"Mode: {scan_mode}", ln=True, align='C')
    pdf.cell(0, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(30)
    pdf.cell(0, 10, txt="Sentinel-V Quantum Security Platform", ln=True, align='C')
    pdf.cell(0, 10, txt="ProSec Networks", ln=True, align='C')
    
    # Calculate stats
    total = len(df)
    critical = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    high = len(df[df['Quantum_Risk'].str.contains('High', na=False)])
    qv = len(df[df['quantum_years_vulnerable'] <= 5]) if 'quantum_years_vulnerable' in df.columns else 0
    
    # Executive Summary
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 15, txt="EXECUTIVE SUMMARY", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 11)
    
    summary = f"""
Assessment completed using {scan_mode}.

KEY FINDINGS:
- Total Assets Scanned: {total}
- Critical Risk: {critical}
- High Risk: {high}
- Quantum Vulnerable (5yr): {qv}

RECOMMENDATION:
Immediate migration to Post-Quantum Cryptography (PQC) is required for {critical + high} high-priority assets. 
Implementation of NIST FIPS 203 (ML-KEM) and FIPS 204 (ML-DSA) standards recommended.
    """
    pdf.multi_cell(0, 6, txt=summary)
    
    # ISO 27001
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, txt="ISO 27001 STATEMENT OF APPLICABILITY", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    iso_controls = [
        ("A.5 Security Policies", "P0", "Define quantum-aware policies"),
        ("A.8 Asset Management", "P0", f"{total} assets discovered"),
        ("A.10 Cryptography", "P0", f"CRITICAL: {qv} need PQC migration"),
        ("A.12 Operations Security", "P1", "Quantum threat monitoring"),
        ("A.13 Communications", "P0", "Deploy quantum-safe TLS"),
        ("A.16 Incident Management", "P0", "Quantum incident procedures"),
        ("A.18 Compliance", "P0", "NIS2 quantum requirements"),
    ]
    
    for ctrl, pri, desc in iso_controls:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, txt=f"{ctrl} [{pri}]", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"   {desc}", ln=True)
    
    # BSI IT-Grundschutz
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, txt="BSI IT-GRUNDSCHUTZ BAUSTEINE", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    bsi = [
        ("ISMS.1 Sicherheitsmanagement", "Quantum-aware ISMS"),
        ("CON.1 Kryptokonzept", "PQC: ML-KEM, ML-DSA, SLH-DSA"),
        ("DER.1 Detektion", "HNDL attack monitoring"),
        ("NET.3.3 VPN", "Quantum-safe VPN deployment"),
    ]
    
    for b, desc in bsi:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, txt=b, ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"   {desc}", ln=True)
    
    # NIS2
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, txt="NIS2 ARTICLE 21 COMPLIANCE", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    pdf.cell(0, 8, txt=f"Critical Gaps: {critical}", ln=True)
    pdf.ln(5)
    
    nis2 = [
        ("Art 21(2)(a) Risk Analysis", "REQUIRED", "Include quantum threats"),
        ("Art 21(2)(d) Supply Chain", "REQUIRED", "Supplier PQC assessment"),
        ("Art 21(2)(h) Cryptography", "CRITICAL", f"{qv} assets need PQC"),
    ]
    
    for req, status, gap in nis2:
        pdf.set_font("Arial", 'B', 10)
        marker = "[!]" if status == "CRITICAL" else "[*]"
        pdf.cell(0, 7, txt=f"{marker} {req} - {status}", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, txt=f"   Gap: {gap}", ln=True)
    
    # PQC Roadmap
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, txt="PQC MIGRATION ROADMAP", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    phases = [
        ("Phase 1 (0-3mo)", f"Migrate {critical} critical assets to ML-KEM-1024"),
        ("Phase 2 (3-6mo)", "Deploy ML-DSA signatures, hybrid TLS"),
        ("Phase 3 (6-12mo)", f"Complete {high} high-priority migrations"),
        ("Phase 4 (12-24mo)", "Full PQC adoption, decommission legacy"),
    ]
    
    for phase, action in phases:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, txt=phase, ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 6, txt=f"   {action}", ln=True)
    
    # Budget
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="BUDGET ESTIMATE", ln=True)
    pdf.set_font("Arial", '', 10)
    
    budget = 150000 + (total * 3000)
    roi = ((4200000 - budget) / budget) * 100
    
    pdf.cell(0, 6, txt=f"Total Investment: EUR {budget:,}", ln=True)
    pdf.cell(0, 6, txt=f"Breach Prevention Value: EUR 4,200,000", ln=True)
    pdf.cell(0, 6, txt=f"ROI: {roi:.0f}%", ln=True)
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 5, txt="Sentinel-V | ProSec Networks | Quantum-Ready Security", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# ============================================================================
# MODE CONFIGURATIONS WITH UNIQUE IDENTITIES
# ============================================================================

MODE_CONFIGS = {
    "Standard Recon": {
        "icon": "🔍",
        "color": "#00f5d4",
        "gradient": "linear-gradient(135deg, #00f5d4 0%, #00bbf9 100%)",
        "tagline": "Fast Attack Surface Mapping",
        "description": "Lightning-fast reconnaissance for quick threat overview",
        "features": [
            "⚡ 10 assets max (speed optimized)",
            "🔍 Common subdomain enumeration",
            "🌍 IP geolocation",
            "🔒 Basic SSL analysis",
            "❌ No quantum analysis",
            "❌ No PQC recommendations"
        ],
        "best_for": "Quick scans, initial recon, time-sensitive assessments"
    },
    "Deep Quantum Analysis": {
        "icon": "⚛️",
        "color": "#9d4edd",
        "gradient": "linear-gradient(135deg, #7b2cbf 0%, #9d4edd 50%, #c77dff 100%)",
        "tagline": "Quantum Threat Intelligence",
        "description": "Full quantum vulnerability assessment with Shor's algorithm analysis",
        "features": [
            "⚛️ 25 assets (balanced)",
            "📜 Certificate transparency logs",
            "🧬 Shor's algorithm threat modeling",
            "🔮 HNDL attack risk assessment",
            "💎 ML-KEM/ML-DSA recommendations",
            "📊 Quantum timeline projections"
        ],
        "best_for": "Security assessments, quantum readiness evaluation"
    },
    "Stealth Mode": {
        "icon": "🥷",
        "color": "#ff4444",
        "gradient": "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
        "tagline": "Ghost Protocol Active",
        "description": "Low-profile scanning with evasion techniques",
        "features": [
            "🥷 15 assets (covert)",
            "⏱️ 2-second request delays",
            "🚫 No active probing",
            "👻 Passive OSINT only",
            "⚛️ Quantum analysis included",
            "🎯 Paranoid risk scoring (+10%)"
        ],
        "best_for": "Red team ops, avoiding IDS/IPS, sensitive targets"
    },
    "Comprehensive Audit": {
        "icon": "📋",
        "color": "#f9a825",
        "gradient": "linear-gradient(135deg, #f9a825 0%, #ff8f00 50%, #e65100 100%)",
        "tagline": "Enterprise Compliance Suite",
        "description": "Full security audit with ISMS framework generation",
        "features": [
            "📋 50 assets maximum",
            "🔍 Extended subdomain list",
            "⚛️ Complete quantum analysis",
            "📜 ISO 27001 SoA generation",
            "🇩🇪 BSI IT-Grundschutz mapping",
            "🇪🇺 NIS2 Article 21 compliance",
            "💰 Budget & ROI analysis"
        ],
        "best_for": "Compliance audits, board presentations, certifications"
    }
}

# ============================================================================
# HEADER
# ============================================================================

st.markdown("<h1 class='quantum-title'>⚛️ SENTINEL-V</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #c77dff; font-size: 1.3rem; margin-top: -10px;'>QUANTUM AI NERVE CENTER</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1rem;'>Next-Generation Agentic Defense | Post-Quantum Cryptography Intelligence</p>", unsafe_allow_html=True)

# Status Row
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: rgba(0,245,212,0.1); border-radius: 10px; border: 1px solid #00f5d4;'>
        <p style='margin: 0; color: #888; font-size: 0.8rem;'>SYSTEM STATUS</p>
        <h3 style='margin: 0; color: #00f5d4;'>ONLINE</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: rgba(157,78,221,0.1); border-radius: 10px; border: 1px solid #9d4edd;'>
        <p style='margin: 0; color: #888; font-size: 0.8rem;'>QUANTUM MODE</p>
        <h3 style='margin: 0; color: #9d4edd;'>ACTIVE</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    years_left = 2030 - datetime.now().year
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: rgba(255,68,68,0.1); border-radius: 10px; border: 1px solid #ff4444;'>
        <p style='margin: 0; color: #888; font-size: 0.8rem;'>CRQC THREAT</p>
        <h3 style='margin: 0; color: #ff4444;'>{years_left} YEARS</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: rgba(249,168,37,0.1); border-radius: 10px; border: 1px solid #f9a825;'>
        <p style='margin: 0; color: #888; font-size: 0.8rem;'>NIST PQC</p>
        <h3 style='margin: 0; color: #f9a825;'>COMPLIANT</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# SIDEBAR - JARVIS COMMAND CENTER
# ============================================================================

with st.sidebar:
    st.markdown("## ⚡ JARVIS")
    st.markdown("<p style='color: #888; margin-top: -10px;'>Quantum Command Interface</p>", unsafe_allow_html=True)
    
    # Target Input
    st.markdown("### 🎯 Target")
    target = st.text_input("Domain", value="", placeholder="example.com", label_visibility="collapsed")
    
    st.markdown("---")
    
    # Mode Selection with Visual Cards
    st.markdown("### 🔧 Operation Mode")
    
    scan_mode = st.radio(
        "Select mode",
        list(MODE_CONFIGS.keys()),
        index=1,
        label_visibility="collapsed"
    )
    
    # Display selected mode info
    mode = MODE_CONFIGS[scan_mode]
    st.markdown(f"""
    <div style='background: {mode["gradient"]}; padding: 1rem; border-radius: 10px; margin: 1rem 0;'>
        <h3 style='margin: 0; color: {"#000" if scan_mode in ["Standard Recon", "Comprehensive Audit"] else "#fff"};'>{mode["icon"]} {scan_mode}</h3>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.85rem; color: {"#333" if scan_mode in ["Standard Recon", "Comprehensive Audit"] else "rgba(255,255,255,0.9)"};'>{mode["tagline"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Mode Features"):
        for feature in mode["features"]:
            st.markdown(f"<span style='font-size: 0.9rem;'>{feature}</span>", unsafe_allow_html=True)
        st.caption(f"**Best for:** {mode['best_for']}")
    
    st.markdown("---")
    
    # Launch Button
    if st.button(f"{mode['icon']} INITIALIZE {scan_mode.upper()}", use_container_width=True, type="primary"):
        if not target or len(target) < 4:
            st.error("⚠️ Enter a valid domain")
        else:
            st.session_state.current_scan_mode = scan_mode
            st.session_state.current_target = target
            st.session_state.jarvis_log = []
            
            jarvis_log(f"Mode: {scan_mode}", "INFO")
            jarvis_log(f"Target: {target}", "INFO")
            
            progress = st.progress(0)
            status = st.empty()
            
            try:
                # Mode-specific initialization messages
                if scan_mode == "Standard Recon":
                    jarvis_log("Fast scan initiated", "INFO")
                    status.info("🔍 Quick reconnaissance...")
                elif scan_mode == "Deep Quantum Analysis":
                    jarvis_log("Quantum analyzers online", "QUANTUM")
                    status.info("⚛️ Initializing quantum threat analysis...")
                elif scan_mode == "Stealth Mode":
                    jarvis_log("Ghost protocol engaged", "STEALTH")
                    status.warning("🥷 Stealth mode - expect delays...")
                else:
                    jarvis_log("Full audit suite loading", "INFO")
                    status.info("📋 Comprehensive audit initializing...")
                
                progress.progress(15)
                time.sleep(0.5)
                
                config = ScanMode.get_config(scan_mode)
                jarvis_log(f"Max assets: {config['max_assets']}", "INFO")
                progress.progress(25)
                
                if config['use_crt_sh']:
                    jarvis_log("Querying crt.sh...", "INFO")
                else:
                    jarvis_log("Passive recon only", "INFO" if scan_mode != "Stealth Mode" else "STEALTH")
                
                progress.progress(40)
                status.info("🌐 Resolving assets...")
                
                # Run scan
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                if config['enable_quantum']:
                    jarvis_log("Shor's algorithm analysis...", "QUANTUM")
                    progress.progress(60)
                
                df = loop.run_until_complete(run_audit(target, scan_mode))
                
                progress.progress(85)
                
                if scan_mode == "Comprehensive Audit":
                    jarvis_log("Generating ISMS framework...", "INFO")
                
                progress.progress(100)
                
                st.session_state.audit_data = df
                st.session_state.scan_complete = True
                
                jarvis_log(f"Complete: {len(df)} assets", "SUCCESS")
                
                st.session_state.scan_history.append({
                    'domain': target,
                    'mode': scan_mode,
                    'assets': len(df),
                    'time': datetime.now().strftime("%H:%M:%S")
                })
                
                status.empty()
                progress.empty()
                
                st.success(f"✅ {len(df)} assets discovered")
                loop.close()
                st.rerun()
                
            except Exception as e:
                jarvis_log(f"Error: {str(e)[:50]}", "ERROR")
                st.error(f"❌ {e}")
    
    st.markdown("---")
    
    # JARVIS Terminal
    st.markdown("### 🖥️ Terminal")
    st.markdown(render_jarvis_terminal(), unsafe_allow_html=True)
    
    # Quick Actions
    if st.session_state.audit_data is not None:
        st.markdown("---")
        if st.button("🔄 New Scan", use_container_width=True):
            st.session_state.audit_data = None
            st.session_state.jarvis_log = []
            st.rerun()

# ============================================================================
# MAIN CONTENT
# ============================================================================

if st.session_state.audit_data is None:
    # Welcome Screen
    st.markdown("## 🎯 Select a Mode & Enter Target")
    
    # Mode Cards
    cols = st.columns(4)
    
    for idx, (mode_name, mode_info) in enumerate(MODE_CONFIGS.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style='background: {mode_info["gradient"]}; padding: 1.5rem; border-radius: 15px; 
                        height: 280px; display: flex; flex-direction: column; justify-content: space-between;'>
                <div>
                    <h2 style='margin: 0; font-size: 2.5rem;'>{mode_info["icon"]}</h2>
                    <h4 style='margin: 0.5rem 0; color: {"#000" if mode_name in ["Standard Recon", "Comprehensive Audit"] else "#fff"};'>{mode_name}</h4>
                    <p style='font-size: 0.85rem; color: {"#333" if mode_name in ["Standard Recon", "Comprehensive Audit"] else "rgba(255,255,255,0.8)"};'>{mode_info["tagline"]}</p>
                </div>
                <p style='font-size: 0.75rem; color: {"#555" if mode_name in ["Standard Recon", "Comprehensive Audit"] else "rgba(255,255,255,0.6)"}; margin: 0;'>{mode_info["best_for"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quantum Timeline Preview
    st.markdown("### ⏰ Quantum Threat Timeline")
    
    years = [2024, 2026, 2028, 2030, 2032, 2035]
    threat = [15, 35, 60, 80, 95, 100]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=threat,
        mode='lines+markers+text',
        text=['NISQ', 'Early FT', 'Transition', 'CRQC', 'Advanced', 'Universal'],
        textposition='top center',
        line=dict(color='#9d4edd', width=4),
        marker=dict(size=12, color='#c77dff'),
        fill='tozeroy',
        fillcolor='rgba(157, 78, 221, 0.2)'
    ))
    
    fig.add_vline(x=2030, line_dash="dash", line_color="#ff4444",
                  annotation_text="RSA-2048 VULNERABLE", annotation_position="top")
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        xaxis_title="Year",
        yaxis_title="Threat Level (%)",
        font=dict(color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:
    # Results Display
    df = st.session_state.audit_data
    mode = st.session_state.current_scan_mode
    target = st.session_state.current_target
    
    # Mode Badge
    mode_info = MODE_CONFIGS[mode]
    st.markdown(f"""
    <div style='display: inline-block; background: {mode_info["gradient"]}; padding: 0.5rem 1.5rem; 
                border-radius: 25px; margin-bottom: 1rem;'>
        <span style='color: {"#000" if mode in ["Standard Recon", "Comprehensive Audit"] else "#fff"}; font-weight: bold;'>
            {mode_info["icon"]} {mode} | {target}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total = len(df)
    critical = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    high = len(df[df['Quantum_Risk'].str.contains('High', na=False)])
    qv = len(df[df['quantum_years_vulnerable'] <= 5]) if 'quantum_years_vulnerable' in df.columns and df['quantum_years_vulnerable'].iloc[0] != 0 else 0
    avg_risk = df['Risk_Score'].mean()
    
    with col1:
        st.metric("🎯 Assets", total)
    with col2:
        st.metric("🔴 Critical", critical)
    with col3:
        st.metric("🟠 High", high)
    with col4:
        st.metric("⚛️ Quantum Vuln", qv if mode != "Standard Recon" else "N/A")
    with col5:
        st.metric("📊 Avg Risk", f"{avg_risk:.0f}")
    
    st.markdown("---")
    
    # Tabs
    if mode == "Comprehensive Audit":
        tabs = st.tabs(["📊 Intelligence", "⚛️ Shor's Analysis", "🗺️ Global Map", "📋 ISMS Framework", "📥 Export"])
    elif mode in ["Deep Quantum Analysis", "Stealth Mode"]:
        tabs = st.tabs(["📊 Intelligence", "⚛️ Shor's Analysis", "🗺️ Global Map", "📥 Export"])
    else:
        tabs = st.tabs(["📊 Intelligence", "🗺️ Global Map", "📥 Export"])
    
    tab_idx = 0
    
    # Intelligence Tab
    with tabs[tab_idx]:
        st.markdown("### 📊 Threat Intelligence Matrix")
        
        display_cols = ['asset', 'ip', 'country', 'criticality', 'Quantum_Risk', 'Risk_Score']
        if mode != "Standard Recon":
            display_cols += ['quantum_years_vulnerable', 'PQC_Migration', 'PQC_Priority']
        display_cols.append('scan_mode')
        
        st.dataframe(df[display_cols], use_container_width=True, height=400)
    
    tab_idx += 1
    
    # Shor's Analysis Tab (quantum modes only)
    if mode in ["Deep Quantum Analysis", "Stealth Mode", "Comprehensive Audit"]:
        with tabs[tab_idx]:
            render_shors_algorithm_analysis(df)
        tab_idx += 1
    
    # Map Tab
    with tabs[tab_idx]:
        st.markdown("### 🗺️ Global Threat Radar")
        
        m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
        
        for _, row in df.iterrows():
            if row['lat'] != 0.0 and row['lon'] != 0.0:
                color = 'red' if 'Critical' in str(row['Quantum_Risk']) else 'orange' if 'High' in str(row['Quantum_Risk']) else 'blue'
                
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=8,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    popup=f"<b>{row['asset']}</b><br>Risk: {row['Quantum_Risk']}<br>Score: {row['Risk_Score']}"
                ).add_to(m)
        
        st_folium(m, width=1200, height=450)
    
    tab_idx += 1
    
    # ISMS Framework Tab (Comprehensive only)
    if mode == "Comprehensive Audit":
        with tabs[tab_idx]:
            st.markdown("### 📋 ISMS Framework Generator")
            st.markdown("Generate compliance documentation for ISO 27001, BSI IT-Grundschutz, and NIS2.")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div style='background: rgba(0,245,212,0.1); padding: 1rem; border-radius: 10px; border: 1px solid #00f5d4;'>
                    <h4 style='color: #00f5d4;'>📜 ISO 27001</h4>
                    <p style='font-size: 0.85rem;'>Statement of Applicability with quantum controls</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style='background: rgba(157,78,221,0.1); padding: 1rem; border-radius: 10px; border: 1px solid #9d4edd;'>
                    <h4 style='color: #9d4edd;'>🇩🇪 BSI Grundschutz</h4>
                    <p style='font-size: 0.85rem;'>Bausteine mapping with PQC requirements</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='background: rgba(249,168,37,0.1); padding: 1rem; border-radius: 10px; border: 1px solid #f9a825;'>
                    <h4 style='color: #f9a825;'>🇪🇺 NIS2 Compliance</h4>
                    <p style='font-size: 0.85rem;'>Article 21 gap analysis & remediation</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Generate ISMS PDF
            isms_pdf = generate_isms_framework_pdf(df, target, mode)
            
            st.download_button(
                "📥 DOWNLOAD ISMS FRAMEWORK (PDF)",
                data=isms_pdf,
                file_name=f"ISMS_Framework_{target}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        
        tab_idx += 1
    
    # Export Tab
    with tabs[tab_idx]:
        st.markdown("### 📥 Export Reports")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 📄 PDF Report")
            pdf = generate_pdf_report(df, target, mode)
            st.download_button(
                "Download PDF",
                data=pdf,
                file_name=f"Sentinel_V_{target}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### 📊 CSV Data")
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download CSV",
                data=csv,
                file_name=f"Sentinel_V_{target}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            st.markdown("#### 🔗 JSON API")
            json_data = df.to_json(orient='records', indent=2)
            st.download_button(
                "Download JSON",
                data=json_data,
                file_name=f"Sentinel_V_{target}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # ISMS download for Comprehensive mode
        if mode == "Comprehensive Audit":
            st.markdown("---")
            st.markdown("#### 📋 ISMS Framework")
            isms_pdf = generate_isms_framework_pdf(df, target, mode)
            st.download_button(
                "Download ISMS Framework (PDF)",
                data=isms_pdf,
                file_name=f"ISMS_Framework_{target}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <p style='color: #9d4edd; font-weight: bold;'>SENTINEL-V | Quantum AI Nerve Center</p>
    <p style='color: #666; font-size: 0.85rem;'>ProSec Networks | NIST PQC Compliant | Built by SORAA for Thokio</p>
</div>
""", unsafe_allow_html=True)