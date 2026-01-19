"""
Quantum Cryptography Module for Sentinel-V
Demonstrates quantum-resistant algorithms and quantum key distribution
"""

import numpy as np
import hashlib
import secrets
from datetime import datetime
from typing import Dict, Tuple, List
import json

class QuantumCryptoSimulator:
    """
    Simulates quantum cryptographic concepts for educational and demonstration purposes
    """
    
    def __init__(self):
        self.ml_kem_key_sizes = {
            'ML-KEM-512': 512,
            'ML-KEM-768': 768,
            'ML-KEM-1024': 1024
        }
        
    def simulate_shor_threat(self, key_size: int) -> Dict:
        """
        Simulate Shor's algorithm threat to classical RSA encryption
        Shows why quantum computers threaten current encryption
        """
        # Classical RSA time complexity: O(exp(n^(1/3)))
        # Quantum (Shor's) time complexity: O(n^3)
        
        classical_time = np.exp(key_size ** (1/3)) / 1e9  # Simplified model
        quantum_time = (key_size ** 3) / 1e12  # With quantum computer
        
        speedup_factor = classical_time / quantum_time
        
        # Estimate when quantum computers will break this
        quantum_breakthrough_year = 2030 if key_size <= 2048 else 2035
        years_until_vulnerable = max(0, quantum_breakthrough_year - datetime.now().year)
        
        return {
            'key_size': key_size,
            'classical_break_time_years': classical_time / (365 * 24 * 3600),
            'quantum_break_time_hours': quantum_time / 3600,
            'speedup_factor': speedup_factor,
            'threat_level': 'CRITICAL' if years_until_vulnerable <= 5 else 'HIGH' if years_until_vulnerable <= 10 else 'MODERATE',
            'years_until_vulnerable': years_until_vulnerable,
            'recommendation': self._get_threat_recommendation(years_until_vulnerable)
        }
    
    def _get_threat_recommendation(self, years: int) -> str:
        if years <= 5:
            return "URGENT: Migrate to PQC immediately. Current encryption vulnerable within 5 years."
        elif years <= 10:
            return "HIGH PRIORITY: Begin PQC migration planning. Quantum threat imminent."
        else:
            return "MONITOR: Stay informed on quantum computing advances. Plan for eventual migration."
    
    def simulate_bb84_qkd(self, num_qubits: int = 100) -> Dict:
        """
        Simulate BB84 Quantum Key Distribution Protocol
        Shows how quantum mechanics enables provably secure key exchange
        """
        # Alice prepares random bits and bases
        alice_bits = np.random.randint(0, 2, num_qubits)
        alice_bases = np.random.randint(0, 2, num_qubits)  # 0: rectilinear, 1: diagonal
        
        # Bob measures in random bases
        bob_bases = np.random.randint(0, 2, num_qubits)
        
        # Simulate eavesdropping attempt (Eve intercepts)
        eve_present = np.random.random() < 0.3  # 30% chance of eavesdropper
        if eve_present:
            eve_bases = np.random.randint(0, 2, num_qubits)
            # Eve's measurement collapses quantum state, introducing errors
            error_rate = 0.25  # Expected error rate from eavesdropping
        else:
            error_rate = 0.01  # Natural noise
        
        # Bob's measurements (with potential Eve-induced errors)
        bob_bits = np.copy(alice_bits)
        matching_bases = alice_bases == bob_bases
        
        # Add errors where bases don't match or Eve interfered
        for i in range(num_qubits):
            if not matching_bases[i] or (eve_present and np.random.random() < error_rate):
                bob_bits[i] = np.random.randint(0, 2)
        
        # Sifting: Keep only bits where bases matched
        sifted_key = alice_bits[matching_bases]
        bob_sifted = bob_bits[matching_bases]
        
        # Error checking on sample
        sample_size = min(20, len(sifted_key))
        if sample_size > 0:
            sample_indices = np.random.choice(len(sifted_key), sample_size, replace=False)
            errors = np.sum(sifted_key[sample_indices] != bob_sifted[sample_indices])
            measured_error_rate = errors / sample_size
        else:
            measured_error_rate = 0
        
        # Determine if key is secure
        secure = measured_error_rate < 0.11  # Threshold for BB84 security
        
        return {
            'protocol': 'BB84 Quantum Key Distribution',
            'total_qubits_sent': num_qubits,
            'sifted_key_length': len(sifted_key),
            'efficiency': len(sifted_key) / num_qubits,
            'eavesdropper_detected': eve_present and not secure,
            'measured_error_rate': measured_error_rate,
            'security_status': 'SECURE' if secure else 'COMPROMISED',
            'key_established': secure,
            'quantum_advantage': 'Information-theoretic security via quantum mechanics'
        }
    
    def analyze_pqc_migration(self, current_crypto: str, asset_criticality: str) -> Dict:
        """
        Analyze Post-Quantum Cryptography migration strategy
        """
        migration_strategies = {
            'RSA-2048': {
                'vulnerability': 'HIGH',
                'recommended_pqc': 'ML-KEM-768',
                'migration_complexity': 'MEDIUM',
                'performance_impact': '15-25% overhead',
                'timeline': 'Immediate (0-6 months)'
            },
            'RSA-4096': {
                'vulnerability': 'MODERATE',
                'recommended_pqc': 'ML-KEM-1024',
                'migration_complexity': 'MEDIUM',
                'performance_impact': '20-30% overhead',
                'timeline': 'Near-term (6-18 months)'
            },
            'ECC-256': {
                'vulnerability': 'HIGH',
                'recommended_pqc': 'ML-KEM-768',
                'migration_complexity': 'LOW',
                'performance_impact': '10-20% overhead',
                'timeline': 'Immediate (0-6 months)'
            },
            'AES-256': {
                'vulnerability': 'LOW',
                'recommended_pqc': 'AES-256 (Quantum-resistant with larger keys)',
                'migration_complexity': 'LOW',
                'performance_impact': 'Minimal',
                'timeline': 'Monitor (Grover\'s algorithm doubles key search space)'
            }
        }
        
        strategy = migration_strategies.get(current_crypto, {
            'vulnerability': 'UNKNOWN',
            'recommended_pqc': 'ML-KEM-768',
            'migration_complexity': 'HIGH',
            'performance_impact': 'Variable',
            'timeline': 'Requires assessment'
        })
        
        # Adjust based on asset criticality
        if asset_criticality == 'CRITICAL':
            strategy['timeline'] = 'IMMEDIATE (0-3 months)'
            strategy['priority'] = 'P0 - Mission Critical'
        elif asset_criticality == 'HIGH':
            strategy['priority'] = 'P1 - High Priority'
        else:
            strategy['priority'] = 'P2 - Standard'
        
        return {
            'current_cryptography': current_crypto,
            'asset_criticality': asset_criticality,
            **strategy,
            'hybrid_mode_available': True,
            'hybrid_benefits': 'Combines classical and PQC for defense-in-depth'
        }
    
    def simulate_quantum_entropy(self, num_bits: int = 256) -> Dict:
        """
        Simulate quantum random number generation
        Shows how quantum mechanics provides true randomness
        """
        # Simulate quantum measurement of superposition states
        # In reality, this would use quantum hardware
        quantum_bits = np.random.randint(0, 2, num_bits)
        
        # Classical PRNG for comparison
        classical_bits = [int(b) for b in bin(secrets.randbits(num_bits))[2:].zfill(num_bits)]
        
        # Calculate entropy (should be close to 1.0 for true randomness)
        def calculate_entropy(bits):
            counts = np.bincount(bits)
            probabilities = counts / len(bits)
            entropy = -np.sum([p * np.log2(p) if p > 0 else 0 for p in probabilities])
            return entropy
        
        quantum_entropy = calculate_entropy(quantum_bits)
        
        # Generate cryptographic key from quantum randomness
        quantum_key = hashlib.sha256(bytes(quantum_bits)).hexdigest()
        
        return {
            'method': 'Quantum Random Number Generation',
            'bits_generated': num_bits,
            'entropy_bits': quantum_entropy,
            'entropy_quality': 'EXCELLENT' if quantum_entropy > 0.99 else 'GOOD' if quantum_entropy > 0.95 else 'POOR',
            'quantum_key_sample': quantum_key[:32] + '...',
            'advantage': 'True randomness from quantum superposition, not algorithmic PRNG',
            'use_cases': ['Cryptographic keys', 'Nonces', 'IVs', 'Session tokens']
        }
    
    def quantum_threat_timeline(self) -> Dict:
        """
        Provide timeline of quantum computing threats
        """
        current_year = datetime.now().year
        
        timeline = {
            'current_state': {
                'year': current_year,
                'status': 'NISQ Era (Noisy Intermediate-Scale Quantum)',
                'qubit_count': '50-1000 qubits',
                'threat_level': 'Research Phase',
                'action': 'Begin PQC planning'
            },
            'near_term': {
                'year': '2026-2028',
                'status': 'Early Fault-Tolerant Quantum Computers',
                'qubit_count': '1,000-10,000 logical qubits',
                'threat_level': 'EMERGING',
                'action': 'Deploy hybrid classical-PQC systems'
            },
            'medium_term': {
                'year': '2028-2032',
                'status': 'Cryptographically Relevant Quantum Computers (CRQC)',
                'qubit_count': '10,000+ logical qubits',
                'threat_level': 'CRITICAL',
                'action': 'Full PQC migration required'
            },
            'long_term': {
                'year': '2032+',
                'status': 'Universal Quantum Computers',
                'qubit_count': '100,000+ logical qubits',
                'threat_level': 'REALITY',
                'action': 'Classical crypto obsolete for many use cases'
            },
            'harvest_now_decrypt_later': {
                'threat': 'Adversaries collecting encrypted data NOW to decrypt later',
                'urgency': 'IMMEDIATE',
                'affected': 'Long-lived sensitive data (medical, financial, government)',
                'timeline': 'Threat is ACTIVE TODAY'
            }
        }
        
        return timeline
    
    def demonstrate_grovers_algorithm(self, database_size: int = 1000000) -> Dict:
        """
        Demonstrate Grover's algorithm for unstructured search
        Shows quadratic speedup for searching
        """
        # Classical search: O(N)
        classical_operations = database_size
        
        # Grover's algorithm: O(√N)
        quantum_operations = int(np.sqrt(database_size) * np.pi / 4)
        
        speedup = classical_operations / quantum_operations
        
        return {
            'algorithm': "Grover's Search Algorithm",
            'database_size': database_size,
            'classical_operations': classical_operations,
            'quantum_operations': quantum_operations,
            'speedup_factor': f'{speedup:.1f}x',
            'impact_on_security': 'Symmetric encryption requires doubled key sizes',
            'example': 'AES-128 becomes effectively AES-64 (insecure)',
            'mitigation': 'Use AES-256 or larger for quantum resistance'
        }
    
    def generate_quantum_report(self, asset: str, current_crypto: str) -> Dict:
        """
        Generate comprehensive quantum threat report for an asset
        """
        report = {
            'asset': asset,
            'timestamp': datetime.now().isoformat(),
            'current_cryptography': current_crypto,
            'assessments': {}
        }
        
        # Shor's algorithm threat
        if 'RSA' in current_crypto or 'ECC' in current_crypto:
            key_size = int(current_crypto.split('-')[1]) if '-' in current_crypto else 2048
            report['assessments']['shor_threat'] = self.simulate_shor_threat(key_size)
        
        # PQC migration analysis
        report['assessments']['pqc_migration'] = self.analyze_pqc_migration(
            current_crypto, 
            'CRITICAL' if any(k in asset for k in ['api', 'vault', 'secure']) else 'MODERATE'
        )
        
        # Quantum timeline
        report['timeline'] = self.quantum_threat_timeline()
        
        # Grover's impact (for symmetric crypto)
        if 'AES' in current_crypto:
            report['assessments']['grovers_impact'] = self.demonstrate_grovers_algorithm()
        
        return report


def generate_quantum_dashboard_data() -> Dict:
    """
    Generate data for quantum threat dashboard visualization
    """
    simulator = QuantumCryptoSimulator()
    
    # Simulate various scenarios
    rsa_2048_threat = simulator.simulate_shor_threat(2048)
    rsa_4096_threat = simulator.simulate_shor_threat(4096)
    bb84_demo = simulator.simulate_bb84_qkd(100)
    quantum_rng = simulator.simulate_quantum_entropy(256)
    timeline = simulator.quantum_threat_timeline()
    
    return {
        'threat_analysis': {
            'RSA-2048': rsa_2048_threat,
            'RSA-4096': rsa_4096_threat
        },
        'qkd_demonstration': bb84_demo,
        'quantum_rng': quantum_rng,
        'threat_timeline': timeline,
        'summary': {
            'immediate_threats': 2,
            'high_priority_migrations': 3,
            'quantum_advantage_demos': 2
        }
    }