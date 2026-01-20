"""
Sentinel-V Intelligence Engine with Quantum Threat Analysis
Complete core module with SCAN MODE SUPPORT
"""

import asyncio
import aiohttp
import socket
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import ssl
import certifi
from typing import Dict, List, Optional
import hashlib
import random


class ScanMode:
    """Scan mode configurations"""
    
    STANDARD = "Standard Recon"
    DEEP_QUANTUM = "Deep Quantum Analysis"
    STEALTH = "Stealth Mode"
    COMPREHENSIVE = "Comprehensive Audit"
    
    @staticmethod
    def get_config(mode: str) -> Dict:
        """Get configuration for each scan mode"""
        configs = {
            "Standard Recon": {
                "max_assets": 10,
                "enable_quantum": False,
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 0,
                "subdomain_sources": ["common"],
                "description": "Fast reconnaissance - basic asset discovery",
                "timeout": 10
            },
            "Deep Quantum Analysis": {
                "max_assets": 25,
                "enable_quantum": True,
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 0.5,
                "subdomain_sources": ["crt.sh", "common"],
                "description": "Full quantum threat assessment with PQC recommendations",
                "timeout": 30
            },
            "Stealth Mode": {
                "max_assets": 15,
                "enable_quantum": True,
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 3,  # Slow to avoid detection
                "subdomain_sources": ["common"],  # Passive only
                "description": "Low-profile scan with delays to avoid detection",
                "timeout": 20
            },
            "Comprehensive Audit": {
                "max_assets": 50,
                "enable_quantum": True,
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 0.25,
                "subdomain_sources": ["crt.sh", "common", "extended"],
                "description": "Full audit - recon + quantum + compliance + ISMS",
                "timeout": 45
            }
        }
        return configs.get(mode, configs["Standard Recon"])


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
        
        if key_size >= 1024:
            crypto_category = 'RSA'
        else:
            crypto_category = crypto_type
        
        threat_info = vulnerability_map.get(crypto_category, vulnerability_map['RSA'])
        years_until_vulnerable = max(0, threat_info['vulnerability_year'] - current_year)
        
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
    
    def __init__(self, domain: str, scan_mode: str = "Deep Quantum Analysis"):
        self.domain = domain
        self.session = None
        self.scan_mode = scan_mode
        self.config = ScanMode.get_config(scan_mode)
        self.quantum_analyzer = QuantumThreatAnalyzer() if self.config['enable_quantum'] else None
        
    async def __aenter__(self):
        """Context manager for proper session handling"""
        timeout = aiohttp.ClientTimeout(total=self.config['timeout'])
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        self.session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup session on exit"""
        if self.session:
            await self.session.close()
            await asyncio.sleep(0.25)

    async def get_geo_data(self, asset: str) -> Dict:
        """Enhanced geolocation with fallback and error handling"""
        if not self.config['enable_geo']:
            return self._default_geo()
            
        try:
            loop = asyncio.get_event_loop()
            ip = await asyncio.wait_for(
                loop.run_in_executor(None, socket.gethostbyname, asset),
                timeout=5.0
            )
            
            # Add stealth delay if configured
            if self.config['delay_between_requests'] > 0:
                await asyncio.sleep(self.config['delay_between_requests'])
            
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
        
        return self._default_geo()
    
    def _default_geo(self) -> Dict:
        """Return default geo data"""
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
        """Enhanced subdomain discovery based on scan mode"""
        discovered_assets = set()
        sources = self.config['subdomain_sources']
        
        # Method 1: Certificate Transparency (crt.sh) - if enabled
        if "crt.sh" in sources:
            try:
                if self.config['delay_between_requests'] > 0:
                    await asyncio.sleep(self.config['delay_between_requests'])
                    
                url = f"https://crt.sh/?q=%.{self.domain}&output=json"
                async with self.session.get(url, timeout=15) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for entry in data[:100]:
                            name = entry.get('name_value', '').lower()
                            for subdomain in name.split('\n'):
                                subdomain = subdomain.strip().replace('*.', '')
                                if subdomain and self.domain in subdomain:
                                    discovered_assets.add(subdomain)
            except Exception as e:
                print(f"crt.sh lookup failed: {str(e)}")
        
        # Method 2: Common subdomains
        if "common" in sources:
            common_subdomains = [
                'www', 'mail', 'remote', 'blog', 'webmail', 'server',
                'ns1', 'ns2', 'smtp', 'secure', 'vpn', 'api', 'vault',
                'admin', 'dev', 'staging', 'test', 'portal', 'gateway',
                'pqc', 'quantum', 'shield', 'sentinel', 'monitor',
                'auth', 'sso', 'identity', 'iam', 'keys', 'crypto'
            ]
            for sub in common_subdomains:
                discovered_assets.add(f"{sub}.{self.domain}")
        
        # Method 3: Extended subdomains (Comprehensive only)
        if "extended" in sources:
            extended_subdomains = [
                'internal', 'external', 'public', 'private', 'prod',
                'backup', 'db', 'database', 'mysql', 'postgres', 'redis',
                'elk', 'kibana', 'grafana', 'prometheus', 'jenkins',
                'gitlab', 'github', 'bitbucket', 'docker', 'k8s',
                'aws', 'azure', 'gcp', 'cloud', 'cdn', 'static',
                'img', 'images', 'assets', 'media', 'video', 'files',
                'app', 'mobile', 'ios', 'android', 'web', 'frontend',
                'backend', 'api-v1', 'api-v2', 'graphql', 'rest'
            ]
            for sub in extended_subdomains:
                discovered_assets.add(f"{sub}.{self.domain}")
        
        # Always include root domain
        discovered_assets.add(self.domain)
        
        # Limit based on scan mode
        max_assets = self.config['max_assets']
        return sorted(list(discovered_assets))[:max_assets]

    async def check_ssl_cert(self, asset: str) -> Dict:
        """Check SSL certificate validity, strength, and quantum readiness"""
        if not self.config['enable_ssl_check']:
            return {'valid': False, 'issuer': 'N/A', 'version': 'N/A', 'cipher': 'Unknown', 'quantum_safe': False}
            
        try:
            # Add stealth delay if configured
            if self.config['delay_between_requests'] > 0:
                await asyncio.sleep(self.config['delay_between_requests'])
                
            context = ssl.create_default_context(cafile=certifi.where())
            loop = asyncio.get_event_loop()
            
            def check_cert():
                with socket.create_connection((asset, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=asset) as ssock:
                        cert = ssock.getpeercert()
                        cipher = ssock.cipher()
                        issuer = dict(x[0] for x in cert.get('issuer', []))
                        cipher_name = cipher[0] if cipher else 'Unknown'
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

    async def build_intelligence(self, assets: List[str], progress_callback=None) -> pd.DataFrame:
        """Enhanced intelligence compilation with progress tracking"""
        results = []
        total = len(assets)
        
        for idx, asset in enumerate(assets):
            try:
                data = await self._analyze_asset(asset)
                if isinstance(data, dict):
                    results.append(data)
                    
                # Progress callback
                if progress_callback:
                    progress_callback(idx + 1, total, asset)
                    
            except Exception as e:
                print(f"Error analyzing {asset}: {e}")
        
        return pd.DataFrame(results)
    
    async def _analyze_asset(self, asset: str) -> Dict:
        """Analyze individual asset with comprehensive quantum threat analysis"""
        # Get geolocation data
        geo_data = await self.get_geo_data(asset)
        
        # Check SSL certificate
        ssl_data = await self.check_ssl_cert(asset)
        
        # Determine criticality based on naming patterns
        critical_keywords = ["vault", "api", "pqc", "secure", "admin", "gateway", "quantum", "keys", "auth", "iam", "sso", "identity"]
        is_critical = any(keyword in asset.lower() for keyword in critical_keywords)
        
        if is_critical:
            criticality = 'CRITICAL'
        elif any(k in asset.lower() for k in ['dev', 'test', 'staging']):
            criticality = 'MODERATE'
        else:
            criticality = 'HIGH'
        
        # Quantum threat assessment (if enabled)
        if self.quantum_analyzer:
            crypto_assessment = self.quantum_analyzer.assess_crypto_vulnerability('RSA', 2048)
            pqc_recommendation = self.quantum_analyzer.recommend_pqc_algorithm(asset, criticality)
        else:
            # Basic assessment without quantum analysis
            crypto_assessment = {
                'threat_algorithm': 'N/A',
                'years_until_vulnerable': 10,
                'urgency': 'MONITOR',
                'quantum_risk_score': 30
            }
            pqc_recommendation = {
                'recommended_kem': 'N/A',
                'recommended_signature': 'N/A',
                'migration_priority': 'N/A',
                'timeline': 'N/A'
            }
        
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
        
        # Factor 3: Quantum vulnerability (30 points max) - only if quantum enabled
        if self.config['enable_quantum']:
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
        
        # Generate solution
        solution_parts = []
        if self.config['enable_quantum'] and (crypto_assessment['urgency'] == 'IMMEDIATE' or crypto_assessment['urgency'] == 'URGENT'):
            solution_parts.append(f"QUANTUM THREAT: Migrate to {pqc_recommendation['recommended_kem']}")
        if not ssl_data.get('valid', False):
            solution_parts.append("Deploy valid SSL/TLS certificate")
        if self.config['enable_quantum'] and not ssl_data.get('quantum_safe', False):
            solution_parts.append("Enable hybrid classical-PQC mode")
        
        if not solution_parts:
            solution_parts.append("Maintain quarterly security audits and monitoring")
        
        solution = " | ".join(solution_parts)
        
        # Generate asset fingerprint
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
            "harvest_now_threat": crypto_assessment['years_until_vulnerable'] <= 10,
            "scan_mode": self.scan_mode
        }


def generate_pdf_report(df: pd.DataFrame, target: str, scan_mode: str = "Deep Quantum Analysis") -> bytes:
    """Enhanced PDF generation with quantum threat intelligence"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header with branding
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 15, txt="SENTINEL-V QUANTUM SECURITY AUDIT", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Target Domain: {target}", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, txt=f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True, align='C')
    pdf.cell(0, 6, txt=f"Scan Mode: {scan_mode}", ln=True, align='C')
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
Sentinel-V conducted a {scan_mode} assessment of {total_assets} assets.
    
