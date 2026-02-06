"""
Synthetic Data Generator
Creates realistic market data for testing and demo purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class SyntheticDataGenerator:
    """Generates synthetic market data for testing"""
    
    @staticmethod
    def generate_trending_data(symbol: str = "DEMO", days: int = 730, 
                              initial_price: float = 100.0, 
                              trend: float = 0.0002, 
                              volatility: float = 0.02) -> pd.DataFrame:
        """
        Generate synthetic market data with a trend
        
        Args:
            symbol: Ticker symbol
            days: Number of days of data
            initial_price: Starting price
            trend: Daily trend (0.0002 = 0.02% daily uptrend)
            volatility: Daily volatility
            
        Returns:
            DataFrame with OHLCV data
        """
        np.random.seed(42)  # For reproducibility
        
        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate price data
        returns = np.random.normal(trend, volatility, days)
        prices = initial_price * np.exp(np.cumsum(returns))
        
        # Generate OHLCV data
        data = []
        for i, date in enumerate(dates[:len(prices)]):
            close = prices[i]
            high = close * (1 + abs(np.random.normal(0, volatility/2)))
            low = close * (1 - abs(np.random.normal(0, volatility/2)))
            open_price = prices[i-1] if i > 0 else initial_price
            volume = int(abs(np.random.normal(1000000, 200000)))
            
            data.append({
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close,
                'Volume': volume
            })
        
        df = pd.DataFrame(data, index=dates[:len(prices)])
        return df
    
    @staticmethod
    def generate_with_cycles(symbol: str = "DEMO", days: int = 730,
                            initial_price: float = 100.0) -> pd.DataFrame:
        """
        Generate synthetic data with market cycles
        
        Args:
            symbol: Ticker symbol
            days: Number of days
            initial_price: Starting price
            
        Returns:
            DataFrame with OHLCV data
        """
        np.random.seed(42)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Create cyclic pattern with noise
        t = np.linspace(0, 4*np.pi, days)
        trend = initial_price + 20 * np.sin(t) + 0.05 * t
        noise = np.random.normal(0, 2, days)
        prices = trend + noise
        
        # Ensure prices are positive
        prices = np.maximum(prices, initial_price * 0.5)
        
        # Generate OHLCV data
        data = []
        for i, date in enumerate(dates[:len(prices)]):
            close = prices[i]
            high = close * (1 + abs(np.random.normal(0, 0.01)))
            low = close * (1 - abs(np.random.normal(0, 0.01)))
            open_price = prices[i-1] if i > 0 else initial_price
            volume = int(abs(np.random.normal(1000000, 200000)))
            
            data.append({
                'Open': open_price,
                'High': high,
                'Low': low,
                'Close': close,
                'Volume': volume
            })
        
        df = pd.DataFrame(data, index=dates[:len(prices)])
        return df
