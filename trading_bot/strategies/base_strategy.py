"""
Base Strategy Class
Abstract base class for all trading strategies
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Optional


class BaseStrategy(ABC):
    """Abstract base class for trading strategies"""
    
    def __init__(self, name: str):
        """
        Initialize strategy
        
        Args:
            name: Strategy name
        """
        self.name = name
        self.position = 0  # Current position: 0 (no position), 1 (long), -1 (short)
        self.trades = []  # History of trades
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy
        
        Args:
            data: DataFrame with market data and indicators
            
        Returns:
            DataFrame with signals column (1 for buy, -1 for sell, 0 for hold)
        """
        pass
    
    def execute_trade(self, signal: int, price: float, timestamp: pd.Timestamp):
        """
        Execute a trade based on the signal
        
        Args:
            signal: Trading signal (1 for buy, -1 for sell, 0 for hold)
            price: Execution price
            timestamp: Trade timestamp
        """
        if signal != 0 and signal != self.position:
            trade = {
                'timestamp': timestamp,
                'action': 'BUY' if signal == 1 else 'SELL',
                'price': price,
                'position': signal
            }
            self.trades.append(trade)
            self.position = signal
            
    def get_performance_metrics(self) -> Dict:
        """
        Calculate performance metrics
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.trades:
            return {'total_trades': 0, 'status': 'No trades executed'}
        
        return {
            'total_trades': len(self.trades),
            'last_trade': self.trades[-1] if self.trades else None,
            'current_position': self.position
        }
