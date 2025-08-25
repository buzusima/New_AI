"""
📏 Spacing Manager - 4D Enhanced No-Collision Edition
spacing_manager.py

🎯 ระบบควบคุมระยะห่างแบบ 4D สำหรับ AI Gold Grid Trading
- ลบ collision detection (วางได้เสมอ)
- Dynamic spacing ตาม 4D analysis
- No minimum spacing enforcement
- Flexible grid building พร้อม 4D guidance

** COMPATIBLE WITH 4D AI RULE ENGINE - NO COLLISION RESTRICTIONS **
"""

import time
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import deque
import statistics

class SpacingMode(Enum):
    """โหมดการคำนวณระยะห่าง 4D"""
    FIXED_4D = "FIXED_4D"                      # ระยะห่างคงที่แบบ 4D
    VOLATILITY_4D = "VOLATILITY_4D"            # ตาม volatility 4D
    TREND_4D = "TREND_4D"                      # ตาม trend strength 4D
    SESSION_4D = "SESSION_4D"                  # ตาม session activity 4D
    ADAPTIVE_4D = "ADAPTIVE_4D"                # ปรับตัวแบบ 4D AI
    OPPORTUNITY_4D = "OPPORTUNITY_4D"          # ตาม market opportunity 4D

class GridBuildingStrategy(Enum):
    """กลยุทธ์การสร้างกริด 4D"""
    UNLIMITED_PLACEMENT = "UNLIMITED_PLACEMENT"  # วางได้ไม่จำกัด
    DYNAMIC_EXPANSION = "DYNAMIC_EXPANSION"      # ขยายตาม 4D score
    OPPORTUNITY_DRIVEN = "OPPORTUNITY_DRIVEN"    # ขับเคลื่อนด้วย opportunity
    BALANCE_FOCUSED = "BALANCE_FOCUSED"          # เน้นการสร้างความสมดุล

@dataclass
class SpacingParameters4D:
    """พารามิเตอร์ 4D สำหรับคำนวณระยะห่าง"""
    # Base parameters (ไม่มี minimum enforcement)
    base_spacing: int = 80              # ระยะห่างพื้นฐาน (points)
    preferred_spacing: int = 120        # ระยะห่างที่นิยม (points)
    max_spacing: int = 600              # ระยะห่างสูงสุด (points)
    no_minimum_spacing: bool = True     # ไม่จำกัดระยะห่างขั้นต่ำ
    
    # 4D AI factors
    volatility_multiplier: float = 2.0   # ตัวคูณ volatility แบบ 4D
    trend_multiplier: float = 1.8        # ตัวคูณ trend แบบ 4D  
    session_multiplier: float = 1.5      # ตัวคูณ session แบบ 4D
    opportunity_multiplier: float = 2.5  # ตัวคูณ opportunity แบบ 4D
    
    # No-collision settings
    collision_detection: bool = False    # ปิดการตรวจสอบการชน
    unlimited_placement: bool = True     # วางได้ไม่จำกัด
    flexible_grid: bool = True           # กริดยืดหยุ่น

@dataclass 
class Spacing4DResult:
    """ผลลัพธ์การคำนวณระยะห่าง 4D"""
    spacing: int
    reasoning: str
    four_d_score: float
    volatility_factor: float
    trend_factor: float
    session_factor: float
    opportunity_factor: float
    final_multiplier: float
    mode_used: SpacingMode
    placement_allowed: bool = True      # วางได้เสมอ
    collision_detected: bool = False    # ไม่เช็คการชน

@dataclass
class GridPlacement4D:
    """ข้อมูลการวางกริด 4D"""
    price_level: float
    order_type: str  # BUY/SELL
    spacing_used: int
    four_d_confidence: float
    opportunity_score: float
    placement_timestamp: datetime
    reasoning: str

