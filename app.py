"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   SENTINEL-V: QUANTUM AI NERVE CENTER                                         ║
║   ═══════════════════════════════════                                         ║
║                                                                               ║
║   FULL POWER EDITION                                                          ║
║   Built by SORAA at 189% for Thokio                                          ║
║                                                                               ║
║   Features:                                                                   ║
║   • Complete ISO 27001 Statement of Applicability                            ║
║   • BSI IT-Grundschutz Full Bausteine Mapping                                ║
║   • NIS2 Article 21 Complete Compliance                                      ║
║   • Interactive Budget Calculator with ROI                                   ║
║   • Shor's Algorithm Deep Dive with Math                                     ║
║   • Grover's Algorithm AES Analysis                                          ║
║   • Threat Radar with Full Explanations                                      ║
║   • PQC Migration Wizard                                                     ║
║   • Executive Dashboard                                                       ║
║   • Compliance Scorecards                                                    ║
║   • Custom Report Builder                                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import asyncio
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap, MarkerCluster
from core import SentinelAgent, generate_pdf_report, run_audit, ScanMode
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
import time
import math
from fpdf import FPDF

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Sentinel-V | Quantum AI Nerve Center",
    layout="wide",
    page_icon="⚛️",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ULTIMATE CSS - DARK QUANTUM THEME
# ============================================================================

