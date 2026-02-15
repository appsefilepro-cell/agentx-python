"""
AgentX5 - Bank Statement Analyzer

AUTOMATED analysis of Bank of America and BMO statements.
Copy/paste bank data - system parses automatically.

APPS HOLDINGS WY, INC.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class BankStatementAnalyzer:
    """
    Automated Bank Statement Analysis

    Supported Banks:
    - Bank of America
    - BMO
    - Chase
    - Wells Fargo

    Usage:
    1. Copy/paste raw bank statement text
    2. System parses transactions automatically
    3. Flags suspicious activity
    4. Generates summary
    """

    transactions: List[Dict[str, Any]] = field(default_factory=list)
    flags: List[Dict[str, Any]] = field(default_factory=list)

    def parse_statement(self, raw_text: str) -> List[Dict[str, Any]]:
        """Parse raw bank statement text into transactions."""
        lines = raw_text.strip().split('\n')
        parsed = []

        for line in lines:
            tx = self._parse_line(line)
            if tx:
                parsed.append(tx)
                # Auto-flag suspicious
                if self._is_suspicious(tx):
                    self.flags.append(tx)

        self.transactions = parsed
        return parsed

    def _parse_line(self, line: str) -> Dict[str, Any]:
        """Parse single transaction line."""
        # Pattern for common bank statement formats
        # Date Description Amount
        patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4})\s+(.+?)\s+\$?([\d,]+\.?\d*)',
            r'(\d{1,2}-\d{1,2}-\d{2,4})\s+(.+?)\s+\$?([\d,]+\.?\d*)',
        ]

        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                amount = float(match.group(3).replace(',', ''))
                return {
                    'date': match.group(1),
                    'description': match.group(2).strip(),
                    'amount': amount,
                    'type': 'withdrawal' if 'withdrawal' in line.lower() or amount < 0 else 'deposit',
                    'raw': line,
                }
        return None

    def _is_suspicious(self, tx: Dict[str, Any]) -> bool:
        """Check if transaction is suspicious."""
        suspicious_keywords = [
            'transfer', 'wire', 'cash', 'atm', 'withdrawal',
            'zelle', 'venmo', 'paypal', 'crypto'
        ]
        desc = tx.get('description', '').lower()
        amount = abs(tx.get('amount', 0))

        # Flag large transactions or suspicious keywords
        if amount > 5000:
            return True
        if any(kw in desc for kw in suspicious_keywords):
            return True
        return False

    def get_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        total_deposits = sum(t['amount'] for t in self.transactions if t['type'] == 'deposit')
        total_withdrawals = sum(abs(t['amount']) for t in self.transactions if t['type'] == 'withdrawal')

        return {
            'total_transactions': len(self.transactions),
            'total_deposits': total_deposits,
            'total_withdrawals': total_withdrawals,
            'net_flow': total_deposits - total_withdrawals,
            'flagged_count': len(self.flags),
            'flagged_transactions': self.flags,
        }


# Bank-specific configurations
BANK_CONFIGS = {
    'bank_of_america': {
        'name': 'Bank of America',
        'date_format': 'MM/DD/YYYY',
        'supported': True,
    },
    'bmo': {
        'name': 'BMO',
        'date_format': 'MM/DD/YYYY',
        'supported': True,
    },
}
