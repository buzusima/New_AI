"""
📊 Modern Market Analyzer
market_analyzer.py
การวิเคราะห์ตลาดแบบครอบคลุม สำหรับ Rule-based Trading System
รองรับการวิเคราะห์เทคนิค, การตรวจจับ patterns และ context awareness
"""

import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import statistics
from collections import deque
import MetaTrader5 as mt5

class MarketCondition(Enum):
    """สภาวะตลาด"""
    TRENDING_UP = "TRENDING_UP"
    TRENDING_DOWN = "TRENDING_DOWN"
    RANGING = "RANGING"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    UNKNOWN = "UNKNOWN"

class TradingSession(Enum):
    """เซสชันการเทรด"""
    ASIAN = "ASIAN"
    LONDON = "LONDON"
    NEW_YORK = "NEW_YORK"
    OVERLAP_LONDON_NY = "OVERLAP_LONDON_NY"
    QUIET = "QUIET"

@dataclass
class SupportResistanceLevel:
    """ระดับ Support/Resistance"""
    level: float
    strength: int
    touches: int
    last_touch: datetime
    level_type: str  # "support" or "resistance"

@dataclass
class MarketAnalysisResult:
    """ผลการวิเคราะห์ตลาด"""
    timestamp: datetime
    current_price: float
    condition: MarketCondition
    trend_strength: float
    volatility_factor: float
    rsi: float
    bollinger_position: float
    support_levels: List[SupportResistanceLevel]
    resistance_levels: List[SupportResistanceLevel]
    atr: float
    volume_surge: bool
    session: TradingSession
    price_deviation_from_mean: float
    recent_price_movement: float
    market_momentum: float
    confidence_score: float