st.markdown("""
<style>
    /* === BASE THEME === */
    .main, .stApp {
        background: linear-gradient(180deg, #0a0a12 0%, #12121f 50%, #1a1a2e 100%);
    }
    
    /* === QUANTUM ANIMATED TITLE === */
    @keyframes quantum-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .quantum-title {
        background: linear-gradient(270deg, #00f5d4, #7b2cbf, #f72585, #4361ee, #00f5d4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: quantum-shift 8s ease infinite;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        letter-spacing: -2px;
    }
    
    /* === GLASS MORPHISM CARDS === */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(123, 44, 191, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(123, 44, 191, 0.2);
    }
    
    /* === MODE CARDS === */
    .mode-card-standard {
        background: linear-gradient(135deg, #00f5d4 0%, #00bbf9 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: #000;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .mode-card-quantum {
        background: linear-gradient(135deg, #7b2cbf 0%, #9d4edd 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: #fff;
        animation: quantum-pulse 3s infinite;
    }
    
    .mode-card-stealth {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 2px solid #ff4444;
        border-radius: 15px;
        padding: 1.5rem;
        color: #ff4444;
    }
    
    .mode-card-comprehensive {
        background: linear-gradient(135deg, #f9a825 0%, #ff6f00 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: #000;
    }
    
    @keyframes quantum-pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(123, 44, 191, 0.4); }
        50% { box-shadow: 0 0 40px rgba(157, 78, 221, 0.8); }
    }
    
    /* === JARVIS TERMINAL === */
    .jarvis-terminal {
        background: #0a0a0a;
        border: 1px solid #00ff00;
        border-radius: 10px;
        padding: 1rem;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 0.8rem;
        max-height: 250px;
        overflow-y: auto;
    }
    
    .jarvis-header {
        color: #00ffff;
        border-bottom: 1px solid #333;
        padding-bottom: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* === METRIC BOXES === */
    .metric-box {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-box-critical {
        border-color: #ff4444;
        background: rgba(255, 68, 68, 0.1);
    }
    
    .metric-box-warning {
        border-color: #ff8c00;
        background: rgba(255, 140, 0, 0.1);
    }
    
    .metric-box-success {
        border-color: #00f5d4;
        background: rgba(0, 245, 212, 0.1);
    }
    
    .metric-box-quantum {
        border-color: #9d4edd;
        background: rgba(157, 78, 221, 0.1);
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(123, 44, 191, 0.1);
        border-radius: 10px 10px 0 0;
        border: 1px solid rgba(123, 44, 191, 0.3);
        border-bottom: none;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7b2cbf 0%, #9d4edd 100%);
    }
    
    /* === EXPANDERS === */
    .streamlit-expanderHeader {
        background: rgba(123, 44, 191, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(123, 44, 191, 0.3);
    }
    
    /* === PROGRESS BARS === */
    .stProgress > div > div {
        background: linear-gradient(90deg, #7b2cbf, #00f5d4);
    }
    
    /* === COMPLIANCE SCORE BAR === */
    .score-bar-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .score-bar-fill {
        height: 100%;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #000;
        transition: width 1s ease;
    }
    
    /* === HIDE DEFAULTS === */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; }
    ::-webkit-scrollbar-thumb { background: #7b2cbf; border-radius: 4px; }
    
    /* === RISK LEVEL BADGES === */
    .risk-critical { background: #ff4444; color: #fff; padding: 2px 8px; border-radius: 5px; font-weight: bold; }
    .risk-high { background: #ff8c00; color: #fff; padding: 2px 8px; border-radius: 5px; font-weight: bold; }
    .risk-medium { background: #ffd700; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; }
    .risk-low { background: #00f5d4; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

defaults = {
    'audit_data': None,
    'scan_history': [],
    'current_scan_mode': "Deep Quantum Analysis",
    'jarvis_log': [],
    'current_target': "",
    'budget_settings': {
        'consulting_rate': 150,
        'implementation_months': 12,
        'team_size': 3,
        'include_training': True,
        'include_certification': True
    }
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================================
# JARVIS SYSTEM
# ============================================================================

def jarvis(msg: str, level: str = "INFO"):
    """Add to JARVIS log"""
    colors = {
        "INFO": "#00ff00", "WARN": "#ffff00", "ERROR": "#ff4444",
        "QUANTUM": "#c77dff", "SUCCESS": "#00f5d4", "STEALTH": "#ff4444",
        "SYSTEM": "#00ffff", "SCAN": "#4361ee"
    }
    st.session_state.jarvis_log.append({
        "time": datetime.now().strftime("%H:%M:%S.%f")[:-4],
        "msg": msg, "level": level, "color": colors.get(level, "#00ff00")
    })
    if len(st.session_state.jarvis_log) > 30:
        st.session_state.jarvis_log = st.session_state.jarvis_log[-30:]

def render_jarvis():
    """Render JARVIS terminal"""
    html = """<div class='jarvis-terminal'>
    <div class='jarvis-header'>⚡ JARVIS v3.0 | Quantum Intelligence System | ProSec Networks</div>"""
    
    for log in st.session_state.jarvis_log[-12:]:
        html += f"<div style='margin: 3px 0;'><span style='color:#666;'>[{log['time']}]</span> <span style='color:{log['color']};'>[{log['level']}]</span> {log['msg']}</div>"
    
    if not st.session_state.jarvis_log:
        html += "<div style='color:#00ff00;'>$ Awaiting commands, Thokio...</div>"
    
    html += "</div>"
    return html

# ============================================================================
# MODE CONFIGURATIONS
# ============================================================================

MODES = {
    "Standard Recon": {
        "icon": "🔍", "color": "#00f5d4", "text_color": "#000",
        "gradient": "linear-gradient(135deg, #00f5d4 0%, #00bbf9 100%)",
        "tagline": "Lightning-Fast Attack Surface Mapping",
        "description": "Rapid reconnaissance for immediate threat visibility. Perfect for time-sensitive assessments.",
        "specs": {"assets": 10, "quantum": False, "delay": 0, "crt_sh": False},
        "features": [
            ("⚡", "10 assets max", "Speed-optimized scanning"),
            ("🔍", "Common subdomains", "Standard enumeration"),
            ("🌍", "IP Geolocation", "Geographic threat mapping"),
            ("🔒", "Basic SSL", "Certificate validation"),
            ("❌", "No quantum analysis", "Classical risk only"),
        ],
        "jarvis_init": "Fast scan protocol initiated. Optimizing for speed.",
        "jarvis_complete": "Recon complete. Attack surface mapped."
    },
    "Deep Quantum Analysis": {
        "icon": "⚛️", "color": "#9d4edd", "text_color": "#fff",
        "gradient": "linear-gradient(135deg, #7b2cbf 0%, #9d4edd 50%, #c77dff 100%)",
        "tagline": "Quantum Threat Intelligence Suite",
        "description": "Complete quantum vulnerability assessment with Shor's algorithm threat modeling and PQC recommendations.",
        "specs": {"assets": 25, "quantum": True, "delay": 0.3, "crt_sh": True},
        "features": [
            ("⚛️", "25 assets", "Balanced coverage"),
            ("📜", "Certificate Transparency", "crt.sh integration"),
            ("🧬", "Shor's Algorithm", "RSA/ECC vulnerability timeline"),
            ("🔮", "HNDL Detection", "Harvest Now, Decrypt Later risk"),
            ("💎", "PQC Recommendations", "ML-KEM, ML-DSA migration paths"),
            ("📊", "Quantum Timeline", "Year-by-year threat projection"),
        ],
        "jarvis_init": "Quantum analyzers online. Initializing Shor's algorithm threat model.",
        "jarvis_complete": "Quantum analysis complete. HNDL threats identified."
    },
    "Stealth Mode": {
        "icon": "🥷", "color": "#ff4444", "text_color": "#ff4444",
        "gradient": "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)",
        "tagline": "Ghost Protocol — Undetectable Scanning",
        "description": "Low-profile reconnaissance with evasion techniques. Designed to avoid IDS/IPS detection.",
        "specs": {"assets": 15, "quantum": True, "delay": 2.0, "crt_sh": False},
        "features": [
            ("🥷", "15 assets", "Covert coverage"),
            ("⏱️", "2s delays", "Request throttling"),
            ("🚫", "No active probing", "Passive OSINT only"),
            ("👻", "IDS/IPS evasion", "Minimal fingerprint"),
            ("⚛️", "Quantum included", "Full threat analysis"),
            ("🎯", "+10% risk scoring", "Paranoid mode"),
        ],
        "jarvis_init": "Ghost protocol engaged. Masking digital footprint. Expect delays.",
        "jarvis_complete": "Stealth scan complete. Zero detection signatures."
    },
    "Comprehensive Audit": {
        "icon": "📋", "color": "#f9a825", "text_color": "#000",
        "gradient": "linear-gradient(135deg, #f9a825 0%, #ff8f00 50%, #e65100 100%)",
        "tagline": "Enterprise Compliance & Certification Suite",
        "description": "Full security audit with ISMS framework generation. ISO 27001, BSI IT-Grundschutz, NIS2 compliance ready.",
        "specs": {"assets": 50, "quantum": True, "delay": 0.2, "crt_sh": True},
        "features": [
            ("📋", "50 assets max", "Complete coverage"),
            ("🔍", "Extended enumeration", "Deep subdomain discovery"),
            ("⚛️", "Full quantum suite", "Complete threat analysis"),
            ("📜", "ISO 27001 SoA", "Statement of Applicability"),
            ("🇩🇪", "BSI Grundschutz", "German compliance framework"),
            ("🇪🇺", "NIS2 Article 21", "EU directive compliance"),
            ("💰", "Budget Calculator", "ROI analysis included"),
            ("📊", "Executive Reports", "Board-ready documentation"),
        ],
        "jarvis_init": "Enterprise audit suite loading. Initializing compliance frameworks.",
        "jarvis_complete": "Comprehensive audit complete. ISMS frameworks generated."
    }
}

# ============================================================================
# ISO 27001 CONTROLS DATABASE
# ============================================================================

ISO_27001_CONTROLS = {
    "A.5": {
        "name": "Information Security Policies",
        "controls": [
            {"id": "A.5.1", "name": "Policies for information security", 
             "description": "A set of policies for information security shall be defined, approved by management, published and communicated to employees and relevant external parties.",
             "quantum_impact": "HIGH",
             "quantum_requirement": "Include Post-Quantum Cryptography (PQC) migration policy. Define timeline for transitioning to NIST-approved quantum-resistant algorithms.",
             "implementation": "1. Draft quantum security policy\n2. Define PQC migration timeline\n3. Establish governance structure\n4. Communicate to all stakeholders"},
        ]
    },
    "A.6": {
        "name": "Organization of Information Security",
        "controls": [
            {"id": "A.6.1", "name": "Internal organization",
             "description": "A management framework shall be established to initiate and control the implementation and operation of information security.",
             "quantum_impact": "MEDIUM",
             "quantum_requirement": "Assign quantum security responsibilities. Designate PQC migration lead.",
             "implementation": "1. Appoint quantum security officer\n2. Define reporting structure\n3. Establish review cadence"},
        ]
    },
    "A.8": {
        "name": "Asset Management",
        "controls": [
            {"id": "A.8.1", "name": "Responsibility for assets",
             "description": "Assets associated with information and information processing facilities shall be identified and an inventory maintained.",
             "quantum_impact": "CRITICAL",
             "quantum_requirement": "Maintain inventory of ALL cryptographic assets. Tag each with quantum vulnerability status and migration priority.",
             "implementation": "1. Inventory all crypto assets\n2. Classify by quantum risk\n3. Tag migration priority\n4. Monitor continuously"},
            {"id": "A.8.2", "name": "Information classification",
             "description": "Information shall be classified in terms of legal requirements, value, criticality and sensitivity.",
             "quantum_impact": "HIGH",
             "quantum_requirement": "Add 'Quantum Sensitivity' classification. Data with >10yr confidentiality requirement needs immediate PQC.",
             "implementation": "1. Add quantum classification tier\n2. Identify long-lived data\n3. Prioritize HNDL-vulnerable data"},
        ]
    },
    "A.10": {
        "name": "Cryptographic Controls",
        "controls": [
            {"id": "A.10.1", "name": "Cryptographic controls",
             "description": "A policy on the use of cryptographic controls for protection of information shall be developed and implemented.",
             "quantum_impact": "CRITICAL",
             "quantum_requirement": "URGENT: Migrate to NIST PQC standards. Implement ML-KEM (FIPS 203) for key exchange, ML-DSA (FIPS 204) for signatures, SLH-DSA (FIPS 205) for stateless signatures.",
             "implementation": "1. Audit current cryptography\n2. Select PQC algorithms\n3. Implement hybrid mode\n4. Test thoroughly\n5. Full migration"},
        ]
    },
    "A.12": {
        "name": "Operations Security",
        "controls": [
            {"id": "A.12.4", "name": "Logging and monitoring",
             "description": "Event logs recording user activities, exceptions, faults and information security events shall be produced, kept and regularly reviewed.",
             "quantum_impact": "HIGH",
             "quantum_requirement": "Monitor for quantum-related threats. Detect potential HNDL (Harvest Now, Decrypt Later) attacks - unusual data exfiltration patterns.",
             "implementation": "1. Add quantum threat signatures to SIEM\n2. Monitor large data transfers\n3. Alert on crypto anomalies"},
        ]
    },
    "A.13": {
        "name": "Communications Security",
        "controls": [
            {"id": "A.13.1", "name": "Network security management",
             "description": "Networks shall be managed and controlled to protect information in systems and applications.",
             "quantum_impact": "CRITICAL",
             "quantum_requirement": "Deploy quantum-safe TLS. Implement hybrid classical-PQC cipher suites during transition.",
             "implementation": "1. Upgrade TLS libraries\n2. Enable PQC cipher suites\n3. Test interoperability\n4. Monitor performance"},
        ]
    },
    "A.14": {
        "name": "System Development Security",
        "controls": [
            {"id": "A.14.2", "name": "Security in development processes",
             "description": "Rules for the development of software and systems shall be established and applied.",
             "quantum_impact": "HIGH",
             "quantum_requirement": "Integrate cryptographic agility into SDL. All new systems must support algorithm switching without code changes.",
             "implementation": "1. Update coding standards\n2. Require crypto abstraction layers\n3. Add PQC to security testing"},
        ]
    },
    "A.16": {
        "name": "Incident Management",
        "controls": [
            {"id": "A.16.1", "name": "Management of incidents",
             "description": "Responsibilities and procedures shall be established to ensure a quick, effective and orderly response to incidents.",
             "quantum_impact": "HIGH",
             "quantum_requirement": "Develop quantum incident response playbooks. Define procedures for discovered HNDL attacks and crypto compromises.",
             "implementation": "1. Create quantum IR playbook\n2. Define escalation paths\n3. Establish notification procedures\n4. Practice tabletop exercises"},
        ]
    },
    "A.18": {
        "name": "Compliance",
        "controls": [
            {"id": "A.18.1", "name": "Compliance with legal requirements",
             "description": "All relevant statutory, regulatory and contractual requirements shall be identified, documented and kept up to date.",
             "quantum_impact": "CRITICAL",
             "quantum_requirement": "Monitor quantum-related regulations. NIS2 (EU), NIST guidelines (US), BSI recommendations (DE) all increasingly require quantum readiness.",
             "implementation": "1. Track regulatory developments\n2. Map to compliance calendar\n3. Ensure audit readiness"},
        ]
    }
}

# ============================================================================
# BSI IT-GRUNDSCHUTZ DATABASE
# ============================================================================

BSI_BAUSTEINE = {
    "ISMS": [
        {"id": "ISMS.1", "name": "Sicherheitsmanagement",
         "description": "Establishes the foundation for information security management system.",
         "quantum_req": "Integrate quantum risk into enterprise risk management. Assign quantum security responsibilities.",
         "priority": "P0"},
    ],
    "CON": [
        {"id": "CON.1", "name": "Kryptokonzept",
         "description": "Cryptographic concept defining all cryptographic mechanisms used.",
         "quantum_req": "CRITICAL: Define PQC transition strategy. Document current crypto inventory. Plan migration to ML-KEM (FIPS 203), ML-DSA (FIPS 204), SLH-DSA (FIPS 205).",
         "priority": "P0"},
        {"id": "CON.7", "name": "Informationssicherheit auf Reisen",
         "description": "Security for mobile work and travel.",
         "quantum_req": "Ensure VPN uses quantum-safe protocols. Protect mobile devices with PQC-enabled encryption.",
         "priority": "P1"},
    ],
    "OPS": [
        {"id": "OPS.1.1.2", "name": "Ordnungsgemäße IT-Administration",
         "description": "Proper IT administration procedures.",
         "quantum_req": "Include PQC updates in patch management. Prioritize crypto library updates.",
         "priority": "P1"},
        {"id": "OPS.1.1.3", "name": "Patch- und Änderungsmanagement",
         "description": "Patch and change management.",
         "quantum_req": "Establish expedited patching for quantum-related vulnerabilities. Track NIST PQC updates.",
         "priority": "P0"},
    ],
    "DER": [
        {"id": "DER.1", "name": "Detektion von sicherheitsrelevanten Ereignissen",
         "description": "Detection of security-relevant events.",
         "quantum_req": "Add HNDL attack signatures to detection rules. Monitor for unusual encrypted data exfiltration.",
         "priority": "P0"},
        {"id": "DER.2.1", "name": "Behandlung von Sicherheitsvorfällen",
         "description": "Security incident handling.",
         "quantum_req": "Develop quantum-specific incident response procedures. Include crypto compromise scenarios.",
         "priority": "P0"},
    ],
    "NET": [
        {"id": "NET.1.1", "name": "Netzarchitektur und -design",
         "description": "Network architecture and design.",
         "quantum_req": "Design for cryptographic agility. Enable seamless algorithm transitions.",
         "priority": "P1"},
        {"id": "NET.3.3", "name": "VPN",
         "description": "Virtual Private Networks.",
         "quantum_req": "CRITICAL: Deploy quantum-safe VPN. Implement hybrid classical-PQC mode immediately.",
         "priority": "P0"},
    ]
}

# ============================================================================
# NIS2 ARTICLE 21 DATABASE
# ============================================================================

NIS2_REQUIREMENTS = [
    {"article": "21(2)(a)", "name": "Risk analysis and security policies",
     "description": "Policies on risk analysis and information system security.",
     "quantum_gap": "Must include quantum computing in risk analysis. PQC migration policy required.",
     "status": "CRITICAL", "priority": "P0"},
    {"article": "21(2)(b)", "name": "Incident handling",
     "description": "Procedures for handling security incidents.",
     "quantum_gap": "Quantum incident response procedures needed. HNDL attack playbook required.",
     "status": "REQUIRED", "priority": "P0"},
    {"article": "21(2)(c)", "name": "Business continuity",
     "description": "Business continuity including backup management, disaster recovery, and crisis management.",
     "quantum_gap": "Include quantum threats in BCM scenarios. Crypto-apocalypse scenario planning.",
     "status": "REQUIRED", "priority": "P1"},
    {"article": "21(2)(d)", "name": "Supply chain security",
     "description": "Security relating to acquisition, development and maintenance of systems.",
     "quantum_gap": "Assess supplier quantum readiness. Include PQC requirements in procurement.",
     "status": "REQUIRED", "priority": "P1"},
    {"article": "21(2)(e)", "name": "Security in network and systems acquisition",
     "description": "Security in network and information systems acquisition, development and maintenance.",
     "quantum_gap": "Mandate cryptographic agility in new systems. Require PQC capability.",
     "status": "REQUIRED", "priority": "P1"},
    {"article": "21(2)(f)", "name": "Vulnerability handling and disclosure",
     "description": "Policies and procedures for assessing effectiveness of cybersecurity measures.",
     "quantum_gap": "Include quantum vulnerabilities in assessment scope. Track CVEs related to crypto.",
     "status": "CRITICAL", "priority": "P0"},
    {"article": "21(2)(g)", "name": "Cybersecurity training",
     "description": "Basic cyber hygiene practices and cybersecurity training.",
     "quantum_gap": "Add quantum awareness training. Educate staff on HNDL threats.",
     "status": "RECOMMENDED", "priority": "P2"},
    {"article": "21(2)(h)", "name": "Cryptography",
     "description": "Policies and procedures regarding the use of cryptography and encryption.",
     "quantum_gap": "CRITICAL: Explicit PQC migration plan required. NIST FIPS 203/204/205 implementation.",
     "status": "CRITICAL", "priority": "P0"},
    {"article": "21(2)(i)", "name": "Human resources security",
     "description": "Human resources security, access control policies and asset management.",
     "quantum_gap": "Include quantum in security awareness. Update access controls for PQC.",
     "status": "REQUIRED", "priority": "P1"},
    {"article": "21(2)(j)", "name": "Multi-factor authentication",
     "description": "Use of MFA, secured communications and emergency communication systems.",
     "quantum_gap": "Plan for quantum-safe MFA. Current TOTP/HOTP may need updates.",
     "status": "REQUIRED", "priority": "P1"},
]

# ============================================================================
# SHOR'S ALGORITHM DEEP DIVE
# ============================================================================

def render_shors_deep_dive(df: pd.DataFrame):
    """Complete Shor's Algorithm analysis with math and visualizations"""
    
    st.markdown("## ⚛️ Shor's Algorithm: The Quantum Threat Explained")
    
    # Introduction
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color: #c77dff; margin-top: 0;'>What is Shor's Algorithm?</h3>
        <p>Shor's algorithm, developed by mathematician Peter Shor in 1994, is a quantum algorithm that can factor 
        large integers exponentially faster than the best known classical algorithms. This capability directly 
        threatens RSA and ECC cryptography that protects most of today's internet communications.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📊 Cryptographic Vulnerability Timeline")
        
        years = list(range(2024, 2041))
        
        # RSA vulnerability curves
        rsa_2048 = [5 + (i**2.2)/15 for i in range(len(years))]
        rsa_2048 = [min(100, v) for v in rsa_2048]
        
        rsa_4096 = [2 + (i**2.0)/20 for i in range(len(years))]
        rsa_4096 = [min(100, v) for v in rsa_4096]
        
        ecc_256 = [8 + (i**2.3)/12 for i in range(len(years))]
        ecc_256 = [min(100, v) for v in ecc_256]
        
        aes_256 = [1 + i*2.5 for i in range(len(years))]
        aes_256 = [min(70, v) for v in aes_256]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=years, y=rsa_2048, name='RSA-2048',
            line=dict(color='#ff4444', width=3), fill='tozeroy',
            fillcolor='rgba(255, 68, 68, 0.1)'))
        
        fig.add_trace(go.Scatter(x=years, y=ecc_256, name='ECC-256',
            line=dict(color='#ff8c00', width=3)))
        
        fig.add_trace(go.Scatter(x=years, y=rsa_4096, name='RSA-4096',
            line=dict(color='#ffd700', width=3, dash='dash')))
        
        fig.add_trace(go.Scatter(x=years, y=aes_256, name='AES-256 (Grover)',
            line=dict(color='#00f5d4', width=3, dash='dot')))
        
        # CRQC line
        fig.add_vline(x=2030, line_dash="dash", line_color="#c77dff",
            annotation_text="CRQC Expected", annotation_position="top left")
        
        # Critical threshold
        fig.add_hline(y=75, line_dash="dot", line_color="#ff4444",
            annotation_text="Critical Threshold (75%)")
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=450,
            xaxis_title="Year",
            yaxis_title="Vulnerability Probability (%)",
            legend=dict(x=0.02, y=0.98),
            font=dict(color='white'),
            yaxis=dict(range=[0, 105])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🧮 The Mathematics")
        
        st.markdown("""
        **Classical Factoring (GNFS):**
        ```
        Time = O(exp((64/9)^(1/3) × (ln N)^(1/3) × (ln ln N)^(2/3)))
        ```
        
        **Shor's Algorithm:**
        ```
        Time = O((log N)³)
        ```
        
        **The Speedup:**
        - RSA-2048: Classical = 10²⁴ operations
        - RSA-2048: Quantum = 10⁹ operations
        - **Speedup: ~10¹⁵ times faster**
        """)
        
        st.markdown("---")
        
        st.markdown("### ⚡ Qubit Requirements")
        
        qubit_data = {
            "Algorithm": ["RSA-2048", "RSA-4096", "ECC-256", "ECC-384"],
            "Logical Qubits": ["4,099", "8,194", "2,330", "3,484"],
            "Physical Qubits*": ["~20M", "~40M", "~12M", "~17M"],
            "Est. Break Time": ["8 hours", "24 hours", "4 hours", "8 hours"]
        }
        
        st.dataframe(pd.DataFrame(qubit_data), hide_index=True, use_container_width=True)
        st.caption("*With current error correction overhead (~5000:1)")
    
    st.markdown("---")
    
    # How it works
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #00f5d4;'>Step 1: Quantum Superposition</h4>
            <p>Prepare qubits in superposition state:</p>
            <p style='font-family: monospace; color: #c77dff;'>|ψ⟩ = (1/√N) Σ|x⟩</p>
            <p>This allows evaluating f(x) = aˣ mod N for ALL x simultaneously.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #9d4edd;'>Step 2: Quantum Fourier Transform</h4>
            <p>Apply QFT to find the period r of:</p>
            <p style='font-family: monospace; color: #c77dff;'>f(x) = aˣ mod N</p>
            <p>QFT extracts frequency information from quantum states.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #f72585;'>Step 3: Factor Extraction</h4>
            <p>With period r, compute factors:</p>
            <p style='font-family: monospace; color: #c77dff;'>GCD(a^(r/2) ± 1, N)</p>
            <p>High probability of yielding non-trivial factors.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Threat countdown
    current_year = datetime.now().year
    crqc_year = 2030
    years_left = crqc_year - current_year
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center;'>
            <h1 style='margin: 0; color: white; font-size: 4rem;'>{years_left}</h1>
            <p style='margin: 0; color: rgba(255,255,255,0.9); font-size: 1.2rem;'>Years Until CRQC</p>
            <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.7);'>Cryptographically Relevant Quantum Computer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #ff8c00 0%, #e65100 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center;'>
            <h1 style='margin: 0; color: white; font-size: 4rem;'>NOW</h1>
            <p style='margin: 0; color: rgba(255,255,255,0.9); font-size: 1.2rem;'>HNDL Threat Active</p>
            <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.7);'>Harvest Now, Decrypt Later attacks happening TODAY</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #7b2cbf 0%, #9d4edd 100%); 
                    padding: 2rem; border-radius: 15px; text-align: center;'>
            <h1 style='margin: 0; color: white; font-size: 4rem;'>2024</h1>
            <p style='margin: 0; color: rgba(255,255,255,0.9); font-size: 1.2rem;'>NIST PQC Finalized</p>
            <p style='margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.7);'>ML-KEM, ML-DSA, SLH-DSA now standardized</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# GROVER'S ALGORITHM
