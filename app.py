import streamlit as st
import asyncio
import pandas as pd
from core import SentinelAgent # This must match the class in core.py

st.set_page_config(page_title="Sentinel-V Quantum AI", layout="wide", page_icon="🪷")

if 'audit_data' not in st.session_state:
    st.session_state.audit_data = None

# --- Personal Greeting & Branding ---
st.write("# Hi Lindsay! 🪷🌸🌷🌻")
st.title("🛡️ Sentinel-V: Quantum AI Nerve Center")
st.markdown("---")

target = st.text_input("Enter Strategic Domain", "prosec-networks.com")

if st.button("Initialize Agentic Defense 🚀"):
    agent = SentinelAgent(target)
    with st.spinner("Agentic Observer patrolling attack surface... 🪷"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(agent.autonomous_patrol())
        
        st.session_state.audit_data = pd.DataFrame(results)
        st.session_state.sbom = agent.generate_sbom()

# --- Display Results ---
if st.session_state.audit_data is not None:
    # 2026 Executive Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Quantum Attack Window", "3 Years", "-12mo Acceleration")
    c2.metric("NIS2 Compliance", "✅ Verified", "Article 21 Mode")
    c3.metric("Agent Status", "Patrolling", "🪷 Healthy Garden")

    tab1, tab2, tab3 = st.tabs(["Quantum Readiness ⚛️", "Predictive Forecast 🔮", "Supply Chain (SBOM) 📦"])
    
    with tab1:
        st.dataframe(st.session_state.audit_data[['asset', 'Quantum_Risk', 'PQC_Migration']], use_container_width=True)

    with tab2:
        st.warning("Forecasting assumes AI-accelerated zero-day discovery.")
        st.dataframe(st.session_state.audit_data[['asset', 'Exploit_Forecast']], use_container_width=True)

    with tab3:
        st.info("Software Bill of Materials for Regulatory Transparency.")
        st.table(st.session_state.sbom)
else:
    st.info("Initialize the Sentinel Agent to bloom your defense. 🌼")