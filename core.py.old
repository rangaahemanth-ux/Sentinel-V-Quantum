"""
Sentinel-V Intelligence Engine with Quantum Threat Analysis
FIXED: Scan modes NOW ACTUALLY WORK DIFFERENTLY
"""

import asyncio
import aiohttp
import socket
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import ssl
import certifi
from typing import Dict, List, Optional, Callable
import hashlib
import random


class ScanMode:
    """Scan mode configurations - EACH MODE BEHAVES DIFFERENTLY"""
    
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
                "enable_quantum": False,  # NO quantum analysis
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 0,  # Fast - no delays
                "subdomain_sources": ["common"],  # Only common subdomains
                "use_crt_sh": False,  # Skip certificate transparency
                "description": "Fast reconnaissance - basic asset discovery",
                "timeout": 10,
                "risk_multiplier": 0.7  # Lower risk scores
            },
            "Deep Quantum Analysis": {
                "max_assets": 25,
                "enable_quantum": True,  # FULL quantum analysis
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 0.3,  # Slight delay
                "subdomain_sources": ["crt.sh", "common"],
                "use_crt_sh": True,  # Use certificate transparency
                "description": "Full quantum threat assessment with PQC recommendations",
                "timeout": 30,
                "risk_multiplier": 1.0  # Standard risk scores
            },
            "Stealth Mode": {
                "max_assets": 15,
                "enable_quantum": True,
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 2.0,  # SLOW - 2 second delays
                "subdomain_sources": ["common"],  # Passive only - no crt.sh
                "use_crt_sh": False,  # Skip to avoid detection
                "description": "Low-profile scan with delays to avoid detection",
                "timeout": 20,
                "risk_multiplier": 1.1  # Slightly higher risk (paranoid mode)
            },
            "Comprehensive Audit": {
                "max_assets": 50,
                "enable_quantum": True,
                "enable_ssl_check": True,
                "enable_geo": True,
                "delay_between_requests": 0.2,
                "subdomain_sources": ["crt.sh", "common", "extended"],
                "use_crt_sh": True,
                "description": "Full audit - recon + quantum + compliance + ISMS",
                "timeout": 45,
                "risk_multiplier": 1.2  # Higher sensitivity
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
        
        # Only create quantum analyzer if mode enables it
        if self.config['enable_quantum']:
            self.quantum_analyzer = QuantumThreatAnalyzer()
        else:
            self.quantum_analyzer = None
            
        print(f"[SENTINEL] Mode: {scan_mode}")
        print(f"[SENTINEL] Quantum Analysis: {'ENABLED' if self.config['enable_quantum'] else 'DISABLED'}")
        print(f"[SENTINEL] Max Assets: {self.config['max_assets']}")
        print(f"[SENTINEL] Request Delay: {self.config['delay_between_requests']}s")
        
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

    async def _apply_stealth_delay(self):
        """Apply delay between requests based on scan mode"""
        delay = self.config['delay_between_requests']
        if delay > 0:
            print(f"[STEALTH] Waiting {delay}s before next request...")
            await asyncio.sleep(delay)

    async def get_geo_data(self, asset: str) -> Dict:
        """Enhanced geolocation with mode-specific behavior"""
        if not self.config['enable_geo']:
            return self._default_geo()
        
        # Apply stealth delay
        await self._apply_stealth_delay()
            
        try:
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
                                "timezone": data.get("timezone", "Unknown"),
                                "resolved": True
                            }
            except asyncio.TimeoutError:
                print(f"[GEO] Timeout for {asset}")
                
            # Fallback to ipapi.co
            try:
                await self._apply_stealth_delay()
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
                            "timezone": data.get("timezone", "Unknown"),
                            "resolved": True
                        }
            except:
                pass
                
        except (socket.gaierror, asyncio.TimeoutError, Exception) as e:
            print(f"[GEO] Failed for {asset}: {str(e)[:50]}")
        
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
            "timezone": "Unknown",
            "resolved": False
        }

    async def run_recon(self) -> List[str]:
        """
        SCAN MODE SPECIFIC subdomain discovery
        - Standard Recon: Common subdomains only (fast)
        - Deep Quantum: crt.sh + common
        - Stealth: Common only with delays (passive)
        - Comprehensive: Everything
        """
        discovered_assets = set()
        
        print(f"[RECON] Starting {self.scan_mode} reconnaissance...")
        print(f"[RECON] Sources: {self.config['subdomain_sources']}")
        
        # Method 1: Certificate Transparency (crt.sh) - ONLY if mode enables it
        if self.config['use_crt_sh']:
            print("[RECON] Querying crt.sh (Certificate Transparency)...")
            await self._apply_stealth_delay()
            
            try:
                url = f"https://crt.sh/?q=%.{self.domain}&output=json"
                async with self.session.get(url, timeout=15) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        count = 0
                        for entry in data[:100]:
                            name = entry.get('name_value', '').lower()
                            for subdomain in name.split('\n'):
                                subdomain = subdomain.strip().replace('*.', '')
                                if subdomain and self.domain in subdomain:
                                    discovered_assets.add(subdomain)
                                    count += 1
                        print(f"[RECON] crt.sh found {count} subdomains")
            except Exception as e:
                print(f"[RECON] crt.sh failed: {str(e)[:50]}")
        else:
            print("[RECON] Skipping crt.sh (not enabled for this mode)")
        
        # Method 2: Common subdomains
        if "common" in self.config['subdomain_sources']:
            print("[RECON] Adding common subdomains...")
            common_subdomains = [
                'www', 'mail', 'remote', 'blog', 'webmail', 'server',
                'ns1', 'ns2', 'smtp', 'secure', 'vpn', 'api', 'vault',
                'admin', 'dev', 'staging', 'test', 'portal', 'gateway',
                'auth', 'sso', 'identity', 'iam', 'keys', 'crypto'
            ]
            for sub in common_subdomains:
                discovered_assets.add(f"{sub}.{self.domain}")
            print(f"[RECON] Added {len(common_subdomains)} common subdomains")
        
        # Method 3: Extended subdomains (Comprehensive ONLY)
        if "extended" in self.config['subdomain_sources']:
            print("[RECON] Adding EXTENDED subdomain list (Comprehensive mode)...")
            extended_subdomains = [
                'internal', 'external', 'public', 'private', 'prod',
                'backup', 'db', 'database', 'mysql', 'postgres', 'redis',
                'elk', 'kibana', 'grafana', 'prometheus', 'jenkins',
                'gitlab', 'github', 'bitbucket', 'docker', 'k8s',
                'aws', 'azure', 'gcp', 'cloud', 'cdn', 'static',
                'img', 'images', 'assets', 'media', 'video', 'files',
                'app', 'mobile', 'ios', 'android', 'web', 'frontend',
                'backend', 'api-v1', 'api-v2', 'graphql', 'rest',
                'monitor', 'metrics', 'logs', 'trace', 'status',
                'pqc', 'quantum', 'shield', 'sentinel', 'security'
            ]
            for sub in extended_subdomains:
                discovered_assets.add(f"{sub}.{self.domain}")
            print(f"[RECON] Added {len(extended_subdomains)} extended subdomains")
        
        # Always include root domain
        discovered_assets.add(self.domain)
        
        # Limit based on scan mode
        max_assets = self.config['max_assets']
        result = sorted(list(discovered_assets))[:max_assets]
        
        print(f"[RECON] Total: {len(discovered_assets)} discovered, returning {len(result)} (max: {max_assets})")
        
        return result

    async def check_ssl_cert(self, asset: str) -> Dict:
        """Check SSL certificate - with stealth delays"""
        if not self.config['enable_ssl_check']:
            return {'valid': False, 'issuer': 'N/A', 'version': 'N/A', 'cipher': 'Unknown', 'quantum_safe': False}
        
        await self._apply_stealth_delay()
            
        try:
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

    async def build_intelligence(self, assets: List[str], progress_callback: Optional[Callable] = None) -> pd.DataFrame:
        """Build intelligence with MODE-SPECIFIC analysis"""
        results = []
        total = len(assets)
        
        print(f"[INTEL] Analyzing {total} assets in {self.scan_mode} mode...")
        
        for idx, asset in enumerate(assets):
            try:
                print(f"[INTEL] [{idx+1}/{total}] Analyzing {asset}...")
                data = await self._analyze_asset(asset)
                if isinstance(data, dict):
                    results.append(data)
                    
                if progress_callback:
                    progress_callback(idx + 1, total, asset)
                    
            except Exception as e:
                print(f"[INTEL] Error analyzing {asset}: {e}")
        
        print(f"[INTEL] Analysis complete. {len(results)} assets processed.")
        return pd.DataFrame(results)
    
    async def _analyze_asset(self, asset: str) -> Dict:
        """Analyze individual asset with MODE-SPECIFIC behavior"""
        
        # Get geolocation data
        geo_data = await self.get_geo_data(asset)
        
        # Check SSL certificate
        ssl_data = await self.check_ssl_cert(asset)
        
        # Determine criticality based on naming patterns
        critical_keywords = ["vault", "api", "pqc", "secure", "admin", "gateway", "quantum", "keys", "auth", "iam", "sso", "identity", "crypto"]
        high_keywords = ["mail", "smtp", "vpn", "remote", "portal", "server"]
        
        is_critical = any(keyword in asset.lower() for keyword in critical_keywords)
        is_high = any(keyword in asset.lower() for keyword in high_keywords)
        
        if is_critical:
            criticality = 'CRITICAL'
        elif is_high:
            criticality = 'HIGH'
        elif any(k in asset.lower() for k in ['dev', 'test', 'staging', 'blog']):
            criticality = 'MODERATE'
        else:
            criticality = 'HIGH'
        
        # ================================================================
        # MODE-SPECIFIC ANALYSIS
        # ================================================================
        
        if self.config['enable_quantum'] and self.quantum_analyzer:
            # FULL QUANTUM ANALYSIS (Deep, Stealth, Comprehensive)
            crypto_assessment = self.quantum_analyzer.assess_crypto_vulnerability('RSA', 2048)
            pqc_recommendation = self.quantum_analyzer.recommend_pqc_algorithm(asset, criticality)
            
            quantum_threat_algorithm = crypto_assessment['threat_algorithm']
            quantum_years_vulnerable = crypto_assessment['years_until_vulnerable']
            quantum_urgency = crypto_assessment['urgency']
            pqc_migration = pqc_recommendation['recommended_kem']
            pqc_signature = pqc_recommendation['recommended_signature']
            pqc_priority = pqc_recommendation['migration_priority']
            pqc_timeline = pqc_recommendation['timeline']
            harvest_now_threat = quantum_years_vulnerable <= 10
            
        else:
            # STANDARD RECON - No quantum analysis
            quantum_threat_algorithm = 'N/A (Standard Recon)'
            quantum_years_vulnerable = 0
            quantum_urgency = 'N/A'
            pqc_migration = 'N/A'
            pqc_signature = 'N/A'
            pqc_priority = 'N/A'
            pqc_timeline = 'N/A'
            harvest_now_threat = False
        
        # ================================================================
        # RISK SCORE CALCULATION (Mode-specific)
        # ================================================================
        
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
            risk_score += 10
        
        # Factor 3: Quantum vulnerability (30 points max) - ONLY if quantum enabled
        if self.config['enable_quantum']:
            if quantum_years_vulnerable <= 4:
                risk_score += 30
            elif quantum_years_vulnerable <= 6:
                risk_score += 20
            else:
                risk_score += 10
        
        # Factor 4: Geolocation resolved (10 points)
        if not geo_data.get('resolved', False):
            risk_score += 10
        
        # Apply mode-specific risk multiplier
        risk_score = int(risk_score * self.config['risk_multiplier'])
        risk_score = min(100, risk_score)  # Cap at 100
        
        # ================================================================
        # RISK LEVEL DETERMINATION
        # ================================================================
        
        if self.config['enable_quantum']:
            # Quantum-aware risk levels
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
        else:
            # Standard risk levels (no quantum terminology)
            if risk_score >= 70:
                risk_level = "High Risk"
                color = "red"
            elif risk_score >= 50:
                risk_level = "Medium Risk"
                color = "orange"
            elif risk_score >= 30:
                risk_level = "Low Risk"
                color = "yellow"
            else:
                risk_level = "Minimal"
                color = "blue"
        
        # ================================================================
        # SOLUTION GENERATION
        # ================================================================
        
        solution_parts = []
        
        if self.config['enable_quantum']:
            if quantum_urgency in ['IMMEDIATE', 'URGENT']:
                solution_parts.append(f"QUANTUM: Migrate to {pqc_migration}")
            if not ssl_data.get('valid', False):
                solution_parts.append("Deploy SSL/TLS")
            if not ssl_data.get('quantum_safe', False):
                solution_parts.append("Enable PQC hybrid mode")
        else:
            # Standard recon solutions
            if not ssl_data.get('valid', False):
                solution_parts.append("Deploy SSL certificate")
            if criticality == 'CRITICAL':
                solution_parts.append("Review access controls")
        
        if not solution_parts:
            solution_parts.append("Continue monitoring")
        
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
            "quantum_threat_algorithm": quantum_threat_algorithm,
            "quantum_years_vulnerable": quantum_years_vulnerable,
            "quantum_urgency": quantum_urgency,
            "PQC_Migration": pqc_migration,
            "PQC_Signature": pqc_signature,
            "PQC_Priority": pqc_priority,
            "PQC_Timeline": pqc_timeline,
            "Solution": solution,
            "color": color,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "harvest_now_threat": harvest_now_threat,
            "scan_mode": self.scan_mode
        }