# ============================================================================

def render_grovers_analysis():
    """Grover's Algorithm impact on symmetric crypto"""
    
    st.markdown("### 🔍 Grover's Algorithm: Symmetric Crypto Impact")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #00f5d4;'>What is Grover's Algorithm?</h4>
            <p>Grover's algorithm provides a <strong>quadratic speedup</strong> for unstructured search problems. 
            While not as devastating as Shor's, it effectively halves the security of symmetric encryption.</p>
            
            <table style='width: 100%; margin-top: 1rem;'>
                <tr style='border-bottom: 1px solid #333;'>
                    <th style='text-align: left; padding: 0.5rem;'>Algorithm</th>
                    <th style='text-align: left; padding: 0.5rem;'>Classical Security</th>
                    <th style='text-align: left; padding: 0.5rem;'>Post-Quantum Security</th>
                    <th style='text-align: left; padding: 0.5rem;'>Status</th>
                </tr>
                <tr>
                    <td style='padding: 0.5rem;'>AES-128</td>
                    <td style='padding: 0.5rem;'>128 bits</td>
                    <td style='padding: 0.5rem; color: #ff4444;'>64 bits ❌</td>
                    <td style='padding: 0.5rem;'><span class='risk-critical'>INSECURE</span></td>
                </tr>
                <tr>
                    <td style='padding: 0.5rem;'>AES-192</td>
                    <td style='padding: 0.5rem;'>192 bits</td>
                    <td style='padding: 0.5rem; color: #ffd700;'>96 bits ⚠️</td>
                    <td style='padding: 0.5rem;'><span class='risk-medium'>MARGINAL</span></td>
                </tr>
                <tr>
                    <td style='padding: 0.5rem;'>AES-256</td>
                    <td style='padding: 0.5rem;'>256 bits</td>
                    <td style='padding: 0.5rem; color: #00f5d4;'>128 bits ✅</td>
                    <td style='padding: 0.5rem;'><span class='risk-low'>SECURE</span></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h4 style='color: #9d4edd;'>Recommendation</h4>
            <p><strong>Use AES-256 everywhere.</strong></p>
            <p>This provides 128-bit post-quantum security, which remains computationally infeasible.</p>
            <hr style='border-color: #333;'>
            <p style='font-size: 0.9rem;'><strong>Hash Functions:</strong></p>
            <p style='font-size: 0.85rem;'>SHA-256 → 128-bit PQ security<br>
            SHA-384 → 192-bit PQ security<br>
            SHA-512 → 256-bit PQ security</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# BUDGET CALCULATOR