THREAT LANDSCAPE:
- {critical_count} assets identified as CRITICAL risk requiring immediate action
- {high_count} assets with HIGH quantum vulnerability
- {quantum_vulnerable} assets will be vulnerable to quantum attacks within 5 years
- {harvest_threat} assets subject to "Harvest Now, Decrypt Later" threat

QUANTUM READINESS:
- Current encryption: RSA-2048/ECC-256 (quantum-vulnerable by 2030)
- Recommended migration: ML-KEM post-quantum cryptography (NIST FIPS 203)
- Estimated timeline: Immediate action required for critical assets
    """
    
    pdf.multi_cell(0, 5, txt=summary_text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    
    # Asset Intelligence Report
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="ASSET INTELLIGENCE MATRIX", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    
    for idx, row in df.iterrows():
        pdf.set_font("Arial", 'B', 11)
        risk_indicator = "[!]" if "Critical" in row['Quantum_Risk'] else "[*]" if "High" in row['Quantum_Risk'] else "[-]"
        asset_line = f"{idx + 1}. {risk_indicator} {row['asset']}"
        pdf.cell(0, 7, txt=asset_line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        
        pdf.set_font("Arial", '', 9)
        
        details = [
            f"   IP: {row['ip']} | Location: {row['city']}, {row['country']}",
            f"   Risk Score: {row['Risk_Score']}/100 | Level: {row['Quantum_Risk']}",
            f"   SSL: {row['ssl_version']} | Quantum-Safe: {'Yes' if row['quantum_safe_crypto'] else 'No'}",
            f"   PQC Strategy: {row['PQC_Migration']} | Priority: {row['PQC_Priority']}",
            f"   ACTION: {row['Solution'][:80]}..."
        ]
        
        for detail in details:
            pdf.multi_cell(0, 4, txt=detail.encode('latin-1', 'replace').decode('latin-1'))
        
        pdf.ln(3)
        
        if (idx + 1) % 4 == 0 and idx < len(df) - 1:
            pdf.add_page()
    
    # Footer
    pdf.ln(8)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 5, txt="Powered by Sentinel-V Quantum Intelligence Engine", ln=True, align='C')
    pdf.cell(0, 5, txt="ProSec Networks - Your Quantum-Ready Security Partner", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')


async def run_audit(domain: str, scan_mode: str = "Deep Quantum Analysis", progress_callback=None) -> pd.DataFrame:
    """Main audit orchestrator with scan mode support"""
    async with SentinelAgent(domain, scan_mode) as agent:
        assets = await agent.run_recon()
        intelligence_df = await agent.build_intelligence(assets, progress_callback)
        return intelligence_df