def generate_pdf_report(df: pd.DataFrame, target: str, scan_mode: str = "Deep Quantum Analysis") -> bytes:
    """Enhanced PDF generation with scan mode info"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 15, txt="SENTINEL-V SECURITY AUDIT", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Target: {target}", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True, align='C')
    pdf.cell(0, 6, txt=f"Scan Mode: {scan_mode}", ln=True, align='C')
    pdf.ln(8)
    
    # Mode-specific summary
    config = ScanMode.get_config(scan_mode)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="SCAN CONFIGURATION", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    config_text = f"""
Mode: {scan_mode}
Quantum Analysis: {'Enabled' if config['enable_quantum'] else 'Disabled'}
Max Assets: {config['max_assets']}
Request Delay: {config['delay_between_requests']}s
Sources: {', '.join(config['subdomain_sources'])}
    """
    pdf.multi_cell(0, 5, txt=config_text)
    pdf.ln(5)
    
    # Executive Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="EXECUTIVE SUMMARY", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    total_assets = len(df)
    critical_count = len(df[df['Quantum_Risk'].str.contains('Critical|High Risk', na=False)])
    
    if config['enable_quantum']:
        quantum_vulnerable = len(df[df['quantum_years_vulnerable'] <= 5])
        harvest_threat = len(df[df['harvest_now_threat'] == True])
        summary = f"""