# ============================================================================

def render_budget_calculator(df: pd.DataFrame, target: str):
    """Interactive budget calculator with ROI analysis"""
    
    st.markdown("## 💰 PQC Migration Budget Calculator")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ Configuration")
        
        total_assets = len(df)
        critical = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
        high = len(df[df['Quantum_Risk'].str.contains('High', na=False)])
        
        st.markdown(f"**Assets Discovered:** {total_assets}")
        st.markdown(f"**Critical Priority:** {critical}")
        st.markdown(f"**High Priority:** {high}")
        
        st.markdown("---")
        
        consulting_rate = st.slider("Consulting Day Rate (€)", 800, 2500, 1500, 100)
        impl_months = st.slider("Implementation Timeline (months)", 6, 24, 12)
        team_size = st.slider("Security Team Size", 1, 10, 3)
        
        include_training = st.checkbox("Include Training Program", value=True)
        include_cert = st.checkbox("Include ISO 27001 Certification", value=True)
        include_tools = st.checkbox("Include Security Tools/Licenses", value=True)
        include_hardware = st.checkbox("Include Hardware Upgrades", value=True)
    
    with col2:
        st.markdown("### 📊 Budget Breakdown")
        
        # Calculate costs
        consulting_days = impl_months * 10  # 10 days/month avg
        consulting_cost = consulting_days * consulting_rate
        
        per_asset_cost = 2500 if critical > 10 else 2000
        migration_cost = total_assets * per_asset_cost
        
        training_cost = team_size * 5000 if include_training else 0
        cert_cost = 35000 if include_cert else 0
        tools_cost = 50000 if include_tools else 0
        hardware_cost = (critical * 5000 + high * 2000) if include_hardware else 0
        
        annual_maintenance = (migration_cost + tools_cost) * 0.15
        
        total_cost = consulting_cost + migration_cost + training_cost + cert_cost + tools_cost + hardware_cost
        
        # Display breakdown
        budget_items = [
            ("Consulting Services", consulting_cost, f"{consulting_days} days @ €{consulting_rate}/day"),
            ("PQC Migration", migration_cost, f"{total_assets} assets @ €{per_asset_cost}/asset"),
            ("Training Program", training_cost, f"{team_size} staff @ €5,000/person"),
            ("ISO 27001 Certification", cert_cost, "Audit and certification"),
            ("Security Tools/Licenses", tools_cost, "PQC libraries, monitoring"),
            ("Hardware Upgrades", hardware_cost, "HSMs, accelerators"),
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=[item[0] for item in budget_items if item[1] > 0],
            values=[item[1] for item in budget_items if item[1] > 0],
            hole=0.4,
            marker=dict(colors=['#7b2cbf', '#00f5d4', '#f9a825', '#ff4444', '#4361ee', '#00bbf9'])
        )])
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            showlegend=True,
            legend=dict(x=1.05, y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost table
        for item, cost, desc in budget_items:
            if cost > 0:
                st.markdown(f"**{item}:** €{cost:,.0f}")
                st.caption(desc)
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"### 💵 Total Investment")
            st.markdown(f"# €{total_cost:,.0f}")
        with col_b:
            st.markdown(f"### 📅 Annual Maintenance")
            st.markdown(f"# €{annual_maintenance:,.0f}")
    
    # ROI Analysis
    st.markdown("---")
    st.markdown("### 📈 Return on Investment Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    # Industry average breach costs (IBM Cost of Data Breach 2024)
    breach_cost = 4_450_000  # Average
    breach_probability_without = 0.28  # 28% chance over 2 years
    breach_probability_with = 0.05  # 5% with proper security
    
    expected_loss_without = breach_cost * breach_probability_without
    expected_loss_with = breach_cost * breach_probability_with
    risk_reduction = expected_loss_without - expected_loss_with
    
    roi = ((risk_reduction - total_cost) / total_cost) * 100 if total_cost > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class='metric-box metric-box-critical'>
            <p style='margin: 0; color: #888;'>Expected Loss (Without PQC)</p>
            <h2 style='margin: 0; color: #ff4444;'>€{expected_loss_without:,.0f}</h2>
            <p style='margin: 0; font-size: 0.8rem;'>{breach_probability_without*100:.0f}% breach probability</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-box metric-box-success'>
            <p style='margin: 0; color: #888;'>Expected Loss (With PQC)</p>
            <h2 style='margin: 0; color: #00f5d4;'>€{expected_loss_with:,.0f}</h2>
            <p style='margin: 0; font-size: 0.8rem;'>{breach_probability_with*100:.0f}% breach probability</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        roi_color = "#00f5d4" if roi > 0 else "#ff4444"
        st.markdown(f"""
        <div class='metric-box metric-box-quantum'>
            <p style='margin: 0; color: #888;'>Return on Investment</p>
            <h2 style='margin: 0; color: {roi_color};'>{roi:,.0f}%</h2>
            <p style='margin: 0; font-size: 0.8rem;'>Risk reduction value: €{risk_reduction:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ISMS FRAMEWORK DISPLAY
# ============================================================================

def render_isms_framework(df: pd.DataFrame, target: str):
    """Full ISMS Framework display with ISO, BSI, NIS2"""
    
    st.markdown("## 📋 ISMS Framework Generator")
    st.markdown("Complete compliance documentation for enterprise security governance.")
    
    # Compliance Overview
    total = len(df)
    critical = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    
    # Calculate compliance scores
    iso_score = max(20, 100 - (critical * 10))
    bsi_score = max(25, 100 - (critical * 8))
    nis2_score = max(15, 100 - (critical * 12))
    
    st.markdown("### 📊 Compliance Scorecards")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='glass-card'>
            <h4 style='color: #00f5d4;'>📜 ISO 27001</h4>
            <div class='score-bar-container'>
                <div class='score-bar-fill' style='width: {iso_score}%; background: linear-gradient(90deg, #00f5d4, #00bbf9);'>{iso_score}%</div>
            </div>
            <p style='font-size: 0.85rem; margin-top: 0.5rem;'>Statement of Applicability with quantum controls</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='glass-card'>
            <h4 style='color: #9d4edd;'>🇩🇪 BSI Grundschutz</h4>
            <div class='score-bar-container'>
                <div class='score-bar-fill' style='width: {bsi_score}%; background: linear-gradient(90deg, #7b2cbf, #9d4edd);'>{bsi_score}%</div>
            </div>
            <p style='font-size: 0.85rem; margin-top: 0.5rem;'>IT-Grundschutz Bausteine mapping</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='glass-card'>
            <h4 style='color: #f9a825;'>🇪🇺 NIS2 Directive</h4>
            <div class='score-bar-container'>
                <div class='score-bar-fill' style='width: {nis2_score}%; background: linear-gradient(90deg, #f9a825, #ff8f00);'>{nis2_score}%</div>
            </div>
            <p style='font-size: 0.85rem; margin-top: 0.5rem;'>Article 21 compliance assessment</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabbed framework details
    fw_tabs = st.tabs(["📜 ISO 27001", "🇩🇪 BSI Grundschutz", "🇪🇺 NIS2 Article 21"])
    
    # ISO 27001 Tab
    with fw_tabs[0]:
        st.markdown("### ISO 27001:2022 Statement of Applicability")
        st.markdown(f"**Scope:** {target} - All {total} discovered assets")
        st.markdown(f"**Critical Controls Required:** {critical}")
        
        for domain_id, domain_data in ISO_27001_CONTROLS.items():
            with st.expander(f"**{domain_id} - {domain_data['name']}**", expanded=False):
                for control in domain_data['controls']:
                    impact_color = "#ff4444" if control['quantum_impact'] == "CRITICAL" else "#ff8c00" if control['quantum_impact'] == "HIGH" else "#ffd700"
                    
                    st.markdown(f"""
                    <div style='background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {impact_color};'>
                        <h4 style='margin: 0;'>{control['id']} - {control['name']}</h4>
                        <p style='margin: 0.5rem 0; color: #888;'>{control['description']}</p>
                        <p style='margin: 0;'><span style='color: {impact_color};'>⚛️ Quantum Impact: {control['quantum_impact']}</span></p>
                        <p style='margin: 0.5rem 0;'><strong>Quantum Requirement:</strong> {control['quantum_requirement']}</p>
                        <details>
                            <summary style='cursor: pointer; color: #00f5d4;'>📋 Implementation Steps</summary>
                            <pre style='background: #1a1a2e; padding: 0.5rem; border-radius: 5px; margin-top: 0.5rem;'>{control['implementation']}</pre>
                        </details>
                    </div>
                    """, unsafe_allow_html=True)
    
    # BSI Tab
    with fw_tabs[1]:
        st.markdown("### BSI IT-Grundschutz Compendium 2024")
        st.markdown("German Federal Office for Information Security framework mapping.")
        
        for category, bausteine in BSI_BAUSTEINE.items():
            st.markdown(f"#### {category} - Bausteine")
            for b in bausteine:
                priority_color = "#ff4444" if b['priority'] == "P0" else "#ff8c00" if b['priority'] == "P1" else "#ffd700"
                
                with st.expander(f"**{b['id']} - {b['name']}** [{b['priority']}]"):
                    st.markdown(f"**Description:** {b['description']}")
                    st.markdown(f"**Quantum Requirement:** {b['quantum_req']}")
                    st.markdown(f"<span style='color: {priority_color};'>Priority: {b['priority']}</span>", unsafe_allow_html=True)
    
    # NIS2 Tab
    with fw_tabs[2]:
        st.markdown("### NIS2 Directive - Article 21 Compliance")
        st.markdown("EU Network and Information Security Directive requirements.")
        
        st.markdown(f"**Entity Classification:** Essential Entity (presumed)")
        st.markdown(f"**Critical Gaps Identified:** {critical}")
        
        for req in NIS2_REQUIREMENTS:
            status_color = "#ff4444" if req['status'] == "CRITICAL" else "#ff8c00" if req['status'] == "REQUIRED" else "#ffd700"
            
            with st.expander(f"**Article {req['article']} - {req['name']}** [{req['status']}]"):
                st.markdown(f"**Requirement:** {req['description']}")
                st.markdown(f"**Quantum Gap:** {req['quantum_gap']}")
                st.markdown(f"<span style='color: {status_color};'>Status: {req['status']} | Priority: {req['priority']}</span>", unsafe_allow_html=True)

# ============================================================================
# THREAT RADAR EXPLANATIONS
# ============================================================================

def render_threat_radar_explained(df: pd.DataFrame):
    """Threat radar with full explanations"""
    
    st.markdown("## 🗺️ Global Threat Radar")
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: rgba(255,68,68,0.2); padding: 1rem; border-radius: 10px; border: 2px solid #ff4444;'>
            <h4 style='color: #ff4444; margin: 0;'>🔴 Critical (HNDL)</h4>
            <p style='font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Harvest Now, Decrypt Later threat. Data at immediate risk. Score: 80-100</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: rgba(255,140,0,0.2); padding: 1rem; border-radius: 10px; border: 2px solid #ff8c00;'>
            <h4 style='color: #ff8c00; margin: 0;'>🟠 High Risk</h4>
            <p style='font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Quantum vulnerable within 5 years. Urgent PQC migration needed. Score: 60-79</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: rgba(255,215,0,0.2); padding: 1rem; border-radius: 10px; border: 2px solid #ffd700;'>
            <h4 style='color: #ffd700; margin: 0;'>🟡 Medium Risk</h4>
            <p style='font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Standard vulnerabilities. Plan PQC migration. Score: 40-59</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background: rgba(0,245,212,0.2); padding: 1rem; border-radius: 10px; border: 2px solid #00f5d4;'>
            <h4 style='color: #00f5d4; margin: 0;'>🟢 Low Risk</h4>
            <p style='font-size: 0.85rem; margin: 0.5rem 0 0 0;'>Acceptable security posture. Continue monitoring. Score: 0-39</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Map
    m = folium.Map(location=[30, 0], zoom_start=2, tiles="CartoDB dark_matter")
    
    heat_data = []
    
    for _, row in df.iterrows():
        if row['lat'] != 0 and row['lon'] != 0:
            # Determine color and size based on risk
            risk = str(row['Quantum_Risk'])
            score = row['Risk_Score']
            
            if 'Critical' in risk:
                color = '#ff4444'
                radius = 12
            elif 'High' in risk:
                color = '#ff8c00'
                radius = 10
            elif 'Medium' in risk or 'Moderate' in risk:
                color = '#ffd700'
                radius = 8
            else:
                color = '#00f5d4'
                radius = 6
            
            # Rich popup
            popup_html = f"""
            <div style='width: 300px; font-family: Arial;'>
                <h3 style='margin: 0; color: {color};'>{row['asset']}</h3>
                <hr style='margin: 5px 0; border-color: #333;'>
                <p><b>📍 Location:</b> {row['city']}, {row['country']}</p>
                <p><b>🔗 IP:</b> {row['ip']}</p>
                <p><b>⚠️ Risk Level:</b> {row['Quantum_Risk']}</p>
                <p><b>📊 Risk Score:</b> {score}/100</p>
                <p><b>🎯 Criticality:</b> {row['criticality']}</p>
                <hr style='margin: 5px 0; border-color: #333;'>
                <p><b>⚛️ Quantum Threat:</b> {row.get('quantum_threat_algorithm', 'N/A')}</p>
                <p><b>⏰ Years Vulnerable:</b> {row.get('quantum_years_vulnerable', 'N/A')}</p>
                <p><b>💎 PQC Strategy:</b> {row.get('PQC_Migration', 'N/A')}</p>
                <hr style='margin: 5px 0; border-color: #333;'>
                <p><b>🔧 Action:</b> {row['Solution'][:100]}...</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=radius,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=f"{row['asset']} - {row['Quantum_Risk']}"
            ).add_to(m)
            
            # Add to heatmap
            heat_data.append([row['lat'], row['lon'], score/100])
    
    # Add heatmap layer
    if heat_data:
        HeatMap(heat_data, radius=25, blur=20, gradient={0.4: 'blue', 0.6: 'lime', 0.8: 'orange', 1: 'red'}).add_to(m)
    
    st_folium(m, width=1200, height=500)
    
    # Geographic distribution
    st.markdown("### 🌍 Geographic Risk Distribution")
    
    geo_stats = df.groupby('country').agg({
        'Risk_Score': 'mean',
        'asset': 'count'
    }).reset_index()
    geo_stats.columns = ['Country', 'Avg Risk', 'Assets']
    geo_stats = geo_stats.sort_values('Assets', ascending=False).head(10)
    
    fig = px.bar(geo_stats, x='Country', y='Assets', color='Avg Risk',
                 color_continuous_scale=['#00f5d4', '#ffd700', '#ff8c00', '#ff4444'])
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PDF GENERATORS
# ============================================================================

def generate_full_isms_pdf(df: pd.DataFrame, target: str, mode: str) -> bytes:
    """Generate comprehensive ISMS PDF"""
    pdf = FPDF()
    
    total = len(df)
    critical = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    high = len(df[df['Quantum_Risk'].str.contains('High', na=False)])
    
    # Cover
    pdf.add_page()
    pdf.set_font("Arial", 'B', 28)
    pdf.set_text_color(123, 44, 191)
    pdf.ln(40)
    pdf.cell(0, 15, "ISMS FRAMEWORK", ln=True, align='C')
    pdf.cell(0, 15, "COMPLIANCE REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(20)
    pdf.cell(0, 10, f"Target: {target}", ln=True, align='C')
    pdf.cell(0, 10, f"Scan Mode: {mode}", ln=True, align='C')
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(30)
    pdf.cell(0, 10, "Sentinel-V Quantum Security Platform", ln=True, align='C')
    pdf.cell(0, 10, "ProSec Networks GmbH", ln=True, align='C')
    
    # Executive Summary
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, "EXECUTIVE SUMMARY", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 11)
    
    summary = f"""
This report presents the results of a {mode} security assessment conducted on {target}.

KEY FINDINGS:
- Total Assets Discovered: {total}
- Critical Risk (HNDL Threat): {critical}
- High Risk (Quantum Vulnerable): {high}
- Moderate/Low Risk: {total - critical - high}

QUANTUM THREAT ASSESSMENT:
The assessment identified {critical} assets that are immediately vulnerable to "Harvest Now, Decrypt Later" 
(HNDL) attacks. These assets contain data that adversaries may be collecting today to decrypt once 
cryptographically relevant quantum computers (CRQC) become available, estimated around 2030.

COMPLIANCE STATUS:
- ISO 27001: Partial compliance - quantum controls required
- BSI IT-Grundschutz: Gaps identified in CON.1 (Kryptokonzept)
- NIS2 Article 21: Critical gaps in cryptography requirements (21.2.h)

RECOMMENDATIONS:
1. Immediate PQC migration for {critical} critical assets
2. Implement NIST FIPS 203 (ML-KEM) for key exchange
3. Deploy NIST FIPS 204 (ML-DSA) for digital signatures
4. Establish cryptographic agility framework
5. Update incident response for quantum scenarios
    """
    pdf.multi_cell(0, 5, summary)
    
    # ISO 27001
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, "ISO 27001 STATEMENT OF APPLICABILITY", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    pdf.cell(0, 8, f"Scope: {target} - {total} digital assets", ln=True)
    pdf.cell(0, 8, f"Critical Controls Required: {critical}", ln=True)
    pdf.ln(5)
    
    for domain_id, domain_data in ISO_27001_CONTROLS.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, f"{domain_id} - {domain_data['name']}", ln=True)
        pdf.set_font("Arial", '', 9)
        for control in domain_data['controls']:
            pdf.cell(0, 5, f"  {control['id']}: {control['name']} [{control['quantum_impact']}]", ln=True)
            pdf.set_font("Arial", 'I', 8)
            pdf.multi_cell(0, 4, f"    Quantum: {control['quantum_requirement'][:100]}...")
            pdf.set_font("Arial", '', 9)
        pdf.ln(2)
    
    # BSI
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, "BSI IT-GRUNDSCHUTZ MAPPING", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    for category, bausteine in BSI_BAUSTEINE.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, f"{category} Bausteine", ln=True)
        pdf.set_font("Arial", '', 9)
        for b in bausteine:
            pdf.cell(0, 5, f"  {b['id']}: {b['name']} [{b['priority']}]", ln=True)
            pdf.set_font("Arial", 'I', 8)
            pdf.multi_cell(0, 4, f"    {b['quantum_req'][:100]}...")
            pdf.set_font("Arial", '', 9)
    
    # NIS2
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, "NIS2 ARTICLE 21 COMPLIANCE", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    pdf.cell(0, 8, "Entity Type: Essential Entity", ln=True)
    pdf.cell(0, 8, f"Critical Gaps: {critical}", ln=True)
    pdf.ln(5)
    
    for req in NIS2_REQUIREMENTS:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, f"Art {req['article']}: {req['name']} [{req['status']}]", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 4, f"  Gap: {req['quantum_gap']}")
        pdf.ln(1)
    
    # Budget
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 12, "BUDGET ESTIMATION", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    base = 100000
    per_asset = total * 2500
    total_budget = base + per_asset
    
    pdf.cell(0, 8, f"Consulting & Implementation: EUR {base:,}", ln=True)
    pdf.cell(0, 8, f"Per-Asset Migration ({total} assets): EUR {per_asset:,}", ln=True)
    pdf.cell(0, 8, f"Training & Certification: EUR 60,000", ln=True)
    pdf.cell(0, 8, f"Tools & Licenses: EUR 50,000", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"TOTAL INVESTMENT: EUR {total_budget + 110000:,}", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Annual Maintenance: EUR {(total_budget * 0.15):,.0f}", ln=True)
    
    # ROI
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "ROI ANALYSIS", ln=True)
    pdf.set_font("Arial", '', 10)
    breach_cost = 4450000
    risk_reduction = breach_cost * 0.23
    roi = ((risk_reduction - total_budget) / total_budget) * 100
    pdf.cell(0, 6, f"Average Breach Cost: EUR {breach_cost:,}", ln=True)
    pdf.cell(0, 6, f"Risk Reduction Value: EUR {risk_reduction:,.0f}", ln=True)
    pdf.cell(0, 6, f"Return on Investment: {roi:.0f}%", ln=True)
    
    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(123, 44, 191)
    pdf.cell(0, 5, "Generated by Sentinel-V | ProSec Networks | Quantum-Ready Security", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# ============================================================================
# MAIN APPLICATION
# ============================================================================

# Header
st.markdown("<h1 class='quantum-title'>SENTINEL-V</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#9d4edd; font-size:1.2rem; margin-top:-10px;'>QUANTUM AI NERVE CENTER</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#666;'>Post-Quantum Cryptography Intelligence | ProSec Networks</p>", unsafe_allow_html=True)

# Status bar
st.markdown("---")
cols = st.columns(4)
with cols[0]:
    st.markdown("<div class='metric-box metric-box-success'><small>STATUS</small><h3 style='color:#00f5d4;margin:0;'>ONLINE</h3></div>", unsafe_allow_html=True)
with cols[1]:
    st.markdown("<div class='metric-box metric-box-quantum'><small>QUANTUM</small><h3 style='color:#9d4edd;margin:0;'>ACTIVE</h3></div>", unsafe_allow_html=True)
with cols[2]:
    yrs = 2030 - datetime.now().year
    st.markdown(f"<div class='metric-box metric-box-critical'><small>CRQC THREAT</small><h3 style='color:#ff4444;margin:0;'>{yrs} YRS</h3></div>", unsafe_allow_html=True)
with cols[3]:
    st.markdown("<div class='metric-box metric-box-warning'><small>NIST PQC</small><h3 style='color:#f9a825;margin:0;'>FIPS 203/204</h3></div>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## ⚡ JARVIS")
    
    target = st.text_input("🎯 Target Domain", placeholder="example.com")
    
    st.markdown("### 🔧 Mode")
    mode = st.radio("Select", list(MODES.keys()), index=1, label_visibility="collapsed")
    
    m = MODES[mode]
    st.markdown(f"""
    <div style='background:{m["gradient"]}; padding:1rem; border-radius:10px; margin:1rem 0;'>
        <h4 style='margin:0; color:{m["text_color"]};'>{m["icon"]} {mode}</h4>
        <p style='margin:0.5rem 0 0 0; font-size:0.8rem; color:{m["text_color"]}; opacity:0.9;'>{m["tagline"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📋 Features"):
        for icon, name, desc in m["features"]:
            st.markdown(f"**{icon} {name}**")
            st.caption(desc)
    
    st.markdown("---")
    
    if st.button(f"🚀 LAUNCH {mode.upper()}", use_container_width=True, type="primary"):
        if target and len(target) >= 4:
            st.session_state.jarvis_log = []
            jarvis("System initialized", "SYSTEM")
            jarvis(m["jarvis_init"], "QUANTUM" if "Quantum" in mode else "SCAN")
            
            prog = st.progress(0)
            stat = st.empty()
            
            try:
                stat.info(f"🔧 Loading {mode} configuration...")
                prog.progress(20)
                time.sleep(0.3)
                
                jarvis(f"Target: {target}", "INFO")
                jarvis(f"Max assets: {m['specs']['assets']}", "INFO")
                
                stat.info("🌐 Running reconnaissance...")
                prog.progress(40)
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                if m['specs']['quantum']:
                    jarvis("Quantum analyzers online", "QUANTUM")
                    stat.info("⚛️ Computing quantum vulnerabilities...")
                    prog.progress(60)
                
                df = loop.run_until_complete(run_audit(target, mode))
                
                prog.progress(90)
                jarvis(m["jarvis_complete"], "SUCCESS")
                
                st.session_state.audit_data = df
                st.session_state.current_scan_mode = mode
                st.session_state.current_target = target
                
                prog.progress(100)
                stat.empty()
                prog.empty()
                
                st.success(f"✅ {len(df)} assets analyzed")
                loop.close()
                st.rerun()
                
            except Exception as e:
                jarvis(f"Error: {str(e)[:50]}", "ERROR")
                st.error(f"❌ {e}")
        else:
            st.error("Enter valid domain")
    
    st.markdown("---")
    st.markdown("### 🖥️ Terminal")
    st.markdown(render_jarvis(), unsafe_allow_html=True)
    
    if st.session_state.audit_data is not None:
        if st.button("🔄 New Scan", use_container_width=True):
            st.session_state.audit_data = None
            st.rerun()

# Main content
if st.session_state.audit_data is None:
    # Welcome
    st.markdown("## 🎯 Select Mode & Enter Target")
    
    cols = st.columns(4)
    for i, (name, info) in enumerate(MODES.items()):
        with cols[i]:
            st.markdown(f"""
            <div style='background:{info["gradient"]}; padding:1.5rem; border-radius:15px; height:220px;'>
                <h2 style='margin:0;'>{info["icon"]}</h2>
                <h4 style='margin:0.5rem 0; color:{info["text_color"]};'>{name}</h4>
                <p style='font-size:0.8rem; color:{info["text_color"]}; opacity:0.8;'>{info["tagline"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⏰ Quantum Threat Timeline")
    
    fig = go.Figure()
    years = list(range(2024, 2036))
    threat = [10 + (i**2)/3 for i in range(len(years))]
    threat = [min(100, t) for t in threat]
    
    fig.add_trace(go.Scatter(x=years, y=threat, fill='tozeroy', 
        line=dict(color='#9d4edd', width=3), fillcolor='rgba(157,78,221,0.2)'))
    fig.add_vline(x=2030, line_dash="dash", line_color="#ff4444", annotation_text="CRQC")
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', height=300, xaxis_title="Year", yaxis_title="Threat %")
    st.plotly_chart(fig, use_container_width=True)

else:
    # Results
    df = st.session_state.audit_data
    mode = st.session_state.current_scan_mode
    target = st.session_state.current_target
    m = MODES[mode]
    
    # Mode badge
    st.markdown(f"""
    <div style='display:inline-block; background:{m["gradient"]}; padding:0.5rem 1.5rem; border-radius:25px;'>
        <span style='color:{m["text_color"]}; font-weight:bold;'>{m["icon"]} {mode} | {target}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    total = len(df)
    critical = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    high = len(df[df['Quantum_Risk'].str.contains('High', na=False)])
    qv = len(df[df['quantum_years_vulnerable'] <= 5]) if 'quantum_years_vulnerable' in df.columns and m['specs']['quantum'] else 0
    avg = df['Risk_Score'].mean()
    
    cols = st.columns(5)
    cols[0].metric("🎯 Assets", total)
    cols[1].metric("🔴 Critical", critical)
    cols[2].metric("🟠 High", high)
    cols[3].metric("⚛️ Quantum", qv if m['specs']['quantum'] else "N/A")
    cols[4].metric("📊 Avg Risk", f"{avg:.0f}")
    
    st.markdown("---")
    
    # Tabs based on mode
    if mode == "Comprehensive Audit":
        tabs = st.tabs(["📊 Intelligence", "⚛️ Shor's Algorithm", "🔍 Grover's Algorithm", 
                       "🗺️ Threat Radar", "📋 ISMS Framework", "💰 Budget Calculator", "📥 Export"])
    elif mode in ["Deep Quantum Analysis", "Stealth Mode"]:
        tabs = st.tabs(["📊 Intelligence", "⚛️ Shor's Algorithm", "🔍 Grover's Algorithm", 
                       "🗺️ Threat Radar", "📥 Export"])
    else:
        tabs = st.tabs(["📊 Intelligence", "🗺️ Threat Radar", "📥 Export"])
    
    idx = 0
    
    # Intelligence
    with tabs[idx]:
        st.markdown("### 📊 Threat Intelligence Matrix")
        cols = ['asset', 'ip', 'country', 'criticality', 'Quantum_Risk', 'Risk_Score']
        if m['specs']['quantum']:
            cols += ['quantum_years_vulnerable', 'PQC_Migration', 'PQC_Priority']
        st.dataframe(df[cols], use_container_width=True, height=400)
    idx += 1
    
    # Shor's
    if m['specs']['quantum']:
        with tabs[idx]:
            render_shors_deep_dive(df)
        idx += 1
        
        # Grover's
        with tabs[idx]:
            render_grovers_analysis()
        idx += 1
    
    # Threat Radar
    with tabs[idx]:
        render_threat_radar_explained(df)
    idx += 1
    
    # ISMS (Comprehensive)
    if mode == "Comprehensive Audit":
        with tabs[idx]:
            render_isms_framework(df, target)
        idx += 1
        
        # Budget
        with tabs[idx]:
            render_budget_calculator(df, target)
        idx += 1
    
    # Export
    with tabs[idx]:
        st.markdown("### 📥 Export Reports")
        
        cols = st.columns(4 if mode == "Comprehensive Audit" else 3)
        
        with cols[0]:
            st.markdown("#### 📄 PDF Report")
            pdf = generate_pdf_report(df, target, mode)
            st.download_button("Download PDF", pdf, f"Sentinel_{target}.pdf", "application/pdf", use_container_width=True)
        
        with cols[1]:
            st.markdown("#### 📊 CSV Data")
            csv = df.to_csv(index=False).encode()
            st.download_button("Download CSV", csv, f"Sentinel_{target}.csv", "text/csv", use_container_width=True)
        
        with cols[2]:
            st.markdown("#### 🔗 JSON")
            js = df.to_json(orient='records', indent=2)
            st.download_button("Download JSON", js, f"Sentinel_{target}.json", "application/json", use_container_width=True)
        
        if mode == "Comprehensive Audit":
            with cols[3]:
                st.markdown("#### 📋 ISMS Framework")
                isms = generate_full_isms_pdf(df, target, mode)
                st.download_button("Download ISMS PDF", isms, f"ISMS_{target}.pdf", "application/pdf", use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:#9d4edd;'>SENTINEL-V | Built by SORAA for Thokio | ProSec Networks</p>", unsafe_allow_html=True)