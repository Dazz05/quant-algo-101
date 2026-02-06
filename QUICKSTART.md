# Quick Start Guide

## Getting Started in 3 Minutes

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/Dazz05/quant-algo-101.git
cd quant-algo-101

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Demo (No Internet Required)
```bash
python demo.py
```

This will run a complete backtest using synthetic data and show you:
- Initial and final portfolio values
- Total return percentage
- Complete trade history
- Current market signal

### 3. Run Tests
```bash
python test_bot.py
```

Validates all core functionality:
- ✓ Synthetic data generation
- ✓ Moving average strategy
- ✓ Risk management
- ✓ Backtesting engine

### 4. Customize Your Strategy

Edit `config.py`:
```python
TRADING_CONFIG = {
    'symbol': 'TSLA',           # Change to any stock
    'initial_capital': 50000,    # Your starting capital
    'backtest_period': '1y',     # Test period
}

STRATEGY_CONFIG = {
    'fast_period': 20,           # Faster = more trades
    'slow_period': 100,          # Slower = fewer trades
}
```

### 5. Run with Real Data
```bash
python main.py
```

**Note:** Requires internet connection to fetch real market data from Yahoo Finance.

## What's Included

- 📊 **Backtesting Engine** - Test strategies before risking real money
- 🎯 **Signal Generation** - Get current buy/sell recommendations  
- 🛡️ **Risk Management** - Automatic position sizing and stop-losses
- 📈 **Technical Analysis** - Moving averages and indicators
- 🧪 **Testing Suite** - Validate functionality

## Next Steps

1. Study the example in `examples.py`
2. Read the full documentation in `README.md`
3. Experiment with different strategy parameters
4. Create your own custom strategies

## Need Help?

- Check `README.md` for detailed documentation
- Review `examples.py` for usage patterns
- Run `demo.py` to see the bot in action

---

**⚠️ Important:** This is for educational purposes. Always test thoroughly before considering live trading.
