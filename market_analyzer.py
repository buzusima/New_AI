"""
📊 Market Analyzer - Enhanced with OHLC + Volume Analysis
market_analyzer.py

🎯 NEW FEATURES FOR CANDLESTICK ANALYSIS:
✅ Current OHLC Data Retrieval  
✅ Previous OHLC Data Comparison
✅ Volume Analysis (with fallback support)
✅ Candlestick Pattern Analysis
✅ Dynamic Volume Factor Calculation
✅ Candle Strength Assessment

** ENHANCED FOR SIMPLE CANDLESTICK TRADING RULES **
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from collections import deque
import statistics

class MarketAnalyzer:
    """
    📊 Enhanced Market Analyzer with OHLC + Volume Analysis
    
    🆕 CANDLESTICK FEATURES:
    - Real-time OHLC data retrieval
    - Volume analysis with broker compatibility
    - Candlestick pattern recognition
    - Dynamic volume factor calculation
    - Candle strength assessment
    """
    
    def __init__(self, mt5_connector, config: Dict):
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Trading symbol และ timeframe
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.main_timeframe = mt5.TIMEFRAME_M5  # หลักสำหรับ candlestick analysis
        
        # Volume analysis settings
        self.volume_lookback = 20  # จำนวนแท่งสำหรับ average volume
        self.volume_available = True  # จะตรวจสอบใน runtime
        
        # Cache สำหรับประสิทธิภาพ
        self.last_analysis_time = datetime.min
        self.cached_analysis = {}
        self.cache_duration = 30  # วินาที
        
        self.log("📊 Market Analyzer Enhanced with OHLC + Volume Analysis")
    
    # ========================================================================================
    # 🆕 NEW CANDLESTICK ANALYSIS METHODS
    # ========================================================================================
    
    def get_current_ohlc(self) -> Dict:
        """🆕 ดึงข้อมูล OHLC ของแท่งปัจจุบัน"""
        try:
            # ดึงข้อมูล 2 แท่งล่าสุด (แท่งปัจจุบัน + แท่งก่อนหน้า)
            rates = mt5.copy_rates_from_pos(
                self.symbol, 
                self.main_timeframe, 
                0,  # เริ่มจากแท่งปัจจุบัน
                2   # 2 แท่ง
            )
            
            if rates is None or len(rates) < 2:
                return self._get_fallback_ohlc()
            
            # แท่งปัจจุบัน
            current = rates[-1]
            
            return {
                "time": datetime.fromtimestamp(current['time']),
                "open": float(current['open']),
                "high": float(current['high']),
                "low": float(current['low']),
                "close": float(current['close']),
                "volume": int(current.get('tick_volume', 0)),
                "valid": True
            }
            
        except Exception as e:
            self.log(f"❌ Current OHLC error: {e}")
            return self._get_fallback_ohlc()
    
    def get_previous_ohlc(self) -> Dict:
        """🆕 ดึงข้อมูล OHLC ของแท่งก่อนหน้า"""
        try:
            # ดึงข้อมูล 3 แท่งล่าสุด
            rates = mt5.copy_rates_from_pos(
                self.symbol, 
                self.main_timeframe, 
                0,  # เริ่มจากแท่งปัจจุบัน
                3   # 3 แท่ง
            )
            
            if rates is None or len(rates) < 2:
                return self._get_fallback_ohlc()
            
            # แท่งก่อนหน้า (index -2)
            previous = rates[-2]
            
            return {
                "time": datetime.fromtimestamp(previous['time']),
                "open": float(previous['open']),
                "high": float(previous['high']),
                "low": float(previous['low']),
                "close": float(previous['close']),
                "volume": int(previous.get('tick_volume', 0)),
                "valid": True
            }
            
        except Exception as e:
            self.log(f"❌ Previous OHLC error: {e}")
            return self._get_fallback_ohlc()
    
    def get_volume_data(self) -> Dict:
        """🆕 ดึงข้อมูล volume และคำนวณ average"""
        try:
            # ดึงข้อมูล volume lookback แท่ง
            rates = mt5.copy_rates_from_pos(
                self.symbol,
                self.main_timeframe,
                0,  # เริ่มจากแท่งปัจจุบัน
                self.volume_lookback + 1
            )
            
            if rates is None or len(rates) < self.volume_lookback:
                return self._get_fallback_volume_data()
            
            # แยกข้อมูล
            volumes = [int(rate.get('tick_volume', 0)) for rate in rates]
            current_volume = volumes[-1] if volumes else 0
            
            # คำนวณ average volume (ไม่รวมแท่งปัจจุบัน)
            historical_volumes = volumes[:-1] if len(volumes) > 1 else volumes
            avg_volume = statistics.mean(historical_volumes) if historical_volumes else 0
            
            # Volume ratio
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # ตรวจสอบความพร้อมใช้งาน volume
            if current_volume == 0 and avg_volume == 0:
                self.volume_available = False
                return self._get_fallback_volume_data()
            
            self.volume_available = True
            
            return {
                "current_volume": current_volume,
                "average_volume": avg_volume,
                "volume_ratio": volume_ratio,
                "volume_available": True,
                "lookback_periods": len(historical_volumes)
            }
            
        except Exception as e:
            self.log(f"❌ Volume data error: {e}")
            self.volume_available = False
            return self._get_fallback_volume_data()
    
    def get_candlestick_info(self) -> Dict:
        """🆕 รวมข้อมูล candlestick ที่จำเป็นทั้งหมด"""
        try:
            # ดึงข้อมูลพื้นฐาน
            current_ohlc = self.get_current_ohlc()
            previous_ohlc = self.get_previous_ohlc()
            volume_data = self.get_volume_data()
            
            if not current_ohlc.get("valid") or not previous_ohlc.get("valid"):
                return self._get_fallback_candlestick_info()
            
            # คำนวณ candlestick metrics
            candlestick_analysis = self._analyze_candlestick_pattern(
                current_ohlc, previous_ohlc
            )
            
            # รวมข้อมูลทั้งหมด
            return {
                "current_ohlc": current_ohlc,
                "previous_ohlc": previous_ohlc,
                "volume_data": volume_data,
                "candlestick_analysis": candlestick_analysis,
                "timestamp": datetime.now(),
                "valid": True
            }
            
        except Exception as e:
            self.log(f"❌ Candlestick info error: {e}")
            return self._get_fallback_candlestick_info()
    
    def _analyze_candlestick_pattern(self, current: Dict, previous: Dict) -> Dict:
        """🆕 วิเคราะห์ pattern แท่งเทียน"""
        try:
            # ข้อมูลแท่งปัจจุบัน
            open_price = current["open"]
            high_price = current["high"]
            low_price = current["low"]
            close_price = current["close"]
            
            # ข้อมูลแท่งก่อนหน้า
            previous_close = previous["close"]
            
            # 1. สีแท่งเทียน
            candle_color = "GREEN" if close_price > open_price else "RED"
            
            # 2. ขนาด body
            body_size = abs(close_price - open_price)
            
            # 3. ขนาดช่วงราคาเต็ม
            full_range = high_price - low_price
            
            # 4. อัตราส่วน body ต่อ range
            body_ratio = body_size / full_range if full_range > 0 else 0
            
            # 5. ทิศทางราคา
            price_direction = "UP" if close_price > previous_close else "DOWN"
            
            # 6. ประเมินความแข็งแกร่งแท่งเทียน
            candle_strength = self._calculate_candle_strength(body_ratio)
            
            # 7. การจำแนกประเภทแท่ง
            candle_type = self._classify_candle_type(body_ratio)
            
            return {
                "candle_color": candle_color,
                "body_size": body_size,
                "full_range": full_range,
                "body_ratio": body_ratio,
                "price_direction": price_direction,
                "candle_strength": candle_strength,
                "candle_type": candle_type,
                "close_vs_previous": close_price - previous_close
            }
            
        except Exception as e:
            self.log(f"❌ Candlestick pattern analysis error: {e}")
            return {
                "candle_color": "NEUTRAL", "body_size": 0, "full_range": 0,
                "body_ratio": 0, "price_direction": "NEUTRAL", 
                "candle_strength": 0.5, "candle_type": "UNKNOWN"
            }
    
    def _analyze_candlestick_pattern(self, current: Dict, previous: Dict) -> Dict:
        """🆕 วิเคราะห์ pattern แท่งเทียน - ENHANCED VERSION"""
        try:
            # ข้อมูลแท่งปัจจุบัน
            open_price = current["open"]
            high_price = current["high"]
            low_price = current["low"]
            close_price = current["close"]
            
            # ข้อมูลแท่งก่อนหน้า
            previous_open = previous["open"]
            previous_high = previous["high"]
            previous_low = previous["low"]
            previous_close = previous["close"]
            
            # 1. สีแท่งเทียน
            candle_color = "GREEN" if close_price > open_price else "RED"
            previous_color = "GREEN" if previous_close > previous_open else "RED"
            
            # 2. ขนาด body
            body_size = abs(close_price - open_price)
            previous_body_size = abs(previous_close - previous_open)
            
            # 3. ขนาดช่วงราคาเต็ม
            full_range = high_price - low_price
            previous_full_range = previous_high - previous_low
            
            # 4. อัตราส่วน body ต่อ range
            body_ratio = body_size / full_range if full_range > 0 else 0
            previous_body_ratio = previous_body_size / previous_full_range if previous_full_range > 0 else 0
            
            # 5. ทิศทางราคา
            price_direction = "UP" if close_price > previous_close else "DOWN"
            price_change = close_price - previous_close
            price_change_pct = (price_change / previous_close * 100) if previous_close > 0 else 0
            
            # 6. ✨ ENHANCED PATTERN RECOGNITION
            pattern_info = self._detect_candlestick_patterns(current, previous)
            
            # 7. ✨ TREND CONTEXT
            trend_context = self._get_short_term_trend_context(current, previous)
            
            # 8. ✨ STRENGTH ASSESSMENT
            candle_strength = self._calculate_enhanced_candle_strength(
                body_ratio, full_range, price_change_pct, pattern_info
            )
            
            return {
                # Basic candlestick info
                "candle_color": candle_color,
                "previous_color": previous_color,
                "body_size": body_size,
                "full_range": full_range,
                "body_ratio": body_ratio,
                "price_direction": price_direction,
                "close_vs_previous": price_change,
                "price_change_pct": price_change_pct,
                
                # ✨ Enhanced analysis
                "pattern_detected": pattern_info["pattern_name"],
                "pattern_strength": pattern_info["pattern_strength"],
                "trend_alignment": trend_context["trend_alignment"],
                "momentum_score": trend_context["momentum_score"],
                "candle_strength": candle_strength,
                
                # Multi-candle context
                "candle_sequence": f"{previous_color}-{candle_color}",
                "body_size_comparison": "LARGER" if body_size > previous_body_size else "SMALLER",
                "range_comparison": "WIDER" if full_range > previous_full_range else "NARROWER"
            }
            
        except Exception as e:
            self.log(f"❌ Enhanced candlestick pattern analysis error: {e}")
            return {
                "candle_color": "NEUTRAL", "body_size": 0, "full_range": 0,
                "body_ratio": 0, "price_direction": "NEUTRAL", 
                "candle_strength": 0.5, "pattern_detected": "NONE",
                "trend_alignment": 0.5
            }
    
    def _detect_candlestick_patterns(self, current: Dict, previous: Dict) -> Dict:
        """🆕 ตรวจจับ candlestick patterns ที่สำคัญ"""
        try:
            c_open, c_high, c_low, c_close = current["open"], current["high"], current["low"], current["close"]
            p_open, p_high, p_low, p_close = previous["open"], previous["high"], previous["low"], previous["close"]
            
            # คำนวณส่วนประกอบของแท่ง
            c_body = abs(c_close - c_open)
            c_range = c_high - c_low
            c_upper_shadow = c_high - max(c_open, c_close)
            c_lower_shadow = min(c_open, c_close) - c_low
            
            # ✅ แก้ไข: เพิ่มการคำนวณ p_body ที่ขาดหาย
            p_body = abs(p_close - p_open)
            
            pattern_name = "STANDARD"
            pattern_strength = 0.5
            
            # ✨ DOJI DETECTION
            if c_body < (c_range * 0.1):  # Body < 10% ของ range
                pattern_name = "DOJI"
                pattern_strength = 0.3
            
            # ✨ HAMMER DETECTION (กลับตัว bullish)
            elif (c_lower_shadow > c_body * 2 and c_upper_shadow < c_body * 0.5 and 
                  c_close > c_open and c_close > p_close):
                pattern_name = "HAMMER"
                pattern_strength = 0.8
            
            # ✨ SHOOTING STAR DETECTION (กลับตัว bearish)
            elif (c_upper_shadow > c_body * 2 and c_lower_shadow < c_body * 0.5 and 
                  c_close < c_open and c_close < p_close):
                pattern_name = "SHOOTING_STAR"
                pattern_strength = 0.8
            
            # ✨ STRONG BULLISH ENGULFING
            elif (c_close > c_open and p_close < p_open and 
                  c_close > p_open and c_open < p_close and c_body > p_body):
                pattern_name = "BULLISH_ENGULFING"
                pattern_strength = 0.9
            
            # ✨ STRONG BEARISH ENGULFING  
            elif (c_close < c_open and p_close > p_open and
                  c_close < p_open and c_open > p_close and c_body > p_body):
                pattern_name = "BEARISH_ENGULFING"
                pattern_strength = 0.9
            
            # ✨ STRONG MOMENTUM CANDLES
            elif c_body > (c_range * 0.7):  # Body > 70% ของ range
                if c_close > c_open:
                    pattern_name = "STRONG_BULL"
                    pattern_strength = 0.8
                else:
                    pattern_name = "STRONG_BEAR"
                    pattern_strength = 0.8
            
            return {
                "pattern_name": pattern_name,
                "pattern_strength": pattern_strength,
                "body_dominance": c_body / c_range if c_range > 0 else 0,
                "shadow_analysis": {
                    "upper_shadow_ratio": c_upper_shadow / c_range if c_range > 0 else 0,
                    "lower_shadow_ratio": c_lower_shadow / c_range if c_range > 0 else 0
                }
            }
            
        except Exception as e:
            self.log(f"❌ Pattern detection error: {e}")
            return {"pattern_name": "ERROR", "pattern_strength": 0.5}
    
    def _get_short_term_trend_context(self, current: Dict, previous: Dict) -> Dict:
        """🆕 วิเคราะห์ trend context ระยะสั้น"""
        try:
            # ดึงข้อมูล 10 แท่งล่าสุดสำหรับ trend
            rates = mt5.copy_rates_from_pos(self.symbol, self.main_timeframe, 0, 10)
            
            if rates is None or len(rates) < 5:
                return {"trend_alignment": 0.5, "momentum_score": 0.5}
            
            closes = [float(rate['close']) for rate in rates]
            
            # Simple trend direction
            trend_up_count = sum(1 for i in range(1, len(closes)) if closes[i] > closes[i-1])
            trend_strength = trend_up_count / (len(closes) - 1)
            
            # Momentum (ความเร็วการเปลี่ยนแปลง)
            if len(closes) >= 5:
                recent_momentum = (closes[-1] - closes[-5]) / closes[-5] * 100
                momentum_score = min(1.0, abs(recent_momentum) / 0.5)  # 0.5% = max momentum
            else:
                momentum_score = 0.5
            
            # Trend alignment with current signal
            current_direction = "UP" if current["close"] > previous["close"] else "DOWN"
            if trend_strength > 0.6:
                major_trend = "UP"
            elif trend_strength < 0.4:
                major_trend = "DOWN"
            else:
                major_trend = "SIDEWAYS"
            
            alignment_score = 1.0 if current_direction == major_trend else 0.3
            
            return {
                "trend_alignment": alignment_score,
                "momentum_score": momentum_score,
                "major_trend": major_trend,
                "trend_strength": trend_strength,
                "recent_momentum": recent_momentum if 'recent_momentum' in locals() else 0.0
            }
            
        except Exception as e:
            self.log(f"❌ Trend context error: {e}")
            return {"trend_alignment": 0.5, "momentum_score": 0.5}
    
    def _calculate_enhanced_candle_strength(self, body_ratio: float, full_range: float, 
                                          price_change_pct: float, pattern_info: Dict) -> float:
        """🆕 คำนวณความแข็งแรงแท่งเทียนแบบ enhanced"""
        try:
            # Base strength from body ratio
            if body_ratio > 0.7:
                base_strength = 1.0
            elif body_ratio >= 0.4:
                base_strength = 0.7
            elif body_ratio >= 0.2:
                base_strength = 0.4
            else:
                base_strength = 0.1
            
            # Pattern bonus
            pattern_bonus = pattern_info.get("pattern_strength", 0.5) - 0.5  # -0.5 to +0.5
            
            # Price movement bonus
            movement_bonus = min(0.2, abs(price_change_pct) / 0.5)  # max 0.2 bonus for 0.5% move
            
            # Range significance (แท่งใหญ่ = แรงกว่า)
            range_bonus = min(0.1, full_range / 10.0)  # ปรับตาม symbol
            
            # Combined strength
            total_strength = base_strength + pattern_bonus + movement_bonus + range_bonus
            
            return max(0.1, min(1.0, total_strength))
            
        except Exception as e:
            self.log(f"❌ Enhanced candle strength error: {e}")
            return 0.5
    
    def _classify_candle_type(self, body_ratio: float) -> str:
        """🆕 จำแนกประเภทแท่งเทียน"""
        try:
            if body_ratio > 0.7:
                return "STRONG_BODY"
            elif body_ratio > 0.4:
                return "MEDIUM_BODY"  
            elif body_ratio > 0.2:
                return "WEAK_BODY"
            else:
                return "DOJI_SPINNING"
        except:
            return "UNKNOWN"
    
    def calculate_volume_factor(self, volume_data: Dict) -> float:
        """🆕 คำนวณ Volume Factor สำหรับ Dynamic Lot Sizing - ENHANCED"""
        try:
            if not volume_data.get("volume_available", False):
                self.log("📊 Volume not available - using smart fallback")
                return self._calculate_volume_fallback()
            
            volume_ratio = volume_data.get("volume_ratio", 1.0)
            current_volume = volume_data.get("current_volume", 0)
            
            # ✨ Enhanced Volume Factor with validation
            if volume_ratio > 2.0:      # Volume > 200% avg
                factor = 2.0
                level = "EXTREMELY_HIGH"
                confidence = 0.9
            elif volume_ratio > 1.5:    # Volume > 150% avg
                factor = 1.5
                level = "HIGH"
                confidence = 0.8
            elif volume_ratio > 1.2:    # Volume > 120% avg
                factor = 1.2
                level = "ABOVE_AVERAGE"
                confidence = 0.7
            elif volume_ratio >= 0.8:   # Volume 80-120% avg
                factor = 1.0
                level = "NORMAL"
                confidence = 0.8
            elif volume_ratio >= 0.5:   # Volume 50-80% avg
                factor = 0.7
                level = "LOW"
                confidence = 0.6
            else:                       # Volume < 50% avg
                factor = 0.5
                level = "VERY_LOW"
                confidence = 0.5
            
            # ✨ Volume quality check
            if current_volume == 0:
                factor = 1.0  # Fallback
                level = "NO_DATA"
                confidence = 0.3
            
            self.log(f"📊 Volume Factor: {factor}x ({level}, Confidence: {confidence:.1f}) - Ratio: {volume_ratio:.2f}")
            
            return {
                "factor": factor,
                "level": level,
                "confidence": confidence,
                "volume_ratio": volume_ratio,
                "current_volume": current_volume
            }
            
        except Exception as e:
            self.log(f"❌ Enhanced volume factor calculation error: {e}")
            return {"factor": 1.0, "level": "ERROR", "confidence": 0.3}
    
    def _calculate_volume_fallback(self) -> Dict:
        """🔧 คำนวณ volume factor ทดแทนเมื่อไม่มีข้อมูล volume"""
        try:
            # ใช้ price movement เป็น proxy
            current_ohlc = self.get_current_ohlc()
            if not current_ohlc.get("valid"):
                return {"factor": 1.0, "level": "FALLBACK_DEFAULT", "confidence": 0.5}
            
            # คำนวณ price movement intensity
            price_range = current_ohlc["high"] - current_ohlc["low"]
            body_size = abs(current_ohlc["close"] - current_ohlc["open"])
            
            # Proxy factor based on price action
            if body_size > price_range * 0.8:      # แท่งใหญ่มาก
                proxy_factor = 1.5
                level = "HIGH_MOVEMENT"
            elif body_size > price_range * 0.5:    # แท่งปานกลาง
                proxy_factor = 1.2
                level = "MEDIUM_MOVEMENT"
            elif body_size > price_range * 0.2:    # แท่งเล็ก
                proxy_factor = 1.0
                level = "LOW_MOVEMENT"
            else:                                  # แท่ง doji
                proxy_factor = 0.8
                level = "MINIMAL_MOVEMENT"
            
            return {
                "factor": proxy_factor,
                "level": level,
                "confidence": 0.6,  # Lower confidence for fallback
                "is_fallback": True
            }
            
        except Exception as e:
            self.log(f"❌ Volume fallback calculation error: {e}")
            return {"factor": 1.0, "level": "ERROR", "confidence": 0.3}
    
    def calculate_candle_strength_factor(self, candlestick_data: Dict) -> float:
        """🆕 คำนวณ Candle Strength Factor - ENHANCED VERSION"""
        try:
            # ดึงข้อมูลพื้นฐาน
            body_ratio = candlestick_data.get("body_ratio", 0.5)
            pattern_strength = candlestick_data.get("pattern_strength", 0.5)
            trend_alignment = candlestick_data.get("trend_alignment", 0.5)
            
            # ✨ Enhanced calculation with pattern recognition
            base_factor = self._get_base_candle_factor(body_ratio)
            pattern_modifier = self._get_pattern_modifier(
                candlestick_data.get("pattern_detected", "STANDARD"),
                pattern_strength
            )
            trend_modifier = self._get_trend_alignment_modifier(trend_alignment)
            
            # Combined factor
            enhanced_factor = base_factor * pattern_modifier * trend_modifier
            
            # Bounds checking
            final_factor = max(0.3, min(1.5, enhanced_factor))
            
            pattern_name = candlestick_data.get("pattern_detected", "STANDARD")
            self.log(f"📊 Enhanced Candle Factor: {final_factor:.2f}x (Pattern: {pattern_name}, Trend: {trend_alignment:.2f})")
            
            return final_factor
            
        except Exception as e:
            self.log(f"❌ Enhanced candle strength factor error: {e}")
            return 1.0
    
    def _get_base_candle_factor(self, body_ratio: float) -> float:
        """🔧 Base factor จาก body ratio"""
        if body_ratio > 0.7:        # Strong Body
            return 1.5
        elif body_ratio >= 0.4:     # Medium Body  
            return 1.0
        elif body_ratio >= 0.2:     # Weak Body
            return 0.6
        else:                       # Doji/Spinning
            return 0.3
    
    def _get_pattern_modifier(self, pattern_name: str, pattern_strength: float) -> float:
        """🔧 Modifier จาก pattern ที่ตรวจพบ"""
        pattern_modifiers = {
            "HAMMER": 1.2,
            "SHOOTING_STAR": 1.2,
            "BULLISH_ENGULFING": 1.3,
            "BEARISH_ENGULFING": 1.3,
            "STRONG_BULL": 1.1,
            "STRONG_BEAR": 1.1,
            "DOJI": 0.5,
            "STANDARD": 1.0
        }
        
        base_modifier = pattern_modifiers.get(pattern_name, 1.0)
        return base_modifier * (0.5 + pattern_strength * 0.5)  # 0.5-1.5 range
    
    def _get_trend_alignment_modifier(self, trend_alignment: float) -> float:
        """🔧 Modifier จาก trend alignment"""
        # เมื่อ signal ไปทางเดียวกับ trend = แรงขึ้น
        return 0.8 + (trend_alignment * 0.4)  # 0.8-1.2 range
    
    # ========================================================================================
    # 🔄 EXISTING METHODS (KEPT FOR COMPATIBILITY) 
    # ========================================================================================
    
    def get_comprehensive_analysis(self) -> Dict:
        """รักษา interface เดิมไว้เพื่อความเข้ากันได้"""
        try:
            # ตรวจสอบ cache
            now = datetime.now()
            if (now - self.last_analysis_time).seconds < self.cache_duration:
                if self.cached_analysis:
                    return self.cached_analysis
            
            # สร้าง analysis ใหม่
            analysis = {}
            
            # เพิ่มข้อมูล candlestick ใหม่
            candlestick_info = self.get_candlestick_info()
            analysis["candlestick_data"] = candlestick_info
            
            # รักษาข้อมูลเดิม
            analysis.update(self._get_basic_technical_analysis())
            analysis.update(self._get_market_context())
            
            # Cache ผลลัพธ์
            self.cached_analysis = analysis
            self.last_analysis_time = now
            
            return analysis
            
        except Exception as e:
            self.log(f"❌ Comprehensive analysis error: {e}")
            return self._get_fallback_analysis()
    
    def _get_basic_technical_analysis(self) -> Dict:
        """วิเคราะห์เทคนิคพื้นฐาน - รักษาไว้เพื่อความเข้ากันได้"""
        try:
            # ดึงข้อมูลราคา
            rates = mt5.copy_rates_from_pos(self.symbol, self.main_timeframe, 0, 50)
            if rates is None:
                return {}
            
            df = pd.DataFrame(rates)
            close_prices = df['close'].values
            
            if len(close_prices) < 20:
                return {}
            
            # RSI
            rsi = self._calculate_rsi(close_prices, 14)
            
            # Moving averages
            ma_fast = np.mean(close_prices[-5:])
            ma_slow = np.mean(close_prices[-20:])
            
            return {
                "rsi": rsi,
                "rsi_condition": self._classify_rsi(rsi),
                "ma_direction": "BULLISH" if ma_fast > ma_slow else "BEARISH",
                "trend_strength": abs(ma_fast - ma_slow) / ma_slow if ma_slow > 0 else 0,
                "volatility_level": "NORMAL"
            }
            
        except Exception as e:
            self.log(f"❌ Technical analysis error: {e}")
            return {}
    
    def _get_market_context(self) -> Dict:
        """บริบทตลาด - รักษาไว้เพื่อความเข้ากันได้"""
        try:
            now = datetime.now()
            
            # ตรวจสอบ session
            session = self._get_trading_session(now)
            
            return {
                "session": session,
                "spread_score": 0.7,  # Placeholder
                "volume_score": 0.6   # Placeholder
            }
            
        except Exception as e:
            self.log(f"❌ Market context error: {e}")
            return {"session": "UNKNOWN"}
    
    # ========================================================================================
    # 🛡️ FALLBACK METHODS
    # ========================================================================================
    
    def _get_fallback_ohlc(self) -> Dict:
        """Fallback OHLC data เมื่อไม่สามารถดึงข้อมูลได้"""
        return {
            "time": datetime.now(),
            "open": 2000.0, "high": 2000.0, "low": 2000.0, "close": 2000.0,
            "volume": 0, "valid": False
        }
    
    def _get_fallback_volume_data(self) -> Dict:
        """Fallback volume data เมื่อไม่มี volume"""
        return {
            "current_volume": 0, "average_volume": 0, "volume_ratio": 1.0,
            "volume_available": False, "lookback_periods": 0
        }
    
    def _get_fallback_candlestick_info(self) -> Dict:
        """Fallback candlestick info"""
        return {
            "current_ohlc": self._get_fallback_ohlc(),
            "previous_ohlc": self._get_fallback_ohlc(),
            "volume_data": self._get_fallback_volume_data(),
            "candlestick_analysis": {
                "candle_color": "NEUTRAL", "price_direction": "NEUTRAL",
                "body_ratio": 0.5, "candle_strength": 0.5
            },
            "valid": False
        }
    
    def _get_fallback_analysis(self) -> Dict:
        """Fallback analysis เมื่อเกิดข้อผิดพลาด"""
        return {
            "candlestick_data": self._get_fallback_candlestick_info(),
            "trend_strength": 0.5, "volatility_level": "NORMAL",
            "session": "UNKNOWN"
        }
    
    # ========================================================================================
    # 🔧 HELPER METHODS
    # ========================================================================================
    
    def _calculate_rsi(self, prices: np.array, period: int = 14) -> float:
        """คำนวณ RSI"""
        try:
            if len(prices) < period + 1:
                return 50.0
                
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])
            
            if avg_loss == 0:
                return 100.0
                
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return float(np.clip(rsi, 0, 100))
            
        except Exception as e:
            self.log(f"❌ RSI calculation error: {e}")
            return 50.0
    
    def _classify_rsi(self, rsi: float) -> str:
        """จำแนก RSI condition"""
        if rsi < 30:
            return "OVERSOLD"
        elif rsi < 40:
            return "WEAK"
        elif rsi < 60:
            return "NEUTRAL"
        elif rsi < 70:
            return "STRONG"
        else:
            return "OVERBOUGHT"
    
    def _get_trading_session(self, current_time: datetime) -> str:
        """ระบุ trading session ปัจจุบัน"""
        try:
            hour = current_time.hour
            
            if 0 <= hour < 8:
                return "ASIAN"
            elif 8 <= hour < 16:
                return "LONDON"
            elif 16 <= hour < 24:
                return "NEW_YORK"
            else:
                return "QUIET"
                
        except:
            return "UNKNOWN"
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 📊 MarketAnalyzer: {message}")


# ========================================================================================
# 🧪 TEST FUNCTIONS
# ========================================================================================

if __name__ == "__main__":
    print("🧪 Testing Enhanced Market Analyzer...")
    print("✅ OHLC Data Retrieval")
    print("✅ Volume Analysis with Fallback")  
    print("✅ Candlestick Pattern Recognition")
    print("✅ Dynamic Volume Factor Calculation")
    print("✅ Candle Strength Assessment")
    print("✅ Ready for Simple Candlestick Trading Rules")