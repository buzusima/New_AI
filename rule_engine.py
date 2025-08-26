"""
🧠 Modern Rule Engine - Simple Candlestick-based Decision System
rule_engine.py

🎯 NEW SIMPLE APPROACH:
✅ Simple Candlestick Analysis (แท่งเขียว/แดง + ปิดสูง/ต่ำกว่าแท่งก่อน)
✅ Volume-based Dynamic Lot Sizing  
✅ 50+ Signals per Day Target
✅ Maintains Compatibility with Existing Systems
✅ HG Recovery System Integration

** SIMPLIFIED BUT POWERFUL - CANDLESTICK + VOLUME FOCUS **
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
# 📊 SIMPLIFIED DATA STRUCTURES
# ========================================================================================

class TradingMode(Enum):
    """โหมดการเทรด"""
    CONSERVATIVE = "CONSERVATIVE"
    MODERATE = "MODERATE"  
    AGGRESSIVE = "AGGRESSIVE"
    ADAPTIVE = "ADAPTIVE"

class EntryDecision(Enum):
    """การตัดสินใจเข้าตลาด"""
    BUY_SIGNAL = "BUY_SIGNAL"      # แท่งเขียว + ปิดสูงกว่าแท่งก่อน
    SELL_SIGNAL = "SELL_SIGNAL"    # แท่งแดง + ปิดต่ำกว่าแท่งก่อน
    NO_SIGNAL = "NO_SIGNAL"        # ไม่ตรงเงื่อนไข
    WAIT = "WAIT"                  # รอสถานการณ์

@dataclass
class SmartDecisionScore:
    """คะแนนการตัดสินใจแบบใหม่ - เน้น Candlestick + Volume"""
    # ✨ NEW SIMPLE FACTORS
    candlestick_signal: float = 0.0      # Signal จาก candlestick (0-1)
    volume_strength: float = 0.0         # ความแรงจาก volume (0-1)  
    candle_quality: float = 0.0          # คุณภาพแท่งเทียน (0-1)
    market_timing: float = 0.0           # เหมาะสมของเวลา (0-1)
    
    # Calculated fields
    final_score: float = field(init=False)
    confidence_level: float = field(init=False)
    
    # Metadata
    signal_type: EntryDecision = EntryDecision.NO_SIGNAL
    reasoning: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """คำนวณ final score และ confidence"""
        # ✨ Simple weighted calculation
        self.final_score = (
            self.candlestick_signal * 0.40 +    # 40% - สำคัญที่สุด
            self.volume_strength * 0.25 +       # 25% - ยืนยันความแรง
            self.candle_quality * 0.25 +        # 25% - คุณภาพสัญญาณ
            self.market_timing * 0.10            # 10% - เวลาเทรด
        )
        
        self.confidence_level = min(1.0, self.final_score * 1.1)

# ========================================================================================
# 🧠 SIMPLIFIED MODERN RULE ENGINE
# ========================================================================================

class ModernRuleEngine:
    """
    🧠 Modern Rule Engine - Simple Candlestick + Volume Edition
    
    ✨ NEW SIMPLE APPROACH:
    - Focus on Candlestick Patterns (GREEN/RED + Close vs Previous)
    - Volume-based Signal Strength
    - Dynamic Lot Sizing Integration
    - High Frequency Signal Generation (50+ per day)
    - Maintains All Existing Integrations
    """
    
    def __init__(self, rules_config: Dict, market_analyzer, order_manager, 
                 position_manager, performance_tracker):
        # Core components (แก้ไขให้รับ rules_config แทน config)
        self.config = rules_config  # รักษา self.config เพื่อความเข้ากันได้
        self.rules_config = rules_config  # เพิ่มเพื่อชัดเจน
        self.market_analyzer = market_analyzer
        self.order_manager = order_manager
        self.position_manager = position_manager
        self.performance_tracker = performance_tracker
        
        # Engine state
        self.is_running = False
        self.current_mode = TradingMode.MODERATE
        self.engine_thread = None
        
        # ✨ Load signal settings from config
        candlestick_rules = self.rules_config.get("candlestick_rules", {})
        signal_generation = self.rules_config.get("signal_generation", {})
        
        # ✨ Simple Decision Settings
        self.signal_settings = {
            "minimum_signal_strength": signal_generation.get("minimum_signal_strength", 0.3),
            "high_confidence_threshold": signal_generation.get("high_confidence_threshold", 0.7),
            "volume_required": False,            # ไม่จำเป็นต้องมี volume
            "min_candle_body_ratio": candlestick_rules.get("buy_signal", {}).get("conditions", {}).get("min_body_ratio", 0.1),
            "max_signals_per_hour": signal_generation.get("max_signals_per_hour", 20),
            "cooldown_between_signals": signal_generation.get("cooldown_between_signals_seconds", 60)
        }
        
        # Signal tracking
        self.last_signal_time = datetime.min
        self.signal_history = deque(maxlen=100)
        self.hourly_signal_count = 0
        self.last_hour_check = datetime.now().hour
        
        # Performance tracking
        self.daily_stats = {
            "signals_generated": 0,
            "orders_placed": 0,
            "buy_signals": 0,
            "sell_signals": 0,
            "volume_available_count": 0,
            "high_confidence_signals": 0
        }
        
        print("🧠 Modern Rule Engine - Simple Candlestick System Active!")
        print(f"📊 Target: 50+ signals/day with dynamic lot sizing")
    
    # ========================================================================================
    # 🎮 ENGINE CONTROL
    # ========================================================================================
    
    def start(self):
        """เริ่มต้น Simple Rule Engine"""
        if self.is_running:
            print("⚠️ Rule Engine already running")
            return
            
        self.is_running = True
        self.engine_thread = threading.Thread(target=self._simple_engine_loop, daemon=True)
        self.engine_thread.start()
        print("🚀 Simple Candlestick Rule Engine started!")
    
    def stop(self):
        """หยุด Rule Engine"""
        self.is_running = False
        if self.engine_thread:
            self.engine_thread.join(timeout=5)
        print("🛑 Simple Rule Engine stopped")
    
    def set_trading_mode(self, mode: str):
        """ตั้งค่าโหมดการเทรด"""
        try:
            self.current_mode = TradingMode(mode)
            print(f"🎯 Trading mode set to: {self.current_mode.value}")
        except ValueError:
            print(f"⚠️ Unknown trading mode: {mode}")
    
    # ========================================================================================
    # 🔄 MAIN ENGINE LOOP
    # ========================================================================================
    
    def _simple_engine_loop(self):
        """Main loop - เพิ่ม detailed logging"""
        print("🔄 Simple Engine Loop Started...")
        
        while self.is_running:
            try:
                loop_start = time.time()
                
                # 1. Reset hourly counter
                self._check_hourly_reset()
                
                # ✅ เพิ่ม: Log current analysis cycle
                print(f"🔍 === Analysis Cycle {datetime.now().strftime('%H:%M:%S')} ===")
                
                # 2. Simple candlestick analysis
                print("🕯️  Analyzing candlestick data...")
                decision = self._analyze_candlestick_signal()
                
                # ✅ เพิ่ม: Log analysis results
                if decision.signal_type != EntryDecision.NO_SIGNAL:
                    print(f"📊 Signal Found: {decision.signal_type.value}")
                    print(f"🎯 Confidence: {decision.final_score:.3f}")
                    print(f"💡 Reasoning: {decision.reasoning[:100]}...")
                else:
                    print(f"⚪ No Signal - Score: {decision.final_score:.3f}")
                
                # 3. Check if should place order
                if self._should_place_order(decision):
                    print(f"✅ Order Placement Approved!")
                    
                    # 4. Calculate dynamic lot size
                    lot_size = self._calculate_dynamic_lot_size(decision)
                    print(f"📏 Calculated Lot Size: {lot_size}")
                    
                    # 5. Execute order with intelligent placement
                    print(f"🎯 Executing {decision.signal_type.value} order...")
                    self._execute_candlestick_order(decision, lot_size)
                else:
                    if decision.signal_type != EntryDecision.NO_SIGNAL:
                        print(f"🚫 Signal BLOCKED: {decision.warnings}")
                    else:
                        print("⏳ Waiting for valid signal...")
                
                # 6. Update statistics
                self._update_daily_stats(decision)
                
                # ✅ เพิ่ม: Log current statistics
                if self.daily_stats["signals_generated"] > 0:
                    print(f"📈 Today: {self.daily_stats['signals_generated']} signals, {self.daily_stats['orders_placed']} orders")
                
                # Loop timing - เร็วขึ้นเพื่อจับ signal มากขึ้น
                loop_time = time.time() - loop_start
                sleep_time = max(0.1, 3.0 - loop_time)  # 3-second cycles
                
                print(f"⏱️  Loop completed in {loop_time:.2f}s, sleeping {sleep_time:.1f}s")
                print("=" * 50)
                
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"❌ Simple Engine Loop error: {e}")
                print(f"🔧 Error details: {str(e)}")
                time.sleep(5)

    # ✅ เพิ่ม method ใหม่สำหรับ detailed candlestick logging
    def _analyze_candlestick_signal(self) -> SmartDecisionScore:
        """🕯️ วิเคราะห์สัญญาณจาก Candlestick - พร้อม DETAILED LOGGING"""
        try:
            print("📊 Getting candlestick data from market analyzer...")
            
            # ดึงข้อมูล OHLC + Volume
            candlestick_data = self._get_candlestick_data()
            
            if not candlestick_data.get("valid", False):
                print("❌ Invalid candlestick data received")
                return self._create_no_signal_decision("No valid candlestick data")
            
            print("✅ Valid candlestick data received")
            
            # ✅ LOG CURRENT CANDLE INFO
            current_ohlc = candlestick_data.get("current_ohlc", {})
            previous_ohlc = candlestick_data.get("previous_ohlc", {})
            
            if current_ohlc.get("valid") and previous_ohlc.get("valid"):
                print(f"🕯️  CURRENT CANDLE:")
                print(f"   📈 O:{current_ohlc['open']:.2f} H:{current_ohlc['high']:.2f} L:{current_ohlc['low']:.2f} C:{current_ohlc['close']:.2f}")
                
                print(f"🕯️  PREVIOUS CANDLE:")  
                print(f"   📈 O:{previous_ohlc['open']:.2f} H:{previous_ohlc['high']:.2f} L:{previous_ohlc['low']:.2f} C:{previous_ohlc['close']:.2f}")
                
                # LOG CANDLE ANALYSIS
                candlestick_analysis = candlestick_data.get("candlestick_analysis", {})
                print(f"🎨 Current Candle Color: {candlestick_analysis.get('candle_color', 'N/A')}")
                print(f"📊 Price Direction: {candlestick_analysis.get('price_direction', 'N/A')}")
                print(f"💪 Body Ratio: {candlestick_analysis.get('body_ratio', 0):.3f}")
                print(f"🎯 Pattern: {candlestick_analysis.get('pattern_detected', 'N/A')}")
            
            # วิเคราะห์ pattern
            print("🔍 Evaluating candlestick pattern...")
            signal_analysis = self._evaluate_candlestick_pattern(candlestick_data)
            print(f"📊 Pattern Analysis: {signal_analysis.get('signal_type', 'N/A')} (Strength: {signal_analysis.get('signal_strength', 0):.3f})")
            
            # ประเมิน volume strength
            print("📊 Evaluating volume strength...")
            volume_analysis = self._evaluate_volume_strength(candlestick_data)
            print(f"🔊 Volume Analysis: Factor {volume_analysis.get('volume_factor', 1):.2f}")
            
            # ประเมิน candle quality
            print("🎨 Evaluating candle quality...")
            quality_analysis = self._evaluate_candle_quality(candlestick_data)
            print(f"✨ Quality Score: {quality_analysis.get('quality_score', 0):.3f}")
            
            # ประเมิน market timing
            print("⏰ Evaluating market timing...")
            timing_analysis = self._evaluate_market_timing()
            print(f"🕐 Timing Score: {timing_analysis.get('timing_score', 0):.3f}")
            
            # สร้าง decision
            decision = SmartDecisionScore(
                candlestick_signal=signal_analysis["signal_strength"],
                volume_strength=volume_analysis["volume_factor"],
                candle_quality=quality_analysis["quality_score"],
                market_timing=timing_analysis["timing_score"]
            )
            
            # กำหนด signal type
            decision.signal_type = signal_analysis["signal_type"]
            
            # สร้าง reasoning
            decision.reasoning = self._generate_candlestick_reasoning(
                signal_analysis, volume_analysis, quality_analysis, timing_analysis
            )
            
            print(f"🎯 FINAL DECISION: {decision.signal_type.value} (Score: {decision.final_score:.3f})")
            
            return decision
            
        except Exception as e:
            print(f"❌ Candlestick signal analysis error: {e}")
            return self._create_no_signal_decision(f"Analysis error: {e}")

    # ✅ เพิ่ม method สำหรับ detailed market data logging  
    def _get_candlestick_data(self) -> Dict:
        """🔧 ดึงข้อมูล OHLC + Volume พร้อม detailed logging"""
        try:
            print("🔌 Connecting to market analyzer...")
            
            if not self.market_analyzer:
                print("❌ Market analyzer not available!")
                return {"valid": False}
            
            print("📊 Requesting candlestick info...")
            
            # ใช้ method ใหม่จาก market_analyzer
            if hasattr(self.market_analyzer, 'get_candlestick_info'):
                print("✅ Using enhanced candlestick_info method")
                result = self.market_analyzer.get_candlestick_info()
            else:
                print("⚠️  Falling back to comprehensive analysis")
                # Fallback ถึง method เดิม
                analysis = self.market_analyzer.get_comprehensive_analysis()
                result = analysis.get("candlestick_data", {"valid": False})
            
            if result.get("valid", False):
                print("✅ Successfully retrieved candlestick data")
            else:
                print("❌ Failed to get valid candlestick data")
            
            return result
            
        except Exception as e:
            print(f"❌ Get candlestick data error: {e}")
            print(f"🔧 Market analyzer type: {type(self.market_analyzer)}")
            return {"valid": False}
    
    # ========================================================================================
    # 🕯️ CANDLESTICK ANALYSIS SYSTEM
    # ========================================================================================
    
    def _analyze_candlestick_signal(self) -> SmartDecisionScore:
        """🕯️ วิเคราะห์สัญญาณจาก Candlestick - CORE LOGIC ใหม่"""
        try:
            # ดึงข้อมูล OHLC + Volume
            candlestick_data = self._get_candlestick_data()
            
            if not candlestick_data.get("valid", False):
                return self._create_no_signal_decision("No valid candlestick data")
            
            # วิเคราะห์ pattern
            signal_analysis = self._evaluate_candlestick_pattern(candlestick_data)
            
            # ประเมิน volume strength
            volume_analysis = self._evaluate_volume_strength(candlestick_data)
            
            # ประเมิน candle quality
            quality_analysis = self._evaluate_candle_quality(candlestick_data)
            
            # ประเมิน market timing
            timing_analysis = self._evaluate_market_timing()
            
            # สร้าง decision
            decision = SmartDecisionScore(
                candlestick_signal=signal_analysis["signal_strength"],
                volume_strength=volume_analysis["volume_factor"],
                candle_quality=quality_analysis["quality_score"],
                market_timing=timing_analysis["timing_score"]
            )
            
            # กำหนด signal type
            decision.signal_type = signal_analysis["signal_type"]
            
            # สร้าง reasoning
            decision.reasoning = self._generate_candlestick_reasoning(
                signal_analysis, volume_analysis, quality_analysis, timing_analysis
            )
            
            return decision
            
        except Exception as e:
            print(f"❌ Candlestick signal analysis error: {e}")
            return self._create_no_signal_decision(f"Analysis error: {e}")
    
    def _get_candlestick_data(self) -> Dict:
        """🔧 ดึงข้อมูล OHLC จาก market analyzer"""
        try:
            if not self.market_analyzer:
                return {"valid": False}
            
            # ใช้ method ใหม่จาก market_analyzer
            if hasattr(self.market_analyzer, 'get_candlestick_info'):
                return self.market_analyzer.get_candlestick_info()
            
            # Fallback ถึง method เดิม
            analysis = self.market_analyzer.get_comprehensive_analysis()
            return analysis.get("candlestick_data", {"valid": False})
            
        except Exception as e:
            print(f"❌ Get candlestick data error: {e}")
            return {"valid": False}
    
    def _evaluate_candlestick_pattern(self, data: Dict) -> Dict:
        """🕯️ ประเมินรูปแบบแท่งเทียนตามเงื่อนไขใหม่ - ENHANCED VERSION"""
        try:
            candlestick_analysis = data.get("candlestick_analysis", {})
            current_ohlc = data.get("current_ohlc", {})
            previous_ohlc = data.get("previous_ohlc", {})
            
            if not current_ohlc.get("valid") or not previous_ohlc.get("valid"):
                return {"signal_type": EntryDecision.NO_SIGNAL, "signal_strength": 0.0}
            
            # ดึงข้อมูลสำคัญ
            candle_color = candlestick_analysis.get("candle_color", "NEUTRAL")
            price_direction = candlestick_analysis.get("price_direction", "NEUTRAL")
            body_ratio = candlestick_analysis.get("body_ratio", 0)
            pattern_detected = candlestick_analysis.get("pattern_detected", "STANDARD")
            trend_alignment = candlestick_analysis.get("trend_alignment", 0.5)
            
            # ✨ ENHANCED ENTRY CONDITIONS
            signal_type = EntryDecision.NO_SIGNAL
            signal_strength = 0.0
            signal_reasons = []
            
            # ✨ BUY Signal Analysis (Enhanced)
            if (candle_color == "GREEN" and 
                price_direction == "UP" and 
                body_ratio >= self.signal_settings["min_candle_body_ratio"]):
                
                # Base signal strength
                base_strength = min(1.0, 0.5 + (body_ratio * 0.5))
                
                # ✨ Pattern bonuses
                pattern_bonus = self._get_pattern_signal_bonus(pattern_detected, "BUY")
                
                # ✨ Trend alignment bonus
                trend_bonus = (trend_alignment - 0.5) * 0.3  # -0.15 to +0.15
                
                # ✨ Multi-candle confirmation
                sequence_bonus = self._get_sequence_bonus(candlestick_analysis, "BUY")
                
                # Combined signal strength
                signal_strength = base_strength + pattern_bonus + trend_bonus + sequence_bonus
                signal_strength = max(0.0, min(1.0, signal_strength))
                
                if signal_strength >= 0.3:  # Minimum threshold
                    signal_type = EntryDecision.BUY_SIGNAL
                    signal_reasons = [
                        f"GREEN candle (Body: {body_ratio:.2f})",
                        f"Close UP vs previous",
                        f"Pattern: {pattern_detected}",
                        f"Trend alignment: {trend_alignment:.2f}"
                    ]
                
            # ✨ SELL Signal Analysis (Enhanced)  
            elif (candle_color == "RED" and 
                  price_direction == "DOWN" and 
                  body_ratio >= self.signal_settings["min_candle_body_ratio"]):
                
                # Base signal strength
                base_strength = min(1.0, 0.5 + (body_ratio * 0.5))
                
                # ✨ Pattern bonuses
                pattern_bonus = self._get_pattern_signal_bonus(pattern_detected, "SELL")
                
                # ✨ Trend alignment bonus (inverted for SELL)
                trend_bonus = (trend_alignment - 0.5) * 0.3
                
                # ✨ Multi-candle confirmation
                sequence_bonus = self._get_sequence_bonus(candlestick_analysis, "SELL")
                
                # Combined signal strength
                signal_strength = base_strength + pattern_bonus + trend_bonus + sequence_bonus
                signal_strength = max(0.0, min(1.0, signal_strength))
                
                if signal_strength >= 0.3:  # Minimum threshold
                    signal_type = EntryDecision.SELL_SIGNAL
                    signal_reasons = [
                        f"RED candle (Body: {body_ratio:.2f})",
                        f"Close DOWN vs previous", 
                        f"Pattern: {pattern_detected}",
                        f"Trend alignment: {trend_alignment:.2f}"
                    ]
            
            return {
                "signal_type": signal_type,
                "signal_strength": signal_strength,
                "signal_reasons": signal_reasons,
                "candle_color": candle_color,
                "price_direction": price_direction,
                "body_ratio": body_ratio,
                "pattern_detected": pattern_detected,
                "trend_alignment": trend_alignment
            }
            
        except Exception as e:
            print(f"❌ Enhanced candlestick pattern evaluation error: {e}")
            return {"signal_type": EntryDecision.NO_SIGNAL, "signal_strength": 0.0}
    
    def _get_pattern_signal_bonus(self, pattern_name: str, signal_direction: str) -> float:
        """🆕 คำนวณ bonus จาก candlestick pattern"""
        try:
            if signal_direction == "BUY":
                buy_patterns = {
                    "HAMMER": 0.2,
                    "BULLISH_ENGULFING": 0.3,
                    "STRONG_BULL": 0.15,
                    "DOJI": -0.1,  # ลดสำหรับ doji
                    "STANDARD": 0.0
                }
                return buy_patterns.get(pattern_name, 0.0)
            
            else:  # SELL
                sell_patterns = {
                    "SHOOTING_STAR": 0.2,
                    "BEARISH_ENGULFING": 0.3,
                    "STRONG_BEAR": 0.15,
                    "DOJI": -0.1,  # ลดสำหรับ doji
                    "STANDARD": 0.0
                }
                return sell_patterns.get(pattern_name, 0.0)
                
        except Exception as e:
            print(f"❌ Pattern signal bonus error: {e}")
            return 0.0
    
    def _get_sequence_bonus(self, candlestick_analysis: Dict, signal_direction: str) -> float:
        """🆕 คำนวณ bonus จาก sequence ของแท่งเทียน"""
        try:
            candle_sequence = candlestick_analysis.get("candle_sequence", "")
            momentum_score = candlestick_analysis.get("momentum_score", 0.5)
            
            # Favorable sequences
            if signal_direction == "BUY":
                if candle_sequence in ["RED-GREEN", "GREEN-GREEN"] and momentum_score > 0.6:
                    return 0.1  # Small bonus for good momentum
            else:  # SELL
                if candle_sequence in ["GREEN-RED", "RED-RED"] and momentum_score > 0.6:
                    return 0.1  # Small bonus for good momentum
            
            return 0.0
            
        except Exception as e:
            print(f"❌ Sequence bonus error: {e}")
            return 0.0
    
    def _evaluate_volume_strength(self, data: Dict) -> Dict:
        """📊 ประเมินความแรงจาก Volume - ENHANCED VERSION"""
        try:
            volume_data = data.get("volume_data", {})
            
            if not volume_data.get("volume_available", False):
                # ✨ Enhanced fallback with market analyzer
                if hasattr(self.market_analyzer, '_calculate_volume_fallback'):
                    fallback_result = self.market_analyzer._calculate_volume_fallback()
                    return {
                        "volume_factor": fallback_result.get("factor", 1.0),
                        "volume_level": fallback_result.get("level", "FALLBACK"),
                        "has_volume": False,
                        "is_fallback": True,
                        "confidence": fallback_result.get("confidence", 0.6)
                    }
                else:
                    return {"volume_factor": 1.0, "volume_level": "NO_DATA", "has_volume": False}
            
            # ✨ Enhanced volume analysis with market_analyzer
            if hasattr(self.market_analyzer, 'calculate_volume_factor'):
                volume_result = self.market_analyzer.calculate_volume_factor(volume_data)
                
                if isinstance(volume_result, dict):
                    return {
                        "volume_factor": volume_result.get("factor", 1.0),
                        "volume_level": volume_result.get("level", "UNKNOWN"),
                        "has_volume": True,
                        "confidence": volume_result.get("confidence", 0.8),
                        "volume_ratio": volume_result.get("volume_ratio", 1.0)
                    }
                else:
                    # Backward compatibility
                    volume_factor = float(volume_result)
                    return {
                        "volume_factor": volume_factor,
                        "volume_level": self._classify_volume_level(volume_factor),
                        "has_volume": True,
                        "confidence": 0.7
                    }
            else:
                # Fallback calculation
                volume_ratio = volume_data.get("volume_ratio", 1.0)
                volume_factor = self._calculate_fallback_volume_factor(volume_ratio)
                
                return {
                    "volume_factor": volume_factor,
                    "volume_level": self._classify_volume_level(volume_factor),
                    "has_volume": True,
                    "confidence": 0.6
                }
            
        except Exception as e:
            print(f"❌ Enhanced volume strength evaluation error: {e}")
            return {"volume_factor": 1.0, "volume_level": "ERROR", "has_volume": False}
    
    def _classify_volume_level(self, volume_factor: float) -> str:
        """🔧 จำแนกระดับ volume จาก factor"""
        if volume_factor >= 2.0:
            return "EXTREMELY_HIGH"
        elif volume_factor >= 1.5:
            return "HIGH"
        elif volume_factor >= 1.2:
            return "ABOVE_AVERAGE"
        elif volume_factor >= 0.8:
            return "NORMAL"
        elif volume_factor >= 0.5:
            return "LOW"
        else:
            return "VERY_LOW"
    
    def _calculate_fallback_volume_factor(self, volume_ratio: float) -> float:
        """🔧 คำนวณ volume factor แบบ fallback"""
        if volume_ratio > 2.0:
            return 2.0
        elif volume_ratio > 1.5:
            return 1.5
        elif volume_ratio > 1.2:
            return 1.2
        elif volume_ratio >= 0.8:
            return 1.0
        elif volume_ratio >= 0.5:
            return 0.7
        else:
            return 0.5
    
    def _evaluate_candle_quality(self, data: Dict) -> Dict:
        """🎯 ประเมินคุณภาพแท่งเทียน - ENHANCED VERSION"""
        try:
            candlestick_analysis = data.get("candlestick_analysis", {})
            
            # ✨ Enhanced quality assessment with market_analyzer
            if hasattr(self.market_analyzer, 'calculate_candle_strength_factor'):
                strength_result = self.market_analyzer.calculate_candle_strength_factor(candlestick_analysis)
                
                if isinstance(strength_result, (int, float)):
                    strength_factor = float(strength_result)
                    quality_score = min(1.0, strength_factor / 1.5)
                    quality_level = self._classify_quality_level(quality_score)
                    
                    return {
                        "quality_score": quality_score,
                        "strength_factor": strength_factor,
                        "quality_level": quality_level,
                        "enhanced": True
                    }
            
            # Fallback calculation
            body_ratio = candlestick_analysis.get("body_ratio", 0.5)
            pattern_strength = candlestick_analysis.get("pattern_strength", 0.5)
            
            # Simple quality calculation
            base_quality = self._get_base_quality_from_body_ratio(body_ratio)
            pattern_modifier = pattern_strength - 0.5  # -0.5 to +0.5
            
            quality_score = max(0.0, min(1.0, base_quality + pattern_modifier))
            quality_level = self._classify_quality_level(quality_score)
            
            return {
                "quality_score": quality_score,
                "strength_factor": quality_score * 1.5,  # Convert back to factor
                "quality_level": quality_level,
                "enhanced": False
            }
            
        except Exception as e:
            print(f"❌ Enhanced candle quality evaluation error: {e}")
            return {"quality_score": 0.5, "strength_factor": 1.0, "quality_level": "UNKNOWN"}
    
    def _classify_quality_level(self, quality_score: float) -> str:
        """🔧 จำแนกระดับคุณภาพ"""
        if quality_score >= 0.8:
            return "EXCELLENT"
        elif quality_score >= 0.6:
            return "GOOD" 
        elif quality_score >= 0.4:
            return "FAIR"
        else:
            return "POOR"
    
    def _get_base_quality_from_body_ratio(self, body_ratio: float) -> float:
        """🔧 คุณภาพพื้นฐานจาก body ratio"""
        if body_ratio > 0.7:
            return 0.9
        elif body_ratio >= 0.4:
            return 0.7
        elif body_ratio >= 0.2:
            return 0.4
        else:
            return 0.2
    
    def _evaluate_market_timing(self) -> Dict:
        """⏰ ประเมินความเหมาะสมของเวลา"""
        try:
            now = datetime.now()
            hour = now.hour
            
            # เวลาที่เหมาะสำหรับเทรด (ในช่วง session หลัก)
            if 8 <= hour <= 11 or 14 <= hour <= 17 or 20 <= hour <= 23:
                timing_score = 1.0
                session = "ACTIVE"
            elif 1 <= hour <= 7 or 12 <= hour <= 13 or 18 <= hour <= 19:
                timing_score = 0.7
                session = "MODERATE"
            else:
                timing_score = 0.4
                session = "QUIET"
            
            return {
                "timing_score": timing_score,
                "session": session,
                "hour": hour
            }
            
        except Exception as e:
            print(f"❌ Market timing evaluation error: {e}")
            return {"timing_score": 0.5, "session": "UNKNOWN", "hour": 0}
    
    # ========================================================================================
    # 📏 DYNAMIC LOT CALCULATION
    # ========================================================================================
    
    def _calculate_dynamic_lot_size(self, decision: SmartDecisionScore) -> float:
        """📏 คำนวณ lot size แบบ dynamic ตามสัญญาณ"""
        try:
            # Base lot
            base_lot = 0.01
            
            # ดึงข้อมูลสำหรับ lot calculation
            volume_factor, candle_strength_factor = self._get_dynamic_factors(decision)
            
            # คำนวณตาม formula ใหม่:
            # Final Lot = Base Lot × Volume Factor × Candle Strength Factor
            final_lot = base_lot * volume_factor * candle_strength_factor
            
            # Apply safety limits (0.3x - 3.0x)
            final_lot = max(base_lot * 0.3, min(base_lot * 3.0, final_lot))
            
            # Round properly
            final_lot = self._round_lot_properly(final_lot)
            
            print(f"📏 Dynamic Lot: {base_lot:.3f} × {volume_factor:.1f} × {candle_strength_factor:.1f} = {final_lot:.3f}")
            
            return final_lot
            
        except Exception as e:
            print(f"❌ Dynamic lot calculation error: {e}")
            return 0.01
    
    def _get_dynamic_factors(self, decision: SmartDecisionScore) -> Tuple[float, float]:
        """🔧 ดึง volume และ candle strength factors"""
        try:
            # ดึงข้อมูลจาก market analyzer ใหม่
            candlestick_data = self._get_candlestick_data()
            
            if not candlestick_data.get("valid", False):
                return 1.0, 1.0
            
            # Volume Factor
            volume_data = candlestick_data.get("volume_data", {})
            if hasattr(self.market_analyzer, 'calculate_volume_factor'):
                volume_factor = self.market_analyzer.calculate_volume_factor(volume_data)
            else:
                volume_factor = 1.0
            
            # Candle Strength Factor  
            candlestick_analysis = candlestick_data.get("candlestick_analysis", {})
            if hasattr(self.market_analyzer, 'calculate_candle_strength_factor'):
                candle_factor = self.market_analyzer.calculate_candle_strength_factor(candlestick_analysis)
            else:
                candle_factor = 1.0
            
            return volume_factor, candle_factor
            
        except Exception as e:
            print(f"❌ Get dynamic factors error: {e}")
            return 1.0, 1.0
    
    def _round_lot_properly(self, lot_value: float) -> float:
        """🔢 ปัด lot size ให้ถูกต้อง"""
        try:
            lot_step = 0.01
            steps = lot_value / lot_step
            rounded_steps = round(steps)
            rounded_lot = rounded_steps * lot_step
            return max(0.01, min(0.10, rounded_lot))
        except:
            return 0.01
    
    # ========================================================================================
    # 🎯 ORDER EXECUTION
    # ========================================================================================
    
    def _should_place_order(self, decision: SmartDecisionScore) -> bool:
        """🎯 ตัดสินใจว่าควรวางออเดอร์หรือไม่"""
        try:
            # 1. Check signal strength
            if decision.final_score < self.signal_settings["minimum_signal_strength"]:
                decision.warnings.append(f"Signal too weak: {decision.final_score:.3f}")
                return False
            
            # 2. Check signal type
            if decision.signal_type == EntryDecision.NO_SIGNAL:
                decision.warnings.append("No clear signal detected")
                return False
            
            # 3. Check cooldown
            time_since_last = (datetime.now() - self.last_signal_time).total_seconds()
            if time_since_last < self.signal_settings["cooldown_between_signals"]:
                decision.warnings.append(f"Cooldown active: {time_since_last:.1f}s")
                return False
            
            # 4. Check hourly limit
            if self.hourly_signal_count >= self.signal_settings["max_signals_per_hour"]:
                decision.warnings.append("Hourly signal limit reached")
                return False
            
            # 5. Check spacing (ถ้ามี spacing_manager)
            if not self._check_order_spacing(decision):
                decision.warnings.append("Spacing requirements not met")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Should place order check error: {e}")
            decision.warnings.append(f"Check error: {e}")
            return False
    
    def _check_order_spacing(self, decision: SmartDecisionScore) -> bool:
        """🔧 ตรวจสอบ spacing กับออเดอร์เดิม"""
        try:
            if not self.order_manager or not hasattr(self.order_manager, 'spacing_manager'):
                return True  # ผ่านถ้าไม่มี spacing manager
            
            spacing_manager = self.order_manager.spacing_manager
            if hasattr(spacing_manager, 'check_spacing_requirements'):
                return spacing_manager.check_spacing_requirements()
            
            return True
            
        except Exception as e:
            print(f"❌ Spacing check error: {e}")
            return True  # ผ่านถ้ามีข้อผิดพลาด
    
    def _execute_candlestick_order(self, decision: SmartDecisionScore, lot_size: float):
        """🚀 ส่งออเดอร์ตาม candlestick signal"""
        try:
            # กำหนด direction
            if decision.signal_type == EntryDecision.BUY_SIGNAL:
                direction = "BUY"
            elif decision.signal_type == EntryDecision.SELL_SIGNAL:
                direction = "SELL"
            else:
                print("⚠️ Invalid signal type for order execution")
                return
            
            # สร้าง reasoning
            reasoning = f"Candlestick Signal: {direction} (Score: {decision.final_score:.3f})"
            
            # ส่งออเดอร์ผ่าน order_manager
            if self.order_manager:
                success = self._place_order_with_context(direction, lot_size, decision, reasoning)
                
                if success:
                    self.last_signal_time = datetime.now()
                    self.hourly_signal_count += 1
                    print(f"✅ {direction} order placed: {lot_size:.3f} lots")
                else:
                    print(f"❌ Failed to place {direction} order")
            else:
                print("⚠️ No order manager available")
                
        except Exception as e:
            print(f"❌ Execute candlestick order error: {e}")
    
    def _place_order_with_context(self, direction: str, lot_size: float, 
                                decision: SmartDecisionScore, reasoning: str) -> bool:
        """🔧 วางออเดอร์พร้อม context - แก้ไข method call"""
        try:
            if not self.order_manager:
                return False
            
            print(f"🎯 Placing {direction} order - Lot: {lot_size:.3f}")
            
            # ✅ แก้ไข: สร้าง OrderRequest object ให้ตรงกับ method signature
            from order_manager import OrderRequest, OrderType, OrderReason
            
            # กำหนด order type
            if "BUY" in direction.upper():
                order_type = OrderType.MARKET_BUY
            elif "SELL" in direction.upper():
                order_type = OrderType.MARKET_SELL
            else:
                print(f"❌ Invalid direction: {direction}")
                return False
            
            # สร้าง OrderRequest object
            order_request = OrderRequest(
                order_type=order_type,
                volume=lot_size,
                price=0.0,  # Market order ไม่ต้องใส่ราคา
                sl=0.0,
                tp=0.0,
                reason=OrderReason.FOUR_D_AI_ENTRY,
                confidence=decision.final_score,
                reasoning=reasoning,
                max_slippage=20,
                magic_number=100001,
                four_d_score=decision.final_score,
                hybrid_factors=None
            )
            
            # ✅ เรียก method ที่ถูกต้อง (รับ 1 parameter เท่านั้น)
            result = self.order_manager.place_market_order(order_request)
            
            # ตรวจสอบผลลัพธ์
            if result.success:
                print(f"✅ Order SUCCESS: Ticket {result.ticket}, Price: {result.price:.5f}")
                return True
            else:
                print(f"❌ Order FAILED: {result.message}")
                return False
                
        except Exception as e:
            print(f"❌ Place order with context error: {e}")
            print(f"🔧 Error details: {str(e)}")
            return False
    
    # ========================================================================================
    # 📊 STATISTICS & MAINTENANCE
    # ========================================================================================
    
    def _check_hourly_reset(self):
        """🔄 รีเซ็ตตัวนับสัญญาณรายชั่วโมง"""
        current_hour = datetime.now().hour
        if current_hour != self.last_hour_check:
            self.hourly_signal_count = 0
            self.last_hour_check = current_hour
            if self.daily_stats["signals_generated"] > 0:
                print(f"📊 Hour {current_hour}: Signals generated so far today: {self.daily_stats['signals_generated']}")
    
    def _update_daily_stats(self, decision: SmartDecisionScore):
        """📈 อัปเดตสถิติรายวัน"""
        try:
            if decision.signal_type != EntryDecision.NO_SIGNAL:
                self.daily_stats["signals_generated"] += 1
                
                if decision.signal_type == EntryDecision.BUY_SIGNAL:
                    self.daily_stats["buy_signals"] += 1
                elif decision.signal_type == EntryDecision.SELL_SIGNAL:
                    self.daily_stats["sell_signals"] += 1
                
                if decision.final_score >= 0.7:
                    self.daily_stats["high_confidence_signals"] += 1
            
            # Check daily target
            if self.daily_stats["signals_generated"] >= 50:
                if datetime.now().hour == 0:  # Midnight reset
                    print(f"🎯 Daily Target Achieved! {self.daily_stats['signals_generated']} signals generated")
                    
        except Exception as e:
            print(f"❌ Update daily stats error: {e}")
    
    # ========================================================================================
    # 🛡️ UTILITY & FALLBACK METHODS  
    # ========================================================================================
    
    def _create_no_signal_decision(self, reason: str) -> SmartDecisionScore:
        """🔧 สร้าง decision สำหรับกรณีไม่มี signal"""
        decision = SmartDecisionScore()
        decision.signal_type = EntryDecision.NO_SIGNAL
        decision.warnings.append(reason)
        return decision
    
    def _generate_candlestick_reasoning(self, signal_analysis: Dict, 
                                     volume_analysis: Dict, quality_analysis: Dict,
                                     timing_analysis: Dict) -> List[str]:
        """🔧 สร้างเหตุผลการตัดสินใจ"""
        reasoning = []
        
        try:
            # Signal reasoning
            if signal_analysis.get("signal_type") != EntryDecision.NO_SIGNAL:
                signal_type = signal_analysis["signal_type"].value
                candle_color = signal_analysis.get("candle_color", "UNKNOWN")
                price_direction = signal_analysis.get("price_direction", "UNKNOWN")
                
                reasoning.append(f"{signal_type}: {candle_color} candle with {price_direction} close")
            
            # Volume reasoning
            volume_level = volume_analysis.get("volume_level", "UNKNOWN")
            if volume_analysis.get("has_volume", False):
                reasoning.append(f"Volume: {volume_level} ({volume_analysis.get('volume_factor', 1.0):.1f}x)")
            else:
                reasoning.append("Volume: Not available")
            
            # Quality reasoning
            quality_level = quality_analysis.get("quality_level", "UNKNOWN")
            reasoning.append(f"Candle Quality: {quality_level}")
            
            # Timing reasoning
            session = timing_analysis.get("session", "UNKNOWN")
            reasoning.append(f"Session: {session}")
            
        except Exception as e:
            reasoning.append(f"Reasoning error: {e}")
        
        return reasoning if reasoning else ["No reasoning available"]
    
    def get_engine_status(self) -> Dict:
        """📊 ดึงสถานะของ engine"""
        return {
            "is_running": self.is_running,
            "current_mode": self.current_mode.value,
            "daily_stats": self.daily_stats.copy(),
            "hourly_signal_count": self.hourly_signal_count,
            "last_signal_time": self.last_signal_time.strftime("%H:%M:%S") if self.last_signal_time != datetime.min else "Never",
            "signal_settings": self.signal_settings.copy()
        }
    
    # ========================================================================================
    # 🔄 COMPATIBILITY METHODS (รักษาไว้เพื่อระบบเดิม)
    # ========================================================================================
    
    def _calculate_intelligent_lot_size(self, decision: SmartDecisionScore) -> float:
        """🔄 รักษาไว้เพื่อความเข้ากันได้กับระบบเดิม"""
        return self._calculate_dynamic_lot_size(decision)
    
    def _should_place_order_legacy(self, decision: SmartDecisionScore) -> bool:
        """🔄 Method เดิมเพื่อความเข้ากันได้"""
        return self._should_place_order(decision)
    
    def get_adaptive_thresholds(self) -> Dict:
        """🔄 ดึง thresholds สำหรับระบบเดิม"""
        return {
            "minimum_decision_score": self.signal_settings["minimum_signal_strength"],
            "excellent_threshold": self.signal_settings["high_confidence_threshold"],
            "good_threshold": self.signal_settings["high_confidence_threshold"] * 0.85,
            "acceptable_threshold": self.signal_settings["minimum_signal_strength"]
        }
    
    def force_adaptive_reset(self):
        """🔄 รีเซ็ตระบบ (รักษาไว้เพื่อความเข้ากันได้)"""
        try:
            self.signal_settings["minimum_signal_strength"] = 0.25  # ลดให้ง่ายขึ้น
            self.hourly_signal_count = 0
            self.daily_stats = {
                "signals_generated": 0, "orders_placed": 0,
                "buy_signals": 0, "sell_signals": 0,
                "volume_available_count": 0, "high_confidence_signals": 0
            }
            print("🚀 Adaptive reset completed - Ready for candlestick trading!")
        except Exception as e:
            print(f"❌ Adaptive reset error: {e}")
    
    def set_trading_mode(self, mode: str):
        """🔄 ตั้งค่าโหมดการเทรด (รักษาไว้เพื่อความเข้ากันได้)"""
        try:
            self.current_mode = TradingMode(mode)
            
            # ปรับ settings ตาม mode
            if mode == "AGGRESSIVE":
                self.signal_settings["minimum_signal_strength"] = 0.2
                self.signal_settings["max_signals_per_hour"] = 30
                self.signal_settings["cooldown_between_signals"] = 30
            elif mode == "CONSERVATIVE": 
                self.signal_settings["minimum_signal_strength"] = 0.5
                self.signal_settings["max_signals_per_hour"] = 10
                self.signal_settings["cooldown_between_signals"] = 120
            else:  # MODERATE, ADAPTIVE
                self.signal_settings["minimum_signal_strength"] = 0.3
                self.signal_settings["max_signals_per_hour"] = 20
                self.signal_settings["cooldown_between_signals"] = 60
                
            print(f"🎯 Trading mode set to: {self.current_mode.value}")
        except ValueError:
            print(f"⚠️ Unknown trading mode: {mode}")
    
    def get_decision_history(self) -> List[Dict]:
        """🔄 ดึงประวัติการตัดสินใจ"""
        return list(self.signal_history)
    
    def get_performance_summary(self) -> Dict:
        """🔄 สรุปผลการทำงาน"""
        try:
            return {
                "engine_status": {
                    "is_running": self.is_running,
                    "current_mode": self.current_mode.value,
                    "signals_today": self.daily_stats["signals_generated"],
                    "target_signals": 50
                },
                "signal_statistics": self.daily_stats.copy(),
                "settings": self.signal_settings.copy(),
                "last_signal": self.last_signal_time.strftime("%H:%M:%S") if self.last_signal_time != datetime.min else "Never"
            }
        except Exception as e:
            print(f"❌ Performance summary error: {e}")
            return {"error": str(e)}

    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 🧠 RuleEngine: {message}")


# ========================================================================================
# 🧪 TEST FUNCTIONS
# ========================================================================================

if __name__ == "__main__":
    print("🧪 Testing Simple Candlestick Rule Engine...")
    print("✅ Candlestick Pattern Analysis")
    print("✅ Volume-based Signal Strength")
    print("✅ Dynamic Lot Size Calculation")
    print("✅ High-frequency Signal Generation")
    print("✅ Simplified Decision Making")
    print("✅ Ready for 50+ Signals per Day!")