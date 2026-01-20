"""
Sentinel-V ISMS Framework Generator
Auto-generates ISO 27001, BSI IT-Grundschutz, and NIS2 compliance frameworks
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import json
from fpdf import FPDF
from isms_templates import ISMSTemplates


class ISMSFrameworkGenerator:
    """Autonomous ISMS framework generator for ProSec Networks"""
    
    def __init__(self, scan_results: pd.DataFrame, target_domain: str):
        self.df = scan_results
        self.domain = target_domain
        self.industry = self._detect_industry()
        self.company_size = self._estimate_company_size()
        
        # Load industry templates
        self.industry_profile = ISMSTemplates.get_industry_profile(self.industry)
        self.compliance_requirements = self.industry_profile['compliance_frameworks']
        
    def _detect_industry(self) -> str:
        """Detect industry from domain"""
        d = self.domain.lower()
        industries = {
            'finance': ['bank', 'finanz', 'invest', 'capital', 'payment'],
            'healthcare': ['health', 'medical', 'hospital', 'pharma'],
            'manufacturing': ['industrie', 'manufacturing', 'factory'],
            'energy': ['energy', 'power', 'electric', 'gas'],
            'government': ['gov', 'stadt', 'kommune', 'behörde']
        }
        for ind, kws in industries.items():
            if any(k in d for k in kws):
                return ind
        return 'general'
    
    def _estimate_company_size(self) -> str:
        """Estimate size from asset count"""
        count = len(self.df)
        if count >= 50: return 'large'
        elif count >= 20: return 'medium'
        return 'small'
    
    def generate_iso27001_soa(self) -> Dict:
        """Generate ISO 27001 Statement of Applicability"""
        critical = len(self.df[self.df['Quantum_Risk'].str.contains('Critical', na=False)])
        qv = len(self.df[self.df['quantum_years_vulnerable'] <= 5])
        
        controls = {
            'A.5 Information Security Policies': {
                'status': 'Required', 'priority': 'P0',
                'implementation': 'Define quantum-aware security policies',
                'quantum': 'Include PQC migration policy'
            },
            'A.8 Asset Management': {
                'status': 'Implemented', 'priority': 'P0',
                'implementation': f'{len(self.df)} assets discovered',
                'quantum': 'Quantum vulnerability per asset'
            },
            'A.10 Cryptography': {
                'status': 'Critical', 'priority': 'P0',
                'implementation': f'{qv} assets need PQC migration',
                'quantum': 'ML-KEM/ML-DSA (FIPS 203/204)'
            },
            'A.13 Communications Security': {
                'status': 'Critical', 'priority': 'P0',
                'implementation': 'Upgrade to quantum-safe TLS',
                'quantum': 'Hybrid classical-PQC ciphers'
            },
            'A.16 Incident Management': {
                'status': 'Required', 'priority': 'P0',
                'implementation': 'Quantum breach response',
                'quantum': 'Quantum incident playbooks'
            }
        }
        
        return {
            'document': 'ISO 27001 SoA',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'scope': f'{self.domain} - {self.industry.title()}',
            'controls': controls,
            'critical_controls': sum(1 for c in controls.values() if c['priority'] == 'P0')
        }
    
    def generate_bsi_grundschutz(self) -> Dict:
        """Generate BSI IT-Grundschutz mapping"""
        bausteine = {
            'ISMS.1 Sicherheitsmanagement': {
                'priority': 'P0',
                'implementation': 'Quantum-aware ISMS',
                'quantum': 'Quantum threat in risk assessment'
            },
            'CON.1 Kryptokonzept': {
                'priority': 'P0',
                'implementation': 'Quantum-safe crypto concept',
                'quantum': 'ML-KEM, ML-DSA, SLH-DSA (NIST FIPS)'
            },
            'DER.1 Detektion': {
                'priority': 'P0',
                'implementation': 'SIEM for quantum threats',
                'quantum': 'Harvest-now-decrypt-later signatures'
            }
        }
        
        return {
            'framework': 'BSI IT-Grundschutz',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'bausteine': bausteine,
            'iso27001_compatible': True
        }
    
    def generate_nis2_compliance(self) -> Dict:
        """Generate NIS2 Article 21 compliance"""
        critical = len(self.df[self.df['Quantum_Risk'].str.contains('Critical', na=False)])
        
        requirements = {
            'Risk Management': {
                'status': 'Partial',
                'gap': 'Continuous quantum monitoring needed',
                'priority': 'P0'
            },
            'Incident Handling': {
                'status': 'Required',
                'gap': 'Quantum incident playbooks',
                'priority': 'P0'
            },
            'Cryptographic Controls': {
                'status': 'Critical',
                'gap': f'{critical} assets need urgent PQC',
                'priority': 'P0'
            }
        }
        
        return {
            'regulation': 'NIS2 Article 21',
            'entity_type': 'Essential' if self.industry in ['energy', 'finance'] else 'Important',
            'requirements': requirements,
            'critical_gaps': sum(1 for r in requirements.values() if r['status'] == 'Critical')
        }
    
    def generate_roadmap(self) -> Dict:
        """Generate implementation roadmap"""
        start = datetime.now()
        
        # Use template-based phases
        phase_templates = ISMSTemplates.get_implementation_phases_template(
            self.industry, 
            self.company_size
        )
        
        phases = []
        budget_ranges = [
            '€80K-120K', '€60K-100K', '€50K-80K', '€40K-70K'
        ]
        
        for i, template in enumerate(phase_templates):
            phases.append({
                'phase': f"Phase {template['number']}: {template['name']}",
                'months': template['months'],
                'budget': budget_ranges[i] if i < len(budget_ranges) else '€30K-50K',
                'milestones': template['key_deliverables']
            })
        
        return {
            'timeline_months': sum(p['months'] for p in phases),
            'phases': phases,
            'total_budget': '€230K-370K'
        }
    
    def estimate_budget(self) -> Dict:
        """Estimate budget using industry templates"""
        mult = {'small': 1.0, 'medium': 1.5, 'large': 2.5}[self.company_size]
        
        # Apply industry-specific multiplier
        mult *= self.industry_profile['budget_multiplier']
        
        items = {
            'Consulting': int(80000 * mult),
            'PQC Migration': len(self.df) * 3000,
            'Technology': int(45000 * mult),
            'Training': int(15000 * mult),
            'Certification': int(25000 * mult),
            'Pentesting': int(20000 * mult)
        }
        
        total = sum(items.values())
        breach_cost = self.industry_profile['avg_breach_cost']
        roi = ((breach_cost - total) / total) * 100
        
        return {
            'total': total,
            'items': items,
            'roi': roi,
            'breach_cost': breach_cost,
            'industry': self.industry_profile['name']
        }
    
    def generate_complete_framework(self) -> Dict:
        """Generate complete framework"""
        return {
            'metadata': {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'target': self.domain,
                'industry': self.industry.title(),
                'size': self.company_size
            },
            'iso27001': self.generate_iso27001_soa(),
            'bsi': self.generate_bsi_grundschutz(),
            'nis2': self.generate_nis2_compliance(),
            'roadmap': self.generate_roadmap(),
            'budget': self.estimate_budget()
        }


def export_framework_pdf(framework: Dict, target: str) -> bytes:
    """Export framework to PDF"""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 15, "ISMS FRAMEWORK REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Target: {target}", ln=True, align='C')
    pdf.cell(0, 8, f"Date: {framework['metadata']['date']}", ln=True, align='C')
    pdf.ln(10)
    
    # ISO 27001
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, "ISO 27001 STATEMENT OF APPLICABILITY", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    for name, ctrl in framework['iso27001']['controls'].items():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, name, ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, f"  Status: {ctrl['status']} | Priority: {ctrl['priority']}", ln=True)
        pdf.cell(0, 5, f"  Implementation: {ctrl['implementation']}", ln=True)
        pdf.cell(0, 5, f"  Quantum: {ctrl['quantum']}", ln=True)
        pdf.ln(2)
    
    # BSI
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, "BSI IT-GRUNDSCHUTZ BAUSTEINE", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    for name, b in framework['bsi']['bausteine'].items():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, name, ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, f"  Priority: {b['priority']}", ln=True)
        pdf.cell(0, 5, f"  Implementation: {b['implementation']}", ln=True)
        pdf.ln(2)
    
    # Roadmap
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 10, "IMPLEMENTATION ROADMAP", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 10)
    
    for phase in framework['roadmap']['phases']:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 7, f"{phase['phase']} ({phase['months']} months)", ln=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, f"Budget: {phase['budget']}", ln=True)
        for m in phase['milestones']:
            pdf.cell(0, 5, f"  - {m}", ln=True)
        pdf.ln(3)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, f"Total Budget: {framework['roadmap']['total_budget']}", ln=True)
    pdf.cell(0, 8, f"ROI: {framework['budget']['roi']:.0f}%", ln=True)
    
    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(102, 51, 153)
    pdf.cell(0, 5, "Generated by Sentinel-V ISMS Framework Generator", ln=True, align='C')
    pdf.cell(0, 5, "ProSec Networks - Quantum-Ready Security Partner", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')