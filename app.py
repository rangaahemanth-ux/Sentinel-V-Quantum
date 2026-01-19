import streamlit as st
import asyncio
import pandas as pd
from core import Scanner

st.set_page_config(page_title="Sentinel-V Quantum Edition", layout="wide")

# Persistent memory
if 'audit_data' not in st.session_state:
    st.session_state.audit_data = None

st.title("🛡️ Sentinel-V: Quantum & NIS2 Compliance")

target = st.text_input("Enter Company Domain", "prosec-networks.com")

if st.button("Initialize Deep-Scan"):
    scanner = Scanner(target)
    with st.spinner("Analyzing Attack Surface & Quantum Longevity..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        assets = loop.run_until_complete(scanner.get_subdomains())
        
        # Build results
        c_res = [scanner.calculate_risk(a) for a in assets[:15]]
        q_res = [scanner.analyze_quantum_risk(a) for a in assets[:15]]
        
        # Safely Merge
        df_c = pd.DataFrame(c_res)
        df_q = pd.DataFrame(q_res)
        st.session_state.audit_data = pd.merge(df_c, df_q, on="asset")

# Display Results from Session State
if st.session_state.audit_data is not None:
    df = st.session_state.audit_data
    
    tab1, tab2 = st.tabs(["Classical NIS2 Risk", "Quantum Readiness (HNDL)"])
    
    with tab1:
        avg_c = df['Classical_Risk'].mean() # This key must match core.py
        st.metric("Overall Classical Risk", f"{avg_c:.1f}%")
        st.dataframe(df[['asset', 'Classical_Risk', 'status', 'risks']], use_container_width=True)

    with tab2:
        st.warning("Adversaries may harvest this data today for future decryption.")
        st.dataframe(df[['asset', 'Quantum_Risk', 'Quantum_Status', 'Recommendation']], use_container_width=True)
else:
    st.info("Enter a domain to begin the audit.")