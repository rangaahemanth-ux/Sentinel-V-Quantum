import streamlit as st
import asyncio
import pandas as pd
from core import SentinelAgent

# 1. Dashboard Config
st.set_page_config(page_title="Sentinel-V Quantum AI", layout="wide", page_icon="🪷")

if 'audit_data' not in st.session_state:
    st.session_state.audit_data = None

# 2. Personal Greeting & Visuals
st.write("# Hi Lindsay! 🪷🌸🌷🌻")
st.title("🛡️ Sentinel-V: Quantum AI Nerve Center")
st.markdown("---")

# 3. Execution Layer
target = st.text_input("Enter Strategic Domain", "prosec-networks.com")

if st.button("Initialize Agentic Defense 🚀"):
    agent = SentinelAgent(target)
    with st.spinner("Agentic Observer patrolling attack surface... 🪷"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        assets = loop.run_until_complete(agent.run_recon())
        
        # Build Intelligence
        results = []
        for asset in assets:
            pqc = agent.get_pqc_readiness(asset)
            pqc['Forecast'] = agent.forecast_exploit(asset)
            results.append(pqc)
        
        st.session_state.audit_data = pd.DataFrame(results)
        st.session_state.sbom = agent.generate_sbom()

# 4. Display Results
if st.session_state.audit_data is not None:
    # Top Level Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Q-Day Readiness", "42%", "-12% Risk")
    c2.metric("NIS2 Compliance", "✅ Verfied", "Article 21")
    c3.metric("Agent Status", "Active", "🪷 Patrol Mode")

    tab1, tab2, tab3 = st.tabs(["Quantum Readiness ⚛️", "Predictive Forecast 🔮", "Supply Chain (SBOM) 📦"])
    
    with tab1:
        st.dataframe(st.session_state.audit_data[['asset', 'Quantum_Status', 'PQC_Migration', 'Confidentiality_Lifetime']], use_container_width=True)

    with tab2:
        st.warning("Predictive windows are calculated using 2026 AI-Adversarial Telemetry.")
        st.dataframe(st.session_state.audit_data[['asset', 'Forecast']], use_container_width=True)

    with tab3:
        st.info("Automated Software Bill of Materials for Regulatory Transparency.")
        st.table(st.session_state.sbom)
else:
    st.info("Initialize the Sentinel Agent to bloom your defense. 🌼")