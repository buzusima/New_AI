"""
🧠 Modern Rule Engine - Enhanced 4D AI Edition
rule_engine.py

Enhanced Features:
- ลด confidence_threshold เพื่อเข้าตลาดได้ง่ายขึ้น
- เพิ่ม 4D AI decision logic
- Market Order approach (ไม่รอราคา)
- Portfolio Balance Weight เพิ่มขึ้น
- Hybrid Entry Logic (Balance + Margin + Time + Opportunity)
- Smart Recovery Integration

** PRODUCTION READY - NO MOCK DATA **
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import deque, defaultdict
import json
import os

# ========================================================================================
# 📊 ENUMS & DATA STRUCTURES
# ========================================================================================

class TradingMode(Enum):
    """โหมดการเทรด"""
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"  
    AGGRESSIVE = "AGGRESSIVE"
    ADAPTIVE = "ADAPTIVE"

class GridPhase(Enum):
    """เฟสของกริด"""
    INITIALIZATION = "INITIALIZATION"
    BUILDING = "BUILDING"
    OPTIMIZATION = "OPTIMIZATION"
    RECOVERY = "RECOVERY"

class MarketSession(Enum):
    """เซสชันตลาด"""
    ASIAN = "ASIAN"
    LONDON = "LONDON"
    NEW_YORK = "NEW_YORK"
    OVERLAP = "OVERLAP"
    QUIET = "QUIET"

class EntryDecision(Enum):
    """การตัดสินใจเข้าตลาด"""
    BUY_MARKET = "BUY_MARKET"
    SELL_MARKET = "SELL_MARKET"
    WAIT = "WAIT"
    ANALYZE = "ANALYZE"

@dataclass
class GridState:
    """สถานะกริดปัจจุบัน"""
    current_phase: GridPhase
    buy_levels: List[float] = field(default_factory=list)
    sell_levels: List[float] = field(default_factory=list)
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

@dataclass
class FourDimensionAnalysis:
    """🧠 4-Dimensional AI Analysis"""
    # Dimension 1: Position Value Analysis (30%)
    position_value_score: float = 0.0
    profit_potential: float = 0.0
    loss_magnitude: float = 0.0
    age_performance_ratio: float = 0.0
    
    # Dimension 2: Portfolio Safety (25%) 
    portfolio_safety_score: float = 0.0
    margin_efficiency: float = 0.0
    risk_contribution: float = 0.0
    safety_buffer: float = 0.0
    
    # Dimension 3: Hedge Relationships (25%)
    hedge_opportunity_score: float = 0.0
    recovery_potential: float = 0.0
    hedge_pairs_count: int = 0
    balance_improvement: float = 0.0
    
    # Dimension 4: Market Context (20%)
    market_context_score: float = 0.0
    trend_alignment: float = 0.0
    session_timing: float = 0.0
    volatility_match: float = 0.0
    
    @property
    def overall_score(self) -> float:
        """คะแนนรวมถ่วงน้ำหนัก"""
        return (
            self.position_value_score * 0.30 +
            self.portfolio_safety_score * 0.25 +
            self.hedge_opportunity_score * 0.25 +
            self.market_context_score * 0.20
        )
    
    @property
    def recommendation(self) -> str:
        """คำแนะนำจาก 4D Analysis"""
        if self.overall_score >= 0.8:
            return "STRONG_ENTRY"
        elif self.overall_score >= 0.6:
            return "MODERATE_ENTRY"
        elif self.overall_score >= 0.4:
            return "CAUTIOUS_ENTRY"
        elif self.overall_score >= 0.2:
            return "RECOVERY_MODE"
        else:
            return "WAIT_OPPORTUNITY"

# ========================================================================================
# 🧠 MODERN RULE ENGINE CLASS
# ========================================================================================

class ModernRuleEngine:
    """
    🧠 Modern Rule Engine - Enhanced 4D AI Edition
    
    ความสามารถใหม่:
    - 4-Dimensional Analysis System
    - Market Order Approach (ไม่รอราคา)
    - Hybrid Entry Logic (Multi-factor)
    - Reduced Confidence Thresholds (เข้าง่ายขึ้น)
    - Portfolio Balance Focus
    - Smart Recovery Integration
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
        
        # 4D AI Analysis
        self.last_4d_analysis = None
        self.analysis_history = deque(maxlen=100)
        
        # Data tracking
        self.last_market_data = {}
        self.last_portfolio_data = {}
        self.recent_decisions = deque(maxlen=100)
        self.decision_history = []
        
        # Performance tracking - Enhanced with 4D metrics
        self.rule_performances = defaultdict(lambda: {
            "success_count": 0,
            "total_count": 0,
            "avg_confidence": 0.0,
            "avg_4d_score": 0.0,
            "last_updated": datetime.now(),
            "profit_factor": 0.0,
            "recovery_success_rate": 0.0
        })
        
        # Grid management - Enhanced
        self.last_grid_analysis_time = datetime.now()
        self.grid_analysis_interval = 30  # วินาที
        self.spacing_history = deque(maxlen=50)
        self.entry_opportunities = deque(maxlen=20)
        
        # Enhanced thresholds (ลดลงเพื่อเข้าง่ายขึ้น)
        self.enhanced_thresholds = {
            "min_entry_confidence": 0.25,  # ลดจาก 0.4
            "portfolio_balance_weight": 3.5,  # เพิ่มจาก 2.0
            "margin_safety_weight": 2.0,
            "recovery_priority_weight": 4.0,  # เพิ่มขึ้น
            "market_opportunity_weight": 1.5
        }
        
        print("🧠 Enhanced 4D AI Rule Engine initialized")
    
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
        print("🚀 Enhanced 4D AI Rule Engine started")
    
    def stop(self):
        """หยุด Rule Engine"""
        self.is_running = False
        if self.engine_thread:
            self.engine_thread.join(timeout=5)
        print("🛑 Enhanced rule engine stopped")
    
    def set_trading_mode(self, mode: TradingMode):
        """ตั้งค่าโหมดการเทรด"""
        if isinstance(mode, str):
            mode_mapping = {
                "CONSERVATIVE": TradingMode.CONSERVATIVE,
                "MODERATE": TradingMode.MODERATE,
                "BALANCED": TradingMode.MODERATE,
                "AGGRESSIVE": TradingMode.AGGRESSIVE,
                "ADAPTIVE": TradingMode.ADAPTIVE
            }
            mode = mode_mapping.get(mode, TradingMode.MODERATE)
        
        self.current_mode = mode
        
        # ปรับ thresholds ตาม mode
        if mode == TradingMode.AGGRESSIVE:
            self.enhanced_thresholds["min_entry_confidence"] = 0.15  # เข้าง่ายมาก
            self.enhanced_thresholds["portfolio_balance_weight"] = 4.0
        elif mode == TradingMode.CONSERVATIVE:
            self.enhanced_thresholds["min_entry_confidence"] = 0.35
            self.enhanced_thresholds["portfolio_balance_weight"] = 2.5
        else:  # MODERATE/ADAPTIVE
            self.enhanced_thresholds["min_entry_confidence"] = 0.25
            self.enhanced_thresholds["portfolio_balance_weight"] = 3.5
            
        print(f"🎯 Trading mode set to: {mode.value}")
        print(f"   Entry confidence: {self.enhanced_thresholds['min_entry_confidence']}")
    
    # ========================================================================================
    # 🔄 MAIN ENGINE LOOP - ENHANCED
    # ========================================================================================
    
    def _engine_loop(self):
        """หลัก Engine Loop - Enhanced with 4D AI"""
        print("🔄 Enhanced 4D AI Engine loop started")
        
        while self.is_running:
            try:
                loop_start = time.time()
                
                # 1. Update market context
                self._update_market_context()
                
                # 2. Update capital allocation
                self._update_capital_allocation()
                
                # 3. 🧠 4D AI Analysis - Core Feature
                four_d_analysis = self._perform_4d_analysis()
                
                # 4. Hybrid Entry Decision
                entry_decision = self._make_hybrid_entry_decision(four_d_analysis)
                
                # 5. Recovery System Check
                recovery_action = self._check_recovery_opportunities(four_d_analysis)
                
                # 6. Execute decisions
                if entry_decision != EntryDecision.WAIT:
                    self._execute_entry_decision(entry_decision, four_d_analysis)
                
                if recovery_action:
                    self._execute_recovery_action(recovery_action, four_d_analysis)
                
                # 7. Update performance tracking
                self._update_performance_tracking(four_d_analysis)
                
                # 8. Grid maintenance
                self._maintain_grid_quality()
                
                # Sleep with dynamic interval
                loop_time = time.time() - loop_start
                sleep_time = max(1.0, 3.0 - loop_time)  # รัดกุมขึ้น
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"❌ Engine loop error: {e}")
                time.sleep(5)  # Wait before retry
                
        print("🛑 Enhanced engine loop stopped")
    
    # ========================================================================================
    # 🧠 4D AI ANALYSIS SYSTEM
    # ========================================================================================
    
    def _perform_4d_analysis(self) -> FourDimensionAnalysis:
        """🧠 ดำเนินการวิเคราะห์ 4 มิติ"""
        try:
            analysis = FourDimensionAnalysis()
            
            # Dimension 1: Position Value Analysis (30%)
            analysis.position_value_score = self._analyze_position_values()
            
            # Dimension 2: Portfolio Safety (25%)
            analysis.portfolio_safety_score = self._analyze_portfolio_safety()
            
            # Dimension 3: Hedge Relationships (25%)
            analysis.hedge_opportunity_score = self._analyze_hedge_opportunities()
            
            # Dimension 4: Market Context (20%)
            analysis.market_context_score = self._analyze_market_context()
            
            # Store for history
            self.last_4d_analysis = analysis
            self.analysis_history.append(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"❌ 4D Analysis error: {e}")
            return FourDimensionAnalysis()  # Return empty analysis
    
    def _analyze_position_values(self) -> float:
        """Dimension 1: วิเคราะห์มูลค่าออเดอร์ (30%)"""
        try:
            positions = self.position_manager.get_active_positions()
            if not positions:
                return 0.5  # Neutral if no positions
            
            total_score = 0.0
            total_weight = 0.0
            
            for pos in positions:
                # Individual profit/loss assessment
                profit_score = min(max((pos.get('profit', 0) + 100) / 200, 0), 1)
                
                # Age vs performance correlation
                age_hours = (datetime.now() - pos.get('time', datetime.now())).total_seconds() / 3600
                age_penalty = max(0, 1 - (age_hours / 24))  # ลดลงตามเวลา
                
                # Growth potential
                volume = pos.get('volume', 0.01)
                growth_potential = min(volume / 0.1, 1.0)  # ออเดอร์ใหญ่ = potential สูง
                
                # Combined score
                position_score = (profit_score * 0.5 + age_penalty * 0.3 + growth_potential * 0.2)
                position_weight = volume
                
                total_score += position_score * position_weight
                total_weight += position_weight
            
            return total_score / total_weight if total_weight > 0 else 0.5
            
        except Exception as e:
            print(f"❌ Position value analysis error: {e}")
            return 0.5
    
    def _analyze_portfolio_safety(self) -> float:
        """Dimension 2: วิเคราะห์ความปลอดภัย Portfolio (25%)"""
        try:
            if not self.capital_allocation:
                return 0.5
            
            # Margin efficiency calculation
            margin_score = 1 - self.capital_allocation.margin_usage_ratio
            margin_score = max(0, min(1, margin_score))
            
            # Risk distribution
            positions = self.position_manager.get_active_positions()
            buy_count = sum(1 for p in positions if p.get('type') == 0)  # BUY
            sell_count = sum(1 for p in positions if p.get('type') == 1)  # SELL
            total_count = len(positions)
            
            if total_count > 0:
                balance_ratio = min(buy_count, sell_count) / max(buy_count, sell_count, 1)
                balance_score = balance_ratio
            else:
                balance_score = 1.0  # Perfect if no positions
            
            # Emergency preparedness
            free_margin_ratio = self.capital_allocation.free_margin / self.capital_allocation.available_margin
            emergency_score = min(max(free_margin_ratio * 2, 0), 1)  # ดีถ้ามี free margin มาก
            
            # Combined safety score
            safety_score = (margin_score * 0.4 + balance_score * 0.4 + emergency_score * 0.2)
            
            return max(0, min(1, safety_score))
            
        except Exception as e:
            print(f"❌ Portfolio safety analysis error: {e}")
            return 0.5
    
    def _analyze_hedge_opportunities(self) -> float:
        """Dimension 3: วิเคราะห์โอกาส Hedge (25%)"""
        try:
            positions = self.position_manager.get_active_positions()
            if len(positions) < 2:
                return 0.3  # โอกาสต่ำถ้าออเดอร์น้อย
            
            hedge_score = 0.0
            hedge_pairs = 0
            recovery_opportunities = 0
            
            # หา hedge pairs
            buy_positions = [p for p in positions if p.get('type') == 0]
            sell_positions = [p for p in positions if p.get('type') == 1]
            
            for buy_pos in buy_positions:
                buy_profit = buy_pos.get('profit', 0)
                if buy_profit <= 0:  # ขาดทุน
                    # หา sell positions ที่กำไร
                    for sell_pos in sell_positions:
                        sell_profit = sell_pos.get('profit', 0)
                        if sell_profit > 0:
                            # คำนวณ hedge potential
                            profit_ratio = abs(sell_profit / buy_profit) if buy_profit != 0 else 0
                            if 0.5 <= profit_ratio <= 2.0:  # Suitable hedge ratio
                                hedge_pairs += 1
                                recovery_opportunities += 1
            
            # Cross-position synergy analysis
            total_profit = sum(p.get('profit', 0) for p in positions)
            positive_positions = sum(1 for p in positions if p.get('profit', 0) > 0)
            negative_positions = len(positions) - positive_positions
            
            if negative_positions > 0:
                synergy_score = positive_positions / len(positions)
                hedge_score = (hedge_pairs / max(negative_positions, 1)) * 0.6 + synergy_score * 0.4
            else:
                hedge_score = 1.0  # Perfect if all profitable
            
            return max(0, min(1, hedge_score))
            
        except Exception as e:
            print(f"❌ Hedge analysis error: {e}")
            return 0.5
    
    def _analyze_market_context(self) -> float:
        """Dimension 4: วิเคราะห์บริบทตลาด (20%)"""
        try:
            if not self.market_context:
                return 0.5
            
            # Trend alignment assessment
            trend_score = 0.5  # Default neutral
            if self.market_context.trend_direction == "SIDEWAYS":
                trend_score = 0.8  # ดีสำหรับกริด
            elif self.market_context.trend_strength < 0.3:
                trend_score = 0.7  # เทรนด์อ่อน = ดีสำหรับกริด
            else:
                trend_score = 0.3  # เทรนด์แรง = ยากสำหรับกริด
            
            # Session timing optimization
            session_score = 0.5
            if self.market_context.session in [MarketSession.LONDON, MarketSession.OVERLAP]:
                session_score = 0.8  # เซสชันดี
            elif self.market_context.session == MarketSession.QUIET:
                session_score = 0.3  # เซสชันเงียบ
            
            # Volatility exposure management
            volatility_score = 0.5
            if self.market_context.volatility_level == "MEDIUM":
                volatility_score = 0.8  # ดีที่สุดสำหรับกริด
            elif self.market_context.volatility_level in ["LOW", "HIGH"]:
                volatility_score = 0.6  # พอใช้ได้
            else:  # VERY_LOW or VERY_HIGH
                volatility_score = 0.2  # ไม่เหมาะ
            
            # Liquidity condition analysis
            liquidity_score = 0.8 if self.market_context.liquidity_level == "HIGH" else 0.5
            
            # Combined context score
            context_score = (
                trend_score * 0.35 +
                session_score * 0.25 +
                volatility_score * 0.25 +
                liquidity_score * 0.15
            )
            
            return max(0, min(1, context_score))
            
        except Exception as e:
            print(f"❌ Market context analysis error: {e}")
            return 0.5
    
    # ========================================================================================
    # 🚀 HYBRID ENTRY LOGIC - ENHANCED
    # ========================================================================================
    
    def _make_hybrid_entry_decision(self, four_d_analysis: FourDimensionAnalysis) -> EntryDecision:
        """🚀 Hybrid Entry Decision - Multi-factor Analysis"""
        try:
            # ใช้ 4D Analysis เป็นหลัก
            base_confidence = four_d_analysis.overall_score
            
            # เพิ่ม factors เพิ่มเติม
            hybrid_factors = self._calculate_hybrid_factors()
            
            # รวม confidence
            total_confidence = (
                base_confidence * 0.60 +
                hybrid_factors['balance_factor'] * 0.20 +
                hybrid_factors['margin_factor'] * 0.10 +
                hybrid_factors['opportunity_factor'] * 0.10
            )
            
            # ตัดสินใจด้วย Enhanced Threshold (ลดลง)
            min_confidence = self.enhanced_thresholds["min_entry_confidence"]
            
            if total_confidence < min_confidence:
                return EntryDecision.WAIT
            
            # ตัดสินใจทิศทาง - Portfolio Balance First
            direction = self._decide_entry_direction(four_d_analysis, hybrid_factors)
            
            reasoning = (f"4D Score: {four_d_analysis.overall_score:.2f}, "
                        f"Total Confidence: {total_confidence:.2f}, "
                        f"Balance Factor: {hybrid_factors['balance_factor']:.2f}")
            
            print(f"📊 Hybrid Entry Decision: {direction.value}")
            print(f"   Reasoning: {reasoning}")
            
            return direction
            
        except Exception as e:
            print(f"❌ Hybrid entry decision error: {e}")
            return EntryDecision.WAIT
    
    def _calculate_hybrid_factors(self) -> Dict[str, float]:
        """คำนวณ factors เพิ่มเติมสำหรับ Hybrid Logic"""
        try:
            factors = {
                'balance_factor': 0.5,
                'margin_factor': 0.5,
                'opportunity_factor': 0.5,
                'time_factor': 0.5
            }
            
            # Balance Factor - สำคัญมาก
            positions = self.position_manager.get_active_positions()
            if positions:
                buy_count = sum(1 for p in positions if p.get('type') == 0)
                sell_count = sum(1 for p in positions if p.get('type') == 1)
                total_count = len(positions)
                
                if total_count > 0:
                    buy_ratio = buy_count / total_count
                    # สมดุล = ดี, ไม่สมดุล = โอกาสสร้างสมดุล
                    imbalance = abs(buy_ratio - 0.5) * 2  # 0-1
                    factors['balance_factor'] = 0.3 + (imbalance * 0.7)  # ยิ่งไม่สมดุล ยิ่งดี
            
            # Margin Factor
            if self.capital_allocation:
                margin_usage = self.capital_allocation.margin_usage_ratio
                factors['margin_factor'] = max(0, 1 - margin_usage)  # ยิ่งใช้น้อย ยิ่งดี
            
            # Opportunity Factor - เวลาที่เหมาะ
            current_hour = datetime.now().hour
            if 8 <= current_hour <= 16:  # London + NY
                factors['opportunity_factor'] = 0.8
            elif 1 <= current_hour <= 8:  # Asian
                factors['opportunity_factor'] = 0.6
            else:  # Quiet hours
                factors['opportunity_factor'] = 0.4
            
            # Time Factor - ห้ามว่างเกินไป
            time_since_last = (datetime.now() - self.grid_state.last_grid_action).total_seconds()
            if time_since_last > 300:  # 5 นาทีแล้วไม่มีการกระทำ
                factors['time_factor'] = min(time_since_last / 1800, 1.0)  # เพิ่มขึ้นถึง 30 นาที
            
            return factors
            
        except Exception as e:
            print(f"❌ Calculate hybrid factors error: {e}")
            return {'balance_factor': 0.5, 'margin_factor': 0.5, 
                   'opportunity_factor': 0.5, 'time_factor': 0.5}
    
    def _decide_entry_direction(self, four_d_analysis: FourDimensionAnalysis, 
                              hybrid_factors: Dict[str, float]) -> EntryDecision:
        """ตัดสินใจทิศทางการเข้า - Portfolio Balance First"""
        try:
            positions = self.position_manager.get_active_positions()
            
            # Portfolio Balance Analysis - Primary Factor
            buy_count = sum(1 for p in positions if p.get('type') == 0)
            sell_count = sum(1 for p in positions if p.get('type') == 1)
            total_count = len(positions)
            
            # Default direction based on balance
            if total_count == 0:
                # ไม่มีออเดอร์ - ดูเทรนด์
                if self.market_context and self.market_context.trend_direction == "UP":
                    preferred_direction = EntryDecision.BUY_MARKET
                elif self.market_context and self.market_context.trend_direction == "DOWN":
                    preferred_direction = EntryDecision.SELL_MARKET
                else:
                    # Random but smart
                    preferred_direction = EntryDecision.BUY_MARKET if four_d_analysis.overall_score > 0.5 else EntryDecision.SELL_MARKET
            else:
                # มีออเดอร์แล้ว - สร้างสมดุล
                buy_ratio = buy_count / total_count
                
                if buy_ratio < 0.3:  # BUY น้อยเกินไป
                    preferred_direction = EntryDecision.BUY_MARKET
                elif buy_ratio > 0.7:  # BUY มากเกินไป
                    preferred_direction = EntryDecision.SELL_MARKET
                else:
                    # สมดุลแล้ว - ดูโอกาส
                    if four_d_analysis.hedge_opportunity_score > 0.6:
                        # มีโอกาส hedge ดี
                        loss_positions = [p for p in positions if p.get('profit', 0) < 0]
                        if loss_positions:
                            # หาทิศทางที่ต้องการ hedge
                            loss_types = [p.get('type') for p in loss_positions]
                            if 0 in loss_types:  # มี BUY ขาดทุน
                                preferred_direction = EntryDecision.SELL_MARKET
                            else:  # มี SELL ขาดทุน
                                preferred_direction = EntryDecision.BUY_MARKET
                        else:
                            preferred_direction = EntryDecision.BUY_MARKET  # Default
                    else:
                        preferred_direction = EntryDecision.BUY_MARKET  # Default
            
            return preferred_direction
            
        except Exception as e:
            print(f"❌ Entry direction decision error: {e}")
            return EntryDecision.WAIT
    
    # ========================================================================================
    # 🎯 SMART RECOVERY SYSTEM
    # ========================================================================================
    
    def _check_recovery_opportunities(self, four_d_analysis: FourDimensionAnalysis) -> Optional[Dict]:
        """🎯 ตรวจสอบโอกาสการ Recovery"""
        try:
            if four_d_analysis.hedge_opportunity_score < 0.4:
                return None  # ไม่มีโอกาส recovery ดี
            
            positions = self.position_manager.get_active_positions()
            loss_positions = [p for p in positions if p.get('profit', 0) < -10]  # ขาดทุนมากกว่า $10
            
            if not loss_positions:
                return None
            
            # หาโอกาส recovery ที่ดีที่สุด
            best_recovery = None
            best_score = 0
            
            for loss_pos in loss_positions:
                recovery_score = self._calculate_recovery_score(loss_pos, positions, four_d_analysis)
                
                if recovery_score > best_score and recovery_score > 0.6:
                    best_score = recovery_score
                    best_recovery = {
                        'action': 'HEDGE_RECOVERY',
                        'target_position': loss_pos,
                        'recovery_score': recovery_score,
                        'reasoning': f"Recovery opportunity for {loss_pos.get('symbol')} with score {recovery_score:.2f}"
                    }
            
            return best_recovery
            
        except Exception as e:
            print(f"❌ Recovery check error: {e}")
            return None
    
    def _calculate_recovery_score(self, loss_position: Dict, all_positions: List[Dict], 
                                 four_d_analysis: FourDimensionAnalysis) -> float:
        """คำนวณคะแนนโอกาส Recovery"""
        try:
            loss_amount = abs(loss_position.get('profit', 0))
            loss_volume = loss_position.get('volume', 0.01)
            
            # หาออเดอร์กำไรที่เกี่ยวข้อง
            profit_positions = [p for p in all_positions if p.get('profit', 0) > 0]
            
            if not profit_positions:
                return 0.0
            
            # คำนวณ recovery potential
            total_profit = sum(p.get('profit', 0) for p in profit_positions)
            recovery_ratio = min(total_profit / loss_amount, 1.0) if loss_amount > 0 else 0
            
            # Age factor - ออเดอร์เก่า = ลำดับความสำคัญสูง
            age_hours = (datetime.now() - loss_position.get('time', datetime.now())).total_seconds() / 3600
            age_factor = min(age_hours / 24, 1.0)  # มากสุด 1 วัน
            
            # Volume factor - ออเดอร์ใหญ่ = สำคัญมาก
            volume_factor = min(loss_volume / 0.1, 1.0)
            
            # Market condition factor
            market_factor = four_d_analysis.market_context_score
            
            # Combined recovery score
            recovery_score = (
                recovery_ratio * 0.40 +
                age_factor * 0.25 +
                volume_factor * 0.20 +
                market_factor * 0.15
            )
            
            return max(0, min(1, recovery_score))
            
        except Exception as e:
            print(f"❌ Recovery score calculation error: {e}")
            return 0.0
    
    # ========================================================================================
    # ⚡ EXECUTION METHODS - MARKET ORDER FOCUS
    # ========================================================================================
    
    def _execute_entry_decision(self, decision: EntryDecision, four_d_analysis: FourDimensionAnalysis):
        """⚡ Execute Market Order Entry - No Waiting"""
        try:
            if decision == EntryDecision.WAIT:
                return
            
            # คำนวณ lot size แบบ dynamic
            lot_size = self._calculate_dynamic_lot_size(four_d_analysis)
            
            # สร้าง OrderRequest สำหรับ Market Order
            from order_manager import OrderRequest, OrderType, OrderReason
            
            order_request = OrderRequest(
                order_type=OrderType.MARKET_BUY if decision == EntryDecision.BUY_MARKET else OrderType.MARKET_SELL,
                volume=lot_size,
                price=0.0,  # Market price
                reason=OrderReason.PORTFOLIO_BALANCE,
                confidence=four_d_analysis.overall_score,
                reasoning=f"4D AI Entry: {four_d_analysis.recommendation}, Balance Focus",
                max_slippage=20  # ยอมรับ slippage สำหรับ market order
            )
            
            # Execute market order
            result = self.order_manager.place_market_order(order_request)
            
            if result.success:
                print(f"✅ Market {decision.value} executed: {lot_size} lots")
                print(f"   4D Score: {four_d_analysis.overall_score:.3f}")
                print(f"   Reasoning: {order_request.reasoning}")
                
                # Update grid state
                self.grid_state.last_grid_action = datetime.now()
                
                # Track performance
                self._track_decision_performance(decision, four_d_analysis, True)
            else:
                print(f"❌ Market order failed: {result.message}")
                self._track_decision_performance(decision, four_d_analysis, False)
                
        except Exception as e:
            print(f"❌ Execute entry decision error: {e}")
    
    def _execute_recovery_action(self, recovery_action: Dict, four_d_analysis: FourDimensionAnalysis):
        """⚡ Execute Smart Recovery Action"""
        try:
            target_position = recovery_action['target_position']
            
            # วิเคราะห์ recovery strategy
            recovery_strategy = self._plan_recovery_strategy(target_position, four_d_analysis)
            
            if recovery_strategy['action'] == 'HEDGE_ENTRY':
                # วาง hedge order แบบ market
                hedge_direction = recovery_strategy['direction']
                hedge_volume = recovery_strategy['volume']
                
                from order_manager import OrderRequest, OrderType, OrderReason
                
                hedge_order = OrderRequest(
                    order_type=OrderType.MARKET_BUY if hedge_direction == "BUY" else OrderType.MARKET_SELL,
                    volume=hedge_volume,
                    price=0.0,  # Market price
                    reason=OrderReason.RISK_MANAGEMENT,
                    confidence=recovery_action['recovery_score'],
                    reasoning=f"Smart Recovery for position {target_position.get('ticket', 'unknown')}",
                    max_slippage=30
                )
                
                result = self.order_manager.place_market_order(hedge_order)
                
                if result.success:
                    print(f"🎯 Recovery hedge executed: {hedge_volume} {hedge_direction}")
                    print(f"   Target: Position {target_position.get('ticket', 'unknown')}")
                else:
                    print(f"❌ Recovery hedge failed: {result.message}")
            
        except Exception as e:
            print(f"❌ Execute recovery action error: {e}")
    
    def _plan_recovery_strategy(self, target_position: Dict, four_d_analysis: FourDimensionAnalysis) -> Dict:
        """วางแผน Recovery Strategy"""
        try:
            loss_amount = abs(target_position.get('profit', 0))
            loss_type = target_position.get('type', 0)  # 0=BUY, 1=SELL
            loss_volume = target_position.get('volume', 0.01)
            
            # ตัดสินใจทิศทาง hedge (ตรงข้าม)
            hedge_direction = "SELL" if loss_type == 0 else "BUY"
            
            # คำนวณ hedge volume - Dynamic sizing
            hedge_volume = self._calculate_hedge_volume(loss_amount, loss_volume, four_d_analysis)
            
            return {
                'action': 'HEDGE_ENTRY',
                'direction': hedge_direction,
                'volume': hedge_volume,
                'target_recovery': loss_amount * 0.8,  # เป้าหมาย recover 80%
                'confidence': four_d_analysis.hedge_opportunity_score
            }
            
        except Exception as e:
            print(f"❌ Plan recovery strategy error: {e}")
            return {'action': 'WAIT'}
    
    def _calculate_hedge_volume(self, loss_amount: float, loss_volume: float, 
                               four_d_analysis: FourDimensionAnalysis) -> float:
        """คำนวณ Volume สำหรับ Hedge"""
        try:
            # Base volume = ใกล้เคียงกับ loss volume
            base_volume = loss_volume
            
            # ปรับตาม 4D Analysis
            if four_d_analysis.portfolio_safety_score > 0.7:
                volume_multiplier = 1.2  # ปลอดภัย = เพิ่มได้
            elif four_d_analysis.portfolio_safety_score < 0.4:
                volume_multiplier = 0.8  # อันตราย = ลดลง
            else:
                volume_multiplier = 1.0
            
            # ปรับตาม margin available
            if self.capital_allocation and self.capital_allocation.can_expand_grid:
                volume_multiplier *= 1.1
            
            hedge_volume = base_volume * volume_multiplier
            
            # จำกัดขั้นต่ำและสูงสุด
            hedge_volume = max(0.01, min(hedge_volume, 0.1))
            
            return round(hedge_volume, 2)
            
        except Exception as e:
            print(f"❌ Calculate hedge volume error: {e}")
            return 0.01
    
    def _calculate_dynamic_lot_size(self, four_d_analysis: FourDimensionAnalysis) -> float:
        """คำนวณ Lot Size แบบ Dynamic ตาม 4D Analysis"""
        try:
            # Base lot size
            base_lot = 0.01
            
            # ปรับตาม 4D Score
            score_multiplier = 1 + (four_d_analysis.overall_score - 0.5)  # 0.5-1.5
            
            # ปรับตาม Portfolio Safety
            if four_d_analysis.portfolio_safety_score > 0.8:
                safety_multiplier = 1.3  # ปลอดภัย = เพิ่มได้
            elif four_d_analysis.portfolio_safety_score < 0.3:
                safety_multiplier = 0.7  # อันตราย = ลดลง
            else:
                safety_multiplier = 1.0
            
            # ปรับตาม Market Context
            if four_d_analysis.market_context_score > 0.7:
                market_multiplier = 1.2  # ตลาดดี = เพิ่มได้
            else:
                market_multiplier = 0.9
            
            # คำนวณ lot สุดท้าย
            final_lot = base_lot * score_multiplier * safety_multiplier * market_multiplier
            
            # จำกัดขอบเขต
            final_lot = max(0.01, min(final_lot, 0.05))  # ขั้นต่ำ 0.01, สูงสุด 0.05
            
            return round(final_lot, 2)
            
        except Exception as e:
            print(f"❌ Dynamic lot size calculation error: {e}")
            return 0.01
    
    # ========================================================================================
    # 📊 CONTEXT UPDATE METHODS
    # ========================================================================================
    
    def _update_market_context(self):
        """อัปเดตบริบทตลาด"""
        try:
            if not self.market_analyzer:
                return
            
            # ดึงข้อมูลตลาดล่าสุด
            market_data = self.market_analyzer.get_comprehensive_analysis()
            
            if market_data:
                self.last_market_data = market_data
                
                # สร้าง MarketContext
                self.market_context = MarketContext(
                    session=self._detect_market_session(),
                    volatility_level=market_data.get('volatility', {}).get('level', 'MEDIUM'),
                    trend_direction=market_data.get('trend', {}).get('direction', 'SIDEWAYS'),
                    trend_strength=market_data.get('trend', {}).get('strength', 0.5),
                    liquidity_level=market_data.get('liquidity', {}).get('level', 'MEDIUM'),
                    spread_condition=market_data.get('spread', {}).get('condition', 'NORMAL'),
                    momentum=market_data.get('momentum', {}).get('value', 0.0)
                )
                
        except Exception as e:
            print(f"❌ Update market context error: {e}")
    
    def _update_capital_allocation(self):
        """อัปเดตการจัดสรรเงินทุน"""
        try:
            if not self.position_manager:
                return
            
            # ดึงข้อมูล account
            account_info = self.position_manager.get_account_info()
            
            if account_info:
                self.capital_allocation = CapitalAllocation(
                    total_balance=account_info.get('balance', 0),
                    available_margin=account_info.get('margin', 0),
                    used_margin=account_info.get('margin_used', 0),
                    free_margin=account_info.get('margin_free', 0),
                    max_grid_allocation=0.8,  # ใช้ 80% สำหรับกริด
                    optimal_grid_size=self._calculate_optimal_grid_size(account_info),
                    risk_budget=self._calculate_risk_budget(account_info)
                )
                
        except Exception as e:
            print(f"❌ Update capital allocation error: {e}")
    
    def _detect_market_session(self) -> MarketSession:
        """ตรวจจับเซสชันตลาดปัจจุบัน"""
        try:
            current_hour = datetime.now().hour
            
            # GMT+0 based sessions
            if 0 <= current_hour <= 3:
                return MarketSession.ASIAN
            elif 7 <= current_hour <= 11:
                return MarketSession.LONDON  
            elif 13 <= current_hour <= 17:
                return MarketSession.NEW_YORK
            elif 11 <= current_hour <= 13:
                return MarketSession.OVERLAP  # London-NY overlap
            else:
                return MarketSession.QUIET
                
        except Exception as e:
            print(f"❌ Detect market session error: {e}")
            return MarketSession.QUIET
    
    def _calculate_optimal_grid_size(self, account_info: Dict) -> int:
        """คำนวณขนาดกริดที่เหมาะสม"""
        try:
            free_margin = account_info.get('margin_free', 0)
            
            # คำนวณจากการใช้ margin ต่อออเดอร์
            margin_per_order = 50  # Estimate $50 margin per 0.01 lot
            max_orders = int(free_margin / margin_per_order * 0.7)  # ใช้ 70% ของที่มี
            
            # จำกัดขอบเขต
            optimal_size = max(5, min(max_orders, 25))
            
            return optimal_size
            
        except Exception as e:
            print(f"❌ Calculate optimal grid size error: {e}")
            return 10  # Default
    
    def _calculate_risk_budget(self, account_info: Dict) -> float:
        """คำนวณงบความเสี่ยงที่เหลือ"""
        try:
            balance = account_info.get('balance', 0)
            used_margin = account_info.get('margin_used', 0)
            
            # Risk budget = % ของ balance ที่ยังไม่ได้ใช้
            max_risk_percent = 0.05  # 5% ของ balance
            max_risk_amount = balance * max_risk_percent
            
            # ประมาณการความเสี่ยงปัจจุบัน (จาก margin ที่ใช้)
            current_risk_estimate = used_margin * 0.1  # Assume 10% of margin as risk
            
            remaining_risk_budget = max(0, max_risk_amount - current_risk_estimate)
            
            return remaining_risk_budget
            
        except Exception as e:
            print(f"❌ Calculate risk budget error: {e}")
            return 0.0
    
    # ========================================================================================
    # 📈 PERFORMANCE & MAINTENANCE
    # ========================================================================================
    
    def _track_decision_performance(self, decision: EntryDecision, 
                                  four_d_analysis: FourDimensionAnalysis, success: bool):
        """ติดตามประสิทธิภาพการตัดสินใจ"""
        try:
            decision_record = {
                'timestamp': datetime.now(),
                'decision': decision.value,
                'four_d_score': four_d_analysis.overall_score,
                'success': success,
                'market_context': self.market_context.__dict__ if self.market_context else {},
                'hybrid_factors': self._calculate_hybrid_factors()
            }
            
            # เพิ่มใน history
            self.decision_history.append(decision_record)
            self.recent_decisions.append(decision_record)
            
            # อัปเดต rule performance
            rule_key = f"4D_HYBRID_{decision.value}"
            perf = self.rule_performances[rule_key]
            
            perf['total_count'] += 1
            if success:
                perf['success_count'] += 1
            
            perf['avg_confidence'] = (
                (perf['avg_confidence'] * (perf['total_count'] - 1) + 
                 four_d_analysis.overall_score) / perf['total_count']
            )
            
            perf['avg_4d_score'] = (
                (perf.get('avg_4d_score', 0) * (perf['total_count'] - 1) + 
                 four_d_analysis.overall_score) / perf['total_count']
            )
            
            perf['last_updated'] = datetime.now()
            
            # คำนวณ success rate
            success_rate = perf['success_count'] / perf['total_count']
            print(f"📊 {rule_key} Performance: {success_rate:.1%} ({perf['success_count']}/{perf['total_count']})")
            
        except Exception as e:
            print(f"❌ Track decision performance error: {e}")
    
    def _update_performance_tracking(self, four_d_analysis: FourDimensionAnalysis):
        """อัปเดตการติดตามประสิทธิภาพ"""
        try:
            if not self.performance_tracker:
                return
            
            # ส่งข้อมูล 4D Analysis ให้ performance tracker
            performance_data = {
                'timestamp': datetime.now(),
                'four_d_overall_score': four_d_analysis.overall_score,
                'position_value_score': four_d_analysis.position_value_score,
                'portfolio_safety_score': four_d_analysis.portfolio_safety_score,
                'hedge_opportunity_score': four_d_analysis.hedge_opportunity_score,
                'market_context_score': four_d_analysis.market_context_score,
                'recommendation': four_d_analysis.recommendation,
                'grid_phase': self.grid_state.current_phase.value,
                'trading_mode': self.current_mode.value
            }
            
            self.performance_tracker.log_4d_analysis(performance_data)
            
        except Exception as e:
            print(f"❌ Update performance tracking error: {e}")
    
    def _maintain_grid_quality(self):
        """บำรุงรักษาคุณภาพกริด"""
        try:
            # เช็คควรทำ grid maintenance หรือไม่
            time_since_last = (datetime.now() - self.last_grid_analysis_time).total_seconds()
            
            if time_since_last < self.grid_analysis_interval:
                return
            
            # วิเคราะห์คุณภาพกริดปัจจุบัน
            grid_quality = self._analyze_grid_quality()
            
            # อัปเดต grid state
            self.grid_state.quality_score = grid_quality['overall_score']
            self.grid_state.spacing_efficiency = grid_quality['spacing_efficiency']
            
            # ตัดสินใจการบำรุงรักษา
            if grid_quality['overall_score'] < 0.4:
                print(f"⚠️ Grid quality low: {grid_quality['overall_score']:.2f}")
                self._suggest_grid_improvements(grid_quality)
            
            self.last_grid_analysis_time = datetime.now()
            
        except Exception as e:
            print(f"❌ Grid maintenance error: {e}")
    
    def _analyze_grid_quality(self) -> Dict:
        """วิเคราะห์คุณภาพกริดปัจจุบัน"""
        try:
            positions = self.position_manager.get_active_positions()
            
            if not positions:
                return {
                    'overall_score': 0.5,
                    'spacing_efficiency': 0.5,
                    'balance_score': 1.0,
                    'coverage_score': 0.0
                }
            
            # Balance score
            buy_count = sum(1 for p in positions if p.get('type') == 0)
            sell_count = len(positions) - buy_count
            balance_score = 1 - abs(buy_count - sell_count) / len(positions)
            
            # Spacing efficiency
            if len(positions) > 1:
                prices = [p.get('price_open', 0) for p in positions]
                prices.sort()
                spacings = [prices[i+1] - prices[i] for i in range(len(prices)-1)]
                avg_spacing = np.mean(spacings) if spacings else 0
                spacing_std = np.std(spacings) if len(spacings) > 1 else 0
                spacing_efficiency = max(0, 1 - (spacing_std / avg_spacing)) if avg_spacing > 0 else 0.5
            else:
                spacing_efficiency = 1.0
            
            # Coverage score - มีการกระจายในช่วงราคาที่เหมาะสม
            price_range = max(prices) - min(prices) if len(prices) > 1 else 0
            target_range = 500  # 500 points coverage target
            coverage_score = min(price_range / target_range, 1.0)
            
            # Overall score
            overall_score = (balance_score * 0.4 + spacing_efficiency * 0.4 + coverage_score * 0.2)
            
            return {
                'overall_score': overall_score,
                'spacing_efficiency': spacing_efficiency,
                'balance_score': balance_score,
                'coverage_score': coverage_score
            }
            
        except Exception as e:
            print(f"❌ Grid quality analysis error: {e}")
            return {'overall_score': 0.5, 'spacing_efficiency': 0.5, 
                   'balance_score': 0.5, 'coverage_score': 0.5}
    
    def _suggest_grid_improvements(self, quality_analysis: Dict):
        """แนะนำการปรับปรุงกริด"""
        try:
            suggestions = []
            
            if quality_analysis['balance_score'] < 0.6:
                suggestions.append("Portfolio needs rebalancing - consider opposite direction entries")
            
            if quality_analysis['spacing_efficiency'] < 0.5:
                suggestions.append("Spacing too irregular - consider spacing optimization")
            
            if quality_analysis['coverage_score'] < 0.3:
                suggestions.append("Grid coverage too narrow - consider expansion")
            
            if suggestions:
                print("💡 Grid Improvement Suggestions:")
                for suggestion in suggestions:
                    print(f"   • {suggestion}")
                    
        except Exception as e:
            print(f"❌ Grid improvement suggestions error: {e}")
    
    # ========================================================================================
    # 📊 STATUS & REPORTING METHODS
    # ========================================================================================
    
    def get_engine_status(self) -> Dict:
        """ดึงสถานะ Engine แบบละเอียด"""
        try:
            status = {
                'is_running': self.is_running,
                'trading_mode': self.current_mode.value,
                'grid_phase': self.grid_state.current_phase.value,
                'last_4d_analysis': self.last_4d_analysis.__dict__ if self.last_4d_analysis else {},
                'grid_quality': self.grid_state.quality_score,
                'total_decisions': len(self.decision_history),
                'recent_decisions_count': len(self.recent_decisions),
                'capital_allocation': self.capital_allocation.__dict__ if self.capital_allocation else {},
                'market_context': self.market_context.__dict__ if self.market_context else {},
                'performance_summary': self._get_performance_summary()
            }
            
            return status
            
        except Exception as e:
            print(f"❌ Get engine status error: {e}")
            return {'is_running': False, 'error': str(e)}
    
    def _get_performance_summary(self) -> Dict:
        """สรุปประสิทธิภาพแบบย่อ"""
        try:
            if not self.rule_performances:
                return {"message": "No performance data available"}
            
            summary = {}
            total_decisions = 0
            total_successes = 0
            
            for rule_name, perf in self.rule_performances.items():
                rule_total = perf.get("total_count", 0)
                rule_success = perf.get("success_count", 0)
                rule_4d_score = perf.get("avg_4d_score", 0)
                
                if rule_total > 0:
                    summary[rule_name] = {
                        "success_rate": rule_success / rule_total,
                        "total_decisions": rule_total,
                        "avg_4d_score": rule_4d_score
                    }
                    
                total_decisions += rule_total
                total_successes += rule_success
            
            # Overall summary
            overall_success_rate = total_successes / total_decisions if total_decisions > 0 else 0
            
            summary["overall"] = {
                "success_rate": overall_success_rate,
                "total_decisions": total_decisions,
                "engine_uptime": (datetime.now() - self.grid_state.last_grid_action).total_seconds() / 3600
            }
            
            return summary
            
        except Exception as e:
            print(f"❌ Performance summary error: {e}")
            return {"error": str(e)}
    
    # ========================================================================================
    # 💾 PERSISTENCE METHODS
    # ========================================================================================
    
    def save_performance_data(self, filepath: str = "performance_data_4d.json"):
        """บันทึกข้อมูลประสิทธิภาพ Enhanced 4D"""
        try:
            performance_data = {
                "engine_version": "4D_AI_Enhanced",
                "last_saved": datetime.now().isoformat(),
                "rule_performances": dict(self.rule_performances),
                "total_decisions": len(self.decision_history),
                "grid_state": {
                    "phase": self.grid_state.current_phase.value,
                    "quality_score": self.grid_state.quality_score,
                    "balance_ratio": self.grid_state.grid_balance_ratio,
                    "total_orders": self.grid_state.total_orders
                },
                "enhanced_thresholds": self.enhanced_thresholds,
                "recent_4d_analyses": [
                    {
                        "timestamp": datetime.now().isoformat(),
                        "overall_score": analysis.overall_score,
                        "recommendation": analysis.recommendation,
                        "position_value": analysis.position_value_score,
                        "portfolio_safety": analysis.portfolio_safety_score,
                        "hedge_opportunity": analysis.hedge_opportunity_score,
                        "market_context": analysis.market_context_score
                    }
                    for analysis in list(self.analysis_history)[-10:]  # เก็บ 10 อันล่าสุด
                ]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(performance_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Enhanced 4D performance data saved to {filepath}")
            
        except Exception as e:
            print(f"❌ Save performance data error: {e}")
    
    def load_performance_data(self, filepath: str = "performance_data_4d.json"):
        """โหลดข้อมูลประสิทธิภาพ Enhanced 4D"""
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
            
            # โหลด enhanced thresholds
            if "enhanced_thresholds" in performance_data:
                self.enhanced_thresholds.update(performance_data["enhanced_thresholds"])
            
            # โหลด grid state
            if "grid_state" in performance_data:
                grid_data = performance_data["grid_state"]
                self.grid_state.quality_score = grid_data.get("quality_score", 0.0)
                self.grid_state.grid_balance_ratio = grid_data.get("balance_ratio", 0.5)
            
            print(f"📁 Enhanced 4D performance data loaded from {filepath}")
            print(f"   Loaded {len(self.rule_performances)} rule performances")
            
        except Exception as e:
            print(f"❌ Load performance data error: {e}")
    
    # ========================================================================================
    # 🔧 UTILITY & HELPER METHODS
    # ========================================================================================
    
    def get_4d_analysis_summary(self) -> str:
        """สรุป 4D Analysis ล่าสุด"""
        try:
            if not self.last_4d_analysis:
                return "No 4D analysis available"
            
            analysis = self.last_4d_analysis
            
            summary = f"""
🧠 4D AI Analysis Summary:
├── Overall Score: {analysis.overall_score:.3f} ({analysis.recommendation})
├── 📊 Position Value: {analysis.position_value_score:.3f} (30% weight)
├── 🛡️ Portfolio Safety: {analysis.portfolio_safety_score:.3f} (25% weight)  
├── 🎯 Hedge Opportunity: {analysis.hedge_opportunity_score:.3f} (25% weight)
└── 🌍 Market Context: {analysis.market_context_score:.3f} (20% weight)

🎮 Trading Context:
├── Mode: {self.current_mode.value}
├── Grid Phase: {self.grid_state.current_phase.value}
├── Grid Quality: {self.grid_state.quality_score:.3f}
└── Balance Ratio: {self.grid_state.grid_balance_ratio:.3f}
            """.strip()
            
            return summary
            
        except Exception as e:
            print(f"❌ 4D analysis summary error: {e}")
            return "Error generating 4D analysis summary"
    
    def get_recent_decisions_summary(self, count: int = 5) -> List[Dict]:
        """สรุปการตัดสินใจล่าสุด"""
        try:
            recent = list(self.recent_decisions)[-count:] if self.recent_decisions else []
            
            summary = []
            for decision in recent:
                summary.append({
                    'time': decision['timestamp'].strftime('%H:%M:%S'),
                    'decision': decision['decision'],
                    '4d_score': f"{decision['four_d_score']:.3f}",
                    'success': "✅" if decision['success'] else "❌",
                    'context': decision.get('market_context', {}).get('session', 'UNKNOWN')
                })
            
            return summary
            
        except Exception as e:
            print(f"❌ Recent decisions summary error: {e}")
            return []
    
    def reset_performance_data(self):
        """รีเซ็ตข้อมูลประสิทธิภาพทั้งหมด"""
        try:
            self.rule_performances = defaultdict(lambda: {
                "success_count": 0,
                "total_count": 0,
                "avg_confidence": 0.0,
                "avg_4d_score": 0.0,
                "last_updated": datetime.now(),
                "profit_factor": 0.0,
                "recovery_success_rate": 0.0
            })
            
            self.decision_history = []
            self.recent_decisions = deque(maxlen=100)
            self.analysis_history = deque(maxlen=100)
            
            print("🔄 Enhanced 4D performance data reset complete")
            
        except Exception as e:
            print(f"❌ Reset performance data error: {e}")
    
    def adjust_thresholds_from_performance(self):
        """ปรับ thresholds จากประสิทธิภาพ - Adaptive Learning"""
        try:
            if len(self.decision_history) < 20:
                return  # ข้อมูลไม่พอ
            
            # วิเคราะห์ประสิทธิภาพล่าสุด 20 ครั้ง
            recent_performance = self.decision_history[-20:]
            success_rate = sum(1 for d in recent_performance if d['success']) / len(recent_performance)
            avg_4d_score = np.mean([d['four_d_score'] for d in recent_performance])
            
            # ปรับ min_entry_confidence
            if success_rate > 0.7 and avg_4d_score > 0.4:
                # ประสิทธิภาพดี = ลด threshold (เข้าง่ายขึ้น)
                adjustment = -0.02
            elif success_rate < 0.4:
                # ประสิทธิภาพแย่ = เพิ่ม threshold (เข้ายากขึ้น)
                adjustment = 0.02
            else:
                adjustment = 0
            
            old_threshold = self.enhanced_thresholds["min_entry_confidence"]
            new_threshold = max(0.1, min(0.5, old_threshold + adjustment))
            
            if abs(adjustment) > 0:
                self.enhanced_thresholds["min_entry_confidence"] = new_threshold
                print(f"🔧 Threshold adjusted: {old_threshold:.3f} → {new_threshold:.3f}")
                print(f"   Based on success rate: {success_rate:.1%}")
            
        except Exception as e:
            print(f"❌ Threshold adjustment error: {e}")
    
    # ========================================================================================
    # 🎯 ENHANCED API METHODS
    # ========================================================================================
    
    def force_entry_opportunity(self, direction: str = "AUTO") -> bool:
        """บังคับสร้างโอกาสเข้าตลาด - Enhanced"""
        try:
            print(f"🎯 Force entry opportunity: {direction}")
            
            # ทำ 4D Analysis ทันที
            four_d_analysis = self._perform_4d_analysis()
            
            # ตัดสินใจทิศทาง
            if direction == "AUTO":
                entry_decision = self._decide_entry_direction(four_d_analysis, self._calculate_hybrid_factors())
            elif direction == "BUY":
                entry_decision = EntryDecision.BUY_MARKET
            elif direction == "SELL":
                entry_decision = EntryDecision.SELL_MARKET
            else:
                print(f"❌ Invalid direction: {direction}")
                return False
            
            # Execute ทันที
            if entry_decision != EntryDecision.WAIT:
                self._execute_entry_decision(entry_decision, four_d_analysis)
                return True
            else:
                print("⚠️ 4D Analysis recommends WAIT")
                return False
                
        except Exception as e:
            print(f"❌ Force entry opportunity error: {e}")
            return False
    
    def force_recovery_scan(self) -> bool:
        """บังคับสแกนหาโอกาส Recovery"""
        try:
            print("🔍 Force recovery scan...")
            
            four_d_analysis = self._perform_4d_analysis()
            recovery_action = self._check_recovery_opportunities(four_d_analysis)
            
            if recovery_action:
                self._execute_recovery_action(recovery_action, four_d_analysis)
                print(f"✅ Recovery action executed: {recovery_action['action']}")
                return True
            else:
                print("ℹ️ No recovery opportunities found")
                return False
                
        except Exception as e:
            print(f"❌ Force recovery scan error: {e}")
            return False
    
    def get_portfolio_recommendations(self) -> List[str]:
        """ดึงคำแนะนำสำหรับ Portfolio"""
        try:
            if not self.last_4d_analysis:
                return ["Perform 4D analysis first"]
            
            recommendations = []
            analysis = self.last_4d_analysis
            
            # Position Value recommendations
            if analysis.position_value_score < 0.4:
                recommendations.append("Consider closing underperforming old positions")
            
            # Portfolio Safety recommendations
            if analysis.portfolio_safety_score < 0.3:
                recommendations.append("CRITICAL: Reduce margin usage immediately")
            elif analysis.portfolio_safety_score < 0.5:
                recommendations.append("Warning: Monitor margin usage closely")
            
            # Hedge Opportunity recommendations
            if analysis.hedge_opportunity_score > 0.7:
                recommendations.append("Excellent hedge opportunities available - consider recovery trades")
            elif analysis.hedge_opportunity_score > 0.5:
                recommendations.append("Moderate hedge opportunities - selective recovery possible")
            
            # Market Context recommendations
            if analysis.market_context_score > 0.7:
                recommendations.append("Favorable market conditions - good time for expansion")
            elif analysis.market_context_score < 0.3:
                recommendations.append("Unfavorable market - focus on risk management")
            
            # Overall recommendations
            if analysis.overall_score > 0.8:
                recommendations.append("🚀 STRONG CONDITIONS: Aggressive expansion recommended")
            elif analysis.overall_score < 0.3:
                recommendations.append("⚠️ CAUTION MODE: Focus on recovery and risk reduction")
            
            return recommendations if recommendations else ["Portfolio in good condition"]
            
        except Exception as e:
            print(f"❌ Portfolio recommendations error: {e}")
            return ["Error generating recommendations"]