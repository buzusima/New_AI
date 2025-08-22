"""
💰 Modern Position Manager
position_manager.py
การจัดการ positions แบบอัจฉริยะ สำหรับ Modern Rule-based Trading System
รองรับการปิด positions แบบ intelligent, portfolio optimization, และ risk management
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import MetaTrader5 as mt5
import numpy as np
from collections import deque, defaultdict
import statistics

class PositionType(Enum):
    """ประเภท Position"""
    BUY = "BUY"
    SELL = "SELL"

class PositionStatus(Enum):
    """สถานะ Position"""
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

class CloseReason(Enum):
    """เหตุผลการปิด Position"""
    PROFIT_TARGET = "PROFIT_TARGET"
    STOP_LOSS = "STOP_LOSS"
    PORTFOLIO_BALANCE = "PORTFOLIO_BALANCE"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"
    MANUAL = "MANUAL"
    EMERGENCY = "EMERGENCY"
    GRID_OPTIMIZATION = "GRID_OPTIMIZATION"
    CORRELATION_HEDGE = "CORRELATION_HEDGE"

@dataclass
class Position:
    """ข้อมูล Position"""
    ticket: int
    symbol: str
    type: PositionType
    volume: float
    open_price: float
    current_price: float
    profit: float
    swap: float
    commission: float
    open_time: datetime
    age_hours: float
    comment: str
    magic: int
    
    @property
    def total_profit(self) -> float:
        """กำไร/ขาดทุนรวม"""
        return self.profit + self.swap + self.commission
    
    @property
    def pips_profit(self) -> float:
        """กำไร/ขาดทุนในหน่วย pips"""
        if self.type == PositionType.BUY:
            return (self.current_price - self.open_price) * 10000
        else:
            return (self.open_price - self.current_price) * 10000

@dataclass
class PositionGroup:
    """กลุ่ม Positions"""
    positions: List[Position]
    total_volume: float
    total_profit: float
    avg_open_price: float
    position_type: PositionType
    
    @property
    def count(self) -> int:
        return len(self.positions)

@dataclass
class ProfitOpportunity:
    """โอกาสในการทำกำไร"""
    profitable_positions: List[Position]
    losing_positions: List[Position]
    net_profit: float
    profit_amount: float
    loss_amount: float
    confidence: float
    reasoning: str
    close_strategy: str

class PositionManager:
    """
    💰 Modern Position Manager
    
    ความสามารถ:
    - Smart position closing with multiple strategies
    - Portfolio balance optimization
    - Risk-based position management
    - Correlation-aware hedging
    - Performance tracking per strategy
    - Emergency protection mechanisms
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """
        Initialize Position Manager
        
        Args:
            mt5_connector: MT5 connection object
            config: Configuration settings
        """
        self.mt5_connector = mt5_connector
        self.config = config
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        
        # Position tracking
        self.active_positions: Dict[int, Position] = {}
        self.position_history = deque(maxlen=1000)
        self.last_position_update = datetime.min
        
        # Portfolio metrics
        self.portfolio_metrics = {
            "total_positions": 0,
            "buy_positions": 0,
            "sell_positions": 0,
            "total_profit": 0.0,
            "total_volume": 0.0,
            "avg_age_hours": 0.0,
            "position_balance": 0.5,  # 0=all sells, 1=all buys
            "risk_level": 0.0,
            "survivability_usage": 0.0
        }
        
        # Risk management settings
        self.max_loss_per_position = config.get("risk_management", {}).get("max_loss_per_position", 500)
        self.max_portfolio_loss = config.get("risk_management", {}).get("max_drawdown_percentage", 20) * 100
        self.correlation_threshold = 0.8
        
        # Performance tracking
        self.close_performance = {
            reason.value: {"count": 0, "success": 0, "total_profit": 0.0}
            for reason in CloseReason
        }
        
        # Position aging settings
        self.max_position_age_hours = 24 * 7  # 1 week
        self.aging_penalty_threshold = 24 * 3  # 3 days
        
        print("💰 Position Manager initialized")
        print(f"   Symbol: {self.symbol}")
        print(f"   Max loss per position: ${self.max_loss_per_position}")
        print(f"   Max portfolio loss: ${self.max_portfolio_loss}")
        print(f"   Position aging threshold: {self.aging_penalty_threshold} hours")
    
    def update_positions(self) -> bool:
        """Update active positions from MT5"""
        try:
            if not self.mt5_connector.is_connected:
                return False
            
            # Get positions from MT5
            mt5_positions = mt5.positions_get(symbol=self.symbol)
            if mt5_positions is None:
                mt5_positions = []
            
            # Clear current positions
            self.active_positions.clear()
            
            # Process each position
            for pos in mt5_positions:
                position = Position(
                    ticket=pos.ticket,
                    symbol=pos.symbol,
                    type=PositionType.BUY if pos.type == mt5.POSITION_TYPE_BUY else PositionType.SELL,
                    volume=pos.volume,
                    open_price=pos.price_open,
                    current_price=pos.price_current,
                    profit=pos.profit,
                    swap=pos.swap,
                    commission=pos.commission,
                    open_time=datetime.fromtimestamp(pos.time),
                    age_hours=(datetime.now() - datetime.fromtimestamp(pos.time)).total_seconds() / 3600,
                    comment=pos.comment,
                    magic=pos.magic
                )
                
                self.active_positions[pos.ticket] = position
            
            # Update portfolio metrics
            self._calculate_portfolio_metrics()
            
            self.last_position_update = datetime.now()
            return True
            
        except Exception as e:
            print(f"❌ Position update error: {e}")
            return False
    
    def _calculate_portfolio_metrics(self):
        """Calculate portfolio metrics"""
        try:
            positions = list(self.active_positions.values())
            
            if not positions:
                self.portfolio_metrics.update({
                    "total_positions": 0,
                    "buy_positions": 0,
                    "sell_positions": 0,
                    "total_profit": 0.0,
                    "total_volume": 0.0,
                    "avg_age_hours": 0.0,
                    "position_balance": 0.5,
                    "risk_level": 0.0,
                    "survivability_usage": 0.0
                })
                return
            
            # Basic counts
            total_positions = len(positions)
            buy_positions = sum(1 for p in positions if p.type == PositionType.BUY)
            sell_positions = total_positions - buy_positions
            
            # Financial metrics
            total_profit = sum(p.total_profit for p in positions)
            total_volume = sum(p.volume for p in positions)
            avg_age = statistics.mean([p.age_hours for p in positions])
            
            # Position balance (0=all sells, 1=all buys, 0.5=balanced)
            position_balance = buy_positions / total_positions if total_positions > 0 else 0.5
            
            # Risk level calculation
            losing_positions = [p for p in positions if p.total_profit < 0]
            total_loss = abs(sum(p.total_profit for p in losing_positions))
            account_balance = self.mt5_connector.get_account_info().get("balance", 10000)
            risk_level = min(1.0, total_loss / account_balance) if account_balance > 0 else 0.0
            
            # Survivability usage (how much of our drawdown capacity is used)
            max_survivable_loss = account_balance * 0.2  # 20% max drawdown
            survivability_usage = min(1.0, total_loss / max_survivable_loss) if max_survivable_loss > 0 else 0.0
            
            # Update metrics
            self.portfolio_metrics.update({
                "total_positions": total_positions,
                "buy_positions": buy_positions,
                "sell_positions": sell_positions,
                "total_profit": round(total_profit, 2),
                "total_volume": round(total_volume, 3),
                "avg_age_hours": round(avg_age, 1),
                "position_balance": round(position_balance, 3),
                "risk_level": round(risk_level, 3),
                "survivability_usage": round(survivability_usage, 3)
            })
            
        except Exception as e:
            print(f"❌ Portfolio metrics calculation error: {e}")
    
    def close_profitable_positions(self, confidence: float = 0.5, reasoning: str = "",
                                 min_profit: float = 10.0) -> bool:
        """
        Close profitable positions intelligently
        
        Args:
            confidence: Confidence level for closing
            reasoning: Reasoning for closing
            min_profit: Minimum profit threshold
            
        Returns:
            True if positions were closed
        """
        try:
            # Update positions first
            if not self.update_positions():
                print("❌ Cannot update positions for profitable closing")
                return False
            
            # Find profitable positions
            profitable_positions = [
                p for p in self.active_positions.values()
                if p.total_profit >= min_profit
            ]
            
            if not profitable_positions:
                print("💭 No profitable positions to close")
                return False
            
            # Sort by profit (highest first)
            profitable_positions.sort(key=lambda x: x.total_profit, reverse=True)
            
            # Determine how many to close based on confidence
            max_to_close = max(1, int(len(profitable_positions) * confidence))
            positions_to_close = profitable_positions[:max_to_close]
            
            print(f"🎯 Closing {len(positions_to_close)} profitable positions")
            print(f"💰 Total profit to realize: ${sum(p.total_profit for p in positions_to_close):.2f}")
            
            # Close positions
            closed_count = 0
            total_profit = 0.0
            
            for position in positions_to_close:
                if self._close_position(position, CloseReason.PROFIT_TARGET, reasoning):
                    closed_count += 1
                    total_profit += position.total_profit
                    print(f"   ✅ Closed #{position.ticket}: ${position.total_profit:.2f}")
                else:
                    print(f"   ❌ Failed to close #{position.ticket}")
                
                time.sleep(0.1)  # Small delay between closes
            
            if closed_count > 0:
                print(f"🎉 Successfully closed {closed_count} positions")
                print(f"💰 Total profit realized: ${total_profit:.2f}")
                
                # Track performance
                self._track_close_performance(CloseReason.PROFIT_TARGET, True, total_profit)
                return True
            else:
                print("❌ No positions were closed")
                self._track_close_performance(CloseReason.PROFIT_TARGET, False)
                return False
                
        except Exception as e:
            print(f"❌ Close profitable positions error: {e}")
            return False
    
    def close_losing_positions(self, confidence: float = 0.5, reasoning: str = "",
                             max_loss: float = -100.0) -> bool:
        """
        Close losing positions to limit damage
        
        Args:
            confidence: Confidence level for closing
            reasoning: Reasoning for closing
            max_loss: Maximum acceptable loss threshold
            
        Returns:
            True if positions were closed
        """
        try:
            # Update positions first
            if not self.update_positions():
                print("❌ Cannot update positions for losing closing")
                return False
            
            # Find losing positions beyond threshold
            losing_positions = [
                p for p in self.active_positions.values()
                if p.total_profit <= max_loss
            ]
            
            if not losing_positions:
                print("💭 No losing positions beyond threshold to close")
                return False
            
            # Sort by loss (worst first)
            losing_positions.sort(key=lambda x: x.total_profit)
            
            # Determine how many to close based on confidence
            max_to_close = max(1, int(len(losing_positions) * confidence))
            positions_to_close = losing_positions[:max_to_close]
            
            print(f"🛡️ Closing {len(positions_to_close)} losing positions")
            print(f"📉 Total loss to cut: ${sum(p.total_profit for p in positions_to_close):.2f}")
            
            # Close positions
            closed_count = 0
            total_loss = 0.0
            
            for position in positions_to_close:
                if self._close_position(position, CloseReason.STOP_LOSS, reasoning):
                    closed_count += 1
                    total_loss += position.total_profit
                    print(f"   ✅ Closed #{position.ticket}: ${position.total_profit:.2f}")
                else:
                    print(f"   ❌ Failed to close #{position.ticket}")
                
                time.sleep(0.1)  # Small delay between closes
            
            if closed_count > 0:
                print(f"🛡️ Successfully closed {closed_count} losing positions")
                print(f"📉 Total loss cut: ${total_loss:.2f}")
                
                # Track performance
                self._track_close_performance(CloseReason.STOP_LOSS, True, total_loss)
                return True
            else:
                print("❌ No losing positions were closed")
                self._track_close_performance(CloseReason.STOP_LOSS, False)
                return False
                
        except Exception as e:
            print(f"❌ Close losing positions error: {e}")
            return False
    
    def find_profit_opportunities(self, min_net_profit: float = 50.0) -> List[ProfitOpportunity]:
        """
        Find opportunities to close profitable and losing positions together
        
        Args:
            min_net_profit: Minimum net profit required
            
        Returns:
            List of profit opportunities
        """
        try:
            # Update positions first
            if not self.update_positions():
                return []
            
            positions = list(self.active_positions.values())
            if not positions:
                return []
            
            # Separate positions by profit/loss
            profitable_positions = [p for p in positions if p.total_profit > 0]
            losing_positions = [p for p in positions if p.total_profit < 0]
            
            if not profitable_positions or not losing_positions:
                return []
            
            opportunities = []
            
            # Strategy 1: Close equal numbers of profitable and losing
            for profit_count in range(1, min(len(profitable_positions), len(losing_positions)) + 1):
                # Get top profitable positions
                top_profitable = sorted(profitable_positions, key=lambda x: x.total_profit, reverse=True)[:profit_count]
                
                # Get worst losing positions
                worst_losing = sorted(losing_positions, key=lambda x: x.total_profit)[:profit_count]
                
                profit_amount = sum(p.total_profit for p in top_profitable)
                loss_amount = abs(sum(p.total_profit for p in worst_losing))
                net_profit = profit_amount - loss_amount
                
                if net_profit >= min_net_profit:
                    confidence = min(0.9, (net_profit / min_net_profit) * 0.5 + 0.3)
                    
                    opportunity = ProfitOpportunity(
                        profitable_positions=top_profitable,
                        losing_positions=worst_losing,
                        net_profit=net_profit,
                        profit_amount=profit_amount,
                        loss_amount=loss_amount,
                        confidence=confidence,
                        reasoning=f"Balance close: {profit_count} profitable + {profit_count} losing positions",
                        close_strategy="BALANCED_CLOSE"
                    )
                    opportunities.append(opportunity)
            
            # Strategy 2: Volume-weighted closing
            total_buy_volume = sum(p.volume for p in positions if p.type == PositionType.BUY)
            total_sell_volume = sum(p.volume for p in positions if p.type == PositionType.SELL)
            
            if total_buy_volume > 0 and total_sell_volume > 0:
                # Find opposing positions that can hedge each other
                buy_positions = [p for p in positions if p.type == PositionType.BUY]
                sell_positions = [p for p in positions if p.type == PositionType.SELL]
                
                for buy_pos in buy_positions:
                    for sell_pos in sell_positions:
                        if abs(buy_pos.volume - sell_pos.volume) < 0.005:  # Similar volumes
                            combined_profit = buy_pos.total_profit + sell_pos.total_profit
                            
                            if combined_profit >= min_net_profit:
                                confidence = min(0.8, (combined_profit / min_net_profit) * 0.4 + 0.4)
                                
                                opportunity = ProfitOpportunity(
                                    profitable_positions=[buy_pos, sell_pos] if combined_profit > 0 else [],
                                    losing_positions=[] if combined_profit > 0 else [buy_pos, sell_pos],
                                    net_profit=combined_profit,
                                    profit_amount=max(0, combined_profit),
                                    loss_amount=abs(min(0, combined_profit)),
                                    confidence=confidence,
                                    reasoning=f"Hedge close: BUY #{buy_pos.ticket} + SELL #{sell_pos.ticket}",
                                    close_strategy="HEDGE_CLOSE"
                                )
                                opportunities.append(opportunity)
            
            # Sort opportunities by net profit and confidence
            opportunities.sort(key=lambda x: x.net_profit * x.confidence, reverse=True)
            
            return opportunities[:5]  # Return top 5 opportunities
            
        except Exception as e:
            print(f"❌ Find profit opportunities error: {e}")
            return []
    
    def execute_profit_opportunity(self, opportunity: ProfitOpportunity) -> bool:
        """Execute a profit opportunity"""
        try:
            print(f"🎯 Executing profit opportunity: {opportunity.close_strategy}")
            print(f"💰 Expected net profit: ${opportunity.net_profit:.2f}")
            print(f"🎲 Confidence: {opportunity.confidence:.1%}")
            print(f"💭 Reasoning: {opportunity.reasoning}")
            
            closed_count = 0
            actual_profit = 0.0
            
            # Close profitable positions
            for position in opportunity.profitable_positions:
                if self._close_position(position, CloseReason.GRID_OPTIMIZATION, opportunity.reasoning):
                    closed_count += 1
                    actual_profit += position.total_profit
                    print(f"   ✅ Closed profitable #{position.ticket}: ${position.total_profit:.2f}")
                else:
                    print(f"   ❌ Failed to close profitable #{position.ticket}")
                
                time.sleep(0.1)
            
            # Close losing positions
            for position in opportunity.losing_positions:
                if self._close_position(position, CloseReason.GRID_OPTIMIZATION, opportunity.reasoning):
                    closed_count += 1
                    actual_profit += position.total_profit
                    print(f"   ✅ Closed losing #{position.ticket}: ${position.total_profit:.2f}")
                else:
                    print(f"   ❌ Failed to close losing #{position.ticket}")
                
                time.sleep(0.1)
            
            if closed_count > 0:
                print(f"🎉 Opportunity executed: {closed_count} positions closed")
                print(f"💰 Actual profit realized: ${actual_profit:.2f}")
                
                # Track performance
                self._track_close_performance(CloseReason.GRID_OPTIMIZATION, True, actual_profit)
                return True
            else:
                print("❌ No positions were closed")
                self._track_close_performance(CloseReason.GRID_OPTIMIZATION, False)
                return False
                
        except Exception as e:
            print(f"❌ Execute opportunity error: {e}")
            return False
    
    def close_aged_positions(self, max_age_hours: float = None) -> bool:
        """Close positions that are too old"""
        try:
            if max_age_hours is None:
                max_age_hours = self.max_position_age_hours
            
            # Update positions first
            if not self.update_positions():
                return False
            
            # Find aged positions
            aged_positions = [
                p for p in self.active_positions.values()
                if p.age_hours >= max_age_hours
            ]
            
            if not aged_positions:
                return False
            
            print(f"⏰ Closing {len(aged_positions)} aged positions (>{max_age_hours:.1f}h old)")
            
            closed_count = 0
            for position in aged_positions:
                if self._close_position(position, CloseReason.RISK_MANAGEMENT, f"Position age: {position.age_hours:.1f}h"):
                    closed_count += 1
                    print(f"   ✅ Closed aged #{position.ticket} ({position.age_hours:.1f}h old)")
                
                time.sleep(0.1)
            
            print(f"⏰ Closed {closed_count} aged positions")
            return closed_count > 0
            
        except Exception as e:
            print(f"❌ Close aged positions error: {e}")
            return False
    
    def emergency_close_all(self) -> bool:
        """Emergency close all positions"""
        try:
            print("🚨 EMERGENCY: Closing all positions")
            
            # Update positions first
            if not self.update_positions():
                return False
            
            positions = list(self.active_positions.values())
            if not positions:
                print("💭 No positions to close")
                return True
            
            closed_count = 0
            total_result = 0.0
            
            for position in positions:
                if self._close_position(position, CloseReason.EMERGENCY, "Emergency closure"):
                    closed_count += 1
                    total_result += position.total_profit
                    print(f"   🚨 Emergency closed #{position.ticket}: ${position.total_profit:.2f}")
                else:
                    print(f"   ❌ Failed to emergency close #{position.ticket}")
                
                time.sleep(0.05)  # Minimal delay for emergency
            
            print(f"🚨 Emergency closure completed: {closed_count}/{len(positions)} positions")
            print(f"💰 Total result: ${total_result:.2f}")
            
            return closed_count > 0
            
        except Exception as e:
            print(f"❌ Emergency close error: {e}")
            return False
    
    def _close_position(self, position: Position, reason: CloseReason, reasoning: str = "") -> bool:
        """Close a specific position"""
        try:
            if not self.mt5_connector.is_connected:
                return False
            
            # Prepare close request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_SELL if position.type == PositionType.BUY else mt5.ORDER_TYPE_BUY,
                "position": position.ticket,
                "deviation": 20,
                "magic": position.magic,
                "comment": f"Close:{reason.value}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Send close request
            result = mt5.order_send(request)
            
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                # Position closed successfully
                
                # Remove from active positions
                if position.ticket in self.active_positions:
                    del self.active_positions[position.ticket]
                
                # Add to history
                position_data = {
                    "ticket": position.ticket,
                    "close_time": datetime.now(),
                    "close_reason": reason.value,
                    "close_reasoning": reasoning,
                    "final_profit": position.total_profit,
                    "duration_hours": position.age_hours
                }
                self.position_history.append(position_data)
                
                return True
            else:
                error_msg = f"Close failed - Code: {result.retcode}" if result else "No result"
                print(f"❌ Close position {position.ticket} failed: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ Close position error: {e}")
            return False
    
    def _track_close_performance(self, reason: CloseReason, success: bool, profit: float = 0.0):
        """Track closing performance by reason"""
        try:
            reason_key = reason.value
            if reason_key in self.close_performance:
                self.close_performance[reason_key]["count"] += 1
                if success:
                    self.close_performance[reason_key]["success"] += 1
                self.close_performance[reason_key]["total_profit"] += profit
        except Exception as e:
            print(f"❌ Close performance tracking error: {e}")
    
    # === Public Interface Methods ===
    
    def get_portfolio_status(self) -> Dict[str, Any]:
        """Get comprehensive portfolio status"""
        try:
            # Update positions first
            self.update_positions()
            
            return self.portfolio_metrics.copy()
            
        except Exception as e:
            print(f"❌ Portfolio status error: {e}")
            return {}
    
    def get_position_summary(self) -> Dict[str, Any]:
        """Get detailed position summary"""
        try:
            # Update positions first
            self.update_positions()
            
            positions = list(self.active_positions.values())
            
            if not positions:
                return {
                    "total_positions": 0,
                    "profitable_positions": 0,
                    "losing_positions": 0,
                    "total_profit": 0.0,
                    "largest_profit": 0.0,
                    "largest_loss": 0.0,
                    "avg_position_age": 0.0,
                    "buy_sell_ratio": 0.5
                }
            
            profitable_positions = [p for p in positions if p.total_profit > 0]
            losing_positions = [p for p in positions if p.total_profit < 0]
            
            buy_positions = [p for p in positions if p.type == PositionType.BUY]
            sell_positions = [p for p in positions if p.type == PositionType.SELL]
            
            return {
                "total_positions": len(positions),
                "profitable_positions": len(profitable_positions),
                "losing_positions": len(losing_positions),
                "total_profit": round(sum(p.total_profit for p in positions), 2),
                "largest_profit": round(max([p.total_profit for p in positions] + [0]), 2),
                "largest_loss": round(min([p.total_profit for p in positions] + [0]), 2),
                "avg_position_age": round(statistics.mean([p.age_hours for p in positions]), 1),
                "buy_sell_ratio": len(buy_positions) / len(positions) if positions else 0.5,
                "buy_volume": round(sum(p.volume for p in buy_positions), 3),
                "sell_volume": round(sum(p.volume for p in sell_positions), 3),
                "oldest_position_age": round(max([p.age_hours for p in positions] + [0]), 1),
                "newest_position_age": round(min([p.age_hours for p in positions] + [24]), 1)
            }
            
        except Exception as e:
            print(f"❌ Position summary error: {e}")
            return {}
    
    def get_close_performance_stats(self) -> Dict[str, Dict]:
        """Get performance statistics by close reason"""
        try:
            stats = {}
            
            for reason, data in self.close_performance.items():
                if data["count"] > 0:
                    success_rate = data["success"] / data["count"]
                    avg_profit = data["total_profit"] / data["count"]
                else:
                    success_rate = 0.0
                    avg_profit = 0.0
                
                stats[reason] = {
                    "total_closes": data["count"],
                    "successful_closes": data["success"],
                    "success_rate": round(success_rate, 3),
                    "total_profit": round(data["total_profit"], 2),
                    "average_profit": round(avg_profit, 2)
                }
            
            return stats
            
        except Exception as e:
            print(f"❌ Close performance stats error: {e}")
            return {}
    
    def get_risk_assessment(self) -> Dict[str, Any]:
        """Get risk assessment of current portfolio"""
        try:
            # Update positions and metrics
            self.update_positions()
            
            positions = list(self.active_positions.values())
            if not positions:
                return {"risk_level": "LOW", "risk_score": 0.0, "recommendations": []}
            
            risk_factors = []
            risk_score = 0.0
            
            # Factor 1: Position concentration
            if self.portfolio_metrics["total_positions"] > 15:
                risk_factors.append("High position count")
                risk_score += 0.2
            
            # Factor 2: Portfolio imbalance
            balance = self.portfolio_metrics["position_balance"]
            if balance < 0.2 or balance > 0.8:
                risk_factors.append("Portfolio imbalance")
                risk_score += 0.15
            
            # Factor 3: Large losses
            if self.portfolio_metrics["total_profit"] < -500:
                risk_factors.append("Significant losses")
                risk_score += 0.3
            
            # Factor 4: Aged positions
            if self.portfolio_metrics["avg_age_hours"] > 48:
                risk_factors.append("Old positions")
                risk_score += 0.1
            
            # Factor 5: High risk level
            if self.portfolio_metrics["risk_level"] > 0.1:
                risk_factors.append("High risk exposure")
                risk_score += self.portfolio_metrics["risk_level"] * 0.5
            
            # Risk level classification
            if risk_score < 0.3:
                risk_level = "LOW"
            elif risk_score < 0.6:
                risk_level = "MEDIUM"
            elif risk_score < 0.8:
                risk_level = "HIGH"
            else:
                risk_level = "CRITICAL"
            
            # Recommendations
            recommendations = []
            if "High position count" in risk_factors:
                recommendations.append("Consider closing some positions")
            if "Portfolio imbalance" in risk_factors:
                recommendations.append("Balance BUY/SELL positions")
            if "Significant losses" in risk_factors:
                recommendations.append("Close losing positions")
            if "Old positions" in risk_factors:
                recommendations.append("Close aged positions")
            if "High risk exposure" in risk_factors:
                recommendations.append("Reduce overall exposure")
            
            return {
                "risk_level": risk_level,
                "risk_score": round(risk_score, 3),
                "risk_factors": risk_factors,
                "recommendations": recommendations,
                "survivability_usage": self.portfolio_metrics["survivability_usage"]
            }
            
        except Exception as e:
            print(f"❌ Risk assessment error: {e}")
            return {"risk_level": "UNKNOWN", "risk_score": 0.0, "recommendations": []}

