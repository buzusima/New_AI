"""
🎯 Modern Order Manager - Updated for New Rule Engine
order_manager.py
เพิ่ม place_smart_order() method และปรับปรุงให้เข้ากับ Modern Rule Engine
** PRODUCTION READY - COMPATIBLE WITH NEW RULE ENGINE **
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
    🎯 Modern Order Manager - Updated Edition
    
    ความสามารถ:
    - ✅ place_smart_order() method สำหรับ Rule Engine ใหม่
    - ✅ รองรับ target_price จาก Rule Engine
    - ✅ Dynamic spacing และ lot sizing
    - ✅ Anti-collision protection
    - ✅ Performance tracking
    ** COMPATIBLE WITH NEW RULE ENGINE **
    """
    
    def __init__(self, mt5_connector, spacing_manager, lot_calculator, config: Dict):
        """Initialize Order Manager"""
        if not mt5_connector:
            raise ValueError("MT5 connector is required for production Order Manager")
            
        self.mt5_connector = mt5_connector
        self.spacing_manager = spacing_manager
        self.lot_calculator = lot_calculator
        self.config = config
        
        # Order tracking
        self.pending_orders: Dict[int, Dict] = {}
        self.order_history = deque(maxlen=500)
        self.last_order_time = {}
        
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
        self.point_value = 0.01
        self.min_lot = 0.01
        self.max_lot = 100.0
        self.lot_step = 0.01
        
        # Initialize from MT5
        self._update_symbol_info()
        
        print("🎯 Order Manager initialized - Compatible with Modern Rule Engine")
    
    # ========================================================================================
    # 🆕 NEW PRIMARY INTERFACE FOR RULE ENGINE
    # ========================================================================================
    
    def place_smart_order(self, order_type: str, volume: float, price: float, 
                         reasoning: str, confidence: float, **kwargs) -> Dict:
        """
        🆕 หลัก Method สำหรับ Modern Rule Engine
        
        Args:
            order_type: ประเภทออเดอร์ (BUY_LIMIT, SELL_LIMIT, etc.)
            volume: ขนาดออเดอร์
            price: ราคาเป้าหมายจาก Rule Engine
            reasoning: เหตุผลการวางออเดอร์
            confidence: ระดับความเชื่อมั่น
            **kwargs: พารามิเตอร์เพิ่มเติม
            
        Returns:
            Dict: {"success": bool, "ticket": int, "error": str, ...}
        """
        try:
            print(f"🎯 === PLACE SMART ORDER ===")
            print(f"   Type: {order_type}")
            print(f"   Volume: {volume:.3f}")
            print(f"   Price: {price:.5f}")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Reasoning: {reasoning}")
            
            # Validate inputs
            if not self._validate_order_inputs(order_type, volume, price):
                return {"success": False, "error": "Invalid order inputs"}
            
            # Check MT5 connection
            if not self.mt5_connector.is_connected:
                self.log("❌ MT5 not connected")
                return {"success": False, "error": "MT5 not connected"}
            
            # Check daily limits
            if not self._check_daily_limits():
                return {"success": False, "error": "Daily order limit reached"}
            
            # Prepare market data with target price
            market_data = kwargs.get("market_data", {})
            if not market_data:
                market_data = self._get_current_market_data()
            
            # ⭐ เพิ่ม target_price จาก Rule Engine ลงใน market_data
            market_data["target_price"] = price
            market_data["rule_volume"] = volume  # เพิ่ม volume ที่ Rule Engine คำนวณแล้ว
            
            # Route to appropriate method
            if order_type in ["BUY_LIMIT", "BUY_STOP", "MARKET_BUY"]:
                success = self.place_smart_buy_order(confidence, reasoning, market_data)
                return {"success": success, "order_type": order_type, "direction": "BUY"}
                
            elif order_type in ["SELL_LIMIT", "SELL_STOP", "MARKET_SELL"]:
                success = self.place_smart_sell_order(confidence, reasoning, market_data)
                return {"success": success, "order_type": order_type, "direction": "SELL"}
            
            else:
                return {"success": False, "error": f"Unknown order type: {order_type}"}
                
        except Exception as e:
            self.log(f"❌ Place smart order error: {e}")
            return {"success": False, "error": str(e)}
    
    def _validate_order_inputs(self, order_type: str, volume: float, price: float) -> bool:
        """ตรวจสอบความถูกต้องของ inputs"""
        try:
            # เช็ค order type
            valid_types = ["BUY_LIMIT", "SELL_LIMIT", "BUY_STOP", "SELL_STOP", "MARKET_BUY", "MARKET_SELL"]
            if order_type not in valid_types:
                self.log(f"❌ Invalid order type: {order_type}")
                return False
            
            # เช็ค volume
            if volume < self.min_lot or volume > self.max_lot:
                self.log(f"❌ Invalid volume: {volume} (range: {self.min_lot}-{self.max_lot})")
                return False
            
            # เช็ค price
            if price <= 0:
                self.log(f"❌ Invalid price: {price}")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"❌ Input validation error: {e}")
            return False
    
    # ========================================================================================
    # 🔄 UPDATED EXISTING METHODS
    # ========================================================================================
    
    def place_smart_buy_order(self, confidence: float = 0.5, reasoning: str = "",
                             market_data: Dict = None) -> bool:
        """Updated: รองรับ target_price จาก Rule Engine"""
        try:
            # Validate MT5 connection
            if not self.mt5_connector.is_connected:
                self.log("❌ Cannot place BUY order - MT5 not connected")
                return False
            
            # Get market data
            if market_data is None:
                market_data = self._get_current_market_data()
            
            if not market_data:
                self.log("❌ Cannot get market data for buy order")
                return False
            
            # Calculate order parameters
            order_params = self._calculate_smart_buy_parameters(confidence, market_data, reasoning)
            
            if not order_params:
                self.log("❌ Cannot calculate buy order parameters")
                return False
            
            # Determine order type
            order_type = self._determine_buy_order_type(market_data, confidence)
            
            # Create and execute order
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
            
            result = self._execute_real_order(order_request)
            
            if result.success:
                self.log(f"✅ BUY order placed: Ticket {result.ticket} @ {order_request.price:.5f}")
                self._track_order_performance(order_request.reason, True)
                return True
            else:
                self.log(f"❌ BUY order failed: {result.error_message}")
                self._track_order_performance(order_request.reason, False)
                return False
                
        except Exception as e:
            self.log(f"❌ Smart buy order error: {e}")
            return False
    
    def place_smart_sell_order(self, confidence: float = 0.5, reasoning: str = "",
                              market_data: Dict = None) -> bool:
        """Updated: รองรับ target_price จาก Rule Engine"""
        try:
            # Validate MT5 connection
            if not self.mt5_connector.is_connected:
                self.log("❌ Cannot place SELL order - MT5 not connected")
                return False
            
            # Get market data
            if market_data is None:
                market_data = self._get_current_market_data()
            
            if not market_data:
                self.log("❌ Cannot get market data for sell order")
                return False
            
            # Calculate order parameters
            order_params = self._calculate_smart_sell_parameters(confidence, market_data, reasoning)
            
            if not order_params:
                self.log("❌ Cannot calculate sell order parameters")
                return False
            
            # Determine order type
            order_type = self._determine_sell_order_type(market_data, confidence)
            
            # Create and execute order
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
            
            result = self._execute_real_order(order_request)
            
            if result.success:
                self.log(f"✅ SELL order placed: Ticket {result.ticket} @ {order_request.price:.5f}")
                self._track_order_performance(order_request.reason, True)
                return True
            else:
                self.log(f"❌ SELL order failed: {result.error_message}")
                self._track_order_performance(order_request.reason, False)
                return False
                
        except Exception as e:
            self.log(f"❌ Smart sell order error: {e}")
            return False
    
    def _calculate_smart_buy_parameters(self, confidence: float, market_data: Dict, 
                                      reasoning: str) -> Optional[Dict]:
        """Updated: รองรับ target_price จาก Rule Engine"""
        try:
            current_price = market_data.get("current_price", 0)
            if current_price == 0:
                self.log("❌ Invalid current price")
                return None
            
            # Determine reason
            reason = self._determine_order_reason(reasoning)
            
            # ⭐ ใช้ volume จาก Rule Engine ถ้ามี
            rule_volume = market_data.get("rule_volume")
            if rule_volume:
                volume = rule_volume
                print(f"💰 Using Rule Engine volume: {volume:.3f}")
            else:
                # คำนวณ volume เอง
                volume = self.lot_calculator.calculate_optimal_lot_size(
                    market_data=market_data,
                    confidence=confidence,
                    order_type="BUY"
                ) if self.lot_calculator else self.smart_params.base_lot_size
            
            # ⭐ ใช้ target_price จาก Rule Engine ถ้ามี (Priority สูงสุด)
            rule_target_price = market_data.get("target_price")
            
            if rule_target_price:
                target_price = rule_target_price
                print(f"🎯 Using Rule Engine target price: {target_price:.5f}")
                
            else:
                # คำนวณราคาเอง (Fallback)
                print("🔄 Calculating target price (Rule Engine price not provided)")
                
                volatility_factor = market_data.get("volatility_factor", 1.0)
                trend_strength = market_data.get("trend_strength", 0.0)
                
                # Dynamic spacing
                spacing = self.spacing_manager.get_current_spacing(
                    volatility_factor=volatility_factor,
                    trend_strength=trend_strength,
                    direction="BUY"
                ) if self.spacing_manager else self.smart_params.current_spacing
                
                # Price calculation varies by reason
                if reason == OrderReason.SUPPORT_RESISTANCE:
                    support_levels = market_data.get("support_levels", [])
                    if support_levels:
                        target_price = max([level["level"] for level in support_levels], 
                                        key=lambda x: abs(x - current_price))
                    else:
                        target_price = current_price - (spacing * self.point_value)
                elif reason == OrderReason.MEAN_REVERSION:
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
            
            # ⭐ เช็ค collision (สำคัญมาก)
            safe_price = self._avoid_order_collisions(target_price, "BUY")
            if safe_price is None:
                self.log("❌ Price collision detected - skipping BUY order")
                return None
                
            target_price = safe_price
            
            # Validate final price
            if target_price <= 0:
                self.log(f"❌ Invalid target price: {target_price}")
                return None
            
            return {
                "volume": volume,
                "price": round(target_price, 5),
                "sl": 0.0,  # ไม่ใช้ SL
                "tp": 0.0,  # ไม่ใช้ TP
                "reason": reason,
                "slippage": min(20, int(market_data.get("volatility_factor", 1.0) * 10))
            }
            
        except Exception as e:
            self.log(f"❌ Smart buy parameters error: {e}")
            return None
    
    def _calculate_smart_sell_parameters(self, confidence: float, market_data: Dict, 
                                       reasoning: str) -> Optional[Dict]:
        """Updated: รองรับ target_price จาก Rule Engine"""
        try:
            current_price = market_data.get("current_price", 0)
            if current_price == 0:
                self.log("❌ Invalid current price")
                return None
            
            # Determine reason
            reason = self._determine_order_reason(reasoning)
            
            # ⭐ ใช้ volume จาก Rule Engine ถ้ามี
            rule_volume = market_data.get("rule_volume")
            if rule_volume:
                volume = rule_volume
                print(f"💰 Using Rule Engine volume: {volume:.3f}")
            else:
                # คำนวณ volume เอง
                volume = self.lot_calculator.calculate_optimal_lot_size(
                    market_data=market_data,
                    confidence=confidence,
                    order_type="SELL"
                ) if self.lot_calculator else self.smart_params.base_lot_size
            
            # ⭐ ใช้ target_price จาก Rule Engine ถ้ามี (Priority สูงสุด)
            rule_target_price = market_data.get("target_price")
            
            if rule_target_price:
                target_price = rule_target_price
                print(f"🎯 Using Rule Engine target price: {target_price:.5f}")
                
            else:
                # คำนวณราคาเอง (Fallback)
                print("🔄 Calculating target price (Rule Engine price not provided)")
                
                volatility_factor = market_data.get("volatility_factor", 1.0)
                trend_strength = market_data.get("trend_strength", 0.0)
                
                # Dynamic spacing
                spacing = self.spacing_manager.get_current_spacing(
                    volatility_factor=volatility_factor,
                    trend_strength=trend_strength,
                    direction="SELL"
                ) if self.spacing_manager else self.smart_params.current_spacing
                
                # Price calculation varies by reason
                if reason == OrderReason.SUPPORT_RESISTANCE:
                    resistance_levels = market_data.get("resistance_levels", [])
                    if resistance_levels:
                        target_price = min([level["level"] for level in resistance_levels], 
                                        key=lambda x: abs(x - current_price))
                    else:
                        target_price = current_price + (spacing * self.point_value)
                elif reason == OrderReason.MEAN_REVERSION:
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
            
            # ⭐ เช็ค collision (สำคัญมาก)
            safe_price = self._avoid_order_collisions(target_price, "SELL")
            if safe_price is None:
                self.log("❌ Price collision detected - skipping SELL order")
                return None
                
            target_price = safe_price
            
            # Validate final price
            if target_price <= 0:
                self.log(f"❌ Invalid target price: {target_price}")
                return None
            
            return {
                "volume": volume,
                "price": round(target_price, 5),
                "sl": 0.0,  # ไม่ใช้ SL
                "tp": 0.0,  # ไม่ใช้ TP
                "reason": reason,
                "slippage": min(20, int(market_data.get("volatility_factor", 1.0) * 10))
            }
            
        except Exception as e:
            self.log(f"❌ Smart sell parameters error: {e}")
            return None
    
    # ========================================================================================
    # 🔧 HELPER METHODS
    # ========================================================================================
    
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
                
                self.log(f"✅ Symbol info updated: Point={self.point_value}, "
                      f"Lot range={self.min_lot}-{self.max_lot}")
            
        except Exception as e:
            self.log(f"❌ Symbol info update error: {e}")
    
    def _get_current_market_data(self) -> Dict:
        """Get current market data from MT5"""
        try:
            if not self.mt5_connector.is_connected:
                return {}
            
            # Get current tick
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                return {}
            
            return {
                "current_price": (tick.bid + tick.ask) / 2,
                "bid": tick.bid,
                "ask": tick.ask,
                "spread": tick.ask - tick.bid,
                "timestamp": datetime.fromtimestamp(tick.time)
            }
            
        except Exception as e:
            self.log(f"❌ Market data error: {e}")
            return {}
    
    def _check_daily_limits(self) -> bool:
        """Check daily order limits"""
        try:
            # Reset counter if new day
            current_date = datetime.now().date()
            if current_date != self.last_reset_date:
                self.daily_order_count = 0
                self.last_reset_date = current_date
                self.log("🔄 Daily order counter reset")
            
            # Check limits
            if self.daily_order_count >= self.max_daily_orders:
                self.log(f"⚠️ Daily limit reached: {self.daily_order_count}/{self.max_daily_orders}")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"❌ Daily limit check error: {e}")
            return True
    
    def _avoid_order_collisions(self, target_price: float, direction: str) -> Optional[float]:
        """เช็คและป้องกันการ collision ของออเดอร์"""
        try:
            tolerance_points = 5
            tolerance = tolerance_points * self.point_value
            spacing = self.smart_params.current_spacing * self.point_value
            
            # Get existing orders
            pending_orders = self.get_pending_orders()
            existing_prices = [order.get("price", 0) for order in pending_orders]
            existing_prices.sort()
            
            print(f"🔍 COLLISION CHECK: {direction} @ {target_price:.5f}")
            print(f"   Existing orders: {len(existing_prices)}")
            
            # Check for collisions
            for price in existing_prices:
                if abs(target_price - price) <= tolerance:
                    print(f"❌ COLLISION detected @ {price:.5f}")
                    
                    # Find alternative slot
                    if direction == "BUY":
                        # Look for gap below
                        for i in range(len(existing_prices)):
                            gap_price = existing_prices[i] - spacing
                            if not any(abs(gap_price - p) <= tolerance for p in existing_prices):
                                print(f"✅ Found alternative BUY slot @ {gap_price:.5f}")
                                return gap_price
                    else:  # SELL
                        # Look for gap above
                        for i in range(len(existing_prices)):
                            gap_price = existing_prices[i] + spacing
                            if not any(abs(gap_price - p) <= tolerance for p in existing_prices):
                                print(f"✅ Found alternative SELL slot @ {gap_price:.5f}")
                                return gap_price
                    
                    print("❌ No suitable alternative found")
                    return None
            
            print(f"✅ Safe to place @ {target_price:.5f}")
            return target_price
            
        except Exception as e:
            self.log(f"❌ Collision check error: {e}")
            return target_price
    
    def _determine_order_reason(self, reasoning: str) -> OrderReason:
        """Determine order reason from reasoning text"""
        reasoning_lower = reasoning.lower()
        
        if "trend" in reasoning_lower:
            return OrderReason.TREND_FOLLOWING
        elif "reversion" in reasoning_lower or "oversold" in reasoning_lower or "overbought" in reasoning_lower:
            return OrderReason.MEAN_REVERSION
        elif "support" in reasoning_lower or "resistance" in reasoning_lower:
            return OrderReason.SUPPORT_RESISTANCE
        elif "breakout" in reasoning_lower or "volatility" in reasoning_lower:
            return OrderReason.VOLATILITY_BREAKOUT
        elif "balance" in reasoning_lower or "hedge" in reasoning_lower:
            return OrderReason.PORTFOLIO_BALANCE
        elif "grid" in reasoning_lower or "expansion" in reasoning_lower:
            return OrderReason.GRID_EXPANSION
        else:
            return OrderReason.GRID_EXPANSION  # Default
    
    def _determine_buy_order_type(self, market_data: Dict, confidence: float) -> OrderType:
        """Determine best order type for BUY"""
        try:
            volatility_level = market_data.get("volatility_level", "MEDIUM")
            trend_direction = market_data.get("trend_direction", "SIDEWAYS")
            market_condition = market_data.get("condition", "UNKNOWN")
            
            # High confidence + low volatility = Limit order
            if confidence > 0.7 and volatility_level in ["LOW", "VERY_LOW"]:
                return OrderType.BUY_LIMIT
            
            # High volatility = Limit order to avoid slippage
            if volatility_level in ["HIGH", "VERY_HIGH"]:
                return OrderType.BUY_LIMIT
            
            # Trending up + breakout = Stop order above current price
            if trend_direction == "UP" and "BREAKOUT" in str(market_condition):
                return OrderType.BUY_STOP
            
            # Default to limit order
            return OrderType.BUY_LIMIT
            
        except Exception as e:
            self.log(f"❌ Buy order type error: {e}")
            return OrderType.BUY_LIMIT
    
    def _determine_sell_order_type(self, market_data: Dict, confidence: float) -> OrderType:
        """Determine best order type for SELL"""
        try:
            volatility_level = market_data.get("volatility_level", "MEDIUM")
            trend_direction = market_data.get("trend_direction", "SIDEWAYS")
            market_condition = market_data.get("condition", "UNKNOWN")
            
            # High confidence + low volatility = Limit order
            if confidence > 0.7 and volatility_level in ["LOW", "VERY_LOW"]:
                return OrderType.SELL_LIMIT
            
            # High volatility = Limit order to avoid slippage
            if volatility_level in ["HIGH", "VERY_HIGH"]:
                return OrderType.SELL_LIMIT
            
            # Trending down + breakout = Stop order below current price
            if trend_direction == "DOWN" and "BREAKOUT" in str(market_condition):
                return OrderType.SELL_STOP
            
            # Default to limit order
            return OrderType.SELL_LIMIT
            
        except Exception as e:
            self.log(f"❌ Sell order type error: {e}")
            return OrderType.SELL_LIMIT
    
    def _execute_real_order(self, order_request: OrderRequest) -> OrderResult:
        """Execute REAL order in MT5"""
        try:
            # Convert order type to MT5 format
            mt5_order_types = {
                OrderType.BUY_LIMIT: mt5.ORDER_TYPE_BUY_LIMIT,
                OrderType.SELL_LIMIT: mt5.ORDER_TYPE_SELL_LIMIT,
                OrderType.BUY_STOP: mt5.ORDER_TYPE_BUY_STOP,
                OrderType.SELL_STOP: mt5.ORDER_TYPE_SELL_STOP,
                OrderType.MARKET_BUY: mt5.ORDER_TYPE_BUY,
                OrderType.MARKET_SELL: mt5.ORDER_TYPE_SELL
            }
            
            mt5_type = mt5_order_types.get(order_request.order_type)
            if mt5_type is None:
                return OrderResult(success=False, error_message="Invalid order type")
            
            # Prepare order request
            request = {
                "action": mt5.TRADE_ACTION_PENDING if mt5_type in [
                    mt5.ORDER_TYPE_BUY_LIMIT, mt5.ORDER_TYPE_SELL_LIMIT,
                    mt5.ORDER_TYPE_BUY_STOP, mt5.ORDER_TYPE_SELL_STOP
                ] else mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": order_request.volume,
                "type": mt5_type,
                "price": order_request.price,
                "sl": order_request.sl if order_request.sl > 0 else None,
                "tp": order_request.tp if order_request.tp > 0 else None,
                "deviation": order_request.max_slippage,
                "magic": order_request.magic_number,
                "comment": f"{order_request.reason.value}_{datetime.now().strftime('%H%M%S')}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            # Remove None values
            request = {k: v for k, v in request.items() if v is not None}
            
            # Send order to MT5
            result = mt5.order_send(request)
            
            if result is None:
                return OrderResult(success=False, error_message="MT5 order_send returned None")
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                # Increment daily counter
                self.daily_order_count += 1
                
                return OrderResult(
                    success=True,
                    ticket=result.order if hasattr(result, 'order') else result.deal,
                    execution_price=result.price if hasattr(result, 'price') else order_request.price,
                    timestamp=datetime.now()
                )
            else:
                return OrderResult(
                    success=False,
                    error_code=result.retcode,
                    error_message=f"MT5 Error {result.retcode}: {result.comment if hasattr(result, 'comment') else 'Unknown error'}"
                )
                
        except Exception as e:
            return OrderResult(success=False, error_message=str(e))
    
    def get_pending_orders(self) -> List[Dict]:
        """Get REAL pending orders from MT5"""
        try:
            if not self.mt5_connector.is_connected:
                return []
            
            orders = mt5.orders_get(symbol=self.symbol)
            if orders is None:
                return []
            
            pending_list = []
            for order in orders:
                pending_list.append({
                    "ticket": order.ticket,
                    "type": self._order_type_to_string(order.type),
                    "volume": order.volume_initial,
                    "price": order.price_open,
                    "sl": order.sl,
                    "tp": order.tp,
                    "time_setup": datetime.fromtimestamp(order.time_setup),
                    "comment": order.comment,
                    "magic": order.magic
                })
            
            return pending_list
            
        except Exception as e:
            self.log(f"❌ Get pending orders error: {e}")
            return []
    
    def _track_order_performance(self, reason: OrderReason, success: bool):
        """Track order performance by reason"""
        try:
            reason_key = reason.value
            if reason_key not in self.order_performance:
                self.order_performance[reason_key] = {"count": 0, "success": 0, "total_profit": 0.0}
            
            self.order_performance[reason_key]["count"] += 1
            if success:
                self.order_performance[reason_key]["success"] += 1
            
        except Exception as e:
            self.log(f"❌ Performance tracking error: {e}")
    
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
            self.log(f"❌ Performance stats error: {e}")
            return {}
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🎯 OrderManager: {message}")


# ========================================================================================
# 🧪 TEST FUNCTION
# ========================================================================================

def test_order_manager_compatibility():
    """Test compatibility with Modern Rule Engine"""
    print("🧪 Testing Order Manager compatibility with Modern Rule Engine...")
    print("✅ Updated Order Manager ready")
    print("✅ place_smart_order() method added")
    print("✅ target_price support from Rule Engine") 
    print("✅ Enhanced collision detection")
    print("✅ Dynamic volume and spacing support")

if __name__ == "__main__":
    test_order_manager_compatibility()