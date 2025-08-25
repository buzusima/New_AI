"""
🧠 Modern Rule Engine - Complete Flexible System
rule_engine.py
สำหรับ Modern AI Gold Grid Trading System - ระบบ Rule-based ที่ยืดหยุ่นและเป็นระบบ
รองรับ Dynamic Spacing, Adaptive Grid Size, และ Smart Resource Management
** PRODUCTION READY - NO MOCK DATA **
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum, auto
import json
import numpy as np
from collections import deque, defaultdict
import statistics
import math

# ========================================================================================
# 🎯 ENUMS และ DATA CLASSES
# ========================================================================================

class TradingDecision(Enum):
    """ประเภทการตัดสินใจเทรด"""
    BUY = "BUY"
    SELL = "SELL"
    CLOSE_PROFITABLE = "CLOSE_PROFITABLE"
    CLOSE_LOSING = "CLOSE_LOSING"
    CLOSE_ALL = "CLOSE_ALL"
    HOLD = "HOLD"
    EMERGENCY_STOP = "EMERGENCY_STOP"

class TradingMode(Enum):
    """โหมดการเทรด"""
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE" 
    AGGRESSIVE = "AGGRESSIVE"
    ADAPTIVE = "ADAPTIVE"
    EMERGENCY = "EMERGENCY"

class GridPhase(Enum):
    """เฟสของการจัดการกริด - 4 Phase System"""
    INITIALIZATION = "INITIALIZATION"    # Phase 1: เริ่มต้นระบบ
    MONITORING = "MONITORING"            # Phase 2: ตรวจสอบความสมดุล
    REBALANCING = "REBALANCING"          # Phase 3: ปรับสมดุลอัจฉริยะ
    MAINTENANCE = "MAINTENANCE"          # Phase 4: บำรุงรักษากริด

class MarketSession(Enum):
    """เซสชันตลาด"""
    ASIAN = "ASIAN"
    LONDON = "LONDON"
    NEW_YORK = "NEW_YORK"
    OVERLAP = "OVERLAP"
    QUIET = "QUIET"

class RiskLevel(Enum):
    """ระดับความเสี่ยง"""
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class RuleResult:
    """ผลลัพธ์จาก Rule"""
    rule_name: str
    decision: TradingDecision
    confidence: float  # 0.0 - 1.0
    reasoning: str
    supporting_data: Dict = field(default_factory=dict)
    weight: float = 1.0
    execution_priority: int = 1  # 1=highest, 5=lowest
    market_context: Dict = field(default_factory=dict)
    risk_assessment: Dict = field(default_factory=dict)
    
    @property
    def weighted_confidence(self) -> float:
        """ความเชื่อมั่นถ่วงน้ำหนัก"""
        return self.confidence * self.weight

@dataclass
class GridState:
    """สถานะของ Grid ปัจจุบัน"""
    current_phase: GridPhase
    buy_levels: List[float] = field(default_factory=list)
    sell_levels: List[float] = field(default_factory=list)
    missing_buy_slots: List[float] = field(default_factory=list)
    missing_sell_slots: List[float] = field(default_factory=list)
    grid_balance_ratio: float = 0.5  # 0.0=all sell, 1.0=all buy
    grid_completeness: float = 0.0   # 0.0-1.0
    last_grid_action: datetime = field(default_factory=datetime.now)
    quality_score: float = 0.0       # คุณภาพของกริดปัจจุบัน
    spacing_efficiency: float = 0.0  # ประสิทธิภาพของ spacing
    
    @property
    def total_orders(self) -> int:
        """จำนวนออเดอร์รวม"""
        return len(self.buy_levels) + len(self.sell_levels)
    
    @property
    def is_balanced(self) -> bool:
        """เช็คว่ากริดสมดุลหรือไม่"""
        return 0.3 <= self.grid_balance_ratio <= 0.7

@dataclass
class CapitalAllocation:
    """การจัดสรรเงินทุน"""
    total_balance: float
    available_margin: float
    used_margin: float
    free_margin: float
    max_grid_allocation: float  # % ของเงินทุนที่ใช้กับกริด
    optimal_grid_size: int     # จำนวนออเดอร์ที่เหมาะสม
    risk_budget: float         # งบความเสี่ยงที่เหลือ
    
    @property
    def margin_usage_ratio(self) -> float:
        """อัตราการใช้ margin"""
        return self.used_margin / self.available_margin if self.available_margin > 0 else 0
    
    @property
    def can_expand_grid(self) -> bool:
        """เช็คว่าสามารถขยายกริดได้หรือไม่"""
        return self.margin_usage_ratio < 0.7 and self.risk_budget > 0

@dataclass
class MarketContext:
    """บริบทตลาดปัจจุบัน"""
    session: MarketSession
    volatility_level: str  # VERY_LOW, LOW, MEDIUM, HIGH, VERY_HIGH
    trend_direction: str   # UP, DOWN, SIDEWAYS
    trend_strength: float  # 0.0-1.0
    liquidity_level: str   # HIGH, MEDIUM, LOW
    spread_condition: str  # NORMAL, WIDE, VERY_WIDE
    momentum: float        # -1.0 to 1.0
    
    @property
    def is_favorable_for_grid(self) -> bool:
        """เช็คว่าสภาพตลาดเหมาะกับกริดหรือไม่"""
        return (self.volatility_level in ["LOW", "MEDIUM"] and 
                self.liquidity_level in ["HIGH", "MEDIUM"] and
                self.spread_condition == "NORMAL")

# ========================================================================================
# 🧠 MODERN RULE ENGINE CLASS
# ========================================================================================

class ModernRuleEngine:
    """
    🧠 Modern Rule Engine - Flexible & Adaptive Edition
    
    ความสามารถใหม่:
    - 4-Phase Grid Management System
    - Dynamic Spacing ตาม Volatility  
    - Adaptive Grid Size ตามเงินทุน
    - Smart Resource Allocation
    - Context-Aware Decision Making
    - Flexible Balance Management
    - Quality-Driven Grid Building
    ** NO STOP LOSS - FOCUS ON PROFIT & RECOVERY **
    """
    
    def __init__(self, config: Dict, market_analyzer, order_manager, 
                 position_manager, performance_tracker):
        # Core components - REAL connections only
        self.rules_config = config
        self.market_analyzer = market_analyzer
        self.order_manager = order_manager
        self.position_manager = position_manager
        self.performance_tracker = performance_tracker
        
        # Grid state management
        self.grid_state = GridState(current_phase=GridPhase.INITIALIZATION)
        self.capital_allocation = None
        self.market_context = None
        
        # Engine state
        self.is_running = False
        self.current_mode = TradingMode.MODERATE
        self.engine_thread = None
        
        # Data tracking
        self.last_market_data = {}
        self.last_portfolio_data = {}
        self.recent_decisions = deque(maxlen=100)
        self.decision_history = []
        
        # Performance tracking
        self.rule_performances = defaultdict(lambda: {
            "success_count": 0,
            "total_count": 0,
            "avg_confidence": 0.0,
            "last_updated": datetime.now()
        })
        
        # Grid management
        self.last_grid_analysis_time = datetime.now()
        self.grid_analysis_interval = 30  # วินาที
        self.spacing_history = deque(maxlen=50)
        
        print("🧠 Modern Rule Engine initialized with Flexible Grid System")
    
    # ========================================================================================
    # 🎮 ENGINE CONTROL METHODS
    # ========================================================================================
    
    def start(self):
        """เริ่มต้น Rule Engine"""
        if self.is_running:
            print("⚠️ Rule engine already running")
            return
            
        self.is_running = True
        self.engine_thread = threading.Thread(target=self._engine_loop, daemon=True)
        self.engine_thread.start()
        print("🚀 Flexible Rule Engine started")
    
    def stop(self):
        """หยุด Rule Engine"""
        self.is_running = False
        if self.engine_thread:
            self.engine_thread.join(timeout=5)
        print("🛑 Rule engine stopped")
    
    def set_trading_mode(self, mode: TradingMode):
        """ตั้งค่าโหมดการเทรด"""
        self.current_mode = mode
        print(f"🎯 Trading mode set to: {mode.value}")
    
    # ========================================================================================
    # 🔄 MAIN ENGINE LOOP  
    # ========================================================================================
    
    def _engine_loop(self):
        """Main engine loop - ลูปหลักที่ทำงานอย่างต่อเนื่อง"""
        while self.is_running:
            try:
                # อัพเดทข้อมูลตลาดและ portfolio
                self._update_market_and_portfolio_data()
                
                # วิเคราะห์บริบทตลาดปัจจุบัน  
                self._analyze_market_context()
                
                # คำนวณการจัดสรรเงินทุน
                self._calculate_capital_allocation()
                
                # ตัดสินใจตาม Rule-based system
                decision_result = self._execute_rule_based_decision()
                
                if decision_result:
                    # ดำเนินการตามการตัดสินใจ
                    self._execute_trading_decision(decision_result)
                    
                    # บันทึกการตัดสินใจ
                    self.decision_history.append(decision_result)
                    self.recent_decisions.append(decision_result)
                
                # อัพเดทประสิทธิภาพของ rules
                self._update_rule_performances()
                
                # Adaptive learning (เรียนรู้และปรับปรุง)
                if self.current_mode == TradingMode.ADAPTIVE:
                    self._adaptive_learning_update()
                
                # หยุดพักระหว่างรอบ
                time.sleep(5)  # 5 วินาทีต่อรอบ
                
            except Exception as e:
                print(f"❌ Rule engine error: {e}")
                time.sleep(10)  # พักนานขึ้นเมื่อเกิดข้อผิดพลาด
    
    def _update_market_and_portfolio_data(self):
        """อัพเดทข้อมูลตลาดและ portfolio"""
        try:
            # ดึงข้อมูลตลาดแบบครบถ้วน
            self.last_market_data = self.market_analyzer.get_comprehensive_analysis()
            
            # ดึงสถานะ portfolio
            self.last_portfolio_data = self.position_manager.get_portfolio_status()
            
        except Exception as e:
            print(f"❌ Data update error: {e}")
    
    def _analyze_market_context(self):
        """วิเคราะห์บริบทตลาดปัจจุบัน"""
        try:
            market_data = self.last_market_data
            
            # ระบุ market session
            current_hour = datetime.now().hour
            if 1 <= current_hour <= 7:
                session = MarketSession.ASIAN
            elif 8 <= current_hour <= 12:
                session = MarketSession.LONDON
            elif 13 <= current_hour <= 17:
                session = MarketSession.OVERLAP
            elif 18 <= current_hour <= 22:
                session = MarketSession.NEW_YORK
            else:
                session = MarketSession.QUIET
            
            # สร้าง market context
            self.market_context = MarketContext(
                session=session,
                volatility_level=market_data.get("volatility_level", "MEDIUM"),
                trend_direction=market_data.get("trend_direction", "SIDEWAYS"),
                trend_strength=market_data.get("trend_strength", 0.5),
                liquidity_level=market_data.get("liquidity_level", "MEDIUM"),
                spread_condition=market_data.get("spread_condition", "NORMAL"),
                momentum=market_data.get("momentum", 0.0)
            )
            
        except Exception as e:
            print(f"❌ Market context analysis error: {e}")
    
    def _calculate_capital_allocation(self):
        """คำนวณการจัดสรรเงินทุนอย่างยืดหยุ่น"""
        try:
            portfolio_data = self.last_portfolio_data
            
            # ข้อมูลเงินทุน
            balance = portfolio_data.get("balance", 10000)
            equity = portfolio_data.get("equity", balance)
            margin = portfolio_data.get("margin", 0)
            free_margin = portfolio_data.get("free_margin", balance)
            
            # คำนวณ optimal grid size ตามเงินทุน
            if balance < 1000:
                optimal_size = max(2, int(balance / 200))  # เงินน้อย กริดน้อย
                max_allocation = 0.3  # ใช้แค่ 30%
            elif balance < 5000:
                optimal_size = max(4, int(balance / 400))  # เงินปานกลาง
                max_allocation = 0.5  # ใช้ 50%
            elif balance < 20000:
                optimal_size = max(6, int(balance / 800))  # เงินพอใช้
                max_allocation = 0.6  # ใช้ 60%
            else:
                optimal_size = max(8, min(15, int(balance / 1500)))  # เงินเยอะ แต่ไม่ให้เกิน 15
                max_allocation = 0.7  # ใช้ 70%
            
            # ปรับตาม market condition
            if self.market_context and self.market_context.volatility_level == "HIGH":
                optimal_size = max(3, int(optimal_size * 0.7))  # ลดกริดเมื่อ volatile
                max_allocation *= 0.8
            elif self.market_context and self.market_context.volatility_level == "VERY_LOW":
                optimal_size = min(20, int(optimal_size * 1.3))  # เพิ่มกริดเมื่อตลาดเงียบ
            
            # สร้าง capital allocation
            self.capital_allocation = CapitalAllocation(
                total_balance=balance,
                available_margin=free_margin,
                used_margin=margin,
                free_margin=free_margin,
                max_grid_allocation=max_allocation,
                optimal_grid_size=optimal_size,
                risk_budget=free_margin * 0.1  # 10% ของ free margin
            )
            
        except Exception as e:
            print(f"❌ Capital allocation error: {e}")
    
    # ========================================================================================
    # 🎯 MAIN DECISION MAKING SYSTEM
    # ========================================================================================
    
    def _execute_rule_based_decision(self) -> Optional[RuleResult]:
        """
        ระบบการตัดสินใจตาม Rules - หัวใจของระบบ
        
        Returns:
            RuleResult ถ้าต้องการดำเนินการ, None ถ้าไม่ต้องทำอะไร
        """
        try:
            # เก็บผลลัพธ์จากทุก rules
            rule_results = []
            
            # ดำเนินการแต่ละ rule
            for rule_name, rule_config in self.rules_config.get("rules", {}).items():
                if not rule_config.get("enabled", True):
                    continue
                
                rule_result = self._execute_individual_rule(rule_name, rule_config)
                if rule_result:
                    rule_results.append(rule_result)
            
            if not rule_results:
                return None
            
            # ตัดสินใจขั้นสุดท้ายด้วยระบบถ่วงน้ำหนัก
            final_decision = self._make_weighted_decision(rule_results)
            
            return final_decision
            
        except Exception as e:
            print(f"❌ Rule execution error: {e}")
            return None
    
    def _execute_individual_rule(self, rule_name: str, rule_config: Dict) -> Optional[RuleResult]:
        """
        ดำเนินการ rule แต่ละตัว
        
        Args:
            rule_name: ชื่อ rule
            rule_config: การตั้งค่า rule
            
        Returns:
            RuleResult ถ้า rule trigger, None ถ้าไม่
        """
        try:
            confidence_threshold = rule_config.get("confidence_threshold", 0.6)
            weight = rule_config.get("weight", 1.0)
            
            # ดำเนินการ rule logic เฉพาะ
            if rule_name == "grid_expansion":
                return self._rule_grid_expansion(rule_config, weight)
            elif rule_name == "portfolio_balance":
                return self._rule_portfolio_balance(rule_config, weight)
            elif rule_name == "trend_following":
                return self._rule_trend_following(rule_config, weight)
            elif rule_name == "mean_reversion":
                return self._rule_mean_reversion(rule_config, weight)
            elif rule_name == "support_resistance":
                return self._rule_support_resistance(rule_config, weight)
            elif rule_name == "volatility_breakout":
                return self._rule_volatility_breakout(rule_config, weight)
            else:
                print(f"❌ Unknown rule: {rule_name}")
                return None
                
        except Exception as e:
            print(f"❌ Rule {rule_name} execution error: {e}")
            return None
    
    # ========================================================================================
    # 🏗️ MODERN GRID EXPANSION RULE - 4 PHASE SYSTEM
    # ========================================================================================
    
    def _rule_grid_expansion(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """
        🏗️ Modern Grid Expansion - 4 Phase Flexible System
        
        Phase 1: Initialization (เริ่มต้นระบบ)
        Phase 2: Monitoring (ตรวจสอบความสมดุล)  
        Phase 3: Rebalancing (ปรับสมดุลอัจฉริยะ)
        Phase 4: Maintenance (บำรุงรักษากริด)
        """
        try:
            print("🔍 === MODERN GRID EXPANSION ANALYSIS ===")
            
            # ตรวจสอบข้อมูลพื้นฐาน
            current_price = self.last_market_data.get("current_price", 0)
            if current_price == 0:
                print("❌ No current price available")
                return None
            
            # ตรวจสอบเงินทุน
            if not self.capital_allocation or not self.capital_allocation.can_expand_grid:
                print("💰 Insufficient capital for grid expansion")
                return None
            
            # คำนวณ dynamic parameters
            dynamic_params = self._calculate_dynamic_grid_parameters()
            
            # วิเคราะห์สถานะกริดปัจจุบัน
            grid_analysis = self._analyze_current_grid_state(current_price, dynamic_params)
            
            # อัพเดท grid state
            self._update_grid_state(grid_analysis, dynamic_params)
            
            # ตัดสินใจตาม Phase ปัจจุบัน
            decision = self._execute_grid_phase_logic(grid_analysis, dynamic_params, weight)
            
            return decision
            
        except Exception as e:
            print(f"❌ Grid expansion error: {e}")
            return None
    
    def _calculate_dynamic_grid_parameters(self) -> Dict:
        """คำนวณพารามิเตอร์กริดแบบ Dynamic - ยืดหยุ่นตามสภาพตลาด"""
        try:
            market_data = self.last_market_data
            
            # Base parameters
            base_spacing = 100  # points
            base_grid_size = 5  # ออเดอร์ต่อฝั่ง
            
            # === DYNAMIC SPACING ตาม VOLATILITY ===
            volatility_factor = market_data.get("volatility_factor", 1.0)
            
            if volatility_factor < 0.5:  # ตลาดเงียบมาก
                spacing_multiplier = 0.7  # กริดหนาขึ้น
                risk_multiplier = 1.2     # เสี่ยงได้มากขึ้น
            elif volatility_factor < 0.8:  # ตลาดเงียบ
                spacing_multiplier = 0.85
                risk_multiplier = 1.1
            elif volatility_factor > 2.0:  # ตลาดผันผวนมาก
                spacing_multiplier = 1.8  # กริดเบาลง
                risk_multiplier = 0.6     # ลดความเสี่ยง
            elif volatility_factor > 1.5:  # ตลาดผันผวน
                spacing_multiplier = 1.4
                risk_multiplier = 0.8
            else:  # ตลาดปกติ
                spacing_multiplier = 1.0
                risk_multiplier = 1.0
            
            # === ADAPTIVE GRID SIZE ตามเงินทุน ===
            optimal_size = self.capital_allocation.optimal_grid_size
            
            # ปรับตาม market session
            if self.market_context:
                if self.market_context.session == MarketSession.OVERLAP:
                    optimal_size = min(optimal_size + 2, 15)  # เพิ่มในช่วงคึกคัก
                elif self.market_context.session == MarketSession.QUIET:
                    optimal_size = max(optimal_size - 2, 3)   # ลดในช่วงเงียบ
            
            # คำนวณ spacing สุดท้าย
            dynamic_spacing = int(base_spacing * spacing_multiplier)
            dynamic_spacing = max(50, min(300, dynamic_spacing))  # จำกัดไว้ 50-300 points
            
            # คำนวณระยะห่างขั้นต่ำ
            min_distance = max(30, int(dynamic_spacing * 0.4))
            
            # เก็บประวัติ spacing
            self.spacing_history.append(dynamic_spacing)
            
            params = {
                "dynamic_spacing": dynamic_spacing,
                "optimal_grid_size": optimal_size,
                "min_distance_points": min_distance,
                "spacing_multiplier": spacing_multiplier,
                "risk_multiplier": risk_multiplier,
                "volatility_factor": volatility_factor,
                "point_value": getattr(self.order_manager, 'point_value', 0.01)
            }
            
            print(f"📊 Dynamic Grid Parameters:")
            print(f"   Volatility Factor: {volatility_factor:.2f}")
            print(f"   Dynamic Spacing: {dynamic_spacing} points (base: {base_spacing})")
            print(f"   Optimal Grid Size: {optimal_size} orders per side")
            print(f"   Min Distance: {min_distance} points")
            print(f"   Market Session: {self.market_context.session.value if self.market_context else 'UNKNOWN'}")
            
            return params
            
        except Exception as e:
            print(f"❌ Dynamic parameters calculation error: {e}")
            return {
                "dynamic_spacing": 100,
                "optimal_grid_size": 5,
                "min_distance_points": 50,
                "spacing_multiplier": 1.0,
                "risk_multiplier": 1.0,
                "volatility_factor": 1.0,
                "point_value": 0.01
            }
    
    def _analyze_current_grid_state(self, current_price: float, params: Dict) -> Dict:
        """วิเคราะห์สถานะกริดปัจจุบันอย่างละเอียด"""
        try:
            print("🗺️ === GRID STATE ANALYSIS ===")
            
            # ดึงข้อมูลจริงจาก MT5
            positions = []
            pending_orders = []
            
            if self.position_manager:
                self.position_manager.update_positions()
                positions = list(self.position_manager.active_positions.values())
            
            if self.order_manager:
                pending_orders = self.order_manager.get_pending_orders()
            
            # === สร้าง Grid Map ===
            buy_levels = []
            sell_levels = []
            
            # จาก positions (ออเดอร์ที่ fill แล้ว)
            for pos in positions:
                price = round(pos.open_price, 2)
                if pos.type.value == "BUY":
                    buy_levels.append(price)
                elif pos.type.value == "SELL":
                    sell_levels.append(price)
            
            # จาก pending orders (ออเดอร์ที่รออยู่)
            for order in pending_orders:
                order_type = order.get("type", "")
                price = round(order.get("price", 0), 2)
                if price > 0:
                    if "BUY" in order_type:
                        buy_levels.append(price)
                    elif "SELL" in order_type:
                        sell_levels.append(price)
            
            # เรียงลำดับ
            buy_levels = sorted(set(buy_levels), reverse=True)  # สูงไปต่ำ
            sell_levels = sorted(set(sell_levels))             # ต่ำไปสูง
            
            # === คำนวณ Grid Template ที่เหมาะสม ===
            spacing_value = params["dynamic_spacing"] * params["point_value"]
            optimal_size = params["optimal_grid_size"]
            
            # สร้าง expected levels
            expected_buy_levels = []
            expected_sell_levels = []
            
            for i in range(1, optimal_size + 1):
                buy_price = round(current_price - (spacing_value * i), 2)
                sell_price = round(current_price + (spacing_value * i), 2)
                
                expected_buy_levels.append(buy_price)
                expected_sell_levels.append(sell_price)
            
            # === หา Missing Slots ===
            missing_buy_slots = [p for p in expected_buy_levels if p not in buy_levels]
            missing_sell_slots = [p for p in expected_sell_levels if p not in sell_levels]
            
            # เลือก slot ถัดไปที่ดีที่สุด
            next_buy_slot = self._select_best_grid_slot(missing_buy_slots, current_price, "BUY")
            next_sell_slot = self._select_best_grid_slot(missing_sell_slots, current_price, "SELL")
            
            # === คำนวณ Grid Quality ===
            grid_quality = self._calculate_grid_quality(buy_levels, sell_levels, 
                                                       expected_buy_levels, expected_sell_levels)
            
            # === Grid Balance Analysis ===
            total_orders = len(buy_levels) + len(sell_levels)
            buy_ratio = len(buy_levels) / total_orders if total_orders > 0 else 0.5
            
            analysis = {
                "current_price": current_price,
                "buy_levels": buy_levels,
                "sell_levels": sell_levels,
                "buy_orders": len(buy_levels),
                "sell_orders": len(sell_levels),
                "total_orders": total_orders,
                "buy_ratio": buy_ratio,
                "expected_buy_levels": expected_buy_levels,
                "expected_sell_levels": expected_sell_levels,
                "missing_buy_slots": missing_buy_slots,
                "missing_sell_slots": missing_sell_slots,
                "next_buy_slot": next_buy_slot,
                "next_sell_slot": next_sell_slot,
                "grid_completeness": len(buy_levels + sell_levels) / (optimal_size * 2),
                "grid_quality_score": grid_quality,
                "spacing_efficiency": self._calculate_spacing_efficiency(buy_levels, sell_levels, spacing_value),
                "optimal_grid_size": optimal_size
            }
            
            print(f"📊 Grid State:")
            print(f"   Current Price: {current_price:.2f}")
            print(f"   BUY: {len(buy_levels)}/{optimal_size} | SELL: {len(sell_levels)}/{optimal_size}")
            print(f"   Balance Ratio: {buy_ratio:.1%} (BUY)")
            print(f"   Completeness: {analysis['grid_completeness']:.1%}")
            print(f"   Quality Score: {grid_quality:.2f}/1.0")
            print(f"   Next BUY Slot: {next_buy_slot:.2f}" if next_buy_slot else "   Next BUY Slot: None")
            print(f"   Next SELL Slot: {next_sell_slot:.2f}" if next_sell_slot else "   Next SELL Slot: None")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Grid state analysis error: {e}")
            return {}
    
    def _select_best_grid_slot(self, available_slots: List[float], current_price: float, direction: str) -> Optional[float]:
        """เลือก grid slot ที่ดีที่สุด"""
        if not available_slots:
            return None
        
        # เรียงตามระยะห่างจาก current price
        if direction == "BUY":
            # เลือก BUY slot ที่ใกล้ current price ที่สุด (ราคาสูงสุด)
            return max(available_slots)
        else:
            # เลือก SELL slot ที่ใกล้ current price ที่สุด (ราคาต่ำสุด)  
            return min(available_slots)
    
    def _calculate_grid_quality(self, buy_levels: List[float], sell_levels: List[float],
                               expected_buy: List[float], expected_sell: List[float]) -> float:
        """คำนวณคุณภาพของกริด (0.0-1.0)"""
        try:
            if not expected_buy and not expected_sell:
                return 0.0
            
            # คำนวณความครบถ้วน
            buy_completeness = len([b for b in expected_buy if b in buy_levels]) / len(expected_buy) if expected_buy else 0
            sell_completeness = len([s for s in expected_sell if s in sell_levels]) / len(expected_sell) if expected_sell else 0
            completeness = (buy_completeness + sell_completeness) / 2
            
            # คำนวณความสม่ำเสมอของ spacing
            spacing_uniformity = self._calculate_spacing_uniformity(buy_levels + sell_levels)
            
            # คำนวณความสมดุล
            total = len(buy_levels) + len(sell_levels)
            balance_score = 1.0 - abs(0.5 - (len(buy_levels) / total)) * 2 if total > 0 else 0.5
            
            # รวมคะแนน
            quality = (completeness * 0.4 + spacing_uniformity * 0.3 + balance_score * 0.3)
            
            return min(1.0, max(0.0, quality))
            
        except Exception as e:
            print(f"❌ Grid quality calculation error: {e}")
            return 0.0
    
    def _calculate_spacing_uniformity(self, levels: List[float]) -> float:
        """คำนวณความสม่ำเสมอของระยะห่าง"""
        if len(levels) < 2:
            return 1.0
        
        try:
            levels = sorted(levels)
            spacings = [levels[i+1] - levels[i] for i in range(len(levels)-1)]
            
            if not spacings:
                return 1.0
            
            avg_spacing = statistics.mean(spacings)
            spacing_variance = statistics.variance(spacings) if len(spacings) > 1 else 0
            
            # ยิ่ง variance น้อย ยิ่งสม่ำเสมอ
            uniformity = 1.0 / (1.0 + spacing_variance / (avg_spacing ** 2)) if avg_spacing > 0 else 0
            
            return min(1.0, max(0.0, uniformity))
            
        except Exception as e:
            return 0.5
    
    def _calculate_spacing_efficiency(self, buy_levels: List[float], sell_levels: List[float], 
                                    expected_spacing: float) -> float:
        """คำนวณประสิทธิภาพของ spacing"""
        try:
            all_levels = sorted(buy_levels + sell_levels)
            if len(all_levels) < 2:
                return 1.0
            
            actual_spacings = [all_levels[i+1] - all_levels[i] for i in range(len(all_levels)-1)]
            
            # เปรียบเทียบกับ expected spacing
            efficiency_scores = []
            for spacing in actual_spacings:
                ratio = min(spacing, expected_spacing) / max(spacing, expected_spacing)
                efficiency_scores.append(ratio)
            
            return statistics.mean(efficiency_scores) if efficiency_scores else 0.0
            
        except Exception as e:
            return 0.0
    
    def _update_grid_state(self, analysis: Dict, params: Dict):
        """อัพเดทสถานะกริด"""
        try:
            self.grid_state.buy_levels = analysis.get("buy_levels", [])
            self.grid_state.sell_levels = analysis.get("sell_levels", [])
            self.grid_state.missing_buy_slots = analysis.get("missing_buy_slots", [])
            self.grid_state.missing_sell_slots = analysis.get("missing_sell_slots", [])
            self.grid_state.grid_balance_ratio = analysis.get("buy_ratio", 0.5)
            self.grid_state.grid_completeness = analysis.get("grid_completeness", 0.0)
            self.grid_state.quality_score = analysis.get("grid_quality_score", 0.0)
            self.grid_state.spacing_efficiency = analysis.get("spacing_efficiency", 0.0)
            
            # กำหนด phase ตามสถานการณ์
            total_orders = analysis.get("total_orders", 0)
            optimal_size = params.get("optimal_grid_size", 5)
            
            if total_orders < optimal_size:
                self.grid_state.current_phase = GridPhase.INITIALIZATION
            elif self.grid_state.quality_score < 0.6:
                self.grid_state.current_phase = GridPhase.MAINTENANCE
            elif not self.grid_state.is_balanced:
                self.grid_state.current_phase = GridPhase.REBALANCING
            else:
                self.grid_state.current_phase = GridPhase.MONITORING
            
        except Exception as e:
            print(f"❌ Grid state update error: {e}")
    
    # ========================================================================================
    # 🏗️ 4-PHASE GRID LOGIC SYSTEM
    # ========================================================================================
    
    def _execute_grid_phase_logic(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """ดำเนินการตาม Phase ของกริด"""
        try:
            current_phase = self.grid_state.current_phase
            
            print(f"🎯 EXECUTING PHASE: {current_phase.value}")
            
            if current_phase == GridPhase.INITIALIZATION:
                return self._phase_1_initialization(analysis, params, weight)
            elif current_phase == GridPhase.MONITORING:
                return self._phase_2_monitoring(analysis, params, weight)
            elif current_phase == GridPhase.REBALANCING:
                return self._phase_3_rebalancing(analysis, params, weight)
            elif current_phase == GridPhase.MAINTENANCE:
                return self._phase_4_maintenance(analysis, params, weight)
            else:
                print(f"❌ Unknown grid phase: {current_phase}")
                return None
                
        except Exception as e:
            print(f"❌ Grid phase execution error: {e}")
            return None
    
    def _phase_1_initialization(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """
        🏗️ Phase 1: Grid Initialization - สร้างกริดเริ่มต้นอย่างเป็นระบบ
        
        เป้าหมาย:
        - สร้างกริดพื้นฐานที่เป็นระเบียบ
        - วางออเดอร์ทั้งสองฝั่งแบบสมดุล
        - ใช้ dynamic spacing ตาม volatility
        """
        try:
            print("🏗️ === PHASE 1: GRID INITIALIZATION ===")
            
            current_price = analysis["current_price"]
            total_orders = analysis["total_orders"]
            optimal_size = params["optimal_grid_size"]
            
            # เป้าหมายเริ่มต้น: สร้างกริดพื้นฐานฝั่งละ 40% ของ optimal size
            initial_target_per_side = max(2, int(optimal_size * 0.4))
            
            print(f"🎯 Initialization Target: {initial_target_per_side} orders per side")
            print(f"   Current: BUY={analysis['buy_orders']} SELL={analysis['sell_orders']}")
            
            # Priority 1: สร้างกริดพื้นฐานให้ครบ
            if analysis["buy_orders"] < initial_target_per_side and analysis["next_buy_slot"]:
                confidence = 0.85  # ความเชื่อมั่นสูงในการสร้างพื้นฐาน
                return RuleResult(
                    rule_name="grid_expansion",
                    decision=TradingDecision.BUY,
                    confidence=confidence,
                    reasoning=f"🏗️ INIT: Build BUY foundation ({analysis['buy_orders']}/{initial_target_per_side})",
                    supporting_data={
                        "target_price": analysis["next_buy_slot"],
                        "grid_phase": "INITIALIZATION",
                        "direction": "BUY",
                        "slot_priority": "FOUNDATION",
                        "spacing_used": params["dynamic_spacing"]
                    },
                    weight=weight,
                    execution_priority=1
                )
            
            if analysis["sell_orders"] < initial_target_per_side and analysis["next_sell_slot"]:
                confidence = 0.85
                return RuleResult(
                    rule_name="grid_expansion",
                    decision=TradingDecision.SELL,
                    confidence=confidence,
                    reasoning=f"🏗️ INIT: Build SELL foundation ({analysis['sell_orders']}/{initial_target_per_side})",
                    supporting_data={
                        "target_price": analysis["next_sell_slot"],
                        "grid_phase": "INITIALIZATION",
                        "direction": "SELL",
                        "slot_priority": "FOUNDATION",
                        "spacing_used": params["dynamic_spacing"]
                    },
                    weight=weight,
                    execution_priority=1
                )
            
            # มีพื้นฐานครบแล้ว - เปลี่ยนไป phase 2
            print("✅ INIT COMPLETE: Foundation grid established")
            self.grid_state.current_phase = GridPhase.MONITORING
            return None
            
        except Exception as e:
            print(f"❌ Phase 1 error: {e}")
            return None
    
    def _phase_2_monitoring(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """
        👁️ Phase 2: Grid Balance Monitoring - ตรวจสอบความสมดุลและขยายแบบชาญฉลาด
        
        เป้าหมาย:
        - ตรวจสอบความสมดุล BUY/SELL
        - ขยายกริดอย่างมีแผน
        - รักษาคุณภาพกริด
        """
        try:
            print("👁️ === PHASE 2: GRID MONITORING ===")
            
            buy_ratio = analysis["buy_ratio"]
            total_orders = analysis["total_orders"]
            optimal_size = params["optimal_grid_size"]
            max_total_orders = optimal_size * 2
            
            print(f"⚖️ Balance Analysis:")
            print(f"   BUY Ratio: {buy_ratio:.1%}")
            print(f"   Grid Size: {total_orders}/{max_total_orders}")
            print(f"   Quality: {analysis['grid_quality_score']:.2f}")
            
            # === เงื่อนไขการขยายกริด ===
            
            # 1. เช็ค market condition
            if not self._is_market_suitable_for_expansion():
                print("⏸️ Market not suitable for expansion")
                return None
            
            # 2. เช็คงบประมาณ
            if not self.capital_allocation.can_expand_grid:
                print("💰 Capital limit reached")
                return None
            
            # 3. ขยายกริดอย่างสมดุล
            if total_orders < max_total_orders:
                
                # ให้ความสำคัญกับฝั่งที่มีน้อยกว่า
                if buy_ratio < 0.35 and analysis["next_buy_slot"]:  # BUY น้อยเกินไป
                    confidence = 0.75
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"⚖️ REBALANCE: Strengthen BUY side ({buy_ratio:.1%} → target 50%)",
                        supporting_data={
                            "target_price": analysis["next_buy_slot"],
                            "grid_phase": "MONITORING",
                            "direction": "BUY",
                            "balance_action": "STRENGTHEN_WEAK_SIDE",
                            "spacing_used": params["dynamic_spacing"]
                        },
                        weight=weight,
                        execution_priority=2
                    )
                
                elif buy_ratio > 0.65 and analysis["next_sell_slot"]:  # SELL น้อยเกินไป
                    confidence = 0.75
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"⚖️ REBALANCE: Strengthen SELL side ({buy_ratio:.1%} → target 50%)",
                        supporting_data={
                            "target_price": analysis["next_sell_slot"],
                            "grid_phase": "MONITORING",
                            "direction": "SELL",
                            "balance_action": "STRENGTHEN_WEAK_SIDE",
                            "spacing_used": params["dynamic_spacing"]
                        },
                        weight=weight,
                        execution_priority=2
                    )
                
                # ขยายกริดแบบสมดุล (เมื่อสมดุลดีอยู่แล้ว)
                elif 0.4 <= buy_ratio <= 0.6:
                    # เลือกฝั่งที่มีน้อยกว่าเล็กน้อย
                    if analysis["buy_orders"] <= analysis["sell_orders"] and analysis["next_buy_slot"]:
                        confidence = 0.6
                        return RuleResult(
                            rule_name="grid_expansion",
                            decision=TradingDecision.BUY,
                            confidence=confidence,
                            reasoning=f"📈 EXPAND: Balanced BUY expansion ({total_orders}/{max_total_orders})",
                            supporting_data={
                                "target_price": analysis["next_buy_slot"],
                                "grid_phase": "MONITORING",
                                "direction": "BUY",
                                "balance_action": "BALANCED_EXPANSION",
                                "spacing_used": params["dynamic_spacing"]
                            },
                            weight=weight,
                            execution_priority=3
                        )
                    
                    elif analysis["sell_orders"] < analysis["buy_orders"] and analysis["next_sell_slot"]:
                        confidence = 0.6
                        return RuleResult(
                            rule_name="grid_expansion",
                            decision=TradingDecision.SELL,
                            confidence=confidence,
                            reasoning=f"📈 EXPAND: Balanced SELL expansion ({total_orders}/{max_total_orders})",
                            supporting_data={
                                "target_price": analysis["next_sell_slot"],
                                "grid_phase": "MONITORING",
                                "direction": "SELL",
                                "balance_action": "BALANCED_EXPANSION",
                                "spacing_used": params["dynamic_spacing"]
                            },
                            weight=weight,
                            execution_priority=3
                        )
            
            # กริดเต็มแล้วหรือไม่มีช่องที่เหมาะสม
            print("✅ MONITORING: Grid is optimal or complete")
            return None
            
        except Exception as e:
            print(f"❌ Phase 2 error: {e}")
            return None
    
    def _phase_3_rebalancing(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """
        ⚖️ Phase 3: Smart Rebalancing - ปรับสมดุลอัจฉริยะ
        
        เป้าหมาย:
        - แก้ไขความไม่สมดุลของกริด
        - ไม่ใช้การปิดออเดอร์ เน้นการปรับแต่ง
        - รักษาคุณภาพกริดโดยรวม
        """
        try:
            print("⚖️ === PHASE 3: SMART REBALANCING ===")
            
            buy_ratio = analysis["buy_ratio"]
            
            print(f"📊 Balance Status:")
            print(f"   BUY Ratio: {buy_ratio:.1%}")
            print(f"   Target Range: 30% - 70%")
            print(f"   Action: {'STRENGTHEN BUY' if buy_ratio < 0.3 else 'STRENGTHEN SELL' if buy_ratio > 0.7 else 'MINOR ADJUSTMENT'}")
            
            # === Critical Imbalance Correction ===
            
            # BUY น้อยมากเกินไป (< 30%)
            if buy_ratio < 0.3 and analysis["next_buy_slot"]:
                confidence = 0.8  # ความเชื่อมั่นสูงสำหรับการแก้ไข
                return RuleResult(
                    rule_name="grid_expansion",
                    decision=TradingDecision.BUY,
                    confidence=confidence,
                    reasoning=f"🚨 CRITICAL REBALANCE: Fix BUY shortage ({buy_ratio:.1%})",
                    supporting_data={
                        "target_price": analysis["next_buy_slot"],
                        "grid_phase": "REBALANCING",
                        "direction": "BUY",
                        "urgency": "CRITICAL",
                        "balance_target": "30-70%",
                        "spacing_used": params["dynamic_spacing"]
                    },
                    weight=weight,
                    execution_priority=1
                )
            
            # SELL น้อยมากเกินไป (> 70% BUY)
            elif buy_ratio > 0.7 and analysis["next_sell_slot"]:
                confidence = 0.8
                return RuleResult(
                    rule_name="grid_expansion",
                    decision=TradingDecision.SELL,
                    confidence=confidence,
                    reasoning=f"🚨 CRITICAL REBALANCE: Fix SELL shortage ({buy_ratio:.1%})",
                    supporting_data={
                        "target_price": analysis["next_sell_slot"],
                        "grid_phase": "REBALANCING",
                        "direction": "SELL",
                        "urgency": "CRITICAL",
                        "balance_target": "30-70%",
                        "spacing_used": params["dynamic_spacing"]
                    },
                    weight=weight,
                    execution_priority=1
                )
            
            # === Moderate Imbalance Correction ===
            
            # BUY น้อยเล็กน้อย (30-40%)
            elif 0.3 <= buy_ratio < 0.4 and analysis["next_buy_slot"]:
                confidence = 0.65
                return RuleResult(
                    rule_name="grid_expansion", 
                    decision=TradingDecision.BUY,
                    confidence=confidence,
                    reasoning=f"📊 MODERATE REBALANCE: Improve BUY side ({buy_ratio:.1%})",
                    supporting_data={
                        "target_price": analysis["next_buy_slot"],
                        "grid_phase": "REBALANCING",
                        "direction": "BUY",
                        "urgency": "MODERATE",
                        "spacing_used": params["dynamic_spacing"]
                    },
                    weight=weight,
                    execution_priority=2
                )
            
            # SELL น้อยเล็กน้อย (60-70% BUY)
            elif 0.6 < buy_ratio <= 0.7 and analysis["next_sell_slot"]:
                confidence = 0.65
                return RuleResult(
                    rule_name="grid_expansion",
                    decision=TradingDecision.SELL,
                    confidence=confidence,
                    reasoning=f"📊 MODERATE REBALANCE: Improve SELL side ({buy_ratio:.1%})",
                    supporting_data={
                        "target_price": analysis["next_sell_slot"],
                        "grid_phase": "REBALANCING", 
                        "direction": "SELL",
                        "urgency": "MODERATE",
                        "spacing_used": params["dynamic_spacing"]
                    },
                    weight=weight,
                    execution_priority=2
                )
            
            # สมดุลแล้ว - เปลี่ยนไป monitoring
            else:
                print("✅ REBALANCING COMPLETE: Grid is now balanced")
                self.grid_state.current_phase = GridPhase.MONITORING
                return None
            
        except Exception as e:
            print(f"❌ Phase 3 error: {e}")
            return None
    
    def _phase_4_maintenance(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """
        🔧 Phase 4: Grid Maintenance - บำรุงรักษากริดให้มีคุณภาพ
        
        เป้าหมาย:
        - ปรับปรุงคุณภาพกริด
        - จัดระเบียบ spacing ที่เสียรูป
        - เติมช่องว่างที่สำคัญ
        """
        try:
            print("🔧 === PHASE 4: GRID MAINTENANCE ===")
            
            quality_score = analysis["grid_quality_score"]
            spacing_efficiency = analysis["spacing_efficiency"]
            
            print(f"🛠️ Maintenance Analysis:")
            print(f"   Quality Score: {quality_score:.2f}/1.0")
            print(f"   Spacing Efficiency: {spacing_efficiency:.2f}/1.0")
            
            # === Quality Improvement Actions ===
            
            # 1. ปรับปรุงคุณภาพโดยรวม
            if quality_score < 0.6:
                # หาช่องว่างที่สำคัญที่สุด
                critical_gap = self._find_critical_grid_gap(analysis, params)
                
                if critical_gap:
                    confidence = 0.7
                    direction = critical_gap["direction"]
                    target_price = critical_gap["price"]
                    
                    decision = TradingDecision.BUY if direction == "BUY" else TradingDecision.SELL
                    
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=decision,
                        confidence=confidence,
                        reasoning=f"🔧 MAINTENANCE: Fill critical gap @ {target_price:.2f} (Quality: {quality_score:.2f})",
                        supporting_data={
                            "target_price": target_price,
                            "grid_phase": "MAINTENANCE",
                            "direction": direction,
                            "maintenance_type": "QUALITY_IMPROVEMENT",
                            "gap_importance": critical_gap["importance"],
                            "spacing_used": params["dynamic_spacing"]
                        },
                        weight=weight,
                        execution_priority=2
                    )
            
            # 2. ปรับปรุง spacing efficiency
            elif spacing_efficiency < 0.7:
                # หาจุดที่ spacing ไม่ดี
                spacing_fix = self._find_spacing_improvement(analysis, params)
                
                if spacing_fix:
                    confidence = 0.6
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.BUY if spacing_fix["direction"] == "BUY" else TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"📏 SPACING FIX: Improve spacing efficiency ({spacing_efficiency:.2f})",
                        supporting_data={
                            "target_price": spacing_fix["price"],
                            "grid_phase": "MAINTENANCE",
                            "direction": spacing_fix["direction"],
                            "maintenance_type": "SPACING_IMPROVEMENT",
                            "spacing_used": params["dynamic_spacing"]
                        },
                        weight=weight,
                        execution_priority=3
                    )
            
            # 3. คุณภาพดีแล้ว - กลับไป monitoring
            else:
                print("✅ MAINTENANCE COMPLETE: Grid quality is good")
                self.grid_state.current_phase = GridPhase.MONITORING
                return None
            
            return None
            
        except Exception as e:
            print(f"❌ Phase 4 error: {e}")
            return None
    
    def _find_critical_grid_gap(self, analysis: Dict, params: Dict) -> Optional[Dict]:
        """หาช่องว่างที่สำคัญที่สุดในกริด"""
        try:
            current_price = analysis["current_price"]
            spacing_value = params["dynamic_spacing"] * params["point_value"]
            
            # ตรวจสอบช่องว่างใกล้ current price
            critical_gaps = []
            
            # เช็ค BUY side
            for slot in analysis["missing_buy_slots"]:
                distance = abs(current_price - slot)
                importance = 1.0 / (1.0 + distance / spacing_value)  # ยิ่งใกล้ ยิ่งสำคัญ
                critical_gaps.append({
                    "direction": "BUY",
                    "price": slot,
                    "distance": distance,
                    "importance": importance
                })
            
            # เช็ค SELL side
            for slot in analysis["missing_sell_slots"]:
                distance = abs(current_price - slot)
                importance = 1.0 / (1.0 + distance / spacing_value)
                critical_gaps.append({
                    "direction": "SELL",
                    "price": slot,
                    "distance": distance,
                    "importance": importance
                })
            
            # เลือกช่องว่างที่สำคัญที่สุด
            if critical_gaps:
                critical_gaps.sort(key=lambda x: x["importance"], reverse=True)
                return critical_gaps[0]
            
            return None
            
        except Exception as e:
            print(f"❌ Critical gap finding error: {e}")
            return None
    
    def _find_spacing_improvement(self, analysis: Dict, params: Dict) -> Optional[Dict]:
        """หาจุดที่ต้องปรับปรุง spacing"""
        try:
            # วิเคราะห์ spacing ปัจจุบัน
            all_levels = sorted(analysis["buy_levels"] + analysis["sell_levels"])
            expected_spacing = params["dynamic_spacing"] * params["point_value"]
            
            # หาช่องว่างที่ใหญ่เกินไป
            for i in range(len(all_levels) - 1):
                gap = all_levels[i+1] - all_levels[i]
                if gap > expected_spacing * 1.8:  # ช่องว่างใหญ่เกินไป
                    # หาราคาที่ควรเติม
                    fill_price = all_levels[i] + expected_spacing
                    direction = "BUY" if fill_price < analysis["current_price"] else "SELL"
                    
                    return {
                        "direction": direction,
                        "price": round(fill_price, 2),
                        "gap_size": gap,
                        "improvement_type": "FILL_LARGE_GAP"
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Spacing improvement error: {e}")
            return None
    
    def _is_market_suitable_for_expansion(self) -> bool:
        """เช็คว่าสภาพตลาดเหมาะสมสำหรับการขยายกริดหรือไม่"""
        try:
            if not self.market_context:
                return True  # ถ้าไม่มีข้อมูล ให้ผ่าน
            
            market_data = self.last_market_data
            
            # เช็คเงื่อนไขที่ไม่เหมาะสม
            unsuitable_conditions = []
            
            # 1. Spread กว้างเกินไป
            spread = market_data.get("spread", 0)
            normal_spread = market_data.get("avg_spread", 5)
            if spread > normal_spread * 3:
                unsuitable_conditions.append(f"Wide spread: {spread}")
            
            # 2. Volatility สูงเกินไป
            volatility = market_data.get("volatility_factor", 1.0)
            if volatility > 3.0:
                unsuitable_conditions.append(f"Extreme volatility: {volatility:.2f}")
            
            # 3. Low liquidity
            if self.market_context.liquidity_level == "LOW":
                unsuitable_conditions.append("Low liquidity")
            
            # 4. News events หรือ market gaps
            if market_data.get("news_impact", 0) > 0.7:
                unsuitable_conditions.append("High news impact")
            
            # 5. เช็ค momentum แรงเกินไป (ราคาวิ่งแรง)
            momentum = abs(market_data.get("momentum", 0))
            if momentum > 0.8:
                unsuitable_conditions.append(f"Strong momentum: {momentum:.2f}")
            
            # แสดงผลการตรวจสอบ
            if unsuitable_conditions:
                print(f"⚠️ Market unsuitable for expansion:")
                for condition in unsuitable_conditions:
                    print(f"   - {condition}")
                return False
            
            print("✅ Market conditions favorable for grid expansion")
            return True
            
        except Exception as e:
            print(f"❌ Market suitability check error: {e}")
            return True  # ถ้าเกิดข้อผิดพลาด ให้ผ่าน

    def _make_weighted_decision(self, rule_results: List[RuleResult]) -> Optional[RuleResult]:
        """ตัดสินใจขั้นสุดท้ายด้วยระบบถ่วงน้ำหนักที่ยืดหยุ่น"""
        try:
            if not rule_results:
                return None
            
            print(f"🎯 === WEIGHTED DECISION ANALYSIS ===")
            print(f"📊 Processing {len(rule_results)} rule results:")
            
            # จัดกลุ่มตาม decision type
            decision_groups = defaultdict(list)
            
            for result in rule_results:
                decision_groups[result.decision].append(result)
                weighted_conf = result.weighted_confidence
                print(f"   {result.rule_name}: {result.decision.value} "
                        f"(conf: {result.confidence:.2f} × weight: {result.weight:.2f} = {weighted_conf:.3f})")
            
            # คำนวณคะแนนรวมแต่ละ decision
            decision_scores = {}
            decision_details = {}
            
            for decision, results in decision_groups.items():
                total_score = sum(r.weighted_confidence for r in results)
                avg_confidence = statistics.mean([r.confidence for r in results])
                avg_priority = statistics.mean([r.execution_priority for r in results])
                
                decision_scores[decision] = total_score
                decision_details[decision] = {
                    "total_score": total_score,
                    "avg_confidence": avg_confidence,
                    "avg_priority": avg_priority,
                    "rule_count": len(results),
                    "results": results
                }
            
            # หา decision ที่ดีที่สุด
            if not decision_scores:
                return None
            
            best_decision = max(decision_scores.keys(), key=lambda d: decision_scores[d])
            best_score = decision_scores[best_decision]
            best_details = decision_details[best_decision]
            
            # เช็ค threshold ที่ยืดหยุ่น
            min_threshold = 0.15  # ลดลงเพื่อให้ grid ทำงานได้
            
            # ปรับ threshold ตาม urgency
            if any("CRITICAL" in r.supporting_data.get("urgency", "") for r in best_details["results"]):
                min_threshold = 0.1  # ลด threshold สำหรับ critical actions
            elif any("FOUNDATION" in r.supporting_data.get("slot_priority", "") for r in best_details["results"]):
                min_threshold = 0.2  # เพิ่ม threshold สำหรับ foundation building
            
            print(f"🏆 Best Decision: {best_decision.value}")
            print(f"   Total Score: {best_score:.3f} (threshold: {min_threshold:.3f})")
            print(f"   Avg Confidence: {best_details['avg_confidence']:.2f}")
            print(f"   Rule Count: {best_details['rule_count']}")
            
            if best_score >= min_threshold:
                # เลือก result ที่ดีที่สุดจากกลุ่ม
                best_result = max(best_details["results"], 
                                key=lambda r: (r.confidence, -r.execution_priority))
                
                print(f"✅ DECISION APPROVED: {best_result.reasoning}")
                return best_result
            else:
                print(f"❌ DECISION REJECTED: Score too low ({best_score:.3f} < {min_threshold:.3f})")
                return None
            
        except Exception as e:
            print(f"❌ Weighted decision error: {e}")
            return None

    def _execute_trading_decision(self, decision_result: RuleResult):
        """ดำเนินการตามการตัดสินใจ"""
        try:
            print(f"⚡ === EXECUTING DECISION ===")
            print(f"🎯 Decision: {decision_result.decision.value}")
            print(f"🧠 Reasoning: {decision_result.reasoning}")
            print(f"📊 Confidence: {decision_result.confidence:.2f}")
            
            # ดำเนินการตาม decision type
            if decision_result.decision == TradingDecision.BUY:
                self._execute_buy_decision(decision_result)
            elif decision_result.decision == TradingDecision.SELL:
                self._execute_sell_decision(decision_result)
            elif decision_result.decision == TradingDecision.CLOSE_PROFITABLE:
                self._execute_close_profitable(decision_result)
            elif decision_result.decision == TradingDecision.CLOSE_LOSING:
                print("⚠️ CLOSE_LOSING skipped - no stop loss system")
            elif decision_result.decision == TradingDecision.CLOSE_ALL:
                self._execute_close_all(decision_result)
            elif decision_result.decision == TradingDecision.EMERGENCY_STOP:
                self._execute_emergency_stop(decision_result)
            
            # อัพเดท grid state
            self.grid_state.last_grid_action = datetime.now()
            
        except Exception as e:
            print(f"❌ Decision execution error: {e}")

    def _execute_buy_decision(self, decision: RuleResult):
        """ดำเนินการวาง BUY order"""
        try:
            supporting_data = decision.supporting_data
            target_price = supporting_data.get("target_price")
            
            if not target_price or target_price <= 0:
                print("❌ Invalid BUY target price")
                return
            
            # คำนวณ lot size ตามสถานการณ์
            lot_size = self._calculate_adaptive_lot_size(decision)
            
            # สร้าง order request
            order_request = {
                "order_type": "BUY_LIMIT",
                "volume": lot_size,
                "price": target_price,
                "reasoning": decision.reasoning,
                "confidence": decision.confidence
            }
            
            # ส่งไปยัง Order Manager
            if self.order_manager:
                result = self.order_manager.place_smart_order(**order_request)
                
                if result and result.get("success"):
                    print(f"✅ BUY order placed: {lot_size:.3f} lots @ {target_price:.2f}")
                    self._track_rule_performance(decision.rule_name, True)
                else:
                    print(f"❌ BUY order failed: {result.get('error', 'Unknown error')}")
                    self._track_rule_performance(decision.rule_name, False)
        
        except Exception as e:
            print(f"❌ BUY execution error: {e}")

    def _execute_sell_decision(self, decision: RuleResult):
        """ดำเนินการวาง SELL order"""
        try:
            supporting_data = decision.supporting_data
            target_price = supporting_data.get("target_price")
            
            if not target_price or target_price <= 0:
                print("❌ Invalid SELL target price")
                return
            
            # คำนวณ lot size ตามสถานการณ์
            lot_size = self._calculate_adaptive_lot_size(decision)
            
            # สร้าง order request
            order_request = {
                "order_type": "SELL_LIMIT",
                "volume": lot_size,
                "price": target_price,
                "reasoning": decision.reasoning,
                "confidence": decision.confidence
            }
            
            # ส่งไปยัง Order Manager
            if self.order_manager:
                result = self.order_manager.place_smart_order(**order_request)
                
                if result and result.get("success"):
                    print(f"✅ SELL order placed: {lot_size:.3f} lots @ {target_price:.2f}")
                    self._track_rule_performance(decision.rule_name, True)
                else:
                    print(f"❌ SELL order failed: {result.get('error', 'Unknown error')}")
                    self._track_rule_performance(decision.rule_name, False)
        
        except Exception as e:
            print(f"❌ SELL execution error: {e}")

    def _calculate_adaptive_lot_size(self, decision: RuleResult) -> float:
        """คำนวณ lot size แบบ adaptive ตามสถานการณ์"""
        try:
            # Base lot จาก Lot Calculator
            base_lot = 0.01
            if self.lot_calculator:
                base_lot = self.lot_calculator.calculate_optimal_lot_size()
            
            # ปรับตาม confidence
            confidence_multiplier = 0.5 + (decision.confidence * 0.5)  # 0.5-1.0
            
            # ปรับตาม grid phase
            phase_multipliers = {
                GridPhase.INITIALIZATION: 1.0,    # ขนาดปกติสำหรับพื้นฐาน
                GridPhase.MONITORING: 0.8,       # เล็กลงเล็กน้อย
                GridPhase.REBALANCING: 1.2,      # ใหญ่ขึ้นเพื่อแก้ไขสมดุล
                GridPhase.MAINTENANCE: 0.7       # เล็กลงสำหรับการปรับปรุง
            }
            
            phase_multiplier = phase_multipliers.get(self.grid_state.current_phase, 1.0)
            
            # ปรับตาม volatility
            volatility = self.last_market_data.get("volatility_factor", 1.0)
            if volatility > 2.0:
                volatility_multiplier = 0.6  # ลดขนาดเมื่อ volatile
            elif volatility < 0.5:
                volatility_multiplier = 1.3  # เพิ่มขนาดเมื่อเงียบ
            else:
                volatility_multiplier = 1.0
            
            # ปรับตามงบประมาณที่เหลือ
            budget_ratio = self.capital_allocation.risk_budget / self.capital_allocation.total_balance
            budget_multiplier = min(1.5, max(0.5, budget_ratio * 10))
            
            # คำนวณ lot size สุดท้าย
            final_lot = base_lot * confidence_multiplier * phase_multiplier * volatility_multiplier * budget_multiplier
            
            # จำกัดขนาดขั้นต่ำและสูงสุด
            min_lot = 0.01
            max_lot = min(1.0, self.capital_allocation.available_margin / 1000)  # ขึ้นกับ margin
            
            final_lot = max(min_lot, min(max_lot, round(final_lot, 2)))
            
            print(f"💰 Adaptive Lot Calculation:")
            print(f"   Base: {base_lot:.3f}")
            print(f"   Confidence: ×{confidence_multiplier:.2f}")
            print(f"   Phase: ×{phase_multiplier:.2f}")
            print(f"   Volatility: ×{volatility_multiplier:.2f}")
            print(f"   Budget: ×{budget_multiplier:.2f}")
            print(f"   Final: {final_lot:.3f} lots")
            
            return final_lot
            
        except Exception as e:
            print(f"❌ Adaptive lot calculation error: {e}")
            return 0.01

# ========================================================================================
# 🎯 OTHER TRADING RULES
# ========================================================================================

    def _rule_portfolio_balance(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """📊 Portfolio Balance Rule - เน้นการเก็บกำไรและการแก้ไม้"""
        try:
            portfolio_data = self.last_portfolio_data
            
            # ดึงข้อมูล positions
            profitable_positions = portfolio_data.get("profitable_positions", [])
            losing_positions = portfolio_data.get("losing_positions", [])
            
            total_profit = sum(pos.get("profit", 0) for pos in profitable_positions)
            total_loss = sum(pos.get("profit", 0) for pos in losing_positions)
            net_profit = total_profit + total_loss
            
            print(f"💰 Portfolio Analysis:")
            print(f"   Profitable: {len(profitable_positions)} positions (+{total_profit:.2f})")
            print(f"   Losing: {len(losing_positions)} positions ({total_loss:.2f})")
            print(f"   Net P&L: {net_profit:.2f}")
            
            # === เก็บกำไรเมื่อมีโอกาส ===
            profit_threshold = config["parameters"].get("profit_take_threshold", 50.0)
            
            if total_profit >= profit_threshold and len(profitable_positions) > 0:
                confidence = min(0.9, 0.5 + (total_profit / profit_threshold) * 0.4)
                
                return RuleResult(
                    rule_name="portfolio_balance",
                    decision=TradingDecision.CLOSE_PROFITABLE,
                    confidence=confidence,
                    reasoning=f"💰 PROFIT TAKE: Secure ${total_profit:.2f} profit (threshold: ${profit_threshold})",
                    supporting_data={
                        "profitable_count": len(profitable_positions),
                        "total_profit": total_profit,
                        "profit_threshold": profit_threshold,
                        "action_type": "PROFIT_SECURING"
                    },
                    weight=weight,
                    execution_priority=1
                )
            
            # === การแก้ไม้อัจฉริยะ ===
            # หาโอกาสแก้ไม้โดยใช้กำไรจากฝั่งหนึ่งไปปิดขาดทุนอีกฝั่ง
            if total_profit > 0 and total_loss < 0 and abs(total_loss) < total_profit * 0.8:
                hedge_confidence = 0.7
                
                return RuleResult(
                    rule_name="portfolio_balance",
                    decision=TradingDecision.CLOSE_PROFITABLE,  # ปิดทั้งคู่เป็น net profit
                    confidence=hedge_confidence,
                    reasoning=f"🔄 SMART HEDGE: Use ${total_profit:.2f} profit to offset ${total_loss:.2f} loss",
                    supporting_data={
                        "hedge_type": "PROFIT_OFFSET",
                        "profit_amount": total_profit,
                        "loss_amount": total_loss,
                        "net_result": net_profit,
                        "action_type": "HEDGE_RECOVERY"
                    },
                    weight=weight,
                    execution_priority=2
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Portfolio balance rule error: {e}")
            return None

    def _rule_trend_following(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """📈 Trend Following Rule - เน้นความยืดหยุ่น"""
        try:
            market_data = self.last_market_data
            
            trend_strength = market_data.get("trend_strength", 0)
            trend_direction = market_data.get("trend_direction", "SIDEWAYS")
            rsi = market_data.get("rsi", 50)
            
            # เงื่อนไขที่ยืดหยุ่น
            if trend_strength > 0.6 and trend_direction != "SIDEWAYS":
                
                if trend_direction == "UP" and rsi < 70:
                    confidence = min(0.8, trend_strength)
                    return RuleResult(
                        rule_name="trend_following",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"📈 TREND BUY: {trend_direction} trend (strength: {trend_strength:.2f})",
                        supporting_data={
                            "trend_direction": trend_direction,
                            "trend_strength": trend_strength,
                            "rsi": rsi
                        },
                        weight=weight
                    )
                
                elif trend_direction == "DOWN" and rsi > 30:
                    confidence = min(0.8, trend_strength)
                    return RuleResult(
                        rule_name="trend_following",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"📉 TREND SELL: {trend_direction} trend (strength: {trend_strength:.2f})",
                        supporting_data={
                            "trend_direction": trend_direction,
                            "trend_strength": trend_strength,
                            "rsi": rsi
                        },
                        weight=weight
                    )
            
            return None
            
        except Exception as e:
            print(f"❌ Trend following rule error: {e}")
            return None

    def _rule_mean_reversion(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """🔄 Mean Reversion Rule"""
        try:
            market_data = self.last_market_data
            
            bb_position = market_data.get("bollinger_position", 0.5)  # 0=lower, 1=upper
            rsi = market_data.get("rsi", 50)
            
            # Oversold condition
            if bb_position < 0.2 and rsi < 35:
                confidence = 0.7
                return RuleResult(
                    rule_name="mean_reversion",
                    decision=TradingDecision.BUY,
                    confidence=confidence,
                    reasoning=f"🔄 MEAN REVERSION BUY: Oversold (BB: {bb_position:.2f}, RSI: {rsi:.1f})",
                    supporting_data={
                        "bollinger_position": bb_position,
                        "rsi": rsi,
                        "reversion_type": "OVERSOLD"
                    },
                    weight=weight
                )
            
            # Overbought condition
            elif bb_position > 0.8 and rsi > 65:
                confidence = 0.7
                return RuleResult(
                    rule_name="mean_reversion",
                    decision=TradingDecision.SELL,
                    confidence=confidence,
                    reasoning=f"🔄 MEAN REVERSION SELL: Overbought (BB: {bb_position:.2f}, RSI: {rsi:.1f})",
                    supporting_data={
                        "bollinger_position": bb_position,
                        "rsi": rsi,
                        "reversion_type": "OVERBOUGHT"
                    },
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Mean reversion rule error: {e}")
            return None

    def _rule_support_resistance(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """🏛️ Support Resistance Rule"""
        try:
            market_data = self.last_market_data
            current_price = market_data.get("current_price", 0)
            
            support_levels = market_data.get("support_levels", [])
            resistance_levels = market_data.get("resistance_levels", [])
            
            # หา level ที่ใกล้ที่สุด
            closest_support = None
            closest_resistance = None
            
            for level in support_levels:
                distance = abs(current_price - level["level"])
                if distance < 50 * 0.01:  # ใกล้ support
                    closest_support = level
                    break
            
            for level in resistance_levels:
                distance = abs(current_price - level["level"])
                if distance < 50 * 0.01:  # ใกล้ resistance
                    closest_resistance = level
                    break
            
            # Near support = BUY opportunity
            if closest_support and current_price <= closest_support["level"] + 20 * 0.01:
                confidence = min(0.8, closest_support["strength"])
                return RuleResult(
                    rule_name="support_resistance",
                    decision=TradingDecision.BUY,
                    confidence=confidence,
                    reasoning=f"🏛️ SUPPORT BUY: Near support @ {closest_support['level']:.2f}",
                    supporting_data={
                        "level": closest_support["level"],
                        "strength": closest_support["strength"],
                        "level_type": "SUPPORT"
                    },
                    weight=weight
                )
            
            # Near resistance = SELL opportunity
            elif closest_resistance and current_price >= closest_resistance["level"] - 20 * 0.01:
                confidence = min(0.8, closest_resistance["strength"])
                return RuleResult(
                    rule_name="support_resistance",
                    decision=TradingDecision.SELL,
                    confidence=confidence,
                    reasoning=f"🏛️ RESISTANCE SELL: Near resistance @ {closest_resistance['level']:.2f}",
                    supporting_data={
                        "level": closest_resistance["level"],
                        "strength": closest_resistance["strength"],
                        "level_type": "RESISTANCE"
                    },
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Support resistance rule error: {e}")
            return None

# ========================================================================================
# 🎖️ PERFORMANCE AND LEARNING SYSTEM
# ========================================================================================

    def _track_rule_performance(self, rule_name: str, success: bool):
        """ติดตามประสิทธิภาพของ rule"""
        try:
            if rule_name not in self.rule_performances:
                self.rule_performances[rule_name] = {
                    "success_count": 0,
                    "total_count": 0,
                    "avg_confidence": 0.0,
                    "last_updated": datetime.now()
                }
            
            perf = self.rule_performances[rule_name]
            perf["total_count"] += 1
            if success:
                perf["success_count"] += 1
            perf["last_updated"] = datetime.now()
            
            success_rate = perf["success_count"] / perf["total_count"]
            print(f"📊 Rule Performance Update: {rule_name}")
            print(f"   Success Rate: {success_rate:.1%} ({perf['success_count']}/{perf['total_count']})")
            
        except Exception as e:
            print(f"❌ Performance tracking error: {e}")

    def _adaptive_learning_update(self):
        """อัพเดทการเรียนรู้แบบ adaptive"""
        try:
            if not self.rule_performances:
                return
            
            print("🧠 === ADAPTIVE LEARNING UPDATE ===")
            
            # ปรับ weight ตามประสิทธิภาพ
            for rule_name, perf in self.rule_performances.items():
                if perf["total_count"] >= 5:  # มีข้อมูลเพียงพอ
                    success_rate = perf["success_count"] / perf["total_count"]
                    
                    # ปรับ weight ใน config
                    if rule_name in self.rules_config.get("rules", {}):
                        current_weight = self.rules_config["rules"][rule_name].get("weight", 1.0)
                        
                        if success_rate > 0.7:
                            new_weight = min(2.0, current_weight * 1.1)  # เพิ่ม weight
                        elif success_rate < 0.4:
                            new_weight = max(0.3, current_weight * 0.9)  # ลด weight
                        else:
                            new_weight = current_weight
                        
                        self.rules_config["rules"][rule_name]["weight"] = new_weight
                        
                        if new_weight != current_weight:
                            print(f"⚡ Weight Update: {rule_name}")
                            print(f"   Success Rate: {success_rate:.1%}")
                            print(f"   Weight: {current_weight:.2f} → {new_weight:.2f}")
            
        except Exception as e:
            print(f"❌ Adaptive learning error: {e}")

    def get_rule_engine_status(self) -> Dict:
        """ดึงสถานะของ Rule Engine"""
        try:
            return {
                "is_running": self.is_running,
                "current_mode": self.current_mode.value,
                "grid_phase": self.grid_state.current_phase.value,
                "grid_quality": self.grid_state.quality_score,
                "grid_balance": self.grid_state.grid_balance_ratio,
                "grid_completeness": self.grid_state.grid_completeness,
                "total_decisions": len(self.decision_history),
                "recent_decisions": len(self.recent_decisions),
                "rule_performances": dict(self.rule_performances),
                "capital_allocation": {
                    "optimal_grid_size": self.capital_allocation.optimal_grid_size if self.capital_allocation else 0,
                    "can_expand": self.capital_allocation.can_expand_grid if self.capital_allocation else False,
                    "margin_usage": self.capital_allocation.margin_usage_ratio if self.capital_allocation else 0
                } if self.capital_allocation else {},
                "market_context": {
                    "session": self.market_context.session.value if self.market_context else "UNKNOWN",
                    "volatility": self.market_context.volatility_level if self.market_context else "UNKNOWN",
                    "suitable_for_expansion": self._is_market_suitable_for_expansion()
                } if self.market_context else {}
            }
            
        except Exception as e:
            print(f"❌ Status retrieval error: {e}")
            return {"error": str(e)}