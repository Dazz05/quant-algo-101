"""
Main Trading Bot
Orchestrates data fetching, strategy execution, and trade management
"""

import pandas as pd
from datetime import datetime
from typing import Optional
from .data.data_fetcher import DataFetcher
from .strategies.base_strategy import BaseStrategy
from .utils.risk_manager import RiskManager


class TradingBot:
    """Automated trading bot that executes trading strategies"""
    
    def __init__(self, symbol: str, strategy: BaseStrategy, 
                 initial_capital: float = 10000, risk_manager: Optional[RiskManager] = None):
        """
        Initialize trading bot
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            strategy: Trading strategy instance
            initial_capital: Starting capital
            risk_manager: Risk manager instance (optional)
        """
        self.symbol = symbol
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.risk_manager = risk_manager or RiskManager()
        self.data_fetcher = DataFetcher(symbol)
        self.portfolio = {
            'cash': initial_capital,
            'shares': 0,
            'value': initial_capital
        }
        self.trade_history = []
        
    def fetch_data(self, period: str = "1y") -> pd.DataFrame:
        """
        Fetch market data for analysis
        
        Args:
            period: Data period to fetch
            
        Returns:
            DataFrame with market data
        """
        data = self.data_fetcher.fetch_historical_data(period=period)
        return data
    
    def run_backtest(self, period: str = "1y") -> dict:
        """
        Run backtest on historical data
        
        Args:
            period: Historical period to backtest
            
        Returns:
            Dictionary with backtest results
        """
        print(f"\n{'='*60}")
        print(f"Running backtest for {self.symbol}")
        print(f"Strategy: {self.strategy.name}")
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print(f"{'='*60}\n")
        
        # Fetch historical data
        data = self.fetch_data(period=period)
        
        # Generate signals
        signals_df = self.strategy.generate_signals(data)
        
        # Simulate trading
        position = 0
        entry_price = 0
        shares = 0
        cash = self.initial_capital
        
        for idx, row in signals_df.iterrows():
            current_price = row['Close']
            signal = row['signal']
            
            # Skip if not enough data
            if pd.isna(signal) or pd.isna(current_price):
                continue
            
            # Buy signal
            if signal == 1 and position == 0:
                shares = self.risk_manager.calculate_position_size(cash, current_price)
                if shares > 0:
                    cost = shares * current_price
                    if cost <= cash:
                        cash -= cost
                        position = 1
                        entry_price = current_price
                        self.trade_history.append({
                            'date': idx,
                            'action': 'BUY',
                            'price': current_price,
                            'shares': shares,
                            'value': cost
                        })
            
            # Sell signal
            elif signal == -1 and position == 1:
                revenue = shares * current_price
                cash += revenue
                profit = revenue - (shares * entry_price)
                self.trade_history.append({
                    'date': idx,
                    'action': 'SELL',
                    'price': current_price,
                    'shares': shares,
                    'value': revenue,
                    'profit': profit
                })
                position = 0
                shares = 0
        
        # Close any open position at the end
        if position == 1:
            final_price = signals_df['Close'].iloc[-1]
            revenue = shares * final_price
            cash += revenue
            profit = revenue - (shares * entry_price)
            self.trade_history.append({
                'date': signals_df.index[-1],
                'action': 'SELL (Close)',
                'price': final_price,
                'shares': shares,
                'value': revenue,
                'profit': profit
            })
        
        # Calculate final portfolio value
        final_value = cash
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100
        
        results = {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_trades': len(self.trade_history),
            'trade_history': self.trade_history
        }
        
        self._print_results(results)
        
        return results
    
    def _print_results(self, results: dict):
        """Print backtest results"""
        print(f"\n{'='*60}")
        print("BACKTEST RESULTS")
        print(f"{'='*60}")
        print(f"Initial Capital:  ${results['initial_capital']:,.2f}")
        print(f"Final Value:      ${results['final_value']:,.2f}")
        print(f"Total Return:     {results['total_return']:.2f}%")
        print(f"Total Trades:     {results['total_trades']}")
        print(f"{'='*60}\n")
        
        if results['trade_history']:
            print("Trade History:")
            print(f"{'Date':<12} {'Action':<12} {'Price':<12} {'Shares':<10} {'Value':<12} {'Profit':<12}")
            print("-" * 80)
            for trade in results['trade_history']:
                date_str = trade['date'].strftime('%Y-%m-%d') if hasattr(trade['date'], 'strftime') else str(trade['date'])
                profit_str = f"${trade.get('profit', 0):,.2f}" if 'profit' in trade else '-'
                print(f"{date_str:<12} {trade['action']:<12} ${trade['price']:<11.2f} {trade['shares']:<10} ${trade['value']:<11.2f} {profit_str:<12}")
        
        print(f"\n{'='*60}\n")
    
    def get_current_signal(self) -> dict:
        """
        Get current trading signal
        
        Returns:
            Dictionary with current signal and price
        """
        # Fetch recent data
        data = self.data_fetcher.fetch_historical_data(period="3mo")
        
        # Generate signals
        signals_df = self.strategy.generate_signals(data)
        
        # Get latest signal
        latest = signals_df.iloc[-1]
        
        return {
            'symbol': self.symbol,
            'date': signals_df.index[-1],
            'price': latest['Close'],
            'signal': latest['signal'],
            'action': 'BUY' if latest['signal'] == 1 else 'SELL' if latest['signal'] == -1 else 'HOLD'
        }
