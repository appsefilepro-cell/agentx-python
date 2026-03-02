"""
Trading Engine - Portfolio Manager

Manages all positions, allocations, and performance tracking.

APPS HOLDINGS WY, INC.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PositionType(Enum):
    """Position types in portfolio."""
    LONG = "long"
    SHORT = "short"
    HEDGE = "hedge"


@dataclass
class Position:
    """Single position in portfolio."""
    symbol: str
    position_type: PositionType
    quantity: float
    entry_price: float
    current_price: float = 0.0
    entry_date: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "open"  # "open", "closed", "liquidated"

    @property
    def current_value(self) -> float:
        """Current market value of position."""
        return self.quantity * self.current_price

    @property
    def entry_value(self) -> float:
        """Entry value of position."""
        return self.quantity * self.entry_price

    @property
    def unrealized_pnl(self) -> float:
        """Unrealized profit/loss."""
        if self.position_type == PositionType.LONG:
            return self.current_value - self.entry_value
        else:  # SHORT
            return self.entry_value - self.current_value

    @property
    def unrealized_pnl_pct(self) -> float:
        """Unrealized P&L as percentage."""
        if self.entry_value == 0:
            return 0.0
        return (self.unrealized_pnl / abs(self.entry_value)) * 100


@dataclass
class Portfolio:
    """
    Portfolio Manager - Track all positions and performance.

    Manages:
    - Multiple positions across different symbols
    - Position sizing and allocations
    - Performance tracking (daily, monthly, YTD)
    - Risk per position
    """

    name: str = "Trading Portfolio"
    initial_capital: float = 100000.0
    current_capital: float = 100000.0
    positions: List[Position] = field(default_factory=list)
    realized_pnl: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def add_position(
        self,
        symbol: str,
        position_type: PositionType,
        quantity: float,
        entry_price: float,
    ) -> Optional[Position]:
        """Add a new position to portfolio."""
        # Check if position already exists
        for pos in self.positions:
            if pos.symbol == symbol and pos.position_type == position_type:
                # Increase position size
                total_cost = (pos.quantity * pos.entry_price) + (quantity * entry_price)
                pos.quantity += quantity
                pos.entry_price = total_cost / pos.quantity
                self.updated_at = datetime.now().isoformat()
                return pos

        # New position
        position = Position(
            symbol=symbol,
            position_type=position_type,
            quantity=quantity,
            entry_price=entry_price,
        )
        self.positions.append(position)
        self.updated_at = datetime.now().isoformat()
        return position

    def close_position(self, symbol: str, position_type: PositionType) -> Optional[float]:
        """Close a position and realize P&L."""
        for pos in self.positions:
            if pos.symbol == symbol and pos.position_type == position_type:
                pnl = pos.unrealized_pnl
                self.realized_pnl += pnl
                pos.status = "closed"
                self.updated_at = datetime.now().isoformat()
                return pnl
        return None

    def get_total_position_value(self) -> float:
        """Get total market value of all open positions."""
        return sum(p.current_value for p in self.positions if p.status == "open")

    def get_total_unrealized_pnl(self) -> float:
        """Get total unrealized P&L across all positions."""
        return sum(p.unrealized_pnl for p in self.positions if p.status == "open")

    def get_net_pnl(self) -> float:
        """Get net P&L (realized + unrealized)."""
        return self.realized_pnl + self.get_total_unrealized_pnl()

    def get_return_pct(self) -> float:
        """Get return as percentage of initial capital."""
        if self.initial_capital == 0:
            return 0.0
        return (self.get_net_pnl() / self.initial_capital) * 100

    def get_status(self) -> Dict[str, Any]:
        """Get portfolio status report."""
        return {
            "name": self.name,
            "initial_capital": self.initial_capital,
            "current_capital": self.current_capital,
            "total_positions": len([p for p in self.positions if p.status == "open"]),
            "total_position_value": self.get_total_position_value(),
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": self.get_total_unrealized_pnl(),
            "net_pnl": self.get_net_pnl(),
            "return_pct": self.get_return_pct(),
            "updated_at": self.updated_at,
            "positions": [
                {
                    "symbol": p.symbol,
                    "type": p.position_type.value,
                    "quantity": p.quantity,
                    "entry_price": p.entry_price,
                    "current_value": p.current_value,
                    "unrealized_pnl": p.unrealized_pnl,
                    "unrealized_pnl_pct": p.unrealized_pnl_pct,
                    "status": p.status,
                }
                for p in self.positions
            ],
        }
