"""
Trading Engine - Order Manager

Executes trade orders. Ready for real broker API integration.

APPS HOLDINGS WY, INC.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    """Order lifecycle status."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """Single trade order."""
    order_id: str
    symbol: str
    action: str  # "buy" or "sell"
    amount: float
    price: float = 0.0
    status: OrderStatus = OrderStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    filled_at: Optional[str] = None
    broker: str = "paper"  # "coinbase", "robinhood", "paper"


@dataclass
class OrderManager:
    """
    Order Manager - Execute trades.

    Supports:
    - Paper trading (default, safe)
    - Coinbase (when API connected)
    - Robinhood (when API connected)
    """
    mode: str = "paper"  # "paper", "live"
    orders: List[Order] = field(default_factory=list)
    total_executed: int = 0

    def execute_order(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a trade order from a signal.

        In paper mode: logs the trade.
        In live mode: sends to broker API.
        """
        order = Order(
            order_id=f"order-{len(self.orders) + 1:06d}",
            symbol=signal.get("symbol", "UNKNOWN"),
            action=signal.get("action", "buy"),
            amount=signal.get("amount", 0),
            broker=self.mode,
        )

        if self.mode == "paper":
            order.status = OrderStatus.FILLED
            order.filled_at = datetime.now().isoformat()
            self.total_executed += 1
            print(f"[PAPER] Executed: {order.action} {order.amount} {order.symbol}")
        else:
            order.status = OrderStatus.SUBMITTED
            print(f"[LIVE] Submitted: {order.action} {order.amount} {order.symbol}")

        self.orders.append(order)

        return {
            "order_id": order.order_id,
            "symbol": order.symbol,
            "action": order.action,
            "amount": order.amount,
            "status": order.status.value,
            "mode": self.mode,
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "mode": self.mode,
            "total_orders": len(self.orders),
            "total_executed": self.total_executed,
            "recent_orders": [
                {
                    "order_id": o.order_id,
                    "symbol": o.symbol,
                    "action": o.action,
                    "status": o.status.value,
                }
                for o in self.orders[-10:]
            ],
        }
