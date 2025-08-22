"""
🧠 Modern Rule-based Trading Engine
rule_engine.py
หัวใจของระบบ AI ที่ใช้ Rule-based Architecture แบบทันสมัย
รองรับการเรียนรู้และปรับตัวแบบ Adaptive
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import numpy as np
from collections import deque
import statistics

class TradingDecision(Enum):
    """ประเภทการตัดสินใจเทรด"""
    BUY = "BUY"
    SELL = "SELL"
    CLOSE_PROFITABLE = "CLOSE_PROFITABLE"
    CLOSE_LOSING = "CLOSE_LOSING"
    WAIT = "WAIT"
    EMERGENCY_STOP = "EMERGENCY_STOP"

class MarketCondition(Enum):
    """สภาวะตลาด"""
    TRENDING_UP = "TRENDING_UP"
    TRENDING_DOWN = "TRENDING_DOWN"
    RANGING = "RANGING"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"
    UNKNOWN = "UNKNOWN"

class TradingMode(Enum):
    """โหมดการเทรด"""
    CONSERVATIVE = "CONSERVATIVE"
    BALANCED = "BALANCED"
    AGGRESSIVE = "AGGRESSIVE"
    ADAPTIVE = "ADAPTIVE"

@dataclass
class RuleResult:
    """ผลลัพธ์จาก Rule"""
    rule_name: str
    decision: TradingDecision
    confidence: float  # 0.0 - 1.0
    reasoning: str
    supporting_data: Dict[str, Any]
    weight: float = 1.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class RulePerformance:
    """ประสิทธิภาพของ Rule"""
    rule_name: str
    total_signals: int = 0
    successful_signals: int = 0
    total_profit: float = 0.0
    avg_confidence: float = 0.0
    last_updated: datetime = None
    performance_history: List[float] = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()
        if self.performance_history is None:
            self.performance_history = []
    
    @property
    def success_rate(self) -> float:
        """อัตราความสำเร็จ"""
        return self.successful_signals / max(self.total_signals, 1)
    
    @property
    def average_profit(self) -> float:
        """กำไรเฉลี่ย"""
        return self.total_profit / max(self.total_signals, 1)

class ModernRuleEngine:
    """
    🧠 Modern Rule-based Trading Engine
    
    ความสามารถหลัก:
    - Multi-rule decision making with weighted scoring
    - Adaptive learning from performance
    - Context-aware rule execution
    - Real-time confidence adjustment
    - Emergency protection mechanisms
    """
    
    def __init__(self, config: Dict, market_analyzer, order_manager, 
                 position_manager, performance_tracker):
        """
        Initialize Modern Rule Engine
        
        Args:
            config: Configuration from rules_config.json
            market_analyzer: Market analysis component
            order_manager: Order management component
            position_manager: Position management component
            performance_tracker: Performance tracking component
        """
        self.config = config
        self.market_analyzer = market_analyzer
        self.order_manager = order_manager
        self.position_manager = position_manager
        self.performance_tracker = performance_tracker
        
        # Engine state
        self.is_running = False
        self.current_mode = TradingMode.BALANCED
        self.last_decision = TradingDecision.WAIT
        self.last_decision_time = datetime.now()
        
        # Rules configuration
        self.rules_config = config.get("rules", {})
        self.adaptive_config = config.get("adaptive_settings", {})
        
        # Performance tracking
        self.rule_performances: Dict[str, RulePerformance] = {}
        self.decision_history = deque(maxlen=100)
        self.recent_decisions = deque(maxlen=10)
        
        # Adaptive parameters
        self.learning_rate = self.adaptive_config.get("learning_rate", 0.1)
        self.performance_window = self.adaptive_config.get("performance_window", 50)
        self.confidence_adjustment_rate = self.adaptive_config.get("confidence_adjustment_rate", 0.05)
        
        # Initialize rule performances
        self._initialize_rule_performances()
        
        # Threading
        self.engine_thread = None
        self.last_market_data = {}
        self.last_portfolio_data = {}
        
        print("🧠 Modern Rule Engine initialized")
        print(f"   Rules loaded: {list(self.rules_config.keys())}")
        print(f"   Learning rate: {self.learning_rate}")
        print(f"   Performance window: {self.performance_window}")
    
    def _initialize_rule_performances(self):
        """Initialize rule performance tracking"""
        for rule_name in self.rules_config.keys():
            self.rule_performances[rule_name] = RulePerformance(rule_name=rule_name)
    
    def set_trading_mode(self, mode: str):
        """Set trading mode and adjust rule weights"""
        try:
            self.current_mode = TradingMode(mode)
            self._adjust_weights_for_mode()
            print(f"🎯 Trading mode set to: {mode}")
        except ValueError:
            print(f"❌ Invalid trading mode: {mode}")
            self.current_mode = TradingMode.BALANCED
    
    def _adjust_weights_for_mode(self):
        """Adjust rule weights based on trading mode"""
        mode_adjustments = {
            TradingMode.CONSERVATIVE: {
                "trend_following": 0.4,      # เพิ่มความระมัดระวัง
                "mean_reversion": 0.3,
                "support_resistance": 0.2,
                "volatility_breakout": 0.05,  # ลดการเสี่ยง
                "portfolio_balance": 0.05
            },
            TradingMode.BALANCED: {
                "trend_following": 0.3,
                "mean_reversion": 0.25,
                "support_resistance": 0.2,
                "volatility_breakout": 0.15,
                "portfolio_balance": 0.1
            },
            TradingMode.AGGRESSIVE: {
                "trend_following": 0.25,
                "mean_reversion": 0.2,
                "support_resistance": 0.15,
                "volatility_breakout": 0.3,   # เพิ่มการเสี่ยง
                "portfolio_balance": 0.1
            },
            TradingMode.ADAPTIVE: {
                # ใช้ performance-based weights
                "dynamic": True
            }
        }
        
        if self.current_mode == TradingMode.ADAPTIVE:
            self._calculate_adaptive_weights()
        else:
            adjustments = mode_adjustments.get(self.current_mode, {})
            for rule_name, weight in adjustments.items():
                if rule_name in self.rules_config:
                    self.rules_config[rule_name]["weight"] = weight
    
    def _calculate_adaptive_weights(self):
        """Calculate weights based on recent performance"""
        total_performance = 0
        rule_scores = {}
        
        # Calculate performance scores for each rule
        for rule_name, performance in self.rule_performances.items():
            if performance.total_signals > 5:  # Minimum signals for reliability
                # Combined score: success rate * average profit * recent performance
                success_factor = performance.success_rate
                profit_factor = max(0, performance.average_profit) / 100  # Normalize
                recent_factor = np.mean(performance.performance_history[-10:]) if len(performance.performance_history) > 0 else 0.5
                
                score = (success_factor * 0.4 + profit_factor * 0.3 + recent_factor * 0.3)
                rule_scores[rule_name] = max(0.05, score)  # Minimum weight
                total_performance += rule_scores[rule_name]
            else:
                # Default weight for rules without enough data
                rule_scores[rule_name] = 0.2
                total_performance += 0.2
        
        # Normalize weights
        if total_performance > 0:
            for rule_name in rule_scores:
                if rule_name in self.rules_config:
                    self.rules_config[rule_name]["weight"] = rule_scores[rule_name] / total_performance
    
    def start(self):
        """Start the rule engine"""
        if self.is_running:
            print("⚠️ Rule engine already running")
            return
        
        self.is_running = True
        self.engine_thread = threading.Thread(target=self._engine_loop, daemon=True)
        self.engine_thread.start()
        print("🚀 Rule engine started")
    
    def stop(self):
        """Stop the rule engine"""
        self.is_running = False
        if self.engine_thread:
            self.engine_thread.join(timeout=5)
        print("🛑 Rule engine stopped")
    
    def _engine_loop(self):
        """Main engine loop"""
        while self.is_running:
            try:
                # Get current market and portfolio data
                self.last_market_data = self.market_analyzer.get_comprehensive_analysis()
                self.last_portfolio_data = self.position_manager.get_portfolio_status()
                
                # Execute rule-based decision making
                decision_result = self._execute_rule_based_decision()
                
                if decision_result:
                    # Execute the decision
                    self._execute_trading_decision(decision_result)
                    
                    # Track decision
                    self.decision_history.append(decision_result)
                    self.recent_decisions.append(decision_result)
                
                # Update rule performances
                self._update_rule_performances()
                
                # Adaptive learning
                if self.current_mode == TradingMode.ADAPTIVE:
                    self._adaptive_learning_update()
                
                # Sleep before next iteration
                time.sleep(5)  # 5-second intervals
                
            except Exception as e:
                print(f"❌ Rule engine error: {e}")
                time.sleep(10)  # Longer sleep on error
    
    def _execute_rule_based_decision(self) -> Optional[RuleResult]:
        """
        Execute rule-based decision making process
        
        Returns:
            RuleResult if decision should be made, None otherwise
        """
        try:
            # Collect results from all active rules
            rule_results = []
            
            # Execute each rule
            for rule_name, rule_config in self.rules_config.items():
                if not rule_config.get("enabled", True):
                    continue
                
                rule_result = self._execute_individual_rule(rule_name, rule_config)
                if rule_result:
                    rule_results.append(rule_result)
            
            if not rule_results:
                return None
            
            # Weighted decision making
            final_decision = self._make_weighted_decision(rule_results)
            
            return final_decision
            
        except Exception as e:
            print(f"❌ Rule execution error: {e}")
            return None
    
    def _execute_individual_rule(self, rule_name: str, rule_config: Dict) -> Optional[RuleResult]:
        """
        Execute individual rule
        
        Args:
            rule_name: Name of the rule
            rule_config: Configuration for the rule
            
        Returns:
            RuleResult if rule triggers, None otherwise
        """
        try:
            confidence_threshold = rule_config.get("confidence_threshold", 0.6)
            weight = rule_config.get("weight", 1.0)
            
            # Execute specific rule logic
            if rule_name == "trend_following":
                return self._rule_trend_following(rule_config, weight)
            elif rule_name == "mean_reversion":
                return self._rule_mean_reversion(rule_config, weight)
            elif rule_name == "support_resistance":
                return self._rule_support_resistance(rule_config, weight)
            elif rule_name == "volatility_breakout":
                return self._rule_volatility_breakout(rule_config, weight)
            elif rule_name == "portfolio_balance":
                return self._rule_portfolio_balance(rule_config, weight)
            else:
                print(f"❌ Unknown rule: {rule_name}")
                return None
                
        except Exception as e:
            print(f"❌ Rule {rule_name} execution error: {e}")
            return None
    
    def _rule_trend_following(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """Trend Following Rule"""
        try:
            market_data = self.last_market_data
            trend_strength = market_data.get("trend_strength", 0)
            rsi = market_data.get("rsi", 50)
            market_condition = market_data.get("condition", MarketCondition.UNKNOWN)
            
            # Rule parameters
            rsi_oversold = config["parameters"].get("rsi_oversold", 30)
            rsi_overbought = config["parameters"].get("rsi_overbought", 70)
            trend_threshold = config["parameters"].get("trend_strength_threshold", 0.5)
            
            confidence = 0.0
            decision = TradingDecision.WAIT
            reasoning = "Trend analysis"
            
            # Strong uptrend + oversold RSI = BUY signal
            if (market_condition == MarketCondition.TRENDING_UP and 
                trend_strength > trend_threshold and rsi < rsi_oversold):
                decision = TradingDecision.BUY
                confidence = min(0.9, 0.5 + trend_strength * 0.4)
                reasoning = f"Strong uptrend detected (strength: {trend_strength:.2f}) with oversold RSI ({rsi:.1f})"
            
            # Strong downtrend + overbought RSI = SELL signal
            elif (market_condition == MarketCondition.TRENDING_DOWN and 
                  trend_strength > trend_threshold and rsi > rsi_overbought):
                decision = TradingDecision.SELL
                confidence = min(0.9, 0.5 + trend_strength * 0.4)
                reasoning = f"Strong downtrend detected (strength: {trend_strength:.2f}) with overbought RSI ({rsi:.1f})"
            
            # Check if confidence meets threshold
            if confidence >= config.get("confidence_threshold", 0.6):
                return RuleResult(
                    rule_name="trend_following",
                    decision=decision,
                    confidence=confidence,
                    reasoning=reasoning,
                    supporting_data={
                        "trend_strength": trend_strength,
                        "rsi": rsi,
                        "market_condition": market_condition.value
                    },
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Trend following rule error: {e}")
            return None
    
    def _rule_mean_reversion(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """Mean Reversion Rule"""
        try:
            market_data = self.last_market_data
            bb_position = market_data.get("bollinger_position", 0.5)  # 0 = bottom, 1 = top
            price_deviation = market_data.get("price_deviation_from_mean", 0)
            volatility = market_data.get("volatility_factor", 1.0)
            
            # Rule parameters
            bb_lower_threshold = 0.1  # Near lower band
            bb_upper_threshold = 0.9  # Near upper band
            deviation_threshold = 2.0  # Standard deviations
            
            confidence = 0.0
            decision = TradingDecision.WAIT
            reasoning = "Mean reversion analysis"
            
            # Price near lower Bollinger Band = potential BUY
            if bb_position < bb_lower_threshold and price_deviation < -deviation_threshold:
                decision = TradingDecision.BUY
                confidence = min(0.85, 0.4 + abs(price_deviation) * 0.1)
                reasoning = f"Price oversold - near lower BB ({bb_position:.2f}) with high deviation ({price_deviation:.2f})"
            
            # Price near upper Bollinger Band = potential SELL
            elif bb_position > bb_upper_threshold and price_deviation > deviation_threshold:
                decision = TradingDecision.SELL
                confidence = min(0.85, 0.4 + abs(price_deviation) * 0.1)
                reasoning = f"Price overbought - near upper BB ({bb_position:.2f}) with high deviation ({price_deviation:.2f})"
            
            # Adjust confidence based on volatility
            if volatility > 2.0:  # High volatility reduces confidence
                confidence *= 0.7
                reasoning += " (reduced due to high volatility)"
            
            # Check confidence threshold
            if confidence >= config.get("confidence_threshold", 0.7):
                return RuleResult(
                    rule_name="mean_reversion",
                    decision=decision,
                    confidence=confidence,
                    reasoning=reasoning,
                    supporting_data={
                        "bollinger_position": bb_position,
                        "price_deviation": price_deviation,
                        "volatility": volatility
                    },
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Mean reversion rule error: {e}")
            return None
    
    def _rule_support_resistance(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """Support/Resistance Rule"""
        try:
            market_data = self.last_market_data
            current_price = market_data.get("current_price", 0)
            support_levels = market_data.get("support_levels", [])
            resistance_levels = market_data.get("resistance_levels", [])
            
            # Rule parameters
            touch_tolerance = config["parameters"].get("touch_tolerance", 5)  # points
            strength_threshold = config["parameters"].get("strength_threshold", 3)
            
            confidence = 0.0
            decision = TradingDecision.WAIT
            reasoning = "Support/resistance analysis"
            
            # Check for support bounce
            for support in support_levels:
                if abs(current_price - support["level"]) <= touch_tolerance:
                    if support["strength"] >= strength_threshold:
                        decision = TradingDecision.BUY
                        confidence = min(0.8, 0.5 + (support["strength"] / 10) * 0.3)
                        reasoning = f"Strong support level ({support['level']}) with strength {support['strength']}"
                        break
            
            # Check for resistance rejection
            if decision == TradingDecision.WAIT:  # Only if no support signal
                for resistance in resistance_levels:
                    if abs(current_price - resistance["level"]) <= touch_tolerance:
                        if resistance["strength"] >= strength_threshold:
                            decision = TradingDecision.SELL
                            confidence = min(0.8, 0.5 + (resistance["strength"] / 10) * 0.3)
                            reasoning = f"Strong resistance level ({resistance['level']}) with strength {resistance['strength']}"
                            break
            
            # Check confidence threshold
            if confidence >= config.get("confidence_threshold", 0.6):
                return RuleResult(
                    rule_name="support_resistance",
                    decision=decision,
                    confidence=confidence,
                    reasoning=reasoning,
                    supporting_data={
                        "current_price": current_price,
                        "support_levels": len(support_levels),
                        "resistance_levels": len(resistance_levels)
                    },
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Support/resistance rule error: {e}")
            return None
    
    def _rule_volatility_breakout(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """Volatility Breakout Rule"""
        try:
            market_data = self.last_market_data
            atr = market_data.get("atr", 0)
            avg_atr = market_data.get("avg_atr", atr)
            price_movement = market_data.get("recent_price_movement", 0)
            volume_surge = market_data.get("volume_surge", False)
            
            # Rule parameters
            atr_multiplier = config["parameters"].get("volatility_threshold", 1.5)
            confirmation_bars = config["parameters"].get("breakout_confirmation", 2)
            
            confidence = 0.0
            decision = TradingDecision.WAIT
            reasoning = "Volatility breakout analysis"
            
            # High volatility detected
            if atr > avg_atr * atr_multiplier and volume_surge:
                # Bullish breakout
                if price_movement > atr * 0.5:
                    decision = TradingDecision.BUY
                    confidence = min(0.9, 0.6 + (atr / avg_atr - 1) * 0.3)
                    reasoning = f"Bullish volatility breakout - ATR: {atr:.1f} (avg: {avg_atr:.1f}), movement: {price_movement:.1f}"
                
                # Bearish breakout
                elif price_movement < -atr * 0.5:
                    decision = TradingDecision.SELL
                    confidence = min(0.9, 0.6 + (atr / avg_atr - 1) * 0.3)
                    reasoning = f"Bearish volatility breakout - ATR: {atr:.1f} (avg: {avg_atr:.1f}), movement: {price_movement:.1f}"
            
            # Check confidence threshold
            if confidence >= config.get("confidence_threshold", 0.8):
                return RuleResult(
                    rule_name="volatility_breakout",
                    decision=decision,
                    confidence=confidence,
                    reasoning=reasoning,
                    supporting_data={
                        "atr": atr,
                        "avg_atr": avg_atr,
                        "price_movement": price_movement,
                        "volume_surge": volume_surge
                    },
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Volatility breakout rule error: {e}")
            return None
    
    def _rule_portfolio_balance(self, config: Dict, weight: float) -> Optional[RuleResult]:
        """Portfolio Balance Rule"""
        try:
            portfolio_data = self.last_portfolio_data
            buy_positions = portfolio_data.get("buy_positions", 0)
            sell_positions = portfolio_data.get("sell_positions", 0)
            total_positions = buy_positions + sell_positions
            total_profit = portfolio_data.get("total_profit", 0)
            max_exposure = config["parameters"].get("max_exposure_ratio", 0.7)
            
            confidence = 0.0
            decision = TradingDecision.WAIT
            reasoning = "Portfolio balance analysis"
            
            # Portfolio too heavy on one side
            if total_positions > 0:
                buy_ratio = buy_positions / total_positions
                sell_ratio = sell_positions / total_positions
                
                # Too many BUY positions, consider SELL for balance
                if buy_ratio > max_exposure:
                    decision = TradingDecision.SELL
                    confidence = 0.6 + (buy_ratio - max_exposure) * 2
                    reasoning = f"Portfolio imbalanced - too many BUY positions ({buy_ratio:.1%})"
                
                # Too many SELL positions, consider BUY for balance
                elif sell_ratio > max_exposure:
                    decision = TradingDecision.BUY
                    confidence = 0.6 + (sell_ratio - max_exposure) * 2
                    reasoning = f"Portfolio imbalanced - too many SELL positions ({sell_ratio:.1%})"
            
            # Consider closing profitable positions
            if total_profit > 100:  # $100 profit threshold
                decision = TradingDecision.CLOSE_PROFITABLE
                confidence = min(0.8, 0.5 + (total_profit / 1000) * 0.3)
                reasoning = f"Close profitable positions - total profit: ${total_profit:.2f}"
            
            # Check confidence threshold
            if confidence >= config.get("confidence_threshold", 0.5):
                return RuleResult(
                    rule_name="portfolio_balance",
                    decision=decision,
                    confidence=confidence,
                    reasoning=reasoning,
                    supporting_data={
                        "buy_positions": buy_positions,
                        "sell_positions": sell_positions,
                        "total_profit": total_profit
                    },
                    weight=weight
                )
            
            return None
            
        except Exception as e:
            print(f"❌ Portfolio balance rule error: {e}")
            return None
    
    def _make_weighted_decision(self, rule_results: List[RuleResult]) -> Optional[RuleResult]:
        """
        Make final decision based on weighted rule results
        
        Args:
            rule_results: List of rule results
            
        Returns:
            Final decision or None
        """
        try:
            if not rule_results:
                return None
            
            # Group by decision type
            decision_scores = {}
            decision_reasons = {}
            decision_data = {}
            
            for result in rule_results:
                decision = result.decision
                weighted_confidence = result.confidence * result.weight
                
                if decision not in decision_scores:
                    decision_scores[decision] = 0
                    decision_reasons[decision] = []
                    decision_data[decision] = []
                
                decision_scores[decision] += weighted_confidence
                decision_reasons[decision].append(f"{result.rule_name}: {result.reasoning}")
                decision_data[decision].append(result.supporting_data)
            
            # Find the decision with highest score
            if not decision_scores:
                return None
            
            best_decision = max(decision_scores.keys(), key=lambda k: decision_scores[k])
            best_score = decision_scores[best_decision]
            
            # Minimum threshold for action
            min_threshold = 0.5
            if best_score < min_threshold:
                return None
            
            # Create final result
            final_result = RuleResult(
                rule_name="weighted_decision",
                decision=best_decision,
                confidence=min(1.0, best_score),
                reasoning=" | ".join(decision_reasons[best_decision]),
                supporting_data={
                    "decision_scores": decision_scores,
                    "contributing_rules": len(decision_reasons[best_decision]),
                    "total_weight": sum(r.weight for r in rule_results)
                }
            )
            
            return final_result
            
        except Exception as e:
            print(f"❌ Weighted decision error: {e}")
            return None
    
    def _execute_trading_decision(self, decision_result: RuleResult):
        """Execute the trading decision"""
        try:
            decision = decision_result.decision
            confidence = decision_result.confidence
            reasoning = decision_result.reasoning
            
            print(f"🎯 Executing decision: {decision.value} (confidence: {confidence:.1%})")
            print(f"💭 Reasoning: {reasoning}")
            
            # Execute based on decision type
            if decision == TradingDecision.BUY:
                success = self.order_manager.place_smart_buy_order(
                    confidence=confidence,
                    reasoning=reasoning
                )
            elif decision == TradingDecision.SELL:
                success = self.order_manager.place_smart_sell_order(
                    confidence=confidence,
                    reasoning=reasoning
                )
            elif decision == TradingDecision.CLOSE_PROFITABLE:
                success = self.position_manager.close_profitable_positions(
                    confidence=confidence,
                    reasoning=reasoning
                )
            elif decision == TradingDecision.CLOSE_LOSING:
                success = self.position_manager.close_losing_positions(
                    confidence=confidence,
                    reasoning=reasoning
                )
            elif decision == TradingDecision.EMERGENCY_STOP:
                success = self.position_manager.emergency_close_all()
            else:
                success = True  # WAIT decision
            
            # Update last decision
            self.last_decision = decision
            self.last_decision_time = datetime.now()
            
            # Track execution
            self.performance_tracker.track_decision(decision_result, success)
            
        except Exception as e:
            print(f"❌ Decision execution error: {e}")
    
    def _update_rule_performances(self):
        """Update rule performance metrics"""
        try:
            # Update based on recent decisions and their outcomes
            for decision in list(self.recent_decisions):
                if decision.timestamp < datetime.now() - timedelta(minutes=30):
                    # Decision is old enough to evaluate
                    outcome = self.performance_tracker.get_decision_outcome(decision)
                    if outcome is not None:
                        self._update_rule_performance(decision.rule_name, outcome)
                        self.recent_decisions.remove(decision)
        
        except Exception as e:
            print(f"❌ Performance update error: {e}")
    
    def _update_rule_performance(self, rule_name: str, outcome: bool):
        """Update individual rule performance"""
        try:
            if rule_name not in self.rule_performances:
                self.rule_performances[rule_name] = RulePerformance(rule_name=rule_name)
            
            performance = self.rule_performances[rule_name]
            performance.total_signals += 1
            
            if outcome:
                performance.successful_signals += 1
                performance.total_profit += 10  # Simplified profit tracking
            
            # Update performance history
            current_success_rate = performance.success_rate
            performance.performance_history.append(current_success_rate)
            
            # Keep history manageable
            if len(performance.performance_history) > self.performance_window:
                performance.performance_history.pop(0)
            
            performance.last_updated = datetime.now()
            
        except Exception as e:
            print(f"❌ Rule performance update error: {e}")
    
    def _adaptive_learning_update(self):
        """Update adaptive learning parameters"""
        try:
            # Adjust confidence thresholds based on performance
            for rule_name, performance in self.rule_performances.items():
                if rule_name in self.rules_config and performance.total_signals > 10:
                    current_threshold = self.rules_config[rule_name].get("confidence_threshold", 0.6)
                    
                    # Increase threshold for poorly performing rules
                    if performance.success_rate < 0.4:
                        new_threshold = min(0.9, current_threshold + self.confidence_adjustment_rate)
                        self.rules_config[rule_name]["confidence_threshold"] = new_threshold
                    
                    # Decrease threshold for well-performing rules
                    elif performance.success_rate > 0.7:
                        new_threshold = max(0.3, current_threshold - self.confidence_adjustment_rate)
                        self.rules_config[rule_name]["confidence_threshold"] = new_threshold
            
            # Recalculate adaptive weights
            self._calculate_adaptive_weights()
            
        except Exception as e:
            print(f"❌ Adaptive learning error: {e}")
    
    # === Public Interface Methods ===
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            portfolio_data = self.last_portfolio_data
            
            return {
                "rule_confidence": self.get_overall_confidence(),
                "market_condition": self.last_market_data.get("condition", "UNKNOWN"),
                "portfolio_health": self._calculate_portfolio_health(),
                "total_profit": portfolio_data.get("total_profit", 0),
                "active_positions": portfolio_data.get("total_positions", 0),
                "pending_orders": self.order_manager.get_pending_orders_count() if self.order_manager else 0,
                "risk_level": portfolio_data.get("risk_level", 0),
                "last_action": self.last_decision.value,
                "action_reason": self._get_last_action_reason(),
                "survivability_usage": portfolio_data.get("survivability_usage", 0),
                "engine_running": self.is_running,
                "trading_mode": self.current_mode.value
            }
        except Exception as e:
            print(f"❌ Status error: {e}")
            return {"error": str(e)}
    
    def get_overall_confidence(self) -> float:
        """Get overall rule engine confidence"""
        try:
            if not self.rule_performances:
                return 0.0
            
            total_weight = 0
            weighted_confidence = 0
            
            for rule_name, rule_config in self.rules_config.items():
                if rule_name in self.rule_performances:
                    performance = self.rule_performances[rule_name]
                    weight = rule_config.get("weight", 1.0)
                    confidence = performance.success_rate if performance.total_signals > 0 else 0.5
                    
                    weighted_confidence += confidence * weight
                    total_weight += weight
            
            return weighted_confidence / max(total_weight, 1)
            
        except Exception as e:
            print(f"❌ Confidence calculation error: {e}")
            return 0.0
    
    def get_rules_status(self) -> Dict[str, Dict]:
        """Get status of all rules"""
        try:
            status = {}
            
            for rule_name, rule_config in self.rules_config.items():
                performance = self.rule_performances.get(rule_name)
                
                status[rule_name] = {
                    "weight": rule_config.get("weight", 1.0),
                    "confidence": performance.success_rate if performance and performance.total_signals > 0 else 0.5,
                    "active": rule_config.get("enabled", True),
                    "total_signals": performance.total_signals if performance else 0,
                    "success_rate": performance.success_rate if performance else 0.0,
                    "confidence_threshold": rule_config.get("confidence_threshold", 0.6)
                }
            
            return status
            
        except Exception as e:
            print(f"❌ Rules status error: {e}")
            return {}
    
    def _calculate_portfolio_health(self) -> float:
        """Calculate overall portfolio health (0.0 - 1.0)"""
        try:
            portfolio_data = self.last_portfolio_data
            
            # Factors: profit ratio, position balance, risk level
            profit_factor = max(0, min(1, (portfolio_data.get("total_profit", 0) + 100) / 200))
            balance_factor = 1 - abs(0.5 - portfolio_data.get("position_balance", 0.5)) * 2
            risk_factor = 1 - portfolio_data.get("risk_level", 0)
            
            return (profit_factor * 0.4 + balance_factor * 0.3 + risk_factor * 0.3)
            
        except Exception as e:
            print(f"❌ Portfolio health calculation error: {e}")
            return 0.5
    
    def _get_last_action_reason(self) -> str:
        """Get reasoning for last action"""
        try:
            if self.decision_history:
                last_decision = self.decision_history[-1]
                return last_decision.reasoning
            return "No actions taken yet"
        except:
            return "Unknown"

# Test function
def test_rule_engine():
    """Test the rule engine with mock components"""
    print("🧪 Testing Modern Rule Engine...")
    
    # Mock configurations
    config = {
        "rules": {
            "trend_following": {
                "weight": 0.3,
                "confidence_threshold": 0.6,
                "parameters": {"rsi_period": 14, "rsi_oversold": 30, "rsi_overbought": 70}
            }
        },
        "adaptive_settings": {
            "learning_rate": 0.1,
            "performance_window": 50
        }
    }
    
    # Mock components (would be real in actual implementation)
    class MockAnalyzer:
        def get_comprehensive_analysis(self):
            return {"condition": "TRENDING_UP", "trend_strength": 0.7, "rsi": 25}
    
    class MockOrderManager:
        def place_smart_buy_order(self, **kwargs): return True
        def get_pending_orders_count(self): return 0
    
    class MockPositionManager:
        def get_portfolio_status(self): return {"total_profit": 50, "total_positions": 3}
    
    class MockTracker:
        def track_decision(self, decision, success): pass
        def get_decision_outcome(self, decision): return True
    
    # Initialize engine
    engine = ModernRuleEngine(
        config=config,
        market_analyzer=MockAnalyzer(),
        order_manager=MockOrderManager(),
        position_manager=MockPositionManager(),
        performance_tracker=MockTracker()
    )
    
    # Test decision making
    engine.last_market_data = {"condition": MarketCondition.TRENDING_UP, "trend_strength": 0.8, "rsi": 25}
    engine.last_portfolio_data = {"total_profit": 50, "total_positions": 3}
    
    decision = engine._execute_rule_based_decision()
    if decision:
        print(f"✅ Decision: {decision.decision.value} (confidence: {decision.confidence:.1%})")
        print(f"💭 Reasoning: {decision.reasoning}")
    else:
        print("🔄 No decision made")
    
    print("✅ Rule engine test completed")

if __name__ == "__main__":
    test_rule_engine()