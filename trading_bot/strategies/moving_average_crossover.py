"""
Moving Average Crossover Strategy
Classic trend-following strategy using two moving averages
"""

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class MovingAverageCrossover(BaseStrategy):
    """
    Moving Average Crossover Strategy
    Generates buy signal when fast MA crosses above slow MA
    Generates sell signal when fast MA crosses below slow MA
    """
    
    def __init__(self, fast_period: int = 50, slow_period: int = 200):
        """
        Initialize MA Crossover strategy
        
        Args:
            fast_period: Period for fast moving average
            slow_period: Period for slow moving average
        """
        super().__init__(name=f"MA_Crossover_{fast_period}_{slow_period}")
        self.fast_period = fast_period
        self.slow_period = slow_period
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on MA crossover
        
        Args:
            data: DataFrame with Close prices
            
        Returns:
            DataFrame with signals
        """
        df = data.copy()
        
        # Calculate moving averages
        df[f'MA_fast'] = df['Close'].rolling(window=self.fast_period).mean()
        df[f'MA_slow'] = df['Close'].rolling(window=self.slow_period).mean()
        
        # Initialize signal column
        df['signal'] = 0
        
        # Generate signals
        # Buy signal: fast MA crosses above slow MA
        df.loc[df[f'MA_fast'] > df[f'MA_slow'], 'signal'] = 1
        # Sell signal: fast MA crosses below slow MA
        df.loc[df[f'MA_fast'] < df[f'MA_slow'], 'signal'] = -1
        
        # Detect crossovers (changes in signal)
        df['position'] = df['signal'].diff()
        
        return df
    
    def backtest(self, data: pd.DataFrame, initial_capital: float = 10000) -> Dict:
        """
        Backtest the strategy
        
        Args:
            data: Historical market data
            initial_capital: Starting capital
            
        Returns:
            Dictionary with backtest results
        """
        df = self.generate_signals(data)
        
        # Calculate returns
        df['returns'] = df['Close'].pct_change()
        df['strategy_returns'] = df['signal'].shift(1) * df['returns']
        
        # Calculate cumulative returns
        df['cumulative_returns'] = (1 + df['returns']).cumprod()
        df['cumulative_strategy_returns'] = (1 + df['strategy_returns']).cumprod()
        
        # Calculate portfolio value
        df['portfolio_value'] = initial_capital * df['cumulative_strategy_returns']
        
        # Calculate metrics
        total_return = (df['portfolio_value'].iloc[-1] - initial_capital) / initial_capital * 100
        
        # Count trades
        trades = df[df['position'] != 0].shape[0]
        
        return {
            'initial_capital': initial_capital,
            'final_value': df['portfolio_value'].iloc[-1],
            'total_return': total_return,
            'total_trades': trades,
            'data': df
        }
