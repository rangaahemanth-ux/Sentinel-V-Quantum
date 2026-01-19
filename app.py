import streamlit as st
import asyncio
import pandas as pd
import folium
from streamlit_folium import st_folium
from core import SentinelAgent, generate_pdf_report

# 1. Page Config & Professional Styling
st.set_page_config(page_title="Sentinel-V Quantum AI", layout="wide", page_icon="🛡️")

# Initialize Session State
if 'audit_data' not in st.session_state:
    st.session_state.audit_data = None
if 'sbom' not in st.session_state:
    st.session_state.sbom = None

st.title("🛡️ Sentinel-V: Quantum AI Nerve Center")
st.markdown("---")

# 2. Sidebar Controls
with st.sidebar:
    st.header("Jarvis Command")
    target = st.text_input("Strategic Domain", "prosec-networks.com")
    if st.button("Initialize Agentic Defense 🚀"):
        agent = SentinelAgent(target)
        with st.spinner("Agentic Observer patrolling attack surface..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            assets = loop.run_until_complete(agent.run_recon())
            results = [agent.get_pqc_readiness(a) for a in assets]
            st.session_state.audit_data = pd.DataFrame(results)
            st.session_state.sbom = agent.generate_sbom()

# 3. Global Threat Radar (The Map)
st.subheader("🌐 Global Adversarial Radar")
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
# Strategic Markers for 2026 Threat Vectors
folium.Marker([48.85, 2.35], popup="Shadow IT Found (EU)", icon=folium.Icon(color='red')).add_to(m)
folium.Marker([34.05, -118.24], popup="HNDL Risk (US)", icon=folium.Icon(color='orange')).add_to(m)
st_folium(m, width=1200, height=350)

# 4. Result Center
if st.session_state.audit_data is not None:
    tab1, tab2, tab3 = st.tabs(["Quantum & NIS2 ⚛️", "Remediation Solutions 💡", "Export & SBOM 📦"])
    
    with tab1:
        st.dataframe(st.session_state.audit_data[['asset', 'Quantum_Risk', 'PQC_Migration']], use_container_width=True)

    with tab2:
        st.info("### 2026 Up-to-Date Solutions")
        for _, row in st.session_state.audit_data.iterrows():
            if "Critical" in row['Quantum_Risk']:
                st.error(f"**{row['asset']}**: {row['Solution']}")
            else:
                st.success(f"**{row['asset']}**: {row['Solution']}")

    with tab3:
        st.table(st.session_state.sbom)
        pdf_bytes = generate_pdf_report(st.session_state.audit_data, target)
        st.download_button("Download PDF Security Audit 📥", data=pdf_bytes, file_name="Audit.pdf")
else:
    st.info("Initialize the Sentinel Agent to begin the boardroom audit.")