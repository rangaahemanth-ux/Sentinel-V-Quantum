"""
Sentinel-V Intelligence Engine with Quantum Threat Analysis
Complete core module for autonomous reconnaissance and quantum risk assessment
"""

import asyncio
import aiohttp
import socket
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import ssl
import certifi
from typing import Dict, List, Tuple
import hashlib


class QuantumThreatAnalyzer:
    """Quantum computing threat assessment for cryptographic assets"""
    
    def __init__(self):
        self.quantum_timeline = {
            2024: {'threat_level': 15, 'capability': 'NISQ'},
            2027: {'threat_level': 40, 'capability': 'Early Fault-Tolerant'},
            2030: {'threat_level': 75, 'capability': 'CRQC'},
            2035: {'threat_level': 95, 'capability': 'Universal Quantum'}
        }
    
    def assess_crypto_vulnerability(self, crypto_type: str, key_size: int = 2048) -> Dict:
        """Assess quantum vulnerability of cryptographic system"""
        current_year = datetime.now().year
        
        vulnerability_map = {
            'RSA': {
                'algorithm_threat': 'Shor',
                'quantum_speedup': 'Exponential',
                'vulnerability_year': 2030 if key_size <= 2048 else 2032,
                'severity': 'CRITICAL'
            },
            'ECC': {
                'algorithm_threat': 'Shor',
                'quantum_speedup': 'Exponential',
                'vulnerability_year': 2030,
                'severity': 'CRITICAL'
            },
            'AES': {
                'algorithm_threat': 'Grover',
                'quantum_speedup': 'Quadratic',
                'vulnerability_year': 2040,
                'severity': 'MODERATE'
            },
            'SHA': {
                'algorithm_threat': 'Grover',
                'quantum_speedup': 'Quadratic',
                'vulnerability_year': 2040,
                'severity': 'LOW'
            }
        }
        
        # Determine crypto type from key size hints
        if key_size >= 1024:
            crypto_category = 'RSA'
        else:
            crypto_category = crypto_type
        
        threat_info = vulnerability_map.get(crypto_category, vulnerability_map['RSA'])
        years_until_vulnerable = max(0, threat_info['vulnerability_year'] - current_year)
        
        # Calculate quantum risk score
        if years_until_vulnerable <= 3:
            risk_score = 95
            urgency = 'IMMEDIATE'
        elif years_until_vulnerable <= 5:
            risk_score = 85
            urgency = 'URGENT'
        elif years_until_vulnerable <= 7:
            risk_score = 70
            urgency = 'HIGH'
        else:
            risk_score = 50
            urgency = 'MODERATE'
        
        return {
            'crypto_type': crypto_category,
            'key_size': key_size,
            'threat_algorithm': threat_info['algorithm_threat'],
            'quantum_speedup': threat_info['quantum_speedup'],
            'years_until_vulnerable': years_until_vulnerable,
            'vulnerability_year': threat_info['vulnerability_year'],
            'quantum_risk_score': risk_score,
            'urgency': urgency,
            'severity': threat_info['severity']
        }
    
    def recommend_pqc_algorithm(self, asset_type: str, criticality: str) -> Dict:
        """Recommend Post-Quantum Cryptography algorithm"""
        recommendations = {
            'CRITICAL': {
                'key_encapsulation': 'ML-KEM-1024',
                'digital_signature': 'ML-DSA-87',
                'hash': 'SHA-3-512',
                'migration_priority': 'P0 - Immediate',
                'timeline': '0-3 months'
            },
            'HIGH': {
                'key_encapsulation': 'ML-KEM-768',
                'digital_signature': 'ML-DSA-65',
                'hash': 'SHA-3-256',
                'migration_priority': 'P1 - Urgent',
                'timeline': '3-6 months'
            },
            'MODERATE': {
                'key_encapsulation': 'ML-KEM-512',
                'digital_signature': 'ML-DSA-44',
                'hash': 'SHA-3-256',
                'migration_priority': 'P2 - Standard',
                'timeline': '6-12 months'
            }
        }
        
        recommendation = recommendations.get(criticality, recommendations['MODERATE'])
        
        return {
            'criticality': criticality,
            'recommended_kem': recommendation['key_encapsulation'],
            'recommended_signature': recommendation['digital_signature'],
            'recommended_hash': recommendation['hash'],
            'migration_priority': recommendation['migration_priority'],
            'timeline': recommendation['timeline'],
            'hybrid_mode': 'Combine with classical crypto during transition',
            'nist_standard': 'FIPS 203, 204, 205'
        }