class MarketAnalyzer:
    """
    📊 Modern Market Analyzer
    
    ความสามารถ:
    - Technical indicators (RSI, MACD, Bollinger Bands, ATR)
    - Support/Resistance detection
    - Trend analysis
    - Volatility measurement
    - Session detection
    - Volume analysis
    - Market context awareness
    """
    
    def __init__(self, mt5_connector, config: Dict):
        """
        Initialize Market Analyzer
        
        Args:
            mt5_connector: MT5 connection object
            config: Configuration settings
        """
        self.mt5_connector = mt5_connector
        self.config = config
        self.symbol = config.get("trading", {}).get("symbol", "XAUUSD")
        
        # Analysis parameters
        self.rsi_period = 14
        self.bollinger_period = 20
        self.bollinger_deviation = 2.0
        self.atr_period = 14
        self.trend_period = 50
        self.support_resistance_lookback = 100
        
        # Data storage
        self.price_history = deque(maxlen=200)
        self.volume_history = deque(maxlen=50)
        self.analysis_cache = {}
        self.cache_timeout = 30  # seconds
        
        # Support/Resistance tracking
        self.support_levels = []
        self.resistance_levels = []
        self.last_sr_update = datetime.min
        
        print("📊 Market Analyzer initialized")
        print(f"   Symbol: {self.symbol}")
        print(f"   RSI Period: {self.rsi_period}")
        print(f"   Bollinger Period: {self.bollinger_period}")
        print(f"   ATR Period: {self.atr_period}")
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive market analysis
        
        Returns:
            Dictionary with complete market analysis
        """
        try:
            # Check cache first
            cache_key = "comprehensive_analysis"
            if self._is_cache_valid(cache_key):
                return self.analysis_cache[cache_key]["data"]
            
            # Get market data
            market_data = self._get_market_data()
            if not market_data:
                return self._get_default_analysis()
            
            # Perform analysis
            analysis_result = self._perform_comprehensive_analysis(market_data)
            
            # Cache result
            self.analysis_cache[cache_key] = {
                "data": analysis_result,
                "timestamp": datetime.now()
            }
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Comprehensive analysis error: {e}")
            return self._get_default_analysis()
    
    def _get_market_data(self) -> Optional[Dict]:
        """Get market data from MT5"""
        try:
            if not self.mt5_connector.is_connected:
                return None
            
            # Get current price
            tick = mt5.symbol_info_tick(self.symbol)
            if not tick:
                return None
            
            current_price = (tick.bid + tick.ask) / 2
            
            # Get historical data
            rates = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M5, 0, 200)
            if rates is None or len(rates) < 50:
                return None
            
            # Convert to lists for easier processing
            prices = [rate[4] for rate in rates]  # Close prices
            highs = [rate[2] for rate in rates]   # High prices
            lows = [rate[3] for rate in rates]    # Low prices
            volumes = [rate[5] for rate in rates] # Tick volumes
            times = [datetime.fromtimestamp(rate[0]) for rate in rates]
            
            # Update price history
            self.price_history.extend(prices[-50:])  # Keep recent prices
            self.volume_history.extend(volumes[-50:])
            
            return {
                "current_price": current_price,
                "prices": prices,
                "highs": highs,
                "lows": lows,
                "volumes": volumes,
                "times": times,
                "bid": tick.bid,
                "ask": tick.ask,
                "spread": tick.ask - tick.bid
            }
            
        except Exception as e:
            print(f"❌ Market data error: {e}")
            return None
    
    def _perform_comprehensive_analysis(self, market_data: Dict) -> Dict[str, Any]:
        """Perform comprehensive market analysis"""
        try:
            prices = market_data["prices"]
            highs = market_data["highs"]
            lows = market_data["lows"]
            volumes = market_data["volumes"]
            current_price = market_data["current_price"]
            
            # Technical indicators
            rsi = self._calculate_rsi(prices)
            bollinger_bands = self._calculate_bollinger_bands(prices)
            atr = self._calculate_atr(highs, lows, prices)
            macd = self._calculate_macd(prices)
            
            # Market condition analysis
            trend_analysis = self._analyze_trend(prices)
            volatility_analysis = self._analyze_volatility(prices, atr)
            
            # Support/Resistance levels
            self._update_support_resistance_levels(highs, lows, current_price)
            
            # Session detection
            current_session = self._detect_trading_session()
            
            # Volume analysis
            volume_analysis = self._analyze_volume(volumes)
            
            # Market momentum
            momentum = self._calculate_momentum(prices)
            
            # Price deviation from mean
            price_deviation = self._calculate_price_deviation(prices, current_price)
            
            # Recent price movement
            recent_movement = self._calculate_recent_movement(prices)
            
            # Overall market condition
            market_condition = self._determine_market_condition(
                trend_analysis, volatility_analysis, rsi, momentum
            )
            
            # Confidence score
            confidence = self._calculate_analysis_confidence(
                len(prices), volatility_analysis["factor"], trend_analysis["strength"]
            )
            
            # Compile comprehensive result
            return {
                "timestamp": datetime.now(),
                "current_price": current_price,
                "condition": market_condition,
                "trend_strength": trend_analysis["strength"],
                "trend_direction": trend_analysis["direction"],
                "volatility_factor": volatility_analysis["factor"],
                "volatility_level": volatility_analysis["level"],
                "rsi": rsi,
                "rsi_signal": self._interpret_rsi(rsi),
                "bollinger_position": bollinger_bands["position"],
                "bollinger_squeeze": bollinger_bands["squeeze"],
                "support_levels": [self._level_to_dict(level) for level in self.support_levels],
                "resistance_levels": [self._level_to_dict(level) for level in self.resistance_levels],
                "atr": atr,
                "avg_atr": np.mean([self._calculate_atr(highs[i-14:i], lows[i-14:i], prices[i-14:i]) 
                                  for i in range(14, len(prices), 5)]) if len(prices) > 20 else atr,
                "macd": macd,
                "volume_surge": volume_analysis["surge"],
                "volume_trend": volume_analysis["trend"],
                "session": current_session,
                "price_deviation_from_mean": price_deviation,
                "recent_price_movement": recent_movement,
                "market_momentum": momentum,
                "confidence_score": confidence,
                "spread": market_data["spread"],
                "bid": market_data["bid"],
                "ask": market_data["ask"]
            }
            
        except Exception as e:
            print(f"❌ Analysis error: {e}")
            return self._get_default_analysis()
    
    def _calculate_rsi(self, prices: List[float], period: int = None) -> float:
        """Calculate RSI indicator"""
        try:
            if period is None:
                period = self.rsi_period
                
            if len(prices) < period + 1:
                return 50.0  # Neutral RSI
            
            deltas = np.diff(prices)
            gains = np.where(deltas > 0, deltas, 0)
            losses = np.where(deltas < 0, -deltas, 0)
            
            avg_gain = np.mean(gains[-period:])
            avg_loss = np.mean(losses[-period:])
            
            if avg_loss == 0:
                return 100.0
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return round(rsi, 2)
            
        except Exception as e:
            print(f"❌ RSI calculation error: {e}")
            return 50.0
    
    def _calculate_bollinger_bands(self, prices: List[float]) -> Dict[str, float]:
        """Calculate Bollinger Bands"""
        try:
            if len(prices) < self.bollinger_period:
                return {"position": 0.5, "squeeze": False, "upper": 0, "lower": 0, "middle": 0}
            
            recent_prices = prices[-self.bollinger_period:]
            middle = np.mean(recent_prices)
            std_dev = np.std(recent_prices)
            
            upper = middle + (self.bollinger_deviation * std_dev)
            lower = middle - (self.bollinger_deviation * std_dev)
            
            current_price = prices[-1]
            
            # Position within bands (0 = lower band, 1 = upper band)
            if upper != lower:
                position = (current_price - lower) / (upper - lower)
            else:
                position = 0.5
            
            # Bollinger squeeze detection
            band_width = (upper - lower) / middle if middle > 0 else 0
            avg_band_width = np.mean([
                (np.mean(prices[i-self.bollinger_period:i]) + 
                 2 * np.std(prices[i-self.bollinger_period:i]) - 
                 (np.mean(prices[i-self.bollinger_period:i]) - 
                  2 * np.std(prices[i-self.bollinger_period:i]))) / np.mean(prices[i-self.bollinger_period:i])
                for i in range(self.bollinger_period, len(prices), 5)
            ]) if len(prices) > self.bollinger_period * 2 else band_width
            
            squeeze = band_width < avg_band_width * 0.8
            
            return {
                "position": max(0, min(1, position)),
                "squeeze": squeeze,
                "upper": upper,
                "lower": lower,
                "middle": middle,
                "width": band_width
            }
            
        except Exception as e:
            print(f"❌ Bollinger Bands error: {e}")
            return {"position": 0.5, "squeeze": False, "upper": 0, "lower": 0, "middle": 0}
    
    def _calculate_atr(self, highs: List[float], lows: List[float], closes: List[float]) -> float:
        """Calculate Average True Range"""
        try:
            if len(highs) < self.atr_period or len(lows) < self.atr_period or len(closes) < self.atr_period:
                return 0.0
            
            true_ranges = []
            for i in range(1, len(closes)):
                tr = max(
                    highs[i] - lows[i],
                    abs(highs[i] - closes[i-1]),
                    abs(lows[i] - closes[i-1])
                )
                true_ranges.append(tr)
            
            if len(true_ranges) >= self.atr_period:
                atr = np.mean(true_ranges[-self.atr_period:])
                return round(atr, 5)
            
            return 0.0
            
        except Exception as e:
            print(f"❌ ATR calculation error: {e}")
            return 0.0
    
    def _calculate_macd(self, prices: List[float]) -> Dict[str, float]:
        """Calculate MACD indicator"""
        try:
            if len(prices) < 26:
                return {"macd": 0, "signal": 0, "histogram": 0}
            
            # Calculate EMAs
            ema12 = self._calculate_ema(prices, 12)
            ema26 = self._calculate_ema(prices, 26)
            
            macd_line = ema12 - ema26
            
            # Calculate signal line (9-period EMA of MACD)
            if len(prices) >= 35:  # Need enough data for signal line
                macd_values = []
                for i in range(26, len(prices)):
                    ema12_i = self._calculate_ema(prices[:i+1], 12)
                    ema26_i = self._calculate_ema(prices[:i+1], 26)
                    macd_values.append(ema12_i - ema26_i)
                
                signal_line = self._calculate_ema(macd_values, 9)
                histogram = macd_line - signal_line
            else:
                signal_line = 0
                histogram = 0
            
            return {
                "macd": round(macd_line, 5),
                "signal": round(signal_line, 5),
                "histogram": round(histogram, 5)
            }
            
        except Exception as e:
            print(f"❌ MACD calculation error: {e}")
            return {"macd": 0, "signal": 0, "histogram": 0}
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        try:
            if len(prices) < period:
                return np.mean(prices) if prices else 0
            
            multiplier = 2 / (period + 1)
            ema = prices[0]
            
            for price in prices[1:]:
                ema = (price * multiplier) + (ema * (1 - multiplier))
            
            return ema
            
        except Exception as e:
            print(f"❌ EMA calculation error: {e}")
            return 0.0
    
    def _analyze_trend(self, prices: List[float]) -> Dict[str, Any]:
        """Analyze market trend"""
        try:
            if len(prices) < self.trend_period:
                return {"direction": "SIDEWAYS", "strength": 0.0}
            
            recent_prices = prices[-self.trend_period:]
            
            # Linear regression for trend
            x = np.arange(len(recent_prices))
            slope, intercept = np.polyfit(x, recent_prices, 1)
            
            # Trend strength based on R-squared
            y_pred = slope * x + intercept
            ss_res = np.sum((recent_prices - y_pred) ** 2)
            ss_tot = np.sum((recent_prices - np.mean(recent_prices)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            # Normalize slope for strength calculation
            price_range = max(recent_prices) - min(recent_prices)
            normalized_slope = abs(slope) / (price_range / len(recent_prices)) if price_range > 0 else 0
            
            strength = min(1.0, r_squared * normalized_slope * 10)
            
            # Determine direction
            if slope > 0 and strength > 0.3:
                direction = "UP"
            elif slope < 0 and strength > 0.3:
                direction = "DOWN"
            else:
                direction = "SIDEWAYS"
            
            return {
                "direction": direction,
                "strength": round(strength, 3),
                "slope": round(slope, 5),
                "r_squared": round(r_squared, 3)
            }
            
        except Exception as e:
            print(f"❌ Trend analysis error: {e}")
            return {"direction": "SIDEWAYS", "strength": 0.0}
    
    def _analyze_volatility(self, prices: List[float], atr: float) -> Dict[str, Any]:
        """Analyze market volatility"""
        try:
            if len(prices) < 20:
                return {"factor": 1.0, "level": "NORMAL"}
            
            # Calculate recent volatility
            recent_prices = prices[-20:]
            price_changes = [abs(recent_prices[i] - recent_prices[i-1]) 
                           for i in range(1, len(recent_prices))]
            
            current_volatility = np.mean(price_changes) if price_changes else 0
            
            # Historical volatility for comparison
            if len(prices) >= 50:
                historical_changes = [abs(prices[i] - prices[i-1]) for i in range(1, len(prices))]
                historical_volatility = np.mean(historical_changes)
            else:
                historical_volatility = current_volatility
            
            # Volatility factor
            if historical_volatility > 0:
                volatility_factor = current_volatility / historical_volatility
            else:
                volatility_factor = 1.0
            
            # Volatility level classification
            if volatility_factor > 2.0:
                level = "VERY_HIGH"
            elif volatility_factor > 1.5:
                level = "HIGH"
            elif volatility_factor > 0.5:
                level = "NORMAL"
            else:
                level = "LOW"
            
            return {
                "factor": round(volatility_factor, 3),
                "level": level,
                "current": round(current_volatility, 5),
                "historical": round(historical_volatility, 5),
                "atr_ratio": round(atr / historical_volatility, 3) if historical_volatility > 0 else 1.0
            }
            
        except Exception as e:
            print(f"❌ Volatility analysis error: {e}")
            return {"factor": 1.0, "level": "NORMAL"}
    
    def _update_support_resistance_levels(self, highs: List[float], lows: List[float], current_price: float):
        """Update support and resistance levels"""
        try:
            # Only update periodically to avoid overprocessing
            if datetime.now() - self.last_sr_update < timedelta(minutes=5):
                return
            
            if len(highs) < self.support_resistance_lookback or len(lows) < self.support_resistance_lookback:
                return
            
            # Find potential levels
            resistance_candidates = self._find_resistance_levels(highs[-self.support_resistance_lookback:])
            support_candidates = self._find_support_levels(lows[-self.support_resistance_lookback:])
            
            # Filter and strengthen levels
            self.resistance_levels = self._filter_and_strengthen_levels(
                resistance_candidates, current_price, "resistance"
            )
            self.support_levels = self._filter_and_strengthen_levels(
                support_candidates, current_price, "support"
            )
            
            self.last_sr_update = datetime.now()
            
        except Exception as e:
            print(f"❌ Support/Resistance update error: {e}")
    
    def _find_resistance_levels(self, highs: List[float]) -> List[float]:
        """Find resistance levels from highs"""
        try:
            levels = []
            
            # Find local maxima
            for i in range(2, len(highs) - 2):
                if (highs[i] > highs[i-1] and highs[i] > highs[i-2] and
                    highs[i] > highs[i+1] and highs[i] > highs[i+2]):
                    levels.append(highs[i])
            
            # Group similar levels
            grouped_levels = []
            for level in sorted(levels):
                added = False
                for group_level in grouped_levels:
                    if abs(level - group_level) < level * 0.001:  # 0.1% tolerance
                        added = True
                        break
                if not added:
                    grouped_levels.append(level)
            
            return grouped_levels[-10:]  # Keep top 10 levels
            
        except Exception as e:
            print(f"❌ Resistance level detection error: {e}")
            return []
    
    def _find_support_levels(self, lows: List[float]) -> List[float]:
        """Find support levels from lows"""
        try:
            levels = []
            
            # Find local minima
            for i in range(2, len(lows) - 2):
                if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and
                    lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                    levels.append(lows[i])
            
            # Group similar levels
            grouped_levels = []
            for level in sorted(levels):
                added = False
                for group_level in grouped_levels:
                    if abs(level - group_level) < level * 0.001:  # 0.1% tolerance
                        added = True
                        break
                if not added:
                    grouped_levels.append(level)
            
            return grouped_levels[-10:]  # Keep top 10 levels
            
        except Exception as e:
            print(f"❌ Support level detection error: {e}")
            return []
    
    def _filter_and_strengthen_levels(self, candidates: List[float], current_price: float, 
                                    level_type: str) -> List[SupportResistanceLevel]:
        """Filter and create strengthened levels"""
        try:
            levels = []
            
            for candidate in candidates:
                # Skip levels too far from current price
                distance_ratio = abs(candidate - current_price) / current_price
                if distance_ratio > 0.05:  # More than 5% away
                    continue
                
                # Calculate strength (simplified)
                strength = min(5, max(1, int(3 + np.random.normal(0, 1))))  # Random strength for now
                
                level = SupportResistanceLevel(
                    level=candidate,
                    strength=strength,
                    touches=1,  # Simplified
                    last_touch=datetime.now(),
                    level_type=level_type
                )
                levels.append(level)
            
            # Sort by strength and return top levels
            levels.sort(key=lambda x: x.strength, reverse=True)
            return levels[:5]  # Keep top 5 levels
            
        except Exception as e:
            print(f"❌ Level filtering error: {e}")
            return []
    
    def _detect_trading_session(self) -> TradingSession:
        """Detect current trading session"""
        try:
            now = datetime.now()
            hour = now.hour
            
            # London session: 8:00-16:00 GMT
            # New York session: 13:00-21:00 GMT
            # Asian session: 22:00-06:00 GMT
            
            if 13 <= hour < 16:  # London-NY overlap
                return TradingSession.OVERLAP_LONDON_NY
            elif 8 <= hour < 16:  # London session
                return TradingSession.LONDON
            elif 13 <= hour < 21:  # New York session
                return TradingSession.NEW_YORK
            elif hour >= 22 or hour < 6:  # Asian session
                return TradingSession.ASIAN
            else:
                return TradingSession.QUIET
                
        except Exception as e:
            print(f"❌ Session detection error: {e}")
            return TradingSession.QUIET
    
    def _analyze_volume(self, volumes: List[float]) -> Dict[str, Any]:
        """Analyze volume patterns"""
        try:
            if len(volumes) < 10:
                return {"surge": False, "trend": "NORMAL"}
            
            recent_volume = np.mean(volumes[-5:])
            avg_volume = np.mean(volumes[-20:]) if len(volumes) >= 20 else np.mean(volumes)
            
            # Volume surge detection
            surge = recent_volume > avg_volume * 1.5
            
            # Volume trend
            if len(volumes) >= 10:
                early_volume = np.mean(volumes[-10:-5])
                if recent_volume > early_volume * 1.2:
                    trend = "INCREASING"
                elif recent_volume < early_volume * 0.8:
                    trend = "DECREASING"
                else:
                    trend = "NORMAL"
            else:
                trend = "NORMAL"
            
            return {
                "surge": surge,
                "trend": trend,
                "recent": round(recent_volume, 2),
                "average": round(avg_volume, 2),
                "ratio": round(recent_volume / avg_volume, 2) if avg_volume > 0 else 1.0
            }
            
        except Exception as e:
            print(f"❌ Volume analysis error: {e}")
            return {"surge": False, "trend": "NORMAL"}
    
    def _calculate_momentum(self, prices: List[float]) -> float:
        """Calculate price momentum"""
        try:
            if len(prices) < 10:
                return 0.0
            
            # Momentum = (current - n periods ago) / n periods ago
            periods = min(10, len(prices) - 1)
            current = prices[-1]
            past = prices[-periods-1]
            
            if past != 0:
                momentum = (current - past) / past
            else:
                momentum = 0.0
            
            return round(momentum, 5)
            
        except Exception as e:
            print(f"❌ Momentum calculation error: {e}")
            return 0.0
    
    def _calculate_price_deviation(self, prices: List[float], current_price: float) -> float:
        """Calculate price deviation from mean"""
        try:
            if len(prices) < 20:
                return 0.0
            
            mean_price = np.mean(prices[-20:])
            std_price = np.std(prices[-20:])
            
            if std_price > 0:
                deviation = (current_price - mean_price) / std_price
            else:
                deviation = 0.0
            
            return round(deviation, 3)
            
        except Exception as e:
            print(f"❌ Price deviation error: {e}")
            return 0.0
    
    def _calculate_recent_movement(self, prices: List[float]) -> float:
        """Calculate recent price movement"""
        try:
            if len(prices) < 5:
                return 0.0
            
            recent_movement = prices[-1] - prices[-5]
            return round(recent_movement, 5)
            
        except Exception as e:
            print(f"❌ Recent movement error: {e}")
            return 0.0
    
    def _determine_market_condition(self, trend_analysis: Dict, volatility_analysis: Dict, 
                                  rsi: float, momentum: float) -> MarketCondition:
        """Determine overall market condition"""
        try:
            trend_direction = trend_analysis["direction"]
            trend_strength = trend_analysis["strength"]
            volatility_level = volatility_analysis["level"]
            
            # High volatility overrides trend
            if volatility_level in ["HIGH", "VERY_HIGH"]:
                return MarketCondition.HIGH_VOLATILITY
            elif volatility_level == "LOW":
                return MarketCondition.LOW_VOLATILITY
            
            # Trend-based conditions
            if trend_direction == "UP" and trend_strength > 0.5:
                return MarketCondition.TRENDING_UP
            elif trend_direction == "DOWN" and trend_strength > 0.5:
                return MarketCondition.TRENDING_DOWN
            else:
                return MarketCondition.RANGING
                
        except Exception as e:
            print(f"❌ Market condition error: {e}")
            return MarketCondition.UNKNOWN
    
    def _interpret_rsi(self, rsi: float) -> str:
        """Interpret RSI signal"""
        if rsi >= 80:
            return "EXTREMELY_OVERBOUGHT"
        elif rsi >= 70:
            return "OVERBOUGHT"
        elif rsi <= 20:
            return "EXTREMELY_OVERSOLD"
        elif rsi <= 30:
            return "OVERSOLD"
        else:
            return "NEUTRAL"
    
    def _calculate_analysis_confidence(self, data_points: int, volatility: float, 
                                     trend_strength: float) -> float:
        """Calculate confidence in analysis"""
        try:
            # Base confidence on data quality
            data_confidence = min(1.0, data_points / 100)
            
            # Reduce confidence in high volatility
            volatility_confidence = max(0.3, 1.0 - (volatility - 1.0) * 0.3)
            
            # Increase confidence with strong trends
            trend_confidence = 0.5 + trend_strength * 0.5
            
            overall_confidence = (data_confidence * 0.3 + volatility_confidence * 0.4 + 
                                trend_confidence * 0.3)
            
            return round(max(0.1, min(1.0, overall_confidence)), 3)
            
        except Exception as e:
            print(f"❌ Confidence calculation error: {e}")
            return 0.5
    
    def _level_to_dict(self, level: SupportResistanceLevel) -> Dict:
        """Convert level object to dictionary"""
        return {
            "level": level.level,
            "strength": level.strength,
            "touches": level.touches,
            "type": level.level_type
        }
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache is still valid"""
        if cache_key not in self.analysis_cache:
            return False
        
        cache_age = (datetime.now() - self.analysis_cache[cache_key]["timestamp"]).total_seconds()
        return cache_age < self.cache_timeout
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default analysis when data is unavailable"""
        return {
            "timestamp": datetime.now(),
            "current_price": 0.0,
            "condition": MarketCondition.UNKNOWN,
            "trend_strength": 0.0,
            "trend_direction": "SIDEWAYS",
            "volatility_factor": 1.0,
            "volatility_level": "NORMAL",
            "rsi": 50.0,
            "rsi_signal": "NEUTRAL",
            "bollinger_position": 0.5,
            "bollinger_squeeze": False,
            "support_levels": [],
            "resistance_levels": [],
            "atr": 0.0,
            "avg_atr": 0.0,
            "macd": {"macd": 0, "signal": 0, "histogram": 0},
            "volume_surge": False,
            "volume_trend": "NORMAL",
            "session": TradingSession.QUIET,
            "price_deviation_from_mean": 0.0,
            "recent_price_movement": 0.0,
            "market_momentum": 0.0,
            "confidence_score": 0.5,
            "spread": 0.0,
            "bid": 0.0,
            "ask": 0.0
        }

# Mock Market Analyzer for Testing
class MockMarketAnalyzer:
    """Mock Market Analyzer for testing purposes"""
    
    def __init__(self):
        self.mock_data_index = 0
        self.mock_scenarios = [
            # Bullish trend scenario
            {
                "condition": MarketCondition.TRENDING_UP,
                "trend_strength": 0.8,
                "rsi": 25,  # Oversold in uptrend
                "volatility_factor": 1.2,
                "bollinger_position": 0.2,
                "current_price": 2020.50
            },
            # Bearish trend scenario
            {
                "condition": MarketCondition.TRENDING_DOWN,
                "trend_strength": 0.7,
                "rsi": 75,  # Overbought in downtrend
                "volatility_factor": 1.5,
                "bollinger_position": 0.8,
                "current_price": 2010.30
            },
            # Ranging market scenario
            {
                "condition": MarketCondition.RANGING,
                "trend_strength": 0.2,
                "rsi": 50,
                "volatility_factor": 0.8,
                "bollinger_position": 0.5,
                "current_price": 2015.75
            }
        ]
        print("🧪 Mock Market Analyzer initialized for testing")
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """Return mock market analysis"""
        scenario = self.mock_scenarios[self.mock_data_index % len(self.mock_scenarios)]
        self.mock_data_index += 1
        
        return {
            "timestamp": datetime.now(),
            "current_price": scenario["current_price"],
            "condition": scenario["condition"],
            "trend_strength": scenario["trend_strength"],
            "trend_direction": "UP" if scenario["condition"] == MarketCondition.TRENDING_UP else 
                             "DOWN" if scenario["condition"] == MarketCondition.TRENDING_DOWN else "SIDEWAYS",
            "volatility_factor": scenario["volatility_factor"],
            "volatility_level": "HIGH" if scenario["volatility_factor"] > 1.3 else "NORMAL",
            "rsi": scenario["rsi"],
            "rsi_signal": "OVERSOLD" if scenario["rsi"] < 30 else "OVERBOUGHT" if scenario["rsi"] > 70 else "NEUTRAL",
            "bollinger_position": scenario["bollinger_position"],
            "bollinger_squeeze": False,
            "support_levels": [{"level": 2000.0, "strength": 4, "touches": 3, "type": "support"}],
            "resistance_levels": [{"level": 2030.0, "strength": 3, "touches": 2, "type": "resistance"}],
            "atr": 15.2,
            "avg_atr": 14.8,
            "macd": {"macd": 0.5, "signal": 0.3, "histogram": 0.2},
            "volume_surge": scenario["volatility_factor"] > 1.3,
            "volume_trend": "INCREASING",
            "session": TradingSession.LONDON,
            "price_deviation_from_mean": -1.2 if scenario["rsi"] < 30 else 1.2 if scenario["rsi"] > 70 else 0.1,
            "recent_price_movement": 8.5 if scenario["condition"] == MarketCondition.TRENDING_UP else
                                   -7.2 if scenario["condition"] == MarketCondition.TRENDING_DOWN else 1.1,
            "market_momentum": 0.03 if scenario["condition"] == MarketCondition.TRENDING_UP else
                             -0.025 if scenario["condition"] == MarketCondition.TRENDING_DOWN else 0.001,
            "confidence_score": 0.85,
            "spread": 0.3,
            "bid": scenario["current_price"] - 0.15,
            "ask": scenario["current_price"] + 0.15
        }

# Test function
def test_market_analyzer():
    """Test the market analyzer"""
    print("🧪 Testing Market Analyzer...")
    
    # Test with mock analyzer
    mock_analyzer = MockMarketAnalyzer()
    
    for i in range(3):
        print(f"\n--- Test Scenario {i+1} ---")
        analysis = mock_analyzer.get_comprehensive_analysis()
        
        print(f"🌍 Market Condition: {analysis['condition'].value}")
        print(f"📈 Trend: {analysis['trend_direction']} (strength: {analysis['trend_strength']:.1%})")
        print(f"📊 RSI: {analysis['rsi']:.1f} ({analysis['rsi_signal']})")
        print(f"💨 Volatility: {analysis['volatility_level']} (factor: {analysis['volatility_factor']:.1f})")
        print(f"🎯 Confidence: {analysis['confidence_score']:.1%}")
    
    print("\n✅ Market Analyzer test completed")

if __name__ == "__main__":
    test_market_analyzer()