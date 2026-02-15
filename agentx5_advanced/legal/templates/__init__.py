"""
AgentX5 Advanced Edition - Legal Document Templates

Harvard/Yale Legal Drafting Standards
Bluebook Citation Format
Court-Ready Document Templates

Templates for:
- Demand Letters (Harvard Style - Briana Williams Format)
- Court Filings (Probate, Civil, Corporate)
- Legal Memoranda
- Declarations and Affidavits
- Forensic Reports

APPS HOLDINGS WY, INC. - ABACUS LEGAL
"""

from agentx5_advanced.legal.templates.demand_letters import (
    HarvardDemandLetter,
    BrianaWilliamsTemplate,
)
from agentx5_advanced.legal.templates.court_filings import (
    ProbatePetition,
    CivilComplaint,
    MotionTemplate,
)
from agentx5_advanced.legal.templates.forensic_reports import (
    ForensicOmnibus,
    PoliceReportTemplate,
    AuditReport,
)

__all__ = [
    "HarvardDemandLetter",
    "BrianaWilliamsTemplate",
    "ProbatePetition",
    "CivilComplaint",
    "MotionTemplate",
    "ForensicOmnibus",
    "PoliceReportTemplate",
    "AuditReport",
]