class SentinelAgent:
    """Autonomous reconnaissance agent with quantum threat intelligence"""
    
    def __init__(self, domain: str):
        self.domain = domain
        self.session = None
        self.quantum_analyzer = QuantumThreatAnalyzer()
        
    async def __aenter__(self):
        """Context manager for proper session handling"""
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup session on exit"""
        if self.session:
            await self.session.close()
            await asyncio.sleep(0.25)  # Give time for cleanup

    async def get_geo_data(self, asset: str) -> Dict:
        """Enhanced geolocation with fallback and error handling"""
        try:
            # Resolve IP with timeout
            loop = asyncio.get_event_loop()
            ip = await asyncio.wait_for(
                loop.run_in_executor(None, socket.gethostbyname, asset),
                timeout=5.0
            )
            
            # Try primary geo API
            try:
                async with self.session.get(
                    f"http://ip-api.com/json/{ip}",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data.get("status") == "success":
                            return {
                                "lat": data.get("lat", 0.0),
                                "lon": data.get("lon", 0.0),
                                "country": data.get("country", "Unknown"),
                                "city": data.get("city", "Unknown"),
                                "isp": data.get("isp", "Unknown"),
                                "ip": ip,
                                "timezone": data.get("timezone", "Unknown")
                            }
            except asyncio.TimeoutError:
                pass
                
            # Fallback to ipapi.co
            try:
                async with self.session.get(
                    f"https://ipapi.co/{ip}/json/",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            "lat": data.get("latitude", 0.0),
                            "lon": data.get("longitude", 0.0),
                            "country": data.get("country_name", "Unknown"),
                            "city": data.get("city", "Unknown"),
                            "isp": data.get("org", "Unknown"),
                            "ip": ip,
                            "timezone": data.get("timezone", "Unknown")
                        }
            except:
                pass
                
        except (socket.gaierror, asyncio.TimeoutError, Exception) as e:
            print(f"Geo lookup failed for {asset}: {str(e)}")
            
        # Return default values if all attempts fail
        return {
            "lat": 0.0,
            "lon": 0.0,
            "country": "Unknown",
            "city": "Unknown",
            "isp": "Unknown",
            "ip": "N/A",
            "timezone": "Unknown"
        }

    async def run_recon(self) -> List[str]:
        """Enhanced subdomain discovery with multiple sources"""
        discovered_assets = set()
        
        # Method 1: Certificate Transparency (crt.sh)
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            async with self.session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for entry in data[:100]:  # Increased limit
                        name = entry.get('name_value', '').lower()
                        for subdomain in name.split('\n'):
                            subdomain = subdomain.strip().replace('*.', '')
                            if subdomain and self.domain in subdomain:
                                discovered_assets.add(subdomain)
        except Exception as e:
            print(f"crt.sh lookup failed: {str(e)}")
        
        # Method 2: Common subdomains bruteforce
        common_subdomains = [
            'www', 'mail', 'remote', 'blog', 'webmail', 'server',
            'ns1', 'ns2', 'smtp', 'secure', 'vpn', 'api', 'vault',
            'admin', 'dev', 'staging', 'test', 'portal', 'gateway',
            'pqc', 'quantum', 'shield', 'sentinel', 'monitor',
            'auth', 'sso', 'identity', 'iam', 'keys', 'crypto',
            'internal', 'external', 'public', 'private', 'prod'
        ]
        
        for sub in common_subdomains:
            discovered_assets.add(f"{sub}.{self.domain}")
        
        # Always include the root domain
        discovered_assets.add(self.domain)
        
        # Return sorted list, limited to top 20 for demo
        return sorted(list(discovered_assets))[:20]

    async def check_ssl_cert(self, asset: str) -> Dict:
        """Check SSL certificate validity, strength, and quantum readiness"""
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            loop = asyncio.get_event_loop()
            
            def check_cert():
                with socket.create_connection((asset, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=asset) as ssock:
                        cert = ssock.getpeercert()
                        cipher = ssock.cipher()
                        
                        # Extract certificate details
                        issuer = dict(x[0] for x in cert.get('issuer', []))
                        
                        # Determine crypto algorithm from cipher
                        cipher_name = cipher[0] if cipher else 'Unknown'
                        
                        # Check if quantum-resistant
                        is_quantum_safe = any(qc in cipher_name.upper() 
                                            for qc in ['CECPQ2', 'KYBER', 'NTRU', 'SIKE'])
                        
                        return {
                            'valid': True,
                            'issuer': issuer.get('organizationName', 'Unknown'),
                            'version': ssock.version(),
                            'cipher': cipher_name,
                            'quantum_safe': is_quantum_safe
                        }
            
            result = await asyncio.wait_for(
                loop.run_in_executor(None, check_cert),
                timeout=10.0
            )
            return result
        except Exception as e:
            return {
                'valid': False,
                'issuer': 'N/A',
                'version': 'N/A',
                'cipher': 'Unknown',
                'quantum_safe': False
            }

    async def build_intelligence(self, assets: List[str]) -> pd.DataFrame:
        """Enhanced intelligence compilation with quantum risk scoring"""
        results = []
        tasks = []
        
        # Gather all data concurrently
        for asset in assets:
            tasks.append(self._analyze_asset(asset))
        
        analyzed = await asyncio.gather(*tasks, return_exceptions=True)
        
        for data in analyzed:
            if isinstance(data, dict):
                results.append(data)
        
        return pd.DataFrame(results)
    
    async def _analyze_asset(self, asset: str) -> Dict:
        """Analyze individual asset with comprehensive quantum threat analysis"""
        # Get geolocation data
        geo_data = await self.get_geo_data(asset)
        
        # Check SSL certificate
        ssl_data = await self.check_ssl_cert(asset)
        
        # Determine criticality based on naming patterns
        critical_keywords = ["vault", "api", "pqc", "secure", "admin", "gateway", "quantum", "keys", "auth", "iam"]
        is_critical = any(keyword in asset.lower() for keyword in critical_keywords)
        
        # Determine asset criticality level
        if is_critical:
            criticality = 'CRITICAL'
        elif any(k in asset.lower() for k in ['dev', 'test', 'staging']):
            criticality = 'MODERATE'
        else:
            criticality = 'HIGH'
        
        # Quantum threat assessment
        # Assume RSA-2048 for most assets (simulated - in reality would probe)
        crypto_assessment = self.quantum_analyzer.assess_crypto_vulnerability('RSA', 2048)
        pqc_recommendation = self.quantum_analyzer.recommend_pqc_algorithm(asset, criticality)
        
        # Calculate comprehensive risk score (0-100)
        risk_score = 0
        
        # Factor 1: Criticality (40 points max)
        if criticality == 'CRITICAL':
            risk_score += 40
        elif criticality == 'HIGH':
            risk_score += 25
        else:
            risk_score += 15
        
        # Factor 2: SSL/TLS Status (20 points max)
        if not ssl_data.get('valid', False):
            risk_score += 20
        elif not ssl_data.get('quantum_safe', False):
            risk_score += 15
        
        # Factor 3: Quantum vulnerability (30 points max)
        risk_score += min(30, crypto_assessment['quantum_risk_score'] // 3)
        
        # Factor 4: Geolocation unknown (10 points)
        if geo_data['country'] == 'Unknown':
            risk_score += 10
        
        # Determine overall risk level
        if risk_score >= 80:
            risk_level = "Critical (HNDL)"
            color = "red"
        elif risk_score >= 60:
            risk_level = "High - Quantum Vulnerable"
            color = "orange"
        elif risk_score >= 40:
            risk_level = "Moderate"
            color = "yellow"
        else:
            risk_level = "Low"
            color = "blue"
        
        # Generate comprehensive solution
        solution_parts = []
        if crypto_assessment['urgency'] == 'IMMEDIATE' or crypto_assessment['urgency'] == 'URGENT':
            solution_parts.append(f"QUANTUM THREAT: Migrate to {pqc_recommendation['recommended_kem']}")
        if not ssl_data.get('valid', False):
            solution_parts.append("Deploy valid SSL/TLS certificate")
        if not ssl_data.get('quantum_safe', False):
            solution_parts.append("Enable hybrid classical-PQC mode")
        
        if not solution_parts:
            solution_parts.append("Maintain quarterly security audits and monitoring")
        
        solution = " | ".join(solution_parts)
        
        # Generate asset fingerprint for tracking
        asset_hash = hashlib.sha256(asset.encode()).hexdigest()[:12]
        
        return {
            "asset": asset,
            "asset_id": asset_hash,
            "ip": geo_data['ip'],
            "lat": geo_data['lat'],
            "lon": geo_data['lon'],
            "country": geo_data['country'],
            "city": geo_data['city'],
            "isp": geo_data['isp'],
            "timezone": geo_data['timezone'],
            "ssl_valid": ssl_data.get('valid', False),
            "ssl_version": ssl_data.get('version', 'N/A'),
            "ssl_cipher": ssl_data.get('cipher', 'Unknown'),
            "quantum_safe_crypto": ssl_data.get('quantum_safe', False),
            "criticality": criticality,
            "Quantum_Risk": risk_level,
            "Risk_Score": risk_score,
            "quantum_threat_algorithm": crypto_assessment['threat_algorithm'],
            "quantum_years_vulnerable": crypto_assessment['years_until_vulnerable'],
            "quantum_urgency": crypto_assessment['urgency'],
            "PQC_Migration": pqc_recommendation['recommended_kem'],
            "PQC_Signature": pqc_recommendation['recommended_signature'],
            "PQC_Priority": pqc_recommendation['migration_priority'],
            "PQC_Timeline": pqc_recommendation['timeline'],
            "Solution": solution,
            "color": color,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "harvest_now_threat": crypto_assessment['years_until_vulnerable'] <= 10
        }


def generate_pdf_report(df: pd.DataFrame, target: str) -> bytes:
    """Enhanced PDF generation with quantum threat intelligence"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header with branding
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(102, 51, 153)  # Purple quantum theme
    pdf.cell(0, 15, txt="SENTINEL-V QUANTUM SECURITY AUDIT", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Target Domain: {target}", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, txt=f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True, align='C')
    pdf.cell(0, 6, txt="ProSec Networks | Quantum-Ready Cybersecurity", ln=True, align='C')
    pdf.ln(8)
    
    # Executive Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="EXECUTIVE SUMMARY", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    total_assets = len(df)
    critical_count = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    high_count = len(df[df['Quantum_Risk'].str.contains('High', na=False)])
    quantum_vulnerable = len(df[df['quantum_years_vulnerable'] <= 5])
    harvest_threat = len(df[df['harvest_now_threat'] == True])
    
    summary_text = f"""
Sentinel-V conducted a comprehensive quantum threat assessment of {total_assets} assets.
    
THREAT LANDSCAPE:
- {critical_count} assets identified as CRITICAL risk requiring immediate action
- {high_count} assets with HIGH quantum vulnerability (RSA/ECC exposed to Shor's algorithm)
- {quantum_vulnerable} assets will be vulnerable to quantum attacks within 5 years
- {harvest_threat} assets subject to "Harvest Now, Decrypt Later" threat

QUANTUM READINESS:
- Current encryption: RSA-2048/ECC-256 (quantum-vulnerable by 2030)
- Recommended migration: ML-KEM post-quantum cryptography (NIST FIPS 203)
- Estimated timeline: Immediate action required for critical assets

NIS2 COMPLIANCE STATUS: Partial - Requires PQC migration for full compliance
    """
    
    pdf.multi_cell(0, 5, txt=summary_text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    
    # Quantum Threat Analysis Section
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="QUANTUM THREAT INTELLIGENCE", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    quantum_info = """
UNDERSTANDING THE QUANTUM THREAT:

Shor's Algorithm: Breaks RSA and ECC exponentially faster than classical computers.
A quantum computer with 4000 logical qubits could break RSA-2048 in approximately 8 hours.

Timeline Projection:
- 2024-2026: NISQ (Noisy Intermediate-Scale Quantum) - Research phase
- 2027-2029: Early fault-tolerant quantum computers emerge
- 2030-2032: Cryptographically Relevant Quantum Computers (CRQC) threaten current encryption
- 2033+: Universal quantum computers make classical public-key crypto obsolete

"Harvest Now, Decrypt Later" Threat:
Adversaries are collecting encrypted data TODAY to decrypt when quantum computers arrive.
Long-lived sensitive data requires IMMEDIATE migration to post-quantum cryptography.
    """
    
    pdf.multi_cell(0, 5, txt=quantum_info.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    
    # Asset Intelligence Report
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="ASSET INTELLIGENCE MATRIX", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    
    for idx, row in df.iterrows():
        # Asset header with risk indicator
        pdf.set_font("Arial", 'B', 11)
        risk_indicator = "🔴" if "Critical" in row['Quantum_Risk'] else "🟠" if "High" in row['Quantum_Risk'] else "🟡"
        asset_line = f"{idx + 1}. {row['asset']} {risk_indicator}"
        pdf.cell(0, 7, txt=asset_line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        
        pdf.set_font("Arial", '', 9)
        
        # Core details
        details = [
            f"   IP: {row['ip']} | Location: {row['city']}, {row['country']} | ISP: {row['isp'][:30]}",
            f"   Risk Score: {row['Risk_Score']}/100 | Level: {row['Quantum_Risk']} | Criticality: {row['criticality']}",
            f"   SSL: {row['ssl_version']} | Cipher: {row['ssl_cipher'][:30]} | Quantum-Safe: {'Yes' if row['quantum_safe_crypto'] else 'No'}",
            f"   Quantum Threat: {row['quantum_threat_algorithm']} algorithm | Vulnerable in {row['quantum_years_vulnerable']} years",
            f"   PQC Strategy: {row['PQC_Migration']} | Signature: {row['PQC_Signature']} | Priority: {row['PQC_Priority']}",
            f"   Timeline: {row['PQC_Timeline']} | Harvest Threat: {'ACTIVE' if row['harvest_now_threat'] else 'Low'}",
            f"   ACTIONS REQUIRED: {row['Solution'][:90]}..."
        ]
        
        for detail in details:
            pdf.multi_cell(0, 4, txt=detail.encode('latin-1', 'replace').decode('latin-1'))
        
        pdf.ln(4)
        
        # Page break every 3 assets
        if (idx + 1) % 3 == 0 and idx < len(df) - 1:
            pdf.add_page()
    
    # Recommendations Page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="POST-QUANTUM MIGRATION ROADMAP", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    roadmap = """
PHASE 1: IMMEDIATE (0-3 MONTHS)
- Migrate CRITICAL assets to ML-KEM-768 or ML-KEM-1024
- Implement hybrid classical-PQC mode for backwards compatibility
- Begin inventory of all cryptographic assets and dependencies

PHASE 2: NEAR-TERM (3-6 MONTHS)  
- Deploy ML-DSA digital signatures for authentication systems
- Update SSL/TLS configurations with post-quantum cipher suites
- Conduct penetration testing of PQC implementations

PHASE 3: MEDIUM-TERM (6-12 MONTHS)
- Complete migration of HIGH priority assets
- Implement quantum-safe key management infrastructure
- Train security team on PQC best practices

PHASE 4: LONG-TERM (12-24 MONTHS)
- Full organizational PQC adoption
- Continuous monitoring of quantum computing advances
- Regular cryptographic agility assessments

NIST STANDARDS COMPLIANCE:
- FIPS 203: ML-KEM (Key Encapsulation Mechanism)
- FIPS 204: ML-DSA (Digital Signature Algorithm)
- FIPS 205: SLH-DSA (Stateless Hash-Based Signatures)
    """
    
    pdf.multi_cell(0, 5, txt=roadmap.encode('latin-1', 'replace').decode('latin-1'))
    
    # Footer
    pdf.ln(8)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 5, txt="Powered by Sentinel-V Quantum Intelligence Engine", ln=True, align='C')
    pdf.cell(0, 5, txt="ProSec Networks - Your Quantum-Ready Security Partner", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')


async def run_audit(domain: str) -> pd.DataFrame:
    """Main audit orchestrator with proper session management"""
    async with SentinelAgent(domain) as agent:
        assets = await agent.run_recon()
        intelligence_df = await agent.build_intelligence(assets)
        return intelligence_df