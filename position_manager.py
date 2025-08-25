"""
💰 Modern Position Manager - 4D Analysis Enhanced Edition
position_manager.py

Enhanced Features:
- 4-Dimensional Analysis System
- Real-time Recovery Scanner (30-second intervals)
- Smart Hedge Detection & Execution
- Portfolio optimization with AI insights
- No Stop Loss - Focus on Recovery & Hedge

** PRODUCTION READY - 4D AI INTEGRATION **
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
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
    """เหตุผลการปิด Position - Enhanced with 4D AI"""
    PROFIT_TARGET = "PROFIT_TARGET"
    PORTFOLIO_BALANCE = "PORTFOLIO_BALANCE"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"
    MANUAL = "MANUAL"
    EMERGENCY = "EMERGENCY"
    GRID_OPTIMIZATION = "GRID_OPTIMIZATION"
    CORRELATION_HEDGE = "CORRELATION_HEDGE"
    SMART_RECOVERY = "SMART_RECOVERY"
    FOUR_D_AI_RECOVERY = "FOUR_D_AI_RECOVERY"      # ⭐ New 4D AI reason
    HEDGE_OPTIMIZATION = "HEDGE_OPTIMIZATION"       # ⭐ New optimization
    PORTFOLIO_REBALANCE = "PORTFOLIO_REBALANCE"     # ⭐ New rebalancing

class RecoveryStrategy(Enum):
    """กลยุทธ์ Recovery - Enhanced"""
    FULL_HEDGE = "FULL_HEDGE"                      # Hedge ครบทั้งหมด
    PARTIAL_HEDGE = "PARTIAL_HEDGE"                # Hedge บางส่วน
    NET_POSITIVE_CLOSE = "NET_POSITIVE_CLOSE"      # ปิดคู่ที่ net positive
    PROFIT_OFFSET = "PROFIT_OFFSET"                # ใช้กำไรหักล้าง
    STRATEGIC_WAIT = "STRATEGIC_WAIT"              # รอโอกาสที่ดีกว่า
    EMERGENCY_CLOSE = "EMERGENCY_CLOSE"            # ปิดฉุกเฉิน

@dataclass
class Position:
    """ข้อมูล Position from REAL MT5 - Enhanced with 4D Analysis"""
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
    
    # 4D Analysis fields
    four_d_value_score: float = 0.0                # Dimension 1: Position Value
    four_d_safety_impact: float = 0.0              # Dimension 2: Safety Impact
    four_d_hedge_potential: float = 0.0            # Dimension 3: Hedge Potential
    four_d_market_alignment: float = 0.0           # Dimension 4: Market Alignment
    recovery_priority: float = 0.0                 # Priority for recovery
    hedge_candidates: List[int] = field(default_factory=list)  # Potential hedge partners
    
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
    
    @property
    def four_d_overall_score(self) -> float:
        """คะแนน 4D รวม - Same weights as rule engine"""
        return (
            self.four_d_value_score * 0.30 +
            self.four_d_safety_impact * 0.25 +
            self.four_d_hedge_potential * 0.25 +
            self.four_d_market_alignment * 0.20
        )

@dataclass
class HedgeOpportunity:
    """โอกาสการ Hedge - Enhanced with 4D"""
    primary_position: Position               # Position ที่ต้องการ hedge
    hedge_positions: List[Position]          # Position ที่จะใช้ hedge
    strategy: RecoveryStrategy               # กลยุทธ์ที่แนะนำ
    net_result: float                        # ผลลัพธ์สุทธิ
    confidence: float                        # ความเชื่อมั่น (0-1)
    four_d_alignment: float                  # ความสอดคล้องกับ 4D Analysis
    urgency_level: float                     # ระดับความเร่งด่วน (0-1)
    execution_order: List[int]               # ลำดับการ execute
    expected_recovery: float                 # การ recover ที่คาดหวัง
    
    @property
    def is_highly_recommended(self) -> bool:
        """แนะนำอย่างยิ่งหรือไม่"""
        return (self.confidence > 0.8 and 
                self.four_d_alignment > 0.7 and 
                self.net_result > 0)

@dataclass
class PortfolioStatus:
    """สถานะ Portfolio - Enhanced with 4D Insights"""
    total_positions: int
    buy_positions: int
    sell_positions: int
    total_profit: float
    total_loss: float
    net_profit: float
    profitable_positions: List[Position]
    losing_positions: List[Position]
    position_balance: float                  # 0.0-1.0 (0=all sell, 1=all buy)
    risk_level: float                        # 0.0-1.0
    margin_usage: float                      # 0.0-1.0
    equity: float
    balance: float
    free_margin: float
    
    # 4D Analysis Portfolio metrics
    four_d_portfolio_health: float = 0.0    # Overall portfolio health (0-1)
    recovery_opportunities: List[HedgeOpportunity] = field(default_factory=list)
    hedge_coverage_ratio: float = 0.0       # ร้อยละของ positions ที่มี hedge
    portfolio_efficiency: float = 0.0       # ประสิทธิภาพการใช้เงินทุน
    stress_test_score: float = 0.0          # ทนต่อความเครียดได้แค่ไหน
    
    @property
    def balance_ratio(self) -> float:
        """อัตราสมดุล BUY:SELL"""
        if self.total_positions == 0:
            return 0.5
        return self.buy_positions / self.total_positions
    
    @property  
    def is_balanced(self) -> bool:
        """Portfolio สมดุลหรือไม่"""
        return 0.3 <= self.balance_ratio <= 0.7
    
    @property
    def dominant_side(self) -> str:
        """ด้านที่เด่นของ portfolio"""
        if self.balance_ratio > 0.6:
            return "BUY_HEAVY"
        elif self.balance_ratio < 0.4:
            return "SELL_HEAVY"
        else:
            return "BALANCED"

# ========================================================================================
# 💰 ENHANCED POSITION MANAGER CLASS
# ========================================================================================

class PositionManager:
    """
    💰 Enhanced Position Manager - 4D Analysis Edition
    
    ความสามารถใหม่:
    - 4-Dimensional Position Analysis
    - Real-time Recovery Scanner (30-second intervals)
    - Smart Hedge Detection & Execution
    - Portfolio optimization with AI insights
    - Advanced recovery strategies
    """
    
    def __init__(self, mt5_connector, config):
        """Initialize Enhanced Position Manager"""
        # Core components
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Trading parameters
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.max_positions = config.get("trading", {}).get("max_positions", 20)
        
        # 4D Analysis parameters
        self.four_d_config = {
            "analysis_interval": 30,              # วินาที - Real-time analysis
            "recovery_scan_interval": 30,         # วินาที - Recovery scanning
            "min_recovery_confidence": 0.6,       # ความเชื่อมั่นขั้นต่ำสำหรับ recovery
            "min_hedge_net_positive": 5.0,        # $5 ขั้นต่ำสำหรับ net positive hedge
            "max_position_age_hours": 48,         # ชั่วโมงสูงสุดก่อนพิจารณา recovery เร่งด่วน
            "portfolio_health_threshold": 0.4,    # เกณฑ์ portfolio health
            "hedge_urgency_threshold": 0.8        # เกณฑ์ความเร่งด่วนของ hedge
        }
        
        # Position tracking
        self.active_positions: Dict[int, Position] = {}
        self.position_history = deque(maxlen=500)
        self.close_performance = defaultdict(lambda: {"count": 0, "success": 0, "total_profit": 0.0})
        
        # 4D Analysis state
        self.last_4d_analysis = None
        self.analysis_history = deque(maxlen=100)
        self.recovery_scanner_running = False
        self.scanner_thread = None
        self.last_recovery_scan = datetime.now()
        
        # Enhanced tracking
        self.hedge_execution_stats = {
            "total_attempts": 0,
            "successful_hedges": 0,
            "total_recovery": 0.0,
            "avg_confidence": 0.0,
            "strategy_performance": defaultdict(int)
        }
        
        # Portfolio optimization
        self.portfolio_optimizer_running = False
        self.optimization_history = deque(maxlen=50)
        
        print("💰 Enhanced 4D Position Manager initialized")
        print(f"   Symbol: {self.symbol}")
        print(f"   4D Analysis Interval: {self.four_d_config['analysis_interval']}s")
        print(f"   Recovery Scanner: {self.four_d_config['recovery_scan_interval']}s")
    
    # ========================================================================================
    # 🧠 4D ANALYSIS SYSTEM - CORE FEATURES
    # ========================================================================================
    
    def start_4d_analysis_system(self):
        """🧠 เริ่ม 4D Analysis System"""
        try:
            if self.recovery_scanner_running:
                print("⚠️ 4D Analysis system already running")
                return
            
            self.recovery_scanner_running = True
            self.scanner_thread = threading.Thread(target=self._4d_analysis_loop, daemon=True)
            self.scanner_thread.start()
            
            print("🧠 4D Analysis System started")
            print(f"   Analysis Interval: {self.four_d_config['analysis_interval']}s")
            print(f"   Recovery Scanning: {self.four_d_config['recovery_scan_interval']}s")
            
        except Exception as e:
            self.log(f"❌ Start 4D system error: {e}")
    
    def stop_4d_analysis_system(self):
        """🛑 หยุด 4D Analysis System"""
        try:
            self.recovery_scanner_running = False
            if self.scanner_thread:
                self.scanner_thread.join(timeout=5)
            
            print("🛑 4D Analysis System stopped")
            
        except Exception as e:
            self.log(f"❌ Stop 4D system error: {e}")
    
    def _4d_analysis_loop(self):
        """🔄 4D Analysis Main Loop"""
        print("🔄 4D Analysis loop started")
        
        while self.recovery_scanner_running:
            try:
                loop_start = time.time()
                
                # 1. Update positions
                self.update_positions()
                
                # 2. Perform 4D Analysis on all positions
                self._perform_4d_position_analysis()
                
                # 3. Scan for recovery opportunities
                recovery_opportunities = self._scan_recovery_opportunities()
                
                # 4. Execute high-priority recovery actions
                if recovery_opportunities:
                    self._execute_priority_recovery(recovery_opportunities)
                
                # 5. Portfolio optimization check
                self._check_portfolio_optimization()
                
                # 6. Update analysis history
                self._update_analysis_history()
                
                # Dynamic sleep based on workload
                loop_time = time.time() - loop_start
                sleep_time = max(1.0, self.four_d_config['analysis_interval'] - loop_time)
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"❌ 4D Analysis loop error: {e}")
                time.sleep(5)  # Wait before retry
        
        print("🛑 4D Analysis loop stopped")
    
    def _perform_4d_position_analysis(self):
        """🧠 ดำเนินการวิเคราะห์ 4D สำหรับทุก positions"""
        try:
            if not self.active_positions:
                return
            
            print(f"🧠 === 4D POSITION ANALYSIS ({len(self.active_positions)} positions) ===")
            
            for ticket, position in self.active_positions.items():
                # Dimension 1: Position Value Analysis (30%)
                position.four_d_value_score = self._analyze_position_value(position)
                
                # Dimension 2: Safety Impact Analysis (25%)
                position.four_d_safety_impact = self._analyze_safety_impact(position)
                
                # Dimension 3: Hedge Potential Analysis (25%)
                position.four_d_hedge_potential = self._analyze_hedge_potential(position)
                
                # Dimension 4: Market Alignment Analysis (20%)
                position.four_d_market_alignment = self._analyze_market_alignment(position)
                
                # Calculate recovery priority
                position.recovery_priority = self._calculate_recovery_priority(position)
                
                print(f"   📊 Position #{ticket}:")
                print(f"      4D Scores: V:{position.four_d_value_score:.2f} | S:{position.four_d_safety_impact:.2f} | H:{position.four_d_hedge_potential:.2f} | M:{position.four_d_market_alignment:.2f}")
                print(f"      Overall: {position.four_d_overall_score:.2f} | Priority: {position.recovery_priority:.2f}")
            
            # Store analysis timestamp
            self.last_4d_analysis = datetime.now()
            
        except Exception as e:
            print(f"❌ 4D position analysis error: {e}")
    
    def _analyze_position_value(self, position: Position) -> float:
        """Dimension 1: วิเคราะห์มูลค่า Position (30% weight)"""
        try:
            score_factors = []
            
            # 1. Profit/Loss assessment (40%)
            if position.total_profit > 0:
                # Profitable position
                profit_score = min(position.total_profit / 50, 1.0)  # Scale to $50 max
            else:
                # Loss position - penalty based on loss amount
                profit_score = max(0, 1 + (position.total_profit / 200))  # -$200 = 0 score
            
            score_factors.append(("profit", profit_score, 0.40))
            
            # 2. Age vs Performance correlation (25%)
            age_days = position.age_hours / 24
            if position.total_profit > 0:
                # Profitable - newer is better (less risk exposure)
                age_score = max(0, 1 - (age_days / 7))  # Decline over 7 days
            else:
                # Loss - older needs more urgent attention
                age_score = min(age_days / 2, 1.0)  # Increase urgency over 2 days
            
            score_factors.append(("age_performance", age_score, 0.25))
            
            # 3. Volume efficiency (20%)
            # Larger positions have higher impact
            volume_score = min(position.volume / 0.1, 1.0)  # Scale to 0.1 lots
            score_factors.append(("volume", volume_score, 0.20))
            
            # 4. Margin efficiency (15%)
            # Estimate margin usage
            estimated_margin = position.volume * 100  # Rough estimate
            margin_score = min(estimated_margin / 500, 1.0)  # Scale to $500
            score_factors.append(("margin", margin_score, 0.15))
            
            # Calculate weighted average
            weighted_sum = sum(score * weight for name, score, weight in score_factors)
            total_weight = sum(weight for name, score, weight in score_factors)
            
            final_score = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, final_score))
            
        except Exception as e:
            print(f"❌ Position value analysis error: {e}")
            return 0.5
    
    def _analyze_safety_impact(self, position: Position) -> float:
        """Dimension 2: วิเคราะห์ผลกระทบต่อความปลอดภัย (25% weight)"""
        try:
            score_factors = []
            
            # 1. Risk contribution to portfolio (40%)
            total_exposure = sum(pos.volume for pos in self.active_positions.values())
            if total_exposure > 0:
                position_risk_ratio = position.volume / total_exposure
                # Lower ratio = safer
                risk_score = 1 - min(position_risk_ratio * 5, 1.0)  # Penalize if >20% of portfolio
            else:
                risk_score = 0.5
            
            score_factors.append(("risk_contribution", risk_score, 0.40))
            
            # 2. Loss potential impact (30%)
            if position.total_profit >= 0:
                loss_impact_score = 0.8  # Profitable positions have lower risk
            else:
                # Calculate potential further loss
                current_loss = abs(position.total_profit)
                potential_loss_score = max(0, 1 - (current_loss / 300))  # Scale to $300
                loss_impact_score = potential_loss_score
            
            score_factors.append(("loss_impact", loss_impact_score, 0.30))
            
            # 3. Portfolio balance impact (20%)
            buy_count = sum(1 for pos in self.active_positions.values() if pos.type == PositionType.BUY)
            total_count = len(self.active_positions)
            current_ratio = buy_count / total_count if total_count > 0 else 0.5
            
            # If closing this position would improve balance
            if position.type == PositionType.BUY and current_ratio > 0.6:
                balance_score = 0.8  # Good to close BUY when BUY-heavy
            elif position.type == PositionType.SELL and current_ratio < 0.4:
                balance_score = 0.8  # Good to close SELL when SELL-heavy
            else:
                balance_score = 0.4  # Neutral impact
            
            score_factors.append(("balance_impact", balance_score, 0.20))
            
            # 4. Correlation risk (10%)
            # Simplified - all positions on same symbol have high correlation
            correlation_score = 0.3 if len(self.active_positions) > 5 else 0.6
            score_factors.append(("correlation", correlation_score, 0.10))
            
            # Calculate weighted average
            weighted_sum = sum(score * weight for name, score, weight in score_factors)
            total_weight = sum(weight for name, score, weight in score_factors)
            
            final_score = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, final_score))
            
        except Exception as e:
            print(f"❌ Safety impact analysis error: {e}")
            return 0.5
    
    def _analyze_hedge_potential(self, position: Position) -> float:
        """Dimension 3: วิเคราะห์ศักยภาพ Hedge (25% weight)"""
        try:
            score_factors = []
            
            # 1. Hedge pair availability (35%)
            hedge_candidates = []
            target_type = PositionType.SELL if position.type == PositionType.BUY else PositionType.BUY
            
            for other_pos in self.active_positions.values():
                if (other_pos.ticket != position.ticket and 
                    other_pos.type == target_type):
                    
                    # Check if they can offset each other
                    net_result = position.total_profit + other_pos.total_profit
                    if net_result > -50:  # Within reasonable range
                        hedge_candidates.append({
                            'position': other_pos,
                            'net_result': net_result,
                            'compatibility': self._calculate_hedge_compatibility(position, other_pos)
                        })
            
            position.hedge_candidates = [candidate['position'].ticket for candidate in hedge_candidates]
            
            if hedge_candidates:
                best_hedge = max(hedge_candidates, key=lambda x: x['compatibility'])
                hedge_availability_score = min(len(hedge_candidates) / 3, 1.0)  # Max at 3 candidates
            else:
                hedge_availability_score = 0.0
            
            score_factors.append(("hedge_availability", hedge_availability_score, 0.35))
            
            # 2. Net positive potential (30%)
            if hedge_candidates:
                positive_hedges = [h for h in hedge_candidates if h['net_result'] > 0]
                if positive_hedges:
                    best_net = max(h['net_result'] for h in positive_hedges)
                    net_positive_score = min(best_net / 30, 1.0)  # Scale to $30
                else:
                    # Even if net negative, smaller loss is better
                    best_net = max(h['net_result'] for h in hedge_candidates)
                    net_positive_score = max(0, (best_net + 100) / 100)  # Scale from -$100
            else:
                net_positive_score = 0.0
            
            score_factors.append(("net_positive", net_positive_score, 0.30))
            
            # 3. Volume compatibility (20%)
            if hedge_candidates:
                volume_compatibilities = []
                for candidate in hedge_candidates:
                    other_volume = candidate['position'].volume
                    volume_ratio = min(position.volume, other_volume) / max(position.volume, other_volume)
                    volume_compatibilities.append(volume_ratio)
                
                avg_volume_compatibility = np.mean(volume_compatibilities)
                volume_score = avg_volume_compatibility
            else:
                volume_score = 0.0
            
            score_factors.append(("volume_compatibility", volume_score, 0.20))
            
            # 4. Timing synergy (15%)
            if hedge_candidates:
                timing_scores = []
                for candidate in hedge_candidates:
                    other_age = candidate['position'].age_hours
                    age_diff = abs(position.age_hours - other_age)
                    timing_score = max(0, 1 - (age_diff / 24))  # Best if opened within 24 hours
                    timing_scores.append(timing_score)
                
                avg_timing_score = np.mean(timing_scores)
            else:
                avg_timing_score = 0.0
            
            score_factors.append(("timing_synergy", avg_timing_score, 0.15))
            
            # Calculate weighted average
            weighted_sum = sum(score * weight for name, score, weight in score_factors)
            total_weight = sum(weight for name, score, weight in score_factors)
            
            final_score = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, final_score))
            
        except Exception as e:
            print(f"❌ Hedge potential analysis error: {e}")
            return 0.5
    
    def _analyze_market_alignment(self, position: Position) -> float:
        """Dimension 4: วิเคราะห์การสอดคล้องกับตลาด (20% weight)"""
        try:
            score_factors = []
            
            # 1. Current session alignment (30%)
            current_hour = datetime.now().hour
            if 7 <= current_hour <= 17:  # London + NY sessions
                session_score = 0.8
            elif 1 <= current_hour <= 7:  # Asian session
                session_score = 0.6
            else:  # Quiet hours
                session_score = 0.4
            
            score_factors.append(("session", session_score, 0.30))
            
            # 2. Position age alignment (25%)
            # Newer positions are more aligned with current market
            age_alignment = max(0, 1 - (position.age_hours / 48))  # Decline over 48 hours
            score_factors.append(("age_alignment", age_alignment, 0.25))
            
            # 3. Volume appropriateness (25%)
            # Standard lot sizes are more market-aligned
            if 0.01 <= position.volume <= 0.05:
                volume_alignment = 1.0  # Standard range
            elif 0.005 <= position.volume <= 0.1:
                volume_alignment = 0.8  # Acceptable range
            else:
                volume_alignment = 0.4  # Unusual sizes
            
            score_factors.append(("volume_alignment", volume_alignment, 0.25))
            
            # 4. Market efficiency (20%)
            # Positions with reasonable spread exposure
            current_spread = 0.003  # Approximate spread
            position_cost = position.commission + abs(position.swap)
            efficiency = max(0, 1 - (position_cost / 10))  # Scale to $10
            
            score_factors.append(("efficiency", efficiency, 0.20))
            
            # Calculate weighted average
            weighted_sum = sum(score * weight for name, score, weight in score_factors)
            total_weight = sum(weight for name, score, weight in score_factors)
            
            final_score = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, final_score))
            
        except Exception as e:
            print(f"❌ Market alignment analysis error: {e}")
            return 0.5
    
    def _calculate_recovery_priority(self, position: Position) -> float:
        """คำนวณลำดับความสำคัญสำหรับ Recovery"""
        try:
            priority_factors = []
            
            # 1. Loss magnitude (30%)
            if position.total_profit < 0:
                loss_amount = abs(position.total_profit)
                loss_priority = min(loss_amount / 200, 1.0)  # Scale to $200
            else:
                loss_priority = 0.1  # Low priority for profitable positions
            
            priority_factors.append(("loss", loss_priority, 0.30))
            
            # 2. Age urgency (25%)
            age_urgency = min(position.age_hours / 48, 1.0)  # Max urgency at 48 hours
            priority_factors.append(("age", age_urgency, 0.25))
            
            # 3. Hedge potential (25%)
            hedge_priority = position.four_d_hedge_potential
            priority_factors.append(("hedge", hedge_priority, 0.25))
            
            # 4. Safety impact (20%)
            safety_priority = 1 - position.four_d_safety_impact  # Invert - lower safety = higher priority
            priority_factors.append(("safety", safety_priority, 0.20))
            
            # Calculate weighted average
            weighted_sum = sum(priority * weight for name, priority, weight in priority_factors)
            total_weight = sum(weight for name, priority, weight in priority_factors)
            
            final_priority = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, final_priority))
            
        except Exception as e:
            print(f"❌ Recovery priority calculation error: {e}")
            return 0.5
    
    def _calculate_hedge_compatibility(self, pos1: Position, pos2: Position) -> float:
        """คำนวณความเข้ากันได้ของ hedge pair"""
        try:
            compatibility_factors = []
            
            # 1. Net result (40%)
            net_result = pos1.total_profit + pos2.total_profit
            if net_result > 0:
                net_score = min(net_result / 30, 1.0)
            else:
                net_score = max(0, (net_result + 100) / 100)  # Scale from -$100
            
            compatibility_factors.append(net_score * 0.40)
            
            # 2. Volume ratio (30%)
            volume_ratio = min(pos1.volume, pos2.volume) / max(pos1.volume, pos2.volume)
            compatibility_factors.append(volume_ratio * 0.30)
            
            # 3. Age difference (20%)
            age_diff = abs(pos1.age_hours - pos2.age_hours)
            age_score = max(0, 1 - (age_diff / 24))
            compatibility_factors.append(age_score * 0.20)
            
            # 4. Combined 4D score (10%)
            combined_4d = (pos1.four_d_overall_score + pos2.four_d_overall_score) / 2
            compatibility_factors.append(combined_4d * 0.10)
            
            return sum(compatibility_factors)
            
        except Exception as e:
            print(f"❌ Hedge compatibility calculation error: {e}")
            return 0.0
    
    # ========================================================================================
    # 🔍 REAL-TIME RECOVERY SCANNER
    # ========================================================================================
    
    def _scan_recovery_opportunities(self) -> List[HedgeOpportunity]:
        """🔍 สแกนโอกาส Recovery แบบ Real-time"""
        try:
            if not self.active_positions:
                return []
            
            print(f"🔍 === RECOVERY OPPORTUNITY SCAN ===")
            
            opportunities = []
            
            # หา losing positions ที่ต้องการ recovery
            losing_positions = [pos for pos in self.active_positions.values() 
                              if pos.total_profit < -10]  # Loss > $10
            
            if not losing_positions:
                print("   ℹ️ No significant losing positions found")
                return []
            
            # เรียงตาม recovery priority
            losing_positions.sort(key=lambda p: p.recovery_priority, reverse=True)
            
            print(f"   📍 Found {len(losing_positions)} positions needing recovery")
            
            for loss_pos in losing_positions[:5]:  # Top 5 priority positions
                opportunity = self._analyze_single_position_recovery(loss_pos)
                if opportunity and opportunity.confidence > self.four_d_config['min_recovery_confidence']:
                    opportunities.append(opportunity)
                    
                    print(f"   ✅ Recovery opportunity for #{loss_pos.ticket}:")
                    print(f"      Strategy: {opportunity.strategy.value}")
                    print(f"      Net Result: ${opportunity.net_result:.2f}")
                    print(f"      Confidence: {opportunity.confidence:.2f}")
                    print(f"      4D Alignment: {opportunity.four_d_alignment:.2f}")
            
            # เรียงตามความเร่งด่วนและความเชื่อมั่น
            opportunities.sort(key=lambda o: (o.urgency_level * o.confidence), reverse=True)
            
            self.last_recovery_scan = datetime.now()
            return opportunities
            
        except Exception as e:
            print(f"❌ Recovery opportunity scan error: {e}")
            return []
    
    def _analyze_single_position_recovery(self, target_position: Position) -> Optional[HedgeOpportunity]:
        """วิเคราะห์โอกาส Recovery สำหรับ position เดียว"""
        try:
            if not target_position.hedge_candidates:
                return None
            
            # หา hedge positions ที่เป็นไปได้
            hedge_positions = []
            for ticket in target_position.hedge_candidates:
                if ticket in self.active_positions:
                    hedge_pos = self.active_positions[ticket]
                    if hedge_pos.total_profit > 0:  # Only profitable hedge candidates
                        hedge_positions.append(hedge_pos)
            
            if not hedge_positions:
                return None
            
            # วิเคราะห์ strategy ที่ดีที่สุด
            best_strategy = None
            best_net_result = float('-inf')
            best_confidence = 0.0
            
            # Strategy 1: Single best hedge
            best_hedge = max(hedge_positions, key=lambda p: p.total_profit)
            single_net = target_position.total_profit + best_hedge.total_profit
            
            if single_net > best_net_result:
                best_strategy = RecoveryStrategy.NET_POSITIVE_CLOSE
                best_net_result = single_net
                selected_hedges = [best_hedge]
            
            # Strategy 2: Multiple hedge combination
            if len(hedge_positions) > 1:
                total_hedge_profit = sum(p.total_profit for p in hedge_positions)
                multi_net = target_position.total_profit + total_hedge_profit
                
                if multi_net > best_net_result:
                    best_strategy = RecoveryStrategy.FULL_HEDGE
                    best_net_result = multi_net
                    selected_hedges = hedge_positions
            
            # Strategy 3: Partial hedge (best subset)
            if len(hedge_positions) > 2:
                # Find optimal subset
                for i in range(2, len(hedge_positions)):
                    subset = hedge_positions[:i]
                    subset_profit = sum(p.total_profit for p in subset)
                    partial_net = target_position.total_profit + subset_profit
                    
                    if partial_net > 0 and partial_net > best_net_result:
                        best_strategy = RecoveryStrategy.PARTIAL_HEDGE
                        best_net_result = partial_net
                        selected_hedges = subset
            
            if not best_strategy or best_net_result < -100:  # Don't suggest if too negative
                return None
            
            # คำนวณ confidence และ metrics
            confidence = self._calculate_recovery_confidence(target_position, selected_hedges, best_net_result)
            four_d_alignment = self._calculate_4d_alignment(target_position, selected_hedges)
            urgency_level = self._calculate_urgency_level(target_position)
            
            # คำนวณ execution order
            execution_order = self._plan_execution_order(target_position, selected_hedges)
            
            # Expected recovery calculation
            expected_recovery = max(0, best_net_result) if best_net_result > 0 else abs(target_position.total_profit) * 0.8
            
            return HedgeOpportunity(
                primary_position=target_position,
                hedge_positions=selected_hedges,
                strategy=best_strategy,
                net_result=best_net_result,
                confidence=confidence,
                four_d_alignment=four_d_alignment,
                urgency_level=urgency_level,
                execution_order=execution_order,
                expected_recovery=expected_recovery
            )
            
        except Exception as e:
            print(f"❌ Single position recovery analysis error: {e}")
            return None
    
    def _calculate_recovery_confidence(self, target_pos: Position, hedge_positions: List[Position], net_result: float) -> float:
        """คำนวณความเชื่อมั่นในการ Recovery"""
        try:
            confidence_factors = []
            
            # 1. Net result quality (35%)
            if net_result > 20:
                net_confidence = 1.0
            elif net_result > 5:
                net_confidence = 0.8
            elif net_result > 0:
                net_confidence = 0.6
            elif net_result > -50:
                net_confidence = 0.4
            else:
                net_confidence = 0.2
            
            confidence_factors.append(("net_result", net_confidence, 0.35))
            
            # 2. 4D scores alignment (25%)
            all_positions = [target_pos] + hedge_positions
            avg_4d_score = np.mean([pos.four_d_overall_score for pos in all_positions])
            confidence_factors.append(("4d_alignment", avg_4d_score, 0.25))
            
            # 3. Hedge quality (20%)
            hedge_profits = [pos.total_profit for pos in hedge_positions]
            if hedge_profits:
                min_hedge_profit = min(hedge_profits)
                avg_hedge_profit = np.mean(hedge_profits)
                hedge_quality = min(avg_hedge_profit / 30, 1.0)  # Scale to $30
            else:
                hedge_quality = 0.0
            
            confidence_factors.append(("hedge_quality", hedge_quality, 0.20))
            
            # 4. Risk/reward ratio (20%)
            potential_risk = abs(min(target_pos.total_profit, 0)) + sum(max(-pos.total_profit, 0) for pos in hedge_positions)
            potential_reward = max(net_result, 0)
            
            if potential_risk > 0:
                risk_reward_ratio = min(potential_reward / potential_risk, 1.0)
            else:
                risk_reward_ratio = 1.0 if potential_reward > 0 else 0.0
            
            confidence_factors.append(("risk_reward", risk_reward_ratio, 0.20))
            
            # Calculate weighted confidence
            weighted_sum = sum(score * weight for name, score, weight in confidence_factors)
            total_weight = sum(weight for name, score, weight in confidence_factors)
            
            final_confidence = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, final_confidence))
            
        except Exception as e:
            print(f"❌ Recovery confidence calculation error: {e}")
            return 0.5
    
    def _calculate_4d_alignment(self, target_pos: Position, hedge_positions: List[Position]) -> float:
        """คำนวณการสอดคล้องของ 4D Analysis"""
        try:
            all_positions = [target_pos] + hedge_positions
            
            # 1. Overall 4D scores
            avg_4d_overall = np.mean([pos.four_d_overall_score for pos in all_positions])
            
            # 2. Hedge potential consistency
            avg_hedge_potential = np.mean([pos.four_d_hedge_potential for pos in all_positions])
            
            # 3. Safety impact balance
            avg_safety_impact = np.mean([pos.four_d_safety_impact for pos in all_positions])
            
            # 4. Market alignment
            avg_market_alignment = np.mean([pos.four_d_market_alignment for pos in all_positions])
            
            # Combined alignment score
            alignment_score = (
                avg_4d_overall * 0.40 +
                avg_hedge_potential * 0.30 +
                avg_safety_impact * 0.20 +
                avg_market_alignment * 0.10
            )
            
            return max(0, min(1, alignment_score))
            
        except Exception as e:
            print(f"❌ 4D alignment calculation error: {e}")
            return 0.5
    
    def _calculate_urgency_level(self, position: Position) -> float:
        """คำนวณระดับความเร่งด่วน"""
        try:
            urgency_factors = []
            
            # 1. Loss magnitude (40%)
            if position.total_profit < 0:
                loss_amount = abs(position.total_profit)
                loss_urgency = min(loss_amount / 300, 1.0)  # Scale to $300
            else:
                loss_urgency = 0.0
            
            urgency_factors.append(("loss_magnitude", loss_urgency, 0.40))
            
            # 2. Age factor (30%)
            age_urgency = min(position.age_hours / 72, 1.0)  # Max urgency at 72 hours
            urgency_factors.append(("age", age_urgency, 0.30))
            
            # 3. Portfolio impact (20%)
            portfolio_impact = 1 - position.four_d_safety_impact  # Lower safety = higher urgency
            urgency_factors.append(("portfolio", portfolio_impact, 0.20))
            
            # 4. Market timing (10%)
            current_hour = datetime.now().hour
            if 7 <= current_hour <= 17:  # Active trading hours
                timing_urgency = 0.8
            else:
                timing_urgency = 0.4
            
            urgency_factors.append(("timing", timing_urgency, 0.10))
            
            # Calculate weighted urgency
            weighted_sum = sum(urgency * weight for name, urgency, weight in urgency_factors)
            total_weight = sum(weight for name, urgency, weight in urgency_factors)
            
            final_urgency = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, final_urgency))
            
        except Exception as e:
            print(f"❌ Urgency level calculation error: {e}")
            return 0.5
    
    def _plan_execution_order(self, target_pos: Position, hedge_positions: List[Position]) -> List[int]:
        """วางแผนลำดับการ Execute"""
        try:
            execution_plan = []
            
            # 1. เรียงตาม profit descending (ปิดกำไรมากก่อน)
            hedge_positions_sorted = sorted(hedge_positions, key=lambda p: p.total_profit, reverse=True)
            
            # 2. เพิ่ม hedge positions
            for pos in hedge_positions_sorted:
                execution_plan.append(pos.ticket)
            
            # 3. เพิ่ม target position ท้ายสุด
            execution_plan.append(target_pos.ticket)
            
            return execution_plan
            
        except Exception as e:
            print(f"❌ Execution order planning error: {e}")
            return []
    
    # ========================================================================================
    # ⚡ SMART RECOVERY EXECUTION
    # ========================================================================================
    
    def _execute_priority_recovery(self, opportunities: List[HedgeOpportunity]):
        """⚡ Execute Recovery Actions ที่มี Priority สูง"""
        try:
            if not opportunities:
                return
            
            # Filter high priority opportunities
            high_priority = [
                opp for opp in opportunities 
                if (opp.urgency_level > self.four_d_config['hedge_urgency_threshold'] and
                    opp.confidence > self.four_d_config['min_recovery_confidence'])
            ]
            
            if not high_priority:
                print("   ℹ️ No high-priority recovery opportunities")
                return
            
            print(f"⚡ === EXECUTING PRIORITY RECOVERY ({len(high_priority)} opportunities) ===")
            
            for opportunity in high_priority[:2]:  # Execute top 2 opportunities
                success = self._execute_single_recovery(opportunity)
                
                if success:
                    print(f"   ✅ Recovery executed for #{opportunity.primary_position.ticket}")
                    
                    # Track performance
                    self._track_recovery_execution(opportunity, True)
                    
                    # Add delay between recoveries
                    time.sleep(1)
                else:
                    print(f"   ❌ Recovery failed for #{opportunity.primary_position.ticket}")
                    self._track_recovery_execution(opportunity, False)
            
        except Exception as e:
            print(f"❌ Execute priority recovery error: {e}")
    
    def _execute_single_recovery(self, opportunity: HedgeOpportunity) -> bool:
        """Execute การ Recovery เดียว"""
        try:
            print(f"   🎯 Executing {opportunity.strategy.value} recovery")
            print(f"      Primary: #{opportunity.primary_position.ticket} (${opportunity.primary_position.total_profit:.2f})")
            print(f"      Hedges: {len(opportunity.hedge_positions)} positions")
            print(f"      Expected Net: ${opportunity.net_result:.2f}")
            
            # Execute according to planned order
            closed_tickets = []
            total_secured = 0.0
            
            for ticket in opportunity.execution_order:
                if ticket in self.active_positions:
                    position = self.active_positions[ticket]
                    
                    if self._close_single_position(position, CloseReason.FOUR_D_AI_RECOVERY):
                        closed_tickets.append(ticket)
                        total_secured += position.total_profit
                        print(f"      ✅ Closed #{ticket}: ${position.total_profit:.2f}")
                        
                        # Brief delay between closes
                        time.sleep(0.5)
                    else:
                        print(f"      ❌ Failed to close #{ticket}")
                        # Continue with partial execution
            
            success = len(closed_tickets) >= len(opportunity.execution_order) * 0.7  # 70% success rate
            
            print(f"   📊 Recovery Result:")
            print(f"      Closed: {len(closed_tickets)}/{len(opportunity.execution_order)} positions")
            print(f"      Secured: ${total_secured:.2f}")
            print(f"      Success: {'Yes' if success else 'No'}")
            
            return success
            
        except Exception as e:
            print(f"❌ Execute single recovery error: {e}")
            return False
    
    def _track_recovery_execution(self, opportunity: HedgeOpportunity, success: bool):
        """ติดตามประสิทธิภาพการ Recovery"""
        try:
            stats = self.hedge_execution_stats
            stats["total_attempts"] += 1
            
            if success:
                stats["successful_hedges"] += 1
                stats["total_recovery"] += max(0, opportunity.net_result)
            
            # Update average confidence
            if stats["total_attempts"] > 0:
                stats["avg_confidence"] = (
                    (stats["avg_confidence"] * (stats["total_attempts"] - 1) + opportunity.confidence)
                    / stats["total_attempts"]
                )
            
            # Track by strategy
            stats["strategy_performance"][opportunity.strategy.value] += 1
            
            # Calculate success rate
            success_rate = stats["successful_hedges"] / stats["total_attempts"]
            
            print(f"   📊 Recovery Performance: {success_rate:.1%} ({stats['successful_hedges']}/{stats['total_attempts']})")
            print(f"      Total Recovered: ${stats['total_recovery']:.2f}")
            print(f"      Avg Confidence: {stats['avg_confidence']:.2f}")
            
        except Exception as e:
            print(f"❌ Track recovery execution error: {e}")
    
    # ========================================================================================
    # 📈 PORTFOLIO OPTIMIZATION
    # ========================================================================================
    
    def _check_portfolio_optimization(self):
        """📈 ตรวจสอบและดำเนินการ Portfolio Optimization"""
        try:
            if not self.active_positions:
                return
            
            # คำนวณ portfolio health
            portfolio_health = self._calculate_portfolio_health()
            
            if portfolio_health < self.four_d_config['portfolio_health_threshold']:
                print(f"⚠️ Portfolio health low: {portfolio_health:.2f}")
                self._suggest_portfolio_optimizations(portfolio_health)
            
        except Exception as e:
            print(f"❌ Portfolio optimization check error: {e}")
    
    def _calculate_portfolio_health(self) -> float:
        """คำนวณสุขภาพ Portfolio รวม"""
        try:
            if not self.active_positions:
                return 1.0
            
            health_factors = []
            
            # 1. Overall P&L health (30%)
            total_profit = sum(pos.total_profit for pos in self.active_positions.values())
            profit_health = max(0, min(1, (total_profit + 200) / 400))  # Scale from -$200 to +$200
            health_factors.append(("profit", profit_health, 0.30))
            
            # 2. Balance health (25%)
            buy_count = sum(1 for pos in self.active_positions.values() if pos.type == PositionType.BUY)
            total_count = len(self.active_positions)
            balance_ratio = buy_count / total_count
            balance_health = 1 - abs(balance_ratio - 0.5) * 2  # Best at 50/50
            health_factors.append(("balance", balance_health, 0.25))
            
            # 3. Average 4D score health (20%)
            avg_4d_score = np.mean([pos.four_d_overall_score for pos in self.active_positions.values()])
            health_factors.append(("4d_score", avg_4d_score, 0.20))
            
            # 4. Recovery potential health (15%)
            positions_with_hedge = sum(1 for pos in self.active_positions.values() if pos.hedge_candidates)
            hedge_coverage = positions_with_hedge / total_count if total_count > 0 else 0
            health_factors.append(("recovery", hedge_coverage, 0.15))
            
            # 5. Age distribution health (10%)
            ages = [pos.age_hours for pos in self.active_positions.values()]
            avg_age = np.mean(ages)
            age_health = max(0, 1 - (avg_age / 48))  # Decline after 48 hours
            health_factors.append(("age", age_health, 0.10))
            
            # Calculate weighted health
            weighted_sum = sum(score * weight for name, score, weight in health_factors)
            total_weight = sum(weight for name, score, weight in health_factors)
            
            portfolio_health = weighted_sum / total_weight if total_weight > 0 else 0.5
            return max(0, min(1, portfolio_health))
            
        except Exception as e:
            print(f"❌ Portfolio health calculation error: {e}")
            return 0.5
    
    def _suggest_portfolio_optimizations(self, current_health: float):
        """แนะนำการปรับปรุง Portfolio"""
        try:
            suggestions = []
            
            # Analyze specific issues
            buy_count = sum(1 for pos in self.active_positions.values() if pos.type == PositionType.BUY)
            sell_count = len(self.active_positions) - buy_count
            total_profit = sum(pos.total_profit for pos in self.active_positions.values())
            
            # Balance suggestions
            if buy_count > sell_count * 1.5:
                suggestions.append("Portfolio BUY-heavy: Consider more SELL positions")
            elif sell_count > buy_count * 1.5:
                suggestions.append("Portfolio SELL-heavy: Consider more BUY positions")
            
            # Profit suggestions
            losing_positions = [pos for pos in self.active_positions.values() if pos.total_profit < -20]
            if len(losing_positions) > len(self.active_positions) * 0.4:
                suggestions.append(f"High loss ratio: {len(losing_positions)} positions need recovery")
            
            # Age suggestions
            old_positions = [pos for pos in self.active_positions.values() if pos.age_hours > 24]
            if len(old_positions) > len(self.active_positions) * 0.3:
                suggestions.append(f"Aging positions: {len(old_positions)} positions > 24 hours old")
            
            # 4D score suggestions
            low_4d_positions = [pos for pos in self.active_positions.values() if pos.four_d_overall_score < 0.3]
            if len(low_4d_positions) > 0:
                suggestions.append(f"Low 4D scores: {len(low_4d_positions)} positions need attention")
            
            if suggestions:
                print(f"💡 Portfolio Optimization Suggestions (Health: {current_health:.2f}):")
                for suggestion in suggestions:
                    print(f"   • {suggestion}")
            
        except Exception as e:
            print(f"❌ Portfolio optimization suggestions error: {e}")
    
    def _update_analysis_history(self):
        """อัปเดตประวัติการวิเคราะห์"""
        try:
            analysis_snapshot = {
                'timestamp': datetime.now(),
                'total_positions': len(self.active_positions),
                'portfolio_health': self._calculate_portfolio_health(),
                'avg_4d_score': np.mean([pos.four_d_overall_score for pos in self.active_positions.values()]) if self.active_positions else 0,
                'recovery_opportunities': len([pos for pos in self.active_positions.values() if pos.recovery_priority > 0.7]),
                'net_profit': sum(pos.total_profit for pos in self.active_positions.values())
            }
            
            self.analysis_history.append(analysis_snapshot)
            
        except Exception as e:
            print(f"❌ Update analysis history error: {e}")
    
    # ========================================================================================
    # 🔧 UTILITY & COMPATIBILITY METHODS
    # ========================================================================================
    
    def update_positions(self):
        """อัปเดตข้อมูล positions จาก MT5 - FIXED: Handle missing commission attribute"""
        try:
            if not self.mt5_connector.is_connected:
                return
            
            # ดึงข้อมูลจาก MT5
            mt5_positions = mt5.positions_get(symbol=self.symbol)
            
            if mt5_positions is None:
                mt5_positions = []
            
            # แปลงเป็น Position objects
            updated_positions = {}
            
            for mt5_pos in mt5_positions:
                # แปลง position type
                pos_type = PositionType.BUY if mt5_pos.type == mt5.POSITION_TYPE_BUY else PositionType.SELL
                
                # คำนวณ age
                open_time = datetime.fromtimestamp(mt5_pos.time)
                age_hours = (datetime.now() - open_time).total_seconds() / 3600
                
                # FIXED: Safe attribute access with defaults
                commission = getattr(mt5_pos, 'commission', 0.0)
                swap = getattr(mt5_pos, 'swap', 0.0)
                profit = getattr(mt5_pos, 'profit', 0.0)
                comment = getattr(mt5_pos, 'comment', '')
                magic = getattr(mt5_pos, 'magic', 0)
                
                # สร้าง Position object
                position = Position(
                    ticket=mt5_pos.ticket,
                    symbol=mt5_pos.symbol,
                    type=pos_type,
                    volume=mt5_pos.volume,
                    open_price=mt5_pos.price_open,
                    current_price=mt5_pos.price_current,
                    profit=profit,
                    swap=swap,
                    commission=commission,  # ← Use safe value
                    open_time=open_time,
                    age_hours=age_hours,
                    comment=comment,
                    magic=magic
                )
                
                # รักษา 4D analysis scores ถ้ามีอยู่แล้ว
                if mt5_pos.ticket in self.active_positions:
                    old_pos = self.active_positions[mt5_pos.ticket]
                    position.four_d_value_score = old_pos.four_d_value_score
                    position.four_d_safety_impact = old_pos.four_d_safety_impact
                    position.four_d_hedge_potential = old_pos.four_d_hedge_potential
                    position.four_d_market_alignment = old_pos.four_d_market_alignment
                    position.recovery_priority = old_pos.recovery_priority
                    position.hedge_candidates = old_pos.hedge_candidates
                
                updated_positions[mt5_pos.ticket] = position
            
            self.active_positions = updated_positions
            
        except Exception as e:
            self.log(f"❌ Update positions error: {e}")

    def get_active_positions(self) -> List[Dict]:
        """ดึงข้อมูล active positions - FIXED: Handle missing commission safely"""
        try:
            self.update_positions()
            
            positions = []
            for pos in self.active_positions.values():
                # Safe commission access
                commission = getattr(pos, 'commission', 0.0) if hasattr(pos, 'commission') else 0.0
                
                positions.append({
                    'ticket': pos.ticket,
                    'symbol': pos.symbol,
                    'type': 0 if pos.type == PositionType.BUY else 1,  # MT5 compatible
                    'volume': pos.volume,
                    'price_open': pos.open_price,
                    'price': pos.current_price,
                    'profit': pos.total_profit,
                    'swap': getattr(pos, 'swap', 0.0),
                    'commission': commission,  # ← Use safe value
                    'time': pos.open_time,
                    'comment': getattr(pos, 'comment', ''),
                    'magic': getattr(pos, 'magic', 0),
                    # 4D Analysis data
                    'four_d_score': pos.four_d_overall_score,
                    'recovery_priority': getattr(pos, 'recovery_priority', 0.0),
                    'hedge_candidates': len(getattr(pos, 'hedge_candidates', []))
                })
            
            return positions
            
        except Exception as e:
            self.log(f"❌ Get active positions error: {e}")
            return []

    @property
    def total_profit(self) -> float:
        """กำไร/ขาดทุนรวม - FIXED: Handle missing commission safely"""
        try:
            commission = getattr(self, 'commission', 0.0) if hasattr(self, 'commission') else 0.0
            swap = getattr(self, 'swap', 0.0) if hasattr(self, 'swap') else 0.0
            profit = getattr(self, 'profit', 0.0) if hasattr(self, 'profit') else 0.0
            
            return profit + swap + commission
        except:
            return getattr(self, 'profit', 0.0)
            
    def get_pending_orders(self) -> List[Dict]:
        """ดึงข้อมูล pending orders - Compatibility method"""
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
    
    def get_account_info(self) -> Dict:
        """ดึงข้อมูล account - Compatibility method"""
        try:
            if not self.mt5_connector.is_connected:
                return {}
            
            account_info = mt5.account_info()
            if not account_info:
                return {}
            
            return {
                'balance': account_info.balance,
                'equity': account_info.equity,
                'margin': account_info.margin,
                'margin_used': account_info.margin_used if hasattr(account_info, 'margin_used') else 0,
                'margin_free': account_info.margin_free,
                'profit': account_info.profit
            }
            
        except Exception as e:
            self.log(f"❌ Get account info error: {e}")
            return {}
    
    def _close_single_position(self, position: Position, reason: CloseReason) -> bool:
        """ปิด position เดียว"""
        try:
            if not self.mt5_connector.is_connected:
                return False
            
            # สร้าง close request
            if position.type == PositionType.BUY:
                close_type = mt5.ORDER_TYPE_SELL
            else:
                close_type = mt5.ORDER_TYPE_BUY
            
            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": close_type,
                "position": position.ticket,
                "deviation": 20,
                "magic": position.magic,
                "comment": f"Close|{reason.value}|4D:{position.four_d_overall_score:.2f}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC
            }
            
            # Execute close
            result = mt5.order_send(close_request)
            
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                self.log(f"✅ Position #{position.ticket} closed: ${position.total_profit:.2f}")
                
                # Track in history
                self.position_history.append({
                    'ticket': position.ticket,
                    'close_time': datetime.now(),
                    'close_reason': reason.value,
                    'final_profit': position.total_profit,
                    'age_hours': position.age_hours,
                    'four_d_score': position.four_d_overall_score
                })
                
                return True
            else:
                error_msg = f"Failed to close #{position.ticket}"
                if result:
                    error_msg += f": {result.comment}"
                self.log(f"❌ {error_msg}")
                return False
                
        except Exception as e:
            self.log(f"❌ Close single position error: {e}")
            return False
    
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
    # 🎯 LEGACY COMPATIBILITY METHODS - UPDATED FOR 4D
    # ========================================================================================
    
    def close_profitable_positions(self, confidence: float = 0.6, reasoning: str = "") -> bool:
        """ปิด positions ที่มีกำไร - Enhanced with 4D"""
        try:
            print(f"💰 === CLOSE PROFITABLE POSITIONS (4D Enhanced) ===")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Reasoning: {reasoning}")
            
            # อัปเดต positions ก่อน
            self.update_positions()
            
            if not self.active_positions:
                print("ℹ️ No positions to close")
                return False
            
            # หา profitable positions with 4D analysis
            profitable_positions = []
            for pos in self.active_positions.values():
                if pos.total_profit > 0:
                    # เพิ่มเงื่อนไข 4D: ต้องมี 4D score ดีด้วย
                    if pos.four_d_overall_score > 0.4:  # 4D threshold
                        profitable_positions.append(pos)
                    else:
                        print(f"   ⚠️ Position #{pos.ticket} profitable but low 4D score: {pos.four_d_overall_score:.2f}")
            
            if not profitable_positions:
                print("ℹ️ No suitable profitable positions found")
                return False
            
            total_profit = sum(pos.total_profit for pos in profitable_positions)
            print(f"💰 Found {len(profitable_positions)} profitable positions")
            print(f"   Total Profit: ${total_profit:.2f}")
            
            # ตัดสินใจ strategy ด้วย 4D analysis
            close_strategy = self._determine_4d_close_strategy(profitable_positions, confidence, reasoning)
            
            # Execute strategy
            if close_strategy == "SMART_HEDGE_RECOVERY":
                success = self._execute_smart_hedge_recovery(profitable_positions)
            elif close_strategy == "SELECTIVE_4D_CLOSE":
                success = self._execute_selective_4d_close(profitable_positions, confidence)
            elif close_strategy == "PORTFOLIO_REBALANCE":
                success = self._execute_portfolio_rebalance(profitable_positions)
            else:  # ALL_PROFITABLE
                success = self._execute_all_profitable_close(profitable_positions)
            
            # Track performance
            self._track_close_performance(CloseReason.FOUR_D_AI_RECOVERY, success)
            
            return success
            
        except Exception as e:
            self.log(f"❌ Close profitable positions error: {e}")
            return False
    
    def _determine_4d_close_strategy(self, profitable_positions: List[Position], 
                                   confidence: float, reasoning: str) -> str:
        """ตัดสินใจ strategy การปิดด้วย 4D Analysis"""
        try:
            # Analyze losing positions
            losing_positions = [pos for pos in self.active_positions.values() if pos.total_profit < 0]
            
            total_profit = sum(pos.total_profit for pos in profitable_positions)
            total_loss = sum(pos.total_profit for pos in losing_positions) if losing_positions else 0
            
            # Strategy decision based on 4D insights
            if losing_positions and total_profit + total_loss > 5:
                # มีโอกาส hedge recovery ดี
                return "SMART_HEDGE_RECOVERY"
            
            elif confidence < 0.5 or "selective" in reasoning.lower():
                # ปิดแบบเลือกสรร
                return "SELECTIVE_4D_CLOSE"
            
            elif "balance" in reasoning.lower():
                # ปิดเพื่อ rebalance portfolio
                return "PORTFOLIO_REBALANCE"
            
            else:
                # ปิดทั้งหมด
                return "ALL_PROFITABLE"
                
        except Exception as e:
            print(f"❌ 4D close strategy determination error: {e}")
            return "ALL_PROFITABLE"
    
    def _execute_smart_hedge_recovery(self, profitable_positions: List[Position]) -> bool:
        """Execute Smart Hedge Recovery - 4D Enhanced"""
        try:
            print("🧠 === SMART HEDGE RECOVERY (4D) ===")
            
            # หา losing positions
            losing_positions = [pos for pos in self.active_positions.values() if pos.total_profit < 0]
            
            if not losing_positions:
                print("ℹ️ No losing positions for hedge recovery")
                return self._execute_all_profitable_close(profitable_positions)
            
            # เรียงตาม recovery priority
            losing_positions.sort(key=lambda p: p.recovery_priority, reverse=True)
            profitable_positions.sort(key=lambda p: p.total_profit, reverse=True)
            
            print(f"   🎯 Analyzing {len(losing_positions)} loss positions")
            print(f"   💰 Available {len(profitable_positions)} profit positions")
            
            closed_pairs = 0
            total_recovered = 0.0
            
            # ทำ hedge pairing แบบ intelligent
            for loss_pos in losing_positions:
                best_hedge_combination = self._find_best_hedge_combination(loss_pos, profitable_positions)
                
                if best_hedge_combination and best_hedge_combination['net_result'] > 0:
                    # Execute hedge combination
                    success = self._execute_hedge_combination(loss_pos, best_hedge_combination)
                    
                    if success:
                        closed_pairs += 1
                        total_recovered += best_hedge_combination['net_result']
                        
                        # Remove used profitable positions from available list
                        for hedge_pos in best_hedge_combination['hedge_positions']:
                            if hedge_pos in profitable_positions:
                                profitable_positions.remove(hedge_pos)
                    
                    if not profitable_positions:  # หมดกำไรแล้ว
                        break
            
            print(f"   📊 Hedge Recovery Results:")
            print(f"      Hedge Pairs Closed: {closed_pairs}")
            print(f"      Total Recovered: ${total_recovered:.2f}")
            
            return closed_pairs > 0
            
        except Exception as e:
            print(f"❌ Smart hedge recovery error: {e}")
            return False
    
    def _find_best_hedge_combination(self, loss_position: Position, 
                                   available_profits: List[Position]) -> Optional[Dict]:
        """หา combination ที่ดีที่สุดสำหรับ hedge"""
        try:
            if not available_profits:
                return None
            
            loss_amount = abs(loss_position.total_profit)
            best_combination = None
            best_score = 0
            
            # Test single hedge
            for profit_pos in available_profits:
                net_result = loss_position.total_profit + profit_pos.total_profit
                if net_result > 0:
                    # Calculate combination score
                    score = self._calculate_hedge_combination_score(
                        loss_position, [profit_pos], net_result
                    )
                    
                    if score > best_score:
                        best_score = score
                        best_combination = {
                            'hedge_positions': [profit_pos],
                            'net_result': net_result,
                            'score': score,
                            'strategy': 'single_hedge'
                        }
            
            # Test multiple hedge (if available)
            if len(available_profits) > 1:
                # Try combinations of 2-3 positions
                for i in range(min(3, len(available_profits))):
                    for j in range(i+1, min(i+3, len(available_profits))):
                        combination = available_profits[i:j+1]
                        combo_profit = sum(pos.total_profit for pos in combination)
                        net_result = loss_position.total_profit + combo_profit
                        
                        if net_result > 0:
                            score = self._calculate_hedge_combination_score(
                                loss_position, combination, net_result
                            )
                            
                            if score > best_score:
                                best_score = score
                                best_combination = {
                                    'hedge_positions': combination,
                                    'net_result': net_result,
                                    'score': score,
                                    'strategy': 'multi_hedge'
                                }
            
            return best_combination
            
        except Exception as e:
            print(f"❌ Find best hedge combination error: {e}")
            return None
    
    def _calculate_hedge_combination_score(self, loss_pos: Position, 
                                         hedge_positions: List[Position], net_result: float) -> float:
        """คำนวณคะแนนของ hedge combination"""
        try:
            score_factors = []
            
            # 1. Net result quality (40%)
            net_score = min(net_result / 50, 1.0) if net_result > 0 else 0
            score_factors.append(net_score * 0.40)
            
            # 2. 4D alignment (30%)
            all_positions = [loss_pos] + hedge_positions
            avg_4d_score = np.mean([pos.four_d_overall_score for pos in all_positions])
            score_factors.append(avg_4d_score * 0.30)
            
            # 3. Volume efficiency (20%)
            total_volume = sum(pos.volume for pos in hedge_positions)
            volume_ratio = min(loss_pos.volume, total_volume) / max(loss_pos.volume, total_volume)
            score_factors.append(volume_ratio * 0.20)
            
            # 4. Simplicity bonus (10%)
            simplicity_score = 1.0 / len(hedge_positions)  # Prefer simpler solutions
            score_factors.append(simplicity_score * 0.10)
            
            return sum(score_factors)
            
        except Exception as e:
            print(f"❌ Hedge combination score error: {e}")
            return 0.0
    
    def _execute_hedge_combination(self, loss_position: Position, combination: Dict) -> bool:
        """Execute hedge combination"""
        try:
            print(f"      🎯 Executing {combination['strategy']} hedge")
            print(f"         Loss Position: #{loss_position.ticket} (${loss_position.total_profit:.2f})")
            print(f"         Hedge Positions: {len(combination['hedge_positions'])}")
            print(f"         Expected Net: ${combination['net_result']:.2f}")
            
            closed_positions = []
            
            # ปิด hedge positions ก่อน (กำไร)
            for hedge_pos in combination['hedge_positions']:
                if self._close_single_position(hedge_pos, CloseReason.HEDGE_OPTIMIZATION):
                    closed_positions.append(hedge_pos.ticket)
                    time.sleep(0.3)  # Brief delay
                else:
                    print(f"         ❌ Failed to close hedge #{hedge_pos.ticket}")
            
            # ปิด loss position ท้ายสุด
            if self._close_single_position(loss_position, CloseReason.SMART_RECOVERY):
                closed_positions.append(loss_position.ticket)
            else:
                print(f"         ❌ Failed to close loss position #{loss_position.ticket}")
            
            success = len(closed_positions) == len(combination['hedge_positions']) + 1
            
            print(f"         📊 Hedge Result: {len(closed_positions)} positions closed")
            return success
            
        except Exception as e:
            print(f"❌ Execute hedge combination error: {e}")
            return False
    
    def _execute_selective_4d_close(self, profitable_positions: List[Position], confidence: float) -> bool:
        """Execute Selective Close ด้วย 4D criteria"""
        try:
            print("🧠 === SELECTIVE 4D CLOSE ===")
            
            # เรียงตาม 4D overall score + profit
            profitable_positions.sort(key=lambda p: (p.four_d_overall_score + p.total_profit/100), reverse=True)
            
            # เลือกปิดตาม confidence และ 4D score
            positions_to_close = []
            for pos in profitable_positions:
                if (pos.four_d_overall_score > 0.5 and 
                    pos.total_profit > 10 and
                    len(positions_to_close) < len(profitable_positions) * confidence):
                    positions_to_close.append(pos)
            
            if not positions_to_close:
                print("   ℹ️ No positions meet 4D criteria for closing")
                return False
            
            print(f"   🎯 Closing {len(positions_to_close)} positions (4D selected)")
            
            closed_count = 0
            total_secured = 0.0
            
            for pos in positions_to_close:
                if self._close_single_position(pos, CloseReason.FOUR_D_AI_RECOVERY):
                    closed_count += 1
                    total_secured += pos.total_profit
                    print(f"      ✅ Closed #{pos.ticket}: ${pos.total_profit:.2f} (4D: {pos.four_d_overall_score:.2f})")
                    time.sleep(0.5)
            
            success = closed_count > 0
            print(f"   📊 4D Selective Close: {closed_count}/{len(positions_to_close)} closed, ${total_secured:.2f} secured")
            
            return success
            
        except Exception as e:
            print(f"❌ Selective 4D close error: {e}")
            return False
    
    def _execute_portfolio_rebalance(self, profitable_positions: List[Position]) -> bool:
        """Execute Portfolio Rebalancing"""
        try:
            print("⚖️ === PORTFOLIO REBALANCE ===")
            
            # วิเคราะห์ balance ปัจจุบัน
            buy_count = sum(1 for pos in self.active_positions.values() if pos.type == PositionType.BUY)
            sell_count = len(self.active_positions) - buy_count
            total_count = len(self.active_positions)
            
            buy_ratio = buy_count / total_count if total_count > 0 else 0.5
            
            print(f"   📊 Current Balance: {buy_count} BUY | {sell_count} SELL (ratio: {buy_ratio:.2f})")
            
            # ตัดสินใจว่าจะปิดอะไร
            positions_to_close = []
            
            if buy_ratio > 0.65:  # BUY มากเกินไป
                print("   ⚖️ BUY-heavy portfolio - closing BUY positions")
                buy_profitable = [pos for pos in profitable_positions if pos.type == PositionType.BUY]
                buy_profitable.sort(key=lambda p: p.four_d_overall_score, reverse=True)
                positions_to_close = buy_profitable[:max(1, len(buy_profitable)//2)]
                
            elif buy_ratio < 0.35:  # SELL มากเกินไป
                print("   ⚖️ SELL-heavy portfolio - closing SELL positions")
                sell_profitable = [pos for pos in profitable_positions if pos.type == PositionType.SELL]
                sell_profitable.sort(key=lambda p: p.four_d_overall_score, reverse=True)
                positions_to_close = sell_profitable[:max(1, len(sell_profitable)//2)]
                
            else:
                print("   ✅ Portfolio already balanced")
                return True
            
            if not positions_to_close:
                print("   ℹ️ No suitable positions for rebalancing")
                return False
            
            # Execute rebalancing
            closed_count = 0
            for pos in positions_to_close:
                if self._close_single_position(pos, CloseReason.PORTFOLIO_REBALANCE):
                    closed_count += 1
                    print(f"      ⚖️ Rebalanced #{pos.ticket}: ${pos.total_profit:.2f}")
                    time.sleep(0.5)
            
            success = closed_count > 0
            print(f"   📊 Rebalance Result: {closed_count}/{len(positions_to_close)} positions closed")
            
            return success
            
        except Exception as e:
            print(f"❌ Portfolio rebalance error: {e}")
            return False
    
    def _execute_all_profitable_close(self, profitable_positions: List[Position]) -> bool:
        """Execute ปิดกำไรทั้งหมด"""
        try:
            print("💰 === CLOSE ALL PROFITABLE ===")
            
            closed_count = 0
            total_secured = 0.0
            
            for pos in profitable_positions:
                if self._close_single_position(pos, CloseReason.PROFIT_TARGET):
                    closed_count += 1
                    total_secured += pos.total_profit
                    print(f"      💰 Closed #{pos.ticket}: ${pos.total_profit:.2f}")
                    time.sleep(0.5)
            
            success = closed_count > 0
            print(f"   📊 All Profitable Close: {closed_count}/{len(profitable_positions)} closed, ${total_secured:.2f} secured")
            
            return success
            
        except Exception as e:
            print(f"❌ All profitable close error: {e}")
            return False
    
    def emergency_close_all(self) -> bool:
        """🚨 ปิดทุก positions ในสถานการณ์ฉุกเฉิน"""
        try:
            print("🚨 === EMERGENCY CLOSE ALL ===")
            
            self.update_positions()
            
            if not self.active_positions:
                print("ℹ️ No positions to close")
                return True
            
            total_positions = len(self.active_positions)
            total_profit = sum(pos.total_profit for pos in self.active_positions.values())
            
            print(f"🚨 Emergency closing {total_positions} positions")
            print(f"   Net P&L: ${total_profit:.2f}")
            
            closed_count = 0
            for pos in list(self.active_positions.values()):
                if self._close_single_position(pos, CloseReason.EMERGENCY):
                    closed_count += 1
                    time.sleep(0.2)  # Quick succession
            
            success = closed_count == total_positions
            
            if success:
                print(f"✅ Emergency close successful: {closed_count}/{total_positions}")
            else:
                print(f"⚠️ Partial emergency close: {closed_count}/{total_positions}")
            
            self._track_close_performance(CloseReason.EMERGENCY, success)
            return success
            
        except Exception as e:
            self.log(f"❌ Emergency close error: {e}")
            return False
    
    # ========================================================================================
    # 📊 ENHANCED STATUS & REPORTING METHODS
    # ========================================================================================
    
    def get_4d_portfolio_status(self) -> Dict:
        """ดึงสถานะ Portfolio พร้อม 4D Analysis"""
        try:
            self.update_positions()
            
            if not self.active_positions:
                return {
                    'total_positions': 0,
                    'portfolio_health': 1.0,
                    'recovery_opportunities': 0,
                    'message': 'No active positions'
                }
            
            # Basic statistics
            buy_positions = [pos for pos in self.active_positions.values() if pos.type == PositionType.BUY]
            sell_positions = [pos for pos in self.active_positions.values() if pos.type == PositionType.SELL]
            
            total_profit = sum(pos.total_profit for pos in self.active_positions.values())
            profitable_count = sum(1 for pos in self.active_positions.values() if pos.total_profit > 0)
            losing_count = len(self.active_positions) - profitable_count
            
            # 4D Analysis aggregates
            avg_4d_score = np.mean([pos.four_d_overall_score for pos in self.active_positions.values()])
            avg_recovery_priority = np.mean([pos.recovery_priority for pos in self.active_positions.values()])
            
            # Recovery opportunities
            high_priority_recovery = sum(1 for pos in self.active_positions.values() if pos.recovery_priority > 0.7)
            total_hedge_candidates = sum(len(pos.hedge_candidates) for pos in self.active_positions.values())
            
            # Portfolio health
            portfolio_health = self._calculate_portfolio_health()
            
            # Balance analysis
            balance_ratio = len(buy_positions) / len(self.active_positions)
            balance_status = "BALANCED"
            if balance_ratio > 0.65:
                balance_status = "BUY_HEAVY"
            elif balance_ratio < 0.35:
                balance_status = "SELL_HEAVY"
            
            return {
                'total_positions': len(self.active_positions),
                'buy_positions': len(buy_positions),
                'sell_positions': len(sell_positions),
                'balance_ratio': balance_ratio,
                'balance_status': balance_status,
                'total_profit': total_profit,
                'profitable_positions': profitable_count,
                'losing_positions': losing_count,
                'portfolio_health': portfolio_health,
                'avg_4d_score': avg_4d_score,
                'avg_recovery_priority': avg_recovery_priority,
                'high_priority_recovery': high_priority_recovery,
                'total_hedge_candidates': total_hedge_candidates,
                'recovery_scanner_active': self.recovery_scanner_running,
                'last_recovery_scan': self.last_recovery_scan.strftime('%H:%M:%S') if self.last_recovery_scan else 'Never',
                'hedge_execution_stats': self.hedge_execution_stats
            }
            
        except Exception as e:
            print(f"❌ 4D portfolio status error: {e}")
            return {'error': str(e)}
    
    def get_recovery_opportunities_report(self) -> str:
        """📊 รายงานโอกาส Recovery แบบละเอียด"""
        try:
            opportunities = self._scan_recovery_opportunities()
            
            if not opportunities:
                return "ℹ️ No recovery opportunities found"
            
            report_lines = []
            report_lines.append("🔍 RECOVERY OPPORTUNITIES REPORT")
            report_lines.append("=" * 50)
            
            for i, opp in enumerate(opportunities, 1):
                report_lines.append(f"{i}. Position #{opp.primary_position.ticket}")
                report_lines.append(f"   Current Loss: ${opp.primary_position.total_profit:.2f}")
                report_lines.append(f"   Strategy: {opp.strategy.value}")
                report_lines.append(f"   Hedge Positions: {len(opp.hedge_positions)}")
                report_lines.append(f"   Net Result: ${opp.net_result:.2f}")
                report_lines.append(f"   Confidence: {opp.confidence:.1%}")
                report_lines.append(f"   4D Alignment: {opp.four_d_alignment:.1%}")
                report_lines.append(f"   Urgency: {opp.urgency_level:.1%}")
                report_lines.append(f"   Expected Recovery: ${opp.expected_recovery:.2f}")
                
                if opp.is_highly_recommended:
                    report_lines.append("   🌟 HIGHLY RECOMMENDED")
                
                report_lines.append("")
            
            # Summary
            total_expected_recovery = sum(opp.expected_recovery for opp in opportunities)
            avg_confidence = np.mean([opp.confidence for opp in opportunities])
            
            report_lines.append("📊 SUMMARY:")
            report_lines.append(f"   Total Opportunities: {len(opportunities)}")
            report_lines.append(f"   Total Expected Recovery: ${total_expected_recovery:.2f}")
            report_lines.append(f"   Average Confidence: {avg_confidence:.1%}")
            report_lines.append(f"   Highly Recommended: {sum(1 for opp in opportunities if opp.is_highly_recommended)}")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            print(f"❌ Recovery opportunities report error: {e}")
            return f"Report generation error: {e}"
    
    def get_4d_analysis_summary(self) -> str:
        """📊 สรุป 4D Analysis สำหรับทุก positions"""
        try:
            if not self.active_positions:
                return "ℹ️ No positions for 4D analysis"
            
            report_lines = []
            report_lines.append("🧠 4D POSITION ANALYSIS SUMMARY")
            report_lines.append("=" * 50)
            
            # Overall statistics
            all_positions = list(self.active_positions.values())
            avg_scores = {
                'value': np.mean([pos.four_d_value_score for pos in all_positions]),
                'safety': np.mean([pos.four_d_safety_impact for pos in all_positions]),
                'hedge': np.mean([pos.four_d_hedge_potential for pos in all_positions]),
                'market': np.mean([pos.four_d_market_alignment for pos in all_positions]),
                'overall': np.mean([pos.four_d_overall_score for pos in all_positions])
            }
            
            report_lines.append("📊 PORTFOLIO 4D AVERAGES:")
            report_lines.append(f"   📈 Position Value: {avg_scores['value']:.2f}")
            report_lines.append(f"   🛡️ Safety Impact: {avg_scores['safety']:.2f}")
            report_lines.append(f"   🎯 Hedge Potential: {avg_scores['hedge']:.2f}")
            report_lines.append(f"   🌍 Market Alignment: {avg_scores['market']:.2f}")
            report_lines.append(f"   🧠 Overall Score: {avg_scores['overall']:.2f}")
            report_lines.append("")
            
            # Top/Bottom performers
            sorted_by_4d = sorted(all_positions, key=lambda p: p.four_d_overall_score, reverse=True)
            
            report_lines.append("🏆 TOP 4D PERFORMERS:")
            for pos in sorted_by_4d[:3]:
                report_lines.append(f"   #{pos.ticket}: 4D:{pos.four_d_overall_score:.2f} | P&L:${pos.total_profit:.2f} | Age:{pos.age_hours:.1f}h")
            
            report_lines.append("")
            report_lines.append("⚠️ NEEDS ATTENTION:")
            for pos in sorted_by_4d[-3:]:
                report_lines.append(f"   #{pos.ticket}: 4D:{pos.four_d_overall_score:.2f} | P&L:${pos.total_profit:.2f} | Age:{pos.age_hours:.1f}h")
            
            # Recovery insights
            high_recovery_priority = [pos for pos in all_positions if pos.recovery_priority > 0.7]
            if high_recovery_priority:
                report_lines.append("")
                report_lines.append("🎯 HIGH RECOVERY PRIORITY:")
                for pos in high_recovery_priority:
                    report_lines.append(f"   #{pos.ticket}: Priority:{pos.recovery_priority:.2f} | Loss:${pos.total_profit:.2f} | Hedges:{len(pos.hedge_candidates)}")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            print(f"❌ 4D analysis summary error: {e}")
            return f"4D analysis summary error: {e}"
    
    # ========================================================================================
    # 🎮 API METHODS FOR EXTERNAL CONTROL
    # ========================================================================================
    
    def force_recovery_scan(self) -> Dict:
        """🎮 บังคับสแกน Recovery ทันที"""
        try:
            print("🔍 Force recovery scan initiated...")
            
            # Update positions first
            self.update_positions()
            
            # Perform 4D analysis
            self._perform_4d_position_analysis()
            
            # Scan for opportunities
            opportunities = self._scan_recovery_opportunities()
            
            # Execute if found
            executed_count = 0
            if opportunities:
                high_confidence_opps = [opp for opp in opportunities if opp.confidence > 0.8]
                
                for opp in high_confidence_opps[:2]:  # Top 2 only
                    if self._execute_single_recovery(opp):
                        executed_count += 1
            
            return {
                'scan_completed': True,
                'opportunities_found': len(opportunities),
                'high_confidence_opportunities': len([o for o in opportunities if o.confidence > 0.8]),
                'recovery_actions_executed': executed_count,
                'scan_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Force recovery scan error: {e}")
            return {'error': str(e)}
    
    def get_hedge_recommendations(self) -> List[Dict]:
        """🎯 ดึงคำแนะนำ Hedge"""
        try:
            opportunities = self._scan_recovery_opportunities()
            
            recommendations = []
            for opp in opportunities:
                if opp.confidence > 0.6:
                    recommendations.append({
                        'primary_ticket': opp.primary_position.ticket,
                        'primary_loss': opp.primary_position.total_profit,
                        'strategy': opp.strategy.value,
                        'hedge_count': len(opp.hedge_positions),
                        'net_result': opp.net_result,
                        'confidence': opp.confidence,
                        'urgency': opp.urgency_level,
                        'recommendation': 'EXECUTE' if opp.is_highly_recommended else 'CONSIDER'
                    })
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Hedge recommendations error: {e}")
            return []
    
    def get_portfolio_optimization_suggestions(self) -> List[str]:
        """💡 ดึงคำแนะนำการปรับปรุง Portfolio"""
        try:
            suggestions = []
            
            if not self.active_positions:
                return ["No positions to optimize"]
            
            # Portfolio health analysis
            portfolio_health = self._calculate_portfolio_health()
            
            if portfolio_health < 0.3:
                suggestions.append("🚨 CRITICAL: Portfolio health very low - immediate action required")
            elif portfolio_health < 0.5:
                suggestions.append("⚠️ Portfolio health below average - consider optimization")
            
            # Balance analysis
            buy_count = sum(1 for pos in self.active_positions.values() if pos.type == PositionType.BUY)
            total_count = len(self.active_positions)
            balance_ratio = buy_count / total_count
            
            if balance_ratio > 0.7:
                suggestions.append("Portfolio heavily BUY-biased - consider SELL entries or BUY closures")
            elif balance_ratio < 0.3:
                suggestions.append("Portfolio heavily SELL-biased - consider BUY entries or SELL closures")
            
            # Recovery analysis
            high_priority_recoveries = sum(1 for pos in self.active_positions.values() if pos.recovery_priority > 0.8)
            if high_priority_recoveries > 0:
                suggestions.append(f"🎯 {high_priority_recoveries} positions need urgent recovery attention")
            
            # 4D score analysis
            low_4d_positions = [pos for pos in self.active_positions.values() if pos.four_d_overall_score < 0.3]
            if len(low_4d_positions) > total_count * 0.3:
                suggestions.append(f"⚠️ {len(low_4d_positions)} positions have low 4D scores - review strategy")
            
            # Age analysis
            old_positions = [pos for pos in self.active_positions.values() if pos.age_hours > 48]
            if len(old_positions) > 0:
                suggestions.append(f"⏰ {len(old_positions)} positions aged >48h - consider recovery or closure")
            
            return suggestions if suggestions else ["✅ Portfolio in good condition"]
            
        except Exception as e:
            print(f"❌ Portfolio optimization suggestions error: {e}")
            return [f"Error generating suggestions: {e}"]
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 💰 PositionManager: {message}")