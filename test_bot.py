#!/usr/bin/env python3
"""
Simple test file for the trading bot
"""

import pandas as pd
import numpy as np
from trading_bot.strategies.moving_average_crossover import MovingAverageCrossover
from trading_bot.utils.risk_manager import RiskManager
from trading_bot.data.synthetic_data import SyntheticDataGenerator


def test_synthetic_data_generator():
    """Test synthetic data generation"""
    print("\n[TEST] Synthetic Data Generator...")
    generator = SyntheticDataGenerator()
    data = generator.generate_trending_data(days=100)
    
    assert not data.empty, "Data should not be empty"
    assert len(data) == 100, f"Expected 100 rows, got {len(data)}"
    assert all(col in data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']), \
        "Missing required columns"
    
    print("✓ Synthetic data generator working correctly")
    return True


def test_moving_average_strategy():
    """Test moving average crossover strategy"""
    print("\n[TEST] Moving Average Crossover Strategy...")
    
    # Generate test data
    generator = SyntheticDataGenerator()
    data = generator.generate_trending_data(days=300)
    
    # Create strategy
    strategy = MovingAverageCrossover(fast_period=20, slow_period=50)
    
    # Generate signals
    signals = strategy.generate_signals(data)
    
    assert 'signal' in signals.columns, "Signal column missing"
    assert 'MA_fast' in signals.columns, "Fast MA missing"
    assert 'MA_slow' in signals.columns, "Slow MA missing"
    
    # Check that signals are valid
    unique_signals = signals['signal'].dropna().unique()
    assert all(s in [-1, 0, 1] for s in unique_signals), "Invalid signal values"
    
    print("✓ Moving average strategy working correctly")
    return True


def test_risk_manager():
    """Test risk manager"""
    print("\n[TEST] Risk Manager...")
    
    risk_manager = RiskManager(
        max_position_size=0.1,
        stop_loss_pct=0.02,
        take_profit_pct=0.05
    )
    
    # Test position sizing
    capital = 10000
    price = 100
    shares = risk_manager.calculate_position_size(capital, price)
    
    assert shares > 0, "Position size should be positive"
    assert shares * price <= capital * 0.1, "Position size exceeds maximum"
    
    # Test stop loss
    entry_price = 100
    current_price = 97.5
    stop_triggered = risk_manager.check_stop_loss(entry_price, current_price, "long")
    assert stop_triggered, "Stop loss should trigger at 2.5% loss with 2% threshold"
    
    # Test take profit
    current_price = 105.5
    profit_triggered = risk_manager.check_take_profit(entry_price, current_price, "long")
    assert profit_triggered, "Take profit should trigger at 5.5% gain with 5% threshold"
    
    print("✓ Risk manager working correctly")
    return True


def test_strategy_backtest():
    """Test strategy backtesting"""
    print("\n[TEST] Strategy Backtesting...")
    
    # Generate test data
    generator = SyntheticDataGenerator()
    data = generator.generate_trending_data(days=300, trend=0.0005)
    
    # Create and test strategy
    strategy = MovingAverageCrossover(fast_period=20, slow_period=50)
    results = strategy.backtest(data, initial_capital=10000)
    
    assert 'initial_capital' in results, "Missing initial_capital"
    assert 'final_value' in results, "Missing final_value"
    assert 'total_return' in results, "Missing total_return"
    assert 'total_trades' in results, "Missing total_trades"
    
    print(f"  Initial Capital: ${results['initial_capital']:,.2f}")
    print(f"  Final Value: ${results['final_value']:,.2f}")
    print(f"  Total Return: {results['total_return']:.2f}%")
    print(f"  Total Trades: {results['total_trades']}")
    
    print("✓ Strategy backtesting working correctly")
    return True


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("RUNNING TRADING BOT TESTS")
    print("="*60)
    
    tests = [
        test_synthetic_data_generator,
        test_moving_average_strategy,
        test_risk_manager,
        test_strategy_backtest
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"TESTS COMPLETED: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
