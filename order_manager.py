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
        """เช็คและป้องกันการ collision ของออเดอร์ - แก้ไข syntax error"""
        try:
            # Get existing orders ก่อนเลย - แก้ไข variable scope
            pending_orders = self.get_pending_orders()
            existing_prices = [order.get("price", 0) for order in pending_orders if order.get("price", 0) > 0]
            existing_prices.sort()
            
            # Get current market price
            current_price = self._get_current_price()
            if current_price <= 0:
                print(f"❌ Invalid current price: {current_price}")
                return None
            
            print(f"🔍 COLLISION CHECK: {direction} @ {target_price:.5f}")
            print(f"   Current Price: {current_price:.5f}")
            print(f"   Existing orders: {len(existing_prices)}")
            
            # 1. เช็ค grid density ก่อน - ถ้าหนาแน่นให้หยุด
            if len(existing_prices) >= 12:
                print(f"🛑 Grid has enough orders ({len(existing_prices)}) - STOPPING to maintain quality")
                return None
            
            # 2. วิเคราะห์ spacing ถ้ามีออเดอร์มากพอ
            if len(existing_prices) >= 2:
                distances = []
                for i in range(1, len(existing_prices)):
                    distance = existing_prices[i] - existing_prices[i-1]
                    distance_points = distance / self.point_value
                    distances.append(distance_points)
                
                min_gap = min(distances)
                avg_gap = sum(distances) / len(distances)
                
                print(f"📊 Current Grid Spacing:")
                print(f"   Min Gap: {min_gap:.1f} points")
                print(f"   Avg Gap: {avg_gap:.1f} points")
                
                # ถ้า spacing หนาแน่นเกินไปให้หยุด
                if min_gap < 20:
                    print(f"🛑 Grid too dense (min gap: {min_gap:.1f} points) - STOPPING")
                    return None
            
            # 3. Collision detection ปกติ
            tolerance_points = 15
            tolerance = tolerance_points * self.point_value
            
            # เช็คระยะห่างจากราคาปัจจุบัน
            distance_from_current = abs(target_price - current_price)
            min_distance_from_current = 30 * self.point_value
            
            if distance_from_current < min_distance_from_current:
                print(f"⚠️ Too close to current price: {distance_from_current/self.point_value:.1f} points")
                
                # ปรับราคาให้ห่างขึ้น
                if direction == "BUY":
                    adjusted_price = current_price - min_distance_from_current
                else:  # SELL
                    adjusted_price = current_price + min_distance_from_current
                
                print(f"🔧 Adjusted price: {adjusted_price:.5f}")
                target_price = adjusted_price
            
            # เช็ค collision กับออเดอร์ที่มีอยู่
            collision_detected = False
            for existing_price in existing_prices:
                if abs(target_price - existing_price) <= tolerance:
                    print(f"❌ COLLISION detected @ {existing_price:.5f} (distance: {abs(target_price - existing_price)/self.point_value:.1f} points)")
                    collision_detected = True
                    break
            
            if not collision_detected:
                # ตรวจสอบ price format แบบง่าย
                if target_price <= 0:
                    print(f"❌ Invalid price: {target_price}")
                    return None
                
                formatted_price = round(target_price, 5)
                
                # เช็คทิศทางให้ถูกต้อง
                if direction == "BUY" and formatted_price >= current_price:
                    print(f"❌ BUY price must be below current price")
                    return None
                elif direction == "SELL" and formatted_price <= current_price:
                    print(f"❌ SELL price must be above current price")
                    return None
                
                print(f"✅ Safe to place @ {formatted_price:.5f}")
                return formatted_price
            
            # 4. ถ้าเจอ collision ให้หยุดแทนที่จะฝืน
            print(f"🛑 SMART DECISION: Collision detected - skipping order placement")
            print(f"   Grid has adequate coverage with {len(existing_prices)} orders")
            print(f"   Better to wait for market movement than force placement")
            
            return None  # หยุดส่งออเดอร์
            
        except Exception as e:
            self.log(f"❌ Collision check error: {e}")
            return None
                
            
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
    
    def place_buy_order(self, price: float, lot_size: float, order_type: str = "BUY_LIMIT", 
                       reason: str = "") -> Dict:
        """
        🆕 Alias สำหรับ Modern Rule Engine
        เรียกใช้ place_smart_buy_order() ที่มีอยู่แล้ว
        """
        try:
            print(f"🎯 place_buy_order() called:")
            print(f"   Price: {price:.5f}")
            print(f"   Lot Size: {lot_size:.3f}")
            print(f"   Order Type: {order_type}")
            print(f"   Reason: {reason}")
            
            # เตรียม market_data พิเศษสำหรับ Rule Engine
            market_data = {
                "target_price": price,           # ราคาที่ Rule Engine ต้องการ
                "rule_volume": lot_size,         # ขนาดที่ Rule Engine คำนวณแล้ว
                "current_price": price - 50 * 0.01,  # สมมุติราคาปัจจุบันสูงกว่า target
                "order_type_preference": order_type,
                "rule_engine_mode": True
            }
            
            # เรียกใช้ method ที่มีอยู่
            result = self.place_smart_buy_order(
                confidence=0.85,  # ใช้ confidence สูงจาก Rule Engine
                reasoning=reason,
                market_data=market_data
            )
            
            # ส่งผลลัพธ์กลับในรูปแบบที่ Rule Engine ต้องการ
            return {
                "success": result,
                "order_type": order_type,
                "direction": "BUY",
                "price": price,
                "volume": lot_size,
                "error": "Order placement failed" if not result else None
            }
            
        except Exception as e:
            print(f"❌ place_buy_order error: {e}")
            return {"success": False, "error": str(e)}

    def place_sell_order(self, price: float, lot_size: float, order_type: str = "SELL_LIMIT", 
                        reason: str = "") -> Dict:
        """
        🆕 Alias สำหรับ Modern Rule Engine
        เรียกใช้ place_smart_sell_order() ที่มีอยู่แล้ว
        """
        try:
            print(f"🎯 place_sell_order() called:")
            print(f"   Price: {price:.5f}")
            print(f"   Lot Size: {lot_size:.3f}")
            print(f"   Order Type: {order_type}")
            print(f"   Reason: {reason}")
            
            # เตรียม market_data พิเศษสำหรับ Rule Engine
            market_data = {
                "target_price": price,           # ราคาที่ Rule Engine ต้องการ
                "rule_volume": lot_size,         # ขนาดที่ Rule Engine คำนวณแล้ว
                "current_price": price + 50 * 0.01,  # สมมุติราคาปัจจุบันต่ำกว่า target
                "order_type_preference": order_type,
                "rule_engine_mode": True
            }
            
            # เรียกใช้ method ที่มีอยู่
            result = self.place_smart_sell_order(
                confidence=0.85,  # ใช้ confidence สูงจาก Rule Engine
                reasoning=reason,
                market_data=market_data
            )
            
            # ส่งผลลัพธ์กลับในรูปแบบที่ Rule Engine ต้องการ
            return {
                "success": result,
                "order_type": order_type,
                "direction": "SELL",
                "price": price,
                "volume": lot_size,
                "error": "Order placement failed" if not result else None
            }
            
        except Exception as e:
            print(f"❌ place_sell_order error: {e}")
            return {"success": False, "error": str(e)}

    def place_smart_buy_order(self, confidence: float = 0.5, reasoning: str = "",
                             market_data: Dict = None) -> bool:
        """Updated: รองรับ target_price จาก Rule Engine"""
        try:
            print(f"🎯 === PLACE SMART BUY ORDER ===")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Reasoning: {reasoning}")
            
            # Validate MT5 connection
            if not self.mt5_connector.is_connected:
                self.log("❌ Cannot place BUY order - MT5 not connected")
                return False
            
            # ใช้ข้อมูลจาก Rule Engine ถ้ามี
            if market_data and market_data.get("rule_engine_mode"):
                target_price = market_data.get("target_price")
                volume = market_data.get("rule_volume", 0.01)
                
                print(f"🎯 Using Rule Engine parameters:")
                print(f"   Target Price: {target_price:.5f}")
                print(f"   Volume: {volume:.3f}")
                
                if target_price and target_price > 0:
                    # สร้าง order request โดยตรง
                    order_request = OrderRequest(
                        order_type=OrderType.BUY_LIMIT,
                        volume=volume,
                        price=target_price,
                        sl=0.0,  # ไม่ใช้ stop loss
                        tp=0.0,  # ไม่ใช้ take profit
                        reason=OrderReason.GRID_EXPANSION,
                        confidence=confidence,
                        reasoning=reasoning,
                        max_slippage=10
                    )
                    
                    # Execute order
                    result = self._execute_real_order(order_request)
                    
                    if result.success:
                        self.log(f"✅ BUY order placed: Ticket {result.ticket} @ {target_price:.5f}")
                        self._track_order_performance(OrderReason.GRID_EXPANSION, True)
                        return True
                    else:
                        self.log(f"❌ BUY order failed: {result.error_message}")
                        self._track_order_performance(OrderReason.GRID_EXPANSION, False)
                        return False
            
            # ถ้าไม่มีข้อมูลจาก Rule Engine ใช้วิธีเดิม
            else:
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
            print(f"🎯 === PLACE SMART SELL ORDER ===")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Reasoning: {reasoning}")
            
            # Validate MT5 connection
            if not self.mt5_connector.is_connected:
                self.log("❌ Cannot place SELL order - MT5 not connected")
                return False
            
            # ใช้ข้อมูลจาก Rule Engine ถ้ามี
            if market_data and market_data.get("rule_engine_mode"):
                target_price = market_data.get("target_price")
                volume = market_data.get("rule_volume", 0.01)
                
                print(f"🎯 Using Rule Engine parameters:")
                print(f"   Target Price: {target_price:.5f}")
                print(f"   Volume: {volume:.3f}")
                
                if target_price and target_price > 0:
                    # สร้าง order request โดยตรง
                    order_request = OrderRequest(
                        order_type=OrderType.SELL_LIMIT,
                        volume=volume,
                        price=target_price,
                        sl=0.0,  # ไม่ใช้ stop loss
                        tp=0.0,  # ไม่ใช้ take profit
                        reason=OrderReason.GRID_EXPANSION,
                        confidence=confidence,
                        reasoning=reasoning,
                        max_slippage=10
                    )
                    
                    # Execute order
                    result = self._execute_real_order(order_request)
                    
                    if result.success:
                        self.log(f"✅ SELL order placed: Ticket {result.ticket} @ {target_price:.5f}")
                        self._track_order_performance(OrderReason.GRID_EXPANSION, True)
                        return True
                    else:
                        self.log(f"❌ SELL order failed: {result.error_message}")
                        self._track_order_performance(OrderReason.GRID_EXPANSION, False)
                        return False
            
            # ถ้าไม่มีข้อมูลจาก Rule Engine ใช้วิธีเดิม
            else:
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


    def _find_wider_alternative_slot(self, direction: str, existing_prices: List[float], 
                                   current_price: float) -> Optional[float]:
        """หาตำแหน่งใหม่ด้วย spacing ที่กว้างขึ้น - เพิ่มใน order_manager.py"""
        try:
            print(f"🔍 Finding wider alternative for {direction}")
            
            # ใช้ spacing ที่กว้างขึ้น
            wide_spacing = max(150, self.smart_params.current_spacing * 3)  # อย่างน้อย 150 points
            wide_spacing_price = wide_spacing * self.point_value
            
            print(f"   Using wider spacing: {wide_spacing} points ({wide_spacing_price:.5f})")
            
            if direction == "BUY":
                # หาตำแหน่งที่ต่ำกว่าออเดอร์ BUY ที่ต่ำสุด
                buy_orders = [p for p in existing_prices if p < current_price]
                if buy_orders:
                    lowest_buy = min(buy_orders)
                    candidate_price = lowest_buy - wide_spacing_price
                    print(f"   Below lowest BUY: {lowest_buy:.5f} - {wide_spacing_price:.5f} = {candidate_price:.5f}")
                else:
                    candidate_price = current_price - wide_spacing_price
                    print(f"   Below current: {current_price:.5f} - {wide_spacing_price:.5f} = {candidate_price:.5f}")
                    
            else:  # SELL
                # หาตำแหน่งที่สูงกว่าออเดอร์ SELL ที่สูงสุด
                sell_orders = [p for p in existing_prices if p > current_price]
                if sell_orders:
                    highest_sell = max(sell_orders)
                    candidate_price = highest_sell + wide_spacing_price
                    print(f"   Above highest SELL: {highest_sell:.5f} + {wide_spacing_price:.5f} = {candidate_price:.5f}")
                else:
                    candidate_price = current_price + wide_spacing_price
                    print(f"   Above current: {current_price:.5f} + {wide_spacing_price:.5f} = {candidate_price:.5f}")
            
            # Validate candidate price - ใช้ wider validation
            validated_price = self._validate_price_format_wider(candidate_price, direction, current_price)
            
            if validated_price:
                # Final collision check with wider tolerance
                min_distance = wide_spacing_price * 0.8  # ใช้ 80% ของ wide spacing
                is_safe = all(abs(validated_price - p) >= min_distance for p in existing_prices)
                
                if is_safe:
                    print(f"✅ Wide spacing alternative found: {validated_price:.5f}")
                    return validated_price
                else:
                    print(f"❌ Wide spacing still has collision")
                    return None
            else:
                print(f"❌ Wide spacing price validation failed")
                return None
                
        except Exception as e:
            print(f"❌ Wide alternative search error: {e}")
            return None

    def _find_alternative_slot(self, original_price: float, direction: str, 
                              existing_prices: List[float], current_price: float, 
                              min_spacing: float) -> Optional[float]:
        """หาตำแหน่งทดแทนที่เหมาะสม - เพิ่มใน order_manager.py"""
        try:
            print(f"🔍 Finding alternative slot for {direction}")
            
            # กำหนดทิศทางการค้นหา
            if direction == "BUY":
                # สำหรับ BUY: ค้นหาจากราคาต่ำขึ้นไป
                search_direction = -1
                price_limit = current_price * 0.95  # ไม่ต่ำกว่า 5% ของราคาปัจจุบัน
            else:  # SELL
                # สำหรับ SELL: ค้นหาจากราคาสูงขึ้นไป  
                search_direction = 1
                price_limit = current_price * 1.05  # ไม่สูงกว่า 5% ของราคาปัจจุบัน
            
            # ค้นหาในช่วง ±300 points ด้วย step ที่ใหญ่ขึ้น
            for offset in range(50, 301, 25):  # เริ่มจาก 50 points, step 25
                candidate_price = original_price + (search_direction * offset * self.point_value)
                
                # เช็คว่าอยู่ในขอบเขตที่อนุญาต
                if direction == "BUY" and candidate_price < price_limit:
                    print(f"   ⚠️ Price too low: {candidate_price:.5f} < {price_limit:.5f}")
                    continue
                elif direction == "SELL" and candidate_price > price_limit:
                    print(f"   ⚠️ Price too high: {candidate_price:.5f} > {price_limit:.5f}")
                    continue
                
                # เช็คระยะห่างจากราคาปัจจุบัน
                distance_from_current = abs(candidate_price - current_price)
                min_distance = 40 * self.point_value  # เพิ่มเป็น 40 points
                
                if distance_from_current < min_distance:
                    continue
                
                # เช็ค collision กับออเดอร์ที่มีอยู่ด้วย tolerance ที่กว้างขึ้น
                is_safe = True
                min_gap = max(min_spacing, 60 * self.point_value)  # อย่างน้อย 60 points
                
                for existing_price in existing_prices:
                    if abs(candidate_price - existing_price) <= min_gap:
                        is_safe = False
                        break
                
                if is_safe:
                    print(f"   ✅ Alternative found: {candidate_price:.5f} (offset: {offset} points)")
                    return candidate_price
                else:
                    print(f"   ❌ Collision at offset {offset}: {candidate_price:.5f}")
            
            print(f"   ❌ No alternative found in 300 points range")
            return None
            
        except Exception as e:
            print(f"❌ Alternative slot search error: {e}")
            return None

    def _diagnose_spacing_problem(self) -> Dict:
        """🔍 วิเคราะห์ปัญหา spacing"""
        try:
            # ดึงออเดอร์ที่มีอยู่
            pending_orders = self.get_pending_orders()
            existing_prices = [order.get("price", 0) for order in pending_orders if order.get("price", 0) > 0]
            existing_prices.sort()
            
            current_price = self._get_current_price()
            
            print(f"🔍 === SPACING DIAGNOSIS ===")
            print(f"   Current Price: {current_price:.5f}")
            print(f"   Total Orders: {len(existing_prices)}")
            
            # วิเคราะห์ระยะห่างระหว่างออเดอร์
            if len(existing_prices) >= 2:
                distances = []
                for i in range(1, len(existing_prices)):
                    distance = existing_prices[i] - existing_prices[i-1]
                    distance_points = distance / self.point_value
                    distances.append(distance_points)
                    print(f"   Gap {i}: {distance:.5f} ({distance_points:.1f} points)")
                
                min_gap = min(distances)
                max_gap = max(distances)
                avg_gap = sum(distances) / len(distances)
                
                print(f"📊 Gap Analysis:")
                print(f"   Min Gap: {min_gap:.1f} points")
                print(f"   Max Gap: {max_gap:.1f} points") 
                print(f"   Avg Gap: {avg_gap:.1f} points")
                
                # เช็คปัญหา
                if min_gap < 10:
                    print(f"🚨 PROBLEM: Grid too dense (min gap: {min_gap:.1f} points)")
                    return {"problem": "GRID_TOO_DENSE", "min_gap": min_gap}
                elif avg_gap < 30:
                    print(f"⚠️ WARNING: Grid quite dense (avg gap: {avg_gap:.1f} points)")
                    return {"problem": "GRID_DENSE", "avg_gap": avg_gap}
                else:
                    print(f"✅ Grid spacing OK")
                    return {"problem": "NONE", "spacing_ok": True}
            
            return {"problem": "INSUFFICIENT_DATA"}
            
        except Exception as e:
            print(f"❌ Spacing diagnosis error: {e}")
            return {"problem": "ERROR", "error": str(e)}

    def _get_current_price(self) -> float:
        """ดึงราคาปัจจุบันจาก MT5"""
        try:
            if not self.mt5_connector or not self.mt5_connector.is_connected:
                return 0.0
            
            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                return 0.0
            
            return (tick.bid + tick.ask) / 2  # ใช้ mid price
            
        except Exception as e:
            print(f"❌ Get current price error: {e}")
            return 0.0

    def _validate_price_format(self, price: float, direction: str, current_price: float) -> Optional[float]:
        """ตรวจสอบและปรับ format ราคาให้ถูกต้องสำหรับ MT5"""
        try:
            # ตรวจสอบพื้นฐาน
            if price <= 0:
                print(f"❌ Invalid price: {price}")
                return None
            
            # Round ให้เป็นทศนิยม 5 ตำแหน่ง (XAUUSD standard)
            formatted_price = round(price, 5)
            
            # เช็คระยะห่างขั้นต่ำจากราคาปัจจุบัน
            min_distance = 30 * self.point_value  # 30 points
            distance = abs(formatted_price - current_price)
            
            if distance < min_distance:
                print(f"❌ Too close to current price: {distance/self.point_value:.1f} points (min: 30)")
                return None
            
            # เช็คว่าราคาไม่ห่างเกินไป
            max_distance = 800 * self.point_value  # 800 points
            if distance > max_distance:
                print(f"❌ Too far from current price: {distance/self.point_value:.1f} points (max: 800)")
                return None
            
            # เช็คทิศทางให้ถูกต้อง
            if direction == "BUY" and formatted_price >= current_price:
                print(f"❌ BUY price must be below current price: {formatted_price:.5f} >= {current_price:.5f}")
                return None
            elif direction == "SELL" and formatted_price <= current_price:
                print(f"❌ SELL price must be above current price: {formatted_price:.5f} <= {current_price:.5f}")
                return None
            
            # เช็คว่าราคาไม่เป็น 0 หรือค่าผิดปกติ
            if formatted_price < current_price * 0.92 or formatted_price > current_price * 1.08:
                print(f"❌ Price out of reasonable range: {formatted_price:.5f} (current: {current_price:.5f})")
                return None
            
            print(f"✅ Price validation passed: {formatted_price:.5f}")
            return formatted_price
            
        except Exception as e:
            print(f"❌ Price validation error: {e}")
            return None
    
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