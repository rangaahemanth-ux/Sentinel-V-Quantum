"""
ISMS Templates for Different Industries
Pre-configured frameworks for Finance, Healthcare, Manufacturing, Energy, Government
"""

from typing import Dict, List


class ISMSTemplates:
    """Industry-specific ISMS framework templates"""
    
    @staticmethod
    def get_industry_profile(industry: str) -> Dict:
        """Get complete industry profile with specific requirements"""
        
        profiles = {
            'finance': {
                'name': 'Financial Services',
                'typical_threats': [
                    'Payment fraud',
                    'Data breaches',
                    'Ransomware',
                    'Quantum harvest attacks on transaction data',
                    'API exploitation'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'BSI IT-Grundschutz',
                    'NIS2',
                    'PSD2',
                    'GDPR',
                    'BaFin BAIT/VAIT'
                ],
                'critical_controls': [
                    'A.10 Cryptography (PQC for transactions)',
                    'A.13 Communications Security (Secure banking channels)',
                    'A.18 Compliance (PSD2, BaFin)',
                    'A.12 Operations Security (Fraud detection)'
                ],
                'quantum_priority': 'CRITICAL',
                'budget_multiplier': 1.8,
                'avg_breach_cost': 5_800_000,
                'implementation_urgency': 'Immediate (0-6 months)'
            },
            
            'healthcare': {
                'name': 'Healthcare & Medical',
                'typical_threats': [
                    'Patient data breaches',
                    'Ransomware on medical devices',
                    'Quantum threats to long-term medical records',
                    'Supply chain attacks',
                    'IoT medical device vulnerabilities'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'NIS2',
                    'GDPR (Healthcare)',
                    'Medical Device Regulation (MDR)',
                    'HIPAA (if US operations)'
                ],
                'critical_controls': [
                    'A.10 Cryptography (Patient data PQC)',
                    'A.8 Asset Management (Medical devices)',
                    'A.18 Compliance (GDPR, MDR)',
                    'A.17 Business Continuity (Life-critical systems)'
                ],
                'quantum_priority': 'CRITICAL',
                'budget_multiplier': 2.2,
                'avg_breach_cost': 10_100_000,
                'implementation_urgency': 'Urgent (0-9 months)'
            },
            
            'manufacturing': {
                'name': 'Manufacturing & Industrial',
                'typical_threats': [
                    'OT/IT convergence attacks',
                    'Industrial espionage',
                    'Supply chain disruption',
                    'Quantum threats to proprietary data',
                    'SCADA/ICS vulnerabilities'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'BSI IT-Grundschutz',
                    'NIS2',
                    'IEC 62443 (Industrial security)',
                    'ISO 27019 (Energy utilities)'
                ],
                'critical_controls': [
                    'A.10 Cryptography (IP protection)',
                    'A.13 Network Security (OT segmentation)',
                    'A.15 Supplier Relationships',
                    'A.11 Physical Security (Facilities)'
                ],
                'quantum_priority': 'HIGH',
                'budget_multiplier': 1.5,
                'avg_breach_cost': 4_300_000,
                'implementation_urgency': 'Standard (6-12 months)'
            },
            
            'energy': {
                'name': 'Energy & Utilities',
                'typical_threats': [
                    'Critical infrastructure attacks',
                    'SCADA/grid manipulation',
                    'Nation-state quantum espionage',
                    'Supply chain compromise',
                    'Physical-cyber combined attacks'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'NIS2 (Critical Entity)',
                    'IEC 62351 (Power systems)',
                    'NERC CIP (if applicable)',
                    'BSI IT-Grundschutz'
                ],
                'critical_controls': [
                    'A.10 Cryptography (Grid communication PQC)',
                    'A.13 Network Security (SCADA isolation)',
                    'A.16 Incident Management (Critical response)',
                    'A.17 Business Continuity (Grid stability)'
                ],
                'quantum_priority': 'CRITICAL',
                'budget_multiplier': 2.0,
                'avg_breach_cost': 6_500_000,
                'implementation_urgency': 'Immediate (0-6 months)'
            },
            
            'government': {
                'name': 'Government & Public Sector',
                'typical_threats': [
                    'Nation-state attacks',
                    'Quantum harvest of classified data',
                    'Citizen data breaches',
                    'Election infrastructure threats',
                    'Critical service disruption'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'BSI IT-Grundschutz (Mandatory for German gov)',
                    'NIS2',
                    'National security classifications',
                    'E-Government Act'
                ],
                'critical_controls': [
                    'A.10 Cryptography (Classified data PQC)',
                    'A.9 Access Control (Clearance-based)',
                    'A.18 Compliance (National regulations)',
                    'A.16 Incident Management (National response)'
                ],
                'quantum_priority': 'CRITICAL',
                'budget_multiplier': 2.5,
                'avg_breach_cost': 8_000_000,
                'implementation_urgency': 'Immediate (0-3 months)'
            },
            
            'ecommerce': {
                'name': 'E-Commerce & Retail',
                'typical_threats': [
                    'Payment card data breaches',
                    'Customer data theft',
                    'Quantum threats to payment history',
                    'API vulnerabilities',
                    'Supply chain attacks'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'PCI-DSS',
                    'GDPR',
                    'NIS2 (if critical size)',
                    'E-Commerce Directive'
                ],
                'critical_controls': [
                    'A.10 Cryptography (Payment PQC)',
                    'A.13 Communications Security (E-commerce TLS)',
                    'A.14 Secure Development (Web apps)',
                    'A.18 Compliance (PCI-DSS, GDPR)'
                ],
                'quantum_priority': 'HIGH',
                'budget_multiplier': 1.3,
                'avg_breach_cost': 3_200_000,
                'implementation_urgency': 'Standard (6-12 months)'
            },
            
            'technology': {
                'name': 'Technology & Software',
                'typical_threats': [
                    'Source code theft',
                    'Quantum IP espionage',
                    'Supply chain attacks',
                    'Cloud infrastructure breaches',
                    'Zero-day exploits'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'SOC 2',
                    'GDPR',
                    'Cloud security standards',
                    'Software supply chain security'
                ],
                'critical_controls': [
                    'A.10 Cryptography (Source code, API keys)',
                    'A.14 Secure Development (SDL)',
                    'A.8 Asset Management (Cloud resources)',
                    'A.15 Supplier Security (Dependencies)'
                ],
                'quantum_priority': 'HIGH',
                'budget_multiplier': 1.4,
                'avg_breach_cost': 4_100_000,
                'implementation_urgency': 'Standard (6-12 months)'
            },
            
            'telecommunications': {
                'name': 'Telecommunications',
                'typical_threats': [
                    'Network infrastructure attacks',
                    'Quantum eavesdropping',
                    'SS7/5G vulnerabilities',
                    'Customer data breaches',
                    'DDoS attacks'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'NIS2 (Essential Entity)',
                    'GDPR',
                    'Telecommunications Act',
                    '5G security requirements'
                ],
                'critical_controls': [
                    'A.10 Cryptography (Network encryption PQC)',
                    'A.13 Network Security (Core network)',
                    'A.17 Business Continuity (Network uptime)',
                    'A.18 Compliance (Telco regulations)'
                ],
                'quantum_priority': 'CRITICAL',
                'budget_multiplier': 2.0,
                'avg_breach_cost': 5_500_000,
                'implementation_urgency': 'Urgent (0-9 months)'
            },
            
            'general': {
                'name': 'General Business',
                'typical_threats': [
                    'Ransomware',
                    'Phishing',
                    'Data breaches',
                    'Quantum threats to archives',
                    'Business email compromise'
                ],
                'compliance_frameworks': [
                    'ISO 27001',
                    'GDPR',
                    'Industry-specific regulations'
                ],
                'critical_controls': [
                    'A.10 Cryptography (Data at rest/transit)',
                    'A.8 Asset Management',
                    'A.12 Operations Security',
                    'A.18 Compliance (GDPR)'
                ],
                'quantum_priority': 'MODERATE',
                'budget_multiplier': 1.0,
                'avg_breach_cost': 4_450_000,
                'implementation_urgency': 'Standard (6-18 months)'
            }
        }
        
        return profiles.get(industry, profiles['general'])
    
    @staticmethod
    def get_quantum_migration_template(industry: str, criticality: str) -> Dict:
        """Get quantum migration strategy template"""
        
        templates = {
            'finance_critical': {
                'timeline': '0-3 months',
                'algorithms': {
                    'key_exchange': 'ML-KEM-1024',
                    'signatures': 'ML-DSA-87',
                    'hash': 'SHA-3-512'
                },
                'priority_assets': [
                    'Payment processing systems',
                    'Customer transaction databases',
                    'API gateways',
                    'Authentication servers'
                ],
                'hybrid_mode': 'Mandatory for backward compatibility',
                'testing_requirements': 'Full regression + penetration test',
                'budget_per_asset': 8000
            },
            
            'healthcare_critical': {
                'timeline': '0-6 months',
                'algorithms': {
                    'key_exchange': 'ML-KEM-1024',
                    'signatures': 'ML-DSA-87',
                    'hash': 'SHA-3-512'
                },
                'priority_assets': [
                    'Electronic Health Records (EHR)',
                    'Medical imaging systems',
                    'Patient portals',
                    'Medical device management'
                ],
                'hybrid_mode': 'Required for legacy medical devices',
                'testing_requirements': 'Clinical validation + security audit',
                'budget_per_asset': 12000
            },
            
            'energy_critical': {
                'timeline': '0-6 months',
                'algorithms': {
                    'key_exchange': 'ML-KEM-1024',
                    'signatures': 'ML-DSA-87',
                    'hash': 'SHA-3-512'
                },
                'priority_assets': [
                    'SCADA systems',
                    'Grid control systems',
                    'Smart meter infrastructure',
                    'Remote terminal units (RTU)'
                ],
                'hybrid_mode': 'Essential for OT compatibility',
                'testing_requirements': 'ICS security validation + grid simulation',
                'budget_per_asset': 15000
            },
            
            'standard_high': {
                'timeline': '3-9 months',
                'algorithms': {
                    'key_exchange': 'ML-KEM-768',
                    'signatures': 'ML-DSA-65',
                    'hash': 'SHA-3-256'
                },
                'priority_assets': [
                    'Web applications',
                    'Databases',
                    'Email servers',
                    'File servers'
                ],
                'hybrid_mode': 'Recommended',
                'testing_requirements': 'Standard penetration test',
                'budget_per_asset': 5000
            },
            
            'standard_moderate': {
                'timeline': '6-18 months',
                'algorithms': {
                    'key_exchange': 'ML-KEM-512',
                    'signatures': 'ML-DSA-44',
                    'hash': 'SHA-3-256'
                },
                'priority_assets': [
                    'Internal systems',
                    'Development environments',
                    'Testing infrastructure'
                ],
                'hybrid_mode': 'Optional',
                'testing_requirements': 'Basic functionality test',
                'budget_per_asset': 3000
            }
        }
        
        # Generate key based on industry and criticality
        key = f"{industry}_{criticality.lower()}"
        
        # Fallback logic
        if key in templates:
            return templates[key]
        elif criticality.lower() == 'critical':
            return templates.get(f"{industry}_critical", templates['standard_high'])
        else:
            return templates.get('standard_high' if criticality.lower() == 'high' else 'standard_moderate')
    
    @staticmethod
    def get_nis2_requirements_template(industry: str) -> Dict:
        """Get NIS2-specific requirements for industry"""
        
        nis2_templates = {
            'essential_entities': ['finance', 'energy', 'healthcare', 'telecommunications', 'government'],
            
            'finance': {
                'entity_type': 'Essential',
                'sector_specific': [
                    'PSD2 strong customer authentication',
                    'BaFin BAIT/VAIT requirements',
                    'Payment service provider obligations',
                    'Quantum-safe payment channels'
                ],
                'incident_reporting': 'Within 24 hours of detection',
                'supply_chain_focus': 'Payment processors, cloud providers, fintech partners'
            },
            
            'healthcare': {
                'entity_type': 'Essential',
                'sector_specific': [
                    'Medical device cybersecurity (MDR)',
                    'Patient data protection (GDPR healthcare)',
                    'Telemedicine security',
                    'Quantum-safe medical records'
                ],
                'incident_reporting': 'Immediate if patient safety affected',
                'supply_chain_focus': 'Medical device vendors, pharma partners, lab systems'
            },
            
            'energy': {
                'entity_type': 'Essential',
                'sector_specific': [
                    'Critical infrastructure protection',
                    'SCADA/ICS security (IEC 62443)',
                    'Grid stability requirements',
                    'Quantum-safe grid communications'
                ],
                'incident_reporting': 'Immediate if grid stability threatened',
                'supply_chain_focus': 'Equipment vendors, smart grid providers, SCADA systems'
            },
            
            'general': {
                'entity_type': 'Important',
                'sector_specific': [
                    'Standard risk management',
                    'Incident handling procedures',
                    'Business continuity planning'
                ],
                'incident_reporting': 'Within 72 hours',
                'supply_chain_focus': 'Key vendors and service providers'
            }
        }
        
        return nis2_templates.get(industry, nis2_templates['general'])
    
    @staticmethod
    def get_bsi_bausteine_template(industry: str) -> List[Dict]:
        """Get BSI IT-Grundschutz Bausteine specific to industry"""
        
        # Core bausteine for all industries
        core_bausteine = [
            {
                'id': 'ISMS.1',
                'name': 'Sicherheitsmanagement',
                'priority': 'P0',
                'quantum_relevant': True
            },
            {
                'id': 'CON.1',
                'name': 'Kryptokonzept',
                'priority': 'P0',
                'quantum_relevant': True
            },
            {
                'id': 'OPS.1.1.2',
                'name': 'Ordnungsgemäße IT-Administration',
                'priority': 'P1',
                'quantum_relevant': False
            },
            {
                'id': 'DER.1',
                'name': 'Detektion von Ereignissen',
                'priority': 'P0',
                'quantum_relevant': True
            }
        ]
        
        # Industry-specific additional bausteine
        industry_specific = {
            'finance': [
                {
                    'id': 'APP.4.3',
                    'name': 'Relationale Datenbanksysteme',
                    'priority': 'P0',
                    'quantum_relevant': True,
                    'note': 'Transaction database encryption'
                },
                {
                    'id': 'NET.3.3',
                    'name': 'VPN',
                    'priority': 'P0',
                    'quantum_relevant': True,
                    'note': 'Quantum-safe banking VPN'
                }
            ],
            
            'healthcare': [
                {
                    'id': 'APP.5.1',
                    'name': 'Groupware',
                    'priority': 'P1',
                    'quantum_relevant': False,
                    'note': 'Medical communication systems'
                },
                {
                    'id': 'IND.1',
                    'name': 'Betriebs- und Steuerungstechnik',
                    'priority': 'P0',
                    'quantum_relevant': True,
                    'note': 'Medical device security'
                }
            ],
            
            'energy': [
                {
                    'id': 'IND.1',
                    'name': 'Betriebs- und Steuerungstechnik',
                    'priority': 'P0',
                    'quantum_relevant': True,
                    'note': 'SCADA/ICS security'
                },
                {
                    'id': 'IND.2.1',
                    'name': 'Allgemeine ICS-Komponente',
                    'priority': 'P0',
                    'quantum_relevant': True,
                    'note': 'Grid control systems'
                }
            ],
            
            'manufacturing': [
                {
                    'id': 'IND.1',
                    'name': 'Betriebs- und Steuerungstechnik',
                    'priority': 'P0',
                    'quantum_relevant': True,
                    'note': 'Industrial control systems'
                }
            ]
        }
        
        result = core_bausteine.copy()
        if industry in industry_specific:
            result.extend(industry_specific[industry])
        
        return result
    
    @staticmethod
    def get_implementation_phases_template(industry: str, company_size: str) -> List[Dict]:
        """Get customized implementation phases"""
        
        # Time multipliers based on company size
        time_mult = {
            'small': 0.75,
            'medium': 1.0,
            'large': 1.5
        }
        
        mult = time_mult.get(company_size, 1.0)
        
        # Industry urgency adjustment
        urgent_industries = ['finance', 'healthcare', 'energy', 'government']
        if industry in urgent_industries:
            mult *= 0.8  # Faster timeline for critical industries
        
        return [
            {
                'number': 1,
                'name': 'Critical Security Controls',
                'months': int(3 * mult),
                'focus': 'Immediate threats and compliance gaps',
                'key_deliverables': [
                    'Critical asset PQC migration',
                    'MFA deployment',
                    'Incident response capability',
                    'Basic monitoring'
                ]
            },
            {
                'number': 2,
                'name': 'ISMS Core Implementation',
                'months': int(3 * mult),
                'focus': 'ISO 27001 and BSI framework',
                'key_deliverables': [
                    'ISMS documentation',
                    'Policy framework',
                    'Risk assessment process',
                    'High-priority PQC migration'
                ]
            },
            {
                'number': 3,
                'name': 'Advanced Controls & Zero Trust',
                'months': int(3 * mult),
                'focus': 'Maturity and optimization',
                'key_deliverables': [
                    'Zero Trust architecture',
                    'Advanced threat detection',
                    'Complete PQC migration',
                    'Penetration testing'
                ]
            },
            {
                'number': 4,
                'name': 'Certification & Continuous Improvement',
                'months': int(3 * mult),
                'focus': 'Validation and certification',
                'key_deliverables': [
                    'ISO 27001 certification',
                    'BSI compliance verification',
                    'NIS2 audit readiness',
                    'Continuous monitoring'
                ]
            }
        ]