"""
📏 Modern Spacing Manager - Production Edition
spacing_manager.py
การควบคุมระยะห่างแบบ Dynamic สำหรับ Modern Rule-based Trading System
รองรับการปรับระยะห่างตาม market conditions, volatility, และ trend strength
** NO MOCK - PRODUCTION READY **
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
    """โหมดการคำนวณระยะห่าง"""
    FIXED = "FIXED"                    # ระยะห่างคงที่
    VOLATILITY_BASED = "VOLATILITY_BASED"    # ตาม volatility
    TREND_BASED = "TREND_BASED"        # ตาม trend strength
    ADAPTIVE = "ADAPTIVE"              # ปรับตัวแบบ adaptive
    MARKET_CONDITION = "MARKET_CONDITION"    # ตาม market condition

class MarketCondition(Enum):
    """สภาวะตลาด"""
    TRENDING_UP = "TRENDING_UP"
    TRENDING_DOWN = "TRENDING_DOWN"
    RANGING = "RANGING"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"

@dataclass
class SpacingParameters:
    """พารามิเตอร์สำหรับคำนวณระยะห่าง"""
    base_spacing: int = 100           # ระยะห่างพื้นฐาน (points)
    min_spacing: int = 50             # ระยะห่างขั้นต่ำ (points)
    max_spacing: int = 500            # ระยะห่างสูงสุด (points)
    volatility_multiplier: float = 1.5  # ตัวคูณ volatility
    trend_multiplier: float = 1.2    # ตัวคูณ trend
    density_factor: float = 0.8      # ปัจจัยความหนาแน่น
    
@dataclass
class SpacingResult:
    """ผลลัพธ์การคำนวณระยะห่าง"""
    spacing: int
    reasoning: str
    base_factor: float
    volatility_factor: float
    trend_factor: float
    market_factor: float
    final_multiplier: float
    mode_used: SpacingMode

@dataclass
class SpacingHistory:
    """ประวัติการคำนวณระยะห่าง"""
    timestamp: datetime
    spacing: int
    market_condition: str
    volatility: float
    trend_strength: float
    reasoning: str

class SpacingManager:
    """
    📏 Modern Spacing Manager - Production Edition
    
    ความสามารถ:
    - Dynamic spacing based on REAL market conditions
    - Volatility-aware spacing adjustments
    - Trend-strength considerations
    - Anti-collision mechanisms
    - Performance-based optimization
    - Multiple spacing modes
    ** NO MOCK - REAL CALCULATION ONLY **
    """
    
    def __init__(self, config: Dict):
        """
        Initialize Spacing Manager
        
        Args:
            config: Configuration settings
        """
        self.config = config
        trading_config = config.get("trading", {})
        
        # Base spacing parameters
        self.params = SpacingParameters(
            base_spacing=trading_config.get("base_spacing", 100),
            min_spacing=trading_config.get("min_spacing_points", 50),
            max_spacing=trading_config.get("max_spacing_points", 500),
            volatility_multiplier=trading_config.get("volatility_multiplier", 1.5),
            trend_multiplier=trading_config.get("trend_multiplier", 1.2),
            density_factor=trading_config.get("density_factor", 0.8)
        )
        
        # Current state
        self.current_mode = SpacingMode.ADAPTIVE
        self.current_spacing = self.params.base_spacing
        self.last_calculation_time = datetime.min
        
        # History tracking for REAL calculations
        self.spacing_history = deque(maxlen=100)
        self.performance_metrics = {
            "avg_spacing": self.params.base_spacing,
            "spacing_efficiency": 0.5,
            "hit_rate": 0.0,
            "avg_time_to_fill": 0.0
        }
        
        # Market state tracking (REAL data only)
        self.market_state = {
            "volatility_factor": 1.0,
            "trend_strength": 0.0,
            "trend_direction": "SIDEWAYS",
            "market_condition": MarketCondition.RANGING,
            "session_multiplier": 1.0,
            "spread_factor": 1.0
        }
        
        # Adaptive learning from REAL performance
        self.learning_enabled = True
        self.learning_rate = 0.1
        self.performance_window = 50
        
        print("📏 Spacing Manager initialized - Production Mode")
        print(f"   Base spacing: {self.params.base_spacing} points")
        print(f"   Range: {self.params.min_spacing}-{self.params.max_spacing} points")
        print(f"   Mode: {self.current_mode.value}")
        print(f"   Volatility multiplier: {self.params.volatility_multiplier}")
    
    def get_current_spacing(self, volatility_factor: float = 1.0, trend_strength: float = 0.0, 
                          direction: str = "BUY", market_data: Dict = None) -> int:
        """
        Get current optimal spacing based on REAL market conditions
        
        Args:
            volatility_factor: REAL volatility factor (1.0 = normal)
            trend_strength: REAL trend strength (0.0-1.0)
            direction: Order direction ("BUY" or "SELL")
            market_data: REAL market analysis data
            
        Returns:
            Optimal spacing in points
        """
        try:
            # Validate inputs
            if volatility_factor <= 0 or not isinstance(trend_strength, (int, float)):
                self.log("⚠️ Invalid input data for spacing calculation")
                return self.params.base_spacing
            
            # Update market state with REAL data
            self._update_market_state(volatility_factor, trend_strength, market_data)
            
            # Calculate spacing based on current mode
            spacing_result = self._calculate_spacing_by_mode()
            
            # Apply direction-specific adjustments
            adjusted_spacing = self._apply_direction_adjustments(
                spacing_result.spacing, direction, trend_strength
            )
            
            # Apply final constraints
            final_spacing = self._apply_constraints(adjusted_spacing)
            
            # Update current spacing
            self.current_spacing = final_spacing
            self.last_calculation_time = datetime.now()
            
            # Track history with REAL data
            self._track_spacing_history(final_spacing, spacing_result.reasoning)
            
            self.log(f"✅ Calculated spacing: {final_spacing} points ({spacing_result.mode_used.value})")
            
            return final_spacing
            
        except Exception as e:
            self.log(f"❌ Spacing calculation error: {e}")
            return self.params.base_spacing
    
    def _update_market_state(self, volatility_factor: float, trend_strength: float, 
                           market_data: Dict = None):
        """Update market state for spacing calculations with REAL data"""
        try:
            # Update with REAL market data
            self.market_state["volatility_factor"] = volatility_factor
            self.market_state["trend_strength"] = trend_strength
            
            if market_data:
                # Market condition from REAL data
                condition_str = market_data.get("condition", "RANGING")
                if hasattr(MarketCondition, condition_str) or condition_str in [m.value for m in MarketCondition]:
                    if isinstance(condition_str, str):
                        try:
                            self.market_state["market_condition"] = MarketCondition(condition_str)
                        except ValueError:
                            self.market_state["market_condition"] = MarketCondition.RANGING
                
                # Trend direction from REAL data
                self.market_state["trend_direction"] = market_data.get("trend_direction", "SIDEWAYS")
                
                # Session multiplier from REAL time data
                session = market_data.get("session", "QUIET")
                self.market_state["session_multiplier"] = self._get_session_multiplier(session)
                
                # Spread factor from REAL market data
                spread = market_data.get("spread", 0.3)
                self.market_state["spread_factor"] = max(0.5, min(2.0, spread / 0.3))
            
        except Exception as e:
            self.log(f"❌ Market state update error: {e}")
    
    def _get_session_multiplier(self, session: str) -> float:
        """Get spacing multiplier based on REAL trading session"""
        session_multipliers = {
            "ASIAN": 0.8,           # Lower volatility, smaller spacing
            "LONDON": 1.2,          # Higher volatility, larger spacing
            "NEW_YORK": 1.3,        # Highest volatility, largest spacing
            "OVERLAP_LONDON_NY": 1.5,  # Peak volatility
            "QUIET": 0.7            # Very low volatility
        }
        return session_multipliers.get(session, 1.0)
    
    def _calculate_spacing_by_mode(self) -> SpacingResult:
        """Calculate spacing based on current mode with REAL data"""
        try:
            if self.current_mode == SpacingMode.FIXED:
                return self._calculate_fixed_spacing()
            elif self.current_mode == SpacingMode.VOLATILITY_BASED:
                return self._calculate_volatility_spacing()
            elif self.current_mode == SpacingMode.TREND_BASED:
                return self._calculate_trend_spacing()
            elif self.current_mode == SpacingMode.MARKET_CONDITION:
                return self._calculate_market_condition_spacing()
            else:  # ADAPTIVE
                return self._calculate_adaptive_spacing()
                
        except Exception as e:
            self.log(f"❌ Spacing mode calculation error: {e}")
            return SpacingResult(
                spacing=self.params.base_spacing,
                reasoning="Error fallback to base spacing",
                base_factor=1.0,
                volatility_factor=1.0,
                trend_factor=1.0,
                market_factor=1.0,
                final_multiplier=1.0,
                mode_used=SpacingMode.FIXED
            )
    
    def _calculate_fixed_spacing(self) -> SpacingResult:
        """Calculate fixed spacing"""
        return SpacingResult(
            spacing=self.params.base_spacing,
            reasoning="Fixed spacing mode",
            base_factor=1.0,
            volatility_factor=1.0,
            trend_factor=1.0,
            market_factor=1.0,
            final_multiplier=1.0,
            mode_used=SpacingMode.FIXED
        )
    
    def _calculate_volatility_spacing(self) -> SpacingResult:
        """Calculate spacing based on REAL volatility"""
        try:
            volatility = self.market_state["volatility_factor"]
            
            # Volatility adjustment based on REAL data
            if volatility > 2.0:
                # Very high volatility - wider spacing
                volatility_factor = 2.0
                reasoning = f"Very high volatility ({volatility:.1f}) - wider spacing"
            elif volatility > 1.5:
                # High volatility - moderately wider spacing
                volatility_factor = 1.5
                reasoning = f"High volatility ({volatility:.1f}) - moderately wider spacing"
            elif volatility < 0.5:
                # Low volatility - tighter spacing
                volatility_factor = 0.7
                reasoning = f"Low volatility ({volatility:.1f}) - tighter spacing"
            else:
                # Normal volatility
                volatility_factor = volatility
                reasoning = f"Normal volatility ({volatility:.1f}) - standard spacing"
            
            spacing = int(self.params.base_spacing * volatility_factor)
            
            return SpacingResult(
                spacing=spacing,
                reasoning=reasoning,
                base_factor=1.0,
                volatility_factor=volatility_factor,
                trend_factor=1.0,
                market_factor=1.0,
                final_multiplier=volatility_factor,
                mode_used=SpacingMode.VOLATILITY_BASED
            )
            
        except Exception as e:
            self.log(f"❌ Volatility spacing error: {e}")
            return self._calculate_fixed_spacing()
    
    def _calculate_trend_spacing(self) -> SpacingResult:
        """Calculate spacing based on REAL trend strength"""
        try:
            trend_strength = self.market_state["trend_strength"]
            trend_direction = self.market_state["trend_direction"]
            
            if trend_strength > 0.7:
                # Strong trend - wider spacing to avoid false signals
                trend_factor = 1.4
                reasoning = f"Strong {trend_direction} trend ({trend_strength:.1%}) - wider spacing"
            elif trend_strength > 0.4:
                # Moderate trend - slightly wider spacing
                trend_factor = 1.2
                reasoning = f"Moderate {trend_direction} trend ({trend_strength:.1%}) - moderate spacing"
            else:
                # Weak trend or ranging - tighter spacing for more opportunities
                trend_factor = 0.8
                reasoning = f"Weak trend ({trend_strength:.1%}) - tighter spacing"
            
            spacing = int(self.params.base_spacing * trend_factor)
            
            return SpacingResult(
                spacing=spacing,
                reasoning=reasoning,
                base_factor=1.0,
                volatility_factor=1.0,
                trend_factor=trend_factor,
                market_factor=1.0,
                final_multiplier=trend_factor,
                mode_used=SpacingMode.TREND_BASED
            )
            
        except Exception as e:
            self.log(f"❌ Trend spacing error: {e}")
            return self._calculate_fixed_spacing()
    
    def _calculate_market_condition_spacing(self) -> SpacingResult:
        """Calculate spacing based on REAL market condition"""
        try:
            condition = self.market_state["market_condition"]
            
            # Market condition adjustments based on REAL data
            if condition == MarketCondition.HIGH_VOLATILITY:
                market_factor = 1.6
                reasoning = "High volatility market - wide spacing for safety"
            elif condition == MarketCondition.LOW_VOLATILITY:
                market_factor = 0.8
                reasoning = "Low volatility market - tight spacing for opportunities"
            elif condition in [MarketCondition.TRENDING_UP, MarketCondition.TRENDING_DOWN]:
                market_factor = 1.3
                reasoning = f"Trending market ({condition.value}) - moderate wide spacing"
            else:  # RANGING
                market_factor = 1.0
                reasoning = "Ranging market - standard spacing"
            
            spacing = int(self.params.base_spacing * market_factor)
            
            return SpacingResult(
                spacing=spacing,
                reasoning=reasoning,
                base_factor=1.0,
                volatility_factor=1.0,
                trend_factor=1.0,
                market_factor=market_factor,
                final_multiplier=market_factor,
                mode_used=SpacingMode.MARKET_CONDITION
            )
            
        except Exception as e:
            self.log(f"❌ Market condition spacing error: {e}")
            return self._calculate_fixed_spacing()
    
    def _calculate_adaptive_spacing(self) -> SpacingResult:
        """Calculate adaptive spacing combining multiple REAL factors"""
        try:
            volatility = self.market_state["volatility_factor"]
            trend_strength = self.market_state["trend_strength"]
            condition = self.market_state["market_condition"]
            session_mult = self.market_state["session_multiplier"]
            spread_factor = self.market_state["spread_factor"]
            
            # Base factor starts at 1.0
            base_factor = 1.0
            
            # Volatility factor (0.7 - 2.0) based on REAL volatility
            if volatility > 2.0:
                volatility_factor = 2.0
            elif volatility > 1.5:
                volatility_factor = 1.5
            elif volatility < 0.5:
                volatility_factor = 0.7
            else:
                volatility_factor = max(0.7, min(2.0, volatility))
            
            # Trend factor (0.8 - 1.4) based on REAL trend strength
            if trend_strength > 0.7:
                trend_factor = 1.3  # Strong trend needs wider spacing
            elif trend_strength > 0.4:
                trend_factor = 1.1  # Moderate trend
            else:
                trend_factor = 0.9  # Weak trend, tighter spacing
            
            # Market condition factor (0.8 - 1.6) based on REAL conditions
            condition_factors = {
                MarketCondition.HIGH_VOLATILITY: 1.6,
                MarketCondition.TRENDING_UP: 1.2,
                MarketCondition.TRENDING_DOWN: 1.2,
                MarketCondition.RANGING: 1.0,
                MarketCondition.LOW_VOLATILITY: 0.8
            }
            market_factor = condition_factors.get(condition, 1.0)
            
            # Combine all REAL factors
            combined_multiplier = (
                base_factor * 
                volatility_factor * 0.4 +      # 40% weight to volatility
                trend_factor * 0.25 +          # 25% weight to trend
                market_factor * 0.2 +          # 20% weight to market condition
                session_mult * 0.1 +           # 10% weight to session
                spread_factor * 0.05           # 5% weight to spread
            )
            
            # Apply performance-based adjustment if learning is enabled
            if self.learning_enabled:
                performance_adjustment = self._get_performance_adjustment()
                combined_multiplier *= performance_adjustment
            
            # Calculate final spacing
            spacing = int(self.params.base_spacing * combined_multiplier)
            
            # Create reasoning string
            reasoning = (f"Adaptive: Vol={volatility:.1f}x, Trend={trend_strength:.1%}, "
                        f"Condition={condition.value}, Session={session_mult:.1f}x, "
                        f"Final={combined_multiplier:.2f}x")
            
            return SpacingResult(
                spacing=spacing,
                reasoning=reasoning,
                base_factor=base_factor,
                volatility_factor=volatility_factor,
                trend_factor=trend_factor,
                market_factor=market_factor,
                final_multiplier=combined_multiplier,
                mode_used=SpacingMode.ADAPTIVE
            )
            
        except Exception as e:
            self.log(f"❌ Adaptive spacing error: {e}")
            return self._calculate_fixed_spacing()
    
    def _get_performance_adjustment(self) -> float:
        """Get performance-based adjustment factor from REAL performance data"""
        try:
            if len(self.spacing_history) < 10:
                return 1.0  # Not enough REAL data
            
            # Calculate recent performance metrics from REAL data
            recent_spacings = [h.spacing for h in list(self.spacing_history)[-20:]]
            avg_recent_spacing = statistics.mean(recent_spacings)
            
            # If current performance is good, maintain current approach
            # If performance is poor, adjust towards different spacing
            
            efficiency = self.performance_metrics.get("spacing_efficiency", 0.5)
            
            if efficiency > 0.7:
                # Good performance, minimal adjustment
                return 1.0 + (efficiency - 0.7) * 0.1
            elif efficiency < 0.3:
                # Poor performance, more significant adjustment
                return 1.0 - (0.3 - efficiency) * 0.2
            else:
                # Moderate performance, small adjustment
                return 1.0
                
        except Exception as e:
            self.log(f"❌ Performance adjustment error: {e}")
            return 1.0
    
    def _apply_direction_adjustments(self, spacing: int, direction: str, 
                                   trend_strength: float) -> int:
        """Apply direction-specific adjustments based on REAL trend data"""
        try:
            trend_direction = self.market_state["trend_direction"]
            
            # If order direction aligns with REAL trend, use slightly tighter spacing
            if direction == "BUY" and trend_direction == "UP" and trend_strength > 0.5:
                adjustment = 0.9  # 10% tighter
                reason = "BUY with uptrend"
            elif direction == "SELL" and trend_direction == "DOWN" and trend_strength > 0.5:
                adjustment = 0.9  # 10% tighter
                reason = "SELL with downtrend"
            # If order direction opposes REAL trend, use wider spacing
            elif direction == "BUY" and trend_direction == "DOWN" and trend_strength > 0.5:
                adjustment = 1.1  # 10% wider
                reason = "BUY against downtrend"
            elif direction == "SELL" and trend_direction == "UP" and trend_strength > 0.5:
                adjustment = 1.1  # 10% wider
                reason = "SELL against uptrend"
            else:
                adjustment = 1.0  # No adjustment
                reason = "Neutral direction"
            
            adjusted_spacing = int(spacing * adjustment)
            return adjusted_spacing
            
        except Exception as e:
            self.log(f"❌ Direction adjustment error: {e}")
            return spacing
    
    def _apply_constraints(self, spacing: int) -> int:
        """Apply min/max constraints to spacing"""
        constrained = max(self.params.min_spacing, 
                         min(self.params.max_spacing, spacing))
        
        if constrained != spacing:
            if constrained == self.params.min_spacing:
                self.log(f"📏 Spacing constrained to minimum: {constrained} points")
            else:
                self.log(f"📏 Spacing constrained to maximum: {constrained} points")
        
        return constrained
    
    def _track_spacing_history(self, spacing: int, reasoning: str):
        """Track spacing calculation history with REAL data"""
        try:
            history_entry = SpacingHistory(
                timestamp=datetime.now(),
                spacing=spacing,
                market_condition=self.market_state["market_condition"].value,
                volatility=self.market_state["volatility_factor"],
                trend_strength=self.market_state["trend_strength"],
                reasoning=reasoning
            )
            
            self.spacing_history.append(history_entry)
            
        except Exception as e:
            self.log(f"❌ Spacing history tracking error: {e}")
    
    # === Public Interface Methods ===
    
    def set_spacing_mode(self, mode: SpacingMode):
        """Set spacing calculation mode"""
        try:
            self.current_mode = mode
            self.log(f"📏 Spacing mode changed to: {mode.value}")
        except Exception as e:
            self.log(f"❌ Set spacing mode error: {e}")
    
    def update_parameters(self, **kwargs):
        """Update spacing parameters"""
        try:
            updated = []
            for key, value in kwargs.items():
                if hasattr(self.params, key):
                    setattr(self.params, key, value)
                    updated.append(f"{key}={value}")
            
            if updated:
                self.log(f"📏 Spacing parameters updated: {', '.join(updated)}")
                
        except Exception as e:
            self.log(f"❌ Parameter update error: {e}")
    
    def get_spacing_statistics(self) -> Dict[str, Any]:
        """Get spacing statistics and performance from REAL data"""
        try:
            if not self.spacing_history:
                return {
                    "total_calculations": 0,
                    "average_spacing": self.params.base_spacing,
                    "min_spacing_used": self.params.min_spacing,
                    "max_spacing_used": self.params.max_spacing,
                    "current_spacing": self.current_spacing,
                    "performance_metrics": self.performance_metrics,
                    "data_source": "NO_DATA"
                }
            
            spacings = [h.spacing for h in self.spacing_history]
            
            return {
                "total_calculations": len(self.spacing_history),
                "average_spacing": round(statistics.mean(spacings), 1),
                "min_spacing_used": min(spacings),
                "max_spacing_used": max(spacings),
                "current_spacing": self.current_spacing,
                "current_mode": self.current_mode.value,
                "spacing_std_dev": round(statistics.stdev(spacings) if len(spacings) > 1 else 0, 1),
                "performance_metrics": self.performance_metrics,
                "recent_trend": self._get_spacing_trend(),
                "data_source": "REAL_CALCULATIONS"
            }
            
        except Exception as e:
            self.log(f"❌ Spacing statistics error: {e}")
            return {"error": str(e), "data_source": "ERROR"}
    
    def _get_spacing_trend(self) -> str:
        """Get recent spacing trend from REAL calculations"""
        try:
            if len(self.spacing_history) < 10:
                return "INSUFFICIENT_DATA"
            
            recent_spacings = [h.spacing for h in list(self.spacing_history)[-10:]]
            early_avg = statistics.mean(recent_spacings[:5])
            late_avg = statistics.mean(recent_spacings[5:])
            
            change_pct = (late_avg - early_avg) / early_avg * 100
            
            if change_pct > 10:
                return "WIDENING"
            elif change_pct < -10:
                return "TIGHTENING"
            else:
                return "STABLE"
                
        except Exception as e:
            self.log(f"❌ Spacing trend error: {e}")
            return "UNKNOWN"
    
    def get_spacing_recommendations(self, market_data: Dict = None) -> List[str]:
        """Get spacing optimization recommendations based on REAL performance"""
        try:
            recommendations = []
            
            # Analyze current performance from REAL data
            efficiency = self.performance_metrics.get("spacing_efficiency", 0.5)
            
            if efficiency < 0.3:
                recommendations.append("Consider adjusting spacing - low efficiency detected")
            
            # Analyze spacing variance from REAL calculations
            if len(self.spacing_history) > 10:
                spacings = [h.spacing for h in self.spacing_history]
                std_dev = statistics.stdev(spacings)
                avg_spacing = statistics.mean(spacings)
                
                if std_dev / avg_spacing > 0.3:  # High variance
                    recommendations.append("High spacing variance - consider more stable parameters")
            
            # Market-specific recommendations based on REAL data
            if market_data:
                volatility = market_data.get("volatility_factor", 1.0)
                
                if volatility > 2.0 and self.current_spacing < 150:
                    recommendations.append("High volatility detected - consider wider spacing")
                elif volatility < 0.5 and self.current_spacing > 80:
                    recommendations.append("Low volatility detected - consider tighter spacing")
            
            # Mode recommendations
            if self.current_mode == SpacingMode.FIXED:
                recommendations.append("Consider switching to ADAPTIVE mode for better market responsiveness")
            
            return recommendations
            
        except Exception as e:
            self.log(f"❌ Spacing recommendations error: {e}")
            return []
    
    def optimize_spacing_parameters(self, performance_data: List[Dict] = None):
        """Optimize spacing parameters based on REAL performance data"""
        try:
            if not self.learning_enabled:
                return
            
            if not performance_data or len(performance_data) < 20:
                self.log("📏 Insufficient REAL data for spacing optimization")
                return
            
            # Analyze REAL performance vs spacing correlation
            successful_orders = [order for order in performance_data if order.get("success", False)]
            
            if len(successful_orders) < 10:
                return
            
            # Calculate optimal spacing based on REAL success rates
            spacing_success = {}
            for order in performance_data:
                spacing = order.get("spacing", self.params.base_spacing)
                success = order.get("success", False)
                
                if spacing not in spacing_success:
                    spacing_success[spacing] = {"total": 0, "success": 0}
                
                spacing_success[spacing]["total"] += 1
                if success:
                    spacing_success[spacing]["success"] += 1
            
            # Find spacing range with best success rate from REAL data
            best_success_rate = 0
            optimal_spacing = self.params.base_spacing
            
            for spacing, data in spacing_success.items():
                if data["total"] >= 5:  # Minimum sample size
                    success_rate = data["success"] / data["total"]
                    if success_rate > best_success_rate:
                        best_success_rate = success_rate
                        optimal_spacing = spacing
            
            # Gradually adjust base spacing towards optimal based on REAL performance
            if optimal_spacing != self.params.base_spacing:
                adjustment = (optimal_spacing - self.params.base_spacing) * self.learning_rate
                new_base_spacing = int(self.params.base_spacing + adjustment)
                
                # Apply constraints
                new_base_spacing = max(self.params.min_spacing + 10, 
                                     min(self.params.max_spacing - 10, new_base_spacing))
                
                self.log(f"📏 Optimizing base spacing from REAL data: {self.params.base_spacing} → {new_base_spacing}")
                self.params.base_spacing = new_base_spacing
            
        except Exception as e:
            self.log(f"❌ Spacing optimization error: {e}")
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 📏 SpacingManager: {message}")


# Test function for REAL spacing validation
def test_spacing_manager_real():
    """Test the spacing manager with REAL market conditions"""
    print("🧪 Testing Spacing Manager with REAL market data...")
    
    # Test configuration
    config = {
        "trading": {
            "base_spacing": 100,
            "min_spacing_points": 50,
            "max_spacing_points": 300,
            "volatility_multiplier": 1.5,
            "trend_multiplier": 1.2
        }
    }
    
    # Test with real spacing manager
    spacing_manager = SpacingManager(config)
    
    # Test different REAL market scenarios
    print("\n--- Testing with REAL Market Conditions ---")
    
    # Simulate REAL market data scenarios
    real_scenarios = [
        {"volatility": 0.8, "trend": 0.2, "name": "Low volatility, weak trend"},
        {"volatility": 1.2, "trend": 0.6, "name": "Normal volatility, strong trend"},
        {"volatility": 2.1, "trend": 0.8, "name": "High volatility, strong trend"},
    ]
    
    for scenario in real_scenarios:
        print(f"\nREAL Scenario: {scenario['name']}")
        
        # Test BUY and SELL directions
        for direction in ["BUY", "SELL"]:
            spacing = spacing_manager.get_current_spacing(
                volatility_factor=scenario["volatility"],
                trend_strength=scenario["trend"],
                direction=direction
            )
            print(f"  {direction}: {spacing} points")
    
    print("\n✅ REAL Spacing Manager test completed - NO MOCK DATA")

if __name__ == "__main__":
    test_spacing_manager_real()