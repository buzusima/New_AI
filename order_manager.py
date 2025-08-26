"""
🎯 Modern Order Manager - Market Order Enhanced Edition
order_manager.py - แก้ไขปัญหาการส่ง Order แล้ว

แก้ไขปัญหา:
- ❌ NO_RESPONSE จาก MT5 
- ❌ All filling types failed
- ❌ Order execution loop failures
- ✅ Enhanced validation
- ✅ Smart retry logic  
- ✅ Better error handling

** ใช้ชื่อ Class และ Method เดิม - ไม่เปลี่ยน **
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

# ========================================================================================
# 📊 DATA CLASSES & ENUMS - ใช้ชื่อเดิม
# ========================================================================================

class OrderType(Enum):
    """ประเภทออเดอร์ - ใช้ชื่อเดิมทั้งหมด"""
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"
    MARKET_BUY = "MARKET_BUY"      
    MARKET_SELL = "MARKET_SELL"    

class OrderStatus(Enum):
    """สถานะออเดอร์ - ใช้ชื่อเดิม"""
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class OrderReason(Enum):
    """เหตุผลการวางออเดอร์ - ใช้ชื่อเดิม"""
    TREND_FOLLOWING = "TREND_FOLLOWING"
    MEAN_REVERSION = "MEAN_REVERSION"
    SUPPORT_RESISTANCE = "SUPPORT_RESISTANCE"
    VOLATILITY_BREAKOUT = "VOLATILITY_BREAKOUT"
    PORTFOLIO_BALANCE = "PORTFOLIO_BALANCE"      
    GRID_EXPANSION = "GRID_EXPANSION"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"          
    FOUR_D_AI_ENTRY = "FOUR_D_AI_ENTRY"         
    SMART_RECOVERY = "SMART_RECOVERY"            

@dataclass
class OrderRequest:
    """คำขอวางออเดอร์ - ใช้ชื่อเดิม"""
    order_type: OrderType
    volume: float
    price: float = 0.0                    
    sl: float = 0.0                       
    tp: float = 0.0                       
    reason: OrderReason = OrderReason.PORTFOLIO_BALANCE
    confidence: float = 0.5
    reasoning: str = ""
    max_slippage: int = 20                
    magic_number: int = 100001
    four_d_score: float = 0.0             
    hybrid_factors: Dict = None           

@dataclass
class OrderResult:
    """ผลลัพธ์การวางออเดอร์ - ใช้ชื่อเดิม"""
    success: bool
    ticket: int = 0
    price: float = 0.0
    volume: float = 0.0
    message: str = ""
    slippage: float = 0.0                 
    execution_time: float = 0.0           
    four_d_score: float = 0.0             
    metadata: Dict = None                 
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

# ========================================================================================
# 🎯 ORDER MANAGER CLASS - ใช้ชื่อเดิม
# ========================================================================================

class OrderManager:
    """
    🎯 Enhanced Order Manager - ใช้ชื่อคลาสเดิม
    แก้ไขปัญหาการส่ง Order แล้ว
    """
    
    def __init__(self, mt5_connector, spacing_manager, lot_calculator, config):
        """Initialize Enhanced Order Manager - ชื่อเดิม"""
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
            "max_slippage_points": 30,        
            "retry_attempts": 3,              
            "retry_delay": 0.5,               
            "execution_timeout": 10.0,        
            "min_spacing_override": False      
        }
        
        # Symbol info
        self.point_value = 0.01
        self.tick_size = 0.01
        self.min_distance = 30
        
        # Performance tracking
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
        
        print("🎯 Enhanced Order Manager initialized - แก้ไขปัญหาการส่ง Order แล้ว")
        print(f"   Symbol: {self.symbol}")
        print(f"   Market Order Config: {self.market_order_config}")

    # ========================================================================================
    # ⚡ MAIN METHODS - ใช้ชื่อเดิมทั้งหมด
    # ========================================================================================
    
    def place_market_order(self, order_request: OrderRequest) -> OrderResult:
        """⚡ วาง Market Order ทันที - METHOD หลัก - แก้ไขแล้ว"""
        try:
            start_time = time.time()
            
            print(f"⚡ === PLACE MARKET ORDER (FIXED) ===")
            print(f"   Type: {order_request.order_type.value}")
            print(f"   Volume: {order_request.volume:.3f}")
            print(f"   Reason: {order_request.reason.value}")
            print(f"   Confidence: {order_request.confidence:.3f}")
            
            # 🔧 FIX 1: Enhanced validation
            if not self._validate_market_order_inputs_enhanced(order_request):
                return OrderResult(False, 0, 0.0, 0.0, "Order validation failed", metadata={})
            
            # 🔧 FIX 2: Check daily limits
            if not self._check_daily_limits():
                return OrderResult(False, 0, 0.0, 0.0, "Daily order limit reached", metadata={})
            
            # 🔧 FIX 3: Enhanced MT5 connection check
            if not self._validate_mt5_connection_enhanced():
                return OrderResult(False, 0, 0.0, 0.0, "MT5 connection validation failed", metadata={})
            
            # 🔧 FIX 4: Get current price
            current_price = self._get_current_price()
            if current_price <= 0:
                return OrderResult(False, 0, 0.0, 0.0, "Invalid current price", metadata={})
            
            # 🔧 FIX 5: Prepare enhanced MT5 request
            mt5_request = self._prepare_mt5_market_request_enhanced(order_request, current_price)
            if not mt5_request:
                return OrderResult(False, 0, 0.0, 0.0, "Failed to prepare MT5 request", metadata={})
            
            # 🔧 FIX 6: Execute with smart retry
            result = self._execute_market_order_with_retry(mt5_request, order_request)
            
            # Set execution time
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            
            # Update tracking
            if result.success:
                self.daily_order_count += 1
                self.last_order_time = datetime.now()
                print(f"✅ Market order SUCCESS: Ticket {result.ticket}")
            else:
                print(f"❌ Market order FAILED: {result.message}")
            
            # Update stats
            self._update_execution_stats(result.success, execution_time, result.slippage)
            
            return result
            
        except Exception as e:
            print(f"❌ Place market order error: {e}")
            return OrderResult(False, 0, 0.0, 0.0, f"Execution error: {e}", metadata={})

    def execute_market_order_to_mt5(self, order_request: OrderRequest) -> OrderResult:
        """Execute market order โดยส่งออเดอร์จริงไป MT5 - ใช้ชื่อเดิม - แก้ไขแล้ว"""
        try:
            start_time = time.time()
            
            print(f"⚡ === EXECUTE MARKET ORDER TO MT5 (FIXED) ===")
            print(f"   Type: {order_request.order_type.value}")
            print(f"   Volume: {order_request.volume:.3f}")
            print(f"   Reason: {order_request.reason.value}")
            print(f"   4D Score: {order_request.four_d_score:.3f}")
            print(f"   Confidence: {order_request.confidence:.3f}")
            
            # Enhanced validation with detailed checks
            if not self.mt5_connector.is_connected:
                return OrderResult(False, 0, 0.0, 0.0, "MT5 not connected", metadata={})
            
            # Check MT5 connection and trading permissions
            terminal_info = mt5.terminal_info()
            if terminal_info is None:
                return OrderResult(False, 0, 0.0, 0.0, "MT5 terminal not accessible", metadata={})
            
            print(f"🔌 MT5 Terminal: {terminal_info.name} (Connected: {terminal_info.connected})")
            
            # Check account info
            account_info = mt5.account_info()
            if account_info is None:
                return OrderResult(False, 0, 0.0, 0.0, "MT5 account not logged in", metadata={})
            
            print(f"👤 Account: {account_info.login} (Trade Allowed: {account_info.trade_allowed})")
            
            if not account_info.trade_allowed:
                return OrderResult(False, 0, 0.0, 0.0, "Trading not allowed on this account", metadata={})
            
            # Get current price
            current_price = self._get_current_price()
            if current_price <= 0:
                return OrderResult(False, 0, 0.0, 0.0, "Invalid current price", metadata={})
            
            print(f"📊 Current Price: {current_price:.5f}")
            
            # Get proper execution price from MT5 tick
            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                return OrderResult(False, 0, 0.0, 0.0, f"Cannot get tick for {self.symbol}", metadata={})
            
            # Use proper bid/ask for execution
            if order_request.order_type == OrderType.MARKET_BUY:
                mt5_action = mt5.TRADE_ACTION_DEAL
                mt5_order_type = mt5.ORDER_TYPE_BUY
                execution_price = tick.ask  # Use ASK for BUY
            elif order_request.order_type == OrderType.MARKET_SELL:
                mt5_action = mt5.TRADE_ACTION_DEAL
                mt5_order_type = mt5.ORDER_TYPE_SELL
                execution_price = tick.bid  # Use BID for SELL
            else:
                return OrderResult(False, 0, 0.0, 0.0, f"Unsupported order type: {order_request.order_type}", metadata={})
            
            print(f"💱 Execution Price: {execution_price:.5f} (Spread: {tick.ask - tick.bid:.5f})")
            
            # สร้าง MT5 request
            mt5_request = {
                "action": mt5_action,
                "symbol": self.symbol,
                "volume": order_request.volume,
                "type": mt5_order_type,
                "price": execution_price,
                "deviation": order_request.max_slippage,
                "magic": getattr(order_request, 'magic_number', 100001),
                "comment": f"4D AI Gold: {order_request.reasoning[:20]}",
                "type_time": mt5.ORDER_TIME_GTC,
            }
            
            # Try different type_filling options with error handling
            filling_options = [
                (mt5.ORDER_FILLING_IOC, "IOC"),      # Immediate or Cancel
                (mt5.ORDER_FILLING_RETURN, "RETURN"), # Return/Partial
                (mt5.ORDER_FILLING_FOK, "FOK"),      # Fill or Kill
            ]
            
            print(f"📋 MT5 Request: {mt5_request}")
            
            # Try multiple filling types if first fails
            last_error = None
            successful_result = None
            
            for filling_type, filling_name in filling_options:
                try:
                    mt5_request["type_filling"] = filling_type
                    
                    print(f"🚀 Sending order to MT5 ({filling_name})...")
                    result = mt5.order_send(mt5_request)
                    execution_time = time.time() - start_time
                    
                    print(f"📨 MT5 Response ({filling_name}): {result}")
                    
                    # Check if successful
                    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                        successful_result = result
                        print(f"✅ Order executed successfully with {filling_name}")
                        break
                    elif result and result.retcode != mt5.TRADE_RETCODE_DONE:
                        # Record error but continue trying
                        error_msg = f"Retcode: {result.retcode}"
                        if hasattr(result, 'comment'):
                            error_msg += f", Comment: {result.comment}"
                        
                        print(f"⚠️ {filling_name} failed: {error_msg}")
                        last_error = error_msg
                        
                        # If it's not a filling type error, stop trying
                        if result.retcode not in [mt5.TRADE_RETCODE_INVALID_FILL, 
                                                mt5.TRADE_RETCODE_INVALID_ORDER,
                                                mt5.TRADE_RETCODE_REJECT]:
                            print(f"❌ Non-filling related error, stopping attempts")
                            break
                    else:
                        print(f"❌ {filling_name}: No response from MT5")
                        last_error = "No response from MT5"
                        
                except Exception as filling_error:
                    print(f"❌ {filling_name} exception: {filling_error}")
                    last_error = str(filling_error)
                    continue
            
            # Check final result
            if successful_result and successful_result.retcode == mt5.TRADE_RETCODE_DONE:
                # Success - order is now in MT5!
                actual_price = successful_result.price if hasattr(successful_result, 'price') else execution_price
                actual_volume = successful_result.volume if hasattr(successful_result, 'volume') else order_request.volume
                ticket = successful_result.order if hasattr(successful_result, 'order') else 0
                
                # Calculate slippage
                requested_price = execution_price
                slippage_points = abs(actual_price - requested_price) if actual_price > 0 else 0
                slippage_pips = slippage_points / self.point_value if self.point_value > 0 else 0
                
                print(f"✅ MARKET ORDER SUCCESS:")
                print(f"   Ticket: {ticket}")
                print(f"   Price: {actual_price:.5f} (requested: {requested_price:.5f})")
                print(f"   Slippage: {slippage_points:.5f} points ({slippage_pips:.1f} pips)")
                print(f"   Volume: {actual_volume:.3f}")
                print(f"   Execution Time: {execution_time:.3f}s")
                
                # Update statistics
                self._update_execution_stats(True, execution_time, slippage_points)
                
                # Store history
                order_history = {
                    'timestamp': datetime.now(),
                    'ticket': ticket,
                    'type': order_request.order_type.value,
                    'volume': actual_volume,
                    'price': actual_price,
                    'slippage': slippage_points,
                    'execution_time': execution_time,
                    'success': True,
                    'four_d_score': order_request.four_d_score,
                    'confidence': order_request.confidence
                }
                self.order_history.append(order_history)
                
                return OrderResult(
                    success=True,
                    ticket=ticket,
                    price=actual_price,
                    volume=actual_volume,
                    message=f"Market order executed successfully",
                    slippage=slippage_points,
                    execution_time=execution_time,
                    four_d_score=order_request.four_d_score,
                    metadata={
                        "mt5_result": successful_result,
                        "slippage_pips": slippage_pips,
                        "order_type": order_request.order_type.value,
                        "reason": order_request.reason.value,
                        "confidence": order_request.confidence
                    }
                )
                
            else:
                # Failed - tried all filling types
                error_code = successful_result.retcode if successful_result else "NO_RESPONSE"
                error_comment = successful_result.comment if successful_result and hasattr(successful_result, 'comment') else last_error
                
                error_msg = f"MT5 Order Failed (All filling types tried) - Code: {error_code}, Comment: {error_comment}"
                
                print(f"❌ MARKET ORDER FAILED:")
                print(f"   Error Code: {error_code}")
                print(f"   Error Comment: {error_comment}")
                print(f"   Tried filling types: IOC, RETURN, FOK")
                print(f"   Request: {mt5_request}")
                print(f"   Execution Time: {execution_time:.3f}s")
                
                # Update statistics
                self._update_execution_stats(False, execution_time, 0)
                
                # Store history
                order_history = {
                    'timestamp': datetime.now(),
                    'ticket': 0,
                    'type': order_request.order_type.value,
                    'volume': order_request.volume,
                    'price': execution_price,
                    'slippage': 0,
                    'execution_time': execution_time,
                    'success': False,
                    'error_code': error_code,
                    'error_comment': error_comment,
                    'four_d_score': order_request.four_d_score,
                    'confidence': order_request.confidence
                }
                self.order_history.append(order_history)
                
                return OrderResult(
                    success=False,
                    ticket=0,
                    price=0.0,
                    volume=0.0,
                    message=error_msg,
                    execution_time=execution_time,
                    metadata={
                        "error_code": error_code,
                        "error_comment": error_comment,
                        "mt5_result": successful_result,
                        "attempted_filling_types": ["IOC", "RETURN", "FOK"]
                    }
                )
                
        except Exception as e:
            print(f"❌ Execute market order to MT5 error: {e}")
            return OrderResult(False, 0, 0.0, 0.0, f"Execution error: {e}", metadata={})

    def _execute_market_order_with_retry(self, mt5_request: Dict, order_request: OrderRequest) -> OrderResult:
        """Execute market order with retry logic - ใช้ชื่อเดิม - แก้ไขแล้ว"""
        try:
            max_attempts = self.market_order_config.get("retry_attempts", 3)
            retry_delay = self.market_order_config.get("retry_delay", 0.5)
            
            # 🔧 FIX: ลำดับ filling types ที่ดีกว่า
            filling_options = [
                (mt5.ORDER_FILLING_IOC, "IOC"),      # Immediate or Cancel (ดีที่สุด)
                (mt5.ORDER_FILLING_RETURN, "RETURN"), # Return/Partial fill
                (mt5.ORDER_FILLING_FOK, "FOK"),      # Fill or Kill (เข้มงวดที่สุด)
            ]
            
            for attempt in range(max_attempts):
                try:
                    self.log(f"🚀 Executing market order (attempt {attempt + 1}/{max_attempts})")
                    
                    # ลอง filling types ทีละตัว
                    last_error = None
                    successful_result = None
                    
                    for filling_type, filling_name in filling_options:
                        try:
                            # ตั้ง filling type
                            mt5_request["type_filling"] = filling_type
                            
                            print(f"🚀 Trying {filling_name} filling type...")
                            
                            # ส่ง order
                            result = mt5.order_send(mt5_request)
                            
                            if result is None:
                                last_error = f"{filling_name}: No response from MT5"
                                print(f"❌ {last_error}")
                                continue
                            
                            print(f"📨 MT5 Response ({filling_name}): Retcode={result.retcode}")
                            
                            # เช็คความสำเร็จ
                            if result.retcode == mt5.TRADE_RETCODE_DONE:
                                print(f"✅ Order executed successfully with {filling_name}")
                                successful_result = result
                                break
                            else:
                                error_msg = f"{filling_name}: Error {result.retcode}"
                                if hasattr(result, 'comment'):
                                    error_msg += f" - {result.comment}"
                                last_error = error_msg
                                print(f"❌ {error_msg}")
                                
                        except Exception as filling_error:
                            last_error = f"{filling_name} exception: {filling_error}"
                            print(f"❌ {last_error}")
                            continue
                    
                    # ตรวจสอบผลลัพธ์
                    if successful_result:
                        # ✅ สำเร็จ!
                        actual_price = successful_result.price if hasattr(successful_result, 'price') else 0.0
                        actual_volume = successful_result.volume if hasattr(successful_result, 'volume') else order_request.volume
                        ticket = successful_result.order if hasattr(successful_result, 'order') else 0
                        
                        return OrderResult(
                            success=True,
                            ticket=ticket,
                            price=actual_price,
                            volume=actual_volume,
                            message=f"Market order executed successfully",
                            slippage=0.0,  
                            execution_time=0.0,  
                            four_d_score=order_request.four_d_score,
                            metadata={"mt5_result": successful_result}
                        )
                        
                    else:
                        # ❌ ล้มเหลวทุก filling type
                        if attempt < max_attempts - 1:
                            self.log(f"🔄 All filling types failed, retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)
                            continue
                        else:
                            return OrderResult(
                                success=False,
                                ticket=0,
                                price=0.0,
                                volume=0.0,
                                message=f"MT5 order failed: {last_error}",
                                execution_time=0.0,
                                metadata={"last_error": last_error}
                            )
                            
                except Exception as e:
                    self.log(f"❌ Market order execution error (attempt {attempt + 1}): {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(retry_delay)
                        continue
                    return OrderResult(False, 0, 0, 0, f"Execution error: {e}")
            
            return OrderResult(False, 0, 0, 0, "Max retry attempts reached")
            
        except Exception as e:
            self.log(f"❌ Execute market order with retry error: {e}")
            return OrderResult(False, 0, 0, 0, f"Retry execution error: {e}")

    def _prepare_mt5_market_request_enhanced(self, order_request: OrderRequest, current_price: float) -> Dict:
        """เตรียม MT5 request สำหรับ Market Order - ใช้ชื่อเดิม - แก้ไขแล้ว"""
        try:
            # 🔧 FIX: ดึงราคาจาก tick ใหม่ทุกครั้ง
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                print(f"❌ Cannot get fresh tick data for {self.symbol}")
                return {}
            
            print(f"📊 Fresh Tick - Bid: {tick.bid:.5f}, Ask: {tick.ask:.5f}, Spread: {tick.ask - tick.bid:.5f}")
            
            # 🔧 FIX: กำหนด order type และราคาที่ถูกต้อง
            if order_request.order_type in [OrderType.MARKET_BUY]:
                mt5_order_type = mt5.ORDER_TYPE_BUY
                execution_price = tick.ask  # ใช้ ask สำหรับ BUY
                print(f"📈 BUY Order - Using ASK price: {execution_price:.5f}")
            elif order_request.order_type in [OrderType.MARKET_SELL]:
                mt5_order_type = mt5.ORDER_TYPE_SELL
                execution_price = tick.bid   # ใช้ bid สำหรับ SELL
                print(f"📉 SELL Order - Using BID price: {execution_price:.5f}")
            else:
                print(f"❌ Unsupported order type: {order_request.order_type}")
                return {}
            
            # 🔧 FIX: สร้าง request ที่สมบูรณ์
            mt5_request = {
                "action": mt5.TRADE_ACTION_DEAL,        # DEAL สำหรับ immediate execution
                "symbol": self.symbol,
                "volume": order_request.volume,
                "type": mt5_order_type,
                "price": execution_price,               
                "deviation": order_request.max_slippage,
                "magic": getattr(order_request, 'magic_number', 100001),
                "comment": f"SmartGrid: {order_request.reason.value[:15]}",
                "type_time": mt5.ORDER_TIME_GTC,
                # type_filling จะถูกตั้งค่าใน _execute_market_order_with_retry
            }
            
            print(f"✅ Enhanced MT5 Request prepared:")
            print(f"   Action: TRADE_ACTION_DEAL")
            print(f"   Symbol: {self.symbol}")
            print(f"   Volume: {order_request.volume}")
            print(f"   Type: {mt5_order_type}")
            print(f"   Price: {execution_price:.5f}")
            print(f"   Deviation: {order_request.max_slippage}")
            
            return mt5_request
            
        except Exception as e:
            print(f"❌ Prepare enhanced MT5 request error: {e}")
            return {}

    def _validate_mt5_connection_enhanced(self) -> bool:
        """เช็ค MT5 connection อย่างละเอียด - ใช้ชื่อเดิม - แก้ไขแล้ว"""
        try:
            # เช็คว่า MT5 module โหลดได้
            if not hasattr(mt5, 'terminal_info'):
                print("❌ MT5 module not properly loaded")
                return False
            
            # เช็ค terminal info
            terminal_info = mt5.terminal_info()
            if terminal_info is None:
                print("❌ Cannot get terminal info - MT5 not running?")
                return False
            
            print(f"🔌 Terminal: {terminal_info.name} - Connected: {terminal_info.connected}")
            
            # เช็คว่า connected
            if not terminal_info.connected:
                print("❌ MT5 terminal not connected to trade server")
                return False
            
            # เช็ค account info
            account_info = mt5.account_info()
            if account_info is None:
                print("❌ Cannot get account info - not logged in?")
                return False
            
            print(f"👤 Account: {account_info.login} - Balance: {account_info.balance:.2f}")
            
            # เช็ค trade permissions
            if not account_info.trade_allowed:
                print("❌ Trading not allowed on this account")
                return False
            
            if not account_info.trade_expert:
                print("❌ Expert Advisor trading not allowed")
                return False
            
            # เช็ค symbol
            symbol_info = mt5.symbol_info(self.symbol)
            if symbol_info is None:
                print(f"❌ Symbol {self.symbol} not found")
                # ลองหา symbol ใหม่
                symbols = mt5.symbols_get()
                if symbols:
                    gold_symbols = [s.name for s in symbols if 'XAU' in s.name or 'GOLD' in s.name]
                    print(f"💡 Available gold symbols: {gold_symbols[:5]}")
                return False
            
            print(f"📊 Symbol: {symbol_info.name} - Spread: {symbol_info.spread}")
            
            # เช็ค trading hours
            if hasattr(symbol_info, 'trade_mode'):
                if symbol_info.trade_mode == mt5.SYMBOL_TRADE_MODE_DISABLED:
                    print(f"❌ Trading disabled for {self.symbol}")
                    return False
            
            print("✅ Enhanced MT5 Connection Validation PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Enhanced MT5 connection validation error: {e}")
            return False

    def _validate_market_order_inputs_enhanced(self, order_request: OrderRequest) -> bool:
        """ตรวจสอบความถูกต้องของ Market Order inputs - ใช้ชื่อเดิม - แก้ไขแล้ว"""
        try:
            # เช็ค order type
            valid_types = [OrderType.MARKET_BUY, OrderType.MARKET_SELL]
            if order_request.order_type not in valid_types:
                print(f"❌ Invalid order type: {order_request.order_type}")
                return False
            
            # เช็ค volume
            if order_request.volume < self.min_lot or order_request.volume > self.max_lot:
                print(f"❌ Invalid volume: {order_request.volume} (range: {self.min_lot}-{self.max_lot})")
                return False
            
            # เช็ค confidence
            if order_request.confidence < 0 or order_request.confidence > 1:
                print(f"❌ Invalid confidence: {order_request.confidence}")
                return False
            
            # เช็ค connection - FIX: ใช้ property ไม่ใช่ method
            if not self.mt5_connector.is_connected:
                print("❌ MT5 not connected")
                return False
            
            print("✅ Order inputs validation passed")
            return True
            
        except Exception as e:
            print(f"❌ Input validation error: {e}")
            return False

    def _get_current_price(self) -> float:
        """ดึงราคาปัจจุบัน - ใช้ชื่อเดิม - แก้ไขแล้ว"""
        try:
            tick = mt5.symbol_info_tick(self.symbol)
            if tick:
                mid_price = (tick.bid + tick.ask) / 2
                print(f"📊 Current Price: {mid_price:.5f} (Bid: {tick.bid:.5f}, Ask: {tick.ask:.5f})")
                return mid_price
            
            print(f"❌ Cannot get tick for {self.symbol}")
            return 0.0
            
        except Exception as e:
            print(f"❌ Get current price error: {e}")
            return 0.0

    def _check_daily_limits(self) -> bool:
        """ตรวจสอบขีดจำกัดรายวัน - ใช้ชื่อเดิม"""
        try:
            # ตรวจสอบว่าวันเปลี่ยนหรือไม่
            today = datetime.now().date()
            if today != self.last_reset_date:
                self.daily_order_count = 0
                self.last_reset_date = today
            
            # ตรวจสอบขีดจำกัด
            if self.daily_order_count >= self.max_daily_orders:
                print(f"⚠️ Daily order limit reached: {self.daily_order_count}/{self.max_daily_orders}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Check daily limits error: {e}")
            return True  # Safe default

    def _update_execution_stats(self, success: bool, execution_time: float, slippage: float):
        """อัปเดตสถิติการ execute - ใช้ชื่อเดิม"""
        try:
            stats = self.execution_stats["market_orders"]
            stats["count"] += 1
            
            if success:
                stats["success"] += 1
                # อัปเดต average slippage
                if stats["success"] > 1:
                    stats["avg_slippage"] = (stats["avg_slippage"] * (stats["success"] - 1) + slippage) / stats["success"]
                else:
                    stats["avg_slippage"] = slippage
                
                # อัปเดต average execution time
                stats["avg_execution_time"] = (stats["avg_execution_time"] * (stats["success"] - 1) + execution_time) / stats["success"]
            
            # คำนวณ success rate
            success_rate = stats["success"] / stats["count"]
            
            print(f"📊 Market Order Stats: {success_rate:.1%} ({stats['success']}/{stats['count']})")
            if success:
                print(f"   Avg Slippage: {stats['avg_slippage']:.5f}")
                print(f"   Avg Execution: {stats['avg_execution_time']:.3f}s")
            
        except Exception as e:
            print(f"❌ Update execution stats error: {e}")

    def _update_symbol_info(self):
        """อัปเดตข้อมูล Symbol - ใช้ชื่อเดิม"""
        try:
            symbol_info = mt5.symbol_info(self.symbol)
            if symbol_info:
                self.point_value = symbol_info.point
                self.tick_size = symbol_info.trade_tick_size
                print(f"📊 Symbol info updated: {self.symbol}")
                print(f"   Point: {self.point_value}")
                print(f"   Tick size: {self.tick_size}")
            
        except Exception as e:
            print(f"❌ Update symbol info error: {e}")

    def log(self, message: str):
        """Logging method - ใช้ชื่อเดิม"""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] OrderManager: {message}")
        except Exception as e:
            print(f"Logging error: {e}")

    # ========================================================================================
    # 🎮 LEGACY COMPATIBILITY METHODS - ใช้ชื่อเดิมทั้งหมด
    # ========================================================================================
    
    def place_smart_order(self, order_type: str, volume: float, price: float,
                         reasoning: str = "", confidence: float = 0.5, **kwargs) -> Dict:
        """🎮 Legacy Compatibility Method - ใช้ชื่อเดิม"""
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
        """🎮 Legacy Method - ใช้ชื่อเดิม"""
        try:
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
        """🎮 Legacy Method - ใช้ชื่อเดิม"""
        try:
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

    def get_active_orders(self) -> List[Dict]:
        """Get active orders - ใช้ชื่อเดิม"""
        try:
            if not self.mt5_connector.is_connected:
                return []
            
            positions = mt5.positions_get(symbol=self.symbol)
            if not positions:
                return []
            
            active_orders = []
            for pos in positions:
                active_orders.append({
                    'ticket': pos.ticket,
                    'type': 'BUY' if pos.type == 0 else 'SELL',
                    'volume': pos.volume,
                    'price': pos.price_open,
                    'profit': pos.profit,
                    'time': pos.time
                })
            
            return active_orders
            
        except Exception as e:
            print(f"❌ Get active orders error: {e}")
            return []

    def get_pending_orders(self) -> List[Dict]:
        """ดึงออเดอร์ที่รออยู่ - ใช้ชื่อเดิม"""
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
        """แปลง reasoning text เป็น OrderReason - ใช้ชื่อเดิม"""
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
        """แปลง MT5 order type เป็น string - ใช้ชื่อเดิม"""
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
    # 📊 UTILITY METHODS - ใช้ชื่อเดิมทั้งหมด
    # ========================================================================================
    
    def get_market_order_stats(self) -> Dict:
        """ดึงสถิติ Market Orders - ใช้ชื่อเดิม"""
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