class SpacingManager:
    """
    📏 Spacing Manager - 4D Enhanced No-Collision Edition
    
    ความสามารถใหม่:
    - ✅ No collision detection - วางได้เสมอ
    - ✅ 4D guided spacing (Trend, Volume, Session, Volatility)
    - ✅ Dynamic spacing ตาม market opportunity
    - ✅ Unlimited placement flexibility
    - ✅ Flexible grid building strategy
    - ✅ 4D AI integration สำหรับ optimal spacing
    - ✅ Real-time spacing adjustment
    """
    
    def __init__(self, config: Dict):
        """Initialize 4D Spacing Manager"""
        self.config = config
        trading_config = config.get("trading", {})
        
        # 4D Spacing parameters
        self.params_4d = SpacingParameters4D(
            base_spacing=trading_config.get("base_spacing_points", 80),
            preferred_spacing=trading_config.get("preferred_spacing_points", 120),
            max_spacing=trading_config.get("max_spacing_points", 600),
            no_minimum_spacing=True,  # 4D AI: ไม่จำกัดระยะห่างขั้นต่ำ
            collision_detection=False,  # 4D AI: ปิดการตรวจสอบการชน
            unlimited_placement=True    # 4D AI: วางได้ไม่จำกัด
        )
        
        # 4D AI configuration
        self.four_d_config = {
            "enable_4d_spacing": True,
            "spacing_4d_weight": 0.30,
            "opportunity_4d_weight": 0.35,
            "safety_4d_weight": 0.20,
            "market_4d_weight": 0.15,
            "min_4d_score_for_expansion": 0.20,
            "dynamic_adjustment": True,
            "unlimited_placement": True,
            "no_collision_mode": True
        }
        
        # Grid building strategy
        self.grid_strategy = GridBuildingStrategy.UNLIMITED_PLACEMENT
        self.current_mode = SpacingMode.ADAPTIVE_4D
        
        # State tracking
        self.current_spacing_4d = self.params_4d.base_spacing
        self.spacing_history_4d = deque(maxlen=200)  # เก็บประวัติ 4D
        self.placement_history_4d = deque(maxlen=500)  # เก็บประวัติการวาง
        
        # Performance metrics
        self.performance_4d = {
            "total_placements": 0,
            "successful_placements": 0,
            "average_4d_score": 0.0,
            "spacing_efficiency": 0.0,
            "opportunity_capture_rate": 0.0,
            "grid_coverage": 0.0
        }
        
        # Market state cache
        self.market_state_4d = {
            "last_4d_analysis": None,
            "last_update": datetime.now(),
            "cache_duration": 15  # วินาที
        }
        
        self.log("4D Spacing Manager initialized - No Collision Mode Active")
    
    # ========================================================================================
    # 🆕 MAIN 4D SPACING METHODS
    # ========================================================================================
    
    def calculate_4d_spacing(self, current_price: float, market_analysis: Dict,
                           order_type: str = "BUY") -> Spacing4DResult:
        """
        🆕 คำนวณระยะห่างแบบ 4D AI - ไม่เช็ค collision
        
        Args:
            current_price: ราคาปัจจุบัน
            market_analysis: ผลการวิเคราะห์ 4D จาก market_analyzer
            order_type: ประเภทออเดอร์ (BUY/SELL)
            
        Returns:
            Spacing4DResult: ผลลัพธ์การคำนวณระยะห่าง 4D
        """
        try:
            self.log(f"Calculating 4D spacing for {order_type} at {current_price}")
            
            # ดึงข้อมูล 4D analysis
            four_d_score = market_analysis.get("market_score_4d", 0.5)
            four_d_confidence = market_analysis.get("four_d_confidence", 0.5)
            
            # === DIMENSION-BASED FACTORS ===
            
            # Dimension 1: Trend Factor
            trend_factor = self._calculate_4d_trend_factor(market_analysis)
            
            # Dimension 2: Volume Factor  
            volume_factor = self._calculate_4d_volume_factor(market_analysis)
            
            # Dimension 3: Session Factor
            session_factor = self._calculate_4d_session_factor(market_analysis)
            
            # Dimension 4: Volatility Factor
            volatility_factor = self._calculate_4d_volatility_factor(market_analysis)
            
            # === 4D OPPORTUNITY FACTOR ===
            opportunity_factor = self._calculate_4d_opportunity_factor(
                four_d_score, four_d_confidence, market_analysis
            )
            
            # === COMBINED 4D MULTIPLIER ===
            four_d_multiplier = self._combine_4d_factors(
                trend_factor, volume_factor, session_factor, 
                volatility_factor, opportunity_factor
            )
            
            # === CALCULATE 4D SPACING ===
            base_spacing = self.params_4d.base_spacing
            spacing_4d = int(base_spacing * four_d_multiplier)
            
            # Apply 4D constraints (ไม่มี minimum, มีแค่ maximum)
            final_spacing = min(spacing_4d, self.params_4d.max_spacing)
            
            # Create reasoning
            reasoning = self._create_4d_reasoning(
                four_d_score, trend_factor, volume_factor,
                session_factor, volatility_factor, opportunity_factor,
                four_d_multiplier, final_spacing
            )
            
            # Update 4D state
            self.current_spacing_4d = final_spacing
            self._update_4d_history(final_spacing, four_d_score, reasoning)
            
            # Return 4D result (วางได้เสมอ - ไม่เช็ค collision)
            result = Spacing4DResult(
                spacing=final_spacing,
                reasoning=reasoning,
                four_d_score=four_d_score,
                volatility_factor=volatility_factor,
                trend_factor=trend_factor,
                session_factor=session_factor,
                opportunity_factor=opportunity_factor,
                final_multiplier=four_d_multiplier,
                mode_used=self.current_mode,
                placement_allowed=True,      # 4D AI: วางได้เสมอ
                collision_detected=False     # 4D AI: ไม่เช็คการชน
            )
            
            self.log(f"4D Spacing calculated: {final_spacing} points (Score: {four_d_score:.3f})")
            
            return result
            
        except Exception as e:
            self.log(f"❌ 4D Spacing calculation error: {e}")
            return self._get_default_4d_spacing()
    
    def get_flexible_spacing(self, target_price: float, current_price: float,
                           market_analysis: Dict, order_type: str = "BUY") -> Dict:
        """
        🆕 ดึงระยะห่างแบบยืดหยุ่น - รองรับการวางได้เสมอ
        
        Args:
            target_price: ราคาเป้าหมายที่ต้องการวาง
            current_price: ราคาปัจจุบัน
            market_analysis: ผลการวิเคราะห์ 4D
            order_type: ประเภทออเดอร์
            
        Returns:
            Dict: ข้อมูลระยะห่างแบบยืดหยุ่น
        """
        try:
            # คำนวณระยะห่าง 4D
            spacing_result = self.calculate_4d_spacing(current_price, market_analysis, order_type)
            
            # คำนวณระยะห่างจริงที่ต้องการ
            actual_distance = abs(target_price - current_price)
            suggested_distance = spacing_result.spacing * self._get_point_value()
            
            # 4D AI: ไม่มีข้อจำกัด - ยอมรับทุกระยะห่าง
            is_acceptable = True  # วางได้เสมอ
            adjustment_needed = False
            
            # แนะนำราคาที่เหมาะสม (แต่ไม่บังคับ)
            if order_type.upper() == "BUY":
                suggested_price = current_price - suggested_distance
            else:
                suggested_price = current_price + suggested_distance
            
            return {
                "spacing_points": spacing_result.spacing,
                "spacing_price": suggested_distance,
                "target_price": target_price,
                "suggested_price": suggested_price,
                "actual_distance": actual_distance,
                "is_acceptable": is_acceptable,        # 4D AI: เสมอ True
                "adjustment_needed": adjustment_needed,  # 4D AI: เสมอ False
                "placement_allowed": True,             # 4D AI: วางได้เสมอ
                "collision_detected": False,           # 4D AI: ไม่เช็คการชน
                "four_d_score": spacing_result.four_d_score,
                "reasoning": spacing_result.reasoning + " | Flexible placement enabled",
                "warnings": [],  # ไม่มี warnings ใน 4D mode
                "recommendations": [
                    f"4D suggested spacing: {spacing_result.spacing} points",
                    f"4D opportunity score: {spacing_result.opportunity_factor:.3f}",
                    "Unlimited placement mode - all positions acceptable"
                ]
            }
            
        except Exception as e:
            self.log(f"❌ Flexible spacing error: {e}")
            return self._get_default_flexible_spacing(target_price, current_price)
    
    def check_placement_opportunity(self, price_level: float, current_price: float,
                                  market_analysis: Dict, order_type: str = "BUY") -> Dict:
        """
        🆕 เช็คโอกาสการวางออเดอร์ - 4D AI จะให้วางได้เสมอ
        
        Args:
            price_level: ระดับราคาที่ต้องการวาง
            current_price: ราคาปัจจุบัน
            market_analysis: ผลการวิเคราะห์ 4D
            order_type: ประเภทออเดอร์
            
        Returns:
            Dict: ข้อมูลโอกาสการวางออเดอร์
        """
        try:
            # คำนวณ 4D opportunity score
            four_d_score = market_analysis.get("market_score_4d", 0.5)
            opportunity_confidence = market_analysis.get("four_d_confidence", 0.5)
            
            # คำนวณ distance และ relative position
            distance = abs(price_level - current_price)
            relative_distance = distance / current_price * 100  # เปอร์เซ็นต์
            
            # 4D Opportunity Assessment
            opportunity_score = self._assess_4d_placement_opportunity(
                price_level, current_price, market_analysis, order_type
            )
            
            # Market context evaluation
            market_favorability = self._evaluate_4d_market_context(
                market_analysis, order_type
            )
            
            # 4D AI Decision: วางได้เสมอแต่ให้ scoring
            placement_recommendation = self._make_4d_placement_decision(
                opportunity_score, market_favorability, four_d_score
            )
            
            return {
                "can_place": True,                    # 4D AI: วางได้เสมอ
                "should_place": placement_recommendation["should_place"],
                "opportunity_score": opportunity_score,
                "market_favorability": market_favorability,
                "four_d_score": four_d_score,
                "confidence": opportunity_confidence,
                "distance_points": int(distance / self._get_point_value()),
                "relative_distance_pct": round(relative_distance, 3),
                "placement_timing": placement_recommendation["timing"],
                "quality_assessment": placement_recommendation["quality"],
                "reasoning": placement_recommendation["reasoning"],
                "collision_status": "NO_CHECK",      # 4D AI: ไม่เช็ค
                "restrictions": [],                  # 4D AI: ไม่มีข้อจำกัด
                "recommendations": placement_recommendation["recommendations"],
                "4d_dimension_scores": {
                    "trend_alignment": market_analysis.get("trend_dimension_score", 0.0),
                    "volume_confirmation": market_analysis.get("volume_dimension_score", 0.0),
                    "session_timing": market_analysis.get("session_dimension_score", 0.0),
                    "volatility_suitability": market_analysis.get("volatility_dimension_score", 0.0)
                }
            }
            
        except Exception as e:
            self.log(f"❌ Placement opportunity check error: {e}")
            return {
                "can_place": True,  # Default ใน 4D mode
                "opportunity_score": 0.5,
                "reasoning": f"Default placement allowed (Error: {str(e)})"
            }
    
    # ========================================================================================
    # 🧮 4D FACTOR CALCULATION METHODS
    # ========================================================================================
    
    def _calculate_4d_trend_factor(self, market_analysis: Dict) -> float:
        """คำนวณ Trend Factor จาก 4D analysis"""
        try:
            trend_strength = market_analysis.get("trend_strength", 0.0)
            trend_alignment = market_analysis.get("trend_alignment", 0.0)
            trend_direction = market_analysis.get("trend_direction", "SIDEWAYS")
            
            # Base trend factor
            if trend_direction in ["UP", "DOWN"]:
                base_factor = 1.2 + (trend_strength * 0.6)  # 1.2-1.8
            else:
                base_factor = 0.8 + (trend_strength * 0.4)  # 0.8-1.2
            
            # Alignment bonus
            alignment_bonus = trend_alignment * 0.3
            
            final_factor = base_factor + alignment_bonus
            return round(min(2.0, max(0.5, final_factor)), 3)
            
        except Exception as e:
            return 1.0
    
    def _calculate_4d_volume_factor(self, market_analysis: Dict) -> float:
        """คำนวณ Volume Factor จาก 4D analysis"""
        try:
            volume_strength = market_analysis.get("volume_strength", 0.5)
            volume_confirms = market_analysis.get("volume_confirms_trend", False)
            volume_trend = market_analysis.get("volume_trend", "UNKNOWN")
            
            # Base volume factor
            base_factor = 0.8 + (volume_strength * 0.8)  # 0.8-1.6
            
            # Confirmation bonus
            if volume_confirms:
                base_factor += 0.2
            
            # Trend bonus
            if volume_trend == "INCREASING":
                base_factor += 0.1
            
            return round(min(2.0, max(0.6, base_factor)), 3)
            
        except Exception as e:
            return 1.0
    
    def _calculate_4d_session_factor(self, market_analysis: Dict) -> float:
        """คำนวณ Session Factor จาก 4D analysis"""
        try:
            session_factor = market_analysis.get("session_factor", 1.0)
            is_major_session = market_analysis.get("is_major_session", False)
            activity_score = market_analysis.get("activity_score", 0.5)
            
            # Enhanced session factor
            enhanced_factor = session_factor * (1 + activity_score * 0.3)
            
            # Major session bonus
            if is_major_session:
                enhanced_factor += 0.2
            
            return round(min(2.0, max(0.5, enhanced_factor)), 3)
            
        except Exception as e:
            return 1.0
    
    def _calculate_4d_volatility_factor(self, market_analysis: Dict) -> float:
        """คำนวณ Volatility Factor จาก 4D analysis"""
        try:
            volatility_factor = market_analysis.get("volatility_factor", 1.0)
            volatility_level = market_analysis.get("volatility_level", "MEDIUM")
            breakout_potential = market_analysis.get("breakout_potential", 1.0)
            
            # Adjust based on volatility level
            level_adjustments = {
                "VERY_LOW": 0.7,
                "LOW": 0.85,
                "MEDIUM": 1.0,
                "HIGH": 1.3,
                "VERY_HIGH": 1.6
            }
            
            adjusted_factor = volatility_factor * level_adjustments.get(volatility_level, 1.0)
            
            # Breakout adjustment
            if breakout_potential > 1.2:
                adjusted_factor += 0.3
            
            return round(min(2.5, max(0.6, adjusted_factor)), 3)
            
        except Exception as e:
            return 1.0
    
    def _calculate_4d_opportunity_factor(self, four_d_score: float, 
                                       four_d_confidence: float,
                                       market_analysis: Dict) -> float:
        """คำนวณ Opportunity Factor จาก 4D analysis รวม"""
        try:
            # Base opportunity from 4D score
            base_opportunity = 0.5 + (four_d_score * 1.0)  # 0.5-1.5
            
            # Confidence multiplier
            confidence_multiplier = 0.8 + (four_d_confidence * 0.4)  # 0.8-1.2
            
            # Market condition bonus
            market_condition = market_analysis.get("market_condition_4d", "AVERAGE_4D")
            condition_bonuses = {
                "EXCELLENT_4D": 0.5,
                "GOOD_4D": 0.3,
                "AVERAGE_4D": 0.0,
                "POOR_4D": -0.2,
                "VERY_POOR_4D": -0.3
            }
            
            condition_bonus = condition_bonuses.get(market_condition, 0.0)
            
            final_opportunity = (base_opportunity * confidence_multiplier) + condition_bonus
            
            return round(min(2.5, max(0.4, final_opportunity)), 3)
            
        except Exception as e:
            return 1.0
    
    def _combine_4d_factors(self, trend: float, volume: float, session: float,
                          volatility: float, opportunity: float) -> float:
        """รวม 4D factors ด้วยการถ่วงน้ำหนัก"""
        try:
            # Weighted combination based on 4D config
            weights = self.four_d_config
            
            combined = (
                trend * 0.25 +           # 25% trend
                volume * 0.20 +          # 20% volume  
                session * 0.15 +         # 15% session
                volatility * 0.20 +      # 20% volatility
                opportunity * 0.20       # 20% opportunity
            )
            
            return round(max(0.3, min(3.0, combined)), 3)
            
        except Exception as e:
            return 1.0
    
    def _create_4d_reasoning(self, four_d_score: float, trend: float, volume: float,
                           session: float, volatility: float, opportunity: float,
                           multiplier: float, final_spacing: int) -> str:
        """สร้างคำอธิบาย 4D reasoning"""
        try:
            reasoning = (
                f"4D-AI: Score={four_d_score:.3f}, "
                f"T={trend:.1f}x, V={volume:.1f}x, S={session:.1f}x, "
                f"Vol={volatility:.1f}x, Opp={opportunity:.1f}x, "
                f"Final={multiplier:.2f}x→{final_spacing}pts"
            )
            
            # Add qualitative assessment
            if four_d_score >= 0.8:
                reasoning += " (EXCELLENT)"
            elif four_d_score >= 0.6:
                reasoning += " (GOOD)"
            elif four_d_score >= 0.4:
                reasoning += " (AVERAGE)"
            else:
                reasoning += " (CAUTIOUS)"
            
            return reasoning
            
        except Exception as e:
            return f"4D-AI: Error in reasoning ({str(e)})"
    
    # ========================================================================================
    # 🔧 ASSESSMENT AND DECISION METHODS
    # ========================================================================================
    
    def _assess_4d_placement_opportunity(self, price_level: float, current_price: float,
                                       market_analysis: Dict, order_type: str) -> float:
        """ประเมินโอกาสการวางออเดอร์แบบ 4D"""
        try:
            # Distance scoring
            distance_pct = abs(price_level - current_price) / current_price * 100
            if distance_pct < 0.1:
                distance_score = 0.9  # ใกล้มาก = โอกาสดี
            elif distance_pct < 0.3:
                distance_score = 0.7  # ใกล้ปานกลาง
            elif distance_pct < 0.8:
                distance_score = 0.5  # ไกลปานกลาง
            else:
                distance_score = 0.3  # ไกลมาก
            
            # Market alignment scoring
            trend_direction = market_analysis.get("trend_direction", "SIDEWAYS")
            if order_type.upper() == "BUY":
                alignment_score = 0.8 if trend_direction == "DOWN" else 0.6
            else:
                alignment_score = 0.8 if trend_direction == "UP" else 0.6
            
            # 4D context scoring
            four_d_score = market_analysis.get("market_score_4d", 0.5)
            context_score = four_d_score
            
            # Combined opportunity score
            opportunity = (distance_score * 0.4 + alignment_score * 0.3 + context_score * 0.3)
            
            return round(min(1.0, max(0.0, opportunity)), 3)
            
        except Exception as e:
            return 0.5
    
    def _evaluate_4d_market_context(self, market_analysis: Dict, order_type: str) -> float:
        """ประเมิน market context สำหรับการวางออเดอร์"""
        try:
            # Session favorability
            session_favorable = market_analysis.get("session_favorable", False)
            session_score = 0.8 if session_favorable else 0.5
            
            # Volatility favorability
            volatility_favorable = market_analysis.get("volatility_favorable", False)
            volatility_score = 0.8 if volatility_favorable else 0.5
            
            # Volume confirmation
            volume_confirms = market_analysis.get("volume_confirms_trend", False)
            volume_score = 0.7 if volume_confirms else 0.5
            
            # Overall 4D market condition
            market_condition = market_analysis.get("market_condition_4d", "AVERAGE_4D")
            condition_scores = {
                "EXCELLENT_4D": 0.9,
                "GOOD_4D": 0.75,
                "AVERAGE_4D": 0.5,
                "POOR_4D": 0.35,
                "VERY_POOR_4D": 0.2
            }
            condition_score = condition_scores.get(market_condition, 0.5)
            
            # Weighted market favorability
            favorability = (
                session_score * 0.25 +
                volatility_score * 0.25 +
                volume_score * 0.25 +
                condition_score * 0.25
            )
            
            return round(min(1.0, max(0.0, favorability)), 3)
            
        except Exception as e:
            return 0.5
    
    def _make_4d_placement_decision(self, opportunity_score: float,
                                  market_favorability: float, 
                                  four_d_score: float) -> Dict:
        """ตัดสินใจการวางออเดอร์แบบ 4D AI"""
        try:
            # Overall decision score
            decision_score = (
                opportunity_score * 0.4 +
                market_favorability * 0.3 +
                four_d_score * 0.3
            )
            
            # Decision categories
            if decision_score >= 0.8:
                should_place = True
                timing = "IMMEDIATE"
                quality = "EXCELLENT"
                recommendations = [
                    "Strong 4D opportunity - immediate placement recommended",
                    "High confidence market conditions",
                    "Optimal entry timing detected"
                ]
            elif decision_score >= 0.6:
                should_place = True
                timing = "FAVORABLE"
                quality = "GOOD"
                recommendations = [
                    "Good 4D opportunity - placement recommended",
                    "Favorable market conditions",
                    "Above-average entry timing"
                ]
            elif decision_score >= 0.4:
                should_place = True  # 4D AI: ยังแนะนำให้วาง
                timing = "ACCEPTABLE"
                quality = "AVERAGE"
                recommendations = [
                    "Acceptable 4D opportunity - placement allowed",
                    "Neutral market conditions",
                    "Standard entry timing"
                ]
            elif decision_score >= 0.25:
                should_place = True  # 4D AI: threshold ต่ำ
                timing = "CAUTIOUS"
                quality = "BELOW_AVERAGE"
                recommendations = [
                    "Below-average opportunity - cautious placement",
                    "Consider smaller position size",
                    "Monitor for improvement"
                ]
            else:
                should_place = True  # 4D AI: วางได้เสมอแต่เตือน
                timing = "WEAK"
                quality = "POOR"
                recommendations = [
                    "Poor opportunity but placement allowed",
                    "Use minimal position size",
                    "High monitoring required"
                ]
            
            reasoning = (
                f"4D Decision: {decision_score:.3f} "
                f"(Opp={opportunity_score:.2f}, Mkt={market_favorability:.2f}, "
                f"4D={four_d_score:.2f}) → {quality}"
            )
            
            return {
                "should_place": should_place,
                "timing": timing,
                "quality": quality,
                "decision_score": decision_score,
                "reasoning": reasoning,
                "recommendations": recommendations
            }
            
        except Exception as e:
            return {
                "should_place": True,  # Default in 4D mode
                "timing": "DEFAULT",
                "quality": "UNKNOWN",
                "reasoning": f"Default decision (Error: {str(e)})"
            }
    
    # ========================================================================================
    # 🔧 HELPER AND UTILITY METHODS
    # ========================================================================================
    
    def _get_point_value(self) -> float:
        """ดึงค่า point สำหรับสัญลักษณ์"""
        symbol_info = {
            "XAUUSD": 0.01,
            "EURUSD": 0.00001,
            "GBPUSD": 0.00001,
            "USDJPY": 0.001
        }
        return symbol_info.get(self.config.get("trading", {}).get("symbol", "XAUUSD"), 0.01)
    
    def _get_default_4d_spacing(self) -> Spacing4DResult:
        """ดึงระยะห่าง 4D default"""
        return Spacing4DResult(
            spacing=self.params_4d.base_spacing,
            reasoning="4D Default spacing - insufficient data",
            four_d_score=0.5,
            volatility_factor=1.0,
            trend_factor=1.0,
            session_factor=1.0,
            opportunity_factor=1.0,
            final_multiplier=1.0,
            mode_used=self.current_mode,
            placement_allowed=True,
            collision_detected=False
        )
    
    def _get_default_flexible_spacing(self, target_price: float, current_price: float) -> Dict:
        """ดึงระยะห่างยืดหยุ่น default"""
        return {
            "spacing_points": self.params_4d.base_spacing,
            "target_price": target_price,
            "is_acceptable": True,
            "placement_allowed": True,
            "collision_detected": False,
            "reasoning": "4D Default flexible spacing",
            "warnings": []
        }
    
    def _update_4d_history(self, spacing: int, four_d_score: float, reasoning: str):
        """อัปเดตประวัติการคำนวณ 4D"""
        try:
            history_entry = {
                "timestamp": datetime.now(),
                "spacing": spacing,
                "four_d_score": four_d_score,
                "mode": self.current_mode.value,
                "reasoning": reasoning
            }
            
            self.spacing_history_4d.append(history_entry)
            
            # Update performance metrics
            self.performance_4d["total_placements"] += 1
            self.performance_4d["average_4d_score"] = (
                (self.performance_4d["average_4d_score"] * 
                 (self.performance_4d["total_placements"] - 1) + four_d_score) /
                self.performance_4d["total_placements"]
            )
            
        except Exception as e:
            self.log(f"❌ 4D History update error: {e}")
    
    # ========================================================================================
    # 🔍 PUBLIC INTERFACE METHODS
    # ========================================================================================
    
    def set_4d_mode(self, mode: SpacingMode):
        """เปลี่ยนโหมด 4D spacing"""
        try:
            self.current_mode = mode
            self.log(f"4D Spacing mode changed to: {mode.value}")
        except Exception as e:
            self.log(f"❌ 4D Mode change error: {e}")
    
    def set_grid_strategy(self, strategy: GridBuildingStrategy):
        """เปลี่ยนกลยุทธ์การสร้างกริด"""
        try:
            self.grid_strategy = strategy
            self.log(f"Grid building strategy changed to: {strategy.value}")
        except Exception as e:
            self.log(f"❌ Grid strategy change error: {e}")
    
    def get_4d_performance(self) -> Dict:
        """ดึงข้อมูลประสิทธิภาพ 4D"""
        try:
            # Calculate additional metrics
            if self.spacing_history_4d:
                spacings = [h["spacing"] for h in self.spacing_history_4d]
                scores = [h["four_d_score"] for h in self.spacing_history_4d]
                
                performance = {
                    **self.performance_4d,
                    "spacing_statistics": {
                        "average_spacing": round(statistics.mean(spacings), 1),
                        "min_spacing": min(spacings),
                        "max_spacing": max(spacings),
                        "spacing_std_dev": round(statistics.stdev(spacings) if len(spacings) > 1 else 0, 1)
                    },
                    "score_statistics": {
                        "average_score": round(statistics.mean(scores), 3),
                        "min_score": round(min(scores), 3),
                        "max_score": round(max(scores), 3),
                        "score_trend": self._get_4d_score_trend()
                    },
                    "current_mode": self.current_mode.value,
                    "grid_strategy": self.grid_strategy.value,
                    "no_collision_active": True,
                    "unlimited_placement_active": True
                }
            else:
                performance = {
                    **self.performance_4d,
                    "spacing_statistics": {"insufficient_data": True},
                    "score_statistics": {"insufficient_data": True},
                    "current_mode": self.current_mode.value,
                    "grid_strategy": self.grid_strategy.value
                }
            
            return performance
            
        except Exception as e:
            self.log(f"❌ 4D Performance retrieval error: {e}")
            return {"error": str(e)}
    
    def _get_4d_score_trend(self) -> str:
        """ดึงแนวโน้มคะแนน 4D"""
        try:
            if len(self.spacing_history_4d) < 10:
                return "INSUFFICIENT_DATA"
            
            recent_scores = [h["four_d_score"] for h in list(self.spacing_history_4d)[-10:]]
            early_avg = statistics.mean(recent_scores[:5])
            late_avg = statistics.mean(recent_scores[5:])
            
            change_pct = (late_avg - early_avg) / early_avg * 100
            
            if change_pct > 5:
                return "IMPROVING"
            elif change_pct < -5:
                return "DECLINING"
            else:
                return "STABLE"
                
        except Exception as e:
            return "UNKNOWN"
    
    def get_placement_recommendations(self, current_price: float, 
                                   market_analysis: Dict) -> List[Dict]:
        """ดึงคำแนะนำการวางออเดอร์ 4D"""
        try:
            recommendations = []
            
            # BUY recommendations
            buy_spacing = self.calculate_4d_spacing(current_price, market_analysis, "BUY")
            buy_price = current_price - (buy_spacing.spacing * self._get_point_value())
            
            recommendations.append({
                "order_type": "BUY",
                "suggested_price": buy_price,
                "spacing": buy_spacing.spacing,
                "four_d_score": buy_spacing.four_d_score,
                "confidence": "HIGH" if buy_spacing.four_d_score > 0.7 else "MEDIUM" if buy_spacing.four_d_score > 0.4 else "LOW",
                "reasoning": buy_spacing.reasoning,
                "placement_allowed": True
            })
            
            # SELL recommendations
            sell_spacing = self.calculate_4d_spacing(current_price, market_analysis, "SELL")
            sell_price = current_price + (sell_spacing.spacing * self._get_point_value())
            
            recommendations.append({
                "order_type": "SELL", 
                "suggested_price": sell_price,
                "spacing": sell_spacing.spacing,
                "four_d_score": sell_spacing.four_d_score,
                "confidence": "HIGH" if sell_spacing.four_d_score > 0.7 else "MEDIUM" if sell_spacing.four_d_score > 0.4 else "LOW",
                "reasoning": sell_spacing.reasoning,
                "placement_allowed": True
            })
            
            return recommendations
            
        except Exception as e:
            self.log(f"❌ Placement recommendations error: {e}")
            return []
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 📏 SpacingManager: {message}")


# ========================================================================================
# 🧪 4D SPACING TEST FUNCTIONS
# ========================================================================================

# def test_4d_spacing_manager():
#     """Test 4D Spacing Manager functionality"""
#     print("🧪 Testing 4D Spacing Manager...")
#     print("✅ 4D Spacing Calculation (No Collision)")
#     print("✅ Flexible Spacing (Unlimited Placement)")
#     print("✅ Placement Opportunity Assessment")
#     print("✅ 4D Factor Calculations")
#     print("✅ Grid Building Strategy")
#     print("✅ Performance Tracking")
#     print("✅ Placement Recommendations")
#     print("✅ Ready for 4D AI Rule Engine Integration")

# if __name__ == "__main__":
#     test_4d_spacing_manager()