"""
Data Fetcher Module
Handles fetching and preprocessing market data
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional


class DataFetcher:
    """Fetches market data for trading algorithms"""
    
    def __init__(self, symbol: str, interval: str = "1d"):
        """
        Initialize data fetcher
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
            interval: Data interval (1m, 5m, 15m, 1h, 1d, etc.)
        """
        self.symbol = symbol
        self.interval = interval
        self.data = None
        
    def fetch_historical_data(self, period: str = "1y", start: Optional[str] = None, 
                             end: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch historical market data
        
        Args:
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            ticker = yf.Ticker(self.symbol)
            
            if start and end:
                self.data = ticker.history(start=start, end=end, interval=self.interval)
            else:
                self.data = ticker.history(period=period, interval=self.interval)
            
            return self.data
        except Exception as e:
            raise Exception(f"Error fetching data for {self.symbol}: {str(e)}")
    
    def get_latest_price(self) -> float:
        """Get the latest closing price"""
        if self.data is None or self.data.empty:
            self.fetch_historical_data(period="1d")
        
        return float(self.data['Close'].iloc[-1])
    
    def add_technical_indicators(self, sma_periods: list = None, ema_periods: list = None):
        """
        Add technical indicators to the data
        
        Args:
            sma_periods: List of SMA periods to calculate
            ema_periods: List of EMA periods to calculate
        """
        if self.data is None or self.data.empty:
            raise ValueError("No data available. Fetch data first.")
        
        # Simple Moving Averages
        if sma_periods:
            for period in sma_periods:
                self.data[f'SMA_{period}'] = self.data['Close'].rolling(window=period).mean()
        
        # Exponential Moving Averages
        if ema_periods:
            for period in ema_periods:
                self.data[f'EMA_{period}'] = self.data['Close'].ewm(span=period, adjust=False).mean()
        
        return self.data
