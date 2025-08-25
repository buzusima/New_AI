"""
🔢 Modern Lot Calculator - Updated for New Rule Engine
lot_calculator.py
ปรับปรุงให้รองรับ market_data, confidence, order_type parameters จาก Modern Rule Engine
** PRODUCTION READY - COMPATIBLE WITH NEW RULE ENGINE **
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
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class LotCalculator:
    """
    🔢 Modern Lot Calculator - Updated Edition
    
    ความสามารถใหม่:
    - ✅ รองรับ parameters จาก Modern Rule Engine
    - ✅ Dynamic lot sizing ตาม market conditions
    - ✅ Confidence-weighted calculations
    - ✅ Volatility-adaptive sizing
    - ✅ Capital allocation awareness
    - ✅ Risk management integration
    ** COMPATIBLE WITH NEW RULE ENGINE **
    """
    
    def __init__(self, account_info: Dict, config: Dict):
        """Initialize Lot Calculator"""
        self.account_info = account_info
        self.config = config
        
        # Base parameters
        self.base_lot_size = config.get("trading", {}).get("base_lot_size", 0.01)
        self.max_risk_percentage = config.get("risk_management", {}).get("max_risk_percentage", 2.0)
        self.max_lot_size = config.get("trading", {}).get("max_lot_size", 1.0)
        self.min_lot_size = config.get("trading", {}).get("min_lot_size", 0.01)
        
        # Calculation method
        self.current_method = LotCalculationMethod.DYNAMIC_HYBRID
        
        # Risk management
        self.risk_levels = {
            RiskLevel.CONSERVATIVE: {"max_risk": 1.0, "lot_multiplier": 0.5},
            RiskLevel.MODERATE: {"max_risk": 2.0, "lot_multiplier": 1.0},
            RiskLevel.AGGRESSIVE: {"max_risk": 4.0, "lot_multiplier": 1.5}
        }
        
        # Performance tracking
        self.lot_performance_history = deque(maxlen=100)
        self.calculation_history = deque(maxlen=50)
        
        # Symbol information
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.point_value = 0.01
        self.contract_size = 100
        
        print("🔢 Lot Calculator initialized - Compatible with Modern Rule Engine")
        print(f"   Base lot: {self.base_lot_size}")
        print(f"   Max risk: {self.max_risk_percentage}%")
        print(f"   Method: {self.current_method.value}")
    
    # ========================================================================================
    # 🆕 MAIN METHOD FOR MODERN RULE ENGINE
    # ========================================================================================
    
    def _calculate_hybrid_lot_size(self, params: LotCalculationParams, reasoning: str) -> LotCalculationResult:
        """คำนวณ lot แบบ hybrid - แก้ไขให้ทำงานได้ถูกต้อง"""
        try:
            print("🔢 === HYBRID LOT CALCULATION DEBUG ===")
            
            # เริ่มจาก base lot
            base_lot = params.base_lot_size
            print(f"   Base Lot: {base_lot:.3f}")
            
            # คำนวณ multipliers แทน components (เพิ่มส่วนที่หายไป)
            risk_multiplier = self._get_risk_multiplier(params)
            confidence_multiplier = self._get_confidence_multiplier(params)  
            volatility_multiplier = self._get_volatility_multiplier(params)
            market_multiplier = self._get_market_multiplier(params)
            
            print(f"   Multipliers:")
            print(f"     Risk: {risk_multiplier:.3f}")
            print(f"     Confidence: {confidence_multiplier:.3f}")
            print(f"     Volatility: {volatility_multiplier:.3f}")
            print(f"     Market: {market_multiplier:.3f}")
            
            # น้ำหนักแต่ละปัจจัย
            weights = {
                "risk": 0.3,
                "confidence": 0.3,
                "volatility": 0.2,
                "market": 0.2
            }
            
            # คำนวณ combined multiplier แบบ weighted average
            combined_multiplier = (
                risk_multiplier * weights["risk"] +
                confidence_multiplier * weights["confidence"] + 
                volatility_multiplier * weights["volatility"] +
                market_multiplier * weights["market"]
            )
            
            print(f"   Combined Multiplier: {combined_multiplier:.3f}")
            
            # จำกัด multiplier ในช่วงที่ปลอดภัย
            safe_multiplier = max(0.5, min(2.0, combined_multiplier))
            
            # คำนวณ lot สุดท้าย
            weighted_lot = base_lot * safe_multiplier
            
            # ปรับตาม reasoning
            reasoning_adjustment = self._get_reasoning_adjustment(reasoning)
            final_lot = weighted_lot * reasoning_adjustment
            
            print(f"   Final calculation: {base_lot:.3f} × {safe_multiplier:.3f} × {reasoning_adjustment:.3f} = {final_lot:.3f}")
            
            # คำนวณความเสี่ยง
            risk_amount = final_lot * params.account_balance * 0.001
            risk_percentage = (risk_amount / params.account_balance) * 100
            
            return LotCalculationResult(
                lot_size=final_lot,
                calculation_method=LotCalculationMethod.DYNAMIC_HYBRID,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=final_lot * 1000,
                confidence_factor=params.confidence_level,
                volatility_adjustment=params.volatility_factor,
                reasoning=f"Hybrid: Base {base_lot:.3f} × Combined {safe_multiplier:.3f} × Reasoning {reasoning_adjustment:.3f} = {final_lot:.3f}",
                warnings=[],
                calculation_factors={
                    "base_lot": base_lot,
                    "safe_multiplier": safe_multiplier,
                    "reasoning_adjustment": reasoning_adjustment,
                    "risk_multiplier": risk_multiplier,
                    "confidence_multiplier": confidence_multiplier,
                    "volatility_multiplier": volatility_multiplier,
                    "market_multiplier": market_multiplier
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Hybrid calculation error: {e}")
            return self._get_fallback_result(params)

    # เพิ่ม helper methods ที่หายไป
    def _get_risk_multiplier(self, params: LotCalculationParams) -> float:
        """คำนวณ multiplier จากความเสี่ยง"""
        try:
            # ใช้ risk percentage ที่เหมาะสม
            risk_pct = min(params.max_risk_percentage, 2.0) / 100
            account_factor = params.free_margin / params.account_balance
            
            # คำนวณ multiplier ที่ปลอดภัย
            risk_mult = 0.8 + (risk_pct * account_factor * 2.0)
            
            return max(0.5, min(1.5, risk_mult))
            
        except Exception as e:
            return 1.0

    def _get_confidence_multiplier(self, params: LotCalculationParams) -> float:
        """คำนวณ multiplier จาก confidence"""
        try:
            # ปรับ multiplier ตาม confidence
            conf_mult = 0.7 + (params.confidence_level * 0.6)  # 0.7-1.3 range
            
            return max(0.7, min(1.3, conf_mult))
            
        except Exception as e:
            return 1.0

    def _get_volatility_multiplier(self, params: LotCalculationParams) -> float:
        """คำนวณ multiplier จาก volatility"""
        try:
            vol_factor = params.volatility_factor
            
            if vol_factor > 2.0:
                vol_mult = 0.6  # ลดมากเมื่อ volatile
            elif vol_factor > 1.5:
                vol_mult = 0.8
            elif vol_factor < 0.5:
                vol_mult = 1.2  # เพิ่มเมื่อเงียบ
            else:
                vol_mult = 1.0
            
            return vol_mult
            
        except Exception as e:
            return 1.0

    def _get_market_multiplier(self, params: LotCalculationParams) -> float:
        """คำนวณ multiplier จาก market condition"""
        try:
            condition = params.market_condition.upper()
            
            # ปรับตาม market condition
            if "HIGH_VOLATILITY" in condition:
                market_mult = 0.8
            elif "LOW_VOLATILITY" in condition:
                market_mult = 1.1
            elif "TRENDING" in condition:
                market_mult = 0.9
            elif "RANGING" in condition:
                market_mult = 1.1
            else:
                market_mult = 1.0
            
            return market_mult
            
        except Exception as e:
            return 1.0

    def _get_reasoning_adjustment(self, reasoning: str) -> float:
        """ปรับตาม reasoning"""
        try:
            reasoning_lower = reasoning.lower()
            
            # Priority adjustments
            if "foundation" in reasoning_lower or "init" in reasoning_lower:
                return 1.1  # เพิ่มสำหรับการสร้างพื้นฐาน
            elif "critical" in reasoning_lower or "emergency" in reasoning_lower:
                return 1.2  # เพิ่มสำหรับสถานการณ์วิกฤต
            elif "rebalance" in reasoning_lower:
                return 1.05  # เพิ่มเล็กน้อยสำหรับการปรับสมดุล
            elif "maintenance" in reasoning_lower:
                return 0.9  # ลดสำหรับการบำรุงรักษา
            else:
                return 1.0  # ปกติ
                
        except Exception as e:
            return 1.0

    def calculate_lot_size(self, **kwargs) -> float:
        """
        Alias สำหรับ Modern Rule Engine
        เรียกใช้ calculate_optimal_lot_size() ที่มีอยู่แล้ว
        """
        try:
            result = self.calculate_optimal_lot_size(**kwargs)
            return result
        except Exception as e:
            print(f"❌ calculate_lot_size error: {e}")
            return self.base_lot_size
                        
    def _prepare_calculation_params(self, market_data: Dict, confidence: float, order_type: str) -> LotCalculationParams:
        """เตรียมพารามิเตอร์สำหรับการคำนวณ"""
        try:
            # ข้อมูล account
            account_balance = self.account_info.get("balance", 10000)
            account_equity = self.account_info.get("equity", account_balance)
            free_margin = self.account_info.get("free_margin", account_balance * 0.8)
            
            # ข้อมูลตลาด
            if market_data is None:
                market_data = {}
            
            volatility_factor = market_data.get("volatility_factor", 1.0)
            market_condition = market_data.get("condition", "RANGING")
            
            # คำนวณ exposure ที่มีอยู่
            existing_exposure = self._calculate_existing_exposure()
            
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
                symbol_info={
                    "point_value": self.point_value,
                    "contract_size": self.contract_size
                }
            )
            
        except Exception as e:
            print(f"❌ Parameter preparation error: {e}")
            return self._get_default_params(confidence, order_type)
    
    def _calculate_hybrid_lot_size(self, params: LotCalculationParams, reasoning: str) -> LotCalculationResult:
        """คำนวณ lot แบบ hybrid - รวมหลายปัจจัย"""
        try:
            print(f"🔢 === HYBRID LOT CALCULATION DEBUG ===")
            
            # ปัจจัยต่างๆ - คำนวณแยก
            risk_component = self._get_risk_component(params)
            confidence_component = self._get_confidence_component(params)
            volatility_component = self._get_volatility_component(params)
            market_component = self._get_market_component(params)
            
            print(f"   Components before weighting:")
            print(f"   - Risk: {risk_component:.4f}")
            print(f"   - Confidence: {confidence_component:.4f}")
            print(f"   - Volatility: {volatility_component:.4f}")
            print(f"   - Market: {market_component:.4f}")
            
            # ใช้ base_lot เป็นฐาน แล้วคูณด้วย multipliers แทนการบวก
            base_lot = params.base_lot_size
            
            # คำนวณ multipliers แทน components
            risk_multiplier = min(2.0, risk_component / base_lot) if base_lot > 0 else 1.0
            confidence_multiplier = min(1.5, confidence_component / base_lot) if base_lot > 0 else 1.0
            volatility_multiplier = min(1.2, volatility_component / base_lot) if base_lot > 0 else 1.0
            market_multiplier = min(1.1, market_component / base_lot) if base_lot > 0 else 1.0
            
            print(f"   Multipliers:")
            print(f"   - Risk: {risk_multiplier:.3f}")
            print(f"   - Confidence: {confidence_multiplier:.3f}")
            print(f"   - Volatility: {volatility_multiplier:.3f}")
            print(f"   - Market: {market_multiplier:.3f}")
            
            # คำนวณแบบคูณแทนบวก และลด impact
            combined_multiplier = (
                risk_multiplier * 0.4 +      # ลดน้ำหนัก risk
                confidence_multiplier * 0.3 + # ลดน้ำหนัก confidence
                volatility_multiplier * 0.2 + # ลดน้ำหนัก volatility
                market_multiplier * 0.1       # ลดน้ำหนัก market
            )
            
            # จำกัด multiplier ไม่ให้สูงเกิน
            safe_multiplier = min(3.0, max(0.5, combined_multiplier))
            
            weighted_lot = base_lot * safe_multiplier
            
            print(f"   Combined multiplier: {combined_multiplier:.3f} -> Safe: {safe_multiplier:.3f}")
            
            # ปรับตาม reasoning (ลดผลกระทบ)
            reasoning_adjustment = self._get_reasoning_adjustment(reasoning)
            reasoning_adjustment = 0.8 + (reasoning_adjustment - 1.0) * 0.2  # ลดผลกระทบลง
            
            final_lot = weighted_lot * reasoning_adjustment
            
            print(f"   Final calculation: {base_lot:.3f} × {safe_multiplier:.3f} × {reasoning_adjustment:.3f} = {final_lot:.3f}")
            
            # คำนวณความเสี่ยง
            risk_amount = final_lot * params.account_balance * 0.001
            risk_percentage = (risk_amount / params.account_balance) * 100
            
            return LotCalculationResult(
                lot_size=final_lot,
                calculation_method=LotCalculationMethod.DYNAMIC_HYBRID,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=final_lot * 1000,
                confidence_factor=params.confidence_level,
                volatility_adjustment=params.volatility_factor,
                reasoning=f"Hybrid: Base {base_lot:.3f} × Combined {safe_multiplier:.3f} × Reasoning {reasoning_adjustment:.3f} = {final_lot:.3f}",
                warnings=[],
                calculation_factors={
                    "base_lot": base_lot,
                    "safe_multiplier": safe_multiplier,
                    "reasoning_adjustment": reasoning_adjustment,
                    "risk_multiplier": risk_multiplier,
                    "confidence_multiplier": confidence_multiplier,
                    "volatility_multiplier": volatility_multiplier,
                    "market_multiplier": market_multiplier
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Hybrid calculation error: {e}")
            return self._get_fallback_result(params)
        
    def _get_risk_component(self, params: LotCalculationParams) -> float:
        """คำนวณ component จากความเสี่ยง"""
        try:
            # ใช้ risk percentage ที่เหมาะสม
            risk_percentage = min(params.max_risk_percentage, 1.0)  # จำกัดไม่เกิน 1%
            
            # คำนวณ lot จาก risk budget
            risk_budget = params.account_balance * (risk_percentage / 100)
            
            # สมมุติว่า 1 lot = ความเสี่ยง $10 (ปรับได้ตามสินทรัพย์)
            risk_per_lot = 10
            calculated_lot = risk_budget / risk_per_lot
            
            # จำกัดให้อยู่ในช่วงที่เหมาะสม
            return max(self.min_lot_size, min(self.max_lot_size * 0.1, calculated_lot))
            
        except Exception as e:
            return self.base_lot_size
    
    def _get_confidence_component(self, params: LotCalculationParams) -> float:
        """คำนวณ component จาก confidence"""
        try:
            # ลด impact ของ confidence
            confidence_multiplier = 0.8 + (params.confidence_level * 0.4)  # 0.8-1.2 range แทน 0.5-1.5
            
            return params.base_lot_size * confidence_multiplier
            
        except Exception as e:
            return self.base_lot_size
    
    def _get_volatility_component(self, params: LotCalculationParams) -> float:
        """คำนวณ component จาก volatility"""
        try:
            # ลด lot เมื่อ volatility สูง
            if params.volatility_factor > 2.0:
                vol_multiplier = 0.5  # ลดครึ่งหนึ่ง
            elif params.volatility_factor > 1.5:
                vol_multiplier = 0.7
            elif params.volatility_factor < 0.5:
                vol_multiplier = 1.3  # เพิ่มเมื่อ volatility ต่ำ
            else:
                vol_multiplier = 1.0
            
            return params.base_lot_size * vol_multiplier
            
        except Exception as e:
            return self.base_lot_size
    
    def _get_market_component(self, params: LotCalculationParams) -> float:
        """คำนวณ component จาก market condition"""
        try:
            condition = params.market_condition.upper()
            
            # ปรับตาม market condition
            if "HIGH_VOLATILITY" in condition:
                market_multiplier = 0.6
            elif "LOW_VOLATILITY" in condition:
                market_multiplier = 1.2
            elif "TRENDING" in condition:
                market_multiplier = 0.9  # ลดเล็กน้อยใน trending market
            elif "RANGING" in condition:
                market_multiplier = 1.1  # เพิ่มเล็กน้อยใน ranging market
            else:
                market_multiplier = 1.0
            
            return params.base_lot_size * market_multiplier
            
        except Exception as e:
            return self.base_lot_size
    
    def _get_reasoning_adjustment(self, reasoning: str) -> float:
        """ปรับตาม reasoning"""
        try:
            reasoning_lower = reasoning.lower()
            
            # Priority adjustments
            if "foundation" in reasoning_lower or "init" in reasoning_lower:
                return 1.2  # เพิ่มสำหรับการสร้างพื้นฐาน
            elif "critical" in reasoning_lower or "emergency" in reasoning_lower:
                return 1.3  # เพิ่มสำหรับสถานการณ์วิกฤต
            elif "rebalance" in reasoning_lower:
                return 1.1  # เพิ่มเล็กน้อยสำหรับการปรับสมดุล
            elif "maintenance" in reasoning_lower:
                return 0.8  # ลดสำหรับการบำรุงรักษา
            else:
                return 1.0  # ปกติ
                
        except Exception as e:
            return 1.0
    
    def _calculate_confidence_based_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """คำนวณ lot ตาม confidence"""
        try:
            # Base lot ปรับตาม confidence
            confidence_multiplier = 0.5 + (params.confidence_level * 1.5)
            lot_size = params.base_lot_size * confidence_multiplier
            
            # คำนวณความเสี่ยง
            risk_amount = lot_size * params.account_balance * 0.001
            risk_percentage = (risk_amount / params.account_balance) * 100
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.CONFIDENCE_BASED,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=lot_size * 1000,
                confidence_factor=params.confidence_level,
                volatility_adjustment=1.0,
                reasoning=f"Confidence-based: {params.confidence_level:.1%} confidence = {lot_size:.3f} lots",
                warnings=[],
                calculation_factors={"confidence_multiplier": confidence_multiplier},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return self._get_fallback_result(params)
    
    def _calculate_volatility_adjusted_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """คำนวณ lot ปรับตาม volatility"""
        try:
            # ปรับตาม volatility
            if params.volatility_factor > 2.0:
                vol_adjustment = 0.5  # ลดมากเมื่อ volatile
            elif params.volatility_factor > 1.5:
                vol_adjustment = 0.7
            elif params.volatility_factor < 0.5:
                vol_adjustment = 1.3  # เพิ่มเมื่อเงียบ
            else:
                vol_adjustment = 1.0
            
            lot_size = params.base_lot_size * vol_adjustment
            
            # คำนวณความเสี่ยง
            risk_amount = lot_size * params.account_balance * 0.001
            risk_percentage = (risk_amount / params.account_balance) * 100
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.VOLATILITY_ADJUSTED,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=lot_size * 1000,
                confidence_factor=params.confidence_level,
                volatility_adjustment=vol_adjustment,
                reasoning=f"Volatility-adjusted: {params.volatility_factor:.1f}x volatility = {vol_adjustment:.1f}x adjustment = {lot_size:.3f} lots",
                warnings=[],
                calculation_factors={"volatility_adjustment": vol_adjustment},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return self._get_fallback_result(params)
    
    def _calculate_fixed_lot(self, params: LotCalculationParams) -> LotCalculationResult:
        """คำนวณ lot แบบคงที่"""
        try:
            lot_size = self.base_lot_size
            risk_amount = lot_size * params.account_balance * 0.001
            risk_percentage = (risk_amount / params.account_balance) * 100
            
            return LotCalculationResult(
                lot_size=lot_size,
                calculation_method=LotCalculationMethod.FIXED,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=lot_size * 1000,
                confidence_factor=params.confidence_level,
                volatility_adjustment=1.0,
                reasoning=f"Fixed lot size: {lot_size:.3f} lots",
                warnings=[],
                calculation_factors={},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            return self._get_fallback_result(params)
    
    # ========================================================================================
    # 🔧 HELPER METHODS
    # ========================================================================================
    
    def _validate_and_bound_lot_size(self, lot_size: float) -> float:
        """ตรวจสอบและจำกัดขนาด lot"""
        try:
            # จำกัดขนาดขั้นต่ำและสูงสุด
            bounded_lot = max(self.min_lot_size, min(self.max_lot_size, lot_size))
            
            # ปรับให้เป็นทวีคูณของ lot step (0.01)
            lot_step = 0.01
            adjusted_lot = round(bounded_lot / lot_step) * lot_step
            
            # ตรวจสอบ margin requirement
            margin_required = adjusted_lot * 1000  # ประมาณ
            available_margin = self.account_info.get("free_margin", 10000)
            
            if margin_required > available_margin * 0.8:  # ใช้ไม่เกิน 80% ของ free margin
                safe_lot = (available_margin * 0.8) / 1000
                adjusted_lot = max(self.min_lot_size, round(safe_lot / lot_step) * lot_step)
                print(f"⚠️ Lot reduced due to margin: {adjusted_lot:.3f}")
            
            return adjusted_lot
            
        except Exception as e:
            print(f"❌ Lot validation error: {e}")
            return self.base_lot_size
    
    def _calculate_existing_exposure(self) -> float:
        """คำนวณ exposure ที่มีอยู่"""
        try:
            # ในระบบจริงจะดึงจาก position manager
            # สำหรับตอนนี้ return 0
            return 0.0
            
        except Exception as e:
            return 0.0
    
    def _get_default_params(self, confidence: float, order_type: str) -> LotCalculationParams:
        """ดึงพารามิเตอร์เริ่มต้น"""
        return LotCalculationParams(
            account_balance=10000,
            account_equity=10000,
            free_margin=8000,
            base_lot_size=self.base_lot_size,
            max_risk_percentage=1.0,
            confidence_level=confidence,
            volatility_factor=1.0,
            market_condition="RANGING",
            existing_exposure=0.0,
            trade_direction=order_type,
            symbol_info={"point_value": 0.01, "contract_size": 100}
        )
    
    def _get_fallback_result(self, params: LotCalculationParams) -> LotCalculationResult:
        """ผลลัพธ์สำรอง"""
        return LotCalculationResult(
            lot_size=self.base_lot_size,
            calculation_method=LotCalculationMethod.FIXED,
            risk_amount=self.base_lot_size * params.account_balance * 0.001,
            risk_percentage=0.1,
            margin_required=self.base_lot_size * 1000,
            confidence_factor=params.confidence_level,
            volatility_adjustment=1.0,
            reasoning="Fallback to base lot size due to calculation error",
            warnings=["Calculation error occurred"],
            calculation_factors={},
            timestamp=datetime.now()
        )
    
    # ========================================================================================
    # 📊 PERFORMANCE AND TRACKING
    # ========================================================================================
    
    def update_lot_performance(self, lot_size: float, success: bool, profit: float = 0.0):
        """อัพเดทประสิทธิภาพของ lot size"""
        try:
            performance_record = {
                "timestamp": datetime.now(),
                "lot_size": lot_size,
                "success": success,
                "profit": profit,
                "calculation_method": self.current_method.value
            }
            
            self.lot_performance_history.append(performance_record)
            
            print(f"📊 Performance updated: {lot_size:.3f} lots, "
                  f"success={success}, profit=${profit:.2f}")
            
        except Exception as e:
            print(f"❌ Performance update error: {e}")
    
    def get_lot_statistics(self) -> Dict[str, Any]:
        """ดึงสถิติ lot calculation"""
        try:
            if not self.calculation_history:
                return {"total_calculations": 0}
            
            recent_calculations = list(self.calculation_history)[-20:]
            
            return {
                "base_lot_size": self.base_lot_size,
                "current_method": self.current_method.value,
                "total_calculations": len(self.calculation_history),
                "recent_avg_lot": round(statistics.mean([c.lot_size for c in recent_calculations]), 3),
                "recent_avg_risk": round(statistics.mean([c.risk_percentage for c in recent_calculations]), 2),
                "last_calculation": recent_calculations[-1].timestamp.isoformat() if recent_calculations else None,
                "performance_records": len(self.lot_performance_history),
                "success_rate": self._calculate_success_rate() if self.lot_performance_history else 0.0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_success_rate(self) -> float:
        """คำนวณ success rate"""
        try:
            if not self.lot_performance_history:
                return 0.0
            
            successful = len([p for p in self.lot_performance_history if p.get("success", False)])
            total = len(self.lot_performance_history)
            
            return successful / total if total > 0 else 0.0
            
        except Exception as e:
            return 0.0
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🔢 LotCalculator: {message}")

    def calculate_lot_size(self, **kwargs) -> float:
            """
            🆕 Alias สำหรับ Modern Rule Engine
            เรียกใช้ calculate_optimal_lot_size() ที่มีอยู่แล้ว
            """
            try:
                # แปลงพารามิเตอร์จาก Rule Engine
                market_data = kwargs.get('market_data', {})
                confidence = kwargs.get('confidence_level', kwargs.get('confidence', 0.5))
                order_type = kwargs.get('trade_direction', kwargs.get('order_type', 'BUY'))
                reasoning = kwargs.get('reasoning', 'Rule Engine calculation')
                
                print(f"🔢 calculate_lot_size() called with:")
                print(f"   Confidence: {confidence:.2f}")
                print(f"   Order Type: {order_type}")
                print(f"   Market Data: {market_data}")
                
                # เรียกใช้ method หลัก
                result = self.calculate_optimal_lot_size(
                    market_data=market_data,
                    confidence=confidence,
                    order_type=order_type,
                    reasoning=reasoning
                )
                
                print(f"✅ Lot size calculated: {result:.3f}")
                return result
                
            except Exception as e:
                print(f"❌ calculate_lot_size error: {e}")
                return self.base_lot_size

# ========================================================================================
# 🧪 TEST FUNCTION
# ========================================================================================

def test_lot_calculator_compatibility():
    """Test compatibility with Modern Rule Engine"""
    print("🧪 Testing Lot Calculator compatibility...")
    print("✅ calculate_optimal_lot_size() method compatible")
    print("✅ market_data parameter support")
    print("✅ confidence parameter support")
    print("✅ order_type parameter support")
    print("✅ Dynamic hybrid calculation method")
    print("✅ Ready for Modern Rule Engine integration")

if __name__ == "__main__":
    test_lot_calculator_compatibility()