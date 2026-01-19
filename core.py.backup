import asyncio
import aiohttp
import socket
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import json
import ssl
import certifi

class SentinelAgent:
    def __init__(self, domain):
        self.domain = domain
        self.session = None
        
    async def __aenter__(self):
        """Context manager for proper session handling"""
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup session on exit"""
        if self.session:
            await self.session.close()

    async def get_geo_data(self, asset):
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
                                "ip": ip
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
                            "ip": ip
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
            "ip": "N/A"
        }

    async def run_recon(self):
        """Enhanced subdomain discovery with multiple sources"""
        discovered_assets = set()
        
        # Method 1: Certificate Transparency (crt.sh)
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            async with self.session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for entry in data[:50]:  # Limit to 50 entries
                        name = entry.get('name_value', '').lower()
                        # Clean up wildcard and multiline entries
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
            'pqc', 'quantum', 'shield', 'sentinel', 'monitor'
        ]
        
        for sub in common_subdomains:
            discovered_assets.add(f"{sub}.{self.domain}")
        
        # Always include the root domain
        discovered_assets.add(self.domain)
        
        # Return sorted list, limited to top 15 for demo
        return sorted(list(discovered_assets))[:15]

    async def check_ssl_cert(self, asset):
        """Check SSL certificate validity and strength"""
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            loop = asyncio.get_event_loop()
            
            def check_cert():
                with socket.create_connection((asset, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=asset) as ssock:
                        cert = ssock.getpeercert()
                        return {
                            'valid': True,
                            'issuer': dict(x[0] for x in cert.get('issuer', [])),
                            'version': ssock.version()
                        }
            
            result = await asyncio.wait_for(
                loop.run_in_executor(None, check_cert),
                timeout=10.0
            )
            return result
        except:
            return {'valid': False, 'issuer': {}, 'version': 'N/A'}

    async def build_intelligence(self, assets):
        """Enhanced intelligence compilation with risk scoring"""
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
    
    async def _analyze_asset(self, asset):
        """Analyze individual asset with comprehensive checks"""
        # Get geolocation data
        geo_data = await self.get_geo_data(asset)
        
        # Check SSL certificate
        ssl_data = await self.check_ssl_cert(asset)
        
        # Determine criticality based on naming patterns
        critical_keywords = ["vault", "api", "pqc", "secure", "admin", "gateway", "quantum"]
        is_critical = any(keyword in asset.lower() for keyword in critical_keywords)
        
        # Calculate risk score (0-100)
        risk_score = 0
        if is_critical:
            risk_score += 60
        if not ssl_data.get('valid', False):
            risk_score += 30
        if geo_data['country'] == 'Unknown':
            risk_score += 10
            
        # Determine risk level
        if risk_score >= 70:
            risk_level = "Critical (HNDL)"
            color = "red"
        elif risk_score >= 40:
            risk_level = "High"
            color = "orange"
        else:
            risk_level = "Moderate"
            color = "blue"
        
        # PQC Migration recommendation
        pqc_migration = "ML-KEM (FIPS 203)" if is_critical else "Standard TLS 1.3"
        
        # Solution recommendation
        if risk_score >= 70:
            solution = "URGENT: Deploy Lattice-based crypto + 24/7 monitoring"
        elif risk_score >= 40:
            solution = "Deploy PQC hybrid mode within 30 days"
        else:
            solution = "Maintain current security posture with quarterly audits"
        
        return {
            "asset": asset,
            "ip": geo_data['ip'],
            "lat": geo_data['lat'],
            "lon": geo_data['lon'],
            "country": geo_data['country'],
            "city": geo_data['city'],
            "isp": geo_data['isp'],
            "ssl_valid": ssl_data.get('valid', False),
            "ssl_version": ssl_data.get('version', 'N/A'),
            "Quantum_Risk": risk_level,
            "Risk_Score": risk_score,
            "PQC_Migration": pqc_migration,
            "Solution": solution,
            "color": color,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


def generate_pdf_report(df, target):
    """Enhanced PDF generation with better formatting and error handling"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 15, txt="SENTINEL-V SECURITY AUDIT", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Target: {target}", ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, txt=f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True, align='C')
    pdf.ln(5)
    
    # Executive Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Executive Summary", ln=True)
    pdf.set_font("Arial", '', 10)
    
    critical_count = len(df[df['Quantum_Risk'].str.contains('Critical', na=False)])
    high_count = len(df[df['Quantum_Risk'].str.contains('High', na=False)])
    total_assets = len(df)
    
    summary = f"Scanned {total_assets} assets. Found {critical_count} critical and {high_count} high-risk endpoints."
    pdf.multi_cell(0, 6, txt=summary.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)
    
    # Asset Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Asset Intelligence Report", ln=True)
    pdf.set_font("Arial", '', 9)
    
    for idx, row in df.iterrows():
        # Asset header
        pdf.set_font("Arial", 'B', 10)
        asset_line = f"{idx + 1}. {row['asset']}"
        pdf.cell(0, 6, txt=asset_line.encode('latin-1', 'replace').decode('latin-1'), ln=True)
        
        pdf.set_font("Arial", '', 9)
        
        # Details
        details = [
            f"   IP: {row['ip']} | Location: {row['city']}, {row['country']}",
            f"   Risk Level: {row['Quantum_Risk']} (Score: {row['Risk_Score']}/100)",
            f"   PQC Strategy: {row['PQC_Migration']}",
            f"   Action Required: {row['Solution']}"
        ]
        
        for detail in details:
            pdf.multi_cell(0, 5, txt=detail.encode('latin-1', 'replace').decode('latin-1'))
        
        pdf.ln(3)
    
    # Footer
    pdf.ln(5)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 5, txt="ProSec Networks - Quantum-Ready Cybersecurity Solutions", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')


# Utility function for session management
async def run_audit(domain):
    """Main audit orchestrator with proper session management"""
    async with SentinelAgent(domain) as agent:
        assets = await agent.run_recon()
        intelligence_df = await agent.build_intelligence(assets)
        return intelligence_df