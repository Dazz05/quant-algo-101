"""
Risk Management Module
Manages position sizing, stop losses, and risk controls
"""

from typing import Dict, Optional


class RiskManager:
    """Manages trading risk and position sizing"""
    
    def __init__(self, max_position_size: float = 0.1, stop_loss_pct: float = 0.02, 
                 take_profit_pct: float = 0.05):
        """
        Initialize risk manager
        
        Args:
            max_position_size: Maximum position size as fraction of capital (0.1 = 10%)
            stop_loss_pct: Stop loss percentage (0.02 = 2%)
            take_profit_pct: Take profit percentage (0.05 = 5%)
        """
        self.max_position_size = max_position_size
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        
    def calculate_position_size(self, capital: float, price: float) -> int:
        """
        Calculate position size based on available capital
        
        Args:
            capital: Available trading capital
            price: Current asset price
            
        Returns:
            Number of shares to trade
        """
        max_investment = capital * self.max_position_size
        shares = int(max_investment / price)
        return shares
    
    def check_stop_loss(self, entry_price: float, current_price: float, 
                       position_type: str = "long") -> bool:
        """
        Check if stop loss should be triggered
        
        Args:
            entry_price: Entry price of the position
            current_price: Current market price
            position_type: "long" or "short"
            
        Returns:
            True if stop loss triggered, False otherwise
        """
        if position_type == "long":
            loss_pct = (entry_price - current_price) / entry_price
            return loss_pct >= self.stop_loss_pct
        else:  # short position
            loss_pct = (current_price - entry_price) / entry_price
            return loss_pct >= self.stop_loss_pct
    
    def check_take_profit(self, entry_price: float, current_price: float, 
                         position_type: str = "long") -> bool:
        """
        Check if take profit should be triggered
        
        Args:
            entry_price: Entry price of the position
            current_price: Current market price
            position_type: "long" or "short"
            
        Returns:
            True if take profit triggered, False otherwise
        """
        if position_type == "long":
            profit_pct = (current_price - entry_price) / entry_price
            return profit_pct >= self.take_profit_pct
        else:  # short position
            profit_pct = (entry_price - current_price) / entry_price
            return profit_pct >= self.take_profit_pct
    
    def validate_trade(self, capital: float, price: float, quantity: int) -> Dict:
        """
        Validate if trade meets risk criteria
        
        Args:
            capital: Available capital
            price: Trade price
            quantity: Number of shares
            
        Returns:
            Dictionary with validation result and message
        """
        trade_value = price * quantity
        position_pct = trade_value / capital
        
        if position_pct > self.max_position_size:
            return {
                'valid': False,
                'message': f'Position size {position_pct:.1%} exceeds maximum {self.max_position_size:.1%}'
            }
        
        if trade_value > capital:
            return {
                'valid': False,
                'message': 'Insufficient capital for trade'
            }
        
        return {'valid': True, 'message': 'Trade validated'}
