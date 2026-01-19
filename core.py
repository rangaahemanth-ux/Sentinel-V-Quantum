import asyncio
import aiohttp

class Scanner:
    def __init__(self, domain):
        self.domain = domain

    async def get_subdomains(self):
        url = f"https://crt.sh/?q={self.domain}&output=json"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=12) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return sorted(list(set(e['name_value'].lower() for e in data)))
            except Exception:
                return [f"www.{self.domain}"]
        return []

    def calculate_risk(self, asset):
        """Classical Risk Analysis (NIS2 Article 21)"""
        score = 15 
        findings = []
        if any(x in asset for x in ["api", "vpn", "gateway"]):
            score += 35
            findings.append("Critical Entry Point")
        if any(x in asset for x in ["dev", "test", "staging"]):
            score += 45
            findings.append("Unsecured Environment")
        
        return {
            "asset": asset, # CRITICAL: Required for merge
            "Classical_Risk": min(score, 100),
            "status": "Healthy" if score < 40 else "Warning",
            "risks": ", ".join(findings) if findings else "Compliant"
        }

    def analyze_quantum_risk(self, asset):
        """Quantum Exposure Layer (HNDL Threat)"""
        q_score = 25
        if any(x in asset for x in ["vault", "secure", "auth", "key"]):
            q_score = 90
            q_status = "High Risk (HNDL Target)"
        else:
            q_status = "Standard Risk"
            
        return {
            "asset": asset, # CRITICAL: Required for merge
            "Quantum_Risk": q_score,
            "Quantum_Status": q_status,
            "Recommendation": "Post-Quantum Cryptography" if q_score > 50 else "Monitor"
        }