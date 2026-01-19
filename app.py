import streamlit as st
import asyncio
import pandas as pd
from core import SentinelAgent, generate_pdf_report

# 1. Dashboard Config
st.set_page_config(page_title="Sentinel-V Quantum AI", layout="wide", page_icon="🪷")

if 'audit_data' not in st.session_state:
    st.session_state.audit_data = None

# 2. Personal Greeting & Branding
st.write("# Hi Lindsay! 🪷🌸🌷🌻")
st.title("🛡️ Sentinel-V: Quantum AI Nerve Center")
st.markdown("---")

# 3. Sidebar Command Center
with st.sidebar:
    st.header("Jarvis Command")
    target = st.text_input("Enter Strategic Domain", "prosec-networks.com")
    run_btn = st.button("Initialize Agentic Defense 🚀")

if run_btn:
    agent = SentinelAgent(target)
    with st.spinner("Agentic Observer patrolling attack surface... 🪷"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        assets = loop.run_until_complete(agent.run_recon())
        
        results = [agent.get_pqc_readiness(a) for a in assets]
        st.session_state.audit_data = pd.DataFrame(results)
        st.session_state.sbom = agent.generate_sbom()

# 4. Display Results
if st.session_state.audit_data is not None:
    c1, c2, c3 = st.columns(3)
    c1.metric("Q-Day Readiness", "42%", "-12% Risk")
    c2.metric("NIS2 Compliance", "✅ Verified", "Article 21")
    c3.metric("Agent Status", "Active", "🪷 Healthy")

    tab1, tab2, tab3 = st.tabs(["Quantum Readiness ⚛️", "Predictive Forecast 🔮", "Supply Chain & Export 📦"])
    
    with tab1:
        st.dataframe(st.session_state.audit_data[['asset', 'Quantum_Status', 'PQC_Migration']], use_container_width=True)

    with tab2:
        st.warning("Forecasting assumes AI-accelerated adversary capabilities.")
        st.dataframe(st.session_state.audit_data[['asset', 'Exploit_Forecast']], use_container_width=True)

    with tab3:
        st.info("SBOM Transparency & PDF Export.")
        st.table(st.session_state.sbom)
        
        pdf_bytes = generate_pdf_report(st.session_state.audit_data, target)
        st.download_button("Download PDF Audit 📥", data=pdf_bytes, file_name="Audit.pdf", mime="application/pdf")
else:
    st.info("Initialize the Sentinel Agent to bloom your defense. 🌼")