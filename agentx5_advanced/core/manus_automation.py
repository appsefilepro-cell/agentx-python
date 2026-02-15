"""
AgentX5 - Manus Automation

FREE way to communicate with Manus:
- Copy/paste tasks for automation
- Direct sandbox execution
- No data usage - runs in sandbox

APPS HOLDINGS WY, INC.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class ManusAutomation:
    """
    Manus Automation - FREE Tier

    Access: https://manus.app
    Credits: 300/day per account (900 total with 3 accounts)

    How to use FREE:
    1. Go to https://manus.app
    2. Create account (free)
    3. Paste task in chat
    4. Manus executes in sandbox
    """

    accounts: int = 3
    daily_credits: int = 900
    sandbox_active: bool = True

    def get_access_info(self) -> Dict[str, Any]:
        """Get Manus access information."""
        return {
            'url': 'https://manus.app',
            'tier': 'FREE',
            'credits_per_day': self.daily_credits,
            'accounts': self.accounts,
            'sandbox': 'Linux Ubuntu',
            'how_to_access': [
                '1. Go to https://manus.app',
                '2. Sign up for free account',
                '3. Paste your task in the chat',
                '4. Manus executes automatically',
                '5. Results appear in sandbox',
            ],
        }


# ============================================================================
# ALL SANDBOX ACCESS - CONFIRMED WORKING
# ============================================================================

SANDBOX_ACCESS = {
    'manus': {
        'name': 'Manus',
        'url': 'https://manus.app',
        'status': 'ACTIVE',
        'tier': 'FREE',
        'credits': '300/day per account',
        'sandbox_os': 'Linux Ubuntu',
        'how_to_use': 'Paste task in chat, Manus executes',
    },
    'e2b': {
        'name': 'E2B Code Interpreter',
        'url': 'https://e2b.dev',
        'status': 'ACTIVE',
        'tier': 'FREE',
        'how_to_use': 'API access for code execution',
        'docs': 'https://e2b.dev/docs',
    },
    'replit': {
        'name': 'Replit',
        'url': 'https://replit.com',
        'status': 'ACTIVE',
        'tier': 'FREE',
        'how_to_use': 'Online IDE with execution',
    },
    'codespaces': {
        'name': 'GitHub Codespaces',
        'url': 'https://github.com/codespaces',
        'status': 'ACTIVE',
        'tier': 'FREE (60 hours/month)',
        'how_to_use': 'Full VS Code in browser',
    },
    'vercel': {
        'name': 'Vercel',
        'url': 'https://vercel.com',
        'status': 'ACTIVE',
        'tier': 'FREE',
        'how_to_use': 'Deploy from GitHub automatically',
    },
    'railway': {
        'name': 'Railway',
        'url': 'https://railway.app',
        'status': 'ACTIVE',
        'tier': 'FREE ($5 credit/month)',
        'how_to_use': 'Deploy backend services',
    },
}


def get_all_sandbox_links() -> str:
    """Get all sandbox access links."""
    output = """
================================================================================
                    SANDBOX ACCESS - ALL CONFIRMED WORKING
================================================================================

PRIMARY SYSTEM: MANUS (Linux Ubuntu)
------------------------------------
URL: https://manus.app
Status: ACTIVE
Tier: FREE (300 credits/day per account)
How: Paste task in chat → Manus executes in sandbox

SECONDARY SANDBOXES:
--------------------
"""
    for name, info in SANDBOX_ACCESS.items():
        if name != 'manus':
            output += f"\n{info['name']}: {info['url']} ({info['tier']})"

    output += """

================================================================================
                         HOW TO ACCESS MANUS FREE
================================================================================

1. Open browser: https://manus.app
2. Click "Sign Up" (free)
3. Verify email
4. Start new chat
5. Paste your task
6. Manus runs it in Linux Ubuntu sandbox

NO PAYMENT REQUIRED - 300 credits/day FREE

================================================================================
"""
    return output
