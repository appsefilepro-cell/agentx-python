"""
AgentX5 Advanced Edition - Master Legal Prompts

Pre-configured prompts for all legal document types.
Use with Claude, Gemini, Perplexity for optimal results.

APPS HOLDINGS WY, INC. - ABACUS LEGAL
"""

from typing import Dict, List, Any

# ============================================================================
# PROBATE PROMPTS
# ============================================================================

PROBATE_PROMPTS = {
    "petition_for_removal": """
LEGAL RESEARCH: PETITION FOR REMOVAL OF FIDUCIARY

Research and draft a petition for removal of fiduciary based on:
1. Breach of fiduciary duties
2. Self-dealing and conflicts of interest
3. Failure to account
4. Mismanagement of estate assets
5. Bad faith administration

Include applicable Probate Code sections and case law.
Format: Court-ready pleading with Bluebook citations.
""",

    "accounting_objection": """
LEGAL RESEARCH: OBJECTION TO ACCOUNTING

Draft objections to fiduciary accounting based on:
1. Missing transactions or incomplete records
2. Unexplained withdrawals
3. Self-dealing transactions
4. Overcompensation claims
5. Improper expense allocations

Include demand for surcharge and removal.
""",

    "surcharge_petition": """
LEGAL RESEARCH: PETITION FOR SURCHARGE

Calculate and document surcharge claims for:
1. Losses due to breach of duty
2. Profits fiduciary should have earned
3. Interest on misappropriated funds
4. Consequential damages
5. Attorney fees and costs

Include itemized damages schedule with calculations.
""",
}

# ============================================================================
# FIDUCIARY PROMPTS
# ============================================================================

FIDUCIARY_PROMPTS = {
    "breach_analysis": """
FIDUCIARY BREACH ANALYSIS

Analyze potential breaches of:
1. Duty of Loyalty - undivided allegiance to beneficiaries
2. Duty of Care - prudent administration
3. Duty to Account - full disclosure
4. Duty of Impartiality - fair treatment of all beneficiaries
5. Duty to Preserve - protect and maintain assets

Document each breach with evidence and damages.
""",

    "self_dealing_investigation": """
SELF-DEALING INVESTIGATION

Investigate and document:
1. Transactions between fiduciary and estate/trust
2. Loans to/from fiduciary
3. Use of trust property for personal benefit
4. Dual representation conflicts
5. Undisclosed compensation

Trace all funds and calculate disgorgement.
""",

    "accounting_demand": """
DEMAND FOR ACCOUNTING

Draft formal demand for:
1. Complete accounting of all transactions
2. Bank statements and records
3. Investment account statements
4. Real property records
5. Tax returns filed

Include statutory basis and deadline for response.
""",
}

# ============================================================================
# CORPORATE PROMPTS
# ============================================================================

CORPORATE_PROMPTS = {
    "incorporation_review": """
CORPORATE FORMATION REVIEW

Review and verify:
1. Articles of Incorporation
2. Bylaws
3. Initial resolutions
4. Stock certificates
5. Registered agent designation

Ensure compliance with state requirements.
""",

    "shareholder_dispute": """
SHAREHOLDER DISPUTE ANALYSIS

Analyze claims for:
1. Breach of fiduciary duty by directors/officers
2. Oppression of minority shareholders
3. Derivative claims on behalf of corporation
4. Direct claims for individual harm
5. Dissolution or buyout remedies

Include business judgment rule analysis.
""",

    "corporate_governance": """
CORPORATE GOVERNANCE AUDIT

Review compliance with:
1. Annual meeting requirements
2. Board meeting protocols
3. Record-keeping obligations
4. Financial reporting
5. Conflict of interest policies

Document deficiencies and remediation steps.
""",
}

# ============================================================================
# TRUST PROMPTS
# ============================================================================

TRUST_PROMPTS = {
    "trust_interpretation": """
TRUST DOCUMENT INTERPRETATION

Analyze trust terms for:
1. Distribution standards
2. Trustee powers and limitations
3. Beneficiary rights
4. Amendment/revocation provisions
5. Spendthrift provisions

Apply rules of construction and cite authority.
""",

    "trustee_removal": """
TRUSTEE REMOVAL GROUNDS

Document grounds for removal:
1. Breach of trust
2. Failure to administer
3. Substantial conflict of interest
4. Unfitness or inability to serve
5. Substantial change in circumstances

Include case law and statutory authority.
""",

    "trust_modification": """
TRUST MODIFICATION PETITION

Draft petition for:
1. Modification due to changed circumstances
2. Cy pres (charitable trusts)
3. Equitable deviation
4. Trust decanting
5. Merger or division

Include legal standards and supporting facts.
""",
}

# ============================================================================
# LITIGATION PROMPTS
# ============================================================================

LITIGATION_PROMPTS = {
    "complaint_drafting": """
CIVIL COMPLAINT DRAFTING

Draft complaint including:
1. Jurisdictional allegations
2. Parties and venue
3. Statement of facts
4. Causes of action with elements
5. Prayer for relief

Format per local court rules.
""",

    "motion_practice": """
MOTION DRAFTING

Draft motion with:
1. Notice of motion
2. Memorandum of points and authorities
3. Statement of facts
4. Legal argument
5. Proposed order

Include proper citation format.
""",

    "discovery_requests": """
DISCOVERY DRAFTING

Prepare discovery including:
1. Interrogatories
2. Requests for production
3. Requests for admission
4. Deposition notices
5. Subpoenas

Tailor to case issues and claims.
""",

    "settlement_demand": """
SETTLEMENT DEMAND LETTER

Draft demand including:
1. Statement of claims
2. Liability analysis
3. Damages calculation
4. Settlement offer
5. Response deadline

Professional tone with firm position.
""",
}

# ============================================================================
# PROMPT REGISTRY
# ============================================================================

ALL_LEGAL_PROMPTS = {
    "probate": PROBATE_PROMPTS,
    "fiduciary": FIDUCIARY_PROMPTS,
    "corporate": CORPORATE_PROMPTS,
    "trust": TRUST_PROMPTS,
    "litigation": LITIGATION_PROMPTS,
}


def get_prompt(category: str, prompt_name: str) -> str:
    """Get specific legal prompt."""
    category_prompts = ALL_LEGAL_PROMPTS.get(category, {})
    return category_prompts.get(prompt_name, "")


def list_all_prompts() -> Dict[str, List[str]]:
    """List all available prompts by category."""
    return {
        category: list(prompts.keys())
        for category, prompts in ALL_LEGAL_PROMPTS.items()
    }


def get_prompt_count() -> int:
    """Get total number of prompts."""
    return sum(len(prompts) for prompts in ALL_LEGAL_PROMPTS.values())
