"""
Configuration file for trading bot
"""

# Trading Configuration
TRADING_CONFIG = {
    'symbol': 'AAPL',  # Trading symbol
    'initial_capital': 10000,  # Starting capital in USD
    'backtest_period': '2y',  # Period for backtesting
}

# Strategy Configuration
STRATEGY_CONFIG = {
    'fast_period': 50,  # Fast moving average period
    'slow_period': 200,  # Slow moving average period
}

# Risk Management Configuration
RISK_CONFIG = {
    'max_position_size': 0.2,  # Maximum 20% of capital per position
    'stop_loss_pct': 0.02,  # 2% stop loss
    'take_profit_pct': 0.05,  # 5% take profit
}

# Data Configuration
DATA_CONFIG = {
    'interval': '1d',  # Daily data
}
