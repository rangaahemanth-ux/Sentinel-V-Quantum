"""
Quantum Computing Concepts Dashboard for Sentinel-V
Educational and demonstration module for quantum cryptography
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from quantum_crypto import QuantumCryptoSimulator, generate_quantum_dashboard_data
import numpy as np
from datetime import datetime

def render_quantum_dashboard():
    """
    Render the quantum computing concepts dashboard
    """
    st.title("⚛️ Quantum Computing Threat Intelligence")
    st.caption("Understanding Post-Quantum Cryptography & Quantum-Safe Security")
    
    # Initialize simulator
    simulator = QuantumCryptoSimulator()
    
    # Create tabs for different concepts
    tabs = st.tabs([
        "🎯 Threat Timeline",
        "🔐 Shor's Algorithm",
        "🌟 Quantum Key Distribution",
        "🎲 Quantum Randomness",
        "📊 PQC Migration",
        "🧪 Live Simulation"
    ])
    
    # TAB 1: Threat Timeline
    with tabs[0]:
        st.header("Quantum Computing Threat Timeline")
        st.markdown("""
        Understanding when quantum computers will threaten current encryption is crucial for planning.
        The **"Harvest Now, Decrypt Later"** threat means adversaries are collecting encrypted data TODAY.
        """)
        
        timeline = simulator.quantum_threat_timeline()
        
        # Create timeline visualization
        years = [2024, 2027, 2030, 2035]
        threat_levels = [20, 50, 85, 100]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years,
            y=threat_levels,
            mode='lines+markers',
            name='Quantum Threat Level',
            line=dict(color='#FF6B6B', width=4),
            marker=dict(size=12),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ))
        
        fig.update_layout(
            title="Quantum Computing Threat Progression",
            xaxis_title="Year",
            yaxis_title="Threat Level (%)",
            template="plotly_dark",
            height=400,
            annotations=[
                dict(x=2024, y=20, text="NISQ Era", showarrow=True, arrowhead=2),
                dict(x=2027, y=50, text="Early Fault-Tolerant", showarrow=True, arrowhead=2),
                dict(x=2030, y=85, text="CRQC Emergence", showarrow=True, arrowhead=2),
                dict(x=2035, y=100, text="Universal QC", showarrow=True, arrowhead=2)
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Timeline cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("**📅 Current State (2024-2026)**")
            st.markdown(f"""
            - **Status:** {timeline['current_state']['status']}
            - **Qubits:** {timeline['current_state']['qubit_count']}
            - **Threat:** {timeline['current_state']['threat_level']}
            - **Action:** {timeline['current_state']['action']}
            """)
            
            st.warning("**⚡ Near-Term (2026-2028)**")
            st.markdown(f"""
            - **Status:** {timeline['near_term']['status']}
            - **Threat:** {timeline['near_term']['threat_level']}
            - **Action:** {timeline['near_term']['action']}
            """)
        
        with col2:
            st.error("**🚨 Medium-Term (2028-2032)**")
            st.markdown(f"""
            - **Status:** {timeline['medium_term']['status']}
            - **Threat:** {timeline['medium_term']['threat_level']}
            - **Action:** {timeline['medium_term']['action']}
            """)
            
            st.error("**⚠️ HARVEST NOW, DECRYPT LATER**")
            st.markdown(f"""
            - **Threat:** {timeline['harvest_now_decrypt_later']['threat']}
            - **Urgency:** {timeline['harvest_now_decrypt_later']['urgency']}
            - **Timeline:** {timeline['harvest_now_decrypt_later']['timeline']}
            """)
    
    # TAB 2: Shor's Algorithm
    with tabs[1]:
        st.header("🔐 Shor's Algorithm: The RSA Killer")
        st.markdown("""
        Shor's algorithm can factor large numbers exponentially faster than classical computers,
        breaking RSA and ECC encryption that protects most of the internet today.
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            key_size = st.select_slider(
                "RSA Key Size",
                options=[1024, 2048, 3072, 4096, 8192],
                value=2048
            )
            
            threat = simulator.simulate_shor_threat(key_size)
            
            # Visualization
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Classical Computer',
                x=['Break Time'],
                y=[threat['classical_break_time_years']],
                marker_color='#4ECDC4'
            ))
            
            fig.add_trace(go.Bar(
                name='Quantum Computer',
                x=['Break Time'],
                y=[threat['quantum_break_time_hours'] / (365 * 24)],
                marker_color='#FF6B6B'
            ))
            
            fig.update_layout(
                title=f"Time to Break RSA-{key_size}",
                yaxis_title="Years",
                template="plotly_dark",
                height=400,
                yaxis_type="log"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric("Key Size", f"{key_size} bits")
            st.metric("Threat Level", threat['threat_level'])
            st.metric("Quantum Speedup", f"{threat['speedup_factor']:.1e}x")
            st.metric("Years Until Vulnerable", threat['years_until_vulnerable'])
        
        st.error(f"**Recommendation:** {threat['recommendation']}")
        
        # Educational explanation
        with st.expander("🧠 How Shor's Algorithm Works"):
            st.markdown("""
            ### The Quantum Advantage
            
            **Classical Factoring:**
            - Uses trial division, Pollard's rho, or general number field sieve
            - Time complexity: O(exp(n^(1/3)))
            - RSA-2048 would take billions of years
            
            **Shor's Algorithm (Quantum):**
            - Uses quantum period-finding
            - Time complexity: O(n³)
            - RSA-2048 could be broken in hours with a large enough quantum computer
            
            **The Process:**
            1. Convert factoring to period-finding problem
            2. Use quantum superposition to evaluate function at all points simultaneously
            3. Apply Quantum Fourier Transform to find period
            4. Extract factors from period
            
            **Why It's Revolutionary:**
            - Exponential speedup over all known classical algorithms
            - Threatens all public-key cryptography based on factoring or discrete log
            - Motivates the entire Post-Quantum Cryptography movement
            """)
    
    # TAB 3: Quantum Key Distribution
    with tabs[2]:
        st.header("🌟 Quantum Key Distribution (BB84)")
        st.markdown("""
        BB84 uses quantum mechanics to create **provably secure** key exchange.
        Any eavesdropping attempt is automatically detected due to quantum measurement collapse.
        """)
        
        if st.button("🚀 Run BB84 Simulation", type="primary"):
            with st.spinner("Exchanging quantum keys..."):
                result = simulator.simulate_bb84_qkd(150)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Qubits Sent", result['total_qubits_sent'])
                with col2:
                    st.metric("Key Length", result['sifted_key_length'])
                with col3:
                    st.metric("Efficiency", f"{result['efficiency']*100:.1f}%")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    status_color = "🟢" if result['security_status'] == 'SECURE' else "🔴"
                    st.metric("Security Status", f"{status_color} {result['security_status']}")
                with col2:
                    st.metric("Error Rate", f"{result['measured_error_rate']*100:.1f}%")
                
                if result['eavesdropper_detected']:
                    st.error("🚨 **EAVESDROPPER DETECTED!** Quantum state collapse revealed unauthorized interception.")
                else:
                    st.success("✅ **KEY ESTABLISHED SECURELY** - No eavesdropping detected.")
                
                st.info(f"**Quantum Advantage:** {result['quantum_advantage']}")
        
        with st.expander("🧠 How BB84 Protocol Works"):
            st.markdown("""
            ### The BB84 Protocol (1984)
            
            **Step 1: Preparation**
            - Alice prepares random bits (0 or 1)
            - She encodes each bit in random basis (rectilinear ↕ or diagonal ⤢)
            - Sends quantum states to Bob
            
            **Step 2: Measurement**
            - Bob measures in random bases
            - Where bases match, he gets Alice's bit
            - Where bases don't match, result is random (50/50)
            
            **Step 3: Basis Reconciliation**
            - Alice and Bob publicly compare bases (NOT bits!)
            - Keep only bits where bases matched (~50%)
            - This is the "sifted key"
            
            **Step 4: Eavesdropping Check**
            - Sample random bits to check error rate
            - High errors = eavesdropper detected!
            - Low errors = key is secure
            
            **Why It's Unbreakable:**
            - Quantum no-cloning theorem: Can't copy unknown quantum states
            - Measurement collapse: Eavesdropping changes quantum states
            - Physics guarantees security, not computational hardness
            """)
    
    # TAB 4: Quantum Randomness
    with tabs[3]:
        st.header("🎲 Quantum Random Number Generation")
        st.markdown("""
        True randomness from quantum superposition vs. pseudo-randomness from algorithms.
        Quantum RNG is essential for cryptographic keys, nonces, and security tokens.
        """)
        
        if st.button("🎲 Generate Quantum Random Numbers", type="primary"):
            result = simulator.simulate_quantum_entropy(512)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Bits Generated", result['bits_generated'])
            with col2:
                st.metric("Entropy", f"{result['entropy_bits']:.4f}")
            with col3:
                st.metric("Quality", result['entropy_quality'])
            
            st.code(result['quantum_key_sample'], language='text')
            
            st.success(f"**Advantage:** {result['advantage']}")
            
            st.markdown("**Use Cases:**")
            for use_case in result['use_cases']:
                st.markdown(f"- {use_case}")
        
        with st.expander("🧠 Quantum vs Classical Randomness"):
            st.markdown("""
            ### The Difference
            
            **Classical Pseudo-Random (PRNG):**
            - Deterministic algorithm
            - Seed-based: same seed = same sequence
            - Statistically random but theoretically predictable
            - Examples: Mersenne Twister, Linear Congruential Generator
            
            **Quantum True Random (QRNG):**
            - Based on quantum superposition
            - Fundamentally non-deterministic
            - No seed, no algorithm
            - Physically impossible to predict
            
            **How QRNG Works:**
            1. Prepare qubit in superposition: |ψ⟩ = (|0⟩ + |1⟩)/√2
            2. Measure in computational basis
            3. Result is 0 or 1 with equal probability
            4. Repeat for each bit needed
            
            **Why It Matters:**
            - Cryptographic keys must be truly random
            - Weak randomness = weak encryption
            - Quantum provides provable randomness
            """)
    
    # TAB 5: PQC Migration
    with tabs[4]:
        st.header("📊 Post-Quantum Cryptography Migration")
        st.markdown("""
        Practical roadmap for transitioning to quantum-resistant algorithms.
        NIST has standardized ML-KEM, ML-DSA, and SLH-DSA for PQC.
        """)
        
        current_crypto = st.selectbox(
            "Current Cryptography",
            ['RSA-2048', 'RSA-4096', 'ECC-256', 'AES-256']
        )
        
        criticality = st.selectbox(
            "Asset Criticality",
            ['CRITICAL', 'HIGH', 'MODERATE', 'LOW']
        )
        
        analysis = simulator.analyze_pqc_migration(current_crypto, criticality)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.error(f"**Vulnerability:** {analysis['vulnerability']}")
            st.success(f"**Recommended PQC:** {analysis['recommended_pqc']}")
            st.info(f"**Migration Complexity:** {analysis['migration_complexity']}")
        
        with col2:
            st.warning(f"**Timeline:** {analysis['timeline']}")
            st.metric("Priority", analysis['priority'])
            st.info(f"**Performance Impact:** {analysis['performance_impact']}")
        
        if analysis['hybrid_mode_available']:
            st.success(f"✅ **Hybrid Mode Available:** {analysis['hybrid_benefits']}")
        
        # Migration roadmap
        st.subheader("📋 Migration Roadmap")
        
        roadmap_data = {
            'Phase': ['Assessment', 'Planning', 'Pilot', 'Deployment', 'Validation'],
            'Duration': ['2 weeks', '1 month', '2 months', '3-6 months', '1 month'],
            'Activities': [
                'Inventory crypto assets, identify dependencies',
                'Select PQC algorithms, design hybrid architecture',
                'Deploy to test environment, performance testing',
                'Phased rollout, monitor compatibility',
                'Security audit, compliance verification'
            ]
        }
        
        st.table(pd.DataFrame(roadmap_data))
    
    # TAB 6: Live Simulation
    with tabs[5]:
        st.header("🧪 Interactive Quantum Simulation")
        st.markdown("Experiment with quantum concepts in real-time.")
        
        sim_type = st.selectbox(
            "Select Simulation",
            ['Shor\'s Algorithm', 'Grover\'s Algorithm', 'BB84 QKD', 'Quantum Superposition']
        )
        
        if sim_type == "Grover's Algorithm":
            database_size = st.slider("Database Size", 1000, 10000000, 1000000, step=1000)
            
            if st.button("Run Grover Simulation"):
                result = simulator.demonstrate_grovers_algorithm(database_size)
                
                st.success(f"**Algorithm:** {result['algorithm']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Classical Operations", f"{result['classical_operations']:,}")
                with col2:
                    st.metric("Quantum Operations", f"{result['quantum_operations']:,}")
                with col3:
                    st.metric("Speedup", result['speedup_factor'])
                
                st.warning(f"**Security Impact:** {result['impact_on_security']}")
                st.info(f"**Example:** {result['example']}")
                st.success(f"**Mitigation:** {result['mitigation']}")


def add_quantum_tab_to_main_app():
    """
    Function to integrate quantum dashboard into main Sentinel-V app
    """
    return render_quantum_dashboard()