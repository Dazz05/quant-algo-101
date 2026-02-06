# Quant Algo 101 - Automated Quantitative Trading Bot

An automated quantitative trading algorithm bot built with Python. This bot implements algorithmic trading strategies with backtesting capabilities, risk management, and real-time signal generation.

## Features

- 📊 **Automated Trading Strategies**: Implements moving average crossover and other quantitative strategies
- 📈 **Historical Data Fetching**: Retrieves market data using Yahoo Finance API
- 🔄 **Backtesting Engine**: Test strategies on historical data before live trading
- 🛡️ **Risk Management**: Built-in position sizing, stop-loss, and take-profit mechanisms
- 📉 **Technical Indicators**: Support for SMA, EMA, and custom indicators
- 🎯 **Signal Generation**: Real-time buy/sell signal generation

## Project Structure

```
quant-algo-101/
├── trading_bot/
│   ├── __init__.py
│   ├── bot.py                    # Main trading bot orchestrator
│   ├── data/
│   │   ├── __init__.py
│   │   └── data_fetcher.py       # Market data fetching module
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base_strategy.py      # Abstract base class for strategies
│   │   └── moving_average_crossover.py  # MA crossover strategy
│   └── utils/
│       ├── __init__.py
│       └── risk_manager.py       # Risk management utilities
├── config.py                      # Configuration settings
├── main.py                        # Main entry point
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Dazz05/quant-algo-101.git
cd quant-algo-101
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the trading bot with default settings:

```bash
python main.py
```

This will:
1. Initialize the trading bot with Apple (AAPL) stock
2. Run a backtest on 2 years of historical data
3. Display performance metrics and trade history
4. Show the current market signal

### Configuration

Edit `config.py` to customize the bot settings:

```python
# Trading Configuration
TRADING_CONFIG = {
    'symbol': 'AAPL',              # Change to your preferred stock symbol
    'initial_capital': 10000,       # Starting capital
    'backtest_period': '2y',        # Backtest period
}

# Strategy Configuration
STRATEGY_CONFIG = {
    'fast_period': 50,              # Fast MA period
    'slow_period': 200,             # Slow MA period
}

# Risk Management Configuration
RISK_CONFIG = {
    'max_position_size': 0.2,       # Max 20% per position
    'stop_loss_pct': 0.02,          # 2% stop loss
    'take_profit_pct': 0.05,        # 5% take profit
}
```

### Custom Strategy Implementation

Create your own trading strategy by extending the `BaseStrategy` class:

```python
from trading_bot.strategies.base_strategy import BaseStrategy
import pandas as pd

class MyCustomStrategy(BaseStrategy):
    def __init__(self):
        super().__init__(name="My Custom Strategy")
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        # Implement your strategy logic here
        df = data.copy()
        df['signal'] = 0  # Initialize signals
        # Your logic to set signals (1 for buy, -1 for sell, 0 for hold)
        return df
```

## Trading Strategies

### Moving Average Crossover

The default strategy uses a moving average crossover approach:

- **Buy Signal**: When the fast moving average (50-day) crosses above the slow moving average (200-day)
- **Sell Signal**: When the fast moving average crosses below the slow moving average
- **Hold**: When there is no crossover

This is a trend-following strategy that aims to capture medium to long-term trends.

## Risk Management

The bot includes built-in risk management features:

- **Position Sizing**: Limits the maximum position size as a percentage of total capital
- **Stop Loss**: Automatically exits positions at a predefined loss threshold
- **Take Profit**: Locks in profits at a predefined gain threshold
- **Capital Management**: Ensures trades don't exceed available capital

## Example Output

```
============================================================
AUTOMATED QUANTITATIVE TRADING BOT
============================================================

============================================================
Running backtest for AAPL
Strategy: MA_Crossover_50_200
Initial Capital: $10,000.00
============================================================

============================================================
BACKTEST RESULTS
============================================================
Initial Capital:  $10,000.00
Final Value:      $12,345.67
Total Return:     23.46%
Total Trades:     8
============================================================

Trade History:
Date         Action       Price        Shares     Value        Profit      
--------------------------------------------------------------------------------
2023-01-15   BUY          $145.23      137        $19,896.51   -           
2023-03-22   SELL         $158.45      137        $21,708.15   $1,673.14   
...
```

## Backtesting

The bot includes a comprehensive backtesting engine that:

1. Fetches historical market data
2. Generates trading signals based on the strategy
3. Simulates trade execution with realistic constraints
4. Calculates performance metrics including:
   - Total return
   - Number of trades
   - Trade history with entry/exit prices
   - Profit/loss per trade

## Data Sources

The bot uses Yahoo Finance (via `yfinance` library) to fetch market data. This provides:
- Historical OHLCV (Open, High, Low, Close, Volume) data
- Real-time price information
- Support for stocks, ETFs, and indices

## Limitations and Disclaimers

⚠️ **IMPORTANT DISCLAIMERS:**

- This is an educational project for learning quantitative trading concepts
- **NOT** intended for live trading without proper testing and validation
- Past performance does not guarantee future results
- Trading involves risk of loss
- Always test thoroughly before considering live trading
- Consult with financial professionals before making trading decisions

## Future Enhancements

Potential improvements and additions:

- [ ] More trading strategies (RSI, MACD, Bollinger Bands, etc.)
- [ ] Multi-asset portfolio management
- [ ] Live trading integration with broker APIs
- [ ] Advanced performance metrics (Sharpe ratio, max drawdown, etc.)
- [ ] Machine learning-based strategies
- [ ] Real-time monitoring dashboard
- [ ] Paper trading mode
- [ ] Notification system for trade signals

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please open an issue on GitHub.

---

**Happy Trading! 📈💰**
