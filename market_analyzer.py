"""
📊 Market Analyzer - 4D Enhanced Edition
market_analyzer.py

🎯 ระบบวิเคราะห์ตลาด 4 มิติสำหรับ AI Gold Grid Trading
- 4D Market Context Analysis
- Session detection และ volatility analysis  
- Market condition scoring สำหรับ 4D AI
- Real-time market data สำหรับ hybrid decisions

** COMPATIBLE WITH 4D AI RULE ENGINE **
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import MetaTrader5 as mt5
import numpy as np
import pandas as pd
from collections import deque
import statistics
import math

class MarketAnalyzer:
    """
    📊 Market Analyzer - 4D Enhanced Edition
    
    ความสามารถใหม่:
    - ✅ get_comprehensive_analysis() ครบถ้วนสำหรับ 4D Rule Engine
    - ✅ 4D Market Context Analysis (Trend, Volume, Session, Volatility)
    - ✅ Dynamic volatility analysis พร้อม adaptive thresholds
    - ✅ Enhanced session detection พร้อม activity scoring
    - ✅ Real-time support/resistance level detection
    - ✅ Market condition scoring สำหรับ hybrid decisions
    - ✅ Performance-optimized analysis caching
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """Initialize 4D Market Analyzer"""
        if not mt5_connector:
            raise ValueError("MT5 connector is required")
            
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Trading parameters
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.timeframes = [mt5.TIMEFRAME_M1, mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_H1]
        self.analysis_period = config.get("analysis", {}).get("period", 100)
        
        # 4D Analysis configuration
        self.four_d_config = {
            "trend_analysis_depth": 50,          # จำนวน candle สำหรับวิเคราะห์ trend
            "volume_analysis_period": 20,        # ช่วงเวลาวิเคราะห์ volume
            "volatility_lookback": 30,           # ย้อนหลังสำหรับ volatility
            "session_scoring_enabled": True,     # เปิดใช้ session scoring
            "support_resistance_levels": 5,      # จำนวน S/R levels
            "market_context_refresh": 10,        # วินาที - อัปเดต market context
            "adaptive_thresholds": True          # ใช้ adaptive thresholds
        }
        
        # Technical indicators settings
        self.rsi_period = 14
        self.bb_period = 20
        self.bb_deviation = 2.0
        self.ma_fast = 10
        self.ma_slow = 30
        
        # 4D Analysis cache
        self.last_4d_analysis = {}
        self.last_analysis_time = datetime.now()
        self.analysis_cache_duration = 15  # seconds - เร็วขึ้นสำหรับ 4D
        self.price_history = deque(maxlen=500)
        
        # Market context tracking
        self.support_levels = []
        self.resistance_levels = []
        self.last_sr_update = datetime.now()
        self.session_context = {}
        self.volatility_context = {}
        
        # Performance tracking
        self.analysis_count = 0
        self.cache_hit_count = 0
        
        self.log("4D Market Analyzer initialized successfully")
    
    # ========================================================================================
    # 🆕 MAIN 4D ANALYSIS METHOD
    # ========================================================================================
    
    def get_comprehensive_analysis(self) -> Dict:
        """
        🆕 4D Market Analysis - ดึงการวิเคราะห์ตลาดแบบ 4 มิติ
        
        4 Dimensions:
        1. Trend Analysis (แนวโน้มราคา)
        2. Volume Analysis (ปริมาณการเทรด) 
        3. Session Analysis (ช่วงเวลาตลาด)
        4. Volatility Analysis (ความผันผวน)
        
        Returns:
            Dict: ข้อมูลการวิเคราะห์ 4D ครบถ้วน
        """
        try:
            self.analysis_count += 1
            self.log(f"Starting 4D Analysis #{self.analysis_count}")
            
            # เช็ค cache สำหรับ 4D analysis
            if self._is_4d_cache_valid():
                self.cache_hit_count += 1
                self.log(f"Using cached 4D analysis (Cache hits: {self.cache_hit_count})")
                return self.last_4d_analysis
            
            # ดึงข้อมูลราคาปัจจุบัน
            current_data = self._get_current_market_data()
            if not current_data:
                self.log("❌ Cannot get current market data")
                return self._minimal_4d_analysis()
            
            # ดึงข้อมูล OHLC สำหรับการวิเคราะห์
            ohlc_data = self._get_ohlc_data(mt5.TIMEFRAME_M5, self.analysis_period)
            if ohlc_data is None or len(ohlc_data) < 30:
                self.log(f"❌ Insufficient OHLC data: {len(ohlc_data) if ohlc_data is not None else 0} candles")
                return self._minimal_4d_analysis(current_data)
            
            # === 4D ANALYSIS EXECUTION ===
            
            # Dimension 1: Trend Analysis
            trend_analysis = self._analyze_4d_trend(ohlc_data)
            
            # Dimension 2: Volume Analysis  
            volume_analysis = self._analyze_4d_volume(ohlc_data)
            
            # Dimension 3: Session Analysis
            session_analysis = self._analyze_4d_session(current_data)
            
            # Dimension 4: Volatility Analysis
            volatility_analysis = self._analyze_4d_volatility(ohlc_data)
            
            # Technical indicators (supporting data)
            technical_data = self._analyze_technical_indicators(ohlc_data)
            
            # Support/Resistance levels
            sr_analysis = self._analyze_support_resistance(ohlc_data)
            
            # Market condition determination
            market_condition = self._determine_4d_market_condition(
                trend_analysis, volume_analysis, session_analysis, volatility_analysis
            )
            
            # 4D Market Score calculation
            market_score_4d = self._calculate_4d_market_score(
                trend_analysis, volume_analysis, session_analysis, volatility_analysis
            )
            
            # รวมผลการวิเคราะห์ 4D
            comprehensive_4d_analysis = {
                # === BASIC MARKET DATA ===
                "current_price": current_data["current_price"],
                "bid": current_data["bid"], 
                "ask": current_data["ask"],
                "spread": current_data["spread"],
                "timestamp": datetime.now(),
                
                # === DIMENSION 1: TREND ANALYSIS ===
                **trend_analysis,
                
                # === DIMENSION 2: VOLUME ANALYSIS ===
                **volume_analysis,
                
                # === DIMENSION 3: SESSION ANALYSIS ===
                **session_analysis,
                
                # === DIMENSION 4: VOLATILITY ANALYSIS ===
                **volatility_analysis,
                
                # === TECHNICAL SUPPORT DATA ===
                **technical_data,
                **sr_analysis,
                
                # === 4D MARKET ASSESSMENT ===
                "market_condition_4d": market_condition,
                "market_score_4d": market_score_4d,
                "four_d_confidence": self._calculate_4d_confidence(
                    trend_analysis, volume_analysis, session_analysis, volatility_analysis
                ),
                
                # === ANALYSIS METADATA ===
                "analysis_quality": self._calculate_analysis_quality(ohlc_data),
                "data_freshness": self._calculate_data_freshness(ohlc_data),
                "cache_performance": {
                    "total_analysis": self.analysis_count,
                    "cache_hits": self.cache_hit_count,
                    "cache_hit_rate": round(self.cache_hit_count / max(1, self.analysis_count), 3)
                }
            }
            
            # อัปเดต cache
            self.last_4d_analysis = comprehensive_4d_analysis
            self.last_analysis_time = datetime.now()
            
            self.log(f"4D Analysis completed - Score: {market_score_4d:.3f}, Condition: {market_condition}")
            
            return comprehensive_4d_analysis
            
        except Exception as e:
            self.log(f"❌ 4D Analysis error: {e}")
            return self._minimal_4d_analysis()
    
    # ========================================================================================
    # 🔍 4D DIMENSION ANALYSIS METHODS
    # ========================================================================================
    
    def _analyze_4d_trend(self, ohlc_data: pd.DataFrame) -> Dict:
        """
        🎯 Dimension 1: Advanced Trend Analysis
        """
        try:
            close_prices = ohlc_data['close'].values
            high_prices = ohlc_data['high'].values
            low_prices = ohlc_data['low'].values
            
            # Multiple timeframe trend analysis
            trend_5m = self._calculate_trend_direction(close_prices[-5:])
            trend_15m = self._calculate_trend_direction(close_prices[-15:])
            trend_30m = self._calculate_trend_direction(close_prices[-30:])
            
            # Trend strength calculation
            trend_strength = self._calculate_trend_strength(close_prices[-30:])
            
            # Trend momentum
            momentum_short = (close_prices[-1] - close_prices[-5]) / close_prices[-5] * 100
            momentum_long = (close_prices[-1] - close_prices[-15]) / close_prices[-15] * 100
            
            # Price action patterns
            recent_highs = high_prices[-10:]
            recent_lows = low_prices[-10:]
            higher_highs = sum(recent_highs[i] > recent_highs[i-1] for i in range(1, len(recent_highs)))
            higher_lows = sum(recent_lows[i] > recent_lows[i-1] for i in range(1, len(recent_lows)))
            
            # Trend consistency
            trend_consistency = self._calculate_trend_consistency(close_prices[-20:])
            
            # Overall trend assessment
            if trend_5m == trend_15m == trend_30m:
                trend_alignment = 1.0
                main_trend = trend_5m
            elif trend_15m == trend_30m:
                trend_alignment = 0.7
                main_trend = trend_15m
            else:
                trend_alignment = 0.3
                main_trend = "MIXED"
            
            return {
                # Primary trend data
                "trend_direction": main_trend,
                "trend_strength": round(trend_strength, 3),
                "trend_alignment": round(trend_alignment, 3),
                "trend_consistency": round(trend_consistency, 3),
                
                # Multi-timeframe trends
                "trend_5m": trend_5m,
                "trend_15m": trend_15m, 
                "trend_30m": trend_30m,
                
                # Momentum data
                "momentum_short": round(momentum_short, 4),
                "momentum_long": round(momentum_long, 4),
                "momentum_divergence": abs(momentum_short - momentum_long),
                
                # Price action
                "higher_highs_count": higher_highs,
                "higher_lows_count": higher_lows,
                "price_action_bullish": higher_highs >= 6 and higher_lows >= 6,
                
                # Trend dimension score
                "trend_dimension_score": round(trend_alignment * trend_strength * trend_consistency, 3)
            }
            
        except Exception as e:
            self.log(f"❌ Trend analysis error: {e}")
            return {
                "trend_direction": "SIDEWAYS", "trend_strength": 0.0,
                "trend_alignment": 0.0, "momentum_short": 0.0,
                "trend_dimension_score": 0.0
            }
    
    def _analyze_4d_volume(self, ohlc_data: pd.DataFrame) -> Dict:
        """
        📊 Dimension 2: Advanced Volume Analysis
        """
        try:
            # ใช้ tick_volume แทน volume จริง (MT5 limitation)
            volumes = ohlc_data['tick_volume'].values if 'tick_volume' in ohlc_data else ohlc_data['real_volume'].values
            close_prices = ohlc_data['close'].values
            
            # Volume moving averages
            vol_ma_10 = np.mean(volumes[-10:])
            vol_ma_20 = np.mean(volumes[-20:])
            current_volume = volumes[-1]
            
            # Volume trend
            volume_trend = "INCREASING" if vol_ma_10 > vol_ma_20 else "DECREASING"
            volume_ratio = vol_ma_10 / vol_ma_20 if vol_ma_20 > 0 else 1.0
            
            # Volume spikes detection
            volume_threshold = vol_ma_20 * 1.5
            recent_spikes = sum(1 for v in volumes[-10:] if v > volume_threshold)
            
            # Volume-price relationship
            price_changes = np.diff(close_prices[-10:])
            volume_changes = np.diff(volumes[-10:])
            
            # Volume strength assessment
            volume_strength = min(1.0, current_volume / vol_ma_20)
            
            # On-balance volume approximation
            obv_trend = self._calculate_obv_trend(close_prices[-20:], volumes[-20:])
            
            return {
                # Primary volume data
                "current_volume": int(current_volume),
                "volume_ma_10": round(vol_ma_10, 0),
                "volume_ma_20": round(vol_ma_20, 0),
                "volume_ratio": round(volume_ratio, 3),
                
                # Volume trend analysis
                "volume_trend": volume_trend,
                "volume_strength": round(volume_strength, 3),
                "volume_spikes_count": recent_spikes,
                
                # Volume-price relationship
                "obv_trend": obv_trend,
                "volume_price_correlation": self._calculate_volume_price_correlation(
                    price_changes, volume_changes
                ),
                
                # Volume dimension score
                "volume_dimension_score": round(
                    (volume_strength + (1 if volume_trend == "INCREASING" else 0.5) + 
                     min(1.0, recent_spikes / 5)) / 3, 3
                ),
                
                # Volume confirmation
                "volume_confirms_trend": recent_spikes >= 2 and volume_trend == "INCREASING"
            }
            
        except Exception as e:
            self.log(f"❌ Volume analysis error: {e}")
            return {
                "current_volume": 0, "volume_trend": "UNKNOWN",
                "volume_strength": 0.5, "volume_dimension_score": 0.5
            }
    
    def _analyze_4d_session(self, current_data: Dict) -> Dict:
        """
        🌍 Dimension 3: Advanced Session Analysis
        """
        try:
            current_time = datetime.now()
            current_hour = current_time.hour
            
            # Session identification
            session_info = self._identify_trading_session(current_hour)
            
            # Session volatility characteristics
            session_volatility = self._get_session_volatility_profile(session_info["session"])
            
            # Session overlap detection
            overlaps = self._detect_session_overlaps(current_hour)
            
            # Time-based activity scoring
            activity_score = self._calculate_time_activity_score(current_hour)
            
            # Market opening/closing proximity
            proximity_events = self._calculate_session_proximity(current_hour)
            
            return {
                # Primary session data
                "market_session": session_info["session"],
                "session_activity_level": session_info["activity_level"],
                "session_factor": session_info["session_factor"],
                "current_hour": current_hour,
                
                # Session characteristics
                "is_major_session": session_info["is_major_session"],
                "session_volatility_expected": session_volatility,
                "activity_score": round(activity_score, 3),
                
                # Session overlaps and events
                "session_overlaps": overlaps,
                "proximity_to_open": proximity_events["open_proximity"],
                "proximity_to_close": proximity_events["close_proximity"],
                
                # Session dimension score
                "session_dimension_score": round(
                    (activity_score + session_info["session_factor"] + 
                     (1.0 if overlaps else 0.5)) / 3, 3
                ),
                
                # Session trading recommendation
                "session_favorable": activity_score > 0.6 and session_info["is_major_session"]
            }
            
        except Exception as e:
            self.log(f"❌ Session analysis error: {e}")
            return {
                "market_session": "UNKNOWN", "session_activity_level": "MEDIUM",
                "session_factor": 1.0, "session_dimension_score": 0.5
            }
    
    def _analyze_4d_volatility(self, ohlc_data: pd.DataFrame) -> Dict:
        """
        📈 Dimension 4: Advanced Volatility Analysis
        """
        try:
            close_prices = ohlc_data['close'].values
            high_prices = ohlc_data['high'].values
            low_prices = ohlc_data['low'].values
            
            # Multiple volatility measures
            price_volatility = np.std(close_prices[-20:]) / np.mean(close_prices[-20:])
            range_volatility = np.mean((high_prices[-20:] - low_prices[-20:]) / close_prices[-20:])
            
            # ATR calculation
            atr_values = []
            for i in range(1, min(15, len(ohlc_data))):
                true_range = max(
                    high_prices[-i] - low_prices[-i],
                    abs(high_prices[-i] - close_prices[-i-1]),
                    abs(low_prices[-i] - close_prices[-i-1])
                )
                atr_values.append(true_range)
            
            current_atr = np.mean(atr_values) if atr_values else 0.0
            atr_percentage = (current_atr / close_prices[-1]) * 100
            
            # Volatility trend
            vol_short = np.std(close_prices[-10:]) / np.mean(close_prices[-10:])
            vol_long = np.std(close_prices[-20:]) / np.mean(close_prices[-20:])
            vol_trend = "INCREASING" if vol_short > vol_long else "DECREASING"
            
            # Volatility classification
            if atr_percentage < 0.05:
                vol_level = "VERY_LOW"
                vol_factor = 0.5
            elif atr_percentage < 0.1:
                vol_level = "LOW"
                vol_factor = 0.7
            elif atr_percentage < 0.2:
                vol_level = "MEDIUM"
                vol_factor = 1.0
            elif atr_percentage < 0.3:
                vol_level = "HIGH"
                vol_factor = 1.3
            else:
                vol_level = "VERY_HIGH"
                vol_factor = 1.5
            
            # Volatility breakout detection
            recent_ranges = [(high_prices[i] - low_prices[i]) for i in range(-10, 0)]
            avg_range = np.mean(recent_ranges)
            current_range = high_prices[-1] - low_prices[-1]
            breakout_potential = current_range / avg_range if avg_range > 0 else 1.0
            
            return {
                # Primary volatility data
                "volatility_level": vol_level,
                "volatility_factor": round(vol_factor, 3),
                "atr": round(current_atr, 5),
                "atr_percentage": round(atr_percentage, 3),
                
                # Volatility analysis
                "price_volatility": round(price_volatility, 5),
                "range_volatility": round(range_volatility, 5),
                "volatility_trend": vol_trend,
                
                # Breakout analysis
                "breakout_potential": round(breakout_potential, 3),
                "is_volatility_expansion": breakout_potential > 1.2,
                
                # Volatility dimension score
                "volatility_dimension_score": round(
                    min(1.0, (vol_factor + breakout_potential + 
                             (1.0 if vol_trend == "INCREASING" else 0.5)) / 3), 3
                ),
                
                # Trading implications
                "volatility_favorable": 0.8 <= vol_factor <= 1.3 and breakout_potential > 1.1
            }
            
        except Exception as e:
            self.log(f"❌ Volatility analysis error: {e}")
            return {
                "volatility_level": "MEDIUM", "volatility_factor": 1.0,
                "atr": 0.0, "volatility_dimension_score": 0.5
            }
    
    # ========================================================================================
    # 🧮 4D SCORING AND ASSESSMENT METHODS  
    # ========================================================================================
    
    def _determine_4d_market_condition(self, trend: Dict, volume: Dict, 
                                      session: Dict, volatility: Dict) -> str:
        """
        🎯 กำหนด Market Condition จาก 4D Analysis
        """
        try:
            trend_score = trend.get("trend_dimension_score", 0.0)
            volume_score = volume.get("volume_dimension_score", 0.0) 
            session_score = session.get("session_dimension_score", 0.0)
            volatility_score = volatility.get("volatility_dimension_score", 0.0)
            
            overall_score = (trend_score + volume_score + session_score + volatility_score) / 4
            
            # Market condition classification
            if overall_score >= 0.8:
                return "EXCELLENT_4D"
            elif overall_score >= 0.65:
                return "GOOD_4D"
            elif overall_score >= 0.5:
                return "AVERAGE_4D"  
            elif overall_score >= 0.35:
                return "POOR_4D"
            else:
                return "VERY_POOR_4D"
                
        except Exception as e:
            return "UNKNOWN_4D"
    
    def _calculate_4d_market_score(self, trend: Dict, volume: Dict,
                                  session: Dict, volatility: Dict) -> float:
        """
        📊 คำนวณ 4D Market Score รวม
        """
        try:
            # Individual dimension scores with weights
            trend_score = trend.get("trend_dimension_score", 0.0) * 0.3
            volume_score = volume.get("volume_dimension_score", 0.0) * 0.25
            session_score = session.get("session_dimension_score", 0.0) * 0.2
            volatility_score = volatility.get("volatility_dimension_score", 0.0) * 0.25
            
            total_4d_score = trend_score + volume_score + session_score + volatility_score
            
            return round(max(0.0, min(1.0, total_4d_score)), 3)
            
        except Exception as e:
            return 0.5
    
    def _calculate_4d_confidence(self, trend: Dict, volume: Dict,
                                session: Dict, volatility: Dict) -> float:
        """
        🎯 คำนวณความเชื่อมั่นของ 4D Analysis
        """
        try:
            # Data quality factors
            trend_alignment = trend.get("trend_alignment", 0.0)
            volume_confirms = 1.0 if volume.get("volume_confirms_trend", False) else 0.5
            session_favorable = 1.0 if session.get("session_favorable", False) else 0.5
            volatility_favorable = 1.0 if volatility.get("volatility_favorable", False) else 0.5
            
            confidence = (trend_alignment + volume_confirms + session_favorable + volatility_favorable) / 4
            
            return round(max(0.0, min(1.0, confidence)), 3)
            
        except Exception as e:
            return 0.5
    
    # ========================================================================================
    # 🔧 SUPPORTING ANALYSIS METHODS
    # ========================================================================================
    
    def _analyze_technical_indicators(self, ohlc_data: pd.DataFrame) -> Dict:
        """วิเคราะห์ technical indicators พื้นฐาน"""
        try:
            close_prices = ohlc_data['close'].values
            high_prices = ohlc_data['high'].values
            low_prices = ohlc_data['low'].values
            
            # RSI
            rsi = self._calculate_rsi(close_prices, self.rsi_period)
            rsi_condition = self._classify_rsi(rsi)
            
            # MACD (simplified)
            ema_12 = self._calculate_ema(close_prices, 12)
            ema_26 = self._calculate_ema(close_prices, 26)
            macd = ema_12[-1] - ema_26[-1] if len(ema_12) > 0 and len(ema_26) > 0 else 0
            
            # Bollinger Bands
            bb_middle = np.mean(close_prices[-self.bb_period:])
            bb_std = np.std(close_prices[-self.bb_period:]) 
            bb_upper = bb_middle + (bb_std * self.bb_deviation)
            bb_lower = bb_middle - (bb_std * self.bb_deviation)
            current_price = close_prices[-1]
            bb_position = (current_price - bb_lower) / (bb_upper - bb_lower) if bb_upper != bb_lower else 0.5
            
            # Moving Averages
            ma_fast = np.mean(close_prices[-self.ma_fast:])
            ma_slow = np.mean(close_prices[-self.ma_slow:])
            ma_direction = "BULLISH" if ma_fast > ma_slow else "BEARISH"
            
            # Stochastic oscillator
            lowest_low = np.min(low_prices[-14:])
            highest_high = np.max(high_prices[-14:])
            stochastic = ((current_price - lowest_low) / (highest_high - lowest_low) * 100) if highest_high != lowest_low else 50
            stoch_condition = self._classify_stochastic(stochastic)
            
            return {
                "rsi": round(rsi, 2),
                "rsi_condition": rsi_condition,
                "macd": round(macd, 5),
                "bollinger_position": round(bb_position, 3),
                "ma_direction": ma_direction,
                "stochastic": round(stochastic, 2),
                "stoch_condition": stoch_condition,
                "bb_upper": round(bb_upper, 5),
                "bb_lower": round(bb_lower, 5),
                "ma_fast": round(ma_fast, 5),
                "ma_slow": round(ma_slow, 5)
            }
            
        except Exception as e:
            self.log(f"❌ Technical analysis error: {e}")
            return {
                "rsi": 50, "rsi_condition": "NEUTRAL", "macd": 0,
                "bollinger_position": 0.5, "ma_direction": "NEUTRAL",
                "stochastic": 50, "stoch_condition": "NEUTRAL"
            }
    
    def _analyze_support_resistance(self, ohlc_data: pd.DataFrame) -> Dict:
        """วิเคราะห์ Support/Resistance levels"""
        try:
            close_prices = ohlc_data['close'].values
            high_prices = ohlc_data['high'].values
            low_prices = ohlc_data['low'].values
            current_price = close_prices[-1]
            
            # Find pivot points
            lookback = min(20, len(ohlc_data) // 2)
            support_levels = []
            resistance_levels = []
            
            for i in range(lookback, len(ohlc_data) - lookback):
                # Support detection
                if (low_prices[i] == min(low_prices[i-lookback:i+lookback]) and
                    low_prices[i] < current_price):
                    support_levels.append({
                        "level": low_prices[i],
                        "strength": self._calculate_level_strength(low_prices, low_prices[i], 'support'),
                        "distance": current_price - low_prices[i]
                    })
                
                # Resistance detection  
                if (high_prices[i] == max(high_prices[i-lookback:i+lookback]) and
                    high_prices[i] > current_price):
                    resistance_levels.append({
                        "level": high_prices[i],
                        "strength": self._calculate_level_strength(high_prices, high_prices[i], 'resistance'),
                        "distance": high_prices[i] - current_price
                    })
            
            # Sort and limit levels
            support_levels = sorted(support_levels, key=lambda x: x['distance'])[:self.four_d_config["support_resistance_levels"]]
            resistance_levels = sorted(resistance_levels, key=lambda x: x['distance'])[:self.four_d_config["support_resistance_levels"]]
            
            # Find nearest levels
            nearest_support = min(support_levels, key=lambda x: x['distance']) if support_levels else None
            nearest_resistance = min(resistance_levels, key=lambda x: x['distance']) if resistance_levels else None
            
            return {
                "support_levels": support_levels,
                "resistance_levels": resistance_levels,
                "nearest_support": nearest_support,
                "nearest_resistance": nearest_resistance,
                "support_distance": nearest_support['distance'] if nearest_support else float('inf'),
                "resistance_distance": nearest_resistance['distance'] if nearest_resistance else float('inf'),
                "near_support": nearest_support['distance'] < current_price * 0.001 if nearest_support else False,
                "near_resistance": nearest_resistance['distance'] < current_price * 0.001 if nearest_resistance else False
            }
            
        except Exception as e:
            self.log(f"❌ S/R analysis error: {e}")
            return {
                "support_levels": [], "resistance_levels": [],
                "nearest_support": None, "nearest_resistance": None,
                "support_distance": float('inf'), "resistance_distance": float('inf')
            }
    
    # ========================================================================================
    # 🔧 HELPER AND UTILITY METHODS
    # ========================================================================================
    
    def _get_current_market_data(self) -> Dict:
        """ดึงข้อมูลตลาดปัจจุบัน"""
        try:
            symbol_info = mt5.symbol_info_tick(self.symbol)
            if symbol_info is None:
                return {}
            
            spread = symbol_info.ask - symbol_info.bid
            current_price = (symbol_info.bid + symbol_info.ask) / 2
            
            return {
                "current_price": round(current_price, 5),
                "bid": round(symbol_info.bid, 5),
                "ask": round(symbol_info.ask, 5),
                "spread": round(spread, 5),
                "time": symbol_info.time
            }
            
        except Exception as e:
            self.log(f"❌ Market data error: {e}")
            return {}
    
    def _get_ohlc_data(self, timeframe: int, count: int) -> pd.DataFrame:
        """ดึงข้อมูล OHLC"""
        try:
            rates = mt5.copy_rates_from_pos(self.symbol, timeframe, 0, count)
            if rates is None or len(rates) == 0:
                return None
                
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            return df
            
        except Exception as e:
            self.log(f"❌ OHLC data error: {e}")
            return None
    
    def _is_4d_cache_valid(self) -> bool:
        """เช็คว่า 4D analysis cache ยังใช้ได้หรือไม่"""
        try:
            if not self.last_4d_analysis:
                return False
            
            time_diff = (datetime.now() - self.last_analysis_time).total_seconds()
            return time_diff < self.analysis_cache_duration
            
        except:
            return False
    
    def _minimal_4d_analysis(self, current_data: Dict = None) -> Dict:
        """การวิเคราะห์ 4D ขั้นต่ำเมื่อไม่มีข้อมูล"""
        if current_data is None:
            current_data = {"current_price": 0, "bid": 0, "ask": 0, "spread": 0.05}
            
        return {
            # Basic data
            "current_price": current_data.get("current_price", 0),
            "bid": current_data.get("bid", 0),
            "ask": current_data.get("ask", 0),
            "spread": current_data.get("spread", 0.05),
            "timestamp": datetime.now(),
            
            # Dimension 1: Trend
            "trend_direction": "SIDEWAYS",
            "trend_strength": 0.0,
            "trend_dimension_score": 0.0,
            
            # Dimension 2: Volume
            "volume_trend": "UNKNOWN",
            "volume_dimension_score": 0.5,
            
            # Dimension 3: Session
            "market_session": "UNKNOWN",
            "session_dimension_score": 0.5,
            
            # Dimension 4: Volatility
            "volatility_level": "MEDIUM",
            "volatility_dimension_score": 0.5,
            
            # 4D Assessment
            "market_condition_4d": "POOR_4D",
            "market_score_4d": 0.25,
            "four_d_confidence": 0.1,
            "analysis_quality": 0.1
        }
    
    # Supporting calculation methods
    def _calculate_trend_direction(self, prices: np.ndarray) -> str:
        """คำนวณทิศทาง trend"""
        if len(prices) < 3:
            return "SIDEWAYS"
        
        first_third = np.mean(prices[:len(prices)//3])
        last_third = np.mean(prices[-len(prices)//3:])
        change_pct = ((last_third - first_third) / first_third) * 100
        
        if change_pct > 0.05:
            return "UP"
        elif change_pct < -0.05:
            return "DOWN" 
        else:
            return "SIDEWAYS"
    
    def _calculate_trend_strength(self, prices: np.ndarray) -> float:
        """คำนวณความแรงของ trend - FIXED: Handle overflow warnings"""
        try:
            if len(prices) < 5:
                return 0.0
            
            # ป้องกัน overflow
            prices = np.array(prices, dtype=np.float64)
            prices = np.clip(prices, -1e10, 1e10)
            
            # Linear regression slope with overflow protection
            x = np.arange(len(prices))
            try:
                slope = np.polyfit(x, prices, 1)[0]
            except (np.RankWarning, RuntimeWarning):
                return 0.0
            
            # Normalize slope to 0-1 scale with overflow protection
            price_range = np.max(prices) - np.min(prices)
            if price_range == 0 or np.isnan(price_range) or np.isinf(price_range):
                return 0.0
                
            normalized_slope = abs(slope) / (price_range / len(prices))
            
            # ตรวจสอบผลลัพธ์
            if np.isnan(normalized_slope) or np.isinf(normalized_slope):
                return 0.0
            
            return float(min(1.0, max(0.0, normalized_slope)))
            
        except (OverflowError, RuntimeWarning, FloatingPointError) as e:
            self.log(f"⚠️ Trend strength calculation overflow handled: {type(e).__name__}")
            return 0.0
        except Exception as e:
            self.log(f"❌ Trend strength calculation error: {e}")
            return 0.0
    
    def _calculate_trend_consistency(self, prices: np.ndarray) -> float:
        """คำนวณความสม่ำเสมอของ trend"""
        if len(prices) < 5:
            return 0.0
        
        directions = []
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                directions.append(1)
            elif prices[i] < prices[i-1]:
                directions.append(-1)
            else:
                directions.append(0)
        
        if not directions:
            return 0.0
        
        direction_sum = sum(directions)
        consistency = abs(direction_sum) / len(directions)
        return min(1.0, consistency)
    
    def _calculate_obv_trend(self, prices: np.ndarray, volumes: np.ndarray) -> str:
        """คำนวณ On-Balance Volume trend - FIXED: Handle overflow warnings"""
        try:
            if len(prices) < 2 or len(volumes) < 2:
                return "NEUTRAL"
            
            # ป้องกัน overflow
            prices = np.array(prices, dtype=np.float64)
            volumes = np.array(volumes, dtype=np.float64)
            prices = np.clip(prices, -1e10, 1e10)
            volumes = np.clip(volumes, 0, 1e10)  # volumes ไม่ติดลบ
            
            obv = [float(volumes[0])]
            for i in range(1, len(prices)):
                try:
                    if prices[i] > prices[i-1]:
                        next_obv = obv[-1] + volumes[i]
                    elif prices[i] < prices[i-1]:
                        next_obv = obv[-1] - volumes[i]
                    else:
                        next_obv = obv[-1]
                    
                    # ตรวจสอบ overflow
                    if np.isnan(next_obv) or np.isinf(next_obv):
                        next_obv = obv[-1]
                    
                    obv.append(float(np.clip(next_obv, -1e15, 1e15)))
                    
                except (OverflowError, FloatingPointError):
                    obv.append(obv[-1])
            
            # คำนวณการเปลี่ยนแปลง
            if abs(obv[0]) < 1e-10:  # ป้องกันการหารด้วยเลขเล็กมาก
                return "NEUTRAL"
            
            obv_change = (obv[-1] - obv[0]) / abs(obv[0])
            
            # ตรวจสอบผลลัพธ์
            if np.isnan(obv_change) or np.isinf(obv_change):
                return "NEUTRAL"
            
            if obv_change > 0.05:
                return "BULLISH"
            elif obv_change < -0.05:
                return "BEARISH"
            else:
                return "NEUTRAL"
                
        except (OverflowError, RuntimeWarning, FloatingPointError) as e:
            self.log(f"⚠️ OBV calculation overflow handled: {type(e).__name__}")
            return "NEUTRAL"
        except Exception as e:
            self.log(f"❌ OBV calculation error: {e}")
            return "NEUTRAL"
            
    def _calculate_volume_price_correlation(self, price_changes: np.ndarray, 
                                          volume_changes: np.ndarray) -> float:
        """คำนวณความสัมพันธ์ volume-price - FIXED: Handle overflow warnings"""
        try:
            if len(price_changes) < 2 or len(volume_changes) < 2:
                return 0.0
            
            # ป้องกัน overflow
            price_changes = np.array(price_changes, dtype=np.float64)
            volume_changes = np.array(volume_changes, dtype=np.float64)
            price_changes = np.clip(price_changes, -1e6, 1e6)
            volume_changes = np.clip(volume_changes, -1e6, 1e6)
            
            # ตรวจสอบ standard deviation เพื่อป้องกัน division by zero
            price_std = np.std(price_changes)
            volume_std = np.std(volume_changes)
            
            if price_std < 1e-10 or volume_std < 1e-10:
                return 0.0
            
            # คำนวณ correlation
            correlation = np.corrcoef(price_changes, volume_changes)[0, 1]
            
            # ตรวจสอบผลลัพธ์
            if np.isnan(correlation) or np.isinf(correlation):
                return 0.0
            
            return float(np.clip(correlation, -1.0, 1.0))
            
        except (OverflowError, RuntimeWarning, FloatingPointError) as e:
            self.log(f"⚠️ Volume-price correlation overflow handled: {type(e).__name__}")
            return 0.0
        except Exception as e:
            self.log(f"❌ Volume-price correlation error: {e}")
            return 0.0
            
    def _identify_trading_session(self, hour: int) -> Dict:
        """ระบุ trading session"""
        if 0 <= hour <= 6:
            return {
                "session": "ASIAN",
                "activity_level": "LOW", 
                "session_factor": 0.7,
                "is_major_session": False
            }
        elif 7 <= hour <= 11:
            return {
                "session": "LONDON_OPEN",
                "activity_level": "HIGH",
                "session_factor": 1.3,
                "is_major_session": True
            }
        elif 12 <= hour <= 16:
            return {
                "session": "LONDON_NY_OVERLAP",
                "activity_level": "VERY_HIGH",
                "session_factor": 1.5,
                "is_major_session": True
            }
        elif 17 <= hour <= 21:
            return {
                "session": "NEW_YORK",
                "activity_level": "HIGH",
                "session_factor": 1.2,
                "is_major_session": True
            }
        else:
            return {
                "session": "QUIET_HOURS",
                "activity_level": "VERY_LOW",
                "session_factor": 0.5,
                "is_major_session": False
            }
    
    def _get_session_volatility_profile(self, session: str) -> str:
        """ดึง volatility profile ของแต่ละ session"""
        profiles = {
            "ASIAN": "LOW",
            "LONDON_OPEN": "HIGH",
            "LONDON_NY_OVERLAP": "VERY_HIGH", 
            "NEW_YORK": "HIGH",
            "QUIET_HOURS": "VERY_LOW"
        }
        return profiles.get(session, "MEDIUM")
    
    def _detect_session_overlaps(self, hour: int) -> bool:
        """ตรวจจับการ overlap ของ session"""
        # London-NY overlap (12:00-16:00)
        return 12 <= hour <= 16
    
    def _calculate_time_activity_score(self, hour: int) -> float:
        """คำนวณคะแนน activity ตามเวลา"""
        activity_scores = {
            0: 0.2, 1: 0.1, 2: 0.1, 3: 0.1, 4: 0.2, 5: 0.3,
            6: 0.5, 7: 0.8, 8: 1.0, 9: 1.0, 10: 0.9, 11: 0.8,
            12: 1.0, 13: 1.0, 14: 1.0, 15: 1.0, 16: 0.9, 17: 0.8,
            18: 0.9, 19: 0.8, 20: 0.7, 21: 0.6, 22: 0.4, 23: 0.3
        }
        return activity_scores.get(hour, 0.5)
    
    def _calculate_session_proximity(self, hour: int) -> Dict:
        """คำนวณความใกล้เคียงกับการเปิด/ปิด session"""
        # Major session times (London: 7-17, NY: 12-22)
        london_open_distance = min(abs(hour - 7), abs(hour - (7 + 24))) if hour != 7 else 0
        london_close_distance = min(abs(hour - 17), abs(hour - (17 - 24))) if hour != 17 else 0
        ny_open_distance = min(abs(hour - 12), abs(hour - (12 + 24))) if hour != 12 else 0
        ny_close_distance = min(abs(hour - 22), abs(hour - (22 - 24))) if hour != 22 else 0
        
        return {
            "open_proximity": 1.0 / (1 + min(london_open_distance, ny_open_distance)),
            "close_proximity": 1.0 / (1 + min(london_close_distance, ny_close_distance))
        }
    
    def _calculate_level_strength(self, prices: np.ndarray, level: float, level_type: str) -> float:
        """คำนวณความแรงของ support/resistance level"""
        touches = 0
        tolerance = level * 0.001  # 0.1% tolerance
        
        for price in prices:
            if abs(price - level) <= tolerance:
                touches += 1
        
        # Normalize to 0-1 scale
        return min(1.0, touches / 5.0)
    
    def _calculate_analysis_quality(self, ohlc_data: pd.DataFrame) -> float:
        """คำนวณคุณภาพของการวิเคราะห์"""
        try:
            if ohlc_data is None or len(ohlc_data) < 20:
                return 0.2
            
            # Data completeness
            data_completeness = len(ohlc_data) / self.analysis_period
            
            # Data freshness
            last_time = ohlc_data.index[-1] 
            time_diff = (datetime.now() - last_time).total_seconds()
            freshness = max(0, 1 - time_diff / 600)  # Fresh within 10 minutes
            
            quality = (data_completeness * 0.7 + freshness * 0.3)
            return round(min(1.0, quality), 3)
            
        except Exception as e:
            return 0.5
    
    def _calculate_data_freshness(self, ohlc_data: pd.DataFrame) -> float:
        """คำนวณความใหม่ของข้อมูล"""
        try:
            if ohlc_data is None:
                return 0.0
            
            last_time = ohlc_data.index[-1]
            time_diff = (datetime.now() - last_time).total_seconds()
            
            # Fresh data = 1.0, old data approaches 0.0
            return max(0.0, 1.0 - time_diff / 1800)  # 30 minutes max age
            
        except Exception as e:
            return 0.0
    
    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """คำนวณ RSI - FIXED: Handle overflow warnings"""
        try:
            if len(prices) < period + 1:
                return 50.0
            
            # ป้องกัน overflow ด้วยการใช้ float64 และ clipping
            prices = np.array(prices, dtype=np.float64)
            prices = np.clip(prices, -1e10, 1e10)  # จำกัดขนาดค่า
            
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            # ป้องกันการหารด้วย 0 และ overflow
            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])
            
            # ตรวจสอบค่าที่ผิดปกติ
            if np.isnan(avg_gain) or np.isnan(avg_loss) or np.isinf(avg_gain) or np.isinf(avg_loss):
                return 50.0
            
            if avg_loss == 0 or avg_loss < 1e-10:  # ป้องกันการหารด้วยเลขที่เล็กมาก
                return 100.0
            
            rs = avg_gain / avg_loss
            
            # ป้องกัน overflow ใน RSI calculation
            if rs > 1e6:  # ถ้า RS ใหญ่เกินไป
                return 100.0
            
            rsi = 100 - (100 / (1 + rs))
            
            # ตรวจสอบผลลัพธ์สุดท้าย
            if np.isnan(rsi) or np.isinf(rsi):
                return 50.0
            
            return round(float(np.clip(rsi, 0, 100)), 2)
            
        except (OverflowError, RuntimeWarning, FloatingPointError) as e:
            self.log(f"⚠️ RSI calculation overflow handled: {type(e).__name__}")
            return 50.0
        except Exception as e:
            self.log(f"❌ RSI calculation error: {e}")
            return 50.0

    def _calculate_ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """คำนวณ EMA - FIXED: Handle overflow warnings"""
        try:
            if len(prices) < period:
                return np.array([])
            
            # ป้องกัน overflow ด้วยการใช้ float64 และ clipping
            prices = np.array(prices, dtype=np.float64)
            prices = np.clip(prices, -1e10, 1e10)  # จำกัดขนาดค่า
            
            alpha = 2.0 / (period + 1)
            ema = [float(prices[0])]
            
            for i in range(1, len(prices)):
                try:
                    next_ema = alpha * float(prices[i]) + (1 - alpha) * ema[-1]
                    
                    # ตรวจสอบค่าผิดปกติ
                    if np.isnan(next_ema) or np.isinf(next_ema):
                        next_ema = ema[-1]  # ใช้ค่าก่อนหน้า
                    
                    ema.append(float(np.clip(next_ema, -1e10, 1e10)))
                    
                except (OverflowError, FloatingPointError):
                    ema.append(ema[-1])  # ใช้ค่าก่อนหน้าถ้า overflow
            
            return np.array(ema, dtype=np.float64)
            
        except (OverflowError, RuntimeWarning, FloatingPointError) as e:
            self.log(f"⚠️ EMA calculation overflow handled: {type(e).__name__}")
            return np.array([])
        except Exception as e:
            self.log(f"❌ EMA calculation error: {e}")
            return np.array([])
            
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
    
    def _classify_stochastic(self, stoch: float) -> str:
        """จำแนก Stochastic condition"""
        if stoch < 20:
            return "OVERSOLD"
        elif stoch < 40:
            return "WEAK"
        elif stoch < 60:
            return "NEUTRAL"
        elif stoch < 80:
            return "STRONG"
        else:
            return "OVERBOUGHT"
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 📊 MarketAnalyzer: {message}")


# ========================================================================================
# 🧪 4D ANALYSIS TEST FUNCTIONS
# ========================================================================================

# def test_4d_market_analyzer():
#     """Test 4D Market Analyzer functionality"""
#     print("🧪 Testing 4D Market Analyzer...")
#     print("✅ 4D Comprehensive Analysis method")
#     print("✅ Trend Analysis (Dimension 1)")
#     print("✅ Volume Analysis (Dimension 2)")  
#     print("✅ Session Analysis (Dimension 3)")
#     print("✅ Volatility Analysis (Dimension 4)")
#     print("✅ 4D Scoring and Assessment")
#     print("✅ Market Condition Classification")
#     print("✅ Real-time Analysis Caching")
#     print("✅ Performance Tracking Integration")
#     print("✅ Ready for 4D AI Rule Engine")

# if __name__ == "__main__":
#     test_4d_market_analyzer()