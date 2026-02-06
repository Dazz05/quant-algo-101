#!/usr/bin/env python3
"""
Demo script using synthetic data
Demonstrates the trading bot without requiring external data sources
"""

import pandas as pd
from trading_bot.bot import TradingBot
from trading_bot.strategies.moving_average_crossover import MovingAverageCrossover
from trading_bot.utils.risk_manager import RiskManager
from trading_bot.data.synthetic_data import SyntheticDataGenerator


class DemoTradingBot(TradingBot):
    """Trading bot that uses synthetic data for demo purposes"""
    
    def fetch_data(self, period: str = "1y") -> pd.DataFrame:
        """Override fetch_data to use synthetic data"""
        print(f"Using synthetic data for demo (no internet connection required)")
        
        # Parse period to days
        period_days = {
            '1mo': 30,
            '3mo': 90,
            '6mo': 180,
            '1y': 365,
            '2y': 730,
            '5y': 1825
        }
        days = period_days.get(period, 730)
        
        # Generate synthetic data
        generator = SyntheticDataGenerator()
        data = generator.generate_with_cycles(
            symbol=self.symbol,
            days=days,
            initial_price=150.0
        )
        
        return data


def main():
    """Main demo function"""
    
    print("\n" + "="*60)
    print("AUTOMATED QUANTITATIVE TRADING BOT - DEMO MODE")
    print("="*60)
    print("\nThis demo uses synthetic market data to demonstrate")
    print("the bot's capabilities without requiring internet access.")
    print("="*60 + "\n")
    
    # Initialize strategy
    strategy = MovingAverageCrossover(fast_period=50, slow_period=200)
    
    # Initialize risk manager
    risk_manager = RiskManager(
        max_position_size=0.2,
        stop_loss_pct=0.02,
        take_profit_pct=0.05
    )
    
    # Initialize demo trading bot
    bot = DemoTradingBot(
        symbol='DEMO',
        strategy=strategy,
        initial_capital=10000,
        risk_manager=risk_manager
    )
    
    # Run backtest
    results = bot.run_backtest(period='2y')
    
    # Get current signal (using recent data)
    print("\nCURRENT MARKET SIGNAL (Latest Data Point):")
    print("-" * 60)
    print("Symbol: DEMO")
    print("Action: Based on Moving Average Crossover Strategy")
    print("-" * 60 + "\n")
    
    print("="*60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nTo use with real data:")
    print("1. Ensure you have internet connection")
    print("2. Run: python main.py")
    print("3. Edit config.py to change symbols and parameters")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
