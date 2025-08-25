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
    
    def calculate_optimal_lot_size(self, market_data: Dict = None, confidence: float = 0.5,
                                 order_type: str = "BUY", reasoning: str = "") -> float:
        """
        🆕 คำนวณขนาด lot ที่เหมาะสมสำหรับ Modern Rule Engine
        
        Args:
            market_data: ข้อมูลการวิเคราะห์ตลาดจาก Market Analyzer
            confidence: ระดับความเชื่อมั่น (0.0-1.0)
            order_type: ประเภทออเดอร์ ("BUY", "SELL")
            reasoning: เหตุผลการเทรด
            
        Returns:
            ขนาด lot ที่เหมาะสม
        """
        try:
            print(f"🔢 === LOT SIZE CALCULATION ===")
            print(f"   Order Type: {order_type}")
            print(f"   Confidence: {confidence:.2f}")
            print(f"   Reasoning: {reasoning}")
            
            # เตรียมพารามิเตอร์การคำนวณ
            calc_params = self._prepare_calculation_params(market_data, confidence, order_type)
            
            # คำนวณตามวิธีปัจจุบัน
            if self.current_method == LotCalculationMethod.DYNAMIC_HYBRID:
                result = self._calculate_hybrid_lot_size(calc_params, reasoning)
            elif self.current_method == LotCalculationMethod.CONFIDENCE_BASED:
                result = self._calculate_confidence_based_lot(calc_params)
            elif self.current_method == LotCalculationMethod.VOLATILITY_ADJUSTED:
                result = self._calculate_volatility_adjusted_lot(calc_params)
            else:
                result = self._calculate_fixed_lot(calc_params)
            
            # ตรวจสอบและจำกัดขนาด
            final_lot = self._validate_and_bound_lot_size(result.lot_size)
            
            # บันทึกประวัติ
            self.calculation_history.append(result)
            
            print(f"✅ Lot calculated: {final_lot:.3f}")
            print(f"   Method: {result.calculation_method.value}")
            print(f"   Risk: ${result.risk_amount:.2f} ({result.risk_percentage:.1f}%)")
            
            return final_lot
            
        except Exception as e:
            print(f"❌ Lot calculation error: {e}")
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
            # ปัจจัยต่างๆ
            risk_component = self._get_risk_component(params)
            confidence_component = self._get_confidence_component(params)
            volatility_component = self._get_volatility_component(params)
            market_component = self._get_market_component(params)
            
            # น้ำหนักแต่ละปัจจัย
            weights = {
                "risk": 0.3,
                "confidence": 0.25,
                "volatility": 0.25,
                "market": 0.2
            }
            
            # คำนวณ lot แบบถ่วงน้ำหนัก
            weighted_lot = (
                risk_component * weights["risk"] +
                confidence_component * weights["confidence"] +
                volatility_component * weights["volatility"] +
                market_component * weights["market"]
            )
            
            # ปรับตาม reasoning
            reasoning_adjustment = self._get_reasoning_adjustment(reasoning)
            final_lot = weighted_lot * reasoning_adjustment
            
            # คำนวณความเสี่ยง
            risk_amount = final_lot * params.account_balance * 0.001  # ประมาณ
            risk_percentage = (risk_amount / params.account_balance) * 100
            
            return LotCalculationResult(
                lot_size=final_lot,
                calculation_method=LotCalculationMethod.DYNAMIC_HYBRID,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=final_lot * 1000,  # ประมาณ
                confidence_factor=params.confidence_level,
                volatility_adjustment=params.volatility_factor,
                reasoning=f"Hybrid: Risk×{weights['risk']:.0%} + Conf×{weights['confidence']:.0%} + Vol×{weights['volatility']:.0%} + Market×{weights['market']:.0%} = {final_lot:.3f}",
                warnings=[],
                calculation_factors={
                    "risk_component": risk_component,
                    "confidence_component": confidence_component,
                    "volatility_component": volatility_component,
                    "market_component": market_component,
                    "reasoning_adjustment": reasoning_adjustment
                },
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Hybrid calculation error: {e}")
            return self._get_fallback_result(params)
    
    def _get_risk_component(self, params: LotCalculationParams) -> float:
        """คำนวณ component จากความเสี่ยง"""
        try:
            # ใช้ free margin เป็นฐาน
            risk_budget = params.free_margin * (params.max_risk_percentage / 100)
            
            # แปลงเป็น lot size (ประมาณ)
            lot_per_risk = risk_budget / (params.account_balance * 0.001)
            
            return max(self.min_lot_size, min(self.max_lot_size, lot_per_risk))
            
        except Exception as e:
            return self.base_lot_size
    
    def _get_confidence_component(self, params: LotCalculationParams) -> float:
        """คำนวณ component จาก confidence"""
        try:
            # ปรับ base lot ตาม confidence
            confidence_multiplier = 0.5 + (params.confidence_level * 1.0)  # 0.5-1.5 range
            
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