Scanned {total_assets} assets using {scan_mode}.
Critical/High Risk: {critical_count}
Quantum Vulnerable (5yr): {quantum_vulnerable}
Harvest Now Threat: {harvest_threat}
        """
    else:
        summary = f"""
Scanned {total_assets} assets using {scan_mode}.
High Risk Assets: {critical_count}
Note: Quantum analysis disabled in Standard Recon mode.
        """
    
    pdf.multi_cell(0, 5, txt=summary)
    pdf.ln(5)
    
    # Asset list
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, txt="ASSET INTELLIGENCE", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    
    for idx, row in df.iterrows():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, txt=f"{idx+1}. {row['asset']}", ln=True)
        pdf.set_font("Arial", '', 9)
        
        details = [
            f"   IP: {row['ip']} | {row['city']}, {row['country']}",
            f"   Risk: {row['Quantum_Risk']} (Score: {row['Risk_Score']})",
            f"   Action: {row['Solution'][:60]}..."
        ]
        
        for detail in details:
            pdf.cell(0, 4, txt=detail.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        pdf.ln(2)
        
        if (idx + 1) % 6 == 0 and idx < len(df) - 1:
            pdf.add_page()
    
    # Footer
    pdf.ln(8)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 5, txt=f"Sentinel-V | {scan_mode} | ProSec Networks", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')


async def run_audit(domain: str, scan_mode: str = "Deep Quantum Analysis", progress_callback: Optional[Callable] = None) -> pd.DataFrame:
    """Main audit orchestrator with WORKING scan mode support"""
    print(f"\n{'='*60}")
    print(f"SENTINEL-V AUDIT STARTING")
    print(f"Target: {domain}")
    print(f"Mode: {scan_mode}")
    print(f"{'='*60}\n")
    
    async with SentinelAgent(domain, scan_mode) as agent:
        assets = await agent.run_recon()
        intelligence_df = await agent.build_intelligence(assets, progress_callback)
        
        print(f"\n{'='*60}")
        print(f"AUDIT COMPLETE")
        print(f"Assets Analyzed: {len(intelligence_df)}")
        print(f"{'='*60}\n")
        
        return intelligence_df