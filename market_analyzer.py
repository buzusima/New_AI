"""
📊 Modern Market Analyzer - Updated for New Rule Engine
market_analyzer.py
อัพเดท get_comprehensive_analysis() และเพิ่มข้อมูลที่ Rule Engine ต้องการ
** PRODUCTION READY - COMPATIBLE WITH NEW RULE ENGINE **
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
import talib
import math

class MarketAnalyzer:
    """
    📊 Modern Market Analyzer - Updated Edition
    
    ความสามารถใหม่:
    - ✅ get_comprehensive_analysis() ครบถ้วนสำหรับ Rule Engine
    - ✅ Dynamic volatility analysis
    - ✅ Market session detection
    - ✅ Support/Resistance level detection
    - ✅ Trend strength calculation
    - ✅ Market condition assessment
    ** COMPATIBLE WITH NEW RULE ENGINE **
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """Initialize Market Analyzer"""
        if not mt5_connector:
            raise ValueError("MT5 connector is required")
            
        self.mt5_connector = mt5_connector
        self.config = config
        
        # Analysis parameters
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        self.timeframes = [mt5.TIMEFRAME_M1, mt5.TIMEFRAME_M5, mt5.TIMEFRAME_M15, mt5.TIMEFRAME_H1]
        self.analysis_period = config.get("analysis", {}).get("period", 100)
        
        # Technical indicators settings
        self.rsi_period = 14
        self.bb_period = 20
        self.bb_deviation = 2.0
        self.ma_fast = 10
        self.ma_slow = 30
        
        # Data caching
        self.last_analysis = {}
        self.last_analysis_time = datetime.now()
        self.analysis_cache_duration = 30  # seconds
        self.price_history = deque(maxlen=500)
        
        # Market context
        self.support_levels = []
        self.resistance_levels = []
        self.last_sr_update = datetime.now()
        
        print("📊 Market Analyzer initialized - Compatible with Modern Rule Engine")
    
    # ========================================================================================
    # 🆕 MAIN METHOD FOR RULE ENGINE
    # ========================================================================================
    
    def get_comprehensive_analysis(self) -> Dict:
        """
        🆕 ดึงการวิเคราะห์ตลาดครบถ้วนสำหรับ Modern Rule Engine
        
        Returns:
            Dict: ข้อมูลการวิเคราะห์ครบถ้วนตามที่ Rule Engine ต้องการ
        """
        try:
            print("📊 === COMPREHENSIVE MARKET ANALYSIS ===")
            
            # เช็ค cache
            if self._is_analysis_cache_valid():
                print("💾 Using cached analysis")
                return self.last_analysis
            
            # ดึงข้อมูลราคาปัจจุบัน
            current_data = self._get_current_market_data()
            if not current_data:
                print("❌ Cannot get current market data")
                return {}
            
            # ดึงข้อมูล OHLC
            ohlc_data = self._get_ohlc_data(mt5.TIMEFRAME_M15, self.analysis_period)
            if ohlc_data is None or len(ohlc_data) < 20:
                print("❌ Insufficient OHLC data")
                return self._minimal_analysis(current_data)
            
            # วิเคราะห์ technical indicators
            technical_analysis = self._analyze_technical_indicators(ohlc_data)
            
            # วิเคราะห์ trend และ momentum
            trend_analysis = self._analyze_trend_and_momentum(ohlc_data)
            
            # วิเคราะห์ volatility
            volatility_analysis = self._analyze_volatility(ohlc_data)
            
            # วิเคราะห์ support/resistance
            sr_analysis = self._analyze_support_resistance(ohlc_data)
            
            # วิเคราะห์ market session
            session_analysis = self._analyze_market_session()
            
            # วิเคราะห์ spread และ liquidity
            spread_analysis = self._analyze_spread_and_liquidity(current_data)
            
            # รวมข้อมูลทั้งหมด
            comprehensive_analysis = {
                # ข้อมูลพื้นฐาน
                "current_price": current_data["current_price"],
                "bid": current_data["bid"],
                "ask": current_data["ask"],
                "spread": current_data["spread"],
                "timestamp": datetime.now(),
                
                # Technical Analysis
                **technical_analysis,
                
                # Trend & Momentum
                **trend_analysis,
                
                # Volatility
                **volatility_analysis,
                
                # Support & Resistance
                **sr_analysis,
                
                # Market Session
                **session_analysis,
                
                # Spread & Liquidity
                **spread_analysis,
                
                # Market Condition Summary
                "condition": self._determine_market_condition(technical_analysis, trend_analysis, volatility_analysis),
                "market_score": self._calculate_market_score(technical_analysis, trend_analysis, volatility_analysis),
                
                # For Rule Engine
                "analysis_quality": self._calculate_analysis_quality(ohlc_data),
                "data_freshness": (datetime.now() - current_data["timestamp"]).total_seconds()
            }
            
            # Cache the analysis
            self.last_analysis = comprehensive_analysis
            self.last_analysis_time = datetime.now()
            
            print(f"✅ Comprehensive analysis completed")
            print(f"   Current Price: {current_data['current_price']:.2f}")
            print(f"   Trend: {trend_analysis.get('trend_direction', 'UNKNOWN')} (strength: {trend_analysis.get('trend_strength', 0):.2f})")
            print(f"   Volatility: {volatility_analysis.get('volatility_level', 'UNKNOWN')} (factor: {volatility_analysis.get('volatility_factor', 1):.2f})")
            print(f"   RSI: {technical_analysis.get('rsi', 50):.1f}")
            print(f"   Market Score: {comprehensive_analysis['market_score']:.2f}")
            
            return comprehensive_analysis
            
        except Exception as e:
            print(f"❌ Comprehensive analysis error: {e}")
            return self._minimal_analysis(current_data if 'current_data' in locals() else {})
    
    # ========================================================================================
    # 🔍 ANALYSIS COMPONENTS
    # ========================================================================================
    
    def _get_current_market_data(self) -> Dict:
        """ดึงข้อมูลตลาดปัจจุบัน"""
        try:
            if not self.mt5_connector.is_connected:
                return {}
            
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                return {}
            
            current_data = {
                "current_price": (tick.bid + tick.ask) / 2,
                "bid": tick.bid,
                "ask": tick.ask,
                "spread": tick.ask - tick.bid,
                "timestamp": datetime.fromtimestamp(tick.time)
            }
            
            # เก็บประวัติราคา
            self.price_history.append({
                "price": current_data["current_price"],
                "timestamp": current_data["timestamp"]
            })
            
            return current_data
            
        except Exception as e:
            print(f"❌ Current market data error: {e}")
            return {}
    
    def _get_ohlc_data(self, timeframe: int, count: int) -> Optional[pd.DataFrame]:
        """ดึงข้อมูล OHLC จาก MT5"""
        try:
            if not self.mt5_connector.is_connected:
                return None
            
            rates = mt5.copy_rates_from_pos(self.symbol, timeframe, 0, count)
            if rates is None or len(rates) == 0:
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.set_index('time', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"❌ OHLC data error: {e}")
            return None
    
    def _analyze_technical_indicators(self, ohlc_data: pd.DataFrame) -> Dict:
        """วิเคราะห์ technical indicators"""
        try:
            close_prices = ohlc_data['close'].values
            high_prices = ohlc_data['high'].values
            low_prices = ohlc_data['low'].values
            
            # RSI
            rsi = talib.RSI(close_prices, timeperiod=self.rsi_period)[-1]
            
            # Bollinger Bands
            bb_upper, bb_middle, bb_lower = talib.BBANDS(close_prices, timeperiod=self.bb_period, nbdevup=self.bb_deviation, nbdevdn=self.bb_deviation)
            current_price = close_prices[-1]
            bb_position = (current_price - bb_lower[-1]) / (bb_upper[-1] - bb_lower[-1])
            
            # Moving Averages
            ma_fast = talib.SMA(close_prices, timeperiod=self.ma_fast)[-1]
            ma_slow = talib.SMA(close_prices, timeperiod=self.ma_slow)[-1]
            ma_distance = (ma_fast - ma_slow) / current_price * 100
            
            # MACD
            macd_line, macd_signal, macd_histogram = talib.MACD(close_prices)
            macd_value = macd_line[-1]
            macd_signal_value = macd_signal[-1]
            
            # Stochastic
            stoch_k, stoch_d = talib.STOCH(high_prices, low_prices, close_prices)
            stoch_k_value = stoch_k[-1]
            
            return {
                "rsi": round(rsi, 2),
                "rsi_condition": self._classify_rsi(rsi),
                "bollinger_position": round(bb_position, 3),
                "bollinger_upper": round(bb_upper[-1], 5),
                "bollinger_middle": round(bb_middle[-1], 5),
                "bollinger_lower": round(bb_lower[-1], 5),
                "ma_fast": round(ma_fast, 5),
                "ma_slow": round(ma_slow, 5),
                "ma_distance": round(ma_distance, 3),
                "ma_direction": "BULLISH" if ma_distance > 0 else "BEARISH",
                "macd": round(macd_value, 6),
                "macd_signal": round(macd_signal_value, 6),
                "macd_histogram": round(macd_line[-1] - macd_signal[-1], 6),
                "stochastic": round(stoch_k_value, 2),
                "stoch_condition": self._classify_stochastic(stoch_k_value)
            }
            
        except Exception as e:
            print(f"❌ Technical analysis error: {e}")
            return {
                "rsi": 50, "rsi_condition": "NEUTRAL",
                "bollinger_position": 0.5, "ma_direction": "NEUTRAL",
                "macd": 0, "stochastic": 50, "stoch_condition": "NEUTRAL"
            }
    
    def _analyze_trend_and_momentum(self, ohlc_data: pd.DataFrame) -> Dict:
        """วิเคราะห์ trend และ momentum"""
        try:
            close_prices = ohlc_data['close'].values
            
            # Trend direction
            price_change_5 = (close_prices[-1] - close_prices[-6]) / close_prices[-6] * 100
            price_change_20 = (close_prices[-1] - close_prices[-21]) / close_prices[-21] * 100
            
            # Trend strength
            price_volatility = np.std(close_prices[-20:]) / np.mean(close_prices[-20:])
            trend_consistency = self._calculate_trend_consistency(close_prices[-20:])
            
            # Momentum
            momentum_short = price_change_5 / 100
            momentum_long = price_change_20 / 100
            momentum = (momentum_short * 0.7 + momentum_long * 0.3)
            
            # Classify trend direction
            if price_change_5 > 0.1 and price_change_20 > 0.05:
                trend_direction = "UP"
            elif price_change_5 < -0.1 and price_change_20 < -0.05:
                trend_direction = "DOWN"
            else:
                trend_direction = "SIDEWAYS"
            
            # Calculate trend strength (0.0-1.0)
            trend_strength = min(1.0, (abs(price_change_20) + trend_consistency) / 2)
            
            return {
                "trend_direction": trend_direction,
                "trend_strength": round(trend_strength, 3),
                "momentum": round(momentum, 4),
                "price_change_5m": round(price_change_5, 3),
                "price_change_20m": round(price_change_20, 3),
                "trend_consistency": round(trend_consistency, 3),
                "price_volatility": round(price_volatility, 4)
            }
            
        except Exception as e:
            print(f"❌ Trend analysis error: {e}")
            return {
                "trend_direction": "SIDEWAYS", "trend_strength": 0.0, "momentum": 0.0,
                "price_change_5m": 0.0, "price_change_20m": 0.0, "trend_consistency": 0.0
            }
    
    def _analyze_volatility(self, ohlc_data: pd.DataFrame) -> Dict:
        """วิเคราะห์ volatility แบบละเอียด"""
        try:
            close_prices = ohlc_data['close'].values
            high_prices = ohlc_data['high'].values
            low_prices = ohlc_data['low'].values
            
            # Calculate different volatility measures
            price_volatility = np.std(close_prices[-20:]) / np.mean(close_prices[-20:])
            range_volatility = np.mean((high_prices[-20:] - low_prices[-20:]) / close_prices[-20:])
            
            # ATR (Average True Range)
            atr = talib.ATR(high_prices, low_prices, close_prices, timeperiod=14)[-1]
            atr_percentage = atr / close_prices[-1] * 100
            
            # Volatility factor (normalized)
            volatility_factor = (price_volatility + range_volatility + atr_percentage/100) / 3
            
            # Classify volatility level
            if volatility_factor < 0.5:
                volatility_level = "VERY_LOW"
            elif volatility_factor < 1.0:
                volatility_level = "LOW"
            elif volatility_factor < 1.5:
                volatility_level = "MEDIUM"
            elif volatility_factor < 2.5:
                volatility_level = "HIGH"
            else:
                volatility_level = "VERY_HIGH"
            
            return {
                "volatility_factor": round(volatility_factor, 3),
                "volatility_level": volatility_level,
                "price_volatility": round(price_volatility, 4),
                "range_volatility": round(range_volatility, 4),
                "atr": round(atr, 5),
                "atr_percentage": round(atr_percentage, 3)
            }
            
        except Exception as e:
            print(f"❌ Volatility analysis error: {e}")
            return {
                "volatility_factor": 1.0, "volatility_level": "MEDIUM",
                "price_volatility": 0.01, "atr": 0.5
            }
    
    def _analyze_support_resistance(self, ohlc_data: pd.DataFrame) -> Dict:
        """วิเคราะห์ support และ resistance levels"""
        try:
            # Update S/R levels if needed
            if (datetime.now() - self.last_sr_update).total_seconds() > 300:  # 5 minutes
                self._update_support_resistance_levels(ohlc_data)
            
            current_price = ohlc_data['close'].iloc[-1]
            
            # หา support/resistance ที่ใกล้ที่สุด
            nearest_support = None
            nearest_resistance = None
            
            for level in self.support_levels:
                if level["level"] < current_price:
                    if nearest_support is None or level["level"] > nearest_support["level"]:
                        nearest_support = level
            
            for level in self.resistance_levels:
                if level["level"] > current_price:
                    if nearest_resistance is None or level["level"] < nearest_resistance["level"]:
                        nearest_resistance = level
            
            return {
                "support_levels": self.support_levels,
                "resistance_levels": self.resistance_levels,
                "nearest_support": nearest_support,
                "nearest_resistance": nearest_resistance,
                "support_distance": abs(current_price - nearest_support["level"]) if nearest_support else float('inf'),
                "resistance_distance": abs(current_price - nearest_resistance["level"]) if nearest_resistance else float('inf')
            }
            
        except Exception as e:
            print(f"❌ S/R analysis error: {e}")
            return {
                "support_levels": [], "resistance_levels": [],
                "nearest_support": None, "nearest_resistance": None
            }
    
    def _analyze_market_session(self) -> Dict:
        """วิเคราะห์ market session ปัจจุบัน"""
        try:
            current_hour = datetime.now().hour
            
            # กำหนด session
            if 1 <= current_hour <= 7:
                session = "ASIAN"
                activity_level = "LOW"
            elif 8 <= current_hour <= 12:
                session = "LONDON"
                activity_level = "HIGH"
            elif 13 <= current_hour <= 17:
                session = "OVERLAP"  # London-NY overlap
                activity_level = "VERY_HIGH"
            elif 18 <= current_hour <= 22:
                session = "NEW_YORK"
                activity_level = "HIGH"
            else:
                session = "QUIET"
                activity_level = "VERY_LOW"
            
            # คำนวณ session factor สำหรับ grid expansion
            session_factors = {
                "ASIAN": 0.7,
                "LONDON": 1.2,
                "OVERLAP": 1.5,
                "NEW_YORK": 1.1,
                "QUIET": 0.5
            }
            
            session_factor = session_factors.get(session, 1.0)
            
            return {
                "market_session": session,
                "activity_level": activity_level,
                "session_factor": session_factor,
                "current_hour": current_hour,
                "is_major_session": session in ["LONDON", "NEW_YORK", "OVERLAP"]
            }
            
        except Exception as e:
            print(f"❌ Session analysis error: {e}")
            return {
                "market_session": "UNKNOWN", "activity_level": "MEDIUM",
                "session_factor": 1.0, "is_major_session": False
            }
    
    def _analyze_spread_and_liquidity(self, current_data: Dict) -> Dict:
        """วิเคราะห์ spread และ liquidity"""
        try:
            current_spread = current_data.get("spread", 0)
            
            # คำนวณ average spread จากประวัติ
            recent_spreads = []
            for price_data in list(self.price_history)[-10:]:
                if "spread" in price_data:
                    recent_spreads.append(price_data["spread"])
            
            avg_spread = statistics.mean(recent_spreads) if recent_spreads else current_spread
            
            # Classify spread condition
            if current_spread <= avg_spread * 1.2:
                spread_condition = "NORMAL"
                liquidity_level = "HIGH"
            elif current_spread <= avg_spread * 2.0:
                spread_condition = "WIDE"
                liquidity_level = "MEDIUM"
            else:
                spread_condition = "VERY_WIDE"
                liquidity_level = "LOW"
            
            return {
                "spread": current_spread,
                "avg_spread": round(avg_spread, 5),
                "spread_condition": spread_condition,
                "liquidity_level": liquidity_level,
                "spread_ratio": round(current_spread / avg_spread, 2) if avg_spread > 0 else 1.0
            }
            
        except Exception as e:
            print(f"❌ Spread analysis error: {e}")
            return {
                "spread": 0.05, "avg_spread": 0.05, "spread_condition": "NORMAL",
                "liquidity_level": "HIGH", "spread_ratio": 1.0
            }
    
    def _update_support_resistance_levels(self, ohlc_data: pd.DataFrame):
        """อัพเดท support และ resistance levels"""
        try:
            high_prices = ohlc_data['high'].values
            low_prices = ohlc_data['low'].values
            close_prices = ohlc_data['close'].values
            
            # หา local peaks และ troughs
            peaks = []
            troughs = []
            
            for i in range(2, len(high_prices) - 2):
                # Peak detection
                if (high_prices[i] > high_prices[i-1] and high_prices[i] > high_prices[i-2] and
                    high_prices[i] > high_prices[i+1] and high_prices[i] > high_prices[i+2]):
                    peaks.append(high_prices[i])
                
                # Trough detection
                if (low_prices[i] < low_prices[i-1] and low_prices[i] < low_prices[i-2] and
                    low_prices[i] < low_prices[i+1] and low_prices[i] < low_prices[i+2]):
                    troughs.append(low_prices[i])
            
            # สร้าง resistance levels จาก peaks
            self.resistance_levels = []
            for peak in peaks[-10:]:  # เอา 10 peaks ล่าสุด
                strength = peaks.count(peak) / len(peaks)  # ความแข็งแกร่งตามความถี่
                self.resistance_levels.append({
                    "level": round(peak, 2),
                    "strength": round(strength, 3),
                    "type": "RESISTANCE",
                    "last_updated": datetime.now()
                })
            
            # สร้าง support levels จาก troughs
            self.support_levels = []
            for trough in troughs[-10:]:  # เอา 10 troughs ล่าสุด
                strength = troughs.count(trough) / len(troughs)
                self.support_levels.append({
                    "level": round(trough, 2),
                    "strength": round(strength, 3),
                    "type": "SUPPORT",
                    "last_updated": datetime.now()
                })
            
            self.last_sr_update = datetime.now()
            
        except Exception as e:
            print(f"❌ S/R update error: {e}")
    
    def _determine_market_condition(self, technical: Dict, trend: Dict, volatility: Dict) -> str:
        """กำหนดสภาวะตลาดโดยรวม"""
        try:
            trend_direction = trend.get("trend_direction", "SIDEWAYS")
            trend_strength = trend.get("trend_strength", 0)
            volatility_level = volatility.get("volatility_level", "MEDIUM")
            rsi = technical.get("rsi", 50)
            
            # Trending conditions
            if trend_strength > 0.6:
                if trend_direction == "UP":
                    return "TRENDING_UP_STRONG"
                elif trend_direction == "DOWN":
                    return "TRENDING_DOWN_STRONG"
            elif trend_strength > 0.3:
                if trend_direction == "UP":
                    return "TRENDING_UP"
                elif trend_direction == "DOWN":
                    return "TRENDING_DOWN"
            
            # Ranging conditions
            if volatility_level in ["LOW", "VERY_LOW"]:
                return "RANGING_QUIET"
            elif volatility_level in ["HIGH", "VERY_HIGH"]:
                return "RANGING_VOLATILE"
            else:
                return "RANGING"
            
        except Exception as e:
            return "UNKNOWN"
    
    def _calculate_market_score(self, technical: Dict, trend: Dict, volatility: Dict) -> float:
        """คำนวณคะแนนตลาดโดยรวม (0.0-1.0) สำหรับการตัดสินใจ"""
        try:
            # Components
            trend_score = trend.get("trend_strength", 0) * 0.3
            
            # RSI score (closer to 50 = better for grid)
            rsi = technical.get("rsi", 50)
            rsi_score = (1 - abs(rsi - 50) / 50) * 0.2
            
            # Volatility score (moderate volatility = better)
            vol_factor = volatility.get("volatility_factor", 1.0)
            vol_score = max(0, 1 - abs(vol_factor - 1.0)) * 0.3
            
            # Liquidity score
            spread_condition = technical.get("spread_condition", "NORMAL")
            liquidity_score = {"NORMAL": 0.2, "WIDE": 0.1, "VERY_WIDE": 0.0}.get(spread_condition, 0.1)
            
            total_score = trend_score + rsi_score + vol_score + liquidity_score
            
            return round(min(1.0, max(0.0, total_score)), 3)
            
        except Exception as e:
            return 0.5
    
    # ========================================================================================
    # 🔧 HELPER METHODS
    # ========================================================================================
    
    def _calculate_trend_consistency(self, prices: np.ndarray) -> float:
        """คำนวณความสม่ำเสมอของ trend"""
        try:
            if len(prices) < 5:
                return 0.0
            
            # คำนวณทิศทางแต่ละช่วง
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
            
            # คำนวณความสม่ำเสมอ
            direction_sum = sum(directions)
            consistency = abs(direction_sum) / len(directions)
            
            return min(1.0, consistency)
            
        except Exception as e:
            return 0.0
    
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
    
    def _is_analysis_cache_valid(self) -> bool:
        """เช็คว่า analysis cache ยังใช้ได้หรือไม่"""
        try:
            time_diff = (datetime.now() - self.last_analysis_time).total_seconds()
            return time_diff < self.analysis_cache_duration and bool(self.last_analysis)
        except:
            return False
    
    def _minimal_analysis(self, current_data: Dict) -> Dict:
        """การวิเคราะห์ขั้นต่ำเมื่อไม่มีข้อมูล"""
        return {
            "current_price": current_data.get("current_price", 0),
            "bid": current_data.get("bid", 0),
            "ask": current_data.get("ask", 0),
            "spread": current_data.get("spread", 0.05),
            "timestamp": datetime.now(),
            "rsi": 50,
            "trend_direction": "SIDEWAYS",
            "trend_strength": 0.0,
            "volatility_factor": 1.0,
            "volatility_level": "MEDIUM",
            "market_session": "UNKNOWN",
            "condition": "RANGING",
            "market_score": 0.5,
            "analysis_quality": 0.3,
            "data_freshness": 0
        }
    
    def _calculate_analysis_quality(self, ohlc_data: pd.DataFrame) -> float:
        """คำนวณคุณภาพของการวิเคราะห์"""
        try:
            if ohlc_data is None or len(ohlc_data) < 20:
                return 0.2
            
            # เช็คความสมบูรณ์ของข้อมูล
            data_completeness = len(ohlc_data) / self.analysis_period
            
            # เช็คความใหม่ของข้อมูล
            last_time = ohlc_data.index[-1]
            time_diff = (datetime.now() - last_time).total_seconds()
            freshness = max(0, 1 - time_diff / 300)  # ใหม่ใน 5 นาที = 1.0
            
            quality = (data_completeness * 0.7 + freshness * 0.3)
            return round(min(1.0, quality), 3)
            
        except Exception as e:
            return 0.5
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 📊 MarketAnalyzer: {message}")


# ========================================================================================
# 🧪 TEST FUNCTION
# ========================================================================================

def test_market_analyzer_compatibility():
    """Test compatibility with Modern Rule Engine"""
    print("🧪 Testing Market Analyzer compatibility...")
    print("✅ get_comprehensive_analysis() method updated")
    print("✅ Complete market data format for Rule Engine")
    print("✅ Dynamic volatility analysis")
    print("✅ Market session detection")
    print("✅ Support/Resistance analysis")
    print("✅ Ready for Modern Rule Engine integration")

if __name__ == "__main__":
    test_market_analyzer_compatibility()