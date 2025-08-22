"""
🔢 Modern Lot Calculator
lot_calculator.py
การคำนวณขนาด lot แบบ optimal สำหรับ Modern Rule-based Trading System
รองรับการปรับขนาดตาม risk, confidence, market conditions และ account balance
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import deque
import statistics

class LotCalculationMethod(Enum):
    """วิธีการคำนวณ lot size"""
    FIXED = "FIXED"
    PERCENTAGE_RISK = "PERCENTAGE_RISK"
    VOLATILITY_ADJUSTED = "VOLATILITY_ADJUSTED"
    CONFIDENCE_BASED = "CONFIDENCE_BASED"
    MARKET_CONDITION = "MARKET_CONDITION"
    DYNAMIC_HYBRID = "DYNAMIC_HYBRID"
    KELLY_CRITERION = "KELLY_CRITERION"
    PROGRESSIVE_SIZING = "PROGRESSIVE_SIZING"

class RiskLevel(Enum):
    """ระดับความเสี่ยง"""
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"
    AGGRESSIVE = "AGGRESSIVE"
    VERY_AGGRESSIVE = "VERY_AGGRESSIVE"

@dataclass
class LotCalculationParams:
    """พารามิเตอร์การคำนวณ lot"""
    account_balance: float
    account_equity: float
    free_margin: float
    base_lot_size: float
    max_risk_percentage: float
    confidence_level: float
    volatility_factor: float
    market_condition: str
    existing_exposure: float
    trade_direction: str
    symbol_info: Dict[str, Any]

@dataclass
class LotCalculationResult:
    """ผลลัพธ์การคำนวณ lot"""
    lot_size: float
    calculation_method: LotCalculationMethod
    risk_amount: float
    risk_percentage: float
    margin_required: float
    confidence_factor: float
    volatility_adjustment: float
    reasoning: str
    warnings: List[str]
    calculation_factors: Dict[str, float]
    timestamp: datetime
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class LotCalculator:
    """
    🔢 Modern Lot Calculator
    
    ความสามารถ:
    - Multiple lot calculation methods
    - Risk-based position sizing
    - Confidence-weighted adjustments
    - Market condition awareness
    - Volatility-adaptive sizing
    - Progressive lot scaling
    - Kelly Criterion implementation
    - Performance-based optimization
    """
    
    def __init__(self, account_info: Dict, config: Dict):
        """
        Initialize Lot Calculator
        
        Args:
            account_info: Account information from MT5
            config: Configuration settings
        """
        self.account_info = account_info
        self.config = config
        
        # Base parameters
        self.base_lot_size = config.get("trading", {}).get("base_lot_size", 0.01)
        self.max_risk_percentage = config.get("risk_management", {}).get("max_risk_percentage", 2.0)
        self.max_lot_size = config.get("trading", {}).get("max_lot_size", 1.0)
        self.min_lot_size = config.get("trading", {}).get("min_lot_size", 0.01)
        
        # Calculation method and weights
        self.current_method = LotCalculationMethod.DYNAMIC_HYBRID
        self.method_weights = {
            LotCalculationMethod.PERCENTAGE_RISK: 0.3,
            LotCalculationMethod.CONFIDENCE_BASED: 0.25,
            LotCalculationMethod.VOLATILITY_ADJUSTED: 0.2,
            LotCalculationMethod.MARKET_CONDITION: 0.15,
            LotCalculationMethod.FIXED: 0.1
        }
        
        # Risk management
        self.risk_levels = {
            RiskLevel.CONSERVATIVE: {"max_risk": 1.0, "lot_multiplier": 0.5},
            RiskLevel.MODERATE: {"max_risk": 2.0, "lot_multiplier": 1.0},
            RiskLevel.AGGRESSIVE: {"max_risk": 4.0, "lot_multiplier": 1.5},
            RiskLevel.VERY_AGGRESSIVE: {"max_risk": 6.0, "lot_multiplier": 2.0}
        }
        
        # Performance tracking
        self.lot_performance_history = deque(maxlen=100)
        self.calculation_history = deque(maxlen=50)
        
        # Adaptive parameters
        self.learning_rate = 0.1
        self.performance_window = 20
        self.optimization_threshold = 0.7
        
        # Symbol information
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.point_value = 0.01
        self.contract_size = 100
        self.margin_percentage = 1.0
        
        # Progressive sizing
        self.progressive_factor = 1.2
        self.max_progressive_multiplier = 3.0
        
        print("🔢 Lot Calculator initialized")
        print(f"   Base lot size: {self.base_lot_size}")
        print(f"   Max risk: {self.max_risk_percentage}%")
        print(f"   Method: {self.current_method.value}")
        print(f"   Account balance: ${self.account_info.get('balance', 0):,.2f}")
    
    def calculate_optimal_lot_size(self, market_data: Dict = None, confidence: float = 0.5,
                                 order_type: str = "BUY", reasoning: str = "") -> float:
        """
        Calculate optimal lot size based on current conditions
        
        Args:
            market_data: Current market analysis data
            confidence: Trading confidence level (0.0-1.0)
            order_type: Type of order ("BUY", "SELL")
            reasoning: Reasoning for the trade
            
        Returns:
            Optimal lot size
        """
        try:
            # Prepare calculation parameters
            calc_params = self._prepare_calculation_params(
                market_data, confidence, order_type
            )
            
            # Calculate using current method
            if self.current_method == LotCalculationMethod.DYNAMIC_HYBRID:
                result = self._calculate_hybrid_lot_size(calc_params, reasoning)
            elif self.current_method == LotCalculationMethod.PERCENTAGE_RISK:
                result = self._calculate_percentage_risk_lot(calc_params)
            elif self.current_method == LotCalculationMethod.CONFIDENCE_BASED:
                result = self._calculate_confidence_based_lot(calc_params)
            elif self.current_method == LotCalculationMethod.VOLATILITY_ADJUSTED:
                result = self._calculate_volatility_adjusted_lot(calc_params)
            elif self.current_method == LotCalculationMethod.KELLY_CRITERION:
                result = self._calculate_kelly_criterion_lot(calc_params)
            elif self.current_method == LotCalculationMethod.PROGRESSIVE_SIZING:
                result = self._calculate_progressive_lot(calc_params)
            else:  # FIXED
                result = self._calculate_fixed_lot(calc_params)
            
            # Validate and apply bounds
            final_lot_size = self._validate_and_bound_lot_size(result.lot_size)
            result.lot_size = final_lot_size
            
            # Add to calculation history
            self.calculation_history.append(result)
            
            print(f"🔢 Lot calculated: {final_lot_size:.3f}")
            print(f"   💭 Method: {result.calculation_method.value}")
            print(f"   📊 Risk: ${result.risk_amount:.2f} ({result.risk_percentage:.1f}%)")
            print(f"   🎯 Confidence factor: {result.confidence_factor:.2f}")
            print(f"   💭 Reasoning: {result.reasoning}")
            
            if result.warnings:
                for warning in result.warnings:
                    print(f"   ⚠️ Warning: {warning}")
            
            return final_lot_size
            
        except Exception as e:
            print(f"❌ Lot calculation error: {e}")
            return self.base_lot_size
    
    def _prepare_calculation_params(self, market_data: Dict, confidence: float,
                                  order_type: str) -> LotCalculationParams:
        """Prepare parameters for lot calculation"""
        try:
            # Account information
            account_balance = self.account_info.get("balance", 10000)
            account_equity = self.account_info.get("equity", account_balance)
            free_margin = self.account_info.get("free_margin", account_balance * 0.8)
            
            # Market data
            if market_data is None:
                market_data = {}
            
            volatility_factor = market_data.get("volatility_factor", 1.0)
            market_condition = market_data.get("condition", "RANGING")
            
            # Calculate existing exposure
            existing_exposure = self._calculate_existing_exposure()
            
            # Symbol information
            symbol_info = {
                "point_value": self.point_value,
                "contract_size": self.contract_size,
                "margin_percentage": self.margin_percentage
            }
            
            return LotCalculationParams(
                account_balance=account_balance,
                account_equity=account_equity,
                free_margin=free_margin,
                base_lot_size=self.base_lot_size,
                max_risk_percentage=self.max_risk_percentage,
                confidence_level=confidence,
                volatility_factor=volatility_factor,
                market_condition=str(market_condition),
                existing_exposure=existing_exposure,
                trade_direction=order_type,
                symbol_info=symbol_info
            )
            
        except Exception as e:
            print(f"❌ Parameter preparation error: {e}")
            # Return safe defaults
            return LotCalculationParams(
                account_balance=10000,
                account_equity=10000,
                free_margin=8000,
                base_lot_size=self.base_lot_size,
                max_risk_percentage=1.0,
                confidence_level=0.5,
                volatility_factor=1.0,
                market_condition="RANGING",
                existing_exposure=0.0,
                trade_direction=order_type,
                symbol_info={"point_value": 0.01, "contract_size": 100, "margin_percentage": 1.0}
            )
    
    def _calculate_hybrid_lot_size(self, params: LotCalculationParams, reasoning: str) -> LotCalculationResult:
        """Calculate lot size using hybrid approach"""
        try:
            # Calculate each component
            risk_component = self._get_risk_component(params)
            confidence_component = self._get_confidence_component(params)
            volatility_component = self._get_volatility_component(params)
            condition_component = self._get_condition_component(params)
            fixed_component = params.base_lot_size
            
            # Weighted combination
            weighted_lot = (
                risk_component * self.method_weights[LotCalculationMethod.PERCENTAGE_RISK] +
                confidence_component * self.method_weights[LotCalculationMethod.CONFIDENCE_BASED] +
                volatility_component * self.method_weights[LotCalculationMethod.VOLATILITY_ADJUSTED] +
                condition_component * self.method_weights[LotCalculationMethod.MARKET_CONDITION] +
                fixed_component * self.method_weights[LotCalculationMethod.FIXED]
            )
            
            # Performance-based adjustment
            if len(self.lot_performance_history) > 10:
                performance_adjustment = self._get_performance_adjustment()
                weighted_lot *= performance_adjustment
            
            # Calculate risk metrics
            risk_amount = self._calculate_risk_amount(weighted_lot, params)
            risk_percentage = (risk_amount / params.account_balance) * 100
            margin_required = self._calculate_margin_required(weighted_lot, params)
            
            # Generate warnings
            warnings = self._generate_warnings(weighted_lot, params, risk_amount, margin_required)
            
            reasoning_text = (f"Hybrid: Risk({risk_component:.3f}) + "
                            f"Conf({confidence_component:.3f}) + "
                            f"Vol({volatility_component:.3f}) + "
                            f"Cond({condition_component:.3f}) + "
                            f"Fixed({fixed_component:.3f}) = {weighted_lot:.3f}")
            
            return LotCalculationResult(
                lot_size=weighted_lot,
                calculation_method=LotCalculationMethod.DYNAMIC_HYBRID,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=margin_required,
                confidence_factor=params.confidence_level,
                volatility_adjustment=params.volatility_factor,
                reasoning=reasoning_text,
                warnings=warnings,
                calculation_factors={
                    "risk_component": risk_component,
                    "confidence_component": confidence_component,
                    "volatility_component": volatility_component,
                    "condition_component": condition_component,
                    "fixed_component": fixed_component
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Hybrid lot calculation error: {e}")
            return self._get_fallback_lot_result(params)
    
    def _calculate_percentage_risk_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """Calculate lot size based on percentage risk"""
        try:
            # Risk amount based on percentage
            max_risk_amount = params.account_balance * (params.max_risk_percentage / 100)
            
            # Adjust risk based on confidence
            confidence_adjusted_risk = max_risk_amount * params.confidence_level
            
            # Calculate lot size based on risk (simplified)
            # Assume risk per lot = account_balance * 0.001 (0.1%)
            risk_per_lot = params.account_balance * 0.001
            lot_size = confidence_adjusted_risk / risk_per_lot if risk_per_lot > 0 else params.base_lot_size
            
            risk_amount = confidence_adjusted_risk
            risk_percentage = (risk_amount / params.account_balance) * 100
            margin_required = self._calculate_margin_required(lot_size, params)
            
            warnings = self._generate_warnings(lot_size, params, risk_amount, margin_required)
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.PERCENTAGE_RISK,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=margin_required,
                confidence_factor=params.confidence_level,
                volatility_adjustment=1.0,
                reasoning=f"Risk-based: {params.max_risk_percentage}% * {params.confidence_level:.2f} confidence = {lot_size:.3f} lots",
                warnings=warnings,
                calculation_factors={
                    "max_risk_amount": max_risk_amount,
                    "confidence_adjusted_risk": confidence_adjusted_risk,
                    "risk_per_lot": risk_per_lot
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Percentage risk calculation error: {e}")
            return self._get_fallback_lot_result(params)
    
    def _calculate_confidence_based_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """Calculate lot size based on confidence level"""
        try:
            # Base lot adjusted by confidence
            confidence_multiplier = 0.5 + (params.confidence_level * 1.5)  # 0.5 to 2.0 range
            lot_size = params.base_lot_size * confidence_multiplier
            
            risk_amount = self._calculate_risk_amount(lot_size, params)
            risk_percentage = (risk_amount / params.account_balance) * 100
            margin_required = self._calculate_margin_required(lot_size, params)
            
            warnings = self._generate_warnings(lot_size, params, risk_amount, margin_required)
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.CONFIDENCE_BASED,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=margin_required,
                confidence_factor=params.confidence_level,
                volatility_adjustment=1.0,
                reasoning=f"Confidence-based: {params.base_lot_size:.3f} * {confidence_multiplier:.2f} = {lot_size:.3f} lots",
                warnings=warnings,
                calculation_factors={
                    "confidence_multiplier": confidence_multiplier
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Confidence-based calculation error: {e}")
            return self._get_fallback_lot_result(params)
    
    def _calculate_volatility_adjusted_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """Calculate lot size adjusted for volatility"""
        try:
            # Inverse volatility adjustment (higher volatility = smaller lots)
            if params.volatility_factor > 2.0:
                volatility_multiplier = 0.5
            elif params.volatility_factor > 1.5:
                volatility_multiplier = 0.7
            elif params.volatility_factor > 0.5:
                volatility_multiplier = 1.0 / params.volatility_factor
            else:
                volatility_multiplier = 1.5  # Low volatility allows larger lots
            
            lot_size = params.base_lot_size * volatility_multiplier
            
            risk_amount = self._calculate_risk_amount(lot_size, params)
            risk_percentage = (risk_amount / params.account_balance) * 100
            margin_required = self._calculate_margin_required(lot_size, params)
            
            warnings = self._generate_warnings(lot_size, params, risk_amount, margin_required)
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.VOLATILITY_ADJUSTED,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=margin_required,
                confidence_factor=params.confidence_level,
                volatility_adjustment=params.volatility_factor,
                reasoning=f"Volatility-adjusted: {params.base_lot_size:.3f} / {params.volatility_factor:.2f} = {lot_size:.3f} lots",
                warnings=warnings,
                calculation_factors={
                    "volatility_multiplier": volatility_multiplier
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Volatility adjustment calculation error: {e}")
            return self._get_fallback_lot_result(params)
    
    def _calculate_kelly_criterion_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """Calculate lot size using Kelly Criterion"""
        try:
            # Kelly formula: f = (bp - q) / b
            # Where: b = odds, p = win probability, q = loss probability
            
            if len(self.lot_performance_history) < 10:
                # Not enough data, use confidence as proxy
                win_probability = 0.5 + (params.confidence_level - 0.5) * 0.4
            else:
                # Calculate from historical data
                recent_results = list(self.lot_performance_history)[-20:]
                wins = sum(1 for result in recent_results if result.get("success", False))
                win_probability = wins / len(recent_results)
            
            loss_probability = 1 - win_probability
            
            # Simplified odds calculation (assume 1:1 risk/reward)
            odds = 1.0
            
            # Kelly percentage
            if odds > 0 and loss_probability > 0:
                kelly_percentage = (odds * win_probability - loss_probability) / odds
            else:
                kelly_percentage = 0.1  # Conservative fallback
            
            # Apply Kelly percentage to account balance
            kelly_percentage = max(0.01, min(0.25, kelly_percentage))  # Bound between 1% and 25%
            
            # Convert to lot size
            risk_amount = params.account_balance * kelly_percentage
            risk_per_lot = params.account_balance * 0.001  # Simplified
            lot_size = risk_amount / risk_per_lot if risk_per_lot > 0 else params.base_lot_size
            
            risk_percentage = kelly_percentage * 100
            margin_required = self._calculate_margin_required(lot_size, params)
            
            warnings = self._generate_warnings(lot_size, params, risk_amount, margin_required)
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.KELLY_CRITERION,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=margin_required,
                confidence_factor=win_probability,
                volatility_adjustment=1.0,
                reasoning=f"Kelly Criterion: {win_probability:.1%} win rate, {kelly_percentage:.1%} allocation = {lot_size:.3f} lots",
                warnings=warnings,
                calculation_factors={
                    "win_probability": win_probability,
                    "kelly_percentage": kelly_percentage,
                    "odds": odds
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Kelly criterion calculation error: {e}")
            return self._get_fallback_lot_result(params)
    
    def _calculate_progressive_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """Calculate lot size using progressive sizing"""
        try:
            # Count recent losses for progression
            recent_losses = 0
            if len(self.lot_performance_history) > 0:
                for result in list(self.lot_performance_history)[-5:]:
                    if not result.get("success", True):
                        recent_losses += 1
                    else:
                        break  # Stop at first win
            
            # Progressive multiplier
            progressive_multiplier = min(
                self.max_progressive_multiplier,
                self.progressive_factor ** recent_losses
            )
            
            lot_size = params.base_lot_size * progressive_multiplier
            
            risk_amount = self._calculate_risk_amount(lot_size, params)
            risk_percentage = (risk_amount / params.account_balance) * 100
            margin_required = self._calculate_margin_required(lot_size, params)
            
            warnings = self._generate_warnings(lot_size, params, risk_amount, margin_required)
            
            if recent_losses > 0:
                warnings.append(f"Progressive sizing active after {recent_losses} losses")
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.PROGRESSIVE_SIZING,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=margin_required,
                confidence_factor=params.confidence_level,
                volatility_adjustment=1.0,
                reasoning=f"Progressive: {params.base_lot_size:.3f} * {progressive_multiplier:.2f} (after {recent_losses} losses) = {lot_size:.3f} lots",
                warnings=warnings,
                calculation_factors={
                    "recent_losses": recent_losses,
                    "progressive_multiplier": progressive_multiplier
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Progressive sizing calculation error: {e}")
            return self._get_fallback_lot_result(params)
    
    def _calculate_fixed_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """Calculate fixed lot size"""
        lot_size = params.base_lot_size
        risk_amount = self._calculate_risk_amount(lot_size, params)
        risk_percentage = (risk_amount / params.account_balance) * 100
        margin_required = self._calculate_margin_required(lot_size, params)
        
        warnings = self._generate_warnings(lot_size, params, risk_amount, margin_required)
        
        return LotCalculationResult(
            lot_size=lot_size,
            calculation_method=LotCalculationMethod.FIXED,
            risk_amount=risk_amount,
            risk_percentage=risk_percentage,
            margin_required=margin_required,
            confidence_factor=params.confidence_level,
            volatility_adjustment=1.0,
            reasoning=f"Fixed lot size: {lot_size:.3f}",
            warnings=warnings,
            calculation_factors={},
            timestamp=datetime.now()
        )
    
    def _get_risk_component(self, params: LotCalculationParams) -> float:
        """Get risk-based component for hybrid calculation"""
        # ใช้ base lot แทนการคำนวณซับซ้อน
        return params.base_lot_size
    
    def _get_confidence_component(self, params: LotCalculationParams) -> float:
        """Get confidence-based component for hybrid calculation"""
        # จำกัดการปรับตาม confidence
        confidence_multiplier = 0.8 + (params.confidence_level * 0.4)  # 0.8-1.2 range
        result = params.base_lot_size * confidence_multiplier
        
        # ใส่ bounds เข้มงวด
        return max(params.base_lot_size * 0.5, min(params.base_lot_size * 2.0, result))
    
    def _get_volatility_component(self, params: LotCalculationParams) -> float:
        """Get volatility-adjusted component for hybrid calculation"""
        # เรียบง่ายขึ้น
        if params.volatility_factor > 1.5:
            return params.base_lot_size * 0.8
        elif params.volatility_factor < 0.7:
            return params.base_lot_size * 1.1
        else:
            return params.base_lot_size
    
    def _get_condition_component(self, params: LotCalculationParams) -> float:
        """Get market condition component for hybrid calculation"""
        # ง่ายๆ ไม่ซับซ้อน
        condition_multipliers = {
            "TRENDING_UP": 1.0,
            "TRENDING_DOWN": 1.0,
            "RANGING": 0.9,
            "HIGH_VOLATILITY": 0.8,
            "LOW_VOLATILITY": 1.0,
            "BREAKOUT": 0.9
        }
        
        multiplier = condition_multipliers.get(params.market_condition, 1.0)
        return params.base_lot_size * multiplier
    
    def _get_performance_adjustment(self) -> float:
        """Get performance-based adjustment factor"""
        try:
            recent_performance = list(self.lot_performance_history)[-10:]
            if len(recent_performance) < 5:
                return 1.0
            
            success_rate = sum(1 for p in recent_performance if p.get("success", False)) / len(recent_performance)
            avg_profit = statistics.mean([p.get("profit", 0) for p in recent_performance])
            
            # Adjust based on performance
            if success_rate > 0.7 and avg_profit > 0:
                return 1.1  # Increase lot size
            elif success_rate < 0.4 or avg_profit < -50:
                return 0.8  # Decrease lot size
            else:
                return 1.0  # No adjustment
                
        except Exception as e:
            print(f"❌ Performance adjustment error: {e}")
            return 1.0
    
    def _calculate_risk_amount(self, lot_size: float, params: LotCalculationParams) -> float:
        """Calculate risk amount for given lot size"""
        # Simplified risk calculation (can be enhanced with actual SL distance)
        return lot_size * params.account_balance * 0.001
    
    def _calculate_margin_required(self, lot_size: float, params: LotCalculationParams) -> float:
        """Calculate margin required for given lot size"""
        try:
            # Simplified margin calculation
            contract_size = params.symbol_info.get("contract_size", 100)
            margin_percentage = params.symbol_info.get("margin_percentage", 1.0)
            
            # Assume current price around 2000 for gold
            estimated_price = 2000.0
            margin_required = (lot_size * contract_size * estimated_price * margin_percentage) / 100
            
            return margin_required
            
        except Exception as e:
            print(f"❌ Margin calculation error: {e}")
            return lot_size * 1000  # Fallback estimate
    
    def _calculate_existing_exposure(self) -> float:
        """Calculate existing position exposure"""
        # Placeholder - would integrate with position manager
        return 0.0
    
    def _generate_warnings(self, lot_size: float, params: LotCalculationParams,
                         risk_amount: float, margin_required: float) -> List[str]:
        """Generate warnings for lot calculation"""
        warnings = []
        
        # Risk warnings
        risk_percentage = (risk_amount / params.account_balance) * 100
        if risk_percentage > params.max_risk_percentage:
            warnings.append(f"Risk {risk_percentage:.1f}% exceeds maximum {params.max_risk_percentage}%")
        
        # Margin warnings
        margin_percentage = (margin_required / params.free_margin) * 100
        if margin_percentage > 50:
            warnings.append(f"High margin usage: {margin_percentage:.1f}%")
        
        # Lot size warnings
        if lot_size > self.max_lot_size:
            warnings.append(f"Lot size {lot_size:.3f} exceeds maximum {self.max_lot_size}")
        elif lot_size < self.min_lot_size:
            warnings.append(f"Lot size {lot_size:.3f} below minimum {self.min_lot_size}")
        
        # Confidence warnings
        if params.confidence_level < 0.3:
            warnings.append("Low confidence level - consider reducing position size")
        
        # Volatility warnings
        if params.volatility_factor > 2.0:
            warnings.append("High volatility detected - position size adjusted")
        
        return warnings
    
    def _validate_and_bound_lot_size(self, lot_size: float) -> float:
        """Validate and apply bounds to lot size"""
        try:
            # เข้มงวดมากขึ้น
            bounded_lot = max(self.min_lot_size, min(self.max_lot_size, lot_size))
            
            # ปัดเศษ
            lot_step = 0.01
            bounded_lot = round(bounded_lot / lot_step) * lot_step
            
            # ห้ามเกิน max_lot_size
            bounded_lot = min(bounded_lot, self.max_lot_size)
            
            # ห้ามต่ำกว่า min_lot_size
            bounded_lot = max(bounded_lot, self.min_lot_size)
            
            return bounded_lot
            
        except Exception as e:
            print(f"❌ Lot validation error: {e}")
            return self.base_lot_size
    
    def _get_fallback_lot_result(self, params: LotCalculationParams) -> LotCalculationResult:
        """Get fallback lot result on error"""
        lot_size = params.base_lot_size
        risk_amount = self._calculate_risk_amount(lot_size, params)
        risk_percentage = (risk_amount / params.account_balance) * 100
        
        return LotCalculationResult(
            lot_size=lot_size,
            calculation_method=LotCalculationMethod.FIXED,
            risk_amount=risk_amount,
            risk_percentage=risk_percentage,
            margin_required=lot_size * 1000,
            confidence_factor=params.confidence_level,
            volatility_adjustment=1.0,
            reasoning="Fallback to base lot size due to calculation error",
            warnings=["Calculation error - using fallback"],
            calculation_factors={"fallback": True},
            timestamp=datetime.now()
        )
    
    # === Performance Tracking Methods ===
    
    def update_lot_performance(self, lot_size: float, success: bool, profit: float = 0.0,
                             calculation_method: str = ""):
        """Update lot performance feedback"""
        try:
            performance_data = {
                "lot_size": lot_size,
                "success": success,
                "profit": profit,
                "method": calculation_method,
                "timestamp": datetime.now()
            }
            
            self.lot_performance_history.append(performance_data)
            
            print(f"🔢 Lot performance updated: {lot_size:.3f} lots, "
                  f"Success: {success}, Profit: ${profit:.2f}")
            
            # Adaptive learning
            if len(self.lot_performance_history) >= self.performance_window:
                self._adaptive_method_adjustment()
                
        except Exception as e:
            print(f"❌ Lot performance update error: {e}")
    
    def _adaptive_method_adjustment(self):
        """Adjust method weights based on performance"""
        try:
            recent_performance = list(self.lot_performance_history)[-self.performance_window:]
            
            # Calculate performance by method
            method_performance = {}
            for perf in recent_performance:
                method = perf.get("method", "UNKNOWN")
                if method not in method_performance:
                    method_performance[method] = {"successes": 0, "total": 0, "profit": 0}
                
                method_performance[method]["total"] += 1
                if perf.get("success", False):
                    method_performance[method]["successes"] += 1
                method_performance[method]["profit"] += perf.get("profit", 0)
            
            # Adjust weights based on performance
            total_adjustment = 0
            for method_name, method_enum in [
                ("PERCENTAGE_RISK", LotCalculationMethod.PERCENTAGE_RISK),
                ("CONFIDENCE_BASED", LotCalculationMethod.CONFIDENCE_BASED),
                ("VOLATILITY_ADJUSTED", LotCalculationMethod.VOLATILITY_ADJUSTED),
                ("MARKET_CONDITION", LotCalculationMethod.MARKET_CONDITION)
            ]:
                if method_name in method_performance:
                    perf_data = method_performance[method_name]
                    if perf_data["total"] >= 3:  # Minimum sample size
                        success_rate = perf_data["successes"] / perf_data["total"]
                        avg_profit = perf_data["profit"] / perf_data["total"]
                        
                        # Calculate adjustment
                        performance_score = success_rate * 0.7 + (avg_profit / 100) * 0.3
                        if performance_score > 0.6:
                            adjustment = self.learning_rate * 0.1
                            self.method_weights[method_enum] += adjustment
                            total_adjustment += adjustment
                        elif performance_score < 0.3:
                            adjustment = self.learning_rate * 0.05
                            self.method_weights[method_enum] -= adjustment
                            total_adjustment -= adjustment
            
            # Normalize weights
            if total_adjustment != 0:
                total_weight = sum(self.method_weights.values())
                if total_weight > 0:
                    for method in self.method_weights:
                        self.method_weights[method] /= total_weight
                        self.method_weights[method] = max(0.05, self.method_weights[method])
                
                print("🔢 Method weights adjusted based on performance")
                
        except Exception as e:
            print(f"❌ Method adjustment error: {e}")
    
    # === Public Interface Methods ===
    
    def get_lot_statistics(self) -> Dict[str, Any]:
        """Get lot calculation statistics"""
        try:
            if not self.calculation_history:
                return {"error": "No calculation history available"}
            
            recent_calculations = list(self.calculation_history)[-20:]
            recent_lots = [calc.lot_size for calc in recent_calculations]
            recent_risks = [calc.risk_percentage for calc in recent_calculations]
            
            performance_data = list(self.lot_performance_history)[-20:] if self.lot_performance_history else []
            
            return {
                "base_lot_size": self.base_lot_size,
                "current_method": self.current_method.value,
                "method_weights": {k.value: v for k, v in self.method_weights.items()},
                "recent_avg_lot": round(statistics.mean(recent_lots), 4),
                "recent_lot_range": f"{min(recent_lots):.3f}-{max(recent_lots):.3f}",
                "recent_avg_risk": round(statistics.mean(recent_risks), 2),
                "performance_records": len(performance_data),
                "success_rate": round(sum(1 for p in performance_data if p.get("success", False)) / len(performance_data), 2) if performance_data else 0.0,
                "avg_profit": round(statistics.mean([p.get("profit", 0) for p in performance_data]), 2) if performance_data else 0.0,
                "total_calculations": len(self.calculation_history)
            }
            
        except Exception as e:
            print(f"❌ Lot statistics error: {e}")
            return {"error": str(e)}
    
    def set_calculation_method(self, method: LotCalculationMethod):
        """Set lot calculation method"""
        try:
            self.current_method = method
            print(f"🔢 Lot calculation method set to: {method.value}")
        except Exception as e:
            print(f"❌ Method setting error: {e}")
    
    def update_account_info(self, account_info: Dict):
        """Update account information"""
        try:
            self.account_info = account_info
            print(f"🔢 Account info updated: Balance ${account_info.get('balance', 0):,.2f}")
        except Exception as e:
            print(f"❌ Account update error: {e}")

# Mock Lot Calculator for Testing
class MockLotCalculator:
    """Mock Lot Calculator for testing purposes"""
    
    def __init__(self):
        self.base_lot_size = 0.01
        self.current_method = LotCalculationMethod.DYNAMIC_HYBRID
        self.calculation_count = 0
        print("🧪 Mock Lot Calculator initialized for testing")
    
    def calculate_optimal_lot_size(self, market_data: Dict = None, confidence: float = 0.5,
                                 order_type: str = "BUY", reasoning: str = "") -> float:
        """Mock lot size calculation"""
        self.calculation_count += 1
        
        # Simple mock logic
        base = self.base_lot_size
        
        # Confidence adjustment
        confidence_factor = 0.5 + confidence * 1.0
        
        # Market data adjustment
        if market_data:
            volatility = market_data.get("volatility_factor", 1.0)
            if volatility > 1.5:
                base *= 0.8
            elif volatility < 0.7:
                base *= 1.2
        
        lot_size = round(base * confidence_factor, 3)
        
        print(f"🧪 Mock lot calculated: {lot_size:.3f} (confidence: {confidence:.1%})")
        return lot_size
    
    def update_lot_performance(self, lot_size: float, success: bool, profit: float = 0.0,
                             calculation_method: str = ""):
        """Mock performance update"""
        print(f"🧪 Mock performance: {lot_size:.3f} lots, success={success}, profit=${profit:.2f}")
    
    def get_lot_statistics(self) -> Dict[str, Any]:
        """Mock lot statistics"""
        return {
            "base_lot_size": self.base_lot_size,
            "current_method": self.current_method.value,
            "recent_avg_lot": 0.015,
            "success_rate": 0.72,
            "total_calculations": self.calculation_count
        }

# Test function
def test_lot_calculator():
    """Test the lot calculator"""
    print("🧪 Testing Lot Calculator...")
    
    # Mock account info
    mock_account = {
        "balance": 10000,
        "equity": 10500,
        "free_margin": 8000
    }
    
    # Mock config
    mock_config = {
        "trading": {
            "base_lot_size": 0.01,
            "max_lot_size": 1.0,
            "symbol": "XAUUSD"
        },
        "risk_management": {
            "max_risk_percentage": 2.0
        }
    }
    
    # Test with mock calculator
    mock_calculator = MockLotCalculator()
    
    # Test different scenarios
    test_scenarios = [
        {"confidence": 0.3, "volatility": 0.8, "condition": "LOW_VOLATILITY"},
        {"confidence": 0.7, "volatility": 1.2, "condition": "RANGING"},
        {"confidence": 0.9, "volatility": 2.0, "condition": "HIGH_VOLATILITY"}
    ]
    
    print("\n--- Testing Calculation Scenarios ---")
    for i, scenario in enumerate(test_scenarios):
        print(f"\nScenario {i+1}:")
        market_data = {
            "volatility_factor": scenario["volatility"],
            "condition": scenario["condition"]
        }
        
        lot_size = mock_calculator.calculate_optimal_lot_size(
            market_data=market_data,
            confidence=scenario["confidence"],
            order_type="BUY"
        )
        
        print(f"  Confidence: {scenario['confidence']:.1%}")
        print(f"  Volatility: {scenario['volatility']:.1f}x")
        print(f"  Condition: {scenario['condition']}")
        print(f"  → Lot size: {lot_size:.3f}")
    
    # Test performance tracking
    print("\n--- Testing Performance Tracking ---")
    mock_calculator.update_lot_performance(0.015, True, 25.5)
    mock_calculator.update_lot_performance(0.020, False, -12.3)
    
    # Test statistics
    print("\n--- Lot Statistics ---")
    stats = mock_calculator.get_lot_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Lot Calculator test completed")

if __name__ == "__main__":
    test_lot_calculator()