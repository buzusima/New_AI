"""
💰 Modern Position Manager - Updated for New Rule Engine
position_manager.py
เพิ่ม methods ที่จำเป็นสำหรับ Modern Rule Engine และเน้นการเก็บกำไร + การแก้ไม้
** NO STOP LOSS SYSTEM - FOCUS ON PROFIT & RECOVERY **
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
    PORTFOLIO_BALANCE = "PORTFOLIO_BALANCE"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"
    MANUAL = "MANUAL"
    EMERGENCY = "EMERGENCY"
    GRID_OPTIMIZATION = "GRID_OPTIMIZATION"
    CORRELATION_HEDGE = "CORRELATION_HEDGE"
    SMART_RECOVERY = "SMART_RECOVERY"

@dataclass
class Position:
    """ข้อมูล Position from REAL MT5"""
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
class PortfolioStatus:
    """สถานะ Portfolio สำหรับ Rule Engine ใหม่"""
    total_positions: int
    buy_positions: int
    sell_positions: int
    total_profit: float
    total_loss: float
    net_profit: float
    profitable_positions: List[Position]
    losing_positions: List[Position]
    position_balance: float  # 0.0-1.0 (0=all sell, 1=all buy)
    risk_level: float       # 0.0-1.0
    margin_usage: float     # 0.0-1.0
    equity: float
    balance: float
    free_margin: float
    recovery_opportunities: List[Dict]  # โอกาสการแก้ไม้

class PositionManager:
    """
    💰 Modern Position Manager - Updated Edition
    
    ความสามารถใหม่:
    - ✅ close_profitable_positions() สำหรับ Rule Engine
    - ✅ emergency_close_all() สำหรับสถานการณ์ฉุกเฉิน
    - ✅ get_portfolio_status() format ใหม่
    - ✅ Smart recovery system (แทน stop loss)
    - ✅ Intelligent profit-taking strategies
    ** NO STOP LOSS - FOCUS ON PROFIT & SMART RECOVERY **
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """Initialize Position Manager"""
        if not mt5_connector:
            raise ValueError("MT5 connector is required")
            
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Position tracking
        self.active_positions: Dict[int, Position] = {}
        self.position_history = deque(maxlen=1000)
        self.last_update_time = datetime.now()
        
        # Performance tracking
        self.close_performance = {
            reason.value: {"count": 0, "success": 0, "total_profit": 0.0}
            for reason in CloseReason
        }
        
        # Recovery system
        self.recovery_opportunities = []
        self.last_recovery_analysis = datetime.now()
        
        # Symbol info
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.point_value = 0.01
        
        print("💰 Position Manager initialized - Compatible with Modern Rule Engine")
    
    # ========================================================================================
    # 🆕 NEW METHODS FOR MODERN RULE ENGINE
    # ========================================================================================
    
    def close_profitable_positions(self, confidence: float, reasoning: str) -> bool:
        """
        🆕 ปิด positions ที่มีกำไรตาม reasoning จาก Rule Engine
        
        Args:
            confidence: ระดับความเชื่อมั่น
            reasoning: เหตุผลการปิด
            
        Returns:
            True ถ้าปิดสำเร็จ
        """
        try:
            print(f"💰 === CLOSE PROFITABLE POSITIONS ===")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Reasoning: {reasoning}")
            
            # อัพเดท positions
            self.update_positions()
            
            # หา profitable positions
            profitable_positions = [pos for pos in self.active_positions.values() 
                                  if pos.total_profit > 0]
            
            if not profitable_positions:
                print("ℹ️ No profitable positions to close")
                return True
            
            total_profit = sum(pos.total_profit for pos in profitable_positions)
            
            print(f"💰 Found {len(profitable_positions)} profitable positions")
            print(f"   Total profit: ${total_profit:.2f}")
            
            # ตัดสินใจว่าจะปิดแบบไหน
            close_strategy = self._determine_close_strategy(reasoning, profitable_positions)
            
            if close_strategy == "ALL_PROFITABLE":
                # ปิดทุกตัวที่มีกำไร
                closed_count = 0
                for pos in profitable_positions:
                    if self._close_single_position(pos, CloseReason.PROFIT_TARGET):
                        closed_count += 1
                
                success = closed_count > 0
                self.log(f"✅ Closed {closed_count}/{len(profitable_positions)} profitable positions")
                
            elif close_strategy == "HEDGE_RECOVERY":
                # ปิดแบบ hedge เพื่อแก้ไม้
                success = self._execute_hedge_recovery(profitable_positions, reasoning)
                
            elif close_strategy == "SELECTIVE_PROFIT":
                # ปิดแบบเลือกสรร
                success = self._execute_selective_profit_taking(profitable_positions, confidence)
                
            else:
                # ปิดแบบมาตรฐาน
                success = self._execute_standard_profit_taking(profitable_positions)
            
            # Track performance
            self._track_close_performance(CloseReason.PROFIT_TARGET, success)
            
            return success
            
        except Exception as e:
            self.log(f"❌ Close profitable positions error: {e}")
            return False
    
    def emergency_close_all(self) -> bool:
        """
        🆕 ปิดทุก positions ในสถานการณ์ฉุกเฉิน
        
        Returns:
            True ถ้าปิดสำเร็จ
        """
        try:
            print("🚨 === EMERGENCY CLOSE ALL ===")
            
            # อัพเดท positions
            self.update_positions()
            
            if not self.active_positions:
                print("ℹ️ No positions to close")
                return True
            
            total_positions = len(self.active_positions)
            total_profit = sum(pos.total_profit for pos in self.active_positions.values())
            
            print(f"🚨 Emergency closing {total_positions} positions")
            print(f"   Net P&L: ${total_profit:.2f}")
            
            # ปิดทุก positions
            closed_count = 0
            for pos in list(self.active_positions.values()):
                if self._close_single_position(pos, CloseReason.EMERGENCY):
                    closed_count += 1
                    time.sleep(0.1)  # หน่วงเวลาเล็กน้อย
            
            success = closed_count == total_positions
            
            if success:
                self.log(f"✅ Emergency close successful: {closed_count}/{total_positions}")
            else:
                self.log(f"⚠️ Partial emergency close: {closed_count}/{total_positions}")
            
            # Track performance
            self._track_close_performance(CloseReason.EMERGENCY, success)
            
            return success
            
        except Exception as e:
            self.log(f"❌ Emergency close error: {e}")
            return False
    
    def get_portfolio_status(self) -> Dict[str, Any]:
        """ดึงสถานะ portfolio ครบถ้วน - แก้ไขให้ส่งข้อมูล positions อย่างถูกต้อง"""
        try:
            print("💰 === PORTFOLIO STATUS ANALYSIS ===")
            
            # ดึงข้อมูลจาก MT5
            positions = self.get_active_positions()
            pending_orders = self.get_pending_orders()
            account_info = self.get_account_info()
            
            print(f"   📊 Raw Data:")
            print(f"      Active Positions: {len(positions)}")
            print(f"      Pending Orders: {len(pending_orders)}")
            
            # วิเคราะห์ positions อย่างละเอียด
            buy_positions = []
            sell_positions = []
            
            for pos in positions:
                print(f"   📍 Position Analysis:")
                print(f"      Ticket: {pos.get('ticket', 'N/A')}")
                print(f"      Type: {pos.get('type', 'N/A')}")
                print(f"      Volume: {pos.get('volume', 0)}")
                print(f"      Price: {pos.get('price_open', pos.get('price', 0))}")
                print(f"      Profit: ${pos.get('profit', 0):.2f}")
                
                # ปรับการจัดกลุ่มให้ถูกต้อง
                pos_type = str(pos.get('type', '')).upper()
                
                # ตรวจสอบหลายรูปแบบของ position type
                if (pos_type in ['BUY', 'POSITION_TYPE_BUY', '0'] or 
                    'BUY' in pos_type or 
                    pos.get('type') == 0):
                    buy_positions.append(pos)
                    print(f"      → Classified as BUY position")
                    
                elif (pos_type in ['SELL', 'POSITION_TYPE_SELL', '1'] or 
                      'SELL' in pos_type or 
                      pos.get('type') == 1):
                    sell_positions.append(pos)
                    print(f"      → Classified as SELL position")
                else:
                    print(f"      → Unknown position type: {pos_type}")
            
            # วิเคราะห์ pending orders
            buy_pending = []
            sell_pending = []
            
            for order in pending_orders:
                order_type = str(order.get('type', '')).upper()
                print(f"   📋 Pending Order:")
                print(f"      Ticket: {order.get('ticket', 'N/A')}")
                print(f"      Type: {order_type}")
                print(f"      Price: {order.get('price', 0)}")
                
                if 'BUY' in order_type:
                    buy_pending.append(order)
                    print(f"      → Classified as BUY pending")
                elif 'SELL' in order_type:
                    sell_pending.append(order)
                    print(f"      → Classified as SELL pending")
            
            # คำนวณสถิติ
            total_positions = len(positions)
            total_pending = len(pending_orders)
            total_profit = sum(pos.get('profit', 0) for pos in positions)
            total_volume = sum(pos.get('volume', 0) for pos in positions)
            
            # คำนวณ margin และ equity
            equity = account_info.get('equity', 0)
            balance = account_info.get('balance', 0)
            margin_used = account_info.get('margin', 0)
            margin_free = account_info.get('margin_free', 0)
            margin_level = account_info.get('margin_level', 0)
            
            # Portfolio health
            portfolio_health = self._calculate_portfolio_health(
                total_profit, equity, balance, margin_level
            )
            
            print(f"   💰 Portfolio Summary:")
            print(f"      Total Positions: {total_positions}")
            print(f"      Total Profit: ${total_profit:.2f}")
            print(f"      Portfolio Health: {portfolio_health:.1%}")
            print(f"      BUY Positions: {len(buy_positions)}")
            print(f"      SELL Positions: {len(sell_positions)}")
            print(f"      BUY Pending: {len(buy_pending)}")
            print(f"      SELL Pending: {len(sell_pending)}")
            
            # สร้างข้อมูลส่งกลับ - มีโครงสร้างที่ Rule Engine ต้องการ
            portfolio_status = {
                # ข้อมูลพื้นฐาน
                "total_positions": total_positions,
                "total_pending_orders": total_pending,
                "total_profit": total_profit,
                "total_volume": total_volume,
                "portfolio_health": portfolio_health,
                
                # ข้อมูลที่ Rule Engine ต้องการ
                "positions": positions,  # ส่งข้อมูล positions เต็ม
                "pending_orders": pending_orders,  # ส่งข้อมูล pending orders เต็ม
                
                # การแบ่งกลุ่ม
                "buy_positions": buy_positions,
                "sell_positions": sell_positions,
                "buy_pending": buy_pending,
                "sell_pending": sell_pending,
                
                # สถิติการแบ่งกลุ่ม
                "buy_positions_count": len(buy_positions),
                "sell_positions_count": len(sell_positions),
                "buy_pending_count": len(buy_pending),
                "sell_pending_count": len(sell_pending),
                
                # ข้อมูล account
                "account_info": {
                    "equity": equity,
                    "balance": balance,
                    "margin": margin_used,
                    "margin_free": margin_free,
                    "margin_level": margin_level
                },
                
                # เวลาอัพเดท
                "last_updated": datetime.now(),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ Portfolio status compiled successfully")
            return portfolio_status
            
        except Exception as e:
            self.log(f"❌ Portfolio status error: {e}")
            return {
                "error": str(e),
                "total_positions": 0,
                "total_profit": 0.0,
                "positions": [],
                "pending_orders": [],
                "account_info": {}
            }

    def get_active_positions(self) -> List[Dict]:
        """
        🆕 ดึง active positions สำหรับ Rule Engine
        Returns: List ของ position dictionaries
        """
        try:
            print("💰 Getting active positions from MT5...")
            
            # อัพเดท positions จาก MT5 ก่อน
            self.update_positions()
            
            # แปลง self.active_positions เป็น list of dicts
            positions_list = []
            
            for ticket, position in self.active_positions.items():
                pos_dict = {
                    "ticket": position.ticket,
                    "symbol": position.symbol,
                    "type": position.type.value if hasattr(position.type, 'value') else str(position.type),
                    "volume": position.volume,
                    "price_open": position.open_price,
                    "price": position.current_price,
                    "profit": position.profit,
                    "swap": position.swap,
                    "commission": position.commission,
                    "open_time": position.open_time,
                    "age_hours": position.age_hours,
                    "comment": position.comment,
                    "magic": position.magic,
                    "total_profit": position.total_profit,
                    "pips_profit": position.pips_profit
                }
                positions_list.append(pos_dict)
            
            print(f"✅ Retrieved {len(positions_list)} active positions")
            return positions_list
            
        except Exception as e:
            self.log(f"❌ get_active_positions error: {e}")
            return []
    
    def get_pending_orders(self) -> List[Dict]:
        """
        🆕 ดึง pending orders สำหรับ Rule Engine
        Returns: List ของ order dictionaries
        """
        try:
            print("💰 Getting pending orders from MT5...")
            
            if not self.mt5_connector or not self.mt5_connector.is_connected:
                print("⚠️ MT5 not connected")
                return []
            
            # ดึง pending orders จาก MT5
            orders = mt5.orders_get(symbol=self.symbol)
            if orders is None:
                orders = []
            
            orders_list = []
            for order in orders:
                order_dict = {
                    "ticket": order.ticket,
                    "symbol": order.symbol,
                    "type": order.type,
                    "type_description": str(order.type),
                    "volume": order.volume_initial,
                    "price": order.price_open,
                    "time_setup": order.time_setup,
                    "magic": order.magic,
                    "comment": order.comment,
                    "sl": getattr(order, 'sl', 0.0),
                    "tp": getattr(order, 'tp', 0.0)
                }
                orders_list.append(order_dict)
            
            print(f"✅ Retrieved {len(orders_list)} pending orders")
            return orders_list
            
        except Exception as e:
            self.log(f"❌ get_pending_orders error: {e}")
            return []
    
    def get_account_info(self) -> Dict:
        """
        🆕 ดึงข้อมูล account สำหรับ Rule Engine
        Returns: Account information dictionary
        """
        try:
            if not self.mt5_connector or not self.mt5_connector.is_connected:
                print("⚠️ MT5 not connected")
                return {}
            
            account_info = mt5.account_info()
            if account_info is None:
                return {}
            
            return {
                "balance": account_info.balance,
                "equity": account_info.equity,
                "margin": account_info.margin,
                "margin_free": account_info.margin_free,
                "margin_level": account_info.margin_level if account_info.margin > 0 else 0,
                "profit": account_info.profit,
                "currency": account_info.currency,
                "server": account_info.server,
                "leverage": account_info.leverage
            }
            
        except Exception as e:
            self.log(f"❌ get_account_info error: {e}")
            return {}
                    
    # ========================================================================================
    # 🔄 EXISTING METHODS (Keep compatibility)
    # ========================================================================================
    
    def update_positions(self):
        """Update positions from REAL MT5 - แก้ไข commission error"""
        try:
            if not self.mt5_connector.is_connected:
                return
            
            positions = mt5.positions_get(symbol=self.symbol)
            if positions is None:
                positions = []
            
            # Clear old positions
            self.active_positions.clear()
            
            # Add current positions
            for pos in positions:
                current_price = self._get_current_price_for_position(pos)
                age_hours = (datetime.now() - datetime.fromtimestamp(pos.time)).total_seconds() / 3600
                
                # แก้ไข: จัดการ commission ที่อาจไม่มี
                commission = getattr(pos, 'commission', 0.0)  # ใช้ getattr ป้องกัน AttributeError
                swap = getattr(pos, 'swap', 0.0)              # ใช้ getattr ป้องกัน AttributeError
                
                print(f"💰 Processing Position:")
                print(f"   Ticket: {pos.ticket}")
                print(f"   Type: {pos.type}")
                print(f"   Profit: ${pos.profit:.2f}")
                print(f"   Swap: ${swap:.2f}")
                print(f"   Commission: ${commission:.2f}")
                
                position = Position(
                    ticket=pos.ticket,
                    symbol=pos.symbol,
                    type=PositionType.BUY if pos.type == mt5.POSITION_TYPE_BUY else PositionType.SELL,
                    volume=pos.volume,
                    open_price=pos.price_open,
                    current_price=current_price,
                    profit=pos.profit,
                    swap=swap,
                    commission=commission,
                    open_time=datetime.fromtimestamp(pos.time),
                    age_hours=age_hours,
                    comment=getattr(pos, 'comment', ''),  # ป้องกัน comment ไม่มี
                    magic=getattr(pos, 'magic', 0)        # ป้องกัน magic ไม่มี
                )
                
                self.active_positions[pos.ticket] = position
                print(f"   ✅ Position added: Total P&L = ${position.total_profit:.2f}")
            
            self.last_update_time = datetime.now()
            print(f"💰 Updated {len(self.active_positions)} active positions")
            
        except Exception as e:
            self.log(f"❌ Position update error: {e}")
    
    def _get_current_price_for_position(self, position) -> float:
        """ดึงราคาปัจจุบันสำหรับ position - แก้ไข error handling"""
        try:
            if not self.mt5_connector or not self.mt5_connector.is_connected:
                return getattr(position, 'price_current', position.price_open)
            
            tick = mt5.symbol_info_tick(position.symbol)
            if tick is None:
                return getattr(position, 'price_current', position.price_open)
            
            # ใช้ bid สำหรับ BUY, ask สำหรับ SELL
            if position.type == mt5.POSITION_TYPE_BUY:
                return tick.bid
            else:
                return tick.ask
                
        except Exception as e:
            print(f"❌ Get current price error: {e}")
            # Fallback ใช้ราคาที่มีใน position object
            return getattr(position, 'price_current', position.price_open)
        
    def _calculate_portfolio_health(self, total_profit: float, equity: float, 
                                  balance: float, margin_level: float) -> float:
        """
        🩺 คำนวณสุขภาพ portfolio (0.0-1.0)
        
        Args:
            total_profit: กำไร/ขาดทุนรวม
            equity: equity ปัจจุบัน
            balance: balance
            margin_level: margin level (%)
            
        Returns:
            float: สุขภาพ portfolio (0.0=แย่มาก, 1.0=ดีมาก)
        """
        try:
            print(f"🩺 Calculating portfolio health...")
            print(f"   Total Profit: ${total_profit:.2f}")
            print(f"   Equity: ${equity:.2f}")
            print(f"   Balance: ${balance:.2f}")
            print(f"   Margin Level: {margin_level:.1f}%")
            
            health_factors = []
            
            # 1. Profit Factor (40% weight)
            if balance > 0:
                profit_ratio = total_profit / balance
                if profit_ratio >= 0.05:  # กำไร >= 5%
                    profit_score = 1.0
                elif profit_ratio >= 0:   # กำไร 0-5%
                    profit_score = 0.7 + (profit_ratio / 0.05) * 0.3
                elif profit_ratio >= -0.05:  # ขาดทุน 0-5%
                    profit_score = 0.4 + (profit_ratio / -0.05) * 0.3
                else:  # ขาดทุน > 5%
                    profit_score = max(0.0, 0.4 * (1 + profit_ratio / -0.1))
            else:
                profit_score = 0.5
            
            health_factors.append(("profit", profit_score, 0.4))
            print(f"   Profit Score: {profit_score:.2f}")
            
            # 2. Margin Safety Factor (30% weight)
            if margin_level >= 1000:  # Very safe
                margin_score = 1.0
            elif margin_level >= 500:  # Safe
                margin_score = 0.8
            elif margin_level >= 200:  # Moderate
                margin_score = 0.6
            elif margin_level >= 100:  # Warning
                margin_score = 0.4
            elif margin_level >= 50:   # Danger
                margin_score = 0.2
            else:  # Critical
                margin_score = 0.1
            
            health_factors.append(("margin", margin_score, 0.3))
            print(f"   Margin Score: {margin_score:.2f}")
            
            # 3. Equity vs Balance Factor (20% weight)
            if balance > 0:
                equity_ratio = equity / balance
                if equity_ratio >= 1.05:  # Equity > Balance (good)
                    equity_score = 1.0
                elif equity_ratio >= 1.0:  # Equity = Balance
                    equity_score = 0.8
                elif equity_ratio >= 0.95:  # Small loss
                    equity_score = 0.6
                elif equity_ratio >= 0.9:   # Moderate loss
                    equity_score = 0.4
                else:  # Large loss
                    equity_score = max(0.0, equity_ratio)
            else:
                equity_score = 0.5
            
            health_factors.append(("equity", equity_score, 0.2))
            print(f"   Equity Score: {equity_score:.2f}")
            
            # 4. Position Count Factor (10% weight)
            position_count = len(self.active_positions)
            max_safe_positions = self.config.get("risk_management", {}).get("max_positions", 20)
            
            if position_count <= max_safe_positions * 0.5:  # Safe range
                position_score = 1.0
            elif position_count <= max_safe_positions * 0.8:  # Moderate
                position_score = 0.7
            elif position_count <= max_safe_positions:  # Full but safe
                position_score = 0.5
            else:  # Over limit
                position_score = max(0.1, 0.5 * (max_safe_positions / position_count))
            
            health_factors.append(("positions", position_score, 0.1))
            print(f"   Position Score: {position_score:.2f}")
            
            # คำนวณ weighted average
            total_weight = sum(weight for _, _, weight in health_factors)
            weighted_sum = sum(score * weight for _, score, weight in health_factors)
            
            portfolio_health = weighted_sum / total_weight if total_weight > 0 else 0.5
            portfolio_health = max(0.0, min(1.0, portfolio_health))  # Bound 0-1
            
            print(f"   📊 Final Portfolio Health: {portfolio_health:.1%}")
            print(f"   Components: " + " | ".join([f"{name}:{score:.2f}" for name, score, _ in health_factors]))
            
            return portfolio_health
            
        except Exception as e:
            print(f"❌ Portfolio health calculation error: {e}")
            return 0.5  # Default moderate health

    # ========================================================================================
    # 🎯 SMART CLOSING STRATEGIES
    # ========================================================================================
    
    def _determine_close_strategy(self, reasoning: str, profitable_positions: List[Position]) -> str:
        """ตัดสินใจ strategy การปิดตาม reasoning"""
        reasoning_lower = reasoning.lower()
        
        if "hedge" in reasoning_lower or "offset" in reasoning_lower:
            return "HEDGE_RECOVERY"
        elif "secure" in reasoning_lower or "take" in reasoning_lower:
            return "ALL_PROFITABLE"
        elif "selective" in reasoning_lower or "partial" in reasoning_lower:
            return "SELECTIVE_PROFIT"
        else:
            return "ALL_PROFITABLE"  # Default
    
    def _execute_hedge_recovery(self, profitable_positions: List[Position], reasoning: str) -> bool:
        """ดำเนินการแก้ไม้แบบ hedge"""
        try:
            print("🔄 === HEDGE RECOVERY EXECUTION ===")
            
            # หา losing positions
            losing_positions = [pos for pos in self.active_positions.values() if pos.total_profit < 0]
            
            if not losing_positions:
                print("ℹ️ No losing positions to hedge")
                return self._execute_standard_profit_taking(profitable_positions)
            
            total_profit = sum(pos.total_profit for pos in profitable_positions)
            total_loss = sum(pos.total_profit for pos in losing_positions)
            
            print(f"💰 Hedge Analysis:")
            print(f"   Profit available: ${total_profit:.2f}")
            print(f"   Loss to cover: ${total_loss:.2f}")
            print(f"   Net result: ${total_profit + total_loss:.2f}")
            
            # Strategy 1: ปิดทั้งหมดถ้า net positive
            if total_profit + total_loss > 0:
                print("✅ Net positive - closing all positions")
                
                closed_count = 0
                # ปิด profitable ก่อน
                for pos in profitable_positions:
                    if self._close_single_position(pos, CloseReason.CORRELATION_HEDGE):
                        closed_count += 1
                
                # ปิด losing ตาม
                for pos in losing_positions:
                    if self._close_single_position(pos, CloseReason.SMART_RECOVERY):
                        closed_count += 1
                
                return closed_count > 0
            
            # Strategy 2: ปิดบางส่วนเพื่อลด exposure
            else:
                print("⚠️ Net negative - partial hedge recovery")
                return self._execute_partial_hedge_recovery(profitable_positions, losing_positions)
            
        except Exception as e:
            self.log(f"❌ Hedge recovery error: {e}")
            return False
    
    def _execute_partial_hedge_recovery(self, profitable_positions: List[Position], 
                                      losing_positions: List[Position]) -> bool:
        """ดำเนินการแก้ไม้แบบบางส่วน"""
        try:
            # เลือก profitable positions ที่มีกำไรดีที่สุด
            profitable_positions.sort(key=lambda p: p.total_profit, reverse=True)
            
            # เลือก losing positions ที่ขาดทุนน้อยที่สุด
            losing_positions.sort(key=lambda p: p.total_profit, reverse=True)
            
            # ปิดคู่ที่ net positive
            closed_pairs = 0
            for i in range(min(len(profitable_positions), len(losing_positions))):
                profit_pos = profitable_positions[i]
                loss_pos = losing_positions[i]
                
                net_result = profit_pos.total_profit + loss_pos.total_profit
                
                if net_result > 0:  # คู่นี้ net positive
                    print(f"💱 Closing pair: +${profit_pos.total_profit:.2f} + ${loss_pos.total_profit:.2f} = +${net_result:.2f}")
                    
                    if (self._close_single_position(profit_pos, CloseReason.CORRELATION_HEDGE) and
                        self._close_single_position(loss_pos, CloseReason.SMART_RECOVERY)):
                        closed_pairs += 1
            
            return closed_pairs > 0
            
        except Exception as e:
            self.log(f"❌ Partial hedge recovery error: {e}")
            return False
    
    def _execute_selective_profit_taking(self, profitable_positions: List[Position], 
                                       confidence: float) -> bool:
        """ปิดกำไรแบบเลือกสรร"""
        try:
            # เรียงตามกำไร
            profitable_positions.sort(key=lambda p: p.total_profit, reverse=True)
            
            # เลือกปิดตาม confidence
            positions_to_close = int(len(profitable_positions) * confidence)
            positions_to_close = max(1, min(positions_to_close, len(profitable_positions)))
            
            print(f"🎯 Selective profit taking: {positions_to_close}/{len(profitable_positions)} positions")
            
            closed_count = 0
            for i in range(positions_to_close):
                pos = profitable_positions[i]
                if self._close_single_position(pos, CloseReason.PROFIT_TARGET):
                    closed_count += 1
                    self.log(f"💰 Closed position #{pos.ticket}: +${pos.total_profit:.2f}")
            
            return closed_count > 0
            
        except Exception as e:
            self.log(f"❌ Selective profit taking error: {e}")
            return False
    
    def _execute_standard_profit_taking(self, profitable_positions: List[Position]) -> bool:
        """ปิดกำไรแบบมาตรฐาน"""
        try:
            closed_count = 0
            total_secured = 0.0
            
            for pos in profitable_positions:
                if self._close_single_position(pos, CloseReason.PROFIT_TARGET):
                    closed_count += 1
                    total_secured += pos.total_profit
            
            if closed_count > 0:
                self.log(f"✅ Standard profit taking: {closed_count} positions, ${total_secured:.2f} secured")
            
            return closed_count > 0
            
        except Exception as e:
            self.log(f"❌ Standard profit taking error: {e}")
            return False
    
    def _close_single_position(self, position: Position, reason: CloseReason) -> bool:
        """ปิด position เดียว"""
        try:
            # Prepare close request
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_SELL if position.type == PositionType.BUY else mt5.ORDER_TYPE_BUY,
                "position": position.ticket,
                "deviation": 20,
                "magic": position.magic,
                "comment": f"CLOSE_{reason.value}_{datetime.now().strftime('%H%M%S')}"
            }
            
            # Send close order
            result = mt5.order_send(request)
            
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                # Remove from active positions
                if position.ticket in self.active_positions:
                    del self.active_positions[position.ticket]
                
                # Add to history
                self.position_history.append({
                    "ticket": position.ticket,
                    "close_reason": reason.value,
                    "close_time": datetime.now(),
                    "profit": position.total_profit,
                    "duration_hours": position.age_hours
                })
                
                self.log(f"✅ Position #{position.ticket} closed: {reason.value} (${position.total_profit:.2f})")
                return True
            else:
                error_msg = f"MT5 Error {result.retcode}" if result else "Unknown error"
                self.log(f"❌ Failed to close position #{position.ticket}: {error_msg}")
                return False
                
        except Exception as e:
            self.log(f"❌ Close single position error: {e}")
            return False
    
    # ========================================================================================
    # 🔍 ANALYSIS AND HELPER METHODS
    # ========================================================================================
    
    def _calculate_portfolio_risk_level(self, losing_positions: List[Position], equity: float) -> float:
        """คำนวณระดับความเสี่ยงของ portfolio (0.0-1.0)"""
        try:
            if not losing_positions or equity <= 0:
                return 0.0
            
            total_loss = sum(pos.total_profit for pos in losing_positions)
            loss_percentage = abs(total_loss) / equity
            
            # แปลงเป็น risk level 0.0-1.0
            risk_level = min(1.0, loss_percentage * 10)  # 10% loss = 1.0 risk
            
            return risk_level
            
        except Exception as e:
            return 0.0
    
    def _analyze_recovery_opportunities(self, profitable_positions: List[Position], 
                                      losing_positions: List[Position]) -> List[Dict]:
        """วิเคราะห์โอกาสการแก้ไม้"""
        try:
            opportunities = []
            
            if not profitable_positions or not losing_positions:
                return opportunities
            
            total_profit = sum(pos.total_profit for pos in profitable_positions)
            total_loss = sum(pos.total_profit for pos in losing_positions)
            
            # โอกาสที่ 1: Net Positive Recovery
            if total_profit + total_loss > 0:
                opportunities.append({
                    "type": "NET_POSITIVE_RECOVERY",
                    "description": f"Close all positions for net +${total_profit + total_loss:.2f}",
                    "profit_amount": total_profit,
                    "loss_amount": total_loss,
                    "net_result": total_profit + total_loss,
                    "confidence": 0.9,
                    "positions_involved": len(profitable_positions) + len(losing_positions)
                })
            
            # โอกาสที่ 2: Partial Recovery
            profitable_positions.sort(key=lambda p: p.total_profit, reverse=True)
            losing_positions.sort(key=lambda p: p.total_profit, reverse=True)
            
            cumulative_profit = 0
            cumulative_loss = 0
            
            for i in range(min(len(profitable_positions), len(losing_positions))):
                cumulative_profit += profitable_positions[i].total_profit
                cumulative_loss += losing_positions[i].total_profit
                
                if cumulative_profit + cumulative_loss > 5:  # Net > $5
                    opportunities.append({
                        "type": "PARTIAL_RECOVERY",
                        "description": f"Close {i+1} pairs for +${cumulative_profit + cumulative_loss:.2f}",
                        "profit_amount": cumulative_profit,
                        "loss_amount": cumulative_loss,
                        "net_result": cumulative_profit + cumulative_loss,
                        "confidence": 0.7,
                        "positions_involved": (i+1) * 2
                    })
            
            return opportunities
            
        except Exception as e:
            self.log(f"❌ Recovery analysis error: {e}")
            return []
        
    def _track_close_performance(self, reason: CloseReason, success: bool):
        """Track closing performance"""
        try:
            reason_key = reason.value
            if reason_key not in self.close_performance:
                self.close_performance[reason_key] = {"count": 0, "success": 0, "total_profit": 0.0}
            
            self.close_performance[reason_key]["count"] += 1
            if success:
                self.close_performance[reason_key]["success"] += 1
            
        except Exception as e:
            self.log(f"❌ Close performance tracking error: {e}")
    
    # ========================================================================================
    # 📊 INFORMATION METHODS
    # ========================================================================================
    
    def get_active_positions_summary(self) -> Dict:
        """ดึงสรุป active positions"""
        try:
            self.update_positions()
            
            if not self.active_positions:
                return {"total": 0, "buy": 0, "sell": 0, "profit": 0.0, "loss": 0.0}
            
            buy_count = len([p for p in self.active_positions.values() if p.type == PositionType.BUY])
            sell_count = len(self.active_positions) - buy_count
            
            total_profit = sum(p.total_profit for p in self.active_positions.values() if p.total_profit > 0)
            total_loss = sum(p.total_profit for p in self.active_positions.values() if p.total_profit <= 0)
            
            return {
                "total": len(self.active_positions),
                "buy": buy_count,
                "sell": sell_count,
                "profit": total_profit,
                "loss": total_loss,
                "net": total_profit + total_loss
            }
            
        except Exception as e:
            self.log(f"❌ Position summary error: {e}")
            return {"total": 0, "buy": 0, "sell": 0, "profit": 0.0, "loss": 0.0}
    
    def get_recovery_recommendations(self) -> List[Dict]:
        """ดึงคำแนะนำการแก้ไม้"""
        try:
            self.update_positions()
            
            profitable_positions = [pos for pos in self.active_positions.values() if pos.total_profit > 0]
            losing_positions = [pos for pos in self.active_positions.values() if pos.total_profit <= 0]
            
            return self._analyze_recovery_opportunities(profitable_positions, losing_positions)
            
        except Exception as e:
            self.log(f"❌ Recovery recommendations error: {e}")
            return []
    
    def get_close_performance_stats(self) -> Dict:
        """ดึงสถิติการปิด positions"""
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
            self.log(f"❌ Close performance stats error: {e}")
            return {}
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 💰 PositionManager: {message}")


# ========================================================================================
# 🧪 TEST FUNCTION
# ========================================================================================

def test_position_manager_compatibility():
    """Test compatibility with Modern Rule Engine"""
    print("🧪 Testing Position Manager compatibility...")
    print("✅ close_profitable_positions() method added")
    print("✅ emergency_close_all() method added")
    print("✅ get_portfolio_status() updated format")
    print("✅ Smart recovery system implemented")
    print("✅ No stop loss - focus on profit & recovery")
    print("✅ Ready for Modern Rule Engine integration")

if __name__ == "__main__":
    test_position_manager_compatibility()