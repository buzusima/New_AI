"""
🧠 Modern Rule Engine - Complete Flexible System
rule_engine.py
สำหรับ Modern AI Gold Grid Trading System - ระบบ Rule-based ที่ยืดหยุ่นและเป็นระบบ
รองรับ Dynamic Spacing, Adaptive Grid Size, และ Smart Resource Management
** PRODUCTION READY - NO MOCK DATA - WITH ALL MISSING METHODS **
"""

import time
import threading
import os
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
    timestamp: datetime = field(default_factory=datetime.now)
    
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
        if isinstance(mode, str):
            # แปลง string เป็น enum ถ้าจำเป็น
            mode_mapping = {
                "CONSERVATIVE": TradingMode.CONSERVATIVE,
                "MODERATE": TradingMode.MODERATE,
                "BALANCED": TradingMode.MODERATE,
                "AGGRESSIVE": TradingMode.AGGRESSIVE,
                "ADAPTIVE": TradingMode.ADAPTIVE
            }
            mode = mode_mapping.get(mode, TradingMode.MODERATE)
        
        self.current_mode = mode
        print(f"🎯 Trading mode set to: {mode.value}")
    
    # ========================================================================================
    # 🔄 MAIN ENGINE LOOP  
    # ========================================================================================
    
    def _engine_loop(self):
        """Main engine loop - ไม่ใช้ใน GUI version"""
        print("🔄 Rule engine loop started (background)")
        while self.is_running:
            try:
                # Execute one decision cycle
                decision_result = self._execute_rule_based_decision()
                
                if decision_result:
                    self._execute_trading_decision(decision_result)
                
                # Performance updates
                self._update_rule_performances()
                
                # Sleep based on mode
                sleep_time = self._get_sleep_time()
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"❌ Engine loop error: {e}")
                time.sleep(10)  # Error recovery
    
    def _get_sleep_time(self) -> int:
        """คำนวณเวลาหยุดระหว่างรอบ"""
        mode_timings = {
            TradingMode.CONSERVATIVE: 60,
            TradingMode.MODERATE: 30,
            TradingMode.AGGRESSIVE: 15,
            TradingMode.ADAPTIVE: 20,
            TradingMode.EMERGENCY: 5
        }
        return mode_timings.get(self.current_mode, 30)
    
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
            elif rule_name == "volatility_adaptation":
                return self._rule_volatility_adaptation(rule_config, weight)
            elif rule_name == "session_timing":
                return self._rule_session_timing(rule_config, weight)
            else:
                print(f"⚠️ Unknown rule: {rule_name}")
                return None
                
        except Exception as e:
            print(f"❌ Individual rule error ({rule_name}): {e}")
            return None
    
    def _make_weighted_decision(self, rule_results: List[RuleResult]) -> Optional[RuleResult]:
        """
        ตัดสินใจขั้นสุดท้ายด้วยระบบถ่วงน้ำหนัก
        
        Args:
            rule_results: ผลลัพธ์จากแต่ละ rule
            
        Returns:
            RuleResult สุดท้าย หรือ None
        """
        try:
            if not rule_results:
                return None
            
            print("🎯 === WEIGHTED DECISION MAKING ===")
            
            # จัดกลุมตามประเภทการตัดสินใจ
            decision_groups = defaultdict(list)
            for result in rule_results:
                decision_groups[result.decision].append(result)
            
            # คำนวณคะแนนถ่วงน้ำหนักสำหรับแต่ละประเภท
            decision_scores = {}
            for decision_type, results in decision_groups.items():
                total_weighted_confidence = sum(r.weighted_confidence for r in results)
                decision_scores[decision_type] = {
                    "score": total_weighted_confidence,
                    "results": results,
                    "avg_confidence": total_weighted_confidence / len(results)
                }
                print(f"   {decision_type.value}: {total_weighted_confidence:.3f} ({len(results)} rules)")
            
            # เลือกการตัดสินใจที่มีคะแนนสูงสุด
            if decision_scores:
                best_decision = max(decision_scores.keys(), key=lambda k: decision_scores[k]["score"])
                best_results = decision_scores[best_decision]["results"]
                
                # เลือก result ที่มี confidence สูงสุดจากกลุ่ม
                final_result = max(best_results, key=lambda r: r.confidence)
                
                print(f"🏆 Final Decision: {final_result.decision.value}")
                print(f"   Confidence: {final_result.confidence:.1%}")
                print(f"   Reasoning: {final_result.reasoning}")
                
                return final_result
            
            return None
            
        except Exception as e:
            print(f"❌ Weighted decision error: {e}")
            return None

    # ========================================================================================
    # 📊 INDIVIDUAL RULE IMPLEMENTATIONS
    # ========================================================================================
    
    def _rule_grid_expansion(self, rule_config: Dict, weight: float) -> Optional[RuleResult]:
        """Rule: การขยายกริดอัจฉริยะ"""
        try:
            if not self.last_market_data or not self.last_portfolio_data:
                return None
            
            analysis = self._get_grid_analysis()
            
            # ใช้ Grid Phase Logic
            return self._execute_grid_phase_logic(analysis, rule_config, weight)
            
        except Exception as e:
            print(f"❌ Grid expansion rule error: {e}")
            return None
    
    def _rule_portfolio_balance(self, rule_config: Dict, weight: float) -> Optional[RuleResult]:
        """Rule: การปรับสมดุล Portfolio"""
        try:
            if not self.last_portfolio_data:
                return None
            
            positions = self.last_portfolio_data.get("positions", [])
            if not positions:
                return None
            
            # ค้นหาโอกาสปิดออเดอร์แบบ intelligent
            profitable_positions = [p for p in positions if p.get("profit", 0) > 0]
            losing_positions = [p for p in positions if p.get("profit", 0) < 0]
            
            if profitable_positions and losing_positions:
                # คำนวณการปิดแบบ optimal combination
                best_combination = self._find_optimal_close_combination(profitable_positions, losing_positions)
                
                if best_combination and best_combination["net_profit"] > 0:
                    confidence = min(0.9, best_combination["confidence"])
                    
                    return RuleResult(
                        rule_name="portfolio_balance",
                        decision=TradingDecision.CLOSE_PROFITABLE,
                        confidence=confidence,
                        reasoning=f"💰 PORTFOLIO BALANCE: Close {len(best_combination['positions'])} positions for ${best_combination['net_profit']:.2f}",
                        supporting_data=best_combination,
                        weight=weight
                    )
            
            return None
            
        except Exception as e:
            print(f"❌ Portfolio balance rule error: {e}")
            return None
    
    def _rule_trend_following(self, rule_config: Dict, weight: float) -> Optional[RuleResult]:
        """Rule: การเทรดตามเทรนด์"""
        try:
            if not self.last_market_data:
                return None
            
            trend_direction = self.last_market_data.get("trend_direction")
            trend_strength = self.last_market_data.get("trend_strength", 0)
            
            if not trend_direction or trend_strength < 0.6:
                return None
            
            current_price = self.last_market_data.get("current_price", 0)
            analysis = self._get_grid_analysis()
            
            # เทรดตามทิศทางเทรนด์
            if trend_direction == "UP" and analysis.get("next_buy_slot"):
                confidence = min(0.8, trend_strength)
                return RuleResult(
                    rule_name="trend_following",
                    decision=TradingDecision.BUY,
                    confidence=confidence,
                    reasoning=f"📈 TREND FOLLOW: Strong uptrend (strength: {trend_strength:.1%})",
                    supporting_data={"trend_direction": trend_direction, "trend_strength": trend_strength},
                    weight=weight
                )
            
            elif trend_direction == "DOWN" and analysis.get("next_sell_slot"):
                confidence = min(0.8, trend_strength)
                return RuleResult(
                    rule_name="trend_following",
                    decision=TradingDecision.SELL,
                    confidence=confidence,
                    reasoning=f"📉 TREND FOLLOW: Strong downtrend (strength: {trend_strength:.1%})",
                    supporting_data={"trend_direction": trend_direction, "trend_strength": trend_strength},
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Trend following rule error: {e}")
            return None

    def _rule_mean_reversion(self, rule_config: Dict, weight: float) -> Optional[RuleResult]:
        """Rule: การเทรด Mean Reversion"""
        try:
            if not self.last_market_data:
                return None
            
            rsi = self.last_market_data.get("rsi")
            bollinger_position = self.last_market_data.get("bollinger_position")
            
            if rsi is None or bollinger_position is None:
                return None
            
            analysis = self._get_grid_analysis()
            
            # Oversold condition - เวลาซื้อ
            if rsi < 30 or bollinger_position < -1.5:
                if analysis.get("next_buy_slot"):
                    oversold_strength = max((30 - rsi) / 30, abs(bollinger_position + 1.5) / 1.0) if rsi < 30 else abs(bollinger_position + 1.5) / 1.0
                    confidence = min(0.85, 0.5 + oversold_strength * 0.4)
                    
                    return RuleResult(
                        rule_name="mean_reversion",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"📉➡️📈 MEAN REVERT BUY: RSI {rsi:.1f}, BB {bollinger_position:.2f}",
                        supporting_data={"rsi": rsi, "bollinger_position": bollinger_position},
                        weight=weight
                    )
            
            # Overbought condition - เวลาขาย
            elif rsi > 70 or bollinger_position > 1.5:
                if analysis.get("next_sell_slot"):
                    overbought_strength = max((rsi - 70) / 30, (bollinger_position - 1.5) / 1.0) if rsi > 70 else (bollinger_position - 1.5) / 1.0
                    confidence = min(0.85, 0.5 + overbought_strength * 0.4)
                    
                    return RuleResult(
                        rule_name="mean_reversion",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"📈➡️📉 MEAN REVERT SELL: RSI {rsi:.1f}, BB {bollinger_position:.2f}",
                        supporting_data={"rsi": rsi, "bollinger_position": bollinger_position},
                        weight=weight
                    )
            
            return None
            
        except Exception as e:
            print(f"❌ Mean reversion rule error: {e}")
            return None

    def _rule_support_resistance(self, rule_config: Dict, weight: float) -> Optional[RuleResult]:
        """Rule: การเทรดตาม Support/Resistance"""
        try:
            if not self.last_market_data:
                return None
            
            current_price = self.last_market_data.get("current_price", 0)
            support_levels = self.last_market_data.get("support_levels", [])
            resistance_levels = self.last_market_data.get("resistance_levels", [])
            
            if not support_levels and not resistance_levels:
                return None
            
            analysis = self._get_grid_analysis()
            
            # ตรวจสอบ Support levels - โอกาสซื้อ
            if support_levels and analysis.get("next_buy_slot"):
                closest_support = min(support_levels, key=lambda x: abs(x["level"] - current_price))
                distance_pct = abs(closest_support["level"] - current_price) / current_price * 100
                
                if distance_pct < 0.1:  # ใกล้ support < 0.1%
                    confidence = min(0.8, closest_support["strength"])
                    
                    return RuleResult(
                        rule_name="support_resistance",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"🛡️ SUPPORT BUY: Near support @ {closest_support['level']:.2f}",
                        supporting_data={
                            "level": closest_support["level"],
                            "strength": closest_support["strength"],
                            "level_type": "SUPPORT"
                        },
                        weight=weight
                    )
            
            # ตรวจสอบ Resistance levels - โอกาสขาย
            if resistance_levels and analysis.get("next_sell_slot"):
                closest_resistance = min(resistance_levels, key=lambda x: abs(x["level"] - current_price))
                distance_pct = abs(closest_resistance["level"] - current_price) / current_price * 100
                
                if distance_pct < 0.1:  # ใกล้ resistance < 0.1%
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

    def _rule_volatility_adaptation(self, rule_config: Dict, weight: float) -> Optional[RuleResult]:
        """Rule: การปรับตัวตาม Volatility"""
        try:
            if not self.last_market_data:
                return None
            
            volatility = self.last_market_data.get("volatility", 0)
            atr = self.last_market_data.get("atr", 0)
            
            if volatility == 0 or atr == 0:
                return None
            
            analysis = self._get_grid_analysis()
            
            # Volatility สูง = โอกาสในการขยายกริด
            if volatility > 0.7 and analysis["total_orders"] < analysis.get("optimal_grid_size", 10):
                confidence = min(0.75, volatility)
                
                # เลือกทิศทางตาม momentum
                momentum = self.last_market_data.get("momentum", 0)
                
                if momentum > 0 and analysis.get("next_buy_slot"):
                    return RuleResult(
                        rule_name="volatility_adaptation",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"⚡ VOLATILITY BUY: High vol {volatility:.1%}, positive momentum",
                        supporting_data={"volatility": volatility, "momentum": momentum},
                        weight=weight
                    )
                elif momentum < 0 and analysis.get("next_sell_slot"):
                    return RuleResult(
                        rule_name="volatility_adaptation",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"⚡ VOLATILITY SELL: High vol {volatility:.1%}, negative momentum",
                        supporting_data={"volatility": volatility, "momentum": momentum},
                        weight=weight
                    )
            
            return None
            
        except Exception as e:
            print(f"❌ Volatility adaptation rule error: {e}")
            return None

    def _rule_session_timing(self, rule_config: Dict, weight: float) -> Optional[RuleResult]:
        """Rule: การเทรดตามเซสชัน"""
        try:
            if not self.last_market_data:
                return None
            
            session = self.last_market_data.get("session", "QUIET")
            liquidity = self.last_market_data.get("liquidity_level", "LOW")
            
            analysis = self._get_grid_analysis()
            
            # เซสชันที่ดีสำหรับการขยายกริด
            if session in ["LONDON", "NEW_YORK", "OVERLAP"] and liquidity in ["HIGH", "MEDIUM"]:
                if analysis["total_orders"] < analysis.get("optimal_grid_size", 10):
                    confidence = 0.6
                    
                    # เลือกทิศทางตาม bias ของเซสชัน
                    session_bias = self._get_session_bias(session)
                    
                    if session_bias == "BUY" and analysis.get("next_buy_slot"):
                        return RuleResult(
                            rule_name="session_timing",
                            decision=TradingDecision.BUY,
                            confidence=confidence,
                            reasoning=f"🕐 SESSION BUY: {session} session, high liquidity",
                            supporting_data={"session": session, "liquidity": liquidity},
                            weight=weight
                        )
                    elif session_bias == "SELL" and analysis.get("next_sell_slot"):
                        return RuleResult(
                            rule_name="session_timing",
                            decision=TradingDecision.SELL,
                            confidence=confidence,
                            reasoning=f"🕐 SESSION SELL: {session} session, high liquidity",
                            supporting_data={"session": session, "liquidity": liquidity},
                            weight=weight
                        )
            
            return None
            
        except Exception as e:
            print(f"❌ Session timing rule error: {e}")
            return None

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
            🏗️ Phase 1: Grid Initialization - แก้ไขให้นับ positions ด้วย
            """
            try:
                print("🏗️ === PHASE 1: GRID INITIALIZATION ===")
                
                current_price = analysis["current_price"]
                total_orders = analysis["total_orders"]
                buy_orders = analysis["buy_orders"]    # รวม positions + pending
                sell_orders = analysis["sell_orders"]  # รวม positions + pending
                optimal_size = params.get("optimal_grid_size", 10)
                
                # เป้าหมายเริ่มต้น: สร้างกริดพื้นฐานฝั่งละ 40% ของ optimal size
                initial_target_per_side = max(2, int(optimal_size * 0.4))
                
                print(f"🎯 Initialization Target: {initial_target_per_side} orders per side")
                print(f"   Current: BUY={buy_orders} (including positions) SELL={sell_orders} (including positions)")
                
                # Priority 1: สร้างกริดพื้นฐานให้ครบ
                if buy_orders < initial_target_per_side and analysis.get("next_buy_slot"):
                    confidence = 0.85  # ความเชื่อมั่นสูงในการสร้างพื้นฐาน
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"🏗️ INIT: Build BUY foundation ({buy_orders}/{initial_target_per_side})",
                        supporting_data={
                            "target_price": analysis["next_buy_slot"],
                            "phase": "INITIALIZATION",
                            "target": initial_target_per_side,
                            "current": buy_orders
                        },
                        weight=weight
                    )
                
                elif sell_orders < initial_target_per_side and analysis.get("next_sell_slot"):
                    confidence = 0.85
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"🏗️ INIT: Build SELL foundation ({sell_orders}/{initial_target_per_side})",
                        supporting_data={
                            "target_price": analysis["next_sell_slot"],
                            "phase": "INITIALIZATION",
                            "target": initial_target_per_side,
                            "current": sell_orders
                        },
                        weight=weight
                    )
                
                # เมื่อกริดพื้นฐานเสร็จแล้ว -> ไป Phase 2
                if (buy_orders >= initial_target_per_side and 
                    sell_orders >= initial_target_per_side):
                    self.grid_state.current_phase = GridPhase.MONITORING
                    print("🎯 Phase 1 Complete -> Moving to Phase 2: MONITORING")
                    
                # หรือถ้ามีความไม่สมดุลมาก -> ไป Rebalancing
                elif total_orders > 0:
                    balance_ratio = buy_orders / total_orders
                    if abs(balance_ratio - 0.5) > 0.3:  # ไม่สมดุลมากกว่า 30%
                        self.grid_state.current_phase = GridPhase.REBALANCING
                        print(f"🎯 Severe Imbalance Detected ({balance_ratio:.1%}) -> Moving to REBALANCING")
                
                return None
                
            except Exception as e:
                print(f"❌ Phase 1 error: {e}")
                return None

    def _phase_2_monitoring(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """
        👀 Phase 2: Grid Monitoring - ตรวจสอบความสมดุลและโอกาส
        
        เป้าหมาย:
        - ตรวจสอบความสมดุลของกริด
        - หาโอกาสในการขยายกริดอย่างชาญฉลาด
        - ติดตามคุณภาพของกริด
        """
        try:
            print("👀 === PHASE 2: GRID MONITORING ===")
            
            balance_ratio = analysis.get("balance_ratio", 0.5)
            grid_quality = analysis.get("grid_quality", 0.0)
            optimal_size = params.get("optimal_grid_size", 10)
            
            print(f"📊 Grid Status: Balance {balance_ratio:.1%}, Quality {grid_quality:.1%}")
            
            # เช็คความไม่สมดุล
            if balance_ratio < 0.3:  # มี SELL มากเกินไป
                if analysis.get("next_buy_slot"):
                    confidence = 0.7
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"⚖️ BALANCE: Too many sells ({balance_ratio:.1%}), add BUY",
                        supporting_data={
                            "phase": "MONITORING",
                            "balance_issue": "TOO_MANY_SELLS",
                            "balance_ratio": balance_ratio
                        },
                        weight=weight
                    )
            
            elif balance_ratio > 0.7:  # มี BUY มากเกินไป
                if analysis.get("next_sell_slot"):
                    confidence = 0.7
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"⚖️ BALANCE: Too many buys ({balance_ratio:.1%}), add SELL",
                        supporting_data={
                            "phase": "MONITORING",
                            "balance_issue": "TOO_MANY_BUYS",
                            "balance_ratio": balance_ratio
                        },
                        weight=weight
                    )
            
            # ขยายกริดหากมีโอกาสและเงินทุนเพียงพอ
            if (analysis["total_orders"] < optimal_size * 0.8 and 
                self.capital_allocation and self.capital_allocation.can_expand_grid):
                
                # เลือกทิศทางที่ต้องการมากกว่า
                if balance_ratio < 0.5 and analysis.get("next_buy_slot"):
                    confidence = 0.65
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"📈 EXPAND: Opportunity expansion, need more BUY orders",
                        supporting_data={
                            "phase": "MONITORING",
                            "expansion_reason": "OPPORTUNITY",
                            "grid_utilization": analysis["total_orders"] / optimal_size
                        },
                        weight=weight
                    )
                elif balance_ratio > 0.5 and analysis.get("next_sell_slot"):
                    confidence = 0.65
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"📉 EXPAND: Opportunity expansion, need more SELL orders",
                        supporting_data={
                            "phase": "MONITORING",
                            "expansion_reason": "OPPORTUNITY",
                            "grid_utilization": analysis["total_orders"] / optimal_size
                        },
                        weight=weight
                    )
            
            # ตรวจสอบว่าต้องไป Phase 3 หรือไม่
            needs_rebalancing = (
                abs(balance_ratio - 0.5) > 0.25 or  # ไม่สมดุลมาก
                grid_quality < 0.6 or                # คุณภาพต่ำ
                analysis["total_orders"] > optimal_size * 1.2  # มีออเดอร์มากเกิน
            )
            
            if needs_rebalancing:
                self.grid_state.current_phase = GridPhase.REBALANCING
                print("🎯 Moving to Phase 3: REBALANCING")
            
            return None
            
        except Exception as e:
            print(f"❌ Phase 2 error: {e}")
            return None

    def _phase_3_rebalancing(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """
        ⚖️ Phase 3: Grid Rebalancing - ปรับสมดุลกริดอย่างชาญฉลาด
        
        เป้าหมาย:
        - ปิดออเดอร์ที่ไม่จำเป็น
        - ปรับสมดุลระหว่าง BUY/SELL
        - เพิ่มคุณภาพกริด
        """
        try:
            print("⚖️ === PHASE 3: GRID REBALANCING ===")
            
            if not self.last_portfolio_data:
                return None
            
            positions = self.last_portfolio_data.get("positions", [])
            balance_ratio = analysis.get("balance_ratio", 0.5)
            
            # Priority 1: ปิดออเดอร์ขาดทุนที่ติดนาน
            old_losing_positions = [
                p for p in positions 
                if (p.get("profit", 0) < 0 and 
                    (datetime.now() - p.get("open_time", datetime.now())).total_seconds() > 3600)
            ]
            
            if old_losing_positions:
                # หาออเดอร์กำไรมาหักลบ
                profitable_positions = [p for p in positions if p.get("profit", 0) > 0]
                
                if profitable_positions:
                    optimal_close = self._find_optimal_close_combination(
                        profitable_positions, old_losing_positions
                    )
                    
                    if optimal_close and optimal_close.get("net_profit", 0) > 0:
                        confidence = 0.8
                        return RuleResult(
                            rule_name="portfolio_balance",
                            decision=TradingDecision.CLOSE_PROFITABLE,
                            confidence=confidence,
                            reasoning=f"⚖️ REBALANCE: Close old positions for ${optimal_close['net_profit']:.2f}",
                            supporting_data={
                                "phase": "REBALANCING",
                                "close_combination": optimal_close
                            },
                            weight=weight
                        )
            
            # Priority 2: แก้ไขความไม่สมดุล
            if abs(balance_ratio - 0.5) > 0.3:
                if balance_ratio < 0.3:  # ต้องการ BUY มากกว่า
                    if analysis.get("next_buy_slot"):
                        confidence = 0.75
                        return RuleResult(
                            rule_name="grid_expansion",
                            decision=TradingDecision.BUY,
                            confidence=confidence,
                            reasoning=f"⚖️ REBALANCE: Severe imbalance, add BUY ({balance_ratio:.1%})",
                            supporting_data={
                                "phase": "REBALANCING",
                                "balance_ratio": balance_ratio,
                                "action": "ADD_BUY"
                            },
                            weight=weight
                        )
                
                elif balance_ratio > 0.7:  # ต้องการ SELL มากกว่า
                    if analysis.get("next_sell_slot"):
                        confidence = 0.75
                        return RuleResult(
                            rule_name="grid_expansion",
                            decision=TradingDecision.SELL,
                            confidence=confidence,
                            reasoning=f"⚖️ REBALANCE: Severe imbalance, add SELL ({balance_ratio:.1%})",
                            supporting_data={
                                "phase": "REBALANCING",
                                "balance_ratio": balance_ratio,
                                "action": "ADD_SELL"
                            },
                            weight=weight
                        )
            
            # ตรวจสอบว่าปรับสมดุลเสร็จแล้วหรือไม่
            if abs(balance_ratio - 0.5) < 0.2:
                self.grid_state.current_phase = GridPhase.MAINTENANCE
                print("🎯 Rebalancing Complete -> Moving to Phase 4: MAINTENANCE")
            
            return None
            
        except Exception as e:
            print(f"❌ Phase 3 error: {e}")
            return None

    def _phase_4_maintenance(self, analysis: Dict, params: Dict, weight: float) -> Optional[RuleResult]:
        """
        🔧 Phase 4: Grid Maintenance - บำรุงรักษาและเพิ่มประสิทธิภาพ
        
        เป้าหมาย:
        - รักษาคุณภาพกริด
        - หาโอกาสปิดออเดอร์เพื่อเก็บกำไร
        - ปรับปรุงประสิทธิภาพ
        """
        try:
            print("🔧 === PHASE 4: GRID MAINTENANCE ===")
            
            if not self.last_portfolio_data:
                return None
            
            positions = self.last_portfolio_data.get("positions", [])
            grid_quality = analysis.get("grid_quality", 0.0)
            
            # Priority 1: เก็บกำไรจากออเดอร์ที่กำไรดี
            highly_profitable = [
                p for p in positions 
                if p.get("profit", 0) > 50  # กำไรมากกว่า $50
            ]
            
            if highly_profitable:
                # หาออเดอร์ขาดทุนเล็กน้อยมาปิดด้วย
                small_losses = [
                    p for p in positions 
                    if -20 <= p.get("profit", 0) < 0  # ขาดทุนไม่เกิน $20
                ]
                
                if small_losses:
                    combination = self._find_profitable_close_combination(highly_profitable, small_losses)
                    
                    if combination and combination.get("net_profit", 0) > 30:
                        confidence = 0.85
                        return RuleResult(
                            rule_name="portfolio_balance",
                            decision=TradingDecision.CLOSE_PROFITABLE,
                            confidence=confidence,
                            reasoning=f"💎 MAINTENANCE: Harvest profits ${combination['net_profit']:.2f}",
                            supporting_data={
                                "phase": "MAINTENANCE",
                                "harvest_combination": combination
                            },
                            weight=weight
                        )
            
            # Priority 2: ขยายกริดหากมีโอกาสดี
            if (grid_quality > 0.7 and 
                analysis["total_orders"] < params.get("optimal_grid_size", 10) * 0.9):
                
                # ใช้ market momentum เลือกทิศทาง
                momentum = self.last_market_data.get("momentum", 0)
                
                if momentum > 0.1 and analysis.get("next_buy_slot"):
                    confidence = 0.7
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.BUY,
                        confidence=confidence,
                        reasoning=f"🚀 MAINTENANCE: Quality expansion BUY (momentum: {momentum:.2f})",
                        supporting_data={
                            "phase": "MAINTENANCE",
                            "expansion_reason": "QUALITY_MOMENTUM",
                            "momentum": momentum
                        },
                        weight=weight
                    )
                
                elif momentum < -0.1 and analysis.get("next_sell_slot"):
                    confidence = 0.7
                    return RuleResult(
                        rule_name="grid_expansion",
                        decision=TradingDecision.SELL,
                        confidence=confidence,
                        reasoning=f"🚀 MAINTENANCE: Quality expansion SELL (momentum: {momentum:.2f})",
                        supporting_data={
                            "phase": "MAINTENANCE",
                            "expansion_reason": "QUALITY_MOMENTUM",
                            "momentum": momentum
                        },
                        weight=weight
                    )
            
            # ตรวจสอบว่าต้องกลับไป Phase 2 หรือไม่
            if grid_quality < 0.5 or abs(analysis.get("balance_ratio", 0.5) - 0.5) > 0.25:
                self.grid_state.current_phase = GridPhase.MONITORING
                print("🎯 Quality degraded -> Moving back to Phase 2: MONITORING")
            
            return None
            
        except Exception as e:
            print(f"❌ Phase 4 error: {e}")
            return None

    # ========================================================================================
    # 📊 ANALYSIS AND HELPER METHODS
    # ========================================================================================
    
    def _get_grid_analysis(self) -> Dict:
        """วิเคราะห์สถานะกริดปัจจุบัน - แก้ไขให้นับ positions ด้วย"""
        try:
            if not self.last_portfolio_data or not self.last_market_data:
                return {"error": "No data available"}
            
            current_price = self.last_market_data.get("current_price", 0)
            
            # ดึงทั้ง positions และ pending orders
            positions = self.last_portfolio_data.get("positions", [])
            pending_orders = self.last_portfolio_data.get("pending_orders", [])
            
            print(f"📊 === GRID ANALYSIS DEBUG ===")
            print(f"   Current Price: {current_price:.2f}")
            print(f"   Active Positions: {len(positions)}")
            print(f"   Pending Orders: {len(pending_orders)}")
            
            # แยก positions ตามทิศทาง
            buy_positions = []
            sell_positions = []
            
            for position in positions:
                pos_type = position.get("type", "").upper()
                if pos_type in ["BUY", "POSITION_TYPE_BUY", "0"]:
                    buy_positions.append(position)
                elif pos_type in ["SELL", "POSITION_TYPE_SELL", "1"]:
                    sell_positions.append(position)
            
            # แยก pending orders ตามทิศทาง
            buy_pending = []
            sell_pending = []
            
            for order in pending_orders:
                order_type = order.get("type", "").upper()
                if "BUY" in order_type:
                    buy_pending.append(order)
                elif "SELL" in order_type:
                    sell_pending.append(order)
            
            # รวมจำนวนทั้งหมด
            total_buy_orders = len(buy_positions) + len(buy_pending)
            total_sell_orders = len(sell_positions) + len(sell_pending)
            total_orders = total_buy_orders + total_sell_orders
            
            print(f"   📊 Breakdown:")
            print(f"      BUY Positions: {len(buy_positions)}")
            print(f"      BUY Pending: {len(buy_pending)}")
            print(f"      SELL Positions: {len(sell_positions)}")
            print(f"      SELL Pending: {len(sell_pending)}")
            print(f"   📊 Totals:")
            print(f"      Total BUY: {total_buy_orders}")
            print(f"      Total SELL: {total_sell_orders}")
            print(f"      Total Orders: {total_orders}")
            
            # คำนวณ balance ratio
            balance_ratio = total_buy_orders / total_orders if total_orders > 0 else 0.5
            
            print(f"   ⚖️ Balance Ratio: {balance_ratio:.1%} BUY")
            
            # รวม levels จาก positions และ pending orders
            all_buy_levels = []
            all_sell_levels = []
            
            # เพิ่ม buy levels
            for pos in buy_positions:
                price = pos.get("price_open", pos.get("price", 0))
                if price > 0:
                    all_buy_levels.append(price)
            
            for order in buy_pending:
                price = order.get("price", 0)
                if price > 0:
                    all_buy_levels.append(price)
            
            # เพิ่ม sell levels
            for pos in sell_positions:
                price = pos.get("price_open", pos.get("price", 0))
                if price > 0:
                    all_sell_levels.append(price)
            
            for order in sell_pending:
                price = order.get("price", 0)
                if price > 0:
                    all_sell_levels.append(price)
            
            print(f"   📍 Price Levels:")
            print(f"      BUY Levels: {len(all_buy_levels)} prices")
            print(f"      SELL Levels: {len(all_sell_levels)} prices")
            
            # หา slot ถัดไป
            next_buy_slot = self._find_next_buy_slot(all_buy_levels, current_price)
            next_sell_slot = self._find_next_sell_slot(all_sell_levels, current_price)
            
            print(f"   🎯 Next Slots:")
            print(f"      Next BUY: {next_buy_slot:.2f}" if next_buy_slot else "      Next BUY: None")
            print(f"      Next SELL: {next_sell_slot:.2f}" if next_sell_slot else "      Next SELL: None")
            
            # คำนวณคุณภาพกริด
            grid_quality = self._calculate_grid_quality(all_buy_levels, all_sell_levels, current_price)
            
            # คำนวณขนาดกริดที่เหมาะสม
            optimal_grid_size = self._calculate_optimal_grid_size()
            
            # คำนวณ completeness
            grid_completeness = total_orders / (optimal_grid_size * 2) if optimal_grid_size > 0 else 0.0
            
            result = {
                "current_price": current_price,
                "total_orders": total_orders,
                "buy_orders": total_buy_orders,
                "sell_orders": total_sell_orders,
                "balance_ratio": balance_ratio,
                "next_buy_slot": next_buy_slot,
                "next_sell_slot": next_sell_slot,
                "grid_quality": grid_quality,
                "optimal_grid_size": optimal_grid_size,
                "can_expand": total_orders < optimal_grid_size * 2,
                "positions_count": len(positions),
                "pending_count": len(pending_orders),
                "total_profit": sum(p.get("profit", 0) for p in positions),
                "grid_completeness": grid_completeness,
                "buy_levels": all_buy_levels,
                "sell_levels": all_sell_levels,
                "analysis_time": datetime.now()
            }
            
            print(f"📊 Analysis Result: {total_buy_orders} BUY, {total_sell_orders} SELL, Balance: {balance_ratio:.1%}")
            
            return result
            
        except Exception as e:
            print(f"❌ Grid analysis error: {e}")
            return {"error": str(e)}
    
    def _find_next_buy_slot(self, existing_levels: List[float], current_price: float) -> Optional[float]:
        """หาตำแหน่ง BUY ถัดไป - รับ list ของ price levels"""
        try:
            if not existing_levels:
                # ไม่มีออเดอร์ BUY -> วางใต้ราคาปัจจุบัน
                spacing = self._calculate_dynamic_spacing()
                new_slot = current_price - spacing * 0.01
                print(f"🎯 No existing BUY levels -> placing {spacing} points below current price")
                return new_slot
            
            # หาราคาที่สูงที่สุดใน BUY levels
            highest_buy = max(existing_levels)
            
            # คำนวณระยะห่างที่เหมาะสม
            spacing = self._calculate_dynamic_spacing()
            
            # slot ใหม่ต้องต่ำกว่าออเดอร์ที่มีอยู่
            new_slot = highest_buy - spacing * 0.01
            
            # ตรวจสอบว่าห่างจากราคาปัจจุบันพอหรือไม่
            min_distance = spacing * 0.01
            if abs(new_slot - current_price) < min_distance:
                new_slot = current_price - min_distance
            
            print(f"🎯 Next BUY slot: {new_slot:.2f} (spacing: {spacing} points)")
            return new_slot
            
        except Exception as e:
            print(f"❌ Find next buy slot error: {e}")
            return None
    
    def _find_next_sell_slot(self, existing_levels: List[float], current_price: float) -> Optional[float]:
        """หาตำแหน่ง SELL ถัดไป - รับ list ของ price levels"""
        try:
            if not existing_levels:
                # ไม่มีออเดอร์ SELL -> วางเหนือราคาปัจจุบัน
                spacing = self._calculate_dynamic_spacing()
                new_slot = current_price + spacing * 0.01
                print(f"🎯 No existing SELL levels -> placing {spacing} points above current price")
                return new_slot
            
            # หาราคาที่ต่ำที่สุดใน SELL levels
            lowest_sell = min(existing_levels)
            
            # คำนวณระยะห่างที่เหมาะสม
            spacing = self._calculate_dynamic_spacing()
            
            # slot ใหม่ต้องสูงกว่าออเดอร์ที่มีอยู่
            new_slot = lowest_sell + spacing * 0.01
            
            # ตรวจสอบว่าห่างจากราคาปัจจุบันพอหรือไม่
            min_distance = spacing * 0.01
            if abs(new_slot - current_price) < min_distance:
                new_slot = current_price + min_distance
            
            print(f"🎯 Next SELL slot: {new_slot:.2f} (spacing: {spacing} points)")
            return new_slot
            
        except Exception as e:
            print(f"❌ Find next sell slot error: {e}")
            return None
    
    def _calculate_dynamic_spacing(self) -> float:
        """คำนวณระยะห่างแบบ dynamic"""
        try:
            # Base spacing
            base_spacing = 100  # points
            
            # ปรับตาม volatility
            volatility = self.last_market_data.get("volatility", 0.5)
            volatility_multiplier = 0.8 + (volatility * 0.6)  # 0.8-1.4
            
            # ปรับตาม spread
            spread = self.last_market_data.get("spread", 20)
            spread_multiplier = max(1.0, spread / 20)  # อย่างน้อย 1.0
            
            # ปรับตาม session
            session = self.last_market_data.get("session", "QUIET")
            session_multipliers = {
                "LONDON": 0.9,
                "NEW_YORK": 0.9,
                "OVERLAP": 0.8,
                "ASIAN": 1.1,
                "QUIET": 1.3
            }
            session_multiplier = session_multipliers.get(session, 1.0)
            
            # คำนวณระยะห่างสุดท้าย
            dynamic_spacing = base_spacing * volatility_multiplier * spread_multiplier * session_multiplier
            
            # จำกัดค่าในช่วงที่เหมาะสม
            min_spacing = 50   # points
            max_spacing = 300  # points
            
            final_spacing = max(min_spacing, min(max_spacing, dynamic_spacing))
            
            return final_spacing
            
        except Exception as e:
            print(f"❌ Dynamic spacing calculation error: {e}")
            return 100  # Default spacing
    
    def _calculate_grid_quality(self, buy_levels: List[float], sell_levels: List[float], current_price: float) -> float:
        """คำนวณคุณภาพของกริด - แก้ไขให้รับ price levels"""
        try:
            if not buy_levels and not sell_levels:
                return 0.0
            
            quality_factors = []
            
            # Factor 1: ความสมดุลระหว่าง BUY/SELL
            total_levels = len(buy_levels) + len(sell_levels)
            if total_levels > 0:
                balance_ratio = len(buy_levels) / total_levels
                balance_score = 1.0 - abs(balance_ratio - 0.5) * 2  # ยิ่งใกล้ 0.5 ยิ่งดี
                quality_factors.append(balance_score)
                print(f"📊 Quality Factor 1 (Balance): {balance_score:.2f}")
            
            # Factor 2: ความสม่ำเสมอของ spacing
            all_levels = sorted(buy_levels + sell_levels)
            
            if len(all_levels) > 2:
                spacings = [all_levels[i+1] - all_levels[i] for i in range(len(all_levels)-1)]
                spacing_std = statistics.stdev(spacings) if len(spacings) > 1 else 0
                avg_spacing = statistics.mean(spacings)
                spacing_consistency = 1.0 - min(1.0, spacing_std / avg_spacing) if avg_spacing > 0 else 0
                quality_factors.append(spacing_consistency)
                print(f"📊 Quality Factor 2 (Spacing): {spacing_consistency:.2f}")
            
            # Factor 3: ความครอบคลุมรอบราคาปัจจุบัน
            if all_levels:
                price_range = max(all_levels) - min(all_levels)
                price_coverage = min(1.0, price_range / (current_price * 0.1))  # ครอบคลุม 10% ของราคา
                quality_factors.append(price_coverage)
                print(f"📊 Quality Factor 3 (Coverage): {price_coverage:.2f}")
            
            # Factor 4: การกระจายตัวรอบราคาปัจจุบัน
            if all_levels:
                distances = [abs(p - current_price) for p in all_levels]
                avg_distance = statistics.mean(distances)
                distribution_score = min(1.0, avg_distance / (current_price * 0.02))  # ระยะเฉลี่ย 2%
                quality_factors.append(distribution_score)
                print(f"📊 Quality Factor 4 (Distribution): {distribution_score:.2f}")
            
            # คำนวณคะแนนรวม
            if quality_factors:
                overall_quality = statistics.mean(quality_factors)
                print(f"📊 Overall Grid Quality: {overall_quality:.2f}")
                return max(0.0, min(1.0, overall_quality))
            else:
                return 0.0
            
        except Exception as e:
            print(f"❌ Grid quality calculation error: {e}")
            return 0.0
    
    def _calculate_optimal_grid_size(self) -> int:
        """คำนวณขนาดกริดที่เหมาะสม"""
        try:
            if not self.capital_allocation:
                return 10  # Default
            
            # ขึ้นอยู่กับเงินทุนที่มี
            available_margin = self.capital_allocation.free_margin
            
            # คำนวณจากงบประมาณ
            base_size = max(6, min(20, int(available_margin / 1000)))
            
            # ปรับตาม trading mode
            mode_multipliers = {
                TradingMode.CONSERVATIVE: 0.7,
                TradingMode.MODERATE: 1.0,
                TradingMode.AGGRESSIVE: 1.3,
                TradingMode.ADAPTIVE: 1.1
            }
            
            multiplier = mode_multipliers.get(self.current_mode, 1.0)
            optimal_size = int(base_size * multiplier)
            
            return max(4, min(25, optimal_size))  # จำกัดในช่วง 4-25
            
        except Exception as e:
            print(f"❌ Optimal grid size calculation error: {e}")
            return 10

    def _find_optimal_close_combination(self, profitable_positions: List[Dict], losing_positions: List[Dict]) -> Optional[Dict]:
        """หาการปิดออเดอร์แบบ optimal combination"""
        try:
            if not profitable_positions or not losing_positions:
                return None
            
            best_combination = None
            best_net_profit = 0
            
            # ลองหาการรวมที่ดีที่สุด
            for profit_pos in profitable_positions:
                profit_amount = profit_pos.get("profit", 0)
                
                # หาออเดอร์ขาดทุนที่เหมาะสม
                suitable_losses = [
                    loss_pos for loss_pos in losing_positions
                    if abs(loss_pos.get("profit", 0)) < profit_amount  # ขาดทุนน้อยกว่ากำไร
                ]
                
                if suitable_losses:
                    # เลือกออเดอร์ขาดทุนที่ให้ผลรวมดีที่สุด
                    for loss_pos in suitable_losses:
                        net_profit = profit_amount + loss_pos.get("profit", 0)
                        
                        if net_profit > best_net_profit:
                            best_net_profit = net_profit
                            best_combination = {
                                "net_profit": net_profit,
                                "positions": [profit_pos, loss_pos],
                                "confidence": min(0.9, net_profit / profit_amount)
                            }
            
            return best_combination
            
        except Exception as e:
            print(f"❌ Optimal close combination error: {e}")
            return None
    
    def _find_profitable_close_combination(self, profitable_positions: List[Dict], small_losses: List[Dict]) -> Optional[Dict]:
        """หาการปิดออเดอร์เพื่อเก็บกำไร"""
        try:
            best_combination = None
            best_net_profit = 0
            
            for profit_pos in profitable_positions:
                profit_amount = profit_pos.get("profit", 0)
                
                # รวมกับออเดอร์ขาดทุนเล็กน้อย
                total_loss = sum(loss_pos.get("profit", 0) for loss_pos in small_losses)
                net_profit = profit_amount + total_loss
                
                if net_profit > best_net_profit and net_profit > 20:  # กำไรสุทธิมากกว่า $20
                    best_net_profit = net_profit
                    positions_to_close = [profit_pos] + small_losses
                    
                    best_combination = {
                        "net_profit": net_profit,
                        "positions": positions_to_close,
                        "confidence": min(0.9, net_profit / profit_amount)
                    }
            
            return best_combination
            
        except Exception as e:
            print(f"❌ Profitable close combination error: {e}")
            return None
    
    def _get_session_bias(self, session: str) -> str:
        """ดึง bias ของแต่ละเซสชัน"""
        session_biases = {
            "ASIAN": "SELL",      # มักจะ consolidate
            "LONDON": "BUY",      # มักจะ breakout
            "NEW_YORK": "SELL",   # มักจะ profit taking
            "OVERLAP": "BUY"      # volatility สูง
        }
        return session_biases.get(session, "NEUTRAL")
    
    def _execute_trading_decision(self, decision_result: RuleResult):
        """ดำเนินการตามการตัดสินใจ"""
        try:
            print(f"🎯 === EXECUTING DECISION ===")
            print(f"   Decision: {decision_result.decision.value}")
            print(f"   Rule: {decision_result.rule_name}")
            print(f"   Confidence: {decision_result.confidence:.1%}")
            print(f"   Reasoning: {decision_result.reasoning}")
            
            success = False
            
            if decision_result.decision == TradingDecision.BUY:
                success = self._execute_buy_order(decision_result)
                
            elif decision_result.decision == TradingDecision.SELL:
                success = self._execute_sell_order(decision_result)
                
            elif decision_result.decision == TradingDecision.CLOSE_PROFITABLE:
                success = self._execute_close_orders(decision_result)
            
            # Track performance
            if self.performance_tracker:
                self.performance_tracker.track_decision(decision_result, success)
            
            # บันทึกการตัดสินใจ
            self.decision_history.append(decision_result)
            self.recent_decisions.append(decision_result)
            
            return success
            
        except Exception as e:
            print(f"❌ Execute decision error: {e}")
            return False
    
    def _execute_buy_order(self, decision_result: RuleResult) -> bool:
        """ดำเนินการออเดอร์ BUY"""
        try:
            if not self.order_manager:
                return False
            
            # ดึงข้อมูลจาก decision
            supporting_data = decision_result.supporting_data
            current_price = self.last_market_data.get("current_price", 0)
            
            # คำนวณราคาและ lot size
            order_price = supporting_data.get("target_price")
            if not order_price:
                analysis = self._get_grid_analysis()
                order_price = analysis.get("next_buy_slot", current_price - 100 * 0.01)
            
            # คำนวณ lot size
            lot_size = self._calculate_position_size(decision_result)
            
            # เตรียมข้อมูลสำหรับ order manager
            market_data = dict(self.last_market_data)
            market_data["target_price"] = order_price
            market_data["rule_volume"] = lot_size
            
            # ใช้ method ที่มีอยู่แล้ว
            result = self.order_manager.place_smart_buy_order(
                confidence=decision_result.confidence,
                reasoning=decision_result.reasoning,
                market_data=market_data
            )
            
            if result:
                print(f"✅ BUY order placed: {lot_size} lots @ {order_price:.2f}")
                return True
            else:
                print(f"❌ BUY order failed")
                return False
            
        except Exception as e:
            print(f"❌ Execute buy order error: {e}")
            return False
    
    def _execute_sell_order(self, decision_result: RuleResult) -> bool:
        """ดำเนินการออเดอร์ SELL"""
        try:
            if not self.order_manager:
                return False
            
            # ดึงข้อมูลจาก decision
            supporting_data = decision_result.supporting_data
            current_price = self.last_market_data.get("current_price", 0)
            
            # คำนวณราคาและ lot size
            order_price = supporting_data.get("target_price")
            if not order_price:
                analysis = self._get_grid_analysis()
                order_price = analysis.get("next_sell_slot", current_price + 100 * 0.01)
            
            # คำนวณ lot size
            lot_size = self._calculate_position_size(decision_result)
            
            # เตรียมข้อมูลสำหรับ order manager
            market_data = dict(self.last_market_data)
            market_data["target_price"] = order_price
            market_data["rule_volume"] = lot_size
            
            # ใช้ method ที่มีอยู่แล้ว
            result = self.order_manager.place_smart_sell_order(
                confidence=decision_result.confidence,
                reasoning=decision_result.reasoning,
                market_data=market_data
            )
            
            if result:
                print(f"✅ SELL order placed: {lot_size} lots @ {order_price:.2f}")
                return True
            else:
                print(f"❌ SELL order failed")
                return False
            
        except Exception as e:
            print(f"❌ Execute sell order error: {e}")
            return False
    
    def _execute_close_orders(self, decision_result: RuleResult) -> bool:
        """ดำเนินการปิดออเดอร์"""
        try:
            if not self.position_manager:
                return False
            
            # ดึงข้อมูลการปิด
            supporting_data = decision_result.supporting_data
            positions_to_close = supporting_data.get("positions", [])
            
            if not positions_to_close:
                return False
            
            # ปิดออเดอร์แต่ละตัว
            success_count = 0
            for position in positions_to_close:
                ticket = position.get("ticket")
                if ticket:
                    result = self.position_manager.close_position(ticket)
                    if result.get("success"):
                        success_count += 1
            
            # ถือว่าสำเร็จถ้าปิดได้มากกว่าครึ่ง
            success_ratio = success_count / len(positions_to_close)
            
            if success_ratio > 0.5:
                print(f"✅ Closed {success_count}/{len(positions_to_close)} positions")
                return True
            else:
                print(f"⚠️ Partial close: {success_count}/{len(positions_to_close)} positions")
                return False
            
        except Exception as e:
            print(f"❌ Execute close orders error: {e}")
            return False
    
    def _calculate_position_size(self, decision_result: RuleResult) -> float:
        """คำนวณขนาด position"""
        try:
            if not self.order_manager or not hasattr(self.order_manager, 'lot_calculator'):
                return 0.01  # Default
            
            # ใช้ lot calculator ที่มีอยู่แล้ว
            lot_calculator = self.order_manager.lot_calculator
            
            # เตรียมข้อมูลสำหรับการคำนวณ
            market_data = {
                "condition": self.last_market_data.get("condition", "UNKNOWN"),
                "volatility_factor": self.last_market_data.get("volatility", 0.5)
            }
            
            # เรียกใช้ method ที่มีอยู่
            lot_size = lot_calculator.calculate_optimal_lot_size(
                market_data=market_data,
                confidence=decision_result.confidence,
                order_type=decision_result.decision.value,
                reasoning=decision_result.reasoning
            )
            
            return max(0.01, lot_size)  # อย่างน้อย 0.01 lot
            
        except Exception as e:
            print(f"❌ Position size calculation error: {e}")
            return 0.01

    # ========================================================================================
    # 🎖️ PERFORMANCE AND LEARNING
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
            
            # คำนวณ success rate
            success_rate = perf["success_count"] / perf["total_count"]
            print(f"📊 Rule Performance Update: {rule_name}")
            print(f"   Success Rate: {success_rate:.1%} ({perf['success_count']}/{perf['total_count']})")
            
        except Exception as e:
            print(f"❌ Performance tracking error: {e}")
    
    def _update_rule_performances(self):
        """อัพเดทประสิทธิภาพของ rules"""
        try:
            # ติดตามผลลัพธ์ของการตัดสินใจล่าสุด
            for decision in list(self.recent_decisions):
                if hasattr(decision, 'timestamp') and decision.timestamp < datetime.now() - timedelta(minutes=30):
                    # ประเมินผลลัพธ์
                    if self.performance_tracker:
                        outcome = self.performance_tracker.get_decision_outcome(decision)
                        if outcome is not None:
                            # Track performance ตาม rule ที่ใช้ในการตัดสินใจ
                            success = (outcome == "SUCCESS")
                            if hasattr(decision, 'rule_name'):
                                self._track_rule_performance(decision.rule_name, success)
                            
                            # ลบออกจาก queue หลังประเมินแล้ว
                            self.recent_decisions.remove(decision)
                            
            # ปรับปรุงการเรียนรู้แบบ adaptive ทุก 10 การตัดสินใจ
            if len(self.decision_history) % 10 == 0 and len(self.decision_history) > 0:
                self._adaptive_learning_update()
                            
        except Exception as e:
            print(f"❌ Rule performance update error: {e}")

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

    # ========================================================================================
    # 🎯 GUI INTERFACE METHODS (Missing Methods)
    # ========================================================================================
    
    def get_overall_confidence(self) -> float:
        """
        คำนวณความเชื่อมั่นรวมของระบบ
        
        Returns:
            float: ค่าความเชื่อมั่นรวม (0.0-1.0)
        """
        try:
            if not self.rule_performances:
                # ใช้ baseline confidence ถ้าไม่มีข้อมูลประสิทธิภาพ
                return 0.5
            
            # คำนวณ weighted confidence จาก rule performances
            total_weight = 0.0
            weighted_confidence = 0.0
            
            for rule_name, perf in self.rule_performances.items():
                if perf.get("total_count", 0) > 0:
                    # ดึง weight จาก rules config
                    rule_weight = self.rules_config.get("rules", {}).get(rule_name, {}).get("weight", 1.0)
                    
                    # คำนวณ success rate
                    success_rate = perf.get("success_count", 0) / perf.get("total_count", 1)
                    
                    # รวม weight
                    total_weight += rule_weight
                    weighted_confidence += success_rate * rule_weight
            
            if total_weight > 0:
                overall_confidence = weighted_confidence / total_weight
            else:
                overall_confidence = 0.5  # Default
            
            # ปรับตามสถานะตลาดและกริด
            market_factor = 1.0
            if self.market_context:
                if self.market_context.is_favorable_for_grid:
                    market_factor = 1.1  # เพิ่มความเชื่อมั่นถ้าตลาดเหมาะสม
                else:
                    market_factor = 0.9  # ลดความเชื่อมั่นถ้าตลาดไม่เหมาะสม
            
            # ปรับตามคุณภาพกริด
            grid_factor = 1.0
            if self.grid_state.quality_score > 0:
                grid_factor = 0.8 + (self.grid_state.quality_score * 0.4)  # 0.8-1.2
            
            final_confidence = overall_confidence * market_factor * grid_factor
            return max(0.0, min(1.0, final_confidence))  # จำกัดค่าระหว่าง 0-1
            
        except Exception as e:
            print(f"❌ Overall confidence calculation error: {e}")
            return 0.5  # Safe default
    
    def get_rules_status(self) -> Dict[str, Dict]:
        """
        ดึงสถานะของ rules ทั้งหมดสำหรับ GUI
        
        Returns:
            Dict: สถานะของแต่ละ rule
        """
        try:
            rules_status = {}
            
            # วนผ่าน rules ที่มีใน config
            for rule_name, rule_config in self.rules_config.get("rules", {}).items():
                # ดึงข้อมูลพื้นฐานจาก config
                enabled = rule_config.get("enabled", True)
                weight = rule_config.get("weight", 1.0)
                confidence_threshold = rule_config.get("confidence_threshold", 0.6)
                
                # ดึงข้อมูลประสิทธิภาพ
                perf = self.rule_performances.get(rule_name, {})
                total_count = perf.get("total_count", 0)
                success_count = perf.get("success_count", 0)
                
                # คำนวณ metrics
                success_rate = success_count / total_count if total_count > 0 else 0.0
                avg_confidence = perf.get("avg_confidence", 0.0)
                
                # เช็คว่า rule active หรือไม่ (มีการใช้งานล่าสุด)
                last_updated = perf.get("last_updated")
                is_recently_active = False
                if last_updated:
                    time_diff = (datetime.now() - last_updated).total_seconds()
                    is_recently_active = time_diff < 3600  # ใช้งานภายใน 1 ชั่วโมง
                
                # สร้างสถานะของ rule
                rules_status[rule_name] = {
                    "enabled": enabled,
                    "active": enabled and is_recently_active,
                    "weight": weight,
                    "confidence_threshold": confidence_threshold,
                    "confidence": success_rate,  # ใช้ success rate เป็น confidence
                    "total_decisions": total_count,
                    "successful_decisions": success_count,
                    "success_rate": success_rate,
                    "avg_confidence": avg_confidence,
                    "last_updated": last_updated,
                    "status": self._get_rule_status_text(rule_name, success_rate, total_count)
                }
            
            return rules_status
            
        except Exception as e:
            print(f"❌ Rules status error: {e}")
            return {}
    
    def _get_rule_status_text(self, rule_name: str, success_rate: float, total_count: int) -> str:
        """สร้างข้อความสถานะของ rule"""
        try:
            if total_count == 0:
                return "🔶 No Data"
            elif total_count < 5:
                return f"🔸 Learning ({total_count} samples)"
            elif success_rate > 0.7:
                return "🟢 Performing Well"
            elif success_rate > 0.5:
                return "🟡 Average Performance"
            elif success_rate > 0.3:
                return "🟠 Below Average"
            else:
                return "🔴 Poor Performance"
                
        except Exception as e:
            return "❓ Status Unknown"
    
    def get_system_status(self) -> Dict:
        """
        ดึงสถานะระบบครบถ้วนสำหรับ GUI
        
        Returns:
            Dict: สถานะระบบทั้งหมด
        """
        try:
            # คำนวณ metrics พื้นฐาน
            overall_confidence = self.get_overall_confidence()
            
            # ดึงข้อมูลจาก market data ล่าสุด
            market_condition = "UNKNOWN"
            current_price = 0.0
            if self.last_market_data:
                market_condition = self.last_market_data.get("condition", "UNKNOWN")
                current_price = self.last_market_data.get("current_price", 0.0)
            
            # ดึงข้อมูลจาก portfolio data ล่าสุด
            total_profit = 0.0
            active_positions = 0
            pending_orders = 0
            if self.last_portfolio_data:
                total_profit = self.last_portfolio_data.get("total_profit", 0.0)
                active_positions = self.last_portfolio_data.get("total_positions", 0)
                pending_orders = self.last_portfolio_data.get("pending_orders", 0)
            
            # คำนวณ risk level
            risk_level = 0.0
            if self.capital_allocation:
                risk_level = self.capital_allocation.margin_usage_ratio
            
            # ดึงการตัดสินใจล่าสุด
            last_action = "NONE"
            action_reason = "System initializing..."
            if self.recent_decisions:
                latest_decision = self.recent_decisions[-1]
                last_action = latest_decision.decision.value
                action_reason = latest_decision.reasoning
            
            # คำนวณ survivability
            survivability_usage = 0.0
            if hasattr(self, 'survivability_points_used') and hasattr(self, 'total_survivability_points'):
                if self.total_survivability_points > 0:
                    survivability_usage = (self.survivability_points_used / self.total_survivability_points) * 100
            
            return {
                'rule_confidence': overall_confidence,
                'market_condition': market_condition,
                'portfolio_health': max(0.0, min(1.0, 1.0 - risk_level)),  # สุขภาพ portfolio
                'total_profit': total_profit,
                'active_positions': active_positions,
                'pending_orders': pending_orders,
                'risk_level': risk_level,
                'last_action': last_action,
                'action_reason': action_reason,
                'survivability_usage': survivability_usage,
                'engine_running': self.is_running,
                'current_price': current_price,
                'grid_quality': self.grid_state.quality_score,
                'grid_balance': self.grid_state.grid_balance_ratio,
                'grid_phase': self.grid_state.current_phase.value
            }
            
        except Exception as e:
            print(f"❌ System status error: {e}")
            return {
                'rule_confidence': 0.5,
                'market_condition': 'ERROR',
                'portfolio_health': 0.5,
                'total_profit': 0.0,
                'active_positions': 0,
                'pending_orders': 0,
                'risk_level': 0.0,
                'last_action': 'ERROR',
                'action_reason': f'System error: {e}',
                'survivability_usage': 0.0,
                'engine_running': False
            }

    # ========================================================================================
    # 🔧 UTILITY AND HELPER METHODS
    # ========================================================================================
    
    def save_performance_data(self, filepath: str = "performance_data.json"):
        """บันทึกข้อมูลประสิทธิภาพลงไฟล์"""
        try:
            performance_data = {
                "rule_performances": dict(self.rule_performances),
                "total_decisions": len(self.decision_history),
                "last_updated": datetime.now().isoformat(),
                "rules_config": self.rules_config
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(performance_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Performance data saved to {filepath}")
            
        except Exception as e:
            print(f"❌ Save performance data error: {e}")
    
    def load_performance_data(self, filepath: str = "performance_data.json"):
        """โหลดข้อมูลประสิทธิภาพจากไฟล์"""
        try:
            if not os.path.exists(filepath):
                print(f"⚠️ Performance data file not found: {filepath}")
                return
            
            with open(filepath, 'r', encoding='utf-8') as f:
                performance_data = json.load(f)
            
            # โหลดข้อมูลประสิทธิภาพ
            if "rule_performances" in performance_data:
                self.rule_performances = performance_data["rule_performances"]
                
                # แปลง datetime strings กลับเป็น datetime objects
                for rule_name, perf in self.rule_performances.items():
                    if "last_updated" in perf and isinstance(perf["last_updated"], str):
                        perf["last_updated"] = datetime.fromisoformat(perf["last_updated"])
            
            # โหลด rules config ถ้ามี
            if "rules_config" in performance_data:
                self.rules_config.update(performance_data["rules_config"])
            
            print(f"📁 Performance data loaded from {filepath}")
            print(f"   Loaded {len(self.rule_performances)} rule performances")
            
        except Exception as e:
            print(f"❌ Load performance data error: {e}")
    
    def reset_performance_data(self):
        """รีเซ็ตข้อมูลประสิทธิภาพทั้งหมด"""
        try:
            self.rule_performances = {}
            self.decision_history = []
            self.recent_decisions = deque(maxlen=20)
            
            print("🔄 Performance data reset complete")
            
        except Exception as e:
            print(f"❌ Reset performance data error: {e}")
    
    def get_performance_summary(self) -> Dict:
        """สร้างสรุปประสิทธิภาพแบบย่อ"""
        try:
            if not self.rule_performances:
                return {"message": "No performance data available"}
            
            summary = {}
            total_decisions = 0
            total_successes = 0
            
            for rule_name, perf in self.rule_performances.items():
                rule_total = perf.get("total_count", 0)
                rule_success = perf.get("success_count", 0)
                rule_rate = rule_success / rule_total if rule_total > 0 else 0.0
                
                summary[rule_name] = {
                    "decisions": rule_total,
                    "success_rate": round(rule_rate, 3),
                    "status": "🟢" if rule_rate > 0.6 else "🟡" if rule_rate > 0.4 else "🔴"
                }
                
                total_decisions += rule_total
                total_successes += rule_success
            
            overall_rate = total_successes / total_decisions if total_decisions > 0 else 0.0
            
            summary["_overall"] = {
                "total_decisions": total_decisions,
                "overall_success_rate": round(overall_rate, 3),
                "confidence_level": self.get_overall_confidence()
            }
            
            return summary
            
        except Exception as e:
            print(f"❌ Performance summary error: {e}")
            return {"error": str(e)}

    def _update_context_awareness(self):
        """อัพเดทความตระหนักในบริบท"""
        try:
            if not self.last_market_data:
                return
            
            # อัพเดท market context
            self.market_context = MarketContext(
                session=MarketSession(self.last_market_data.get("session", "QUIET")),
                volatility_level=self.last_market_data.get("volatility_level", "MEDIUM"),
                trend_direction=self.last_market_data.get("trend_direction", "SIDEWAYS"),
                trend_strength=self.last_market_data.get("trend_strength", 0.5),
                liquidity_level=self.last_market_data.get("liquidity_level", "MEDIUM"),
                spread_condition=self.last_market_data.get("spread_condition", "NORMAL"),
                momentum=self.last_market_data.get("momentum", 0.0)
            )
            
            # อัพเดท capital allocation
            if self.last_portfolio_data:
                account_data = self.last_portfolio_data.get("account_info", {})
                self.capital_allocation = CapitalAllocation(
                    total_balance=account_data.get("balance", 0),
                    available_margin=account_data.get("margin", 0),
                    used_margin=account_data.get("margin_used", 0),
                    free_margin=account_data.get("margin_free", 0),
                    max_grid_allocation=0.6,  # ใช้ 60% ของเงินทุนกับกริด
                    optimal_grid_size=self._calculate_optimal_grid_size(),
                    risk_budget=account_data.get("margin_free", 0) * 0.1  # 10% ของ free margin
                )
            
        except Exception as e:
            print(f"❌ Context awareness update error: {e}")

    def _is_market_suitable_for_expansion(self) -> bool:
        """เช็คว่าตลาดเหมาะสำหรับการขยายกริดหรือไม่"""
        try:
            if not self.market_context:
                return True  # Default: อนุญาต
            
            # เช็คเงื่อนไขตลาด
            suitable_volatility = self.market_context.volatility_level in ["LOW", "MEDIUM", "HIGH"]
            suitable_liquidity = self.market_context.liquidity_level in ["HIGH", "MEDIUM"]
            suitable_spread = self.market_context.spread_condition in ["NORMAL", "WIDE"]
            
            return suitable_volatility and suitable_liquidity and suitable_spread
            
        except Exception as e:
            print(f"❌ Market suitability check error: {e}")
            return True  # Default: อนุญาต

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

    def _check_emergency_conditions(self) -> bool:
        """ตรวจสอบสถานการณ์ฉุกเฉิน"""
        try:
            if not self.last_portfolio_data:
                return False
            
            # เช็ค margin level
            account_info = self.last_portfolio_data.get("account_info", {})
            margin_level = account_info.get("margin_level", 1000)
            
            if margin_level < 200:  # Margin call risk
                print("🚨 EMERGENCY: Low margin level!")
                return True
            
            # เช็ค total loss
            total_profit = self.last_portfolio_data.get("total_profit", 0)
            if total_profit < -1000:  # Loss มากกว่า $1000
                print("🚨 EMERGENCY: High total loss!")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Emergency check error: {e}")
            return False

    def force_emergency_stop(self) -> bool:
        """บังคับหยุดฉุกเฉิน"""
        try:
            print("🚨 === EMERGENCY STOP ACTIVATED ===")
            
            self.is_running = False
            self.current_mode = TradingMode.EMERGENCY
            
            # ปิดออเดอร์ที่ขาดทุนหนัก
            if self.position_manager and self.last_portfolio_data:
                positions = self.last_portfolio_data.get("positions", [])
                heavy_losses = [p for p in positions if p.get("profit", 0) < -100]
                
                for position in heavy_losses:
                    ticket = position.get("ticket")
                    if ticket:
                        self.position_manager.close_position(ticket)
            
            print("🚨 Emergency stop completed")
            return True
            
        except Exception as e:
            print(f"❌ Emergency stop error: {e}")
            return False

    def __del__(self):
        """Cleanup เมื่อ object ถูกลบ"""
        try:
            if self.is_running:
                self.stop()
        except:
            pass  # ไม่ต้องแสดง error ตอน cleanup