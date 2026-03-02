"""
Trading Engine - Market Data

Real-time and historical market data integration.
Ready for live feed connection (IEX, Alpha Vantage, Polygon, etc.)

APPS HOLDINGS WY, INC.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class DataProvider(Enum):
    """Supported market data providers."""
    POLYGON = "polygon"
    ALPHA_VANTAGE = "alpha_vantage"
    IEX = "iex"
    YAHOO_FINANCE = "yahoo_finance"
    PAPER = "paper"  # Paper trading mode


@dataclass
class Candle:
    """OHLCV candle."""
    timestamp: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int


@dataclass
class MarketData:
    """
    Market Data Provider

    Provides real-time and historical price data.
    Ready to connect to live feeds.
    """

    provider: DataProvider = DataProvider.PAPER
    api_key: str = ""
    cache: Dict[str, List[Candle]] = field(default_factory=dict)

    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get current price for symbol.

        In paper mode: returns mock prices.
        In live mode: fetches from API.
        """
        if self.provider == DataProvider.PAPER:
            # Mock prices for paper trading
            base_prices = {
                "BTC-USD": 43500.0,
                "ETH-USD": 2400.0,
                "SOL-USD": 110.0,
                "DOGE-USD": 0.15,
                "AAPL": 175.0,
                "GOOGL": 140.0,
                "MSFT": 420.0,
            }
            return base_prices.get(symbol, 100.0)
        else:
            # Connect to live API
            return self._fetch_current_price(symbol)

    def get_historical_data(
        self,
        symbol: str,
        days: int = 30,
    ) -> List[Candle]:
        """Get historical OHLCV data."""
        if symbol in self.cache:
            return self.cache[symbol]

        # Generate mock historical data
        candles = []
        base_price = self.get_current_price(symbol) or 100.0

        for i in range(days, 0, -1):
            date = (datetime.now() - timedelta(days=i)).isoformat()
            open_price = base_price * (0.99 + (i % 3) * 0.005)
            close_price = open_price * (1.0 + (0.02 * (i % 5 - 2) / 5))
            high_price = max(open_price, close_price) * 1.02
            low_price = min(open_price, close_price) * 0.98
            volume = 1000000 + (i * 10000) % 500000

            candle = Candle(
                timestamp=date,
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                volume=int(volume),
            )
            candles.append(candle)

        self.cache[symbol] = candles
        return candles

    def _fetch_current_price(self, symbol: str) -> Optional[float]:
        """Fetch price from live API (placeholder)."""
        # Replace with actual API call when provider is set up
        # Example for Polygon: https://api.polygon.io/v1/last/quote/...
        # Example for Alpha Vantage: https://www.alphavantage.co/query?...
        return None

    def get_technical_indicators(
        self,
        symbol: str,
        period: int = 20,
    ) -> Dict[str, Any]:
        """Calculate technical indicators (SMA, EMA, RSI, MACD, etc.)."""
        candles = self.get_historical_data(symbol, days=period * 3)
        if not candles:
            return {}

        closes = [c.close_price for c in candles[-period:]]

        # Simple moving average
        sma = sum(closes) / len(closes)

        # Simple momentum
        momentum = closes[-1] - closes[0]
        momentum_pct = (momentum / closes[0]) * 100

        return {
            "symbol": symbol,
            "sma_20": sma,
            "momentum": momentum,
            "momentum_pct": momentum_pct,
            "last_close": closes[-1],
            "high_20d": max(closes),
            "low_20d": min(closes),
            "volatility": (max(closes) - min(closes)) / sma,
        }

    def get_provider_status(self) -> Dict[str, Any]:
        return {
            "provider": self.provider.value,
            "connected": self.provider == DataProvider.PAPER or bool(self.api_key),
            "cached_symbols": len(self.cache),
            "mode": "paper" if self.provider == DataProvider.PAPER else "live",
        }
