"""
🎯 Modern Order Manager - Market Order Enhanced Edition
order_manager.py

Enhanced Features:
- Market Order Approach (ไม่รอราคา)
- ลบ Collision Detection (วางได้เสมอ)
- 4D AI Integration Support
- Hybrid Entry Logic Support
- Dynamic Lot Sizing
- Smart Recovery Integration

** PRODUCTION READY - MARKET ORDER FOCUS **
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
    """ประเภทออเดอร์ - เน้น Market Orders"""
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"
    MARKET_BUY = "MARKET_BUY"      # ⭐ Primary focus
    MARKET_SELL = "MARKET_SELL"    # ⭐ Primary focus

class OrderStatus(Enum):
    """สถานะออเดอร์"""
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class OrderReason(Enum):
    """เหตุผลการวางออเดอร์ - Enhanced with 4D AI"""
    TREND_FOLLOWING = "TREND_FOLLOWING"
    MEAN_REVERSION = "MEAN_REVERSION"
    SUPPORT_RESISTANCE = "SUPPORT_RESISTANCE"
    VOLATILITY_BREAKOUT = "VOLATILITY_BREAKOUT"
    PORTFOLIO_BALANCE = "PORTFOLIO_BALANCE"      # ⭐ Primary focus
    GRID_EXPANSION = "GRID_EXPANSION"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"          # ⭐ Recovery focus
    FOUR_D_AI_ENTRY = "FOUR_D_AI_ENTRY"         # ⭐ New AI reason
    SMART_RECOVERY = "SMART_RECOVERY"            # ⭐ New recovery reason

@dataclass
class OrderRequest:
    """คำขอวางออเดอร์ - Enhanced for Market Orders"""
    order_type: OrderType
    volume: float
    price: float = 0.0                    # 0.0 for market orders
    sl: float = 0.0                       # No stop loss (use recovery instead)
    tp: float = 0.0                       # No take profit (use management)
    reason: OrderReason = OrderReason.PORTFOLIO_BALANCE
    confidence: float = 0.5
    reasoning: str = ""
    max_slippage: int = 20                # ⭐ Higher slippage for market orders
    magic_number: int = 100001
    four_d_score: float = 0.0             # ⭐ 4D AI Score
    hybrid_factors: Dict = None           # ⭐ Hybrid factors

@dataclass
class OrderResult:
    """ผลลัพธ์การวางออเดอร์ - Enhanced"""
    success: bool
    ticket: int = 0
    price: float = 0.0
    volume: float = 0.0
    message: str = ""
    slippage: float = 0.0                 # ⭐ Track actual slippage
    execution_time: float = 0.0           # ⭐ Track execution speed
    four_d_score: float = 0.0             # ⭐ Associated 4D score

# ========================================================================================
# 🎯 ENHANCED ORDER MANAGER CLASS
# ========================================================================================

class OrderManager:
    """
    🎯 Enhanced Order Manager - Market Order Focus
    
    ความสามารถใหม่:
    - Market Order Primary Approach
    - No Collision Detection (วางได้เสมอ)
    - 4D AI Integration 
    - Smart Recovery Support
    - Dynamic Execution Parameters
    - Enhanced Performance Tracking
    """
    
    def __init__(self, mt5_connector, spacing_manager, lot_calculator, config):
        """Initialize Enhanced Order Manager"""
        # Core components
        self.mt5_connector = mt5_connector
        self.spacing_manager = spacing_manager
        self.lot_calculator = lot_calculator
        self.config = config
        
        # Trading parameters
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.max_daily_orders = config.get("risk_management", {}).get("max_daily_orders", 100)
        self.min_lot = config.get("trading", {}).get("min_lot_size", 0.01)
        self.max_lot = config.get("trading", {}).get("max_lot_size", 1.0)
        
        # Market order parameters - Enhanced
        self.market_order_config = {
            "max_slippage_points": 30,        # ⭐ ยอมรับ slippage สูงขึ้น
            "retry_attempts": 3,              # ⭐ ลองใหม่ถ้าไม่สำเร็จ
            "retry_delay": 0.5,               # วินาที
            "execution_timeout": 10.0,        # Timeout สำหรับ market order
            "min_spacing_override": False      # ⭐ ไม่เช็ค spacing (วางได้เสมอ)
        }
        
        # Symbol info
        self.point_value = 0.01
        self.tick_size = 0.01
        self.min_distance = 30
        
        # Performance tracking - Enhanced
        self.order_performance = {}
        self.execution_stats = {
            "market_orders": {"count": 0, "success": 0, "avg_slippage": 0.0, "avg_execution_time": 0.0},
            "limit_orders": {"count": 0, "success": 0, "fill_rate": 0.0},
            "recovery_orders": {"count": 0, "success": 0, "recovery_rate": 0.0}
        }
        
        # State tracking
        self.daily_order_count = 0
        self.last_reset_date = datetime.now().date()
        self.last_order_time = datetime.now()
        self.order_history = deque(maxlen=100)
        
        # Initialize symbol info
        self._update_symbol_info()
        
        print("🎯 Enhanced Order Manager initialized - Market Order Focus")
        print(f"   Symbol: {self.symbol}")
        print(f"   Market Order Config: {self.market_order_config}")
    
    # ========================================================================================
    # ⚡ MARKET ORDER METHODS - CORE FEATURES
    # ========================================================================================
    
    def  place_market_order(self, order_request: OrderRequest) -> OrderResult:
        """⚡ แก้ไข: วาง Market Order ทันที พร้อม Enhanced Spacing Check"""
        try:
            start_time = time.time()
            
            print(f"⚡ === ENHANCED MARKET ORDER EXECUTION ===")
            print(f"   Type: {order_request.order_type.value}")
            print(f"   Volume: {order_request.volume:.3f}")
            print(f"   Reason: {order_request.reason.value}")
            print(f"   4D Score: {order_request.four_d_score:.3f}")
            print(f"   Confidence: {order_request.confidence:.3f}")
            
            # Validate connection
            if not self.mt5_connector.is_connected():
                return OrderResult(False, 0, 0.0, 0.0, "MT5 not connected", {})
            
            # ✅ เพิ่มใหม่: Enhanced Spacing Check
            try:
                # ดึง active orders
                active_orders = self.get_active_orders()
                print(f"📊 Active positions: {len(active_orders)}")
                
                # ดึง market analysis
                current_price = self.mt5_connector.get_current_price(self.symbol)
                
                if active_orders and current_price and hasattr(self, 'spacing_manager'):
                    # สร้าง basic market analysis ถ้าไม่มี
                    market_analysis = {
                        "market_score_4d": order_request.four_d_score,
                        "four_d_confidence": order_request.confidence,
                        "trend_direction": "SIDEWAYS",
                        "volatility_multiplier": 1.0,
                        "session_multiplier": 1.0,
                        "trend_strength": 1.0,
                        "volume_factor": 1.0
                    }
                    
                    # ตรวจสอบ collision
                    order_type_str = "BUY" if "BUY" in order_request.order_type.value else "SELL"
                    
                    spacing_result = self.spacing_manager.calculate_4d_spacing(
                        current_price, market_analysis, order_type_str, active_orders
                    )
                    
                    print(f"🎯 Enhanced Spacing Check:")
                    print(f"   Spacing: {spacing_result.spacing} points")
                    print(f"   Collision Detected: {spacing_result.collision_detected}")
                    print(f"   Placement Allowed: {spacing_result.placement_allowed}")
                    print(f"   Reasoning: {spacing_result.reasoning}")
                    
                    # ✅ ตรวจสอบการอนุญาต
                    if not spacing_result.placement_allowed:
                        print(f"❌ ORDER BLOCKED: Collision detected!")
                        return OrderResult(
                            False, 0, 0.0, 0.0, 
                            f"Blocked: {spacing_result.reasoning}", 
                            {"collision_detected": True, "spacing": spacing_result.spacing}
                        )
                    else:
                        print(f"✅ ORDER APPROVED: Safe to place")
                    
            except Exception as spacing_error:
                print(f"⚠️ Enhanced spacing check error: {spacing_error} - proceeding with order")
            
            # Validate daily limits
            if not self._check_daily_limits():
                return OrderResult(False, 0, 0.0, 0.0, "Daily order limit exceeded", {})
            
            # Get current price
            current_price = self.mt5_connector.get_current_price(self.symbol)
            if not current_price or current_price <= 0:
                return OrderResult(False, 0, 0.0, 0.0, "Invalid current price", {})
            
            # Prepare MT5 request
            if order_request.order_type == OrderType.MARKET_BUY:
                action = self.mt5_connector.mt5.TRADE_ACTION_DEAL
                order_type = self.mt5_connector.mt5.ORDER_TYPE_BUY
                price = current_price
            elif order_request.order_type == OrderType.MARKET_SELL:
                action = self.mt5_connector.mt5.TRADE_ACTION_DEAL
                order_type = self.mt5_connector.mt5.ORDER_TYPE_SELL
                price = current_price
            else:
                return OrderResult(False, 0, 0.0, 0.0, f"Unsupported order type: {order_request.order_type}", {})
            
            # Create request
            request = {
                "action": action,
                "symbol": self.symbol,
                "volume": order_request.volume,
                "type": order_type,
                "price": price,
                "magic": self.magic_number,
                "comment": f"{order_request.reason.value[:20]}|{order_request.confidence:.2f}",
                "type_filling": self.mt5_connector.mt5.ORDER_FILLING_FOK,
            }
            
            # Add slippage for market orders
            if order_request.max_slippage > 0:
                request["deviation"] = order_request.max_slippage
            
            print(f"📋 Order Request: {request}")
            
            # Execute order
            result = self.mt5_connector.mt5.order_send(request)
            execution_time = time.time() - start_time
            
            if result and result.retcode == self.mt5_connector.mt5.TRADE_RETCODE_DONE:
                # Success
                actual_price = float(result.price) if result.price else price
                actual_volume = float(result.volume) if result.volume else order_request.volume
                ticket = int(result.order) if result.order else 0
                
                slippage = abs(actual_price - price) / price * 10000  # in points
                
                print(f"✅ ENHANCED Market order SUCCESS:")
                print(f"   Ticket: {ticket}")
                print(f"   Price: {actual_price:.5f}")
                print(f"   Volume: {actual_volume:.3f}")
                print(f"   Slippage: {slippage:.1f} points")
                print(f"   Execution time: {execution_time:.3f}s")
                print(f"   Enhanced spacing: ✅ USED")
                
                # Update performance tracking
                self._track_order_performance(order_request, True, actual_price, execution_time, slippage)
                
                # Update daily counter
                self.daily_order_count += 1
                self.last_order_time = datetime.now()
                
                return OrderResult(
                    success=True,
                    ticket=ticket,
                    price=actual_price,
                    volume=actual_volume,
                    message=f"Enhanced market order executed successfully",
                    metadata={
                        "slippage": slippage,
                        "execution_time": execution_time,
                        "order_type": order_request.order_type.value,
                        "enhanced_spacing": True,  # ✅ flag ว่าใช้ enhanced spacing
                        "collision_check_passed": True
                    }
                )
            else:
                # Failed
                error_msg = f"Order failed - Code: {result.retcode if result else 'NO_RESULT'}"
                if result and hasattr(result, 'comment'):
                    error_msg += f", Comment: {result.comment}"
                
                print(f"❌ Enhanced market order FAILED: {error_msg}")
                
                # Update performance tracking
                self._track_order_performance(order_request, False, 0.0, execution_time, 0.0)
                
                return OrderResult(False, 0, 0.0, 0.0, error_msg, {"execution_time": execution_time})
        
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Enhanced market order exception: {str(e)}"
            print(f"❌ {error_msg}")
            
            return OrderResult(False, 0, 0.0, 0.0, error_msg, {"execution_time": execution_time})
    
    def get_active_orders(self) -> List[Dict]:
        """🆕 ดึงรายการออเดอร์ที่ใช้งานอยู่สำหรับ collision detection"""
        try:
            if not self.mt5_connector.is_connected:
                return []
            
            # ดึง positions ที่เปิดอยู่
            positions = self.mt5_connector.get_positions()
            if not positions:
                return []
            
            active_orders = []
            for pos in positions:
                try:
                    active_orders.append({
                        'ticket': pos.ticket,
                        'type': 'BUY' if pos.type == 0 else 'SELL',
                        'price': float(pos.price_open),
                        'volume': float(pos.volume),
                        'symbol': pos.symbol,
                        'profit': float(pos.profit),
                        'comment': pos.comment
                    })
                except Exception as e:
                    continue
            
            print(f"📊 Retrieved {len(active_orders)} active positions for collision check")
            return active_orders
            
        except Exception as e:
            print(f"❌ Get active orders error: {e}")
            return []

    def _prepare_mt5_market_request(self, order_request: OrderRequest, current_price: float) -> Dict:
        """เตรียม MT5 request สำหรับ Market Order"""
        try:
            # กำหนด order type สำหรับ MT5
            if order_request.order_type == OrderType.MARKET_BUY:
                mt5_order_type = mt5.ORDER_TYPE_BUY
                execution_price = current_price  # Market price
            elif order_request.order_type == OrderType.MARKET_SELL:
                mt5_order_type = mt5.ORDER_TYPE_SELL
                execution_price = current_price  # Market price
            else:
                raise ValueError(f"Not a market order type: {order_request.order_type}")
            
            # เตรียม request
            mt5_request = {
                "action": mt5.TRADE_ACTION_DEAL,        # ⭐ DEAL for immediate execution
                "symbol": self.symbol,
                "volume": order_request.volume,
                "type": mt5_order_type,
                "price": execution_price,
                "deviation": order_request.max_slippage,  # Slippage tolerance
                "magic": order_request.magic_number,
                "comment": f"{order_request.reason.value}|4D:{order_request.four_d_score:.2f}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK   # ⭐ Immediate or Cancel
            }
            
            # ไม่ใส่ SL/TP (ใช้ recovery system แทน)
            # if order_request.sl > 0:
            #     mt5_request["sl"] = order_request.sl
            # if order_request.tp > 0:
            #     mt5_request["tp"] = order_request.tp
            
            return mt5_request
            
        except Exception as e:
            self.log(f"❌ Prepare MT5 request error: {e}")
            return {}
    
    def _execute_market_order_with_retry(self, mt5_request: Dict, 
                                        order_request: OrderRequest) -> OrderResult:
        """Execute Market Order with Retry Logic"""
        try:
            max_attempts = self.market_order_config["retry_attempts"]
            retry_delay = self.market_order_config["retry_delay"]
            
            for attempt in range(max_attempts):
                print(f"🎯 Market order attempt {attempt + 1}/{max_attempts}")
                
                # ส่งออเดอร์
                result = mt5.order_send(mt5_request)
                
                if result is None:
                    error_msg = f"MT5 order_send returned None (attempt {attempt + 1})"
                    print(f"❌ {error_msg}")
                    
                    if attempt < max_attempts - 1:
                        time.sleep(retry_delay)
                        continue
                    else:
                        return OrderResult(False, 0, 0, 0, error_msg)
                
                # เช็คผลลัพธ์
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    # สำเร็จ!
                    actual_price = result.price
                    requested_price = mt5_request["price"]
                    slippage = abs(actual_price - requested_price)
                    
                    self.log(f"✅ Market order SUCCESS")
                    self.log(f"   Ticket: {result.order}")
                    self.log(f"   Price: {actual_price:.5f}")
                    self.log(f"   Slippage: {slippage:.5f}")
                    self.log(f"   Volume: {result.volume:.3f}")
                    
                    # Update counters
                    self.daily_order_count += 1
                    self.last_order_time = datetime.now()
                    
                    # Add to history
                    self.order_history.append({
                        'timestamp': datetime.now(),
                        'ticket': result.order,
                        'type': order_request.order_type.value,
                        'volume': result.volume,
                        'price': actual_price,
                        'reason': order_request.reason.value,
                        'four_d_score': order_request.four_d_score,
                        'slippage': slippage,
                        'attempt': attempt + 1
                    })
                    
                    return OrderResult(
                        success=True,
                        ticket=result.order,
                        price=actual_price,
                        volume=result.volume,
                        message="Market order executed successfully",
                        slippage=slippage,
                        execution_time=time.time() - time.time(),  # Will be updated by caller
                        four_d_score=order_request.four_d_score
                    )
                
                else:
                    # ไม่สำเร็จ
                    error_msg = f"MT5 error {result.retcode}: {result.comment}"
                    print(f"❌ {error_msg}")
                    
                    # เช็คว่าควรลองใหม่หรือไม่
                    if self._should_retry_market_order(result.retcode):
                        if attempt < max_attempts - 1:
                            print(f"🔄 Retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)
                            continue
                    
                    return OrderResult(False, 0, 0, 0, error_msg)
            
            return OrderResult(False, 0, 0, 0, "Max retry attempts reached")
            
        except Exception as e:
            self.log(f"❌ Execute market order error: {e}")
            return OrderResult(False, 0, 0, 0, f"Execution error: {e}")
    
    def _should_retry_market_order(self, retcode: int) -> bool:
        """ตัดสินใจว่าควรลองใหม่หรือไม่"""
        # Retryable errors
        retryable_codes = [
            mt5.TRADE_RETCODE_REQUOTE,
            mt5.TRADE_RETCODE_CONNECTION,
            mt5.TRADE_RETCODE_TIMEOUT,
            mt5.TRADE_RETCODE_PRICE_OFF,
            mt5.TRADE_RETCODE_REJECT
        ]
        
        return retcode in retryable_codes
    
    def _validate_market_order_inputs(self, order_request: OrderRequest) -> bool:
        """ตรวจสอบความถูกต้องของ Market Order inputs"""
        try:
            # เช็ค order type
            if order_request.order_type not in [OrderType.MARKET_BUY, OrderType.MARKET_SELL]:
                self.log(f"❌ Not a market order type: {order_request.order_type}")
                return False
            
            # เช็ค volume
            if order_request.volume < self.min_lot or order_request.volume > self.max_lot:
                self.log(f"❌ Invalid volume: {order_request.volume} (range: {self.min_lot}-{self.max_lot})")
                return False
            
            # เช็ค confidence
            if order_request.confidence < 0 or order_request.confidence > 1:
                self.log(f"❌ Invalid confidence: {order_request.confidence}")
                return False
            
            return True
            
        except Exception as e:
            self.log(f"❌ Market order validation error: {e}")
            return False
    
    # ========================================================================================
    # 🚀 HYBRID ENTRY METHODS - INTEGRATION WITH 4D AI
    # ========================================================================================
    
    def place_hybrid_entry_order(self, direction: str, four_d_analysis: Any, 
                                 hybrid_factors: Dict) -> OrderResult:
        """🚀 วาง Hybrid Entry Order ตาม 4D AI Analysis"""
        try:
            print(f"🚀 === HYBRID ENTRY ORDER ===")
            print(f"   Direction: {direction}")
            print(f"   4D Overall Score: {four_d_analysis.overall_score:.3f}")
            print(f"   Recommendation: {four_d_analysis.recommendation}")
            
            # คำนวณ volume ตาม 4D Analysis
            volume = self._calculate_4d_volume(four_d_analysis, hybrid_factors)
            
            # สร้าง OrderRequest
            order_type = OrderType.MARKET_BUY if direction == "BUY" else OrderType.MARKET_SELL
            
            order_request = OrderRequest(
                order_type=order_type,
                volume=volume,
                price=0.0,  # Market price
                reason=OrderReason.FOUR_D_AI_ENTRY,
                confidence=four_d_analysis.overall_score,
                reasoning=f"4D AI Hybrid Entry: {four_d_analysis.recommendation}",
                max_slippage=25,  # ยอมรับ slippage เพิ่ม
                four_d_score=four_d_analysis.overall_score,
                hybrid_factors=hybrid_factors
            )
            
            # Execute market order
            result = self.place_market_order(order_request)
            
            if result.success:
                print(f"✅ Hybrid entry executed: {volume:.3f} lots {direction}")
                print(f"   4D Score: {four_d_analysis.overall_score:.3f}")
                print(f"   Balance Factor: {hybrid_factors.get('balance_factor', 0):.3f}")
            else:
                print(f"❌ Hybrid entry failed: {result.message}")
            
            return result
            
        except Exception as e:
            self.log(f"❌ Hybrid entry order error: {e}")
            return OrderResult(False, 0, 0, 0, f"Hybrid entry error: {e}")
    
    def place_recovery_order(self, target_position: Dict, recovery_strategy: Dict,
                            four_d_analysis: Any) -> OrderResult:
        """🎯 วาง Recovery Order สำหรับ Smart Recovery"""
        try:
            print(f"🎯 === RECOVERY ORDER ===")
            print(f"   Target Position: {target_position.get('ticket', 'unknown')}")
            print(f"   Recovery Strategy: {recovery_strategy.get('action', 'unknown')}")
            print(f"   Hedge Direction: {recovery_strategy.get('direction', 'unknown')}")
            
            # สร้าง recovery order
            direction = recovery_strategy.get('direction', 'BUY')
            volume = recovery_strategy.get('volume', 0.01)
            
            order_type = OrderType.MARKET_BUY if direction == "BUY" else OrderType.MARKET_SELL
            
            order_request = OrderRequest(
                order_type=order_type,
                volume=volume,
                price=0.0,  # Market price
                reason=OrderReason.SMART_RECOVERY,
                confidence=four_d_analysis.hedge_opportunity_score,
                reasoning=f"Smart Recovery for position {target_position.get('ticket')}",
                max_slippage=30,  # ยอมรับ slippage สูงสำหรับ recovery
                four_d_score=four_d_analysis.overall_score
            )
            
            # Execute recovery order
            result = self.place_market_order(order_request)
            
            if result.success:
                print(f"✅ Recovery order executed: {volume:.3f} lots {direction}")
                print(f"   For position: {target_position.get('ticket')}")
                
                # Track recovery attempt
                self._track_recovery_attempt(target_position, result, recovery_strategy)
                
            else:
                print(f"❌ Recovery order failed: {result.message}")
            
            return result
            
        except Exception as e:
            self.log(f"❌ Recovery order error: {e}")
            return OrderResult(False, 0, 0, 0, f"Recovery error: {e}")
    
    def _calculate_4d_volume(self, four_d_analysis: Any, hybrid_factors: Dict) -> float:
        """คำนวณ Volume ตาม 4D Analysis"""
        try:
            # Base volume
            base_volume = 0.01
            
            # ปรับตาม 4D Overall Score
            score_multiplier = 1 + (four_d_analysis.overall_score - 0.5)  # 0.5-1.5 range
            
            # ปรับตาม Portfolio Safety
            safety_multiplier = 1.0
            if four_d_analysis.portfolio_safety_score > 0.8:
                safety_multiplier = 1.4  # ปลอดภัย = เพิ่มได้
            elif four_d_analysis.portfolio_safety_score < 0.3:
                safety_multiplier = 0.6  # อันตราย = ลดลง
            
            # ปรับตาม Balance Factor
            balance_factor = hybrid_factors.get('balance_factor', 0.5)
            balance_multiplier = 0.8 + (balance_factor * 0.4)  # 0.8-1.2 range
            
            # ปรับตาม Market Context
            market_multiplier = 1.0
            if four_d_analysis.market_context_score > 0.7:
                market_multiplier = 1.2  # ตลาดดี = เพิ่มได้
            elif four_d_analysis.market_context_score < 0.4:
                market_multiplier = 0.8  # ตลาดไม่ดี = ลดลง
            
            # คำนวณ volume สุดท้าย
            final_volume = (base_volume * score_multiplier * safety_multiplier * 
                           balance_multiplier * market_multiplier)
            
            # จำกัดขอบเขต
            final_volume = max(self.min_lot, min(final_volume, 0.08))  # ขั้นต่ำ min_lot, สูงสุด 0.08
            
            # Round ให้ถูกต้อง
            final_volume = round(final_volume, 2)
            
            print(f"📊 4D Volume Calculation:")
            print(f"   Base: {base_volume:.3f}")
            print(f"   Score Mult: {score_multiplier:.2f}")
            print(f"   Safety Mult: {safety_multiplier:.2f}")
            print(f"   Balance Mult: {balance_multiplier:.2f}")
            print(f"   Market Mult: {market_multiplier:.2f}")
            print(f"   Final Volume: {final_volume:.3f}")
            
            return final_volume
            
        except Exception as e:
            self.log(f"❌ 4D volume calculation error: {e}")
            return 0.01  # Safe default
    
    # ========================================================================================
    # 📊 PERFORMANCE TRACKING - ENHANCED
    # ========================================================================================
    
    def _track_market_order_performance(self, order_request: OrderRequest, 
                                       result: OrderResult, execution_time: float):
        """ติดตามประสิทธิภาพ Market Order"""
        try:
            # Update execution stats
            stats = self.execution_stats["market_orders"]
            stats["count"] += 1
            
            if result.success:
                stats["success"] += 1
                
                # Update average slippage
                if stats["count"] > 1:
                    stats["avg_slippage"] = (
                        (stats["avg_slippage"] * (stats["count"] - 1) + result.slippage) 
                        / stats["count"]
                    )
                else:
                    stats["avg_slippage"] = result.slippage
                
                # Update average execution time
                if stats["count"] > 1:
                    stats["avg_execution_time"] = (
                        (stats["avg_execution_time"] * (stats["count"] - 1) + execution_time)
                        / stats["count"]
                    )
                else:
                    stats["avg_execution_time"] = execution_time
            
            # Track by reason
            reason_key = order_request.reason.value
            if reason_key not in self.order_performance:
                self.order_performance[reason_key] = {
                    "count": 0, "success": 0, "total_profit": 0.0,
                    "avg_4d_score": 0.0, "avg_execution_time": 0.0
                }
            
            perf = self.order_performance[reason_key]
            perf["count"] += 1
            
            if result.success:
                perf["success"] += 1
                
                # Update average 4D score
                perf["avg_4d_score"] = (
                    (perf["avg_4d_score"] * (perf["count"] - 1) + order_request.four_d_score)
                    / perf["count"]
                )
                
                # Update average execution time
                perf["avg_execution_time"] = (
                    (perf["avg_execution_time"] * (perf["count"] - 1) + execution_time)
                    / perf["count"]
                )
            
            # Log performance update
            success_rate = stats["success"] / stats["count"]
            print(f"📊 Market Order Performance: {success_rate:.1%} ({stats['success']}/{stats['count']})")
            print(f"   Avg Slippage: {stats['avg_slippage']:.5f}")
            print(f"   Avg Execution: {stats['avg_execution_time']:.3f}s")
            
        except Exception as e:
            self.log(f"❌ Track market order performance error: {e}")
    
    def _track_recovery_attempt(self, target_position: Dict, result: OrderResult, 
                               recovery_strategy: Dict):
        """ติดตามความสำเร็จของ Recovery"""
        try:
            # Update recovery stats
            stats = self.execution_stats["recovery_orders"]
            stats["count"] += 1
            
            if result.success:
                stats["success"] += 1
                
                # Calculate recovery rate
                stats["recovery_rate"] = stats["success"] / stats["count"]
                
                print(f"📈 Recovery Stats: {stats['recovery_rate']:.1%} ({stats['success']}/{stats['count']})")
            
            # Log recovery attempt details
            recovery_log = {
                'timestamp': datetime.now(),
                'target_ticket': target_position.get('ticket', 0),
                'target_profit': target_position.get('profit', 0),
                'recovery_direction': recovery_strategy.get('direction', 'unknown'),
                'recovery_volume': result.volume,
                'success': result.success,
                'hedge_ticket': result.ticket if result.success else 0
            }
            
            # Store in order history
            self.order_history.append(recovery_log)
            
        except Exception as e:
            self.log(f"❌ Track recovery attempt error: {e}")
    
    # ========================================================================================
    # 🔧 UTILITY METHODS - ENHANCED
    # ========================================================================================
    
    def get_market_order_stats(self) -> Dict:
        """ดึงสถิติ Market Orders"""
        try:
            stats = self.execution_stats["market_orders"]
            
            if stats["count"] == 0:
                return {"message": "No market orders executed yet"}
            
            success_rate = stats["success"] / stats["count"]
            
            return {
                "total_orders": stats["count"],
                "successful_orders": stats["success"],
                "success_rate": f"{success_rate:.1%}",
                "average_slippage": f"{stats['avg_slippage']:.5f}",
                "average_execution_time": f"{stats['avg_execution_time']:.3f}s",
                "daily_count": self.daily_order_count,
                "last_order": self.last_order_time.strftime("%H:%M:%S") if self.last_order_time else "None"
            }
            
        except Exception as e:
            self.log(f"❌ Market order stats error: {e}")
            return {"error": str(e)}
    
    def get_recovery_stats(self) -> Dict:
        """ดึงสถิติ Recovery Orders"""
        try:
            stats = self.execution_stats["recovery_orders"]
            
            if stats["count"] == 0:
                return {"message": "No recovery orders executed yet"}
            
            return {
                "total_attempts": stats["count"],
                "successful_recoveries": stats["success"],
                "recovery_rate": f"{stats['recovery_rate']:.1%}",
                "recent_recoveries": len([h for h in self.order_history 
                                        if h.get('target_ticket') and 
                                        (datetime.now() - h.get('timestamp', datetime.now())).total_seconds() < 3600])
            }
            
        except Exception as e:
            self.log(f"❌ Recovery stats error: {e}")
            return {"error": str(e)}
    
    def get_recent_orders(self, count: int = 10) -> List[Dict]:
        """ดึงออเดอร์ล่าสุด"""
        try:
            recent_orders = list(self.order_history)[-count:] if self.order_history else []
            
            formatted_orders = []
            for order in recent_orders:
                formatted_orders.append({
                    'time': order.get('timestamp', datetime.now()).strftime('%H:%M:%S'),
                    'ticket': order.get('ticket', 0),
                    'type': order.get('type', 'unknown'),
                    'volume': f"{order.get('volume', 0):.3f}",
                    'price': f"{order.get('price', 0):.5f}",
                    'reason': order.get('reason', 'unknown'),
                    '4d_score': f"{order.get('four_d_score', 0):.3f}",
                    'slippage': f"{order.get('slippage', 0):.5f}" if 'slippage' in order else 'N/A'
                })
            
            return formatted_orders
            
        except Exception as e:
            self.log(f"❌ Recent orders error: {e}")
            return []
    
    def _get_current_price(self) -> float:
        """ดึงราคาปัจจุบัน"""
        try:
            if not self.mt5_connector.is_connected:
                return 0.0
            
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                return 0.0
            
            # ใช้ mid price
            return (tick.bid + tick.ask) / 2
            
        except Exception as e:
            self.log(f"❌ Get current price error: {e}")
            return 0.0
    
    def _update_symbol_info(self):
        """อัปเดตข้อมูล Symbol"""
        try:
            if not self.mt5_connector.is_connected:
                return
            
            symbol_info = mt5.symbol_info(self.symbol)
            if symbol_info:
                self.point_value = symbol_info.point
                self.tick_size = symbol_info.trade_tick_size
                self.min_distance = getattr(symbol_info, 'trade_stops_level', 30)
                
                print(f"📊 Symbol Info Updated:")
                print(f"   Point Value: {self.point_value}")
                print(f"   Tick Size: {self.tick_size}")
                print(f"   Min Distance: {self.min_distance}")
            
        except Exception as e:
            self.log(f"❌ Symbol info update error: {e}")
    
    # ========================================================================================
    # 🎮 LEGACY COMPATIBILITY METHODS - KEPT FOR TRANSITION
    # ========================================================================================
    
    def place_smart_order(self, order_type: str, volume: float, price: float,
                         reasoning: str = "", confidence: float = 0.5, **kwargs) -> Dict:
        """🎮 Legacy Compatibility Method - Routes to Market Orders"""
        try:
            print(f"🔄 Legacy smart order call - routing to market order")
            
            # แปลง legacy call เป็น modern OrderRequest
            if "BUY" in order_type.upper():
                modern_order_type = OrderType.MARKET_BUY
            elif "SELL" in order_type.upper():
                modern_order_type = OrderType.MARKET_SELL
            else:
                return {"success": False, "error": f"Unknown order type: {order_type}"}
            
            # สร้าง OrderRequest
            order_request = OrderRequest(
                order_type=modern_order_type,
                volume=volume,
                price=0.0,  # Market order
                reason=self._determine_order_reason(reasoning),
                confidence=confidence,
                reasoning=reasoning,
                max_slippage=20
            )
            
            # Execute
            result = self.place_market_order(order_request)
            
            # แปลงกลับเป็น legacy format
            return {
                "success": result.success,
                "ticket": result.ticket,
                "price": result.price,
                "volume": result.volume,
                "error": result.message if not result.success else "",
                "order_type": order_type,
                "direction": "BUY" if "BUY" in order_type else "SELL"
            }
            
        except Exception as e:
            self.log(f"❌ Legacy smart order error: {e}")
            return {"success": False, "error": str(e)}
    
    def place_smart_buy_order(self, confidence: float = 0.5, reasoning: str = "",
                             market_data: Dict = None) -> bool:
        """🎮 Legacy Method - Route to Market Buy"""
        try:
            # Get volume from legacy method or use default
            volume = market_data.get("rule_volume", 0.01) if market_data else 0.01
            
            order_request = OrderRequest(
                order_type=OrderType.MARKET_BUY,
                volume=volume,
                price=0.0,
                reason=OrderReason.PORTFOLIO_BALANCE,
                confidence=confidence,
                reasoning=reasoning,
                max_slippage=20
            )
            
            result = self.place_market_order(order_request)
            return result.success
            
        except Exception as e:
            self.log(f"❌ Legacy buy order error: {e}")
            return False
    
    def place_smart_sell_order(self, confidence: float = 0.5, reasoning: str = "",
                              market_data: Dict = None) -> bool:
        """🎮 Legacy Method - Route to Market Sell"""
        try:
            # Get volume from legacy method or use default
            volume = market_data.get("rule_volume", 0.01) if market_data else 0.01
            
            order_request = OrderRequest(
                order_type=OrderType.MARKET_SELL,
                volume=volume,
                price=0.0,
                reason=OrderReason.PORTFOLIO_BALANCE,
                confidence=confidence,
                reasoning=reasoning,
                max_slippage=20
            )
            
            result = self.place_market_order(order_request)
            return result.success
            
        except Exception as e:
            self.log(f"❌ Legacy sell order error: {e}")
            return False
    
    def get_pending_orders(self) -> List[Dict]:
        """ดึงออเดอร์ที่รออยู่ - สำหรับ compatibility"""
        try:
            if not self.mt5_connector.is_connected:
                return []
            
            orders = mt5.orders_get(symbol=self.symbol)
            if not orders:
                return []
            
            pending_orders = []
            for order in orders:
                pending_orders.append({
                    "ticket": order.ticket,
                    "type": self._order_type_to_string(order.type),
                    "volume": order.volume_initial,
                    "price": order.price_open,
                    "time": datetime.fromtimestamp(order.time_setup),
                    "comment": order.comment,
                    "magic": order.magic
                })
            
            return pending_orders
            
        except Exception as e:
            self.log(f"❌ Get pending orders error: {e}")
            return []
    
    def _determine_order_reason(self, reasoning: str) -> OrderReason:
        """แปลง reasoning text เป็น OrderReason"""
        reasoning_lower = reasoning.lower()
        
        if "4d ai" in reasoning_lower or "4d" in reasoning_lower:
            return OrderReason.FOUR_D_AI_ENTRY
        elif "recovery" in reasoning_lower or "hedge" in reasoning_lower:
            return OrderReason.SMART_RECOVERY
        elif "balance" in reasoning_lower:
            return OrderReason.PORTFOLIO_BALANCE
        elif "trend" in reasoning_lower:
            return OrderReason.TREND_FOLLOWING
        elif "reversion" in reasoning_lower:
            return OrderReason.MEAN_REVERSION
        elif "support" in reasoning_lower or "resistance" in reasoning_lower:
            return OrderReason.SUPPORT_RESISTANCE
        elif "breakout" in reasoning_lower or "volatility" in reasoning_lower:
            return OrderReason.VOLATILITY_BREAKOUT
        elif "risk" in reasoning_lower:
            return OrderReason.RISK_MANAGEMENT
        else:
            return OrderReason.GRID_EXPANSION  # Default
    
    def _order_type_to_string(self, order_type: int) -> str:
        """แปลง MT5 order type เป็น string"""
        type_mapping = {
            mt5.ORDER_TYPE_BUY: "MARKET_BUY",
            mt5.ORDER_TYPE_SELL: "MARKET_SELL",
            mt5.ORDER_TYPE_BUY_LIMIT: "BUY_LIMIT",
            mt5.ORDER_TYPE_SELL_LIMIT: "SELL_LIMIT",
            mt5.ORDER_TYPE_BUY_STOP: "BUY_STOP",
            mt5.ORDER_TYPE_SELL_STOP: "SELL_STOP"
        }
        return type_mapping.get(order_type, "UNKNOWN")
    
    # ========================================================================================
    # 🎯 ENHANCED ORDER PLACEMENT METHODS
    # ========================================================================================
    
    def place_immediate_entry(self, direction: str, reason: str = "IMMEDIATE_OPPORTUNITY") -> OrderResult:
        """🎯 วางออเดอร์ทันทีไม่รอเงื่อนไข - Emergency Entry"""
        try:
            print(f"🚨 === IMMEDIATE ENTRY ===")
            print(f"   Direction: {direction}")
            print(f"   Reason: {reason}")
            
            # คำนวณ volume แบบ conservative
            volume = 0.01  # Safe volume for immediate entry
            
            # สร้าง order request
            order_type = OrderType.MARKET_BUY if direction.upper() == "BUY" else OrderType.MARKET_SELL
            
            order_request = OrderRequest(
                order_type=order_type,
                volume=volume,
                price=0.0,
                reason=OrderReason.RISK_MANAGEMENT,
                confidence=0.8,  # High confidence for immediate action
                reasoning=f"Immediate Entry: {reason}",
                max_slippage=50  # ยอมรับ slippage สูงเพื่อความรวดเร็ว
            )
            
            # Execute ทันที
            result = self.place_market_order(order_request)
            
            if result.success:
                print(f"⚡ Immediate entry executed: {volume:.3f} lots {direction}")
            else:
                print(f"❌ Immediate entry failed: {result.message}")
            
            return result
            
        except Exception as e:
            self.log(f"❌ Immediate entry error: {e}")
            return OrderResult(False, 0, 0, 0, f"Immediate entry error: {e}")
    
    def place_balanced_entry(self, imbalance_ratio: float) -> OrderResult:
        """🎯 วางออเดอร์เพื่อสร้างสมดุล Portfolio"""
        try:
            print(f"⚖️ === BALANCED ENTRY ===")
            print(f"   Imbalance Ratio: {imbalance_ratio:.3f}")
            
            # ตัดสินใจทิศทางจาก imbalance
            if imbalance_ratio > 0:
                # มี BUY มากเกินไป -> วาง SELL
                direction = "SELL"
                order_type = OrderType.MARKET_SELL
            else:
                # มี SELL มากเกินไป -> วาง BUY
                direction = "BUY"
                order_type = OrderType.MARKET_BUY
            
            # คำนวณ volume ตาม imbalance
            base_volume = 0.01
            imbalance_multiplier = min(abs(imbalance_ratio) * 2, 1.5)  # ยิ่งไม่สมดุล ยิ่งเพิ่ม volume
            volume = round(base_volume * (1 + imbalance_multiplier), 2)
            volume = max(self.min_lot, min(volume, 0.05))  # จำกัด 0.05
            
            # สร้าง order request
            order_request = OrderRequest(
                order_type=order_type,
                volume=volume,
                price=0.0,
                reason=OrderReason.PORTFOLIO_BALANCE,
                confidence=0.7 + min(abs(imbalance_ratio), 0.3),  # ยิ่งไม่สมดุล ยิ่งมั่นใจ
                reasoning=f"Portfolio Balance: {direction} to fix imbalance {imbalance_ratio:.3f}",
                max_slippage=25
            )
            
            # Execute
            result = self.place_market_order(order_request)
            
            if result.success:
                print(f"⚖️ Balance entry executed: {volume:.3f} lots {direction}")
                print(f"   Imbalance correction: {imbalance_ratio:.3f}")
            else:
                print(f"❌ Balance entry failed: {result.message}")
            
            return result
            
        except Exception as e:
            self.log(f"❌ Balanced entry error: {e}")
            return OrderResult(False, 0, 0, 0, f"Balance entry error: {e}")
    
    # ========================================================================================
    # 📊 MONITORING & DIAGNOSTICS
    # ========================================================================================
    
    def get_order_manager_status(self) -> Dict:
        """ดึงสถานะ Order Manager แบบครบถ้วน"""
        try:
            return {
                'connection_status': self.mt5_connector.is_connected if self.mt5_connector else False,
                'symbol': self.symbol,
                'daily_order_count': self.daily_order_count,
                'max_daily_orders': self.max_daily_orders,
                'market_order_config': self.market_order_config,
                'execution_stats': self.execution_stats,
                'recent_orders_count': len(self.order_history),
                'performance_by_reason': self.get_order_performance_stats(),
                'current_price': self._get_current_price(),
                'symbol_info': {
                    'point_value': self.point_value,
                    'tick_size': self.tick_size,
                    'min_distance': self.min_distance
                }
            }
            
        except Exception as e:
            self.log(f"❌ Order manager status error: {e}")
            return {'error': str(e)}
    
    def diagnose_order_issues(self) -> List[str]:
        """🔍 วินิจฉัยปัญหาการวางออเดอร์"""
        try:
            issues = []
            
            # เช็ค connection
            if not self.mt5_connector.is_connected:
                issues.append("❌ MT5 connection lost")
            
            # เช็ค daily limits
            if self.daily_order_count >= self.max_daily_orders:
                issues.append(f"⚠️ Daily order limit reached: {self.daily_order_count}/{self.max_daily_orders}")
            
            # เช็ค success rate
            stats = self.execution_stats["market_orders"]
            if stats["count"] > 10:  # มีข้อมูลพอ
                success_rate = stats["success"] / stats["count"]
                if success_rate < 0.8:
                    issues.append(f"⚠️ Low market order success rate: {success_rate:.1%}")
            
            # เช็ค slippage
            if stats["count"] > 5 and stats["avg_slippage"] > 0.0005:  # 5 points
                issues.append(f"⚠️ High average slippage: {stats['avg_slippage']:.5f}")
            
            # เช็ค execution time
            if stats["count"] > 5 and stats["avg_execution_time"] > 2.0:
                issues.append(f"⚠️ Slow execution time: {stats['avg_execution_time']:.2f}s")
            
            return issues if issues else ["✅ No issues detected"]
            
        except Exception as e:
            self.log(f"❌ Diagnose issues error: {e}")
            return [f"❌ Diagnostic error: {e}"]
    
    def reset_daily_counters(self):
        """🔄 รีเซ็ต counters รายวัน"""
        try:
            self.daily_order_count = 0
            self.last_reset_date = datetime.now().date()
            self.log("🔄 Daily counters reset")
            
        except Exception as e:
            self.log(f"❌ Reset counters error: {e}")
    
    def get_execution_efficiency(self) -> Dict:
        """📊 วิเคราะห์ประสิทธิภาพการ execute"""
        try:
            total_orders = sum(stats["count"] for stats in self.execution_stats.values())
            total_successes = sum(stats["success"] for stats in self.execution_stats.values())
            
            overall_success_rate = total_successes / total_orders if total_orders > 0 else 0
            
            return {
                "overall_success_rate": f"{overall_success_rate:.1%}",
                "total_orders_today": self.daily_order_count,
                "market_orders": self.execution_stats["market_orders"],
                "recovery_orders": self.execution_stats["recovery_orders"],
                "efficiency_score": min(overall_success_rate * 1.2, 1.0)  # Bonus for high success
            }
            
        except Exception as e:
            self.log(f"❌ Execution efficiency error: {e}")
            return {"error": str(e)}
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🎯 OrderManager: {message}")
    
    # ========================================================================================
    # 🎯 SPECIAL MARKET ORDER VARIANTS
    # ========================================================================================
    
    def place_opportunity_order(self, opportunity_data: Dict) -> OrderResult:
        """🎯 วางออเดอร์จากโอกาสพิเศษ"""
        try:
            direction = opportunity_data.get('direction', 'BUY')
            confidence = opportunity_data.get('confidence', 0.6)
            reasoning = opportunity_data.get('reasoning', 'Market opportunity detected')
            
            order_type = OrderType.MARKET_BUY if direction == "BUY" else OrderType.MARKET_SELL
            
            # Volume ตาม confidence
            volume = 0.01 + (confidence - 0.5) * 0.02  # 0.01-0.02 range
            volume = max(self.min_lot, min(volume, 0.03))
            
            order_request = OrderRequest(
                order_type=order_type,
                volume=volume,
                price=0.0,
                reason=OrderReason.VOLATILITY_BREAKOUT,
                confidence=confidence,
                reasoning=reasoning,
                max_slippage=35  # ยอมรับ slippage เพิ่มสำหรับโอกาส
            )
            
            return self.place_market_order(order_request)
            
        except Exception as e:
            self.log(f"❌ Opportunity order error: {e}")
            return OrderResult(False, 0, 0, 0, f"Opportunity error: {e}")
    
    def place_time_based_order(self, time_factor: float) -> OrderResult:
        """🕐 วางออเดอร์ตาม Time Factor"""
        try:
            if time_factor < 0.5:
                return OrderResult(False, 0, 0, 0, "Time factor too low")
            
            # ยิ่งห่างจาก last action ยิ่งมี pressure ให้เข้า
            direction = "BUY" if datetime.now().minute % 2 == 0 else "SELL"  # Simple alternating
            
            order_type = OrderType.MARKET_BUY if direction == "BUY" else OrderType.MARKET_SELL
            volume = 0.01 + (time_factor - 0.5) * 0.01  # เพิ่ม volume ตาม time pressure
            
            order_request = OrderRequest(
                order_type=order_type,
                volume=round(volume, 2),
                price=0.0,
                reason=OrderReason.GRID_EXPANSION,
                confidence=0.5 + time_factor * 0.3,
                reasoning=f"Time-based entry: factor {time_factor:.3f}",
                max_slippage=20
            )
            
            return self.place_market_order(order_request)
            
        except Exception as e:
            self.log(f"❌ Time-based order error: {e}")
            return OrderResult(False, 0, 0, 0, f"Time-based error: {e}")
    
    # ========================================================================================
    # 🔧 ENHANCED UTILITY METHODS
    # ========================================================================================
    
    def force_market_entry(self, direction: str, volume: float = 0.01, 
                          reason: str = "FORCED_ENTRY") -> OrderResult:
        """🚨 บังคับเข้าตลาดทันที - Emergency Method"""
        try:
            print(f"🚨 === FORCE MARKET ENTRY ===")
            print(f"   Direction: {direction}")
            print(f"   Volume: {volume:.3f}")
            print(f"   Reason: {reason}")
            
            order_type = OrderType.MARKET_BUY if direction.upper() == "BUY" else OrderType.MARKET_SELL
            
            order_request = OrderRequest(
                order_type=order_type,
                volume=volume,
                price=0.0,
                reason=OrderReason.RISK_MANAGEMENT,
                confidence=1.0,  # Maximum confidence for forced entry
                reasoning=f"FORCED: {reason}",
                max_slippage=100  # ยอมรับ slippage สูงมาก
            )
            
            result = self.place_market_order(order_request)
            
            if result.success:
                print(f"🚨 FORCED entry executed: {volume:.3f} lots {direction}")
            else:
                print(f"❌ FORCED entry failed: {result.message}")
            
            return result
            
        except Exception as e:
            self.log(f"❌ Force market entry error: {e}")
            return OrderResult(False, 0, 0, 0, f"Force entry error: {e}")
    
    def get_order_performance_stats(self) -> Dict[str, Dict]:
        """ดึงสถิติประสิทธิภาพแยกตาม reason"""
        try:
            stats = {}
            
            for reason, data in self.order_performance.items():
                if data["count"] > 0:
                    success_rate = data["success"] / data["count"]
                    avg_profit = data["total_profit"] / data["count"]
                    avg_4d_score = data.get("avg_4d_score", 0)
                    avg_execution = data.get("avg_execution_time", 0)
                else:
                    success_rate = avg_profit = avg_4d_score = avg_execution = 0.0
                
                stats[reason] = {
                    "total_orders": data["count"],
                    "successful_orders": data["success"],
                    "success_rate": round(success_rate, 3),
                    "total_profit": round(data["total_profit"], 2),
                    "average_profit": round(avg_profit, 2),
                    "avg_4d_score": round(avg_4d_score, 3),
                    "avg_execution_time": round(avg_execution, 3)
                }
            
            return stats
            
        except Exception as e:
            self.log(f"❌ Performance stats error: {e}")
            return {}
    
    def cleanup_old_tracking_data(self, days_to_keep: int = 7):
        """🧹 ทำความสะอาดข้อมูลติดตาม"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # ทำความสะอาด order_history
            original_count = len(self.order_history)
            self.order_history = deque([
                order for order in self.order_history 
                if order.get('timestamp', datetime.now()) > cutoff_date
            ], maxlen=100)
            
            cleaned_count = original_count - len(self.order_history)
            
            if cleaned_count > 0:
                print(f"🧹 Cleaned {cleaned_count} old order records")
            
        except Exception as e:
            self.log(f"❌ Cleanup tracking data error: {e}")
    
    def emergency_stop_all_orders(self) -> Dict:
        """🚨 หยุดการวางออเดอร์ฉุกเฉิน"""
        try:
            print("🚨 === EMERGENCY STOP ===")
            
            # ไม่ได้ cancel ออเดอร์ที่วางแล้ว (เป็น position แล้ว)
            # แต่หยุดการวางออเดอร์ใหม่
            
            # Reset daily counter เพื่อหยุดวางออเดอร์
            original_limit = self.max_daily_orders
            self.max_daily_orders = 0
            
            result = {
                "emergency_stop_activated": True,
                "timestamp": datetime.now().isoformat(),
                "original_daily_limit": original_limit,
                "current_daily_count": self.daily_order_count,
                "message": "Order placement stopped. Use restore_order_placement() to resume."
            }
            
            print("🚨 Emergency stop activated - order placement halted")
            return result
            
        except Exception as e:
            self.log(f"❌ Emergency stop error: {e}")
            return {"error": str(e)}
    
    def restore_order_placement(self):
        """🔄 คืนค่าการวางออเดอร์หลัง emergency stop"""
        try:
            # คืนค่า daily limit
            self.max_daily_orders = self.config.get("risk_management", {}).get("max_daily_orders", 100)
            
            print(f"🔄 Order placement restored - daily limit: {self.max_daily_orders}")
            
        except Exception as e:
            self.log(f"❌ Restore order placement error: {e}")
    
    def get_detailed_execution_report(self) -> str:
        """📊 รายงานการ execution แบบละเอียด"""
        try:
            report_lines = []
            report_lines.append("📊 DETAILED EXECUTION REPORT")
            report_lines.append("=" * 50)
            
            # Overall stats
            total_orders = sum(stats["count"] for stats in self.execution_stats.values())
            total_successes = sum(stats["success"] for stats in self.execution_stats.values())
            overall_rate = total_successes / total_orders if total_orders > 0 else 0
            
            report_lines.append(f"Overall Performance: {overall_rate:.1%} ({total_successes}/{total_orders})")
            report_lines.append("")
            
            # Market order stats
            market_stats = self.execution_stats["market_orders"]
            if market_stats["count"] > 0:
                market_rate = market_stats["success"] / market_stats["count"]
                report_lines.append(f"📈 Market Orders: {market_rate:.1%} ({market_stats['success']}/{market_stats['count']})")
                report_lines.append(f"   Avg Slippage: {market_stats['avg_slippage']:.5f}")
                report_lines.append(f"   Avg Execution: {market_stats['avg_execution_time']:.3f}s")
                report_lines.append("")
            
            # Recovery stats
            recovery_stats = self.execution_stats["recovery_orders"]
            if recovery_stats["count"] > 0:
                recovery_rate = recovery_stats["success"] / recovery_stats["count"]
                report_lines.append(f"🎯 Recovery Orders: {recovery_rate:.1%} ({recovery_stats['success']}/{recovery_stats['count']})")
                report_lines.append("")
            
            # Performance by reason
            if self.order_performance:
                report_lines.append("📊 Performance by Reason:")
                for reason, stats in self.order_performance.items():
                    if stats["count"] > 0:
                        rate = stats["success"] / stats["count"]
                        report_lines.append(f"   {reason}: {rate:.1%} ({stats['success']}/{stats['count']})")
                report_lines.append("")
            
            # Recent activity
            if self.order_history:
                report_lines.append("🕒 Recent Orders (last 5):")
                recent_orders = list(self.order_history)[-5:]
                for order in recent_orders:
                    time_str = order.get('timestamp', datetime.now()).strftime('%H:%M:%S')
                    ticket = order.get('ticket', 0)
                    order_type = order.get('type', 'unknown')
                    volume = order.get('volume', 0)
                    price = order.get('price', 0)
                    report_lines.append(f"   {time_str} | #{ticket} | {order_type} | {volume:.3f} @ {price:.5f}")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            self.log(f"❌ Detailed report error: {e}")
            return f"Report generation error: {e}"