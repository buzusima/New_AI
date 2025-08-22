"""
🎯 Modern Order Manager
order_manager.py
การจัดการออเดอร์อัจฉริยะ สำหรับ Modern Rule-based Trading System
รองรับการวางออเดอร์แบบ intelligent, dynamic spacing, และ smart lot sizing
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import MetaTrader5 as mt5
import numpy as np
from collections import deque
import json

class OrderType(Enum):
    """ประเภทออเดอร์"""
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"
    MARKET_BUY = "MARKET_BUY"
    MARKET_SELL = "MARKET_SELL"

class OrderStatus(Enum):
    """สถานะออเดอร์"""
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class OrderReason(Enum):
    """เหตุผลการวางออเดอร์"""
    TREND_FOLLOWING = "TREND_FOLLOWING"
    MEAN_REVERSION = "MEAN_REVERSION"
    SUPPORT_RESISTANCE = "SUPPORT_RESISTANCE"
    VOLATILITY_BREAKOUT = "VOLATILITY_BREAKOUT"
    PORTFOLIO_BALANCE = "PORTFOLIO_BALANCE"
    GRID_EXPANSION = "GRID_EXPANSION"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"

@dataclass
class OrderRequest:
    """คำขอวางออเดอร์"""
    order_type: OrderType
    volume: float
    price: float
    sl: float = 0.0
    tp: float = 0.0
    reason: OrderReason = OrderReason.GRID_EXPANSION
    confidence: float = 0.5
    reasoning: str = ""
    max_slippage: int = 10
    magic_number: int = 100001

@dataclass
class OrderResult:
    """ผลลัพธ์การวางออเดอร์"""
    success: bool
    ticket: int = 0
    error_code: int = 0
    error_message: str = ""
    execution_price: float = 0.0
    slippage: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class SmartOrderParameters:
    """พารามิเตอร์สำหรับ Smart Order"""
    base_lot_size: float
    current_spacing: int
    max_spread_multiplier: float = 3.0
    min_distance_points: int = 50
    volatility_adjustment: float = 1.0
    trend_bias: float = 0.0  # -1 to 1 (bearish to bullish)
    risk_per_trade: float = 0.01  # 1% risk per trade

class OrderManager:
    """
    🎯 Modern Order Manager
    
    ความสามารถ:
    - Intelligent order placement with reasoning
    - Dynamic spacing and lot sizing
    - Smart order type selection
    - Risk-aware order management
    - Anti-collision spacing control
    - Performance tracking per order reason
    """
    
    def __init__(self, mt5_connector, spacing_manager, lot_calculator, config: Dict):
        """
        Initialize Order Manager
        
        Args:
            mt5_connector: MT5 connection object
            spacing_manager: Dynamic spacing manager
            lot_calculator: Lot size calculator
            config: Configuration settings
        """
        self.mt5_connector = mt5_connector
        self.spacing_manager = spacing_manager
        self.lot_calculator = lot_calculator
        self.config = config
        
        # Order tracking
        self.pending_orders: Dict[int, Dict] = {}
        self.order_history = deque(maxlen=500)
        self.last_order_time = {}  # Track last order time by type
        
        # Performance tracking
        self.order_performance = {
            reason.value: {"count": 0, "success": 0, "total_profit": 0.0}
            for reason in OrderReason
        }
        
        # Risk management
        self.max_orders_per_direction = config.get("trading", {}).get("max_positions", 20)
        self.max_daily_orders = 100
        self.daily_order_count = 0
        self.last_reset_date = datetime.now().date()
        
        # Smart parameters
        self.smart_params = SmartOrderParameters(
            base_lot_size=config.get("trading", {}).get("base_lot_size", 0.01),
            current_spacing=config.get("trading", {}).get("min_spacing_points", 80)
        )
        
        # Symbol info
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.point_value = 0.01  # Will be updated from MT5
        self.min_lot = 0.01
        self.max_lot = 100.0
        self.lot_step = 0.01
        
        # Initialize symbol info
        self._update_symbol_info()
        
        print("🎯 Order Manager initialized")
        print(f"   Symbol: {self.symbol}")
        print(f"   Base lot size: {self.smart_params.base_lot_size}")
        print(f"   Max orders per direction: {self.max_orders_per_direction}")
        print(f"   Current spacing: {self.smart_params.current_spacing} points")
    
    def _update_symbol_info(self):
        """Update symbol information from MT5"""
        try:
            if not self.mt5_connector.is_connected:
                return
            
            symbol_info = mt5.symbol_info(self.symbol)
            if symbol_info:
                self.point_value = symbol_info.point
                self.min_lot = symbol_info.volume_min
                self.max_lot = symbol_info.volume_max
                self.lot_step = symbol_info.volume_step
                
                print(f"✅ Symbol info updated - Point: {self.point_value}, "
                      f"Lot range: {self.min_lot}-{self.max_lot}, Step: {self.lot_step}")
        except Exception as e:
            print(f"❌ Symbol info update error: {e}")
    
    def place_smart_buy_order(self, confidence: float = 0.5, reasoning: str = "",
                             market_data: Dict = None) -> bool:
        """
        Place intelligent BUY order based on market conditions
        
        Args:
            confidence: Confidence level (0.0-1.0)
            reasoning: Reasoning for the order
            market_data: Current market analysis data
            
        Returns:
            True if order placed successfully
        """
        try:
            # Reset daily counter if needed
            self._reset_daily_counter()
            
            # Check daily limits
            if not self._check_daily_limits():
                print("⚠️ Daily order limit reached")
                return False
            
            # Get current market data
            if market_data is None:
                market_data = self._get_current_market_data()
            
            if not market_data:
                print("❌ Cannot get market data for buy order")
                return False
            
            # Calculate smart order parameters
            order_params = self._calculate_smart_buy_parameters(
                confidence, market_data, reasoning
            )
            
            if not order_params:
                print("❌ Cannot calculate buy order parameters")
                return False
            
            # Determine order type based on market conditions
            order_type = self._determine_buy_order_type(market_data, confidence)
            
            # Create order request
            order_request = OrderRequest(
                order_type=order_type,
                volume=order_params["volume"],
                price=order_params["price"],
                sl=order_params.get("sl", 0.0),
                tp=order_params.get("tp", 0.0),
                reason=order_params["reason"],
                confidence=confidence,
                reasoning=reasoning,
                max_slippage=order_params.get("slippage", 10)
            )
            
            # Execute order
            result = self._execute_order(order_request)
            
            if result.success:
                print(f"✅ BUY order placed successfully")
                print(f"   📊 Ticket: {result.ticket}")
                print(f"   💰 Volume: {order_request.volume}")
                print(f"   📈 Price: {order_request.price}")
                print(f"   🎯 Reason: {order_request.reason.value}")
                print(f"   💭 Reasoning: {reasoning}")
                
                # Track performance
                self._track_order_performance(order_request.reason, True)
                
                return True
            else:
                print(f"❌ BUY order failed: {result.error_message}")
                self._track_order_performance(order_request.reason, False)
                return False
                
        except Exception as e:
            print(f"❌ Smart buy order error: {e}")
            return False
    
    def place_smart_sell_order(self, confidence: float = 0.5, reasoning: str = "",
                              market_data: Dict = None) -> bool:
        """
        Place intelligent SELL order based on market conditions
        
        Args:
            confidence: Confidence level (0.0-1.0)
            reasoning: Reasoning for the order
            market_data: Current market analysis data
            
        Returns:
            True if order placed successfully
        """
        try:
            # Reset daily counter if needed
            self._reset_daily_counter()
            
            # Check daily limits
            if not self._check_daily_limits():
                print("⚠️ Daily order limit reached")
                return False
            
            # Get current market data
            if market_data is None:
                market_data = self._get_current_market_data()
            
            if not market_data:
                print("❌ Cannot get market data for sell order")
                return False
            
            # Calculate smart order parameters
            order_params = self._calculate_smart_sell_parameters(
                confidence, market_data, reasoning
            )
            
            if not order_params:
                print("❌ Cannot calculate sell order parameters")
                return False
            
            # Determine order type based on market conditions
            order_type = self._determine_sell_order_type(market_data, confidence)
            
            # Create order request
            order_request = OrderRequest(
                order_type=order_type,
                volume=order_params["volume"],
                price=order_params["price"],
                sl=order_params.get("sl", 0.0),
                tp=order_params.get("tp", 0.0),
                reason=order_params["reason"],
                confidence=confidence,
                reasoning=reasoning,
                max_slippage=order_params.get("slippage", 10)
            )
            
            # Execute order
            result = self._execute_order(order_request)
            
            if result.success:
                print(f"✅ SELL order placed successfully")
                print(f"   📊 Ticket: {result.ticket}")
                print(f"   💰 Volume: {order_request.volume}")
                print(f"   📉 Price: {order_request.price}")
                print(f"   🎯 Reason: {order_request.reason.value}")
                print(f"   💭 Reasoning: {reasoning}")
                
                # Track performance
                self._track_order_performance(order_request.reason, True)
                
                return True
            else:
                print(f"❌ SELL order failed: {result.error_message}")
                self._track_order_performance(order_request.reason, False)
                return False
                
        except Exception as e:
            print(f"❌ Smart sell order error: {e}")
            return False
    
    def _calculate_smart_buy_parameters(self, confidence: float, market_data: Dict, 
                                      reasoning: str) -> Optional[Dict]:
        """Calculate smart parameters for BUY order"""
        try:
            current_price = market_data.get("current_price", 0)
            if current_price == 0:
                return None
            
            # Determine reason based on reasoning text
            reason = self._determine_order_reason(reasoning)
            
            # Calculate volume using lot calculator
            volume = self.lot_calculator.calculate_optimal_lot_size(
                market_data=market_data,
                confidence=confidence,
                order_type="BUY"
            )
            
            # Calculate price based on market conditions and order type
            volatility_factor = market_data.get("volatility_factor", 1.0)
            trend_strength = market_data.get("trend_strength", 0.0)
            
            # Dynamic spacing based on market conditions
            spacing = self.spacing_manager.get_current_spacing(
                volatility_factor=volatility_factor,
                trend_strength=trend_strength,
                direction="BUY"
            )
            
            # Price calculation varies by reason
            if reason == OrderReason.SUPPORT_RESISTANCE:
                # Place near support level
                support_levels = market_data.get("support_levels", [])
                if support_levels:
                    target_price = min([level["level"] for level in support_levels], 
                                     key=lambda x: abs(x - current_price))
                else:
                    target_price = current_price - (spacing * self.point_value)
            elif reason == OrderReason.MEAN_REVERSION:
                # Place below current price expecting reversion
                deviation = market_data.get("price_deviation_from_mean", 0)
                adjustment = abs(deviation) * 10 * self.point_value if deviation < 0 else spacing * self.point_value
                target_price = current_price - adjustment
            else:
                # Standard grid placement
                target_price = current_price - (spacing * self.point_value)
            
            # Ensure minimum distance
            min_distance = self.config.get("trading", {}).get("min_spacing_points", 50) * self.point_value
            if abs(target_price - current_price) < min_distance:
                target_price = current_price - min_distance
            
            # Check for collisions with existing orders
            target_price = self._avoid_order_collisions(target_price, "BUY")
            
            # Calculate SL/TP if needed
            sl_price = 0.0  # No SL for grid trading
            tp_price = 0.0  # No TP for grid trading
            
            return {
                "volume": volume,
                "price": round(target_price, 5),
                "sl": sl_price,
                "tp": tp_price,
                "reason": reason,
                "slippage": min(20, int(volatility_factor * 10))
            }
            
        except Exception as e:
            print(f"❌ Smart buy parameters error: {e}")
            return None
    
    def _calculate_smart_sell_parameters(self, confidence: float, market_data: Dict, 
                                       reasoning: str) -> Optional[Dict]:
        """Calculate smart parameters for SELL order"""
        try:
            current_price = market_data.get("current_price", 0)
            if current_price == 0:
                return None
            
            # Determine reason based on reasoning text
            reason = self._determine_order_reason(reasoning)
            
            # Calculate volume using lot calculator
            volume = self.lot_calculator.calculate_optimal_lot_size(
                market_data=market_data,
                confidence=confidence,
                order_type="SELL"
            )
            
            # Calculate price based on market conditions and order type
            volatility_factor = market_data.get("volatility_factor", 1.0)
            trend_strength = market_data.get("trend_strength", 0.0)
            
            # Dynamic spacing based on market conditions
            spacing = self.spacing_manager.get_current_spacing(
                volatility_factor=volatility_factor,
                trend_strength=trend_strength,
                direction="SELL"
            )
            
            # Price calculation varies by reason
            if reason == OrderReason.SUPPORT_RESISTANCE:
                # Place near resistance level
                resistance_levels = market_data.get("resistance_levels", [])
                if resistance_levels:
                    target_price = min([level["level"] for level in resistance_levels], 
                                     key=lambda x: abs(x - current_price))
                else:
                    target_price = current_price + (spacing * self.point_value)
            elif reason == OrderReason.MEAN_REVERSION:
                # Place above current price expecting reversion
                deviation = market_data.get("price_deviation_from_mean", 0)
                adjustment = abs(deviation) * 10 * self.point_value if deviation > 0 else spacing * self.point_value
                target_price = current_price + adjustment
            else:
                # Standard grid placement
                target_price = current_price + (spacing * self.point_value)
            
            # Ensure minimum distance
            min_distance = self.config.get("trading", {}).get("min_spacing_points", 50) * self.point_value
            if abs(target_price - current_price) < min_distance:
                target_price = current_price + min_distance
            
            # Check for collisions with existing orders
            target_price = self._avoid_order_collisions(target_price, "SELL")
            
            # Calculate SL/TP if needed
            sl_price = 0.0  # No SL for grid trading
            tp_price = 0.0  # No TP for grid trading
            
            return {
                "volume": volume,
                "price": round(target_price, 5),
                "sl": sl_price,
                "tp": tp_price,
                "reason": reason,
                "slippage": min(20, int(volatility_factor * 10))
            }
            
        except Exception as e:
            print(f"❌ Smart sell parameters error: {e}")
            return None
    
    def _determine_order_reason(self, reasoning: str) -> OrderReason:
        """Determine order reason from reasoning text"""
        reasoning_lower = reasoning.lower()
        
        if "trend" in reasoning_lower or "uptrend" in reasoning_lower or "downtrend" in reasoning_lower:
            return OrderReason.TREND_FOLLOWING
        elif "reversion" in reasoning_lower or "bollinger" in reasoning_lower or "deviation" in reasoning_lower:
            return OrderReason.MEAN_REVERSION
        elif "support" in reasoning_lower or "resistance" in reasoning_lower:
            return OrderReason.SUPPORT_RESISTANCE
        elif "volatility" in reasoning_lower or "breakout" in reasoning_lower:
            return OrderReason.VOLATILITY_BREAKOUT
        elif "balance" in reasoning_lower or "portfolio" in reasoning_lower:
            return OrderReason.PORTFOLIO_BALANCE
        elif "risk" in reasoning_lower or "protection" in reasoning_lower:
            return OrderReason.RISK_MANAGEMENT
        else:
            return OrderReason.GRID_EXPANSION
    
    def _determine_buy_order_type(self, market_data: Dict, confidence: float) -> OrderType:
        """Determine best order type for BUY order"""
        try:
            volatility_level = market_data.get("volatility_level", "NORMAL")
            trend_direction = market_data.get("trend_direction", "SIDEWAYS")
            market_condition = market_data.get("condition", "UNKNOWN")
            
            # High confidence + favorable conditions = Market order
            if confidence > 0.8 and trend_direction == "UP":
                return OrderType.MARKET_BUY
            
            # High volatility = Limit order to avoid slippage
            if volatility_level in ["HIGH", "VERY_HIGH"]:
                return OrderType.BUY_LIMIT
            
            # Trending up + breakout = Stop order above current price
            if trend_direction == "UP" and "BREAKOUT" in str(market_condition):
                return OrderType.BUY_STOP
            
            # Default to limit order
            return OrderType.BUY_LIMIT
            
        except Exception as e:
            print(f"❌ Buy order type error: {e}")
            return OrderType.BUY_LIMIT
    
    def _determine_sell_order_type(self, market_data: Dict, confidence: float) -> OrderType:
        """Determine best order type for SELL order"""
        try:
            volatility_level = market_data.get("volatility_level", "NORMAL")
            trend_direction = market_data.get("trend_direction", "SIDEWAYS")
            market_condition = market_data.get("condition", "UNKNOWN")
            
            # High confidence + favorable conditions = Market order
            if confidence > 0.8 and trend_direction == "DOWN":
                return OrderType.MARKET_SELL
            
            # High volatility = Limit order to avoid slippage
            if volatility_level in ["HIGH", "VERY_HIGH"]:
                return OrderType.SELL_LIMIT
            
            # Trending down + breakout = Stop order below current price
            if trend_direction == "DOWN" and "BREAKOUT" in str(market_condition):
                return OrderType.SELL_STOP
            
            # Default to limit order
            return OrderType.SELL_LIMIT
            
        except Exception as e:
            print(f"❌ Sell order type error: {e}")
            return OrderType.SELL_LIMIT
    
    def _avoid_order_collisions(self, target_price: float, direction: str) -> float:
        """Avoid placing orders too close to existing orders"""
        try:
            min_distance = self.config.get("trading", {}).get("min_spacing_points", 50) * self.point_value
            
            # Get pending orders
            pending_orders = self.get_pending_orders()
            
            for order in pending_orders:
                order_price = order.get("price", 0)
                order_type = order.get("type", "")
                
                # Check same direction orders
                if ((direction == "BUY" and "BUY" in order_type) or 
                    (direction == "SELL" and "SELL" in order_type)):
                    
                    distance = abs(target_price - order_price)
                    if distance < min_distance:
                        # Adjust price to maintain minimum distance
                        if direction == "BUY":
                            if target_price > order_price:
                                target_price = order_price + min_distance
                            else:
                                target_price = order_price - min_distance
                        else:  # SELL
                            if target_price > order_price:
                                target_price = order_price + min_distance
                            else:
                                target_price = order_price - min_distance
            
            return target_price
            
        except Exception as e:
            print(f"❌ Collision avoidance error: {e}")
            return target_price
    
    def _execute_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute order request with MT5"""
        try:
            if not self.mt5_connector.is_connected:
                return OrderResult(
                    success=False,
                    error_message="MT5 not connected"
                )
            
            # Prepare order request for MT5
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": self.symbol,
                "volume": order_request.volume,
                "price": order_request.price,
                "sl": order_request.sl,
                "tp": order_request.tp,
                "deviation": order_request.max_slippage,
                "magic": order_request.magic_number,
                "comment": f"{order_request.reason.value}|{order_request.confidence:.2f}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Set order type
            if order_request.order_type == OrderType.BUY_LIMIT:
                request["type"] = mt5.ORDER_TYPE_BUY_LIMIT
            elif order_request.order_type == OrderType.SELL_LIMIT:
                request["type"] = mt5.ORDER_TYPE_SELL_LIMIT
            elif order_request.order_type == OrderType.BUY_STOP:
                request["type"] = mt5.ORDER_TYPE_BUY_STOP
            elif order_request.order_type == OrderType.SELL_STOP:
                request["type"] = mt5.ORDER_TYPE_SELL_STOP
            elif order_request.order_type == OrderType.MARKET_BUY:
                request["action"] = mt5.TRADE_ACTION_DEAL
                request["type"] = mt5.ORDER_TYPE_BUY
                del request["price"]  # Market orders don't need price
            elif order_request.order_type == OrderType.MARKET_SELL:
                request["action"] = mt5.TRADE_ACTION_DEAL
                request["type"] = mt5.ORDER_TYPE_SELL
                del request["price"]  # Market orders don't need price
            
            # Send order
            result = mt5.order_send(request)
            
            if result is None:
                return OrderResult(
                    success=False,
                    error_message="Order send failed - no result"
                )
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                # Order successful
                order_result = OrderResult(
                    success=True,
                    ticket=result.order,
                    execution_price=result.price,
                    slippage=abs(result.price - order_request.price) if hasattr(result, 'price') and order_request.price > 0 else 0
                )
                
                # Track the order
                self._track_order(order_request, order_result)
                
                # Update daily counter
                self.daily_order_count += 1
                
                return order_result
            else:
                # Order failed
                error_message = f"Order failed - Code: {result.retcode}"
                if hasattr(result, 'comment'):
                    error_message += f", Comment: {result.comment}"
                
                return OrderResult(
                    success=False,
                    error_code=result.retcode,
                    error_message=error_message
                )
                
        except Exception as e:
            return OrderResult(
                success=False,
                error_message=f"Order execution error: {e}"
            )
    
    def _track_order(self, order_request: OrderRequest, order_result: OrderResult):
        """Track order for monitoring and analysis"""
        try:
            order_data = {
                "ticket": order_result.ticket,
                "type": order_request.order_type.value,
                "volume": order_request.volume,
                "requested_price": order_request.price,
                "execution_price": order_result.execution_price,
                "slippage": order_result.slippage,
                "reason": order_request.reason.value,
                "confidence": order_request.confidence,
                "reasoning": order_request.reasoning,
                "timestamp": order_result.timestamp,
                "status": OrderStatus.PENDING.value if "LIMIT" in order_request.order_type.value or "STOP" in order_request.order_type.value else OrderStatus.FILLED.value
            }
            
            # Add to pending orders if not market order
            if order_data["status"] == OrderStatus.PENDING.value:
                self.pending_orders[order_result.ticket] = order_data
            
            # Add to history
            self.order_history.append(order_data)
            
            # Update last order time
            self.last_order_time[order_request.order_type.value] = datetime.now()
            
        except Exception as e:
            print(f"❌ Order tracking error: {e}")
    
    def _track_order_performance(self, reason: OrderReason, success: bool, profit: float = 0.0):
        """Track performance by order reason"""
        try:
            reason_key = reason.value
            if reason_key in self.order_performance:
                self.order_performance[reason_key]["count"] += 1
                if success:
                    self.order_performance[reason_key]["success"] += 1
                self.order_performance[reason_key]["total_profit"] += profit
        except Exception as e:
            print(f"❌ Performance tracking error: {e}")
    
    def _get_current_market_data(self) -> Optional[Dict]:
        """Get current market data for order calculation"""
        try:
            if not self.mt5_connector.is_connected:
                return None
            
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                return None
            
            current_price = (tick.bid + tick.ask) / 2
            spread = tick.ask - tick.bid
            
            return {
                "current_price": current_price,
                "bid": tick.bid,
                "ask": tick.ask,
                "spread": spread,
                "volatility_factor": 1.0,  # Default values
                "trend_strength": 0.0,
                "trend_direction": "SIDEWAYS",
                "volatility_level": "NORMAL",
                "condition": "RANGING"
            }
            
        except Exception as e:
            print(f"❌ Market data error: {e}")
            return None
    
    def _reset_daily_counter(self):
        """Reset daily order counter if new day"""
        current_date = datetime.now().date()
        if current_date != self.last_reset_date:
            self.daily_order_count = 0
            self.last_reset_date = current_date
            print(f"📅 Daily counter reset for {current_date}")
    
    def _check_daily_limits(self) -> bool:
        """Check if daily order limits allow new orders"""
        return self.daily_order_count < self.max_daily_orders
    
    # === Public Interface Methods ===
    
    def get_pending_orders(self) -> List[Dict]:
        """Get list of pending orders"""
        try:
            if not self.mt5_connector.is_connected:
                return []
            
            # Get orders from MT5
            orders = mt5.orders_get(symbol=self.symbol)
            if orders is None:
                return []
            
            pending_list = []
            for order in orders:
                order_data = {
                    "ticket": order.ticket,
                    "type": self._order_type_to_string(order.type),
                    "volume": order.volume_initial,
                    "price": order.price_open,
                    "sl": order.sl,
                    "tp": order.tp,
                    "time": datetime.fromtimestamp(order.time_setup),
                    "comment": order.comment,
                    "magic": order.magic
                }
                pending_list.append(order_data)
            
            return pending_list
            
        except Exception as e:
            print(f"❌ Get pending orders error: {e}")
            return []
    
    def get_pending_orders_count(self) -> int:
        """Get count of pending orders"""
        return len(self.get_pending_orders())
    
    def cancel_order(self, ticket: int, reason: str = "") -> bool:
        """Cancel specific order"""
        try:
            if not self.mt5_connector.is_connected:
                return False
            
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": ticket,
            }
            
            result = mt5.order_send(request)
            
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                print(f"✅ Order {ticket} cancelled successfully - {reason}")
                
                # Remove from tracking
                if ticket in self.pending_orders:
                    del self.pending_orders[ticket]
                
                return True
            else:
                error_msg = f"Cancel failed - Code: {result.retcode}" if result else "No result"
                print(f"❌ Cancel order {ticket} failed: {error_msg}")
                return False
                
        except Exception as e:
            print(f"❌ Cancel order error: {e}")
            return False
    
    def cancel_all_pending_orders(self, reason: str = "Manual cancellation") -> int:
        """Cancel all pending orders"""
        try:
            pending_orders = self.get_pending_orders()
            cancelled_count = 0
            
            for order in pending_orders:
                if self.cancel_order(order["ticket"], reason):
                    cancelled_count += 1
                time.sleep(0.1)  # Small delay between cancellations
            
            print(f"✅ Cancelled {cancelled_count}/{len(pending_orders)} orders")
            return cancelled_count
            
        except Exception as e:
            print(f"❌ Cancel all orders error: {e}")
            return 0
    
    def get_order_performance_stats(self) -> Dict[str, Dict]:
        """Get performance statistics by order reason"""
        try:
            stats = {}
            
            for reason, data in self.order_performance.items():
                if data["count"] > 0:
                    success_rate = data["success"] / data["count"]
                    avg_profit = data["total_profit"] / data["count"]
                else:
                    success_rate = 0.0
                    avg_profit = 0.0
                
                stats[reason] = {
                    "total_orders": data["count"],
                    "successful_orders": data["success"],
                    "success_rate": round(success_rate, 3),
                    "total_profit": round(data["total_profit"], 2),
                    "average_profit": round(avg_profit, 2)
                }
            
            return stats
            
        except Exception as e:
            print(f"❌ Performance stats error: {e}")
            return {}
    
    def update_smart_parameters(self, **kwargs):
        """Update smart order parameters"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.smart_params, key):
                    setattr(self.smart_params, key, value)
                    print(f"📝 Updated {key} to {value}")
        except Exception as e:
            print(f"❌ Parameter update error: {e}")
    
    def _order_type_to_string(self, order_type: int) -> str:
        """Convert MT5 order type to string"""
        type_mapping = {
            mt5.ORDER_TYPE_BUY: "MARKET_BUY",
            mt5.ORDER_TYPE_SELL: "MARKET_SELL",
            mt5.ORDER_TYPE_BUY_LIMIT: "BUY_LIMIT",
            mt5.ORDER_TYPE_SELL_LIMIT: "SELL_LIMIT",
            mt5.ORDER_TYPE_BUY_STOP: "BUY_STOP",
            mt5.ORDER_TYPE_SELL_STOP: "SELL_STOP"
        }
        return type_mapping.get(order_type, "UNKNOWN")

# Mock Order Manager for Testing
class MockOrderManager:
    """Mock Order Manager for testing purposes"""
    
    def __init__(self):
        self.order_count = 0
        self.pending_orders = []
        self.success_rate = 0.8  # 80% success rate for testing
        print("🧪 Mock Order Manager initialized for testing")
    
    def place_smart_buy_order(self, confidence: float = 0.5, reasoning: str = "",
                             market_data: Dict = None) -> bool:
        """Mock BUY order placement"""
        self.order_count += 1
        success = np.random.random() < self.success_rate
        
        if success:
            self.pending_orders.append({
                "ticket": 100000 + self.order_count,
                "type": "BUY_LIMIT",
                "volume": 0.01,
                "price": 2020.50,
                "reason": "TREND_FOLLOWING",
                "confidence": confidence
            })
            print(f"🧪 Mock BUY order placed - Confidence: {confidence:.1%}")
        else:
            print(f"🧪 Mock BUY order failed")
        
        return success
    
    def place_smart_sell_order(self, confidence: float = 0.5, reasoning: str = "",
                              market_data: Dict = None) -> bool:
        """Mock SELL order placement"""
        self.order_count += 1
        success = np.random.random() < self.success_rate
        
        if success:
            self.pending_orders.append({
                "ticket": 200000 + self.order_count,
                "type": "SELL_LIMIT", 
                "volume": 0.01,
                "price": 2010.30,
                "reason": "MEAN_REVERSION",
                "confidence": confidence
            })
            print(f"🧪 Mock SELL order placed - Confidence: {confidence:.1%}")
        else:
            print(f"🧪 Mock SELL order failed")
        
        return success
    
    def get_pending_orders_count(self) -> int:
        """Get mock pending orders count"""
        return len(self.pending_orders)
    
    def cancel_order(self, ticket: int, reason: str = "") -> bool:
        """Mock order cancellation"""
        for i, order in enumerate(self.pending_orders):
            if order["ticket"] == ticket:
                del self.pending_orders[i]
                print(f"🧪 Mock order {ticket} cancelled")
                return True
        return False

# Test function
def test_order_manager():
    """Test the order manager"""
    print("🧪 Testing Order Manager...")
    
    # Test with mock order manager
    mock_manager = MockOrderManager()
    
    # Test order placement
    print("\n--- Testing Order Placement ---")
    for i in range(3):
        confidence = 0.6 + (i * 0.1)
        buy_success = mock_manager.place_smart_buy_order(confidence=confidence, 
                                                        reasoning="Uptrend detected with oversold RSI")
        sell_success = mock_manager.place_smart_sell_order(confidence=confidence,
                                                          reasoning="Resistance level reached")
        
        print(f"Test {i+1}: BUY={buy_success}, SELL={sell_success}")
    
    # Test pending orders
    print(f"\n--- Pending Orders ---")
    print(f"Total pending orders: {mock_manager.get_pending_orders_count()}")
    
    # Test cancellation
    if mock_manager.pending_orders:
        first_ticket = mock_manager.pending_orders[0]["ticket"]
        mock_manager.cancel_order(first_ticket, "Test cancellation")
        print(f"Orders after cancellation: {mock_manager.get_pending_orders_count()}")
    
    print("\n✅ Order Manager test completed")

if __name__ == "__main__":
    test_order_manager()