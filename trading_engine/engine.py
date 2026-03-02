"""
Trading Engine - Main Integration

Unified trading system connecting all components:
- Strategies (arbitrage, momentum, mean reversion, etc.)
- Portfolio management
- Market data feeds
- Order execution
- Risk management
- Backtesting

APPS HOLDINGS WY, INC.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from trading_engine.strategies.arbitrage import ArbitrageStrategy
from trading_engine.execution.order_manager import OrderManager
from trading_engine.risk.risk_engine import RiskEngine
from trading_engine.portfolio_manager import Portfolio, PositionType
from trading_engine.market_data import MarketData, DataProvider
from trading_engine.backtester import Backtester


@dataclass
class TradingEngine:
    """
    Trading Engine - Complete Trading System

    Integrates all components:
    - Multiple trading strategies
    - Portfolio management
    - Market data (live or paper)
    - Order execution
    - Risk controls
    - Backtesting

    Ready for:
    - Paper trading (default, safe)
    - Live trading (when API keys added)
    """

    name: str = "AgentX5 Trading Engine"
    mode: str = "paper"  # "paper" or "live"
    status: str = "initialized"

    # Components
    portfolio: Portfolio = field(default_factory=Portfolio)
    market_data: MarketData = field(default_factory=MarketData)
    order_manager: OrderManager = field(default_factory=OrderManager)
    risk_engine: RiskEngine = field(default_factory=RiskEngine)
    arbitrage: ArbitrageStrategy = field(default_factory=ArbitrageStrategy)
    backtester: Backtester = field(default_factory=Backtester)

    # Tracking
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    total_trades_executed: int = 0

    def activate(self) -> Dict[str, Any]:
        """Activate trading engine."""
        self.status = "active"
        return {
            "engine": self.name,
            "mode": self.mode,
            "status": self.status,
            "portfolio": self.portfolio.name,
            "activated_at": datetime.now().isoformat(),
        }

    def execute_arbitrage_scan(self) -> Dict[str, Any]:
        """Scan for arbitrage opportunities."""
        opportunities = self.arbitrage.find_opportunities()
        results = []

        for opp in opportunities:
            # Check risk limits
            risk_check = self.risk_engine.check_order(opp)
            if not risk_check["approved"]:
                continue

            # Execute order
            order_result = self.order_manager.execute_order(opp)
            self.total_trades_executed += 1

            # Update portfolio
            self.portfolio.add_position(
                symbol=opp["symbol"],
                position_type=PositionType.LONG,
                quantity=opp["amount"],
                entry_price=opp.get("price", 0),
            )

            results.append({
                "signal": opp,
                "order": order_result,
                "risk_check": risk_check,
            })

        return {
            "scan_time": datetime.now().isoformat(),
            "opportunities_found": len(opportunities),
            "approved": len(results),
            "results": results,
        }

    def get_full_status(self) -> Dict[str, Any]:
        """Get complete system status."""
        return {
            "engine": self.name,
            "mode": self.mode,
            "status": self.status,
            "created_at": self.created_at,
            "total_trades": self.total_trades_executed,
            "portfolio": self.portfolio.get_status(),
            "market_data": self.market_data.get_provider_status(),
            "order_manager": self.order_manager.get_status(),
            "risk_engine": self.risk_engine.get_status(),
            "arbitrage": self.arbitrage.get_config(),
        }

    def shutdown(self) -> Dict[str, Any]:
        """Shutdown trading engine."""
        self.status = "shutdown"
        return {
            "status": "shutdown",
            "timestamp": datetime.now().isoformat(),
            "total_trades_executed": self.total_trades_executed,
            "final_portfolio": self.portfolio.get_status(),
        }


# ============================================================================
# CONVENIENCE INSTANCE - USE THIS IN YOUR CODE
# ============================================================================

engine = TradingEngine()
