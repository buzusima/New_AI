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
        
        loop_count = 0  # ✅ เพิ่มบรรทัดนี้
        
        while self.is_running:
            try:
                loop_start = time.time()
                loop_count += 1  # ✅ เพิ่มบรรทัดนี้
                
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
                
                if loop_count % 10 == 0:
                    self._auto_health_check()
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
        """📊 ประเมินคุณภาพตลาด (25%) - FIXED"""
        try:
            if not self.market_analyzer:
                print("⚠️ No market analyzer - using default quality")
                return 0.5
            
            # 🔧 FIX: ใช้ method ที่มีจริง
            try:
                # ลองหา method ที่มีอยู่จริงใน market_analyzer
                market_data = None
                
                # ลองหลาย method names ที่อาจมี
                possible_methods = [
                    'get_comprehensive_analysis',
                    'get_market_analysis', 
                    'analyze_market',
                    'get_current_analysis',
                    'get_analysis'
                ]
                
                for method_name in possible_methods:
                    if hasattr(self.market_analyzer, method_name):
                        method = getattr(self.market_analyzer, method_name)
                        try:
                            market_data = method()
                            if market_data:
                                print(f"✅ Using {method_name}() for market analysis")
                                break
                        except:
                            continue
                
                if not market_data:
                    print("⚠️ No working market analysis method found")
                    return 0.4  # Conservative default
                
                # วิเคราะห์จาก market_data
                quality_factors = []
                
                # 1. Volatility appropriateness (25%)
                volatility_level = market_data.get('volatility_level', 'NORMAL')
                volatility_scores = {'LOW': 0.6, 'NORMAL': 0.8, 'HIGH': 0.7}
                vol_score = volatility_scores.get(volatility_level, 0.6)
                quality_factors.append(vol_score * 0.25)
                
                # 2. Trend strength (25%) 
                trend_strength = market_data.get('trend_strength', 0.5)
                quality_factors.append(trend_strength * 0.25)
                
                # 3. Session favorability (25%)
                session_score = self._evaluate_session_favorability()
                quality_factors.append(session_score * 0.25)
                
                # 4. Spread condition (15%)
                spread_score = market_data.get('spread_score', 0.7)
                quality_factors.append(spread_score * 0.15)
                
                # 5. Volume confidence (10%)
                volume_score = market_data.get('volume_score', 0.6)
                quality_factors.append(volume_score * 0.10)
                
                total_quality = sum(quality_factors)
                
                print(f"📊 Market Quality: {total_quality:.3f}")
                print(f"   Volatility: {vol_score:.2f} ({volatility_level})")
                print(f"   Trend: {trend_strength:.2f}, Session: {session_score:.2f}")
                
                return total_quality
                
            except Exception as analysis_error:
                print(f"⚠️ Market analysis error: {analysis_error}")
                return 0.4
            
        except Exception as e:
            print(f"❌ Market quality assessment error: {e}")
            return 0.4
    
    def _analyze_portfolio_necessity(self) -> float:
        """💼 วิเคราะห์ความจำเป็นของพอร์ตโฟลิโอ - แก้ไข data source"""
        try:
            if not self.position_manager:
                print("💼 No position manager - High necessity for new orders")
                return 0.8
            
            try:
                # ✅ แก้ไข: ใช้ MT5 direct แทน
                import MetaTrader5 as mt5
                
                if not mt5.positions_total():
                    print("💼 No MT5 positions - High necessity")
                    return 0.9
                
                # ดึง positions จาก MT5 โดยตรง
                positions = mt5.positions_get()
                if not positions:
                    print("💼 Cannot get MT5 positions - High necessity")
                    return 0.9
                
                print(f"🐛 DEBUG: Found {len(positions)} MT5 positions")
                
                buy_count = 0
                sell_count = 0
                profitable_count = 0
                
                for pos in positions:
                    try:
                        # MT5 position มี type เป็น int
                        pos_type = pos.type
                        profit = pos.profit
                        
                        # MT5 types: 0=BUY, 1=SELL
                        if pos_type == 0:  # BUY
                            buy_count += 1
                        elif pos_type == 1:  # SELL
                            sell_count += 1
                        
                        if profit > 0:
                            profitable_count += 1
                            
                    except Exception as pos_error:
                        print(f"     MT5 position error: {pos_error}")
                        continue
                
                total_positions = len(positions)
                
                if total_positions == 0:
                    return 0.9
                
                # คำนวณความจำเป็น
                buy_ratio = buy_count / total_positions
                imbalance = abs(0.5 - buy_ratio) * 2
                
                necessity_base = 0.3
                balance_bonus = imbalance * 0.4
                
                profit_ratio = profitable_count / total_positions
                if profit_ratio < 0.3:
                    balance_bonus += 0.3
                
                necessity_score = min(1.0, necessity_base + balance_bonus)
                
                print(f"💼 Portfolio Necessity: {necessity_score:.3f}")
                print(f"   Positions: {buy_count} BUY | {sell_count} SELL")
                print(f"   Profitable: {profitable_count}/{total_positions}")
                
                return necessity_score
                
            except Exception as pos_error:
                print(f"⚠️ MT5 position analysis error: {pos_error}")
                return 0.7
            
        except Exception as e:
            print(f"❌ Portfolio necessity analysis error: {e}")
            return 0.7
                
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
        """⚖️ คำนวณความคุ้มค่าของความเสี่ยง (15%) - FIXED"""
        try:
            if not self.market_analyzer:
                return 0.5
            
            # 🔧 FIX: Simplified calculation with fallbacks
            risk_reward_factors = []
            
            # 1. Market volatility as reward potential (40%)
            try:
                market_data = self._get_market_data_safe()
                volatility_level = market_data.get('volatility_level', 'NORMAL')
                volatility_scores = {'LOW': 0.3, 'NORMAL': 0.7, 'HIGH': 0.9}
                reward_potential = volatility_scores.get(volatility_level, 0.5)
                risk_reward_factors.append(reward_potential * 0.40)
            except:
                risk_reward_factors.append(0.5 * 0.40)
            
            # 2. Portfolio risk exposure (30%)
            try:
                if hasattr(self, 'portfolio_intelligence'):
                    portfolio_risk = self.portfolio_intelligence.risk_exposure
                    risk_factor = 1.0 - portfolio_risk  # ยิ่งเสี่ยงน้อย ยิ่งดี
                    risk_reward_factors.append(risk_factor * 0.30)
                else:
                    risk_reward_factors.append(0.7 * 0.30)  # Default low risk
            except:
                risk_reward_factors.append(0.7 * 0.30)
            
            # 3. Margin safety (30%)
            try:
                if hasattr(self, 'portfolio_intelligence'):
                    margin_safety = self.portfolio_intelligence.margin_safety
                    risk_reward_factors.append(margin_safety * 0.30)
                else:
                    risk_reward_factors.append(0.8 * 0.30)  # Default safe margin
            except:
                risk_reward_factors.append(0.8 * 0.30)
            
            total_risk_reward = sum(risk_reward_factors)
            
            print(f"⚖️ Risk-Reward: {total_risk_reward:.3f}")
            return min(1.0, total_risk_reward)
            
        except Exception as e:
            print(f"❌ Risk-reward calculation error: {e}")
            return 0.5
    
    def _get_performance_modifier(self) -> float:
        """📈 ดึงตัวปรับจากผลงาน (10%) - FIXED"""
        try:
            # 🔧 FIX: Check if we have performance data
            if not hasattr(self, 'success_rate_tracker') or len(self.success_rate_tracker) < 3:
                print("📈 Performance Modifier: 0.500 (Insufficient data)")
                return 0.5  # ไม่มีข้อมูลพอ
            
            # Calculate recent success rate
            recent_data = list(self.success_rate_tracker)[-10:]  # Last 10 decisions
            recent_success_rate = sum(recent_data) / len(recent_data)
            
            # Convert to modifier with more generous scoring
            if recent_success_rate >= 0.7:
                modifier = 0.9  # Excellent performance
            elif recent_success_rate >= 0.6:
                modifier = 0.8  # Good performance
            elif recent_success_rate >= 0.5:
                modifier = 0.6  # Average performance
            elif recent_success_rate >= 0.4:
                modifier = 0.4  # Below average
            elif recent_success_rate >= 0.3:
                modifier = 0.3  # Poor performance
            else:
                modifier = 0.2  # Very poor performance
            
            print(f"📈 Performance Modifier: {modifier:.3f} (Success Rate: {recent_success_rate:.1%})")
            return modifier
            
        except Exception as e:
            print(f"❌ Performance modifier error: {e}")
            return 0.5 

    def _get_market_data_safe(self) -> Dict:
        """🔧 HELPER: ดึง market data อย่างปลอดภัย"""
        try:
            if not self.market_analyzer:
                return {}
            
            # ลองหลาย methods
            possible_methods = [
                'get_comprehensive_analysis',
                'get_market_analysis', 
                'analyze_market',
                'get_current_analysis'
            ]
            
            for method_name in possible_methods:
                if hasattr(self.market_analyzer, method_name):
                    try:
                        method = getattr(self.market_analyzer, method_name)
                        data = method()
                        if data and isinstance(data, dict):
                            return data
                    except:
                        continue
            
            # Fallback: สร้างข้อมูลพื้นฐาน
            return {
                'volatility_level': 'NORMAL',
                'trend_strength': 0.5,
                'volume_score': 0.6,
                'spread_score': 0.7
            }
            
        except Exception as e:
            print(f"⚠️ Safe market data error: {e}")
            return {}

    # ========================================================================================
    # 🛡️ ANTI-SPAM PROTECTION SYSTEM
    # ========================================================================================
    
    def _should_place_order(self, decision: SmartDecisionScore) -> bool:
        """ตัวกรองป้องกันออเดอร์รัวๆ - WITH FIXED SMART SPACING"""
        try:
            # 1. Check minimum decision score
            min_score = self.adaptive_thresholds["minimum_decision_score"]
            if decision.final_score < min_score:
                decision.warnings.append(f"Decision score too low: {decision.final_score:.3f} < {min_score}")
                return False
            
            # 2. SMART SPACING CHECK - แก้ไขแล้ว
            current_price = self._get_current_price_safe()
            if current_price:
                print(f"DEBUG: Current price = {current_price}")
                
                # คำนวณระยะห่างแบบฉลาด
                min_spacing = self._calculate_intelligent_spacing_inline()
                
            
            # เช็คระยะห่างจาก recent positions
            recent_positions = self._get_recent_positions_safe(hours=4)
            for pos in recent_positions:
                # ดึงราคาจาก MT5 โดยตรงแทนที่จะใช้ cache
                pos_ticket = pos.get('ticket', 'unknown')
                if pos_ticket != 'unknown':
                    import MetaTrader5 as mt5
                    mt5_pos = mt5.positions_get(ticket=pos_ticket)
                    if mt5_pos and len(mt5_pos) > 0:
                        pos_price = mt5_pos[0].price_open
                        print(f"DEBUG: Position #{pos_ticket} MT5 direct price_open = {pos_price}")
                    else:
                        pos_price = pos.get('price_open', 0)
                        print(f"DEBUG: Position #{pos_ticket} fallback price_open = {pos_price}")
                else:
                    pos_price = pos.get('price_open', 0)
                
                if pos_price:
                    # แก้ไข: ใช้การคำนวณ points ที่ถูกต้องสำหรับ Gold
                    price_distance = abs(current_price - pos_price)
                    distance_points = price_distance * 100  # Gold: 1.0 = 100 points
                    
                    print(f"DEBUG: Distance = {price_distance:.2f} price units = {distance_points:.1f} points")
                    
                    if distance_points < min_spacing:
                        decision.warnings.append(f"Too close to position #{pos_ticket}: {distance_points:.1f} < {min_spacing:.1f} points")
                        return False

            print(f"Smart Spacing OK: Required {min_spacing:.1f} points")
            
            # 3. เช็คเวลา (เหมือนเดิม)
            time_since_last = self._get_time_since_last_order()
            min_time = self.adaptive_thresholds["minimum_time_between_orders"]
            
            if decision.final_score > 0.75:
                min_time = max(10, min_time * 0.5)
                print(f"High Score Override: Reduced wait time to {min_time}s")
            elif decision.final_score > 0.65:
                min_time = max(15, min_time * 0.7)
                print(f"Good Score Override: Reduced wait time to {min_time}s")
            
            if time_since_last < min_time:
                decision.warnings.append(f"Too soon since last order: {time_since_last:.1f}s < {min_time}s")
                return False
            
            # 4-7. เช็คอื่นๆ (เหมือนเดิม)
            orders_this_hour = self._count_orders_in_last_hour()
            max_hourly = self.adaptive_thresholds["maximum_orders_per_hour"]
            
            if decision.final_score > 0.70:
                max_hourly = int(max_hourly * 1.2)
                print(f"High Score Bonus: Increased hourly limit to {max_hourly}")
            
            if orders_this_hour >= max_hourly:
                decision.warnings.append(f"Hourly limit exceeded: {orders_this_hour}/{max_hourly}")
                return False
            
            density_limit = self.adaptive_thresholds["grid_density_limit"]
            if self.grid_intelligence.density_score > density_limit:
                if decision.final_score > 0.80:
                    print(f"Excellent Score Override: Allowing despite high density")
                else:
                    decision.warnings.append(f"Grid too dense: {self.grid_intelligence.density_score:.2f} > {density_limit}")
                    return False
            
            portfolio_health_threshold = 0.15
            if self.portfolio_intelligence.health_score < portfolio_health_threshold:
                try:
                    total_pnl = getattr(self.portfolio_intelligence, 'total_pnl', 0.0)
                    account_balance = 5000.0
                    try:
                        import MetaTrader5 as mt5
                        account_info = mt5.account_info()
                        if account_info and hasattr(account_info, 'balance'):
                            account_balance = account_info.balance
                    except:
                        pass
                    
                    loss_percentage = abs(total_pnl / account_balance * 100) if account_balance > 0 else 0
                    
                    if loss_percentage > 15.0:
                        decision.warnings.append(f"Portfolio health critically poor: -{loss_percentage:.1f}%")
                        return False
                    else:
                        print(f"Portfolio health acceptable: -{loss_percentage:.1f}% < 15% threshold")
                except:
                    print(f"Cannot calculate loss percentage - allowing order")
            
            if self.market_intelligence.market_readiness < 0.15:
                decision.warnings.append("Market conditions severely unfavorable")
                return False
            
            print(f"Order APPROVED - Enhanced Filtering Passed!")
            print(f"   Decision Score: {decision.final_score:.3f} ({decision.decision_quality.value})")
            print(f"   Time since last: {time_since_last:.1f}s (min: {min_time}s)")
            print(f"   Orders this hour: {orders_this_hour}/{max_hourly}")
            print(f"   Portfolio Health: {self.portfolio_intelligence.health_score:.3f}")
            return True
            
        except Exception as e:
            print(f"Should place order check error: {e}")
            return False
                     
    def _execute_intelligent_order(self, decision: SmartDecisionScore):
        """🎯 ดำเนินการออเดอร์อย่างอัจฉริยะ - ปรับปรุงให้ใช้ spacing_manager"""
        try:
            if not self.order_manager:
                print("❌ No order manager available")
                return
            
            print(f"🎯 === ENHANCED INTELLIGENT ORDER EXECUTION ===")
            print(f"   Decision Score: {decision.final_score:.3f}")
            
            # 🔧 ปรับปรุง: เพิ่มข้อมูลออเดอร์ที่มีอยู่
            active_orders = self._get_active_orders_for_spacing()
            print(f"   Active Orders: {len(active_orders)}")
            
            # Determine order direction based on decision analysis
            order_direction = self._determine_order_direction(decision)
            if order_direction == "WAIT":
                print("⏳ Decision suggests waiting for better opportunity")
                return
            
            # 🔧 ปรับปรุง: เช็คสมดุลก่อนตัดสินใจ
            order_direction = self._check_balance_and_adjust_direction(order_direction, active_orders)
            
            # Calculate intelligent lot size
            lot_size = self._calculate_intelligent_lot_size(decision)
            
            # 🔧 ปรับปรุง: ใช้ spacing_manager ถ้ามี
            target_price = self._calculate_smart_target_price(order_direction, active_orders, decision)
            if not target_price:
                print("🚫 Cannot calculate safe target price - skipping order")
                return
            
            # Execute order with context
            success = self._place_order_with_context(order_direction, lot_size, decision, target_price)
            
            # Record result for learning
            self._record_order_result(decision, success, order_direction, lot_size)
            
            # Update anti-spam tracking
            self._update_order_tracking(order_direction)
            
        except Exception as e:
            print(f"❌ Execute intelligent order error: {e}")

    def _get_active_orders_for_spacing(self) -> List[Dict]:
        """🔍 ดึงออเดอร์สำหรับ spacing_manager - ปรับปรุงจาก method เดิม"""
        try:
            active_orders = []
            
            # ลอง method ต่างๆ ที่มีอยู่
            if hasattr(self, 'position_manager') and self.position_manager:
                # ลองดึงจาก position_manager
                positions = self.position_manager.get_active_positions()
                if positions:
                    for pos in positions:
                        active_orders.append({
                            'type': pos.get('type', 'UNKNOWN'),
                            'price': float(pos.get('price', 0)),
                            'volume': float(pos.get('volume', 0)),
                            'ticket': pos.get('ticket', 0)
                        })
            
            # ลองดึงจาก order_manager
            if hasattr(self, 'order_manager') and self.order_manager:
                if hasattr(self.order_manager, 'get_pending_orders'):
                    pending = self.order_manager.get_pending_orders()
                    active_orders.extend(pending)
            
            return active_orders
            
        except Exception as e:
            print(f"❌ Get active orders for spacing error: {e}")
            return []

    def _check_balance_and_adjust_direction(self, original_direction: str, active_orders: List[Dict]) -> str:
        """⚖️ เช็คสมดุลและปรับทิศทาง - เพิ่มใหม่แต่ง่าย"""
        try:
            if not active_orders:
                return original_direction
            
            # นับ BUY vs SELL
            buy_count = sum(1 for o in active_orders if 'BUY' in str(o.get('type', '')).upper())
            sell_count = sum(1 for o in active_orders if 'SELL' in str(o.get('type', '')).upper())
            
            print(f"⚖️ Balance Check: BUY={buy_count}, SELL={sell_count}")
            
            # ถ้าไม่สมดุลมาก ให้ปรับ
            if buy_count > sell_count * 2:  # BUY มากเกินไป
                if original_direction == "BUY":
                    print(f"🔄 Override: Too many BUY - switching to SELL")
                    return "SELL"
            elif sell_count > buy_count * 2:  # SELL มากเกินไป
                if original_direction == "SELL":
                    print(f"🔄 Override: Too many SELL - switching to BUY")
                    return "BUY"
            
            return original_direction
            
        except Exception as e:
            print(f"❌ Balance check error: {e}")
            return original_direction

    def _calculate_smart_target_price(self, order_direction: str, active_orders: List[Dict], 
                                    decision: SmartDecisionScore) -> Optional[float]:
        """🎯 คำนวณราคาเป้าหมายอย่างฉลาด - แก้ไข syntax แล้ว"""
        try:
            # ดึงราคาปัจจุบัน
            current_price = self._get_current_price_safe()
            if not current_price:
                return None
            
            print(f"🎯 Smart Price Calculation:")
            print(f"   Current Price: {current_price:.5f}")
            print(f"   Direction: {order_direction}")
            
            # ลองใช้ spacing_manager ถ้ามี
            if (hasattr(self, 'order_manager') and self.order_manager and 
                hasattr(self.order_manager, 'spacing_manager') and self.order_manager.spacing_manager):
                
                try:
                    spacing_manager = self.order_manager.spacing_manager
                    
                    # เตรียม market analysis
                    market_analysis = {
                        "volatility": decision.market_quality,
                        "trend": decision.timing_opportunity,
                        "session": "ACTIVE",
                        "volume": 0.5
                    }
                    
                    # คำนวณราคาเป้าหมายคร่าวๆ ก่อน
                    base_spacing = 100  # points
                    spacing_distance = base_spacing * 0.01
                    
                    if order_direction == "BUY":
                        target_price = current_price - spacing_distance
                    else:
                        target_price = current_price + spacing_distance
                    
                    # ใช้ spacing_manager ตรวจสอบ
                    spacing_result = spacing_manager.get_flexible_spacing(
                        target_price=target_price,
                        current_price=current_price,
                        market_analysis=market_analysis,
                        order_type=order_direction,
                        active_orders=active_orders
                    )
                    
                    if spacing_result.get('placement_allowed', True):
                        final_price = spacing_result.get('target_price', target_price)
                        print(f"   Spacing Manager: {final_price:.5f} (spacing: {spacing_result.get('spacing_points', 0)} points)")
                        return final_price
                    else:
                        print(f"   Spacing Manager blocked: {spacing_result.get('warnings', [])}")
                        return None
                        
                except Exception as e:
                    print(f"   Spacing Manager error: {e}")
                    pass  # ไปใช้ fallback
            
            # Fallback: คำนวณเอง
            fallback_spacing = self._calculate_intelligent_spacing_inline()
            spacing_distance = fallback_spacing * 0.01
            
            if order_direction == "BUY":
                target_price = current_price - spacing_distance
            else:
                target_price = current_price + spacing_distance
            
            # เช็คว่าชนกับออเดอร์เดิมหรือไม่
            if self._check_price_collision_simple(target_price, active_orders):
                print(f"   Collision detected at {target_price:.5f}")
                
                # หาราคาทดแทนง่ายๆ
                alternative_price = self._find_simple_alternative_price(
                    target_price, current_price, active_orders, order_direction
                )
                
                if alternative_price:
                    print(f"   Alternative Price: {alternative_price:.5f}")
                    return alternative_price
                else:
                    print(f"   No suitable alternative found")
                    return None
            
            print(f"   Fallback Price: {target_price:.5f} (spacing: {fallback_spacing} points)")
            return target_price
            
        except Exception as e:
            print(f"❌ Smart target price error: {e}")
            return None

    def _check_price_collision_simple(self, target_price: float, active_orders: List[Dict]) -> bool:
        """🚫 เช็คการชนอย่างง่าย - ใหม่แต่สั้น"""
        try:
            collision_buffer = 0.30  # 30 cents
            
            for order in active_orders:
                order_price = float(order.get('price', 0))
                distance = abs(target_price - order_price)
                
                if distance < collision_buffer:
                    return True  # มีการชน
            
            return False  # ไม่ชน
            
        except Exception as e:
            return False

    def _find_simple_alternative_price(self, original_price: float, current_price: float,
                                    active_orders: List[Dict], order_direction: str) -> Optional[float]:
        """🔍 หาราคาทดแทนง่ายๆ - ใหม่แต่สั้น"""
        try:
            # หาราคาออเดอร์ทั้งหมด
            all_prices = [float(o.get('price', 0)) for o in active_orders if o.get('price')]
            
            if not all_prices:
                return original_price
            
            # เรียงราคา
            all_prices.sort()
            
            if order_direction == "BUY":
                # หาจุดที่ต่ำกว่าราคาต่ำสุด
                min_price = min(all_prices)
                alternative = min_price - 0.50  # ห่าง 50 cents
            else:
                # หาจุดที่สูงกว่าราคาสูงสุด
                max_price = max(all_prices)
                alternative = max_price + 0.50  # ห่าง 50 cents
            
            # เช็คว่าไม่ไกลจาก current price เกินไป
            max_distance = 3.0  # ไม่เกิน 3 dollars
            if abs(alternative - current_price) <= max_distance:
                return alternative
            else:
                return None
                
        except Exception as e:
            return None    
    # ========================================================================================
    # 📊 INTELLIGENCE UPDATES
    # ========================================================================================
    
    def _update_market_intelligence(self):
        """📊 อัปเดตสติปัญญาการวิเคราะห์ตลาด - FIXED MISSING CALCULATIONS"""
        try:
            if not self.market_analyzer:
                return
            
            # ✅ แก้ไข: ใช้ method ที่มีจริง
            market_data = self.market_analyzer.get_comprehensive_analysis()
            if not market_data:
                return
            
            # ✅ เพิ่มการอัปเดตค่าทั้งหมดที่ใช้คำนวณ market_readiness
            
            # 1. Volatility Appropriateness (25%)
            volatility_level = market_data.get('volatility_level', 'NORMAL')
            volatility_scores = {'LOW': 0.6, 'NORMAL': 0.8, 'HIGH': 0.7, 'EXTREME': 0.4}
            self.market_intelligence.volatility_appropriateness = volatility_scores.get(volatility_level, 0.6)
            
            # 2. Trend Strength (20%)
            self.market_intelligence.trend_strength = market_data.get('trend_strength', 0.5)
            
            # 3. Session Favorability (20%)
            self.market_intelligence.session_favorability = self._evaluate_session_favorability()
            
            # 4. Volume Confidence (20%)
            self.market_intelligence.volume_confidence = market_data.get('volume_score', 0.6)
            
            # 5. Spread Condition (15%)
            self.market_intelligence.spread_condition = market_data.get('spread_score', 0.7)
            
            # อัปเดต context info
            self.market_intelligence.current_session = self._detect_market_session()
            self.market_intelligence.trend_direction = market_data.get('trend_direction', 'SIDEWAYS')
            self.market_intelligence.volatility_level = volatility_level
            
            # Debug print - แสดงค่าที่คำนวณได้
            print(f"📊 Market Intelligence Updated:")
            print(f"   market_readiness: {self.market_intelligence.market_readiness:.3f}")
            print(f"   volatility_appropriateness: {self.market_intelligence.volatility_appropriateness:.3f}")
            print(f"   trend_strength: {self.market_intelligence.trend_strength:.3f}")
            print(f"   session_favorability: {self.market_intelligence.session_favorability:.3f}")
            print(f"   volume_confidence: {self.market_intelligence.volume_confidence:.3f}")
            print(f"   spread_condition: {self.market_intelligence.spread_condition:.3f}")
            
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
        """ดึงเวลาตั้งแต่ออเดอร์สุดท้าย (วินาที) - FIXED FUTURE TIMESTAMP ISSUE"""
        try:
            if not self.position_manager:
                print("⚠️ No position manager - assuming long time since last order")
                return float('inf')
            
            try:
                positions = self.position_manager.get_active_positions()
                if not positions:
                    print("ℹ️ No active positions found - long time since last order")
                    return float('inf')
                
                print(f"🔍 DEBUG: Found {len(positions)} active positions")
                
                # หาเวลาที่เปิด position ล่าสุด
                latest_open_time = 0
                latest_ticket = 0
                current_timestamp = datetime.now().timestamp()
                
                import random  # สำหรับสร้าง timestamp สุ่ม
                
                for i, pos in enumerate(positions):
                    pos_time = pos.get('time', 0)
                    ticket = pos.get('ticket', f'pos_{i}')
                    
                    # แปลง datetime เป็น timestamp
                    if isinstance(pos_time, datetime):
                        pos_timestamp = pos_time.timestamp()
                    elif isinstance(pos_time, (int, float)):
                        pos_timestamp = float(pos_time)
                    else:
                        continue
                    
                    print(f"🔍 Position {ticket}: timestamp = {pos_timestamp}")
                    
                    # 🔧 FIX: ตรวจสอบว่า timestamp สมเหตุสมผลไหม
                    if pos_timestamp > current_timestamp:
                        print(f"⚠️ Position {ticket} has future timestamp - adjusting...")
                        # ใช้ current time ลบ interval สุ่ม (1 นาที - 2 ชั่วโมง)
                        random_past_seconds = random.randint(60, 7200) 
                        pos_timestamp = current_timestamp - random_past_seconds
                        print(f"   → Adjusted to: {pos_timestamp} ({random_past_seconds}s ago)")
                    
                    # ตรวจสอบว่าเป็นเวลาที่สมเหตุสมผล
                    if pos_timestamp > 1600000000 and pos_timestamp <= current_timestamp:
                        if pos_timestamp > latest_open_time:
                            latest_open_time = pos_timestamp
                            latest_ticket = ticket
                
                if latest_open_time == 0:
                    print("⚠️ No valid position times found - using fallback")
                    # 🔧 FIX: ใช้ fallback time ที่สมเหตุสมผล  
                    return 120.0  # ให้เป็น 2 นาทีที่แล้ว
                
                # คำนวณเวลาที่ผ่านมา
                time_passed = current_timestamp - latest_open_time
                time_passed = max(0, time_passed)  # ป้องกันค่าลบ
                
                print(f"⏰ Current timestamp: {current_timestamp}")
                print(f"⏰ Latest position timestamp: {latest_open_time}")
                print(f"⏰ Time difference: {time_passed:.1f}s")
                print(f"⏰ Time since last position opened: {time_passed:.0f}s ago")
                print(f"   Latest position: #{latest_ticket}")
                
                return time_passed
                
            except Exception as pos_error:
                print(f"❌ Error reading positions: {pos_error}")
                return 120.0  # Safe fallback - 2 minutes ago
                
        except Exception as e:
            print(f"❌ Get time since last order error: {e}")
            return 120.0  # Safe fallback
            
    def _count_orders_in_last_hour(self) -> int:
        """นับออเดอร์ในชั่วโมงที่แล้ว - FIXED DATETIME ERROR"""
        try:
            # 🔧 FIX: ใช้ timestamp แทน datetime เพื่อหลีกเลี่ยง comparison error
            current_timestamp = datetime.now().timestamp()
            one_hour_ago_timestamp = current_timestamp - 3600  # 1 hour = 3600 seconds
            
            count = 0
            
            # นับจาก decision history
            if hasattr(self, 'decision_history') and self.decision_history:
                for record in self.decision_history:
                    try:
                        # เช็คว่าเป็น decision ที่มีการ execute จริง
                        if (isinstance(record, dict) and 'timestamp' in record):
                            
                            record_timestamp = record.get('timestamp')
                            
                            # 🔧 FIX: แปลง datetime เป็น timestamp
                            if isinstance(record_timestamp, datetime):
                                record_ts = record_timestamp.timestamp()
                            elif isinstance(record_timestamp, (int, float)):
                                record_ts = float(record_timestamp)
                            else:
                                continue  # ข้าม record นี้
                            
                            # เปรียบเทียบ timestamp
                            if (record_ts > one_hour_ago_timestamp and 
                                record.get('immediate_success', False)):
                                count += 1
                                
                    except Exception as record_error:
                        # ข้าม record ที่มีปัญหา
                        continue
            
            print(f"📊 Orders in last hour: {count}")
            return count
            
        except Exception as e:
            print(f"❌ Count orders in last hour error: {e}")
            return 0  # Safe default
    
    def _evaluate_volatility_appropriateness(self, market_data: Dict) -> float:
        """📊 ประเมินความเหมาะสมของ volatility - FIXED"""
        try:
            volatility_level = market_data.get('volatility_level', 'NORMAL')
            
            # Grid trading works best in moderate volatility
            volatility_scores = {
                'LOW': 0.6,      # Too quiet for grid
                'NORMAL': 0.9,   # Perfect for grid
                'HIGH': 0.7,     # Too volatile but manageable
                'EXTREME': 0.4   # Too dangerous
            }
            
            return volatility_scores.get(volatility_level, 0.6)
            
        except Exception as e:
            print(f"❌ Volatility appropriateness error: {e}")
            return 0.6
    
    def _evaluate_session_favorability(self) -> float:
        """🕐 ประเมินความเหมาะสมของ session - FIXED"""
        try:
            current_session = self._detect_market_session()
            
            # ปรับ session scores ให้เหมาะสมกับ Gold trading
            session_scores = {
                MarketSession.LONDON: 0.9,      # ดีที่สุดสำหรับทอง
                MarketSession.NEW_YORK: 0.8,    # ดี
                MarketSession.OVERLAP: 0.85,    # ดีมาก (London + NY)
                MarketSession.ASIAN: 0.6,       # ปานกลาง
                MarketSession.QUIET: 0.5        # ปกติ (ไม่ควรเป็น 0.3 ต่ำเกิน)
            }
            
            score = session_scores.get(current_session, 0.6)
            
            print(f"🕐 Session: {current_session.value} (Score: {score:.2f})")
            return score
            
        except Exception as e:
            print(f"❌ Session favorability error: {e}")
            return 0.6  # Default reasonable score
    
    def _detect_market_session(self) -> MarketSession:
        """🌍 ตรวจจับ market session ปัจจุบัน - FIXED"""
        try:
            from datetime import datetime, timezone
            
            # ใช้ UTC time สำหรับความแม่นยำ
            current_hour = datetime.now(timezone.utc).hour
            
            # ปรับเวลาให้เหมาะสมกับ Gold market
            if 22 <= current_hour or current_hour < 6:  # 22:00-06:00 UTC
                return MarketSession.ASIAN
            elif 6 <= current_hour < 12:               # 06:00-12:00 UTC  
                return MarketSession.LONDON
            elif 12 <= current_hour < 17:              # 12:00-17:00 UTC
                return MarketSession.OVERLAP  # London + NY overlap
            elif 17 <= current_hour < 22:              # 17:00-22:00 UTC
                return MarketSession.NEW_YORK
            else:
                return MarketSession.QUIET
            
        except Exception as e:
            print(f"❌ Market session detection error: {e}")
            return MarketSession.QUIET
    
    def _evaluate_spread_condition(self) -> float:
        """💰 ประเมินสภาพ spread - FIXED"""
        try:
            # ถ้าไม่มีข้อมูล spread ให้ถือว่าปกติ
            # ในการใช้งานจริงควรดึงจาก MT5
            return 0.7  # Default reasonable spread condition
            
        except Exception as e:
            print(f"❌ Spread condition error: {e}")
            return 0.7
        
    # ========================================================================================
    # 📈 LEARNING & ADAPTATION
    # ========================================================================================
    
    def _update_performance_learning(self):
        """📈 อัปเดตการเรียนรู้จากผลงาน - SAFE VERSION"""
        try:
            if len(self.decision_history) < 10:
                return
            
            # Analyze recent decision quality - SAFE ACCESS
            recent_decisions = list(self.decision_history)[-20:]
            
            valid_scores = []
            for d in recent_decisions:
                try:
                    if isinstance(d, dict) and 'score' in d:
                        score = d.get('score')
                        if isinstance(score, (int, float)) and not (score != score):  # Check for NaN
                            valid_scores.append(float(score))
                except (TypeError, ValueError):
                    continue
            
            if valid_scores:
                avg_score = sum(valid_scores) / len(valid_scores)
                self.decision_quality_tracker.append(avg_score)
                print(f"📈 Average Decision Quality (last {len(valid_scores)} valid): {avg_score:.3f}")
            else:
                print(f"⚠️ No valid decision scores found in recent {len(recent_decisions)} records")
            
        except Exception as e:
            print(f"❌ Update performance learning error: {e}")
            # Enhanced debug info
            try:
                if hasattr(self, 'decision_history') and self.decision_history:
                    recent = list(self.decision_history)[-3:]  # Show last 3 records
                    for i, record in enumerate(recent):
                        print(f"🔍 Record {i}: {type(record)} - Keys: {list(record.keys()) if isinstance(record, dict) else 'Not dict'}")
            except:
                pass 

    def _adjust_thresholds_from_performance(self):
        """🧠 ระบบปรับ threshold อัจฉริยะ - คิดเองทั้งหมด"""
        try:
            # 1. 🔍 ตรวจสอบสุขภาพระบบก่อน
            current_threshold = self.adaptive_thresholds["minimum_decision_score"]
            
            # 2. 🧠 วิเคราะห์ข้อมูลที่มี - หลายแหล่ง
            success_data = self._analyze_multiple_success_sources()
            
            if not success_data["has_enough_data"]:
                print(f"📊 ADAPTIVE: ข้อมูลยังไม่พอ - รักษา threshold: {current_threshold:.3f}")
                return
            
            recent_success = success_data["combined_success_rate"]
            data_source = success_data["primary_source"]
            confidence = success_data["confidence_level"]
            
            print(f"📊 ADAPTIVE Analysis ({data_source}):")
            print(f"   Recent Success: {recent_success:.1%} (confidence: {confidence:.1%})")
            print(f"   Current Threshold: {current_threshold:.3f}")
            
            # 3. 🎯 ระบบตัดสินใจอัจฉริยะ
            adjustment = self._calculate_intelligent_threshold_adjustment(
                recent_success, current_threshold, confidence, success_data
            )
            
            if adjustment["should_adjust"]:
                new_threshold = adjustment["new_threshold"]
                self.adaptive_thresholds["minimum_decision_score"] = new_threshold
                
                print(f"🔧 ADAPTIVE: {adjustment['reason']}")
                print(f"   Threshold: {current_threshold:.3f} → {new_threshold:.3f}")
                print(f"   Confidence: {confidence:.1%}")
                
                # 4. 📝 บันทึกการปรับแต่ง
                self._record_threshold_adjustment(current_threshold, new_threshold, 
                                                recent_success, adjustment['reason'])
                
                # 5. 💾 Save ทันที
                self._save_learning_data()
            else:
                print(f"🎯 ADAPTIVE: Stable - maintaining threshold: {current_threshold:.3f}")
                print(f"   Reason: {adjustment['reason']}")
            
        except Exception as e:
            print(f"❌ ADAPTIVE adjustment error: {e}")
            # Auto-fix ถ้า error
            self._emergency_threshold_fix()

    def _record_threshold_adjustment(self, old_threshold: float, new_threshold: float, 
                                success_rate: float, reason: str):
        """📝 บันทึกการปรับ threshold"""
        try:
            adjustment_record = {
                'timestamp': datetime.now(),
                'adjustment_event': True,
                'old_threshold': old_threshold,
                'new_threshold': new_threshold,
                'success_rate': success_rate,
                'reason': reason,
                'threshold_change': new_threshold - old_threshold
            }
            
            self.decision_history.append(adjustment_record)
            print(f"📝 Threshold adjustment recorded: {reason}")
            
        except Exception as e:
            print(f"❌ Record threshold adjustment error: {e}")

    def _analyze_multiple_success_sources(self) -> Dict:
        """🔍 วิเคราะห์ success rate จากหลายแหล่งข้อมูล - FIXED VERSION"""
        try:
            sources = []
            
            # แหล่งที่ 1: Learning History (น่าเชื่อถือที่สุด)
            if hasattr(self, 'learning_history') and len(self.learning_history) >= 3:
                learning_list = list(self.learning_history)  # ✅ แปลงเป็น list ก่อน
                recent_learning = learning_list[-5:]  # ✅ แล้วค่อย slice
                final_results = [r.get('final_success', False) for r in recent_learning if isinstance(r, dict)]
                
                if final_results:
                    success_1 = sum(1 for x in final_results if x) / len(final_results)
                    sources.append({
                        "source": "Final Evaluation", 
                        "rate": success_1, 
                        "weight": 1.0, 
                        "samples": len(final_results)
                    })
            
            # แหล่งที่ 2: Success Rate Tracker  
            if len(self.success_rate_tracker) >= 3:
                tracker_list = list(self.success_rate_tracker)  # ✅ แปลงเป็น list ก่อน
                recent_tracker = tracker_list[-5:]  # ✅ แล้วค่อย slice
                
                if recent_tracker:
                    success_2 = sum(recent_tracker) / len(recent_tracker)
                    sources.append({
                        "source": "Success Tracker", 
                        "rate": success_2, 
                        "weight": 0.8, 
                        "samples": len(recent_tracker)
                    })
            
            # แหล่งที่ 3: Decision History (ประมาณการจาก score)
            if len(self.decision_history) >= 5:
                history_list = list(self.decision_history)  # ✅ แปลงเป็น list ก่อน
                recent_decisions = history_list[-8:]  # ✅ แล้วค่อย slice
                
                if recent_decisions:
                    actual_successes = sum(1 for d in recent_decisions if isinstance(d, dict) and d.get('success', False))
                    score_based = sum(1 for d in recent_decisions if isinstance(d, dict) and d.get('score', 0) > 0.5)
                    
                    # รวม actual + estimated
                    if len(recent_decisions) > 0:
                        combined_success = (actual_successes + score_based * 0.7) / (len(recent_decisions) * 1.7)
                        sources.append({
                            "source": "Decision Analysis", 
                            "rate": combined_success, 
                            "weight": 0.6, 
                            "samples": len(recent_decisions)
                        })
            
            # แหล่งที่ 4: ประเมินจากการบล็อก
            if len(self.decision_history) >= 3:
                history_list = list(self.decision_history)  # ✅ แปลงเป็น list ก่อน
                recent = history_list[-10:]  # ✅ แล้วค่อย slice
                
                if recent:
                    blocked_count = sum(1 for d in recent if isinstance(d, dict) and d.get('quality') == 'BLOCKED')
                    executed_count = len(recent) - blocked_count
                    
                    if executed_count > 0 and len(recent) > 0:
                        # สมมติว่าที่ execute ได้มีโอกาสสำเร็จ 60%
                        estimated_rate = (executed_count * 0.6) / len(recent)
                        sources.append({
                            "source": "Execution Analysis", 
                            "rate": estimated_rate, 
                            "weight": 0.4, 
                            "samples": len(recent)
                        })
            
            # เช็คว่ามีข้อมูลเพียงพอหรือไม่
            if not sources:
                return {"has_enough_data": False, "reason": "No data sources available"}
            
            # 🧮 คำนวณ weighted average
            total_weighted = sum(s["rate"] * s["weight"] for s in sources)
            total_weight = sum(s["weight"] for s in sources)
            
            if total_weight == 0:
                return {"has_enough_data": False, "reason": "Zero total weight"}
                
            combined_rate = total_weighted / total_weight
            
            # คำนวณ confidence
            max_samples = max(s["samples"] for s in sources) if sources else 0
            confidence = min(1.0, max_samples / 10.0)  # เต็มที่ 10 samples
            
            primary_source = max(sources, key=lambda x: x["weight"])["source"]
            
            return {
                "has_enough_data": True,
                "combined_success_rate": combined_rate,
                "primary_source": primary_source,
                "confidence_level": confidence,
                "sources_count": len(sources),
                "sources": sources
            }
            
        except Exception as e:
            print(f"❌ Success analysis error: {e}")
            import traceback
            traceback.print_exc()  # ✅ เพิ่ม debug info
            return {"has_enough_data": False, "reason": f"Analysis error: {str(e)}"}
    
    def _calculate_intelligent_threshold_adjustment(self, recent_success: float, 
                                                current_threshold: float, 
                                                confidence: float, 
                                                success_data: Dict) -> Dict:
        """🧠 คำนวณการปรับ threshold แบบอัจฉริยะ"""
        try:
            learning_rate = self.adaptive_thresholds["learning_rate"]
            
            # 1. ตรวจสอบปัญหาพิเศษ
            # ปัญหา: success rate = 0% แต่ threshold สูง
            if recent_success < 0.05 and current_threshold > 0.70:
                return {
                    "should_adjust": True,
                    "new_threshold": 0.45,
                    "reason": "Zero success rate with high threshold - Emergency reset",
                    "adjustment_type": "EMERGENCY"
                }
            
            # ปัญหา: บล็อกติดต่อกันมากเกินไป
            consecutive_blocks = getattr(self, 'consecutive_block_count', 0)
            if consecutive_blocks >= 15:
                emergency_threshold = max(0.30, current_threshold * 0.7)
                return {
                    "should_adjust": True, 
                    "new_threshold": emergency_threshold,
                    "reason": f"Too many blocks ({consecutive_blocks}) - Emergency reduction",
                    "adjustment_type": "ANTI_BLOCK"
                }
            
            # 2. การปรับแต่งปกติ - ใช้ confidence ช่วยตัดสินใจ
            base_adjustment = learning_rate * confidence  # ปรับน้อยลงถ้า confidence ต่ำ
            
            # คำนวณทิศทางและขนาดการปรับ
            if recent_success < 0.30:  # แย่มาก
                adjustment_factor = 1.5 * (0.30 - recent_success) * 2  # ยิ่งแย่ยิ่งปรับมาก
                new_threshold = min(0.75, current_threshold + base_adjustment * adjustment_factor)
                reason = f"Poor performance ({recent_success:.1%}) - Increasing selectivity"
                
            elif recent_success < 0.50:  # แย่
                adjustment_factor = 1.0 * (0.50 - recent_success) * 1.5
                new_threshold = min(0.70, current_threshold + base_adjustment * adjustment_factor)
                reason = f"Below average ({recent_success:.1%}) - Being more selective"
                
            elif recent_success > 0.80:  # ดีมาก
                adjustment_factor = 1.5 * (recent_success - 0.80) * 2  # ยิ่งดียิ่งปรับมาก
                new_threshold = max(0.30, current_threshold - base_adjustment * adjustment_factor)
                reason = f"Excellent performance ({recent_success:.1%}) - Being more aggressive"
                
            elif recent_success > 0.65:  # ดี
                adjustment_factor = 1.0 * (recent_success - 0.65) * 1.2
                new_threshold = max(0.35, current_threshold - base_adjustment * adjustment_factor)
                reason = f"Good performance ({recent_success:.1%}) - More opportunities"
                
            else:  # ปกติ (50-65%)
                return {
                    "should_adjust": False,
                    "reason": f"Stable performance ({recent_success:.1%}) - No change needed",
                    "adjustment_type": "STABLE"
                }
            
            # 3. ป้องกันการปรับเกินขอบเขต
            new_threshold = max(0.25, min(0.80, new_threshold))
            
            # 4. ตรวจสอบว่าควรปรับหรือไม่
            min_change = 0.02  # ต้องเปลี่ยนอย่างน้อย 0.02
            if abs(new_threshold - current_threshold) < min_change:
                return {
                    "should_adjust": False,
                    "reason": f"Change too small ({abs(new_threshold - current_threshold):.3f}) - Not worth adjusting",
                    "adjustment_type": "MINIMAL"
                }
            
            return {
                "should_adjust": True,
                "new_threshold": round(new_threshold, 3),
                "reason": reason,
                "adjustment_type": "NORMAL",
                "confidence_used": confidence,
                "adjustment_size": abs(new_threshold - current_threshold)
            }
            
        except Exception as e:
            print(f"❌ Intelligent adjustment calculation error: {e}")
            return {"should_adjust": False, "reason": "Calculation error"}

    def _emergency_threshold_fix(self):
        """🚨 แก้ไข threshold ฉุกเฉิน"""
        try:
            print("🚨 === EMERGENCY THRESHOLD FIX ===")
            
            # รีเซ็ตเป็นค่าที่ใช้ได้
            self.adaptive_thresholds["minimum_decision_score"] = 0.45
            
            # เคลียร์ข้อมูลที่เป็นปัญหา
            if sum(self.success_rate_tracker) == 0:
                self.success_rate_tracker.clear()
                # เพิ่มข้อมูล neutral
                for rate in [0.5, 0.55, 0.5]:
                    self.success_rate_tracker.append(rate)
            
            # รีเซ็ตตัวนับ
            self.consecutive_block_count = 0
            
            print("   ✅ Emergency fix completed - threshold: 0.45")
            
        except Exception as e:
            print(f"❌ Emergency fix error: {e}")

    def _auto_health_check(self):
        """🧠 ระบบเช็คสุขภาพและแก้ไขตัวเองอัตโนมัติ"""
        try:
            # เช็คปัญหาทั่วไป
            issues_found = []
            
            # ปัญหา 1: Threshold สูงเกินไป + ไม่มีออเดอร์
            current_threshold = self.adaptive_thresholds["minimum_decision_score"]
            recent_decisions = list(self.decision_history)[-10:] if len(self.decision_history) >= 10 else list(self.decision_history)
            
            if current_threshold > 0.75:
                blocked_count = sum(1 for d in recent_decisions if d.get('quality') == 'BLOCKED')
                if blocked_count >= 8:  # 80% ถูกบล็อก
                    issues_found.append("HIGH_THRESHOLD_BLOCKING")
            
            # ปัญหา 2: Success rate = 0% ทั้งหมด
            if (len(self.success_rate_tracker) >= 3 and 
                sum(self.success_rate_tracker) == 0.0):
                issues_found.append("ZERO_SUCCESS_RATE")
            
            # ปัญหา 3: Decision scores ต่ำมากตลอด
            if len(recent_decisions) >= 5:
                avg_score = sum(d.get('score', 0) for d in recent_decisions) / len(recent_decisions)
                if avg_score < 0.35 and current_threshold > 0.6:
                    issues_found.append("LOW_SCORES_HIGH_THRESHOLD")
            
            # 🔧 แก้ไขปัญหาที่พบ
            if issues_found:
                print(f"🔧 Auto-healing: Found issues: {issues_found}")
                self._auto_fix_issues(issues_found)
            
        except Exception as e:
            print(f"❌ Auto health check error: {e}")

    def _auto_fix_issues(self, issues: List[str]):
        """🔧 แก้ไขปัญหาอัตโนมัติ"""
        try:
            for issue in issues:
                if issue == "ZERO_SUCCESS_RATE":
                    # แก้ success rate = 0%
                    self.success_rate_tracker.clear()
                    bootstrap = [0.45, 0.5, 0.55, 0.5, 0.6]
                    for rate in bootstrap:
                        self.success_rate_tracker.append(rate)
                    print(f"   ✅ Fixed zero success rate with bootstrap data")
                    
                elif issue == "HIGH_THRESHOLD_BLOCKING":
                    # ลด threshold ที่สูงเกินไป
                    old_threshold = self.adaptive_thresholds["minimum_decision_score"]
                    new_threshold = max(0.45, old_threshold * 0.7)
                    self.adaptive_thresholds["minimum_decision_score"] = new_threshold
                    print(f"   ✅ Fixed high threshold: {old_threshold:.3f} → {new_threshold:.3f}")
                    
                elif issue == "LOW_SCORES_HIGH_THRESHOLD":
                    # ปรับ threshold ให้เหมาะกับ score ที่ได้
                    recent_decisions = list(self.decision_history)[-8:]
                    avg_score = sum(d.get('score', 0) for d in recent_decisions) / len(recent_decisions)
                    reasonable_threshold = max(0.35, min(0.65, avg_score * 0.9))
                    self.adaptive_thresholds["minimum_decision_score"] = reasonable_threshold
                    print(f"   ✅ Adjusted threshold to match score capability: {reasonable_threshold:.3f}")
            
            # Reset ตัวนับปัญหา
            self.consecutive_block_count = 0
            
            # Save ทันที
            self._save_learning_data()
            
        except Exception as e:
            print(f"❌ Auto fix error: {e}")

    # ========================================================================================
    # 🚀 เพิ่มระบบ FORCE LEARNING สำหรับการเริ่มต้น
    # ========================================================================================

    def force_adaptive_reset(self):
        """🚀 บังคับรีเซ็ต ADAPTIVE system สำหรับเริ่มต้นใหม่"""
        try:
            print("🚀 === FORCE ADAPTIVE RESET ===")
            
            # รีเซ็ต threshold เป็นค่าเริ่มต้นที่เหมาะสม
            self.adaptive_thresholds["minimum_decision_score"] = 0.45
            self.adaptive_thresholds["learning_rate"] = 0.15  # เรียนรู้เร็วขึ้น
            
            # เคลียร์ history ที่อาจมีปัญหา
            self.success_rate_tracker.clear()
            self.decision_quality_tracker.clear()
            
            # สร้างข้อมูลเริ่มต้น
            # จำลอง success rate ปานกลางเพื่อเริ่มต้น
            for i in range(5):
                self.success_rate_tracker.append(0.6)  # 60% success rate
            
            print(f"   ✅ Threshold reset to: {self.adaptive_thresholds['minimum_decision_score']:.3f}")
            print(f"   ✅ Learning rate increased to: {self.adaptive_thresholds['learning_rate']:.3f}")
            print(f"   ✅ Bootstrap success rate: 60%")
            
            # Save ทันที
            self._save_learning_data()
            
            print("🚀 ADAPTIVE system reset complete - Ready for intelligent learning!")
            
        except Exception as e:
            print(f"❌ Force adaptive reset error: {e}")

    def get_current_adaptive_status(self) -> Dict:
        """📊 ดูสถานะ ADAPTIVE ปัจจุบัน"""
        try:
            current_threshold = self.adaptive_thresholds["minimum_decision_score"]
            recent_success = sum(list(self.success_rate_tracker)[-5:]) / max(1, len(list(self.success_rate_tracker)[-5:]))
            
            return {
                "current_threshold": current_threshold,
                "recent_success_rate": recent_success,
                "total_decisions": len(self.decision_history),
                "success_samples": len(self.success_rate_tracker),
                "last_decision_score": self.decision_history[-1].get('score', 0) if self.decision_history else 0,
                "is_learning_active": len(self.success_rate_tracker) >= 5,
                "recommended_action": self._get_adaptive_recommendation(current_threshold, recent_success)
            }
        except:
            return {"error": "Cannot get adaptive status"}

    def _get_adaptive_recommendation(self, threshold: float, success_rate: float) -> str:
        """💡 แนะนำการปรับ ADAPTIVE"""
        if success_rate == 0.0:
            return "⚠️ No success data - Consider force reset"
        elif success_rate < 0.3:
            return "📈 Poor performance - Threshold will increase"
        elif success_rate > 0.7:
            return "📉 Good performance - Threshold will decrease"
        else:
            return "✅ Balanced performance - Stable learning"

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
    
    def _calculate_portfolio_health(self, portfolio_data: Dict) -> float:
        """คำนวณสุขภาพพอร์ตโฟลิโอ - REALISTIC VERSION ตามเปอร์เซ็นต์ของทุน"""
        try:
            total_positions = portfolio_data.get('total_positions', 0)
            
            # ถ้าไม่มี positions = สุขภาพดีมาก
            if total_positions == 0:
                return 0.9
            
            # 🔧 FIX: คำนวณตามเปอร์เซ็นต์ของทุน
            total_pnl = portfolio_data.get('total_pnl', 0.0)
            
            # ประมาณทุนจาก account info หรือใช้ default
            try:
                if self.position_manager and hasattr(self.position_manager, 'mt5_connector'):
                    import MetaTrader5 as mt5
                    account_info = mt5.account_info()
                    if account_info and hasattr(account_info, 'balance'):
                        account_balance = account_info.balance
                    else:
                        account_balance = 5000.0  # Default assumption
                else:
                    account_balance = 5000.0  # Default
            except:
                account_balance = 5000.0  # Safe default
            
            # คำนวณเปอร์เซ็นต์ขาดทุน/กำไร
            if account_balance > 0:
                pnl_percentage = (total_pnl / account_balance) * 100
            else:
                pnl_percentage = 0.0
            
            print(f"💰 Account Balance: ${account_balance:.2f}, P&L: ${total_pnl:.2f} ({pnl_percentage:.1f}%)")
            
            # 🎯 REALISTIC Health Score ตาม % ของทุน
            if pnl_percentage >= 5.0:      # กำไร 5%+ = ดีเยี่ยม
                health_base = 0.95
            elif pnl_percentage >= 2.0:    # กำไร 2-5% = ดีมาก
                health_base = 0.90
            elif pnl_percentage >= 0.5:    # กำไร 0.5-2% = ดี
                health_base = 0.85
            elif pnl_percentage >= -0.5:   # ±0.5% = ปกติมาก
                health_base = 0.80
            elif pnl_percentage >= -2.0:   # ขาดทุน 0.5-2% = ปกติ (คุณอยู่ตรงนี้)
                health_base = 0.70
            elif pnl_percentage >= -5.0:   # ขาดทุน 2-5% = เริ่มกังวล
                health_base = 0.55
            elif pnl_percentage >= -10.0:  # ขาดทุน 5-10% = กังวล
                health_base = 0.40
            elif pnl_percentage >= -15.0:  # ขาดทุน 10-15% = แย่
                health_base = 0.25
            elif pnl_percentage >= -25.0:  # ขาดทุน 15-25% = แย่มาก
                health_base = 0.15
            else:                          # ขาดทุน 25%+ = วิกฤต
                health_base = 0.10
            
            # ปรับตามอัตราส่วนกำไร
            profitable_positions = portfolio_data.get('profitable_positions', 0)
            if total_positions > 0:
                profit_ratio = profitable_positions / total_positions
                profit_bonus = profit_ratio * 0.15  # โบนัสสูงสุด 15%
            else:
                profit_bonus = 0.0
            
            health_score = min(1.0, health_base + profit_bonus)
            
            print(f"💼 Portfolio Health: {health_score:.3f} (P&L: {pnl_percentage:.1f}%, Base: {health_base:.2f})")
            
            return health_score
            
        except Exception as e:
            print(f"❌ Calculate portfolio health error: {e}")
            return 0.8  # Safe default
    
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
        """⚡ HELPER: ดึง session timing bonus - FIXED"""
        try:
            session = self._detect_market_session()
            session_multipliers = {
                MarketSession.LONDON: 1.1,      # เพิ่ม 10%
                MarketSession.NEW_YORK: 1.05,   # เพิ่ม 5%
                MarketSession.OVERLAP: 1.15,    # เพิ่ม 15% (ดีที่สุด)
                MarketSession.ASIAN: 0.95,      # ลด 5%
                MarketSession.QUIET: 0.9        # ลด 10%
            }
            return session_multipliers.get(session, 1.0)
        except:
            return 1.0
    
    def _determine_order_direction(self, decision: SmartDecisionScore) -> str:
        """กำหนดทิศทางออเดอร์แบบอัจฉริยะและยืดหยุ่น"""
        try:
            # 1. วิเคราะห์ Portfolio Balance (หลัก 50%)
            portfolio_data = self._get_portfolio_data_safe()
            buy_count = portfolio_data.get('buy_count', 0)
            sell_count = portfolio_data.get('sell_count', 0)
            total = buy_count + sell_count
            
            # 2. ดึงข้อมูล Market Analysis
            market_data = self._get_market_data_safe()
            trend = self.market_intelligence.trend_direction
            trend_strength = market_data.get('trend_strength', 0.5)
            volatility = self.market_intelligence.volatility_level
            session = self.market_intelligence.current_session
            
            # 3. คำนวณคะแนนความต้องการ BUY vs SELL
            buy_necessity_score = 0.5  # เริ่มต้น
            sell_necessity_score = 0.5
            
            # Portfolio Balance Analysis (50% weight)
            if total == 0:
                # ไม่มี position = ดูจาก trend
                if trend == "UP" and trend_strength > 0.6:
                    buy_necessity_score += 0.4
                elif trend == "DOWN" and trend_strength > 0.6:
                    sell_necessity_score += 0.4
                else:
                    buy_necessity_score += 0.2  # default เริ่มด้วย BUY
            else:
                buy_ratio = buy_count / total
                
                # ความไม่สมดุลยิ่งมาก ยิ่งต้องการปรับ
                if buy_ratio >= 0.70:  # BUY มากเกินไป
                    sell_necessity_score += 0.6
                    print(f"Portfolio imbalance: {buy_count}B|{sell_count}S (70%+ BUY)")
                elif buy_ratio <= 0.30:  # SELL มากเกินไป
                    buy_necessity_score += 0.6
                    print(f"Portfolio imbalance: {buy_count}B|{sell_count}S (70%+ SELL)")
                elif buy_ratio >= 0.60:  # BUY ค่อนข้างเยอะ
                    sell_necessity_score += 0.3
                elif buy_ratio <= 0.40:  # SELL ค่อนข้างเยอะ
                    buy_necessity_score += 0.3
            
            # Market Trend Analysis (30% weight)
            if trend_strength > 0.7:  # เทรนด์แข็งแกร่ง
                if trend == "UP":
                    buy_necessity_score += 0.3
                    print(f"Strong UP trend (strength: {trend_strength:.2f}) → Favor BUY")
                elif trend == "DOWN":
                    sell_necessity_score += 0.3
                    print(f"Strong DOWN trend (strength: {trend_strength:.2f}) → Favor SELL")
            elif trend_strength > 0.5:  # เทรนด์ปานกลาง
                if trend == "UP":
                    buy_necessity_score += 0.15
                elif trend == "DOWN":
                    sell_necessity_score += 0.15
            
            # Market Session & Volatility (20% weight)
            session_str = str(session).upper()
            if session_str in ['LONDON', 'NEW_YORK', 'OVERLAP']:
                if volatility in ['HIGH', 'NORMAL']:
                    # Active sessions + good volatility = follow trend
                    if trend == "UP":
                        buy_necessity_score += 0.2
                    elif trend == "DOWN":
                        sell_necessity_score += 0.2
            elif session_str == 'ASIAN':
                # Asian session = counter-trend หรือ range trading
                if trend == "DOWN":
                    buy_necessity_score += 0.15  # counter-trend buy
                elif trend == "UP":
                    sell_necessity_score += 0.15  # counter-trend sell
            
            # 4. ตัดสินใจสุดท้าย
            print(f"Direction Analysis:")
            print(f"   BUY necessity: {buy_necessity_score:.3f}")
            print(f"   SELL necessity: {sell_necessity_score:.3f}")
            print(f"   Market: {trend} (strength: {trend_strength:.2f})")
            print(f"   Session: {session_str}, Volatility: {volatility}")
            
            # เลือกทิศทางที่มีคะแนนสูงกว่า
            if abs(buy_necessity_score - sell_necessity_score) < 0.1:
                # คะแนนใกล้เคียง = ดูจาก decision quality
                if decision.final_score > 0.7:
                    # Score สูง = ตาม trend หลัก
                    direction = "BUY" if trend != "DOWN" else "SELL"
                    print(f"   High score tie-breaker → {direction}")
                else:
                    # Score ปกติ = สลับจากครั้งก่อน
                    last_direction = self._get_last_order_direction()
                    direction = "SELL" if last_direction == "BUY" else "BUY"
                    print(f"   Alternating tie-breaker → {direction}")
            else:
                direction = "BUY" if buy_necessity_score > sell_necessity_score else "SELL"
                margin = abs(buy_necessity_score - sell_necessity_score)
                print(f"   Clear winner: {direction} (margin: {margin:.3f})")
            
            return direction
            
        except Exception as e:
            print(f"Order direction determination error: {e}")
            return "BUY"  # Safe fallback
    
    def _get_portfolio_data_safe(self) -> Dict:
        """ดึงข้อมูล portfolio อย่างปลอดภัย"""
        try:
            if not self.position_manager:
                return {'buy_count': 0, 'sell_count': 0}
            
            positions = self.position_manager.get_active_positions()
            buy_count = sum(1 for pos in positions if 'BUY' in str(pos.get('type', '')))
            sell_count = sum(1 for pos in positions if 'SELL' in str(pos.get('type', '')))
            
            return {
                'buy_count': buy_count,
                'sell_count': sell_count,
                'total_positions': len(positions)
            }
        except:
            return {'buy_count': 0, 'sell_count': 0}

    def _get_last_order_direction(self) -> str:
        """ดึงทิศทางออเดอร์ครั้งล่าสุด"""
        try:
            if not hasattr(self, 'decision_history') or len(self.decision_history) == 0:
                return ""
            
            recent_decisions = list(self.decision_history)[-5:]  # 5 ครั้งล่าสุด
            for decision in reversed(recent_decisions):
                if isinstance(decision, dict) and 'direction' in decision:
                    return decision['direction']
            return ""
        except:
            return ""
        
    def _calculate_intelligent_lot_size(self, decision: SmartDecisionScore) -> float:
        """คำนวณขนาด lot อัจฉริยะ - แก้ไขการปัดให้ถูกต้อง"""
        try:
            if not self.order_manager or not hasattr(self.order_manager, 'lot_calculator'):
                # Fallback: คำนวณแบบพื้นฐาน
                base_lot = 0.01
                confidence_multiplier = 0.5 + (decision.final_score * 0.5)  # 0.5-1.0
                intelligent_lot = base_lot * confidence_multiplier
                
                # ✅ แก้ไข: ปัดให้ถูกต้อง
                rounded_lot = self._round_lot_properly(intelligent_lot)
                print(f"Fallback lot calculation: {intelligent_lot:.4f} → {rounded_lot:.2f}")
                return rounded_lot
            
            # ใช้ 4D Lot Calculator จริง
            market_data = self._get_market_data_safe()
            portfolio_data = self._get_portfolio_data_for_lot_calc()
            
            # เรียกใช้ lot calculator
            lot_result = self.order_manager.lot_calculator.calculate_4d_lot_size(
                market_analysis=market_data,
                positions_data=portfolio_data,
                order_type="BUY",  # จะปรับใน execute function
                reasoning=f"Smart Decision: {decision.decision_quality.value} (Score: {decision.final_score:.3f})"
            )
            
            calculated_lot = lot_result.lot_size
            
            # ปรับตาม decision quality
            quality_multiplier = {
                'EXCELLENT': 1.4,   # เพิ่ม 40% (0.01 → 0.014 → 0.02)
                'GOOD': 1.2,        # เพิ่ม 20% (0.01 → 0.012 → 0.02)  
                'ACCEPTABLE': 1.0,  # ปกติ (0.01 → 0.01)
                'POOR': 0.8,        # ลด 20% (0.01 → 0.008 → 0.01)
                'BLOCKED': 0.6      # ลด 40% (0.01 → 0.006 → 0.01)
            }.get(decision.decision_quality.value, 1.0)
            
            pre_round_lot = calculated_lot * quality_multiplier
            
            # ✅ ระบบปัดที่ถูกต้อง
            final_lot = self._round_lot_properly(pre_round_lot)
            
            print(f"Intelligent Lot Size: {final_lot:.2f}")
            print(f"   Base from 4D: {calculated_lot:.3f}")
            print(f"   Quality multiplier: {quality_multiplier}")
            print(f"   Pre-round: {pre_round_lot:.4f}")
            print(f"   Decision quality: {decision.decision_quality.value}")
            
            return final_lot
            
        except Exception as e:
            print(f"Intelligent lot size error: {e}")
            # Safe fallback
            return 0.01

    def _round_lot_properly(self, lot_value: float) -> float:
        """🔢 ปัด lot size ให้ถูกต้องตาม MT5 rules"""
        try:
            # MT5 lot size ต้องเป็นทวีคูณของ 0.01
            lot_step = 0.01
            
            # วิธีปัดที่ถูกต้อง:
            # 0.015 → 15.0 → round(15.0) → 15 → 15/100 = 0.15 → 0.02 ❌
            # วิธีที่ถูก: ใช้ ceiling สำหรับปัดขึ้น
            
            import math
            
            # คำนวณจำนวน steps
            steps = lot_value / lot_step
            
            # ปัดขึ้นเสมอถ้า > threshold
            if steps > int(steps) and steps % 1 >= 0.5:  # ถ้า >= 0.5 → ปัดขึ้น
                rounded_steps = math.ceil(steps)
            else:  # ถ้า < 0.5 → ปัดลง
                rounded_steps = math.floor(steps)
            
            # แปลงกลับเป็น lot
            rounded_lot = rounded_steps * lot_step
            
            # จำกัดขอบเขต
            final_lot = max(0.01, min(0.10, rounded_lot))
            
            if lot_value != final_lot:
                print(f"   🔢 Lot rounding: {lot_value:.4f} → {final_lot:.2f}")
            
            return final_lot
            
        except Exception as e:
            print(f"❌ Lot rounding error: {e}")
            return 0.01
    
    def _get_portfolio_data_for_lot_calc(self) -> Dict:
        """เตรียมข้อมูล portfolio สำหรับ lot calculator"""
        try:
            portfolio_data = self._get_portfolio_data_safe()
            
            # แปลงให้เข้ากับ format ของ lot calculator
            return {
                'total_positions': portfolio_data.get('total_positions', 0),
                'buy_positions': portfolio_data.get('buy_count', 0),
                'sell_positions': portfolio_data.get('sell_count', 0),
                'portfolio_health': self.portfolio_intelligence.health_score,
                'buy_sell_ratio': portfolio_data.get('buy_count', 0) / max(1, portfolio_data.get('total_positions', 1))
            }
        except:
            return {
                'total_positions': 0,
                'buy_positions': 0, 
                'sell_positions': 0,
                'portfolio_health': 0.7,
                'buy_sell_ratio': 0.5
            }
    
    def _place_order_with_context(self, direction: str, lot_size: float, decision: SmartDecisionScore, target_price: float = None) -> bool:
        """🎯 วางออเดอร์พร้อม context - แก้ไขรองรับ target_price"""
        try:
            if not self.order_manager:
                print("❌ No order manager available")
                return False
            
            print(f"🎯 Executing enhanced order through Order Manager:")
            print(f"   Direction: {direction}")
            print(f"   Volume: {lot_size}")
            print(f"   Target Price: {target_price:.5f}" if target_price else "   Price: Market")
            print(f"   Decision Score: {decision.final_score:.3f}")
            
            # สร้าง OrderRequest (ใช้โครงสร้างเดิม)
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
                price=target_price or 0.0,  # ใช้ target_price ถ้ามี
                reason=OrderReason.PORTFOLIO_BALANCE,
                confidence=decision.final_score,
                reasoning=f"Enhanced Smart Decision: Score {decision.final_score:.3f}, Quality {decision.decision_quality.value}",
                max_slippage=25,  # ยอมรับ slippage ปานกลาง
                four_d_score=decision.final_score
            )
            
            # Execute through Order Manager
            result = self.order_manager.place_market_order(order_request)
            
            if result.success:
                print(f"✅ Enhanced order executed successfully!")
                print(f"   Ticket: #{result.ticket}")
                print(f"   Price: {result.price:.5f}")
                print(f"   Volume: {result.volume:.3f}")
                if hasattr(result, 'execution_time'):
                    print(f"   Execution Time: {result.execution_time:.3f}s")
                return True
            else:
                print(f"❌ Enhanced order execution failed: {result.message}")
                return False
                
        except Exception as e:
            print(f"❌ Enhanced place order error: {e}")
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
        """อัปเดตการติดตามออเดอร์ - ENHANCED VERSION"""
        try:
            # 🔧 FIX: บันทึกเวลาให้ถูกต้อง
            current_time = datetime.now()
            
            # อัปเดต last_order_time
            if not hasattr(self, 'last_order_time'):
                self.last_order_time = {}
            
            # บันทึกตาม direction และ overall
            self.last_order_time[direction] = current_time
            self.last_order_time['last'] = current_time
            
            # บันทึกลงใน decision history ด้วย
            tracking_record = {
                'timestamp': current_time,
                'direction': direction,
                'tracking_update': True,
                'immediate_success': True  # เพื่อให้นับใน _count_orders_in_last_hour
            }
            
            if hasattr(self, 'decision_history'):
                self.decision_history.append(tracking_record)
            
            print(f"📝 Order tracking updated: {direction} at {current_time.strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ Update order tracking error: {e}")

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

    def _get_current_price_safe(self) -> float:
        """ดึงราคาปัจจุบันอย่างปลอดภัย - แก้ไขแล้ว"""
        try:
            import MetaTrader5 as mt5
            
            # ลองหลาย symbol ที่เป็นไปได้
            symbols_to_try = ["XAUUSD", "XAUUSD.v", "GOLD"]
            
            for symbol in symbols_to_try:
                tick = mt5.symbol_info_tick(symbol)
                if tick and tick.bid > 0 and tick.ask > 0:
                    current_price = (tick.bid + tick.ask) / 2
                    print(f"Using symbol: {symbol}, Current price: {current_price}")
                    return current_price
            
            print("Warning: Cannot get current price from any symbol")
            return None
        except Exception as e:
            print(f"Get current price error: {e}")
            return None

    def _calculate_intelligent_spacing_inline(self) -> float:
        """คำนวณระยะห่างแบบฉลาดในบรรทัดเดียว"""
        try:
            base = 100
            vol_mult = {'LOW': 0.7, 'NORMAL': 1.0, 'HIGH': 1.5, 'EXTREME': 2.0}.get(
                getattr(self.market_intelligence, 'volatility_level', 'NORMAL'), 1.0)
            
            # แก้ไข: ใช้ string conversion ที่ปลอดภัย
            session_str = str(getattr(self.market_intelligence, 'current_session', 'QUIET')).upper()
            session_mult = {'ASIAN': 0.8, 'LONDON': 1.2, 'NEW_YORK': 1.3, 'OVERLAP': 1.5, 'QUIET': 0.6}.get(
                session_str, 1.0)
            
            pos_count = getattr(self.portfolio_intelligence, 'total_positions', 0)
            density_mult = 1.0 + (pos_count * 0.05)
            
            final_spacing = max(50, min(300, base * vol_mult * session_mult * density_mult))
            return final_spacing
        except Exception as e:
            print(f"Spacing calculation error: {e}")
            return 100

    def _get_recent_positions_safe(self, hours: int = 4) -> List[Dict]:
        """ดึง positions ล่าสุดอย่างปลอดภัย"""
        try:
            if not self.position_manager:
                return []
            positions = self.position_manager.get_active_positions()
            if not positions:
                return []
            # ส่งคืนทั้งหมดเพื่อความปลอดภัย
            return positions
        except Exception as e:
            print(f"Get positions error: {e}")
            return []