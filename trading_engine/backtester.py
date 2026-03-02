"""
Trading Engine - Backtester

Run historical backtests to validate strategies before live trading.

APPS HOLDINGS WY, INC.
"""

from typing import Dict, List, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BacktestResult:
    """Single backtest result."""
    strategy_name: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return: float
    return_pct: float
    max_drawdown_pct: float
    win_rate: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy_name,
            "start": self.start_date,
            "end": self.end_date,
            "initial_capital": self.initial_capital,
            "final_capital": self.final_capital,
            "return": self.total_return,
            "return_pct": self.return_pct,
            "max_drawdown_pct": self.max_drawdown_pct,
            "win_rate": self.win_rate,
            "trades": self.total_trades,
            "wins": self.winning_trades,
            "losses": self.losing_trades,
            "sharpe": self.sharpe_ratio,
            "sortino": self.sortino_ratio,
        }


@dataclass
class Backtester:
    """
    Backtester - Validate strategies on historical data.

    Simulates strategy execution on past price data
    to evaluate performance before live trading.
    """

    initial_capital: float = 100000.0
    commission_pct: float = 0.001  # 0.1% per trade
    max_position_pct: float = 0.2  # Max 20% per position

    def backtest(
        self,
        strategy_func: Callable,
        symbol: str,
        candles: List[Any],
        start_date: str = "",
        end_date: str = "",
    ) -> BacktestResult:
        """
        Run backtest on strategy.

        strategy_func: Function that takes candles and returns signals
        symbol: Trading symbol
        candles: Historical candle data
        """
        if not candles:
            return BacktestResult(
                strategy_name=strategy_func.__name__,
                start_date=start_date or "N/A",
                end_date=end_date or "N/A",
                initial_capital=self.initial_capital,
                final_capital=self.initial_capital,
                total_return=0,
                return_pct=0,
                max_drawdown_pct=0,
                win_rate=0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
            )

        # Simulate trades
        capital = self.initial_capital
        trades = []
        portfolio_values = [capital]
        position = None
        position_entry = 0

        for i, candle in enumerate(candles):
            # Get signal from strategy
            signal = strategy_func(candles[:i+1])

            if signal == "BUY" and position is None:
                # Open long position
                position = capital / candle.close_price
                position_entry = candle.close_price
                capital -= position * candle.close_price * self.commission_pct

            elif signal == "SELL" and position is not None:
                # Close position
                exit_price = candle.close_price
                pnl = (exit_price - position_entry) * position
                capital += position * exit_price
                capital -= position * exit_price * self.commission_pct
                trades.append({"entry": position_entry, "exit": exit_price, "pnl": pnl})
                position = None

            # Calculate portfolio value
            if position is not None:
                value = capital + (position * candle.close_price)
            else:
                value = capital
            portfolio_values.append(value)

        # Calculate metrics
        final_capital = capital if position is None else capital + (position * candles[-1].close_price)
        total_return = final_capital - self.initial_capital
        return_pct = (total_return / self.initial_capital) * 100 if self.initial_capital else 0

        # Drawdown
        max_val = max(portfolio_values) if portfolio_values else self.initial_capital
        max_drawdown = max(max_val - v for v in portfolio_values) if portfolio_values else 0
        max_drawdown_pct = (max_drawdown / max_val * 100) if max_val else 0

        # Win rate
        if trades:
            winning = sum(1 for t in trades if t["pnl"] > 0)
            losing = sum(1 for t in trades if t["pnl"] <= 0)
            win_rate = (winning / len(trades)) * 100 if trades else 0
        else:
            winning = losing = win_rate = 0

        return BacktestResult(
            strategy_name=strategy_func.__name__,
            start_date=start_date or candles[0].timestamp,
            end_date=end_date or candles[-1].timestamp,
            initial_capital=self.initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            return_pct=return_pct,
            max_drawdown_pct=max_drawdown_pct,
            win_rate=win_rate,
            total_trades=len(trades),
            winning_trades=winning,
            losing_trades=losing,
        )
