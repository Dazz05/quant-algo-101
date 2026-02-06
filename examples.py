#!/usr/bin/env python3
"""
Example usage of the trading bot with different configurations
"""

from trading_bot.bot import TradingBot
from trading_bot.strategies.moving_average_crossover import MovingAverageCrossover
from trading_bot.utils.risk_manager import RiskManager


def example_basic_backtest():
    """Example: Basic backtest with default settings"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Backtest")
    print("="*60)
    
    # Create strategy
    strategy = MovingAverageCrossover(fast_period=50, slow_period=200)
    
    # Create bot
    bot = TradingBot(symbol='AAPL', strategy=strategy, initial_capital=10000)
    
    # Run backtest
    results = bot.run_backtest(period='1y')
    
    return results


def example_custom_strategy_parameters():
    """Example: Custom strategy parameters"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Strategy Parameters")
    print("="*60)
    
    # Create strategy with custom parameters
    strategy = MovingAverageCrossover(fast_period=20, slow_period=50)
    
    # Create bot
    bot = TradingBot(symbol='MSFT', strategy=strategy, initial_capital=5000)
    
    # Run backtest
    results = bot.run_backtest(period='6mo')
    
    return results


def example_with_risk_management():
    """Example: Bot with custom risk management"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Risk Management")
    print("="*60)
    
    # Create strategy
    strategy = MovingAverageCrossover(fast_period=50, slow_period=200)
    
    # Create custom risk manager
    risk_manager = RiskManager(
        max_position_size=0.15,  # 15% max position
        stop_loss_pct=0.03,      # 3% stop loss
        take_profit_pct=0.08     # 8% take profit
    )
    
    # Create bot with risk manager
    bot = TradingBot(
        symbol='GOOGL',
        strategy=strategy,
        initial_capital=15000,
        risk_manager=risk_manager
    )
    
    # Run backtest
    results = bot.run_backtest(period='2y')
    
    return results


def example_current_signals():
    """Example: Get current trading signals for multiple stocks"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Current Trading Signals")
    print("="*60)
    
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    strategy = MovingAverageCrossover(fast_period=50, slow_period=200)
    
    print("\nCurrent Signals:")
    print("-" * 60)
    
    for symbol in symbols:
        bot = TradingBot(symbol=symbol, strategy=strategy)
        signal = bot.get_current_signal()
        print(f"{signal['symbol']:<8} ${signal['price']:>8.2f}  {signal['action']:>6}")
    
    print("-" * 60)


if __name__ == "__main__":
    # Run examples
    print("\n" + "="*60)
    print("TRADING BOT EXAMPLES")
    print("="*60)
    
    # Example 1: Basic backtest
    example_basic_backtest()
    
    # Example 2: Custom parameters
    # example_custom_strategy_parameters()
    
    # Example 3: With risk management
    # example_with_risk_management()
    
    # Example 4: Current signals
    # example_current_signals()
    
    print("\nExamples completed!")