# Mock Position Manager for Testing
class MockPositionManager:
    """Mock Position Manager for testing purposes"""
    
    def __init__(self):
        self.mock_positions = self._generate_mock_positions()
        self.portfolio_metrics = {
            "total_positions": len(self.mock_positions),
            "buy_positions": sum(1 for p in self.mock_positions if p.type == PositionType.BUY),
            "sell_positions": sum(1 for p in self.mock_positions if p.type == PositionType.SELL),
            "total_profit": sum(p.total_profit for p in self.mock_positions),
            "position_balance": 0.6,
            "risk_level": 0.15,
            "survivability_usage": 0.25
        }
        print("🧪 Mock Position Manager initialized for testing")
    
    def _generate_mock_positions(self) -> List[Position]:
        """Generate mock positions for testing"""
        positions = []
        
        # Create some mock positions
        for i in range(8):
            position = Position(
                ticket=100000 + i,
                symbol="XAUUSD",
                type=PositionType.BUY if i % 2 == 0 else PositionType.SELL,
                volume=0.01 + (i * 0.005),
                open_price=2020.0 + (i * 2),
                current_price=2020.0 + (i * 2) + np.random.uniform(-10, 10),
                profit=np.random.uniform(-50, 100),
                swap=np.random.uniform(-5, 5),
                commission=-2.0,
                open_time=datetime.now() - timedelta(hours=np.random.uniform(1, 72)),
                age_hours=np.random.uniform(1, 72),
                comment=f"Grid_{i}",
                magic=100001
            )
            positions.append(position)
        
        return positions
    
    def get_portfolio_status(self) -> Dict[str, Any]:
        """Get mock portfolio status"""
        return self.portfolio_metrics.copy()
    
    def close_profitable_positions(self, confidence: float = 0.5, reasoning: str = "",
                                 min_profit: float = 10.0) -> bool:
        """Mock profitable position closing"""
        profitable_count = sum(1 for p in self.mock_positions if p.total_profit >= min_profit)
        
        if profitable_count > 0:
            to_close = max(1, int(profitable_count * confidence))
            print(f"🧪 Mock closing {to_close} profitable positions")
            return True
        return False
    
    def find_profit_opportunities(self, min_net_profit: float = 50.0) -> List[ProfitOpportunity]:
        """Mock profit opportunity finding"""
        # Return a mock opportunity
        opportunity = ProfitOpportunity(
            profitable_positions=self.mock_positions[:2],
            losing_positions=self.mock_positions[2:3],
            net_profit=75.5,
            profit_amount=125.0,
            loss_amount=49.5,
            confidence=0.75,
            reasoning="Mock balanced close opportunity",
            close_strategy="BALANCED_CLOSE"
        )
        return [opportunity]

# Test function
def test_position_manager():
    """Test the position manager"""
    print("🧪 Testing Position Manager...")
    
    # Test with mock position manager
    mock_manager = MockPositionManager()
    
    # Test portfolio status
    print("\n--- Portfolio Status ---")
    status = mock_manager.get_portfolio_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    # Test profitable position closing
    print("\n--- Testing Profitable Position Closing ---")
    success = mock_manager.close_profitable_positions(confidence=0.7, min_profit=20.0)
    print(f"Profitable closing result: {success}")
    
    # Test profit opportunities
    print("\n--- Testing Profit Opportunities ---")
    opportunities = mock_manager.find_profit_opportunities(min_net_profit=50.0)
    for i, opp in enumerate(opportunities):
        print(f"Opportunity {i+1}:")
        print(f"  Strategy: {opp.close_strategy}")
        print(f"  Net profit: ${opp.net_profit:.2f}")
        print(f"  Confidence: {opp.confidence:.1%}")
        print(f"  Reasoning: {opp.reasoning}")
    
    print("\n✅ Position Manager test completed")

if __name__ == "__main__":
    test_position_manager()