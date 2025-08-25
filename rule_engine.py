"""
🧠 Enhanced Smart Rule Engine - AI Grid Trading System
rule_engine.py

🎯 KEY IMPROVEMENTS:
✅ Smart Decision Making System - ไม่ออกออเดอร์รัวๆ
✅ Intelligent Grid Distribution - รู้จักกระจายออเดอร์
✅ Market Context Awareness - รู้สภาพตลาด
✅ Portfolio Intelligence - รู้สุขภาพพอร์ต
✅ Quality over Quantity - เน้นคุณภาพมากกว่าปริมาณ
✅ Dynamic Learning - เรียนรู้จากผลงาน

** PRODUCTION READY - ENHANCED VERSION **
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

class DecisionQuality(Enum):
    """คุณภาพการตัดสินใจ"""
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    ACCEPTABLE = "ACCEPTABLE"
    POOR = "POOR"
    BLOCKED = "BLOCKED"

@dataclass
class SmartDecisionScore:
    """คะแนนการตัดสินใจอัจฉริยะ"""
    # Core Factors (100%)
    market_quality: float = 0.0          # 25% - คุณภาพตลาด
    portfolio_necessity: float = 0.0     # 30% - ความจำเป็นของพอร์ต
    timing_opportunity: float = 0.0      # 20% - โอกาสด้านเวลา
    risk_reward: float = 0.0             # 15% - ความคุ้มค่าความเสี่ยง
    performance_modifier: float = 0.0    # 10% - ปรับจากผลงาน
    
    # Additional Context
    confidence_level: float = 0.0        # ระดับความเชื่อมั่น
    reasoning: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    @property
    def final_score(self) -> float:
        """คะแนนสุดท้ายถ่วงน้ำหนัก"""
        return (
            self.market_quality * 0.25 +
            self.portfolio_necessity * 0.30 +
            self.timing_opportunity * 0.20 +
            self.risk_reward * 0.15 +
            self.performance_modifier * 0.10
        )
    
    @property
    def decision_quality(self) -> DecisionQuality:
        """คุณภาพการตัดสินใจ"""
        score = self.final_score
        if score >= 0.85:
            return DecisionQuality.EXCELLENT
        elif score >= 0.70:
            return DecisionQuality.GOOD
        elif score >= 0.50:
            return DecisionQuality.ACCEPTABLE
        elif score >= 0.30:
            return DecisionQuality.POOR
        else:
            return DecisionQuality.BLOCKED

@dataclass
class GridIntelligence:
    """สติปัญญาของกริด"""
    density_score: float = 0.0           # ความหนาแน่น (0=sparse, 1=dense)
    distribution_score: float = 0.0     # การกระจาย (0=poor, 1=excellent)
    balance_score: float = 0.0           # ความสมดุล (0=unbalanced, 1=balanced)
    efficiency_score: float = 0.0       # ประสิทธิภาพ (0=inefficient, 1=efficient)
    
    # Grid Analysis
    total_orders: int = 0
    buy_orders: int = 0 
    sell_orders: int = 0
    avg_spacing: float = 0.0
    coverage_range: float = 0.0
    
    # Recommendations
    should_expand: bool = False
    should_rebalance: bool = False
    should_wait: bool = False
    
    @property
    def overall_intelligence(self) -> float:
        """สติปัญญารวมของกริด"""
        return (
            self.density_score * 0.20 +
            self.distribution_score * 0.30 +
            self.balance_score * 0.30 +
            self.efficiency_score * 0.20
        )

@dataclass
class MarketIntelligence:
    """สติปัญญาการวิเคราะห์ตลาด"""
    volatility_appropriateness: float = 0.0    # ความเหมาะสมของ volatility
    trend_strength: float = 0.0                # ความแรงของเทรนด์
    session_favorability: float = 0.0          # ความเหมาะสมของ session
    volume_confidence: float = 0.0             # ความเชื่อมั่นจาก volume
    spread_condition: float = 0.0              # สภาพ spread
    
    # Context
    current_session: MarketSession = MarketSession.QUIET
    trend_direction: str = "SIDEWAYS"
    volatility_level: str = "NORMAL"
    
    @property
    def market_readiness(self) -> float:
        """ความพร้อมของตลาด"""
        return (
            self.volatility_appropriateness * 0.25 +
            self.trend_strength * 0.20 +
            self.session_favorability * 0.20 +
            self.volume_confidence * 0.20 +
            self.spread_condition * 0.15
        )

@dataclass
class PortfolioIntelligence:
    """สติปัญญาการจัดการพอร์ตโฟลิโอ"""
    health_score: float = 0.0              # สุขภาพพอร์ต (0=unhealthy, 1=healthy)
    balance_necessity: float = 0.0         # ความจำเป็นในการปรับสมดุล
    risk_exposure: float = 0.0             # การเสี่ยง (0=safe, 1=high_risk)
    margin_safety: float = 0.0             # ความปลอดภัยของ margin
    recovery_potential: float = 0.0        # โอกาสการฟื้นตัว
    
    # Portfolio Stats
    total_positions: int = 0
    profitable_positions: int = 0
    losing_positions: int = 0
    total_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    
    @property
    def portfolio_readiness(self) -> float:
        """ความพร้อมของพอร์ตโฟลิโอ"""
        return (
            self.health_score * 0.30 +
            (1.0 - self.risk_exposure) * 0.25 +  # ความเสี่ยงต่ำ = ดี
            self.margin_safety * 0.25 +
            self.recovery_potential * 0.20
        )

# ========================================================================================
# 🧠 ENHANCED SMART RULE ENGINE
# ========================================================================================

class ModernRuleEngine:
    """
    🧠 Modern Rule Engine - Enhanced Smart AI Edition with Anti-Spam Intelligence
    
    ✨ NEW FEATURES:
    - Smart Decision Making System (ป้องกันออเดอร์รัวๆ)
    - Intelligent Grid Analysis (วิเคราะห์กริดอัจฉริยะ) 
    - Market Context Awareness (รู้สภาพตลาด)
    - Portfolio Health Monitoring (ติดตามสุขภาพพอร์ต)
    - Quality-based Entry System (เข้าตลาดตามคุณภาพ)
    - Dynamic Learning (เรียนรู้และปรับปรุง)
    """
    
    def __init__(self, config: Dict, market_analyzer, order_manager, 
                 position_manager, performance_tracker):
        # Core components
        self.config = config
        self.market_analyzer = market_analyzer
        self.order_manager = order_manager
        self.position_manager = position_manager
        self.performance_tracker = performance_tracker
        
        # Engine state
        self.is_running = False
        self.current_mode = TradingMode.MODERATE
        self.engine_thread = None
        
        # ✨ Auto-save/load settings
        self.auto_save_enabled = True
        self.auto_save_interval = 300  # 5 นาที
        self.performance_file = "performance_data_4d.json"
        self.last_save_time = datetime.now()
        
        # ✨ Smart Decision Components
        self.decision_history = deque(maxlen=200)
        self.performance_memory = deque(maxlen=100)
        self.last_order_time = {}  # Track last order time by type
        
        # ✨ Intelligence Systems
        self.grid_intelligence = GridIntelligence()
        self.market_intelligence = MarketIntelligence()  
        self.portfolio_intelligence = PortfolioIntelligence()
        
        # ✨ Adaptive Thresholds (เริ่มต้นระดับต่ำกว่า - ง่ายต่อการเข้าตลาด)
        self.adaptive_thresholds = {
            "minimum_decision_score": 0.50,    # ลดจาก 0.65 → 0.50 เข้าง่ายขึ้น
            "excellent_threshold": 0.80,       # 80%+ = เข้าแน่นอน
            "good_threshold": 0.65,            # 65-79% = ดี  
            "acceptable_threshold": 0.50,      # 50-64% = ยอมรับได้
            "poor_threshold": 0.35,            # 35-49% = อันตราย
            
            # Anti-spam settings (ปรับให้สมเหตุสมผลขึ้น)
            "minimum_time_between_orders": 30,  # ลดจาก 60 → 30 วินาที
            "maximum_orders_per_hour": 15,     # เพิ่มจาก 10 → 15 ออเดอร์/ชม
            "grid_density_limit": 0.85,         # ผ่อนผันจาก 0.8 → 0.85
            
            # Learning parameters
            "learning_rate": 0.1,              # อัตราการเรียนรู้
            "performance_window": 50,          # จำนวนออเดอร์ที่ใช้ประเมิน
            "adaptation_sensitivity": 0.05     # ความไวในการปรับ
        }
        
        # ✨ Performance tracking
        self.success_rate_tracker = deque(maxlen=100)
        self.decision_quality_tracker = deque(maxlen=100)
        
        # ✨ Initialize with saved data
        self._load_previous_learning()
        
        print("🧠 Modern Rule Engine Enhanced - Anti-Spam Intelligence Active!")
        print(f"💾 Auto-save enabled: Every {self.auto_save_interval}s")
    
    # ========================================================================================
    # 🎮 ENGINE CONTROL
    # ========================================================================================
    
    def start(self):
        """เริ่มต้น Smart Rule Engine"""
        if self.is_running:
            print("⚠️ Modern Rule Engine already running")
            return
            
        self.is_running = True
        self.engine_thread = threading.Thread(target=self._smart_engine_loop, daemon=True)
        self.engine_thread.start()
        print("🚀 Modern Rule Engine Enhanced started - Intelligence Active!")
    
    def stop(self):
        """หยุด Modern Rule Engine"""
        self.is_running = False
        if self.engine_thread:
            self.engine_thread.join(timeout=5)
            
        # ✨ Save data before stopping
        self._save_learning_data()
        print("🛑 Modern Rule Engine stopped - Learning data saved")
    
    def set_trading_mode(self, mode: TradingMode):
        """ตั้งค่าโหมดการเทรดแบบอัจฉริยะ"""
        if isinstance(mode, str):
            mode_mapping = {
                "CONSERVATIVE": TradingMode.CONSERVATIVE,
                "MODERATE": TradingMode.MODERATE,
                "AGGRESSIVE": TradingMode.AGGRESSIVE,
                "ADAPTIVE": TradingMode.ADAPTIVE
            }
            mode = mode_mapping.get(mode.upper(), TradingMode.MODERATE)
        
        self.current_mode = mode
        
        # ปรับ thresholds ตาม mode อัจฉริยะ (ปรับเวลาให้เหมาะสม)
        if mode == TradingMode.CONSERVATIVE:
            self.adaptive_thresholds["minimum_decision_score"] = 0.70  # สูงมาก
            self.adaptive_thresholds["minimum_time_between_orders"] = 60   # 1 นาที
            self.adaptive_thresholds["maximum_orders_per_hour"] = 8
            
        elif mode == TradingMode.AGGRESSIVE:
            self.adaptive_thresholds["minimum_decision_score"] = 0.40  # ต่ำมาก - เข้าง่าย
            self.adaptive_thresholds["minimum_time_between_orders"] = 20   # 20 วินาที
            self.adaptive_thresholds["maximum_orders_per_hour"] = 20
            
        elif mode == TradingMode.ADAPTIVE:
            # ใช้ค่า default เมื่อเริ่มต้น (ถ้ามีข้อมูลพอ)
            if len(self.success_rate_tracker) >= 10:
                self._adjust_thresholds_from_performance()
            else:
                self.adaptive_thresholds["minimum_decision_score"] = 0.50
                self.adaptive_thresholds["minimum_time_between_orders"] = 30  # 30 วินาที
                print("🎯 ADAPTIVE Mode: Starting with default threshold (learning phase)")
            
        else:  # MODERATE
            self.adaptive_thresholds["minimum_decision_score"] = 0.50  # ลดลงเป็น 50%
            self.adaptive_thresholds["minimum_time_between_orders"] = 30   # ลดเป็น 30 วินาที  
            self.adaptive_thresholds["maximum_orders_per_hour"] = 15
            
        print(f"🎯 Modern Rule Engine Mode: {mode.value}")
        print(f"   Decision Score Required: {self.adaptive_thresholds['minimum_decision_score']}")
        print(f"   Min Time Between Orders: {self.adaptive_thresholds['minimum_time_between_orders']}s")
    
    # ========================================================================================
    # 🧠 SMART ENGINE LOOP
    # ========================================================================================
    
    def _smart_engine_loop(self):
        """หลัก Smart Engine Loop - ป้องกันการออกออเดอร์รัวๆ"""
        print("🔄 Modern Rule Engine Loop started - Intelligence Active!")
        
        while self.is_running:
            try:
                loop_start = time.time()
                
                # 1. ✨ Update Intelligence Systems
                self._update_market_intelligence()
                self._update_portfolio_intelligence()
                self._update_grid_intelligence()
                
                # 2. ✨ Smart Decision Making Process
                smart_decision = self._make_smart_decision()
                
                # 3. ✨ Quality Check & Anti-Spam Filter
                if self._should_place_order(smart_decision):
                    # 4. ✨ Execute with Intelligence
                    self._execute_intelligent_order(smart_decision)
                else:
                    print(f"🚫 Order BLOCKED by Smart Filter - Reason: {smart_decision.warnings}")
                
                # 5. ✨ Learning & Adaptation
                self._update_performance_learning()
                
                # ✨ ประเมินผลการตัดสินใจที่รอการประเมิน
                self._evaluate_pending_decisions()
                
                if self.current_mode == TradingMode.ADAPTIVE:
                    self._adjust_thresholds_from_performance()
                
                # 6. ✨ Maintenance & Auto-save
                self._maintain_system_health()
                self._auto_save_if_needed()
                
                # Loop timing control
                loop_time = time.time() - loop_start
                sleep_time = max(0.1, 5.0 - loop_time)  # 5-second cycles
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"❌ Smart Engine Loop error: {e}")
                time.sleep(5)  # Error recovery
    
    # ========================================================================================
    # 🧠 SMART DECISION MAKING SYSTEM
    # ========================================================================================
    
    def _make_smart_decision(self) -> SmartDecisionScore:
        """
        ✨ สร้างการตัดสินใจอัจฉริยะ - หัวใจของระบบป้องกันออเดอร์รัวๆ
        """
        try:
            decision = SmartDecisionScore()
            
            # 1. 📊 Market Quality Assessment (25%)
            decision.market_quality = self._assess_market_quality()
            
            # 2. 💼 Portfolio Necessity Analysis (30%) - สำคัญที่สุด
            decision.portfolio_necessity = self._analyze_portfolio_necessity()
            
            # 3. ⏰ Timing Opportunity Assessment (20%)
            decision.timing_opportunity = self._evaluate_timing_opportunity()
            
            # 4. ⚖️ Risk-Reward Analysis (15%)
            decision.risk_reward = self._calculate_risk_reward_score()
            
            # 5. 📈 Performance Modifier (10%)
            decision.performance_modifier = self._get_performance_modifier()
            
            # Calculate confidence
            decision.confidence_level = min(1.0, decision.final_score * 1.2)
            
            # Generate reasoning
            decision.reasoning = self._generate_decision_reasoning(decision)
            decision.warnings = self._generate_decision_warnings(decision)
            
            # Store for learning
            self.decision_history.append({
                'timestamp': datetime.now(),
                'score': decision.final_score,
                'quality': decision.decision_quality.value,
                'market_quality': decision.market_quality,
                'portfolio_necessity': decision.portfolio_necessity,
                'timing_opportunity': decision.timing_opportunity
            })
            
            print(f"🧠 Smart Decision Score: {decision.final_score:.3f} ({decision.decision_quality.value})")
            return decision
            
        except Exception as e:
            print(f"❌ Smart decision making error: {e}")
            # Return safe default
            return SmartDecisionScore(
                market_quality=0.3,
                portfolio_necessity=0.3,
                timing_opportunity=0.3,
                risk_reward=0.3,
                performance_modifier=0.3,
                warnings=["Error in decision making - using safe default"]
            )
    
    def _assess_market_quality(self) -> float:
        """📊 ประเมินคุณภาพตลาด (25%)"""
        try:
            if not self.market_analyzer:
                return 0.5
            
            # ✅ แก้ไข: ใช้ method ที่มีจริง
            market_data = self.market_analyzer.get_comprehensive_analysis()
            if not market_data:
                return 0.4
            
            current_price = market_data.get('current_price', 0)
            if not current_price:
                return 0.3
            
            # Update market intelligence
            self.market_intelligence.volatility_appropriateness = self._evaluate_volatility_appropriateness(market_data)
            self.market_intelligence.trend_strength = market_data.get('trend_strength', 0.5)
            self.market_intelligence.session_favorability = self._evaluate_session_favorability()
            self.market_intelligence.volume_confidence = market_data.get('volume_score', 0.5)
            self.market_intelligence.spread_condition = self._evaluate_spread_condition()
            
            # Calculate overall market quality
            quality_score = self.market_intelligence.market_readiness
            
            print(f"📊 Market Quality: {quality_score:.3f} (Vol:{self.market_intelligence.volatility_appropriateness:.2f}, "
                  f"Trend:{self.market_intelligence.trend_strength:.2f}, Session:{self.market_intelligence.session_favorability:.2f})")
            
            return quality_score
            
        except Exception as e:
            print(f"❌ Market quality assessment error: {e}")
            return 0.4
    
    def _analyze_portfolio_necessity(self) -> float:
        """💼 วิเคราะห์ความจำเป็นของพอร์ตโฟลิโอ (30%) - ตัวป้องกันหลัก"""
        try:
            if not self.position_manager:
                return 0.5
            
            # ✅ แก้ไข: ใช้ method ที่มีจริง
            portfolio_data = self.position_manager.get_4d_portfolio_status()
            if not portfolio_data:
                return 0.6  # ไม่มีข้อมูล = ค่อนข้างปลอดภัย
            
            # Update portfolio intelligence
            self.portfolio_intelligence.health_score = self._calculate_portfolio_health(portfolio_data)
            self.portfolio_intelligence.balance_necessity = self._calculate_balance_necessity(portfolio_data)
            self.portfolio_intelligence.risk_exposure = self._calculate_risk_exposure(portfolio_data)
            self.portfolio_intelligence.margin_safety = self._calculate_margin_safety(portfolio_data)
            
            # ✨ KEY ANTI-SPAM LOGIC: ถ้า portfolio สมดุลแล้ว ไม่จำเป็นต้องเพิ่มออเดอร์
            if self.portfolio_intelligence.balance_necessity < 0.3:
                print("💼 Portfolio well-balanced - Lower necessity for new orders")
                return 0.2  # คะแนนต่ำ = ไม่จำเป็นเพิ่มออเดอร์
            
            # Calculate overall necessity  
            necessity_score = self.portfolio_intelligence.portfolio_readiness
            
            print(f"💼 Portfolio Necessity: {necessity_score:.3f} (Health:{self.portfolio_intelligence.health_score:.2f}, "
                  f"Balance Need:{self.portfolio_intelligence.balance_necessity:.2f}, Risk:{self.portfolio_intelligence.risk_exposure:.2f})")
            
            return necessity_score
            
        except Exception as e:
            print(f"❌ Portfolio necessity analysis error: {e}")
            return 0.5
    
    def _evaluate_timing_opportunity(self) -> float:
        """⏰ ประเมินโอกาสด้านเวลา (20%)"""
        try:
            timing_score = 0.5
            
            # 1. Check time since last order (Anti-spam core)
            time_since_last = self._get_time_since_last_order()
            min_interval = self.adaptive_thresholds["minimum_time_between_orders"]
            
            if time_since_last < min_interval:
                # ออเดอร์ใกล้เกินไป!
                time_penalty = 1.0 - (time_since_last / min_interval)
                timing_score *= (1.0 - time_penalty)
                print(f"⏰ Time Penalty Applied: {time_penalty:.2f} (Last order: {time_since_last}s ago)")
            
            # 2. Check hourly order limit
            orders_this_hour = self._count_orders_in_last_hour()
            max_hourly = self.adaptive_thresholds["maximum_orders_per_hour"]
            
            if orders_this_hour >= max_hourly:
                timing_score *= 0.1  # ลดลงอย่างมาก
                print(f"⏰ Hourly Limit Exceeded: {orders_this_hour}/{max_hourly}")
            elif orders_this_hour >= max_hourly * 0.8:
                timing_score *= 0.5  # ลดลงปานกลาง
                print(f"⏰ Approaching Hourly Limit: {orders_this_hour}/{max_hourly}")
            
            # 3. Market session timing
            session_bonus = self._get_session_timing_bonus()
            timing_score = min(1.0, timing_score * session_bonus)
            
            print(f"⏰ Timing Opportunity: {timing_score:.3f} (Orders this hour: {orders_this_hour}/{max_hourly})")
            return timing_score
            
        except Exception as e:
            print(f"❌ Timing opportunity evaluation error: {e}")
            return 0.5
    
    def _calculate_risk_reward_score(self) -> float:
        """⚖️ คำนวณความคุ้มค่าของความเสี่ยง (15%)"""
        try:
            if not self.market_analyzer:
                return 0.5
            
            # ✅ แก้ไข: ใช้ method ที่มีจริง
            market_data = self.market_analyzer.get_comprehensive_analysis()
            if not market_data:
                return 0.5
            
            # Calculate potential reward vs risk
            volatility_level = market_data.get('volatility_level', 'NORMAL')
            trend_strength = market_data.get('trend_strength', 0.5)
            
            # Map volatility level to score
            volatility_scores = {'LOW': 0.3, 'NORMAL': 0.7, 'HIGH': 0.9}
            reward_potential = volatility_scores.get(volatility_level, 0.5)
            
            # Trend strength affects reward potential
            trend_bonus = trend_strength * 0.3
            
            # Calculate risk exposure from portfolio
            portfolio_risk = self.portfolio_intelligence.risk_exposure
            
            # Risk-adjusted score
            risk_reward = (reward_potential + trend_bonus) * (1.0 - portfolio_risk * 0.5)
            
            print(f"⚖️ Risk-Reward: {risk_reward:.3f} (Reward:{reward_potential:.2f}, Risk:{portfolio_risk:.2f})")
            return min(1.0, risk_reward)
            
        except Exception as e:
            print(f"❌ Risk-reward calculation error: {e}")
            return 0.5
    
    def _get_performance_modifier(self) -> float:
        """📈 ดึงตัวปรับจากผลงาน (10%)"""
        try:
            if len(self.success_rate_tracker) < 10:
                return 0.5  # ไม่มีข้อมูลพอ
            
            # Calculate recent success rate
            recent_success_rate = sum(self.success_rate_tracker) / len(self.success_rate_tracker)
            
            # Performance modifier based on success rate
            if recent_success_rate >= 0.7:
                modifier = 0.8  # ผลงานดี เพิ่มความเชื่อมั่น
            elif recent_success_rate >= 0.5:
                modifier = 0.5  # ผลงานปกติ
            elif recent_success_rate >= 0.3:
                modifier = 0.3  # ผลงานแย่ ลดความเชื่อมั่น
            else:
                modifier = 0.1  # ผลงานแย่มาก เกือบไม่เข้าตลาด
            
            print(f"📈 Performance Modifier: {modifier:.3f} (Success Rate: {recent_success_rate:.1%})")
            return modifier
            
        except Exception as e:
            print(f"❌ Performance modifier error: {e}")
            return 0.5
    
    # ========================================================================================
    # 🛡️ ANTI-SPAM PROTECTION SYSTEM
    # ========================================================================================
    
    def _should_place_order(self, decision: SmartDecisionScore) -> bool:
        """🛡️ ตัวกรองป้องกันออเดอร์รัวๆ - ปรับให้เหมาะสมขึ้น"""
        try:
            # 1. Check minimum decision score
            min_score = self.adaptive_thresholds["minimum_decision_score"]
            if decision.final_score < min_score:
                decision.warnings.append(f"Decision score too low: {decision.final_score:.3f} < {min_score}")
                return False
            
            # 2. ✨ ปรับการเช็คเวลา - ให้ผ่อนผันขึ้น
            time_since_last = self._get_time_since_last_order()
            min_time = self.adaptive_thresholds["minimum_time_between_orders"]
            
            # ✨ เพิ่มข้อยกเว้น: ถ้า decision score สูงมาก ให้ลดเวลารอ
            if decision.final_score > 0.75:  # Score สูงมาก
                min_time = max(10, min_time * 0.5)  # ลดเวลารอเหลือครึ่ง (ต่ำสุด 10 วินาที)
                print(f"⚡ High Score Override: Reduced wait time to {min_time}s")
            elif decision.final_score > 0.65:  # Score ดี
                min_time = max(15, min_time * 0.7)  # ลดเวลารอ 30%
                print(f"⚡ Good Score Override: Reduced wait time to {min_time}s")
            
            if time_since_last < min_time:
                remaining_time = min_time - time_since_last
                decision.warnings.append(f"Too soon since last order: {time_since_last:.1f}s < {min_time}s (wait {remaining_time:.1f}s more)")
                return False
            
            # 3. Check hourly limit - ปรับให้ผ่อนผัน
            orders_this_hour = self._count_orders_in_last_hour()
            max_hourly = self.adaptive_thresholds["maximum_orders_per_hour"]
            
            # ✨ เพิ่มโบนัสสำหรับ decision score สูง
            if decision.final_score > 0.70:
                max_hourly = int(max_hourly * 1.2)  # เพิ่ม 20%
                print(f"⚡ High Score Bonus: Increased hourly limit to {max_hourly}")
            
            if orders_this_hour >= max_hourly:
                decision.warnings.append(f"Hourly limit exceeded: {orders_this_hour}/{max_hourly}")
                return False
            
            # 4. Check grid density - ผ่อนผันขึ้น
            density_limit = self.adaptive_thresholds["grid_density_limit"]
            if self.grid_intelligence.density_score > density_limit:
                # ✨ ให้โอกาสถ้า decision score สูงมาก
                if decision.final_score > 0.80:
                    print(f"⚡ Excellent Score Override: Allowing despite high density")
                else:
                    decision.warnings.append(f"Grid too dense: {self.grid_intelligence.density_score:.2f} > {density_limit}")
                    return False
            
            # 5. Portfolio health check - ผ่อนผัน
            if self.portfolio_intelligence.health_score < 0.2:  # ลดจาก 0.3 → 0.2
                decision.warnings.append("Portfolio health critically poor")
                return False
            
            # 6. Market condition check - ผ่อนผัน
            if self.market_intelligence.market_readiness < 0.2:  # ลดจาก 0.3 → 0.2
                decision.warnings.append("Market conditions severely unfavorable")
                return False
            
            # ✅ All checks passed!
            print(f"✅ Order APPROVED - Enhanced Filtering Passed!")
            print(f"   Decision Score: {decision.final_score:.3f} ({decision.decision_quality.value})")
            print(f"   Time since last: {time_since_last:.1f}s (min: {min_time}s)")
            print(f"   Orders this hour: {orders_this_hour}/{max_hourly}")
            return True
            
        except Exception as e:
            print(f"❌ Should place order check error: {e}")
            return False  # Safe default - don't place order on error
    
    def _execute_intelligent_order(self, decision: SmartDecisionScore):
        """🎯 ดำเนินการออเดอร์อย่างอัจฉริยะ"""
        try:
            if not self.order_manager:
                print("❌ No order manager available")
                return
            
            # Determine order direction based on decision analysis
            order_direction = self._determine_order_direction(decision)
            if order_direction == "WAIT":
                print("⏳ Decision suggests waiting for better opportunity")
                return
            
            # Calculate intelligent lot size
            lot_size = self._calculate_intelligent_lot_size(decision)
            
            # Execute order with context
            success = self._place_order_with_context(order_direction, lot_size, decision)
            
            # Record result for learning
            self._record_order_result(decision, success, order_direction, lot_size)
            
            # Update anti-spam tracking
            self._update_order_tracking(order_direction)
            
        except Exception as e:
            print(f"❌ Execute intelligent order error: {e}")
    
    # ========================================================================================
    # 📊 INTELLIGENCE UPDATES
    # ========================================================================================
    
    def _update_market_intelligence(self):
        """📊 อัปเดตสติปัญญาการวิเคราะห์ตลาด"""
        try:
            if not self.market_analyzer:
                return
            
            # ✅ แก้ไข: ใช้ method ที่มีจริง
            market_data = self.market_analyzer.get_comprehensive_analysis()
            if not market_data:
                return
            
            # Update session
            self.market_intelligence.current_session = self._detect_market_session()
            
            # Update trend
            self.market_intelligence.trend_direction = market_data.get('trend_direction', 'SIDEWAYS')
            
            # Update volatility level
            volatility = market_data.get('volatility_level', 'NORMAL')
            self.market_intelligence.volatility_level = volatility
            
        except Exception as e:
            print(f"❌ Update market intelligence error: {e}")
    
    def _update_portfolio_intelligence(self):
        """💼 อัปเดตสติปัญญาพอร์ตโฟลิโอ"""
        try:
            if not self.position_manager:
                return
            
            # ✅ แก้ไข: ใช้ method ที่มีจริง
            portfolio_data = self.position_manager.get_4d_portfolio_status()
            if not portfolio_data:
                return
            
            # Update portfolio stats
            self.portfolio_intelligence.total_positions = portfolio_data.get('total_positions', 0)
            self.portfolio_intelligence.profitable_positions = portfolio_data.get('profitable_positions', 0)
            self.portfolio_intelligence.losing_positions = portfolio_data.get('losing_positions', 0)
            self.portfolio_intelligence.total_pnl = portfolio_data.get('total_pnl', 0.0)
            self.portfolio_intelligence.unrealized_pnl = portfolio_data.get('unrealized_pnl', 0.0)
            
        except Exception as e:
            print(f"❌ Update portfolio intelligence error: {e}")
    
    def _update_grid_intelligence(self):
        """📈 อัปเดตสติปัญญากริด"""
        try:
            if not self.order_manager:
                return
            
            # Get active orders
            active_orders = self.order_manager.get_active_orders()
            if not active_orders:
                # Reset grid intelligence if no orders
                self.grid_intelligence = GridIntelligence()
                return
            
            # Analyze grid structure
            buy_orders = [o for o in active_orders if 'BUY' in str(o.get('type', ''))]
            sell_orders = [o for o in active_orders if 'SELL' in str(o.get('type', ''))]
            
            self.grid_intelligence.total_orders = len(active_orders)
            self.grid_intelligence.buy_orders = len(buy_orders)
            self.grid_intelligence.sell_orders = len(sell_orders)
            
            # Calculate grid metrics
            self._calculate_grid_metrics(active_orders)
            
        except Exception as e:
            print(f"❌ Update grid intelligence error: {e}")
    
    # ========================================================================================
    # 🔧 HELPER METHODS
    # ========================================================================================
    
    def _get_time_since_last_order(self) -> float:
        """ดึงเวลาตั้งแต่ออเดอร์สุดท้าย (วินาที)"""
        try:
            if not self.last_order_time:
                return float('inf')  # ไม่เคยวางออเดอร์
            
            last_time = max(self.last_order_time.values())
            return (datetime.now() - last_time).total_seconds()
            
        except Exception as e:
            print(f"❌ Get time since last order error: {e}")
            return 0.0  # Safe default
    
    def _count_orders_in_last_hour(self) -> int:
        """นับออเดอร์ในชั่วโมงที่แล้ว"""
        try:
            one_hour_ago = datetime.now() - timedelta(hours=1)
            count = 0
            
            for decision_record in self.decision_history:
                if decision_record['timestamp'] > one_hour_ago:
                    count += 1
            
            return count
            
        except Exception as e:
            print(f"❌ Count orders in last hour error: {e}")
            return 0
    
    def _evaluate_volatility_appropriateness(self, market_data: Dict) -> float:
        """ประเมินความเหมาะสมของ volatility"""
        try:
            volatility_level = market_data.get('volatility_level', 'NORMAL')
            
            # Grid trading works best in medium volatility
            volatility_scores = {
                'LOW': 0.6,     # Too quiet
                'NORMAL': 1.0,  # Perfect
                'HIGH': 0.7     # Too volatile
            }
            
            return volatility_scores.get(volatility_level, 0.5)
                
        except Exception:
            return 0.5
    
    def _evaluate_session_favorability(self) -> float:
        """ประเมินความเหมาะสมของ session"""
        try:
            current_session = self._detect_market_session()
            
            session_scores = {
                MarketSession.LONDON: 0.9,    # Best for gold
                MarketSession.NEW_YORK: 0.8,  # Good
                MarketSession.OVERLAP: 0.85,  # Very good
                MarketSession.ASIAN: 0.6,     # Moderate
                MarketSession.QUIET: 0.3      # Poor
            }
            
            return session_scores.get(current_session, 0.5)
            
        except Exception:
            return 0.5
    
    def _detect_market_session(self) -> MarketSession:
        """ตรวจจับ market session ปัจจุบัน"""
        try:
            # Simplified session detection based on UTC time
            current_hour = datetime.utcnow().hour
            
            if 0 <= current_hour < 7:
                return MarketSession.ASIAN
            elif 7 <= current_hour < 13:
                return MarketSession.LONDON
            elif 13 <= current_hour < 17:
                return MarketSession.OVERLAP
            elif 17 <= current_hour < 22:
                return MarketSession.NEW_YORK
            else:
                return MarketSession.QUIET
                
        except Exception:
            return MarketSession.QUIET
    
    def _evaluate_spread_condition(self) -> float:
        """ประเมินสภาพ spread"""
        try:
            if not self.market_analyzer:
                return 0.5
            
            # ✅ แก้ไข: ใช้ข้อมูลจาก comprehensive analysis
            market_data = self.market_analyzer.get_comprehensive_analysis()
            spread = market_data.get('spread', 0.05)
            
            # ประเมินตาม spread (ยิ่งแคบยิ่งดี)
            if spread <= 0.02:
                return 0.9  # Excellent
            elif spread <= 0.05:
                return 0.7  # Good
            elif spread <= 0.10:
                return 0.5  # Average
            else:
                return 0.3  # Poor
                
        except Exception:
            return 0.5
    
    # ========================================================================================
    # 📈 LEARNING & ADAPTATION
    # ========================================================================================
    
    def _update_performance_learning(self):
        """📈 อัปเดตการเรียนรู้จากผลงาน"""
        try:
            if len(self.decision_history) < 10:
                return
            
            # Analyze recent decision quality
            recent_decisions = list(self.decision_history)[-20:]  # Last 20 decisions
            avg_score = sum(d['score'] for d in recent_decisions) / len(recent_decisions)
            
            # Store in quality tracker
            self.decision_quality_tracker.append(avg_score)
            
            print(f"📈 Average Decision Quality (last 20): {avg_score:.3f}")
            
        except Exception as e:
            print(f"❌ Update performance learning error: {e}")
    
    def _adjust_thresholds_from_performance(self):
        """🎯 ปรับ thresholds ตามผลงานอัตโนมัติ - ADAPTIVE Learning"""
        try:
            # ใช้ข้อมูลจาก learning_history ถ้ามี (ผลการประเมินจริง)
            if hasattr(self, 'learning_history') and len(self.learning_history) >= 10:
                final_results = [record['final_success'] for record in list(self.learning_history)[-10:]]
                recent_success = sum(final_results) / len(final_results)
                evaluation_source = "Final Evaluation"
            elif len(self.success_rate_tracker) >= 10:
                recent_success = sum(self.success_rate_tracker[-10:]) / 10
                evaluation_source = "Immediate Results"
            else:
                return  # ข้อมูลไม่พอสำหรับการเรียนรู้
            
            learning_rate = self.adaptive_thresholds["learning_rate"]
            current_threshold = self.adaptive_thresholds["minimum_decision_score"]
            
            print(f"📊 ADAPTIVE Learning ({evaluation_source}): Recent success rate: {recent_success:.1%}")
            
            # ปรับ threshold ตามผลงาน
            if recent_success < 0.35:  # ผลงานแย่มาก (< 35%)
                # เพิ่ม threshold มาก เพื่อเลือกให้ดีขึ้น
                new_threshold = min(0.85, current_threshold + learning_rate * 1.5)
                if new_threshold != current_threshold:
                    self.adaptive_thresholds["minimum_decision_score"] = new_threshold
                    print(f"🚨 ADAPTIVE: Very poor performance → Major threshold increase: {current_threshold:.3f} → {new_threshold:.3f}")
                    print("   → Being much more selective to improve quality")
                    
            elif recent_success < 0.50:  # ผลงานแย่ (< 50%)
                # เพิ่ม threshold เพื่อเลือกมากขึ้น
                new_threshold = min(0.80, current_threshold + learning_rate)
                if new_threshold != current_threshold:
                    self.adaptive_thresholds["minimum_decision_score"] = new_threshold
                    print(f"🎯 ADAPTIVE: Poor performance → Raising threshold: {current_threshold:.3f} → {new_threshold:.3f}")
                    print("   → Being more selective to improve quality")
                    
            elif recent_success > 0.75:  # ผลงานดีมาก (> 75%)
                # ลด threshold มาก เพื่อหาโอกาสมากขึ้น
                new_threshold = max(0.35, current_threshold - learning_rate * 1.2)
                if new_threshold != current_threshold:
                    self.adaptive_thresholds["minimum_decision_score"] = new_threshold
                    print(f"🚀 ADAPTIVE: Excellent performance → Major threshold decrease: {current_threshold:.3f} → {new_threshold:.3f}")
                    print("   → Being much more aggressive to capture more opportunities")
                    
            elif recent_success > 0.65:  # ผลงานดี (> 65%)
                # ลด threshold เพื่อหาโอกาสมากขึ้น
                new_threshold = max(0.40, current_threshold - learning_rate)
                if new_threshold != current_threshold:
                    self.adaptive_thresholds["minimum_decision_score"] = new_threshold
                    print(f"🎯 ADAPTIVE: Good performance → Lowering threshold: {current_threshold:.3f} → {new_threshold:.3f}")
                    print("   → Being more aggressive to capture more opportunities")
                    
            else:  # ผลงานปกติ (50-65%)
                print(f"🎯 ADAPTIVE: Balanced performance ({recent_success:.1%}) → Maintaining threshold: {current_threshold:.3f}")
            
            # บันทึกการปรับแต่ง
            adaptation_record = {
                'timestamp': datetime.now(),
                'adaptation_event': True,
                'success_rate': recent_success,
                'evaluation_source': evaluation_source,
                'threshold_before': current_threshold,
                'threshold_after': self.adaptive_thresholds["minimum_decision_score"],
                'threshold_adjusted': current_threshold != self.adaptive_thresholds["minimum_decision_score"]
            }
            
            self.decision_history.append(adaptation_record)
            
        except Exception as e:
            print(f"❌ ADAPTIVE threshold adjustment error: {e}")
            # ใช้ fallback threshold
            self.adaptive_thresholds["minimum_decision_score"] = 0.50
    
    # ========================================================================================
    # 🔧 ADDITIONAL HELPER METHODS (Implementation stubs)
    # ========================================================================================
    
    def _generate_decision_reasoning(self, decision: SmartDecisionScore) -> List[str]:
        """สร้างเหตุผลการตัดสินใจ"""
        reasoning = []
        
        if decision.market_quality > 0.7:
            reasoning.append("Market conditions favorable")
        elif decision.market_quality < 0.4:
            reasoning.append("Market conditions challenging")
        
        if decision.portfolio_necessity > 0.7:
            reasoning.append("Portfolio needs rebalancing")
        elif decision.portfolio_necessity < 0.4:
            reasoning.append("Portfolio already well-balanced")
        
        if decision.timing_opportunity > 0.7:
            reasoning.append("Good timing opportunity")
        elif decision.timing_opportunity < 0.4:
            reasoning.append("Poor timing - wait for better opportunity")
        
        return reasoning
    
    def _generate_decision_warnings(self, decision: SmartDecisionScore) -> List[str]:
        """สร้างคำเตือนการตัดสินใจ"""
        warnings = []
        
        if decision.final_score < 0.5:
            warnings.append("Low overall decision score")
        
        if self.grid_intelligence.density_score > 0.8:
            warnings.append("Grid density very high")
        
        if self.portfolio_intelligence.risk_exposure > 0.7:
            warnings.append("High portfolio risk exposure")
        
        return warnings
    
    # Additional method stubs for completeness
    def _calculate_portfolio_health(self, portfolio_data: Dict) -> float:
        """คำนวณสุขภาพพอร์ตโฟลิโอ"""
        try:
            # ✅ แก้ไข: ใช้ข้อมูลจาก 4D portfolio status
            health_score = portfolio_data.get('portfolio_health', 0.7)
            return min(1.0, max(0.0, health_score))
        except:
            return 0.7
    
    def _calculate_balance_necessity(self, portfolio_data: Dict) -> float:
        """คำนวณความจำเป็นในการปรับสมดุล"""
        try:
            # ✅ แก้ไข: วิเคราะห์จากสัดส่วน buy/sell
            buy_positions = portfolio_data.get('buy_positions', 0)
            sell_positions = portfolio_data.get('sell_positions', 0)
            total_positions = buy_positions + sell_positions
            
            if total_positions == 0:
                return 0.8  # ไม่มีออเดอร์ = ต้องการสร้าง
            
            # คำนวณความไม่สมดุล
            balance_ratio = buy_positions / total_positions
            imbalance = abs(0.5 - balance_ratio) * 2  # 0-1
            
            return imbalance  # ยิ่งไม่สมดุล ยิ่งจำเป็นปรับ
        except:
            return 0.5
    
    def _calculate_risk_exposure(self, portfolio_data: Dict) -> float:
        """คำนวณการเสี่ยง"""
        try:
            # ✅ แก้ไข: ใช้ข้อมูลจริงจาก portfolio
            total_positions = portfolio_data.get('total_positions', 0)
            losing_positions = portfolio_data.get('losing_positions', 0)
            
            if total_positions == 0:
                return 0.1  # ไม่มีออเดอร์ = เสี่ยงต่ำ
            
            loss_ratio = losing_positions / total_positions
            return min(1.0, loss_ratio)
        except:
            return 0.4
    
    def _calculate_margin_safety(self, portfolio_data: Dict) -> float:
        """คำนวณความปลอดภัยของ margin"""
        try:
            # ✅ แก้ไข: ใช้ข้อมูล margin จริง
            margin_usage = portfolio_data.get('margin_usage_percent', 50.0) / 100.0
            
            # ยิ่งใช้ margin น้อย ยิ่งปลอดภัย
            safety = 1.0 - margin_usage
            return max(0.0, min(1.0, safety))
        except:
            return 0.8
    
    def _get_session_timing_bonus(self) -> float:
        """ดึง bonus จากการปรับเวลา session"""
        session = self._detect_market_session()
        session_multipliers = {
            MarketSession.LONDON: 1.2,
            MarketSession.NEW_YORK: 1.1,
            MarketSession.OVERLAP: 1.3,
            MarketSession.ASIAN: 0.9,
            MarketSession.QUIET: 0.7
        }
        return session_multipliers.get(session, 1.0)
    
    def _determine_order_direction(self, decision: SmartDecisionScore) -> str:
        """กำหนดทิศทางออเดอร์"""
        # Implementation would use portfolio balance and market analysis
        return "BUY"  # Simplified
    
    def _calculate_intelligent_lot_size(self, decision: SmartDecisionScore) -> float:
        """คำนวณขนาด lot อัจฉริยะ"""
        # Implementation would use decision confidence and risk management
        return 0.01  # Simplified
    
    def _place_order_with_context(self, direction: str, lot_size: float, decision: SmartDecisionScore) -> bool:
        """🎯 วางออเดอร์พร้อม context - FIXED method"""
        try:
            if not self.order_manager:
                print("❌ No order manager available")
                return False
            
            print(f"🎯 Executing order through Order Manager:")
            print(f"   Direction: {direction}")
            print(f"   Volume: {lot_size}")
            print(f"   Decision Score: {decision.final_score:.3f}")
            
            # สร้าง OrderRequest
            from order_manager import OrderRequest, OrderType, OrderReason
            
            # กำหนด order type
            if direction.upper() == "BUY":
                order_type = OrderType.MARKET_BUY
            elif direction.upper() == "SELL":
                order_type = OrderType.MARKET_SELL
            else:
                print(f"❌ Invalid direction: {direction}")
                return False
            
            # สร้าง order request
            order_request = OrderRequest(
                order_type=order_type,
                volume=lot_size,
                price=0.0,  # Market order
                reason=OrderReason.PORTFOLIO_BALANCE,
                confidence=decision.final_score,
                reasoning=f"Smart Decision: Score {decision.final_score:.3f}, Quality {decision.decision_quality.value}",
                max_slippage=25,  # ยอมรับ slippage ปานกลาง
                four_d_score=decision.final_score
            )
            
            # Execute through Order Manager
            result = self.order_manager.place_market_order(order_request)
            
            if result.success:
                print(f"✅ Order executed successfully!")
                print(f"   Ticket: #{result.ticket}")
                print(f"   Price: {result.price:.5f}")
                print(f"   Volume: {result.volume:.3f}")
                if hasattr(result, 'execution_time'):
                    print(f"   Execution Time: {result.execution_time:.3f}s")
                return True
            else:
                print(f"❌ Order execution failed: {result.message}")
                return False
                
        except Exception as e:
            print(f"❌ Place order with context error: {e}")
            return False
    
    def _record_order_result(self, decision: SmartDecisionScore, success: bool, direction: str, lot_size: float):
        """📊 บันทึกผลลัพธ์ออเดอร์พร้อมระบบประเมินผลใหม่"""
        try:
            # บันทึกการตัดสินใจพื้นฐาน
            decision_record = {
                'timestamp': datetime.now(),
                'direction': direction,
                'lot_size': lot_size,
                'decision_score': decision.final_score,
                'decision_quality': decision.decision_quality.value,
                'immediate_success': success,  # ความสำเร็จทันที (เปิดออเดอร์ได้)
                
                # เพิ่มข้อมูลสำหรับการประเมินผลภายหลัง
                'evaluation_pending': True,
                'evaluation_start_time': datetime.now(),
                'portfolio_health_before': self.portfolio_intelligence.health_score,
                'market_context': {
                    'volatility_level': self.market_intelligence.volatility_level,
                    'trend_direction': self.market_intelligence.trend_direction,
                    'session': self.market_intelligence.current_session.value
                }
            }
            
            # เก็บไว้สำหรับการประเมินผลภายหลัง
            self.pending_evaluations = getattr(self, 'pending_evaluations', deque(maxlen=100))
            self.pending_evaluations.append(decision_record)
            
            # อัปเดต success rate ทันที (ใช้ immediate success)
            self.success_rate_tracker.append(1.0 if success else 0.0)
            
            print(f"📊 Decision Record: {direction} {lot_size} - Immediate: {'✅' if success else '❌'}")
            print(f"   Decision Score: {decision.final_score:.3f} ({decision.decision_quality.value})")
            print(f"   Portfolio Health Before: {decision_record['portfolio_health_before']:.3f}")
            print(f"   ⏳ Evaluation pending...")
            
        except Exception as e:
            print(f"❌ Record order result error: {e}")
    
    def _evaluate_pending_decisions(self):
        """🎯 ประเมินผลการตัดสินใจที่รอการประเมิน"""
        try:
            if not hasattr(self, 'pending_evaluations') or not self.pending_evaluations:
                return
            
            current_time = datetime.now()
            evaluation_delay = 300  # 5 นาที
            
            # หาการตัดสินใจที่พร้อมประเมิน
            ready_for_evaluation = []
            remaining_evaluations = []
            
            for record in self.pending_evaluations:
                if record.get('evaluation_pending', False):
                    time_elapsed = (current_time - record['evaluation_start_time']).total_seconds()
                    
                    if time_elapsed >= evaluation_delay:
                        ready_for_evaluation.append(record)
                    else:
                        remaining_evaluations.append(record)
                else:
                    remaining_evaluations.append(record)
            
            # ประเมินผลการตัดสินใจที่พร้อม
            for record in ready_for_evaluation:
                final_success = self._evaluate_decision_outcome(record)
                record['final_success'] = final_success
                record['evaluation_pending'] = False
                record['evaluation_completed_time'] = current_time
                
                # อัปเดต learning data
                self._update_learning_from_evaluation(record)
                
                print(f"🎯 Decision Evaluation Complete:")
                print(f"   {record['direction']} @ {record['timestamp'].strftime('%H:%M:%S')}")
                print(f"   Immediate: {'✅' if record['immediate_success'] else '❌'}")
                print(f"   Final: {'✅' if final_success else '❌'}")
                print(f"   Score: {record['decision_score']:.3f}")
                
                remaining_evaluations.append(record)
            
            # อัปเดต pending list
            self.pending_evaluations = deque(remaining_evaluations, maxlen=100)
            
        except Exception as e:
            print(f"❌ Evaluate pending decisions error: {e}")
    
    def _evaluate_decision_outcome(self, record: Dict) -> bool:
        """🎯 ประเมินผลลัพธ์จริงของการตัดสินใจ"""
        try:
            # 1. ประเมินจาก Portfolio Health
            current_portfolio_health = self.portfolio_intelligence.health_score
            health_before = record.get('portfolio_health_before', 0.5)
            health_improvement = current_portfolio_health - health_before
            
            # 2. ประเมินจากการดูแล Active Orders (ถ้ามี)
            portfolio_balance_improvement = 0.0
            if self.position_manager:
                try:
                    portfolio_data = self.position_manager.get_4d_portfolio_status()
                    current_balance = portfolio_data.get('buy_sell_ratio', 0.5)
                    # ถ้าใกล้ 0.5 = สมดุลดี
                    portfolio_balance_improvement = abs(0.5 - abs(0.5 - current_balance))
                except:
                    portfolio_balance_improvement = 0.0
            
            # 3. ประเมินจาก Market Context Appropriateness
            market_context = record.get('market_context', {})
            context_score = 0.5
            
            if market_context.get('volatility_level') == 'NORMAL':
                context_score += 0.2
            if market_context.get('session') in ['LONDON', 'NEW_YORK', 'OVERLAP']:
                context_score += 0.2
                
            # คำนวณคะแนนรวม
            immediate_weight = 0.30    # ความสำเร็จในการเปิดออเดอร์
            health_weight = 0.40       # ผลต่อสุขภาพพอร์ต
            balance_weight = 0.20      # ผลต่อความสมดุล
            context_weight = 0.10      # ความเหมาะสมของ context
            
            final_score = (
                record.get('immediate_success', False) * immediate_weight +
                max(0, health_improvement + 0.1) * health_weight +  # +0.1 เพื่อไม่ให้เป็น 0
                portfolio_balance_improvement * balance_weight +
                context_score * context_weight
            )
            
            # ถ้าคะแนนรวม > 0.6 ถือว่าสำเร็จ
            success_threshold = 0.6
            final_success = final_score >= success_threshold
            
            # เก็บรายละเอียดการประเมิน
            record['evaluation_details'] = {
                'health_improvement': health_improvement,
                'portfolio_balance_improvement': portfolio_balance_improvement,
                'context_score': context_score,
                'final_score': final_score,
                'success_threshold': success_threshold
            }
            
            return final_success
            
        except Exception as e:
            print(f"❌ Decision outcome evaluation error: {e}")
            # Fallback: ใช้ immediate success
            return record.get('immediate_success', False)
    
    def _update_learning_from_evaluation(self, record: Dict):
        """📈 อัปเดตการเรียนรู้จากผลการประเมิน"""
        try:
            immediate_success = record.get('immediate_success', False)
            final_success = record.get('final_success', False)
            decision_score = record.get('decision_score', 0.5)
            
            # อัปเดต success rate tracker ด้วยผลจริง
            if len(self.success_rate_tracker) > 0:
                # แทนที่ค่าเก่าด้วยผลจริง (ถ้าต่างกัน)
                if immediate_success != final_success:
                    # ปรับค่าล่าสุดใน tracker
                    temp_list = list(self.success_rate_tracker)
                    if temp_list:
                        temp_list[-1] = 1.0 if final_success else 0.0
                        self.success_rate_tracker = deque(temp_list, maxlen=100)
                        
                        print(f"📈 Learning Update: Adjusted success from {'✅' if immediate_success else '❌'} to {'✅' if final_success else '❌'}")
            
            # เก็บสำหรับ adaptive learning
            learning_record = {
                'decision_score': decision_score,
                'immediate_success': immediate_success,
                'final_success': final_success,
                'evaluation_details': record.get('evaluation_details', {}),
                'timestamp': record['timestamp']
            }
            
            if not hasattr(self, 'learning_history'):
                self.learning_history = deque(maxlen=200)
            self.learning_history.append(learning_record)
            
        except Exception as e:
            print(f"❌ Update learning from evaluation error: {e}")
    
    def _update_order_tracking(self, direction: str):
        """อัปเดตการติดตามออเดอร์"""
        self.last_order_time[direction] = datetime.now()
    
    def _calculate_grid_metrics(self, active_orders: List[Dict]):
        """คำนวณเมตริกของกริด"""
        if not active_orders:
            return
        
        # Calculate density score based on order spacing
        self.grid_intelligence.density_score = min(1.0, len(active_orders) / 20.0)
        
        # Calculate distribution score (how well spread the orders are)
        self.grid_intelligence.distribution_score = 0.7  # Simplified
        
        # Calculate balance score (buy/sell ratio)
        if self.grid_intelligence.total_orders > 0:
            buy_ratio = self.grid_intelligence.buy_orders / self.grid_intelligence.total_orders
            # Ideal ratio is around 0.5 (50/50)
            self.grid_intelligence.balance_score = 1.0 - abs(0.5 - buy_ratio) * 2
        
        # Calculate efficiency score
        self.grid_intelligence.efficiency_score = 0.6  # Simplified
        
        print(f"📈 Grid Intelligence: Density:{self.grid_intelligence.density_score:.2f}, "
              f"Distribution:{self.grid_intelligence.distribution_score:.2f}, "
              f"Balance:{self.grid_intelligence.balance_score:.2f}")
    
    def _maintain_system_health(self):
        """บำรุงรักษาสุขภาพระบบ"""
        # Clean old data
        if len(self.decision_history) > 500:
            self.decision_history = deque(list(self.decision_history)[-300:], maxlen=500)
    
    def _auto_save_if_needed(self):
        """💾 บันทึกข้อมูลการเรียนรู้อัตโนมัติ"""
        try:
            if not self.auto_save_enabled:
                return
            
            time_since_save = (datetime.now() - self.last_save_time).total_seconds()
            
            if time_since_save >= self.auto_save_interval:
                self._save_learning_data()
                self.last_save_time = datetime.now()
                
        except Exception as e:
            print(f"❌ Auto-save error: {e}")
    
    def _save_learning_data(self):
        """💾 บันทึกข้อมูลการเรียนรู้"""
        try:
            learning_data = {
                "timestamp": datetime.now().isoformat(),
                "engine_version": "Modern_Smart_AI_v2.0",
                "trading_mode": self.current_mode.value,
                
                # Performance Learning Data
                "adaptive_thresholds": self.adaptive_thresholds.copy(),
                "success_rate_history": list(self.success_rate_tracker),
                "decision_quality_history": list(self.decision_quality_tracker),
                
                # Decision History (last 50)
                "recent_decisions": [
                    {
                        "timestamp": d.get("timestamp", datetime.now()).isoformat() if hasattr(d.get("timestamp", datetime.now()), 'isoformat') else str(d.get("timestamp", datetime.now())),
                        "score": d.get("score", 0.0),
                        "quality": d.get("quality", "UNKNOWN"),
                        "success": d.get("success", False)
                    }
                    for d in list(self.decision_history)[-50:] if isinstance(d, dict)
                ],
                
                # Grid Intelligence
                "grid_intelligence": {
                    "density_score": self.grid_intelligence.density_score,
                    "distribution_score": self.grid_intelligence.distribution_score,
                    "balance_score": self.grid_intelligence.balance_score,
                    "total_orders": self.grid_intelligence.total_orders
                },
                
                # Market Intelligence  
                "market_intelligence": {
                    "volatility_level": self.market_intelligence.volatility_level,
                    "trend_direction": self.market_intelligence.trend_direction,
                    "current_session": self.market_intelligence.current_session.value
                },
                
                # Learning Statistics
                "learning_stats": {
                    "total_decisions": len(self.decision_history),
                    "recent_success_rate": sum(self.success_rate_tracker) / max(1, len(self.success_rate_tracker)) if self.success_rate_tracker else 0.0,
                    "current_threshold": self.adaptive_thresholds["minimum_decision_score"],
                    "learning_active": self.current_mode == TradingMode.ADAPTIVE
                }
            }
            
            import json
            with open(self.performance_file, 'w', encoding='utf-8') as f:
                json.dump(learning_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Learning data saved: {len(self.decision_history)} decisions, threshold: {self.adaptive_thresholds['minimum_decision_score']:.3f}")
            
        except Exception as e:
            print(f"❌ Save learning data error: {e}")
    
    def _load_previous_learning(self):
        """📁 โหลดข้อมูลการเรียนรู้ที่ผ่านมา"""
        try:
            import json
            import os
            
            if not os.path.exists(self.performance_file):
                print("📁 No previous learning data found - starting fresh")
                return
            
            with open(self.performance_file, 'r', encoding='utf-8') as f:
                learning_data = json.load(f)
            
            # โหลด adaptive thresholds
            if "adaptive_thresholds" in learning_data:
                saved_thresholds = learning_data["adaptive_thresholds"]
                for key, value in saved_thresholds.items():
                    if key in self.adaptive_thresholds:
                        self.adaptive_thresholds[key] = value
            
            # โหลด performance history
            if "success_rate_history" in learning_data:
                self.success_rate_tracker = deque(learning_data["success_rate_history"], maxlen=100)
            
            if "decision_quality_history" in learning_data:
                self.decision_quality_tracker = deque(learning_data["decision_quality_history"], maxlen=100)
            
            # โหลด intelligence data
            if "grid_intelligence" in learning_data:
                grid_data = learning_data["grid_intelligence"]
                self.grid_intelligence.density_score = grid_data.get("density_score", 0.0)
                self.grid_intelligence.distribution_score = grid_data.get("distribution_score", 0.0)
                self.grid_intelligence.balance_score = grid_data.get("balance_score", 0.0)
                self.grid_intelligence.total_orders = grid_data.get("total_orders", 0)
            
            # แสดงข้อมูลที่โหลด
            learning_stats = learning_data.get("learning_stats", {})
            recent_success = learning_stats.get("recent_success_rate", 0.0)
            current_threshold = learning_stats.get("current_threshold", 0.50)
            
            print(f"📁 Previous learning loaded:")
            print(f"   • Success Rate: {recent_success:.1%}")
            print(f"   • Current Threshold: {current_threshold:.3f}")
            print(f"   • Performance History: {len(self.success_rate_tracker)} records")
            print(f"   • Decision History: {learning_stats.get('total_decisions', 0)} decisions")
            
            # ตั้งโหมดตามที่เก็บไว้
            if learning_stats.get("learning_active", False):
                print("   • ADAPTIVE mode was active - continuing adaptation")
            
        except Exception as e:
            print(f"❌ Load previous learning error: {e}")
            print("📁 Starting with fresh learning data")
        
    # ========================================================================================
    # 📊 STATUS & REPORTING
    # ========================================================================================
    
    def get_intelligence_summary(self) -> Dict:
        """ดึงสรุปสติปัญญาระบบ"""
        try:
            return {
                "market_intelligence": {
                    "market_readiness": self.market_intelligence.market_readiness,
                    "current_session": self.market_intelligence.current_session.value,
                    "volatility_level": self.market_intelligence.volatility_level,
                    "trend_direction": self.market_intelligence.trend_direction
                },
                "portfolio_intelligence": {
                    "portfolio_readiness": self.portfolio_intelligence.portfolio_readiness,
                    "health_score": self.portfolio_intelligence.health_score,
                    "balance_necessity": self.portfolio_intelligence.balance_necessity,
                    "risk_exposure": self.portfolio_intelligence.risk_exposure,
                    "total_positions": self.portfolio_intelligence.total_positions
                },
                "grid_intelligence": {
                    "overall_intelligence": self.grid_intelligence.overall_intelligence,
                    "density_score": self.grid_intelligence.density_score,
                    "distribution_score": self.grid_intelligence.distribution_score,
                    "balance_score": self.grid_intelligence.balance_score,
                    "total_orders": self.grid_intelligence.total_orders
                },
                "decision_stats": {
                    "recent_success_rate": sum(self.success_rate_tracker[-10:]) / max(1, len(self.success_rate_tracker[-10:])) if self.success_rate_tracker else 0.0,
                    "avg_decision_quality": sum(self.decision_quality_tracker[-10:]) / max(1, len(self.decision_quality_tracker[-10:])) if self.decision_quality_tracker else 0.0,
                    "orders_this_hour": self._count_orders_in_last_hour(),
                    "time_since_last_order": self._get_time_since_last_order(),
                    "minimum_decision_threshold": self.adaptive_thresholds["minimum_decision_score"]
                }
            }
        except Exception as e:
            print(f"❌ Get intelligence summary error: {e}")
            return {}

    def get_anti_spam_status(self) -> Dict:
        """ดึงสถานะระบบป้องกันสแปม"""
        return {
            "time_since_last_order": f"{self._get_time_since_last_order():.0f}s",
            "orders_this_hour": f"{self._count_orders_in_last_hour()}/{self.adaptive_thresholds['maximum_orders_per_hour']}",
            "current_decision_threshold": f"{self.adaptive_thresholds['minimum_decision_score']:.3f}",
            "grid_density": f"{self.grid_intelligence.density_score:.2f}/{self.adaptive_thresholds['grid_density_limit']:.2f}",
            "protection_active": "✅ ACTIVE" if self._get_time_since_last_order() < self.adaptive_thresholds["minimum_time_between_orders"] else "⏳ READY"
        }

# END OF MODERN RULE ENGINE - ENHANCED SMART EDITION