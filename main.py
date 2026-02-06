#!/usr/bin/env python3
"""
Main entry point for the automated trading bot
"""

from trading_bot.bot import TradingBot
from trading_bot.strategies.moving_average_crossover import MovingAverageCrossover
from trading_bot.utils.risk_manager import RiskManager
from config import TRADING_CONFIG, STRATEGY_CONFIG, RISK_CONFIG


def main():
    """Main function to run the trading bot"""
    
    print("\n" + "="*60)
    print("AUTOMATED QUANTITATIVE TRADING BOT")
    print("="*60 + "\n")
    
    # Initialize strategy
    strategy = MovingAverageCrossover(
        fast_period=STRATEGY_CONFIG['fast_period'],
        slow_period=STRATEGY_CONFIG['slow_period']
    )
    
    # Initialize risk manager
    risk_manager = RiskManager(
        max_position_size=RISK_CONFIG['max_position_size'],
        stop_loss_pct=RISK_CONFIG['stop_loss_pct'],
        take_profit_pct=RISK_CONFIG['take_profit_pct']
    )
    
    # Initialize trading bot
    bot = TradingBot(
        symbol=TRADING_CONFIG['symbol'],
        strategy=strategy,
        initial_capital=TRADING_CONFIG['initial_capital'],
        risk_manager=risk_manager
    )
    
    # Run backtest
    results = bot.run_backtest(period=TRADING_CONFIG['backtest_period'])
    
    # Get current signal
    print("\nCURRENT MARKET SIGNAL:")
    print("-" * 60)
    current_signal = bot.get_current_signal()
    print(f"Symbol: {current_signal['symbol']}")
    print(f"Date: {current_signal['date']}")
    print(f"Price: ${current_signal['price']:.2f}")
    print(f"Signal: {current_signal['action']}")
    print("-" * 60 + "\n")


if __name__ == "__main__":
    main()
