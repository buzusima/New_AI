"""
🔢 Lot Calculator - 4D Enhanced Portfolio Safety Edition
lot_calculator.py

🎯 ระบบคำนวณ Lot Size แบบ 4D สำหรับ AI Gold Grid Trading
- 4D-guided lot sizing จาก market analysis
- Portfolio safety integration
- Dynamic risk-based calculations
- Market order volume optimization

** COMPATIBLE WITH 4D AI RULE ENGINE - PORTFOLIO FOCUSED **
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import deque
import statistics

class LotCalculationMethod4D(Enum):
    """วิธีการคำนวณ lot size แบบ 4D"""
    FIXED_4D = "FIXED_4D"
    PORTFOLIO_SAFETY_4D = "PORTFOLIO_SAFETY_4D"          # เน้นความปลอดภัย portfolio
    FOUR_D_GUIDED = "FOUR_D_GUIDED"                      # ขับเคลื่อนด้วย 4D analysis
    RECOVERY_OPTIMIZED = "RECOVERY_OPTIMIZED"            # เหมาะสำหรับ recovery
    BALANCE_FOCUSED = "BALANCE_FOCUSED"                  # เน้นการสร้างความสมดุล
    DYNAMIC_4D_HYBRID = "DYNAMIC_4D_HYBRID"              # รวม 4D factors ทั้งหมด

class PortfolioSafetyLevel(Enum):
    """ระดับความปลอดภัย portfolio"""
    MAXIMUM_SAFETY = "MAXIMUM_SAFETY"      # ความปลอดภัยสูงสุด
    HIGH_SAFETY = "HIGH_SAFETY"            # ความปลอดภัยสูง
    MODERATE_SAFETY = "MODERATE_SAFETY"    # ความปลอดภัยปานกลาง
    BALANCED_RISK = "BALANCED_RISK"        # ความเสี่ยงสมดุล
    GROWTH_FOCUSED = "GROWTH_FOCUSED"      # เน้นการเติบโต

@dataclass
class LotCalculationParams4D:
    """พารามิเตอร์การคำนวณ lot แบบ 4D"""
    # Account information
    account_balance: float
    account_equity: float
    free_margin: float
    margin_level: float
    
    # Trading parameters
    base_lot_size: float
    max_risk_percentage: float
    current_positions_count: int
    total_exposure: float
    
    # 4D Analysis data
    four_d_score: float
    four_d_confidence: float
    trend_dimension_score: float
    volume_dimension_score: float
    session_dimension_score: float
    volatility_dimension_score: float
    
    # Market data
    market_condition_4d: str
    volatility_factor: float
    spread: float
    
    # Portfolio context
    buy_sell_ratio: float                 # อัตราส่วน BUY:SELL positions
    portfolio_health: float               # สุขภาพ portfolio (0-1)
    recovery_opportunity: bool            # มีโอกาส recovery หรือไม่
    
    # Order specifics
    order_type: str                      # BUY/SELL
    reasoning: str                       # เหตุผลการเทรด
    is_recovery_order: bool = False      # เป็นออเดอร์ recovery หรือไม่

@dataclass
class LotCalculationResult4D:
    """ผลลัพธ์การคำนวณ lot แบบ 4D"""
    lot_size: float
    calculation_method: LotCalculationMethod4D
    
    # Risk metrics
    risk_amount: float
    risk_percentage: float
    margin_required: float
    position_value: float
    
    # 4D factors
    four_d_score_impact: float
    portfolio_safety_factor: float
    recovery_adjustment: float
    balance_adjustment: float
    
    # Quality metrics
    confidence_level: float
    safety_rating: PortfolioSafetyLevel
    reasoning: str
    warnings: List[str]
    recommendations: List[str]
    
    # Calculation breakdown
    calculation_factors: Dict[str, float]
    timestamp: datetime
    
    @property
    def is_safe_size(self) -> bool:
        """เช็คว่าขนาด lot ปลอดภัยหรือไม่"""
        return self.risk_percentage <= 2.0 and self.margin_required <= self.margin_required * 0.8

class LotCalculator:
    """
    🔢 Lot Calculator - 4D Enhanced Portfolio Safety Edition
    
    ความสามารถใหม่:
    - ✅ 4D-guided lot sizing จาก comprehensive market analysis
    - ✅ Portfolio safety integration พร้อมการประเมินความเสี่ยง
    - ✅ Dynamic risk-based calculations ตาม portfolio health
    - ✅ Market order volume optimization สำหรับ immediate execution
    - ✅ Recovery-optimized lot sizing สำหรับ hedge operations
    - ✅ Balance-focused calculations เพื่อสร้างความสมดุล
    - ✅ Real-time portfolio impact assessment
    """
    
    def __init__(self, account_info: Dict, config: Dict):
        """Initialize 4D Lot Calculator"""
        self.account_info = account_info
        self.config = config
        
        # Base configuration
        self.base_lot_size = config.get("trading", {}).get("base_lot_size", 0.01)
        self.max_lot_size = config.get("trading", {}).get("max_lot_size", 0.10)
        self.min_lot_size = config.get("trading", {}).get("min_lot_size", 0.01)
        self.max_risk_percentage = config.get("risk_management", {}).get("max_risk_percentage", 2.0)
        
        # 4D Configuration
        self.four_d_config = {
            "lot_sizing_4d_enabled": True,
            "portfolio_safety_priority": 0.40,      # 40% น้ำหนักความปลอดภัย
            "four_d_score_weight": 0.30,            # 30% น้ำหนัก 4D score
            "recovery_weight": 0.20,                # 20% น้ำหนัก recovery
            "balance_weight": 0.10,                 # 10% น้ำหนัก balance
            "max_single_position_risk": 1.5,        # เปอร์เซ็นต์ความเสี่ยงสูงสุดต่อออเดอร์
            "portfolio_health_threshold": 0.6,      # เกณฑ์สุขภาพ portfolio
            "margin_safety_buffer": 0.20           # บัฟเฟอร์ความปลอดภัย margin
        }
        
        # Portfolio safety parameters
        self.portfolio_safety = {
            "max_total_exposure_pct": 15.0,         # เปอร์เซ็นต์ exposure รวมสูงสุด
            "max_positions_count": 30,              # จำนวนออเดอร์สูงสุด
            "balance_tolerance": 0.3,               # ความเบี่ยงเบนของสมดุล BUY:SELL
            "emergency_safety_mode": False,         # โหมดความปลอดภัยฉุกเฉิน
            "recovery_lot_multiplier": 1.2,         # ตัวคูณสำหรับ recovery orders
            "foundation_lot_multiplier": 1.5        # ตัวคูณสำหรับ foundation orders
        }
        
        # Current calculation method
        self.current_method = LotCalculationMethod4D.DYNAMIC_4D_HYBRID
        
        # Performance tracking
        self.calculation_history = deque(maxlen=100)
        self.performance_metrics = {
            "total_calculations": 0,
            "average_lot_size": 0.0,
            "average_risk_percentage": 0.0,
            "safety_violations": 0,
            "portfolio_impact_positive": 0,
            "four_d_score_correlation": 0.0
        }
        
        # Symbol information
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.point_value = self._get_symbol_point_value()
        self.contract_size = self._get_symbol_contract_size()
        
        self.log("4D Lot Calculator initialized - Portfolio Safety Mode Active")
    
    # ========================================================================================
    # 🆕 MAIN 4D LOT CALCULATION METHODS
    # ========================================================================================
    
    def calculate_4d_lot_size(self, market_analysis: Dict, positions_data: Dict,
                            order_type: str, reasoning: str = "") -> LotCalculationResult4D:
        """
        🆕 คำนวณ lot size แบบ 4D พร้อม portfolio safety
        
        Args:
            market_analysis: ผลการวิเคราะห์ 4D จาก market_analyzer
            positions_data: ข้อมูลออเดอร์ปัจจุบันจาก position_manager
            order_type: ประเภทออเดอร์ (BUY/SELL)
            reasoning: เหตุผลการเทรด
            
        Returns:
            LotCalculationResult4D: ผลลัพธ์การคำนวณ lot แบบ 4D
        """
        try:
            self.log(f"Calculating 4D lot size for {order_type} - Reason: {reasoning}")
            
            # เตรียมพารามิเตอร์ 4D
            params_4d = self._prepare_4d_calculation_params(
                market_analysis, positions_data, order_type, reasoning
            )
            
            # เลือกวิธีการคำนวณตาม reasoning
            calculation_method = self._determine_4d_calculation_method(reasoning, params_4d)
            
            # คำนวณ lot size ตามวิธีการที่เลือก
            if calculation_method == LotCalculationMethod4D.PORTFOLIO_SAFETY_4D:
                result = self._calculate_portfolio_safety_lot(params_4d)
            elif calculation_method == LotCalculationMethod4D.FOUR_D_GUIDED:
                result = self._calculate_four_d_guided_lot(params_4d)
            elif calculation_method == LotCalculationMethod4D.RECOVERY_OPTIMIZED:
                result = self._calculate_recovery_optimized_lot(params_4d)
            elif calculation_method == LotCalculationMethod4D.BALANCE_FOCUSED:
                result = self._calculate_balance_focused_lot(params_4d)
            else:
                result = self._calculate_dynamic_4d_hybrid_lot(params_4d)
            
            # ประเมินความปลอดภัยและคุณภาพ
            result = self._assess_4d_lot_quality(result, params_4d)
            
            # บันทึกการคำนวณ
            self._track_4d_calculation(result)
            
            self.log(f"4D Lot calculated: {result.lot_size:.3f} ({result.safety_rating.value})")
            
            return result
            
        except Exception as e:
            self.log(f"❌ 4D Lot calculation error: {e}")
            return self._get_fallback_4d_result(order_type, reasoning)
    
    def calculate_recovery_lot_size(self, losing_positions: List[Dict], 
                                  target_recovery: float,
                                  market_analysis: Dict) -> LotCalculationResult4D:
        """
        🆕 คำนวณ lot size สำหรับ recovery operations
        
        Args:
            losing_positions: รายการออเดอร์ขาดทุน
            target_recovery: เป้าหมายการกู้คืน ($)
            market_analysis: ผลการวิเคราะห์ 4D
            
        Returns:
            LotCalculationResult4D: ผลลัพธ์การคำนวณ lot สำหรับ recovery
        """
        try:
            self.log(f"Calculating recovery lot size - Target: ${target_recovery:.2f}")
            
            # คำนวณ lot size ที่ต้องการสำหรับ recovery
            total_loss = sum(pos.get("profit", 0) for pos in losing_positions)
            recovery_needed = abs(total_loss) + target_recovery
            
            # ประเมิน 4D opportunity สำหรับ recovery
            four_d_score = market_analysis.get("market_score_4d", 0.5)
            recovery_confidence = market_analysis.get("four_d_confidence", 0.5)
            
            # คำนวณ lot size พื้นฐานสำหรับ recovery
            # สมมุติว่า 1 lot สามารถทำกำไร $10 per 100 points movement
            points_needed = recovery_needed / 10  # $10 per lot per 100 points
            base_recovery_lot = points_needed / 100 * self.base_lot_size
            
            # ปรับตาม 4D confidence และ market conditions
            four_d_multiplier = 0.5 + (four_d_score * recovery_confidence * 1.0)
            
            # ปรับตาม portfolio safety
            safety_multiplier = self._get_portfolio_safety_multiplier()
            
            # คำนวณ lot size สุดท้าย
            recovery_lot = base_recovery_lot * four_d_multiplier * safety_multiplier
            
            # จำกัดให้อยู่ในช่วงที่ปลอดภัย
            recovery_lot = max(self.min_lot_size, 
                             min(self.max_lot_size * 0.5, recovery_lot))
            
            # สร้างผลลัพธ์
            risk_amount = recovery_lot * self.account_info.get("balance", 10000) * 0.002
            
            result = LotCalculationResult4D(
                lot_size=recovery_lot,
                calculation_method=LotCalculationMethod4D.RECOVERY_OPTIMIZED,
                risk_amount=risk_amount,
                risk_percentage=(risk_amount / self.account_info.get("balance", 10000)) * 100,
                margin_required=recovery_lot * 1000,  # ประมาณการ
                position_value=recovery_lot * market_analysis.get("current_price", 2000),
                four_d_score_impact=four_d_multiplier,
                portfolio_safety_factor=safety_multiplier,
                recovery_adjustment=1.2,  # Recovery bonus
                balance_adjustment=1.0,
                confidence_level=recovery_confidence,
                safety_rating=PortfolioSafetyLevel.MODERATE_SAFETY,
                reasoning=f"Recovery: Target ${target_recovery:.2f}, 4D={four_d_score:.3f}, Safety={safety_multiplier:.2f}",
                warnings=[],
                recommendations=[
                    f"Recovery lot size optimized for ${target_recovery:.2f} target",
                    f"4D market score: {four_d_score:.3f} - {'Favorable' if four_d_score > 0.6 else 'Cautious'}",
                    f"Portfolio safety factor: {safety_multiplier:.2f}"
                ],
                calculation_factors={
                    "base_recovery_lot": base_recovery_lot,
                    "four_d_multiplier": four_d_multiplier,
                    "safety_multiplier": safety_multiplier,
                    "target_recovery": target_recovery,
                    "total_loss": total_loss
                },
                timestamp=datetime.now()
            )
            
            self.log(f"Recovery lot calculated: {recovery_lot:.3f} for ${target_recovery:.2f} target")
            
            return result
            
        except Exception as e:
            self.log(f"❌ Recovery lot calculation error: {e}")
            return self._get_fallback_4d_result("RECOVERY", f"Recovery calculation error: {e}")
    
    # ========================================================================================
    # 🧮 4D CALCULATION METHOD IMPLEMENTATIONS
    # ========================================================================================
    
    def _calculate_portfolio_safety_lot(self, params: LotCalculationParams4D) -> LotCalculationResult4D:
        """คำนวณ lot แบบเน้นความปลอดภัย portfolio"""
        try:
            # Base safety calculation
            max_safe_risk = self.four_d_config["max_single_position_risk"]
            risk_budget = params.account_balance * (max_safe_risk / 100)
            
            # Portfolio health adjustment
            health_multiplier = 0.5 + (params.portfolio_health * 0.5)  # 0.5-1.0
            
            # Position count adjustment (ลด lot เมื่อมีออเดอร์เยอะ)
            position_adjustment = max(0.3, 1.0 - (params.current_positions_count / 50))
            
            # Margin safety check
            margin_safety = max(0.2, (params.margin_level - 200) / 800) if params.margin_level > 0 else 0.2
            
            # Calculate safe lot size
            safe_lot = (risk_budget / 1000) * health_multiplier * position_adjustment * margin_safety
            safe_lot = max(self.min_lot_size, min(self.max_lot_size * 0.3, safe_lot))
            
            return self._create_4d_result(
                lot_size=safe_lot,
                method=LotCalculationMethod4D.PORTFOLIO_SAFETY_4D,
                params=params,
                calculation_factors={
                    "health_multiplier": health_multiplier,
                    "position_adjustment": position_adjustment,
                    "margin_safety": margin_safety,
                    "risk_budget": risk_budget
                },
                reasoning=f"Safety: Health={health_multiplier:.2f}, Positions={position_adjustment:.2f}, Margin={margin_safety:.2f}"
            )
            
        except Exception as e:
            self.log(f"❌ Portfolio safety calculation error: {e}")
            return self._get_fallback_4d_result(params.order_type, "Portfolio safety error")
    
    def _calculate_four_d_guided_lot(self, params: LotCalculationParams4D) -> LotCalculationResult4D:
        """คำนวณ lot แบบขับเคลื่อนด้วย 4D analysis"""
        try:
            # Base lot from 4D score
            four_d_base = self.base_lot_size * (0.5 + params.four_d_score * 1.0)
            
            # Individual dimension impacts
            trend_impact = params.trend_dimension_score * 0.3
            volume_impact = params.volume_dimension_score * 0.25
            session_impact = params.session_dimension_score * 0.25
            volatility_impact = params.volatility_dimension_score * 0.2
            
            # Combined dimension multiplier
            dimension_multiplier = 1.0 + (trend_impact + volume_impact + session_impact + volatility_impact)
            
            # Confidence multiplier
            confidence_multiplier = 0.8 + (params.four_d_confidence * 0.4)
            
            # Market condition adjustment
            condition_multiplier = self._get_4d_market_condition_multiplier(params.market_condition_4d)
            
            # Calculate final lot
            guided_lot = four_d_base * dimension_multiplier * confidence_multiplier * condition_multiplier
            guided_lot = max(self.min_lot_size, min(self.max_lot_size * 0.6, guided_lot))
            
            return self._create_4d_result(
                lot_size=guided_lot,
                method=LotCalculationMethod4D.FOUR_D_GUIDED,
                params=params,
                calculation_factors={
                    "four_d_base": four_d_base,
                    "dimension_multiplier": dimension_multiplier,
                    "confidence_multiplier": confidence_multiplier,
                    "condition_multiplier": condition_multiplier,
                    "trend_impact": trend_impact,
                    "volume_impact": volume_impact,
                    "session_impact": session_impact,
                    "volatility_impact": volatility_impact
                },
                reasoning=f"4D-Guided: Score={params.four_d_score:.3f}, Dims={dimension_multiplier:.2f}, Conf={confidence_multiplier:.2f}"
            )
            
        except Exception as e:
            self.log(f"❌ 4D guided calculation error: {e}")
            return self._get_fallback_4d_result(params.order_type, "4D guided error")
    
    def _calculate_balance_focused_lot(self, params: LotCalculationParams4D) -> LotCalculationResult4D:
        """คำนวณ lot แบบเน้นการสร้างความสมดุล"""
        try:
            # Base lot
            base_lot = self.base_lot_size
            
            # Balance adjustment - เพิ่ม lot สำหรับฝั่งที่น้อยกว่า
            target_ratio = 0.5  # เป้าหมาย 50:50
            current_imbalance = abs(params.buy_sell_ratio - target_ratio)
            
            # ถ้าเป็น BUY และ buy_sell_ratio < 0.5 (BUY น้อยกว่า) = เพิ่ม lot
            # ถ้าเป็น SELL และ buy_sell_ratio > 0.5 (SELL น้อยกว่า) = เพิ่ม lot
            if params.order_type.upper() == "BUY" and params.buy_sell_ratio < target_ratio:
                balance_multiplier = 1.0 + (current_imbalance * 2.0)  # เพิ่มสูงสุด 100%
            elif params.order_type.upper() == "SELL" and params.buy_sell_ratio > target_ratio:
                balance_multiplier = 1.0 + (current_imbalance * 2.0)  # เพิ่มสูงสุด 100%
            else:
                balance_multiplier = 1.0 - (current_imbalance * 0.5)  # ลดเล็กน้อย
            
            # 4D quality bonus
            quality_bonus = 1.0 + (params.four_d_score * 0.3)
            
            # Calculate balanced lot
            balanced_lot = base_lot * balance_multiplier * quality_bonus
            balanced_lot = max(self.min_lot_size, min(self.max_lot_size * 0.4, balanced_lot))
            
            return self._create_4d_result(
                lot_size=balanced_lot,
                method=LotCalculationMethod4D.BALANCE_FOCUSED,
                params=params,
                calculation_factors={
                    "base_lot": base_lot,
                    "balance_multiplier": balance_multiplier,
                    "quality_bonus": quality_bonus,
                    "current_imbalance": current_imbalance,
                    "target_ratio": target_ratio
                },
                reasoning=f"Balance: Ratio={params.buy_sell_ratio:.2f}, Imbalance={current_imbalance:.2f}, Mult={balance_multiplier:.2f}"
            )
            
        except Exception as e:
            self.log(f"❌ Balance focused calculation error: {e}")
            return self._get_fallback_4d_result(params.order_type, "Balance focused error")
    
    def _calculate_dynamic_4d_hybrid_lot(self, params: LotCalculationParams4D) -> LotCalculationResult4D:
        """คำนวณ lot แบบ hybrid รวม 4D factors ทั้งหมด"""
        try:
            # Base lot
            base_lot = self.base_lot_size
            
            # 1. Portfolio Safety Factor (40% weight)
            safety_factor = self._get_portfolio_safety_factor(params)
            safety_weight = self.four_d_config["portfolio_safety_priority"]
            
            # 2. 4D Score Factor (30% weight)
            four_d_factor = 0.6 + (params.four_d_score * params.four_d_confidence * 0.8)
            four_d_weight = self.four_d_config["four_d_score_weight"]
            
            # 3. Recovery Factor (20% weight)
            recovery_factor = 1.2 if params.is_recovery_order else 1.0
            recovery_weight = self.four_d_config["recovery_weight"]
            
            # 4. Balance Factor (10% weight)
            balance_factor = self._get_balance_factor(params)
            balance_weight = self.four_d_config["balance_weight"]
            
            # Weighted combination
            hybrid_multiplier = (
                safety_factor * safety_weight +
                four_d_factor * four_d_weight +
                recovery_factor * recovery_weight +
                balance_factor * balance_weight
            )
            
            # Market condition adjustment
            market_adjustment = self._get_4d_market_condition_multiplier(params.market_condition_4d)
            
            # Volatility adjustment
            volatility_adjustment = self._get_volatility_adjustment(params.volatility_factor)
            
            # Calculate final hybrid lot
            hybrid_lot = base_lot * hybrid_multiplier * market_adjustment * volatility_adjustment
            
            # Apply final constraints
            hybrid_lot = max(self.min_lot_size, 
                           min(self.max_lot_size * 0.8, hybrid_lot))
            
            return self._create_4d_result(
                lot_size=hybrid_lot,
                method=LotCalculationMethod4D.DYNAMIC_4D_HYBRID,
                params=params,
                calculation_factors={
                    "base_lot": base_lot,
                    "safety_factor": safety_factor,
                    "four_d_factor": four_d_factor,
                    "recovery_factor": recovery_factor,
                    "balance_factor": balance_factor,
                    "hybrid_multiplier": hybrid_multiplier,
                    "market_adjustment": market_adjustment,
                    "volatility_adjustment": volatility_adjustment,
                    "weights": {
                        "safety": safety_weight,
                        "four_d": four_d_weight,
                        "recovery": recovery_weight,
                        "balance": balance_weight
                    }
                },
                reasoning=f"4D-Hybrid: Safety={safety_factor:.2f}, 4D={four_d_factor:.2f}, Rec={recovery_factor:.2f}, Bal={balance_factor:.2f}"
            )
            
        except Exception as e:
            self.log(f"❌ Dynamic 4D hybrid calculation error: {e}")
            return self._get_fallback_4d_result(params.order_type, "Dynamic 4D hybrid error")
    
    # ========================================================================================
    # 🔧 HELPER AND FACTOR CALCULATION METHODS
    # ========================================================================================
    
    def _prepare_4d_calculation_params(self, market_analysis: Dict, positions_data: Dict,
                                     order_type: str, reasoning: str) -> LotCalculationParams4D:
        """เตรียมพารามิเตอร์สำหรับการคำนวณ 4D"""
        try:
            # Account information
            balance = self.account_info.get("balance", 10000)
            equity = self.account_info.get("equity", balance)
            free_margin = self.account_info.get("free_margin", balance * 0.8)
            margin_level = self.account_info.get("margin_level", 1000)
            
            # Positions data
            current_positions = positions_data.get("active_positions", {})
            positions_count = len(current_positions)
            total_exposure = sum(abs(pos.get("profit", 0)) for pos in current_positions.values())
            
            # Portfolio metrics
            buy_positions = sum(1 for pos in current_positions.values() if pos.get("type") == 0)
            sell_positions = sum(1 for pos in current_positions.values() if pos.get("type") == 1)
            total_positions = buy_positions + sell_positions
            buy_sell_ratio = buy_positions / max(1, total_positions)
            
            portfolio_health = positions_data.get("portfolio_health", 0.7)
            recovery_opportunity = positions_data.get("recovery_opportunities", [])
            
            # 4D Analysis data
            four_d_score = market_analysis.get("market_score_4d", 0.5)
            four_d_confidence = market_analysis.get("four_d_confidence", 0.5)
            
            # Dimension scores
            trend_score = market_analysis.get("trend_dimension_score", 0.0)
            volume_score = market_analysis.get("volume_dimension_score", 0.0)
            session_score = market_analysis.get("session_dimension_score", 0.0)
            volatility_score = market_analysis.get("volatility_dimension_score", 0.0)
            
            # Market condition
            market_condition_4d = market_analysis.get("market_condition_4d", "AVERAGE_4D")
            volatility_factor = market_analysis.get("volatility_factor", 1.0)
            spread = market_analysis.get("spread", 0.05)
            
            return LotCalculationParams4D(
                account_balance=balance,
                account_equity=equity,
                free_margin=free_margin,
                margin_level=margin_level,
                base_lot_size=self.base_lot_size,
                max_risk_percentage=self.max_risk_percentage,
                current_positions_count=positions_count,
                total_exposure=total_exposure,
                four_d_score=four_d_score,
                four_d_confidence=four_d_confidence,
                trend_dimension_score=trend_score,
                volume_dimension_score=volume_score,
                session_dimension_score=session_score,
                volatility_dimension_score=volatility_score,
                market_condition_4d=market_condition_4d,
                volatility_factor=volatility_factor,
                spread=spread,
                buy_sell_ratio=buy_sell_ratio,
                portfolio_health=portfolio_health,
                recovery_opportunity=bool(recovery_opportunity),
                order_type=order_type,
                reasoning=reasoning,
                is_recovery_order="recovery" in reasoning.lower()
            )
            
        except Exception as e:
            self.log(f"❌ 4D parameter preparation error: {e}")
            # Return minimal parameters
            return LotCalculationParams4D(
                account_balance=10000, account_equity=10000, free_margin=8000,
                margin_level=1000, base_lot_size=self.base_lot_size,
                max_risk_percentage=2.0, current_positions_count=0,
                total_exposure=0.0, four_d_score=0.5, four_d_confidence=0.5,
                trend_dimension_score=0.0, volume_dimension_score=0.0,
                session_dimension_score=0.0, volatility_dimension_score=0.0,
                market_condition_4d="AVERAGE_4D", volatility_factor=1.0,
                spread=0.05, buy_sell_ratio=0.5, portfolio_health=0.7,
                recovery_opportunity=False, order_type=order_type, reasoning=reasoning
            )
    
    def _determine_4d_calculation_method(self, reasoning: str, 
                                       params: LotCalculationParams4D) -> LotCalculationMethod4D:
        """กำหนดวิธีการคำนวณ 4D ตาม reasoning"""
        try:
            reasoning_lower = reasoning.lower()
            
            # Recovery operations
            if "recovery" in reasoning_lower or "hedge" in reasoning_lower:
                return LotCalculationMethod4D.RECOVERY_OPTIMIZED
            
            # Balance operations
            elif "balance" in reasoning_lower or "rebalance" in reasoning_lower:
                return LotCalculationMethod4D.BALANCE_FOCUSED
            
            # Safety-first operations
            elif "safety" in reasoning_lower or "conservative" in reasoning_lower:
                return LotCalculationMethod4D.PORTFOLIO_SAFETY_4D
            
            # High 4D score - use 4D guided
            elif params.four_d_score >= 0.7:
                return LotCalculationMethod4D.FOUR_D_GUIDED
            
            # Default to hybrid
            else:
                return LotCalculationMethod4D.DYNAMIC_4D_HYBRID
                
        except Exception as e:
            return LotCalculationMethod4D.DYNAMIC_4D_HYBRID
    
    def _get_portfolio_safety_factor(self, params: LotCalculationParams4D) -> float:
        """คำนวณ portfolio safety factor"""
        try:
            # Health factor
            health_factor = 0.5 + (params.portfolio_health * 0.5)
            
            # Position count factor
            max_positions = self.portfolio_safety["max_positions_count"]
            position_factor = max(0.3, 1.0 - (params.current_positions_count / max_positions))
            
            # Margin factor
            margin_factor = max(0.2, min(1.0, (params.margin_level - 200) / 800)) if params.margin_level > 0 else 0.5
            
            # Exposure factor
            max_exposure_pct = self.portfolio_safety["max_total_exposure_pct"]
            current_exposure_pct = (params.total_exposure / params.account_balance) * 100
            exposure_factor = max(0.3, 1.0 - (current_exposure_pct / max_exposure_pct))
            
            # Combined safety factor
            safety_factor = (health_factor + position_factor + margin_factor + exposure_factor) / 4
            
            return round(max(0.2, min(1.0, safety_factor)), 3)
            
        except Exception as e:
            return 0.6  # Default moderate safety
    
    def _get_balance_factor(self, params: LotCalculationParams4D) -> float:
        """คำนวณ balance factor"""
        try:
            target_ratio = 0.5
            current_imbalance = abs(params.buy_sell_ratio - target_ratio)
            tolerance = self.portfolio_safety["balance_tolerance"]
            
            if current_imbalance <= tolerance:
                return 1.0  # สมดุลดี
            
            # ถ้าไม่สมดุล และออเดอร์นี้จะช่วยสร้างสมดุล
            if params.order_type.upper() == "BUY" and params.buy_sell_ratio < target_ratio:
                return 1.0 + (current_imbalance * 0.5)  # Bonus สำหรับการสร้างสมดุล
            elif params.order_type.upper() == "SELL" and params.buy_sell_ratio > target_ratio:
                return 1.0 + (current_imbalance * 0.5)  # Bonus สำหรับการสร้างสมดุล
            else:
                return 1.0 - (current_imbalance * 0.3)  # Penalty สำหรับทำให้ไม่สมดุลมากขึ้น
                
        except Exception as e:
            return 1.0
    
    def _get_4d_market_condition_multiplier(self, condition: str) -> float:
        """คำนวณตัวคูณจาก market condition 4D"""
        condition_multipliers = {
            "EXCELLENT_4D": 1.3,
            "GOOD_4D": 1.15,
            "AVERAGE_4D": 1.0,
            "POOR_4D": 0.85,
            "VERY_POOR_4D": 0.7
        }
        return condition_multipliers.get(condition, 1.0)
    
    def _get_volatility_adjustment(self, volatility_factor: float) -> float:
        """คำนวณการปรับจาก volatility"""
        try:
            if volatility_factor > 2.0:
                return 0.6  # ลดมากเมื่อ volatility สูงมาก
            elif volatility_factor > 1.5:
                return 0.8  # ลดปานกลางเมื่อ volatility สูง
            elif volatility_factor < 0.5:
                return 1.2  # เพิ่มเมื่อ volatility ต่ำ
            elif volatility_factor < 0.8:
                return 1.1  # เพิ่มเล็กน้อยเมื่อ volatility ค่อนข้างต่ำ
            else:
                return 1.0  # ปกติ
                
        except Exception as e:
            return 1.0
    
    def _get_portfolio_safety_multiplier(self) -> float:
        """คำนวณตัวคูณความปลอดภัย portfolio"""
        try:
            # เช็คสถานะความปลอดภัยปัจจุบัน
            balance = self.account_info.get("balance", 10000)
            equity = self.account_info.get("equity", balance)
            margin_level = self.account_info.get("margin_level", 1000)
            
            # Equity to balance ratio
            equity_ratio = equity / balance if balance > 0 else 1.0
            
            # Margin safety
            margin_safety = margin_level / 1000 if margin_level > 0 else 1.0
            
            # Combined safety multiplier
            safety_multiplier = min(1.0, (equity_ratio + margin_safety) / 2)
            
            return max(0.3, safety_multiplier)  # ขั้นต่ำ 30%
            
        except Exception as e:
            return 0.6  # Default moderate
    
    # ========================================================================================
    # 🔧 RESULT CREATION AND ASSESSMENT METHODS
    # ========================================================================================
    
    def _create_4d_result(self, lot_size: float, method: LotCalculationMethod4D,
                        params: LotCalculationParams4D, calculation_factors: Dict,
                        reasoning: str) -> LotCalculationResult4D:
        """สร้างผลลัพธ์การคำนวณ 4D"""
        try:
            # Calculate risk metrics
            risk_amount = lot_size * params.account_balance * 0.001  # ประมาณการ
            risk_percentage = (risk_amount / params.account_balance) * 100
            margin_required = lot_size * 1000  # ประมาณการ
            position_value = lot_size * 2000  # ประมาณการ (XAUUSD ~$2000)
            
            # 4D factors
            four_d_impact = params.four_d_score * params.four_d_confidence
            portfolio_safety = self._get_portfolio_safety_factor(params)
            recovery_adj = 1.2 if params.is_recovery_order else 1.0
            balance_adj = self._get_balance_factor(params)
            
            # Safety rating
            safety_rating = self._determine_safety_rating(risk_percentage, portfolio_safety)
            
            # Warnings and recommendations
            warnings = self._generate_4d_warnings(lot_size, risk_percentage, params)
            recommendations = self._generate_4d_recommendations(lot_size, params, four_d_impact)
            
            return LotCalculationResult4D(
                lot_size=lot_size,
                calculation_method=method,
                risk_amount=risk_amount,
                risk_percentage=risk_percentage,
                margin_required=margin_required,
                position_value=position_value,
                four_d_score_impact=four_d_impact,
                portfolio_safety_factor=portfolio_safety,
                recovery_adjustment=recovery_adj,
                balance_adjustment=balance_adj,
                confidence_level=params.four_d_confidence,
                safety_rating=safety_rating,
                reasoning=reasoning,
                warnings=warnings,
                recommendations=recommendations,
                calculation_factors=calculation_factors,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.log(f"❌ 4D result creation error: {e}")
            return self._get_fallback_4d_result(params.order_type, f"Result creation error: {e}")
    
    def _assess_4d_lot_quality(self, result: LotCalculationResult4D, 
                             params: LotCalculationParams4D) -> LotCalculationResult4D:
        """ประเมินคุณภาพของ lot size 4D"""
        try:
            # Check risk limits
            if result.risk_percentage > self.max_risk_percentage:
                result.warnings.append(f"Risk {result.risk_percentage:.1f}% exceeds limit {self.max_risk_percentage:.1f}%")
            
            # Check portfolio impact
            if params.current_positions_count > 25:
                result.warnings.append(f"High position count: {params.current_positions_count}")
            
            # Check margin safety
            if params.margin_level < 300 and params.margin_level > 0:
                result.warnings.append(f"Low margin level: {params.margin_level:.0f}%")
            
            # Check portfolio balance
            if abs(params.buy_sell_ratio - 0.5) > 0.4:
                result.warnings.append(f"Portfolio imbalanced: {params.buy_sell_ratio:.1%} BUY ratio")
            
            # Adjust safety rating based on warnings
            if len(result.warnings) >= 3:
                result.safety_rating = PortfolioSafetyLevel.BALANCED_RISK
            elif len(result.warnings) >= 5:
                result.safety_rating = PortfolioSafetyLevel.GROWTH_FOCUSED  # Riskier
            
            return result
            
        except Exception as e:
            self.log(f"❌ 4D quality assessment error: {e}")
            return result
    
    def _determine_safety_rating(self, risk_percentage: float, 
                               portfolio_safety: float) -> PortfolioSafetyLevel:
        """กำหนด safety rating"""
        combined_score = (1 - risk_percentage/10) * 0.6 + portfolio_safety * 0.4
        
        if combined_score >= 0.9:
            return PortfolioSafetyLevel.MAXIMUM_SAFETY
        elif combined_score >= 0.75:
            return PortfolioSafetyLevel.HIGH_SAFETY
        elif combined_score >= 0.6:
            return PortfolioSafetyLevel.MODERATE_SAFETY
        elif combined_score >= 0.4:
            return PortfolioSafetyLevel.BALANCED_RISK
        else:
            return PortfolioSafetyLevel.GROWTH_FOCUSED
    
    def _generate_4d_warnings(self, lot_size: float, risk_percentage: float,
                            params: LotCalculationParams4D) -> List[str]:
        """สร้าง warnings สำหรับ lot calculation"""
        warnings = []
        
        try:
            if lot_size > self.max_lot_size * 0.8:
                warnings.append(f"Large lot size: {lot_size:.3f}")
            
            if risk_percentage > 3.0:
                warnings.append(f"High risk: {risk_percentage:.1f}%")
            
            if params.four_d_score < 0.3:
                warnings.append(f"Low 4D market score: {params.four_d_score:.3f}")
            
            if params.portfolio_health < 0.4:
                warnings.append(f"Poor portfolio health: {params.portfolio_health:.1%}")
            
        except Exception as e:
            warnings.append(f"Warning generation error: {e}")
        
        return warnings
    
    def _generate_4d_recommendations(self, lot_size: float, params: LotCalculationParams4D,
                                   four_d_impact: float) -> List[str]:
        """สร้าง recommendations สำหรับ lot calculation"""
        recommendations = []
        
        try:
            if four_d_impact > 0.7:
                recommendations.append("Strong 4D signals - lot size optimized")
            elif four_d_impact > 0.4:
                recommendations.append("Moderate 4D signals - standard sizing")
            else:
                recommendations.append("Weak 4D signals - conservative sizing")
            
            if params.portfolio_health > 0.8:
                recommendations.append("Excellent portfolio health - can increase risk")
            elif params.portfolio_health < 0.5:
                recommendations.append("Poor portfolio health - recommend smaller lots")
            
            if abs(params.buy_sell_ratio - 0.5) > 0.3:
                side_needed = "SELL" if params.buy_sell_ratio > 0.5 else "BUY"
                recommendations.append(f"Portfolio needs more {side_needed} positions")
            
        except Exception as e:
            recommendations.append(f"Recommendation generation error: {e}")
        
        return recommendations
    
    # ========================================================================================
    # 🔧 UTILITY AND HELPER METHODS
    # ========================================================================================
    
    def _get_fallback_4d_result(self, order_type: str, reason: str) -> LotCalculationResult4D:
        """สร้างผลลัพธ์ fallback สำหรับกรณีเกิดข้อผิดพลาด"""
        return LotCalculationResult4D(
            lot_size=self.base_lot_size,
            calculation_method=LotCalculationMethod4D.FIXED_4D,
            risk_amount=self.base_lot_size * 100,
            risk_percentage=1.0,
            margin_required=self.base_lot_size * 1000,
            position_value=self.base_lot_size * 2000,
            four_d_score_impact=0.0,
            portfolio_safety_factor=0.5,
            recovery_adjustment=1.0,
            balance_adjustment=1.0,
            confidence_level=0.3,
            safety_rating=PortfolioSafetyLevel.MODERATE_SAFETY,
            reasoning=f"Fallback lot due to: {reason}",
            warnings=[f"Fallback calculation: {reason}"],
            recommendations=["Review calculation parameters"],
            calculation_factors={},
            timestamp=datetime.now()
        )
    
    def _track_4d_calculation(self, result: LotCalculationResult4D):
        """บันทึกการคำนวณ 4D เพื่อ tracking"""
        try:
            # Add to history
            self.calculation_history.append(result)
            
            # Update performance metrics
            self.performance_metrics["total_calculations"] += 1
            
            # Update averages
            total = self.performance_metrics["total_calculations"]
            current_avg_lot = self.performance_metrics["average_lot_size"]
            current_avg_risk = self.performance_metrics["average_risk_percentage"]
            
            self.performance_metrics["average_lot_size"] = (
                (current_avg_lot * (total - 1) + result.lot_size) / total
            )
            
            self.performance_metrics["average_risk_percentage"] = (
                (current_avg_risk * (total - 1) + result.risk_percentage) / total
            )
            
            # Track safety violations
            if result.risk_percentage > self.max_risk_percentage:
                self.performance_metrics["safety_violations"] += 1
            
            # Track positive portfolio impact
            if result.four_d_score_impact > 0.6:
                self.performance_metrics["portfolio_impact_positive"] += 1
                
        except Exception as e:
            self.log(f"❌ 4D calculation tracking error: {e}")
    
    def _get_symbol_point_value(self) -> float:
        """ดึงค่า point สำหรับสัญลักษณ์"""
        symbol_points = {
            "XAUUSD": 0.01,
            "EURUSD": 0.00001,
            "GBPUSD": 0.00001,
            "USDJPY": 0.001
        }
        return symbol_points.get(self.symbol, 0.01)
    
    def _get_symbol_contract_size(self) -> int:
        """ดึงขนาด contract สำหรับสัญลักษณ์"""
        contract_sizes = {
            "XAUUSD": 100,
            "EURUSD": 100000,
            "GBPUSD": 100000,
            "USDJPY": 100000
        }
        return contract_sizes.get(self.symbol, 100)
    
    # ========================================================================================
    # 🔍 PUBLIC INTERFACE METHODS
    # ========================================================================================
    
    def get_4d_performance_metrics(self) -> Dict:
        """ดึงข้อมูลประสิทธิภาพ 4D lot calculator"""
        try:
            # Calculate additional metrics
            if self.calculation_history:
                recent_calculations = list(self.calculation_history)[-20:]
                
                lot_sizes = [calc.lot_size for calc in recent_calculations]
                risk_percentages = [calc.risk_percentage for calc in recent_calculations]
                four_d_scores = [calc.four_d_score_impact for calc in recent_calculations]
                
                additional_metrics = {
                    "recent_statistics": {
                        "average_lot": round(statistics.mean(lot_sizes), 4),
                        "min_lot": round(min(lot_sizes), 4),
                        "max_lot": round(max(lot_sizes), 4),
                        "lot_std_dev": round(statistics.stdev(lot_sizes) if len(lot_sizes) > 1 else 0, 4)
                    },
                    "risk_statistics": {
                        "average_risk": round(statistics.mean(risk_percentages), 2),
                        "max_risk": round(max(risk_percentages), 2),
                        "risk_violations": sum(1 for r in risk_percentages if r > self.max_risk_percentage)
                    },
                    "four_d_statistics": {
                        "average_4d_impact": round(statistics.mean(four_d_scores), 3),
                        "high_4d_count": sum(1 for s in four_d_scores if s > 0.7),
                        "low_4d_count": sum(1 for s in four_d_scores if s < 0.3)
                    }
                }
            else:
                additional_metrics = {
                    "recent_statistics": {"insufficient_data": True},
                    "risk_statistics": {"insufficient_data": True},
                    "four_d_statistics": {"insufficient_data": True}
                }
            
            return {
                **self.performance_metrics,
                **additional_metrics,
                "configuration": {
                    "base_lot_size": self.base_lot_size,
                    "max_risk_percentage": self.max_risk_percentage,
                    "current_method": self.current_method.value,
                    "four_d_enabled": self.four_d_config["lot_sizing_4d_enabled"]
                }
            }
            
        except Exception as e:
            self.log(f"❌ 4D performance metrics error: {e}")
            return {"error": str(e)}
    
    def set_4d_configuration(self, **config_updates):
        """อัปเดต 4D configuration"""
        try:
            updated_items = []
            for key, value in config_updates.items():
                if key in self.four_d_config:
                    old_value = self.four_d_config[key]
                    self.four_d_config[key] = value
                    updated_items.append(f"{key}: {old_value} → {value}")
            
            if updated_items:
                self.log(f"4D Config updated: {'; '.join(updated_items)}")
            
        except Exception as e:
            self.log(f"❌ 4D configuration update error: {e}")
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 🔢 LotCalculator: {message}")


# ========================================================================================
# 🧪 4D LOT CALCULATOR TEST FUNCTIONS
# ========================================================================================

# def test_4d_lot_calculator():
#     """Test 4D Lot Calculator functionality"""
#     print("🧪 Testing 4D Lot Calculator...")
#     print("✅ 4D-Guided Lot Sizing")
#     print("✅ Portfolio Safety Integration")
#     print("✅ Recovery Lot Optimization")
#     print("✅ Balance-Focused Calculations")
#     print("✅ Dynamic Risk Assessment")
#     print("✅ Market Order Volume Optimization")
#     print("✅ Real-time Performance Tracking")
#     print("✅ Ready for 4D AI Rule Engine Integration")

# if __name__ == "__main__":
#     test_4d_lot_calculator()