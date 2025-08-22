"""
📈 Modern Performance Tracker
performance_tracker.py
การติดตามผลงานแบบครอบคลุม สำหรับ Modern Rule-based Trading System
รองรับการวิเคราะห์ performance, rule effectiveness, และ system optimization
"""

import time
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from collections import deque, defaultdict
import statistics
import json

class PerformanceMetric(Enum):
    """ประเภทตัวชี้วัดผลงาน"""
    TOTAL_PROFIT = "TOTAL_PROFIT"
    WIN_RATE = "WIN_RATE"
    PROFIT_FACTOR = "PROFIT_FACTOR"
    SHARPE_RATIO = "SHARPE_RATIO"
    MAX_DRAWDOWN = "MAX_DRAWDOWN"
    AVERAGE_TRADE = "AVERAGE_TRADE"
    RISK_REWARD_RATIO = "RISK_REWARD_RATIO"
    RULE_EFFECTIVENESS = "RULE_EFFECTIVENESS"
    SYSTEM_UPTIME = "SYSTEM_UPTIME"

class TradeResult(Enum):
    """ผลลัพธ์การเทรด"""
    WIN = "WIN"
    LOSS = "LOSS"
    BREAKEVEN = "BREAKEVEN"
    PENDING = "PENDING"

@dataclass
class TradeRecord:
    """บันทึกการเทรด"""
    trade_id: str
    timestamp: datetime
    symbol: str
    direction: str
    lot_size: float
    entry_price: float
    exit_price: float = 0.0
    profit: float = 0.0
    commission: float = 0.0
    swap: float = 0.0
    duration_minutes: int = 0
    rule_triggered: str = ""
    confidence_level: float = 0.0
    market_condition: str = ""
    result: TradeResult = TradeResult.PENDING
    reasoning: str = ""
    
    @property
    def net_profit(self) -> float:
        """กำไร/ขาดทุนสุทธิ"""
        return self.profit + self.commission + self.swap
    
    @property
    def pips_profit(self) -> float:
        """กำไร/ขาดทุนในหน่วย pips"""
        if self.exit_price == 0:
            return 0.0
        
        if self.direction == "BUY":
            return (self.exit_price - self.entry_price) * 10000
        else:
            return (self.entry_price - self.exit_price) * 10000

@dataclass
class RulePerformance:
    """ผลงานของ Rule"""
    rule_name: str
    total_signals: int = 0
    successful_signals: int = 0
    total_profit: float = 0.0
    total_loss: float = 0.0
    avg_confidence: float = 0.0
    best_trade: float = 0.0
    worst_trade: float = 0.0
    avg_duration_minutes: float = 0.0
    last_signal_time: datetime = field(default_factory=datetime.now)
    signal_history: List[Dict] = field(default_factory=list)
    
    @property
    def win_rate(self) -> float:
        """อัตราการชนะ"""
        return self.successful_signals / max(self.total_signals, 1)
    
    @property
    def profit_factor(self) -> float:
        """Profit Factor"""
        return abs(self.total_profit) / max(abs(self.total_loss), 1)
    
    @property
    def average_profit(self) -> float:
        """กำไรเฉลี่ยต่อ signal"""
        return (self.total_profit + self.total_loss) / max(self.total_signals, 1)

@dataclass
class SystemPerformance:
    """ผลงานระบบรวม"""
    start_time: datetime
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    total_profit: float = 0.0
    total_commission: float = 0.0
    total_swap: float = 0.0
    max_profit: float = 0.0
    max_loss: float = 0.0
    max_drawdown: float = 0.0
    max_drawdown_percentage: float = 0.0
    current_drawdown: float = 0.0
    peak_balance: float = 0.0
    avg_trade_duration: float = 0.0
    system_uptime_percentage: float = 100.0
    
    @property
    def net_profit(self) -> float:
        """กำไรสุทธิ"""
        return self.total_profit + self.total_commission + self.total_swap
    
    @property
    def win_rate(self) -> float:
        """อัตราการชนะ"""
        return self.winning_trades / max(self.total_trades, 1)
    
    @property
    def profit_factor(self) -> float:
        """Profit Factor"""
        gross_profit = sum([trade.net_profit for trade in self.get_winning_trades()])
        gross_loss = abs(sum([trade.net_profit for trade in self.get_losing_trades()]))
        return gross_profit / max(gross_loss, 1)
    
    def get_winning_trades(self) -> List[TradeRecord]:
        """Placeholder - would return winning trades"""
        return []
    
    def get_losing_trades(self) -> List[TradeRecord]:
        """Placeholder - would return losing trades"""
        return []

class PerformanceTracker:
    """
    📈 Modern Performance Tracker
    
    ความสามารถ:
    - Comprehensive trade tracking
    - Rule performance analysis
    - System performance metrics
    - Real-time analytics
    - Performance optimization insights
    - Risk management statistics
    - Benchmarking and comparison
    - Automated reporting
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize Performance Tracker
        
        Args:
            config: Configuration settings
        """
        self.config = config or {}
        
        # Trade tracking
        self.trade_records: List[TradeRecord] = []
        self.active_trades: Dict[str, TradeRecord] = {}
        self.trade_id_counter = 0
        
        # Rule performance tracking
        self.rule_performances: Dict[str, RulePerformance] = {}
        
        # System performance
        self.system_performance = SystemPerformance(start_time=datetime.now())
        
        # Performance history
        self.daily_performance = deque(maxlen=365)  # 1 year of daily data
        self.hourly_performance = deque(maxlen=24*7)  # 1 week of hourly data
        self.equity_curve = deque(maxlen=1000)
        
        # Analytics
        self.performance_analytics = {}
        self.last_analytics_update = datetime.min
        self.analytics_update_interval = timedelta(minutes=5)
        
        # Benchmarking
        self.benchmarks = {
            "daily_target": 0.5,  # 0.5% daily target
            "weekly_target": 3.0,  # 3% weekly target
            "monthly_target": 12.0,  # 12% monthly target
            "max_drawdown_limit": 20.0,  # 20% max drawdown limit
            "min_win_rate": 55.0,  # 55% minimum win rate
            "min_profit_factor": 1.2  # 1.2 minimum profit factor
        }
        
        # System health
        self.system_health_score = 100.0
        self.last_system_check = datetime.now()
        self.downtime_periods = []
        
        print("📈 Performance Tracker initialized")
        print(f"   Start time: {self.system_performance.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Analytics interval: {self.analytics_update_interval.total_seconds():.0f} seconds")
        print(f"   Daily target: {self.benchmarks['daily_target']}%")
    
    def track_decision(self, decision_result, success: bool, profit: float = 0.0):
        """
        Track rule decision and outcome
        
        Args:
            decision_result: RuleResult object from rule engine
            success: Whether the decision was successful
            profit: Profit/loss from the decision
        """
        try:
            rule_name = decision_result.rule_name
            
            # Initialize rule performance if not exists
            if rule_name not in self.rule_performances:
                self.rule_performances[rule_name] = RulePerformance(rule_name=rule_name)
            
            rule_perf = self.rule_performances[rule_name]
            
            # Update rule performance
            rule_perf.total_signals += 1
            rule_perf.last_signal_time = datetime.now()
            
            if success:
                rule_perf.successful_signals += 1
                rule_perf.total_profit += max(0, profit)
                rule_perf.best_trade = max(rule_perf.best_trade, profit)
            else:
                rule_perf.total_loss += min(0, profit)
                rule_perf.worst_trade = min(rule_perf.worst_trade, profit)
            
            # Update average confidence
            total_confidence = rule_perf.avg_confidence * (rule_perf.total_signals - 1)
            rule_perf.avg_confidence = (total_confidence + decision_result.confidence) / rule_perf.total_signals
            
            # Add to signal history
            signal_data = {
                "timestamp": datetime.now(),
                "confidence": decision_result.confidence,
                "decision": decision_result.decision.value,
                "success": success,
                "profit": profit,
                "reasoning": decision_result.reasoning
            }
            rule_perf.signal_history.append(signal_data)
            
            # Keep history manageable
            if len(rule_perf.signal_history) > 100:
                rule_perf.signal_history.pop(0)
            
            print(f"📈 Rule performance tracked: {rule_name}")
            print(f"   Success: {success}, Profit: ${profit:.2f}")
            print(f"   Win rate: {rule_perf.win_rate:.1%}, Avg profit: ${rule_perf.average_profit:.2f}")
            
        except Exception as e:
            print(f"❌ Decision tracking error: {e}")
    
    def start_trade_tracking(self, symbol: str, direction: str, lot_size: float,
                           entry_price: float, rule_triggered: str = "", 
                           confidence: float = 0.0, market_condition: str = "",
                           reasoning: str = "") -> str:
        """
        Start tracking a new trade
        
        Args:
            symbol: Trading symbol
            direction: BUY or SELL
            lot_size: Position size
            entry_price: Entry price
            rule_triggered: Rule that triggered the trade
            confidence: Confidence level
            market_condition: Market condition
            reasoning: Reasoning for the trade
            
        Returns:
            Trade ID for tracking
        """
        try:
            self.trade_id_counter += 1
            trade_id = f"T{self.trade_id_counter:06d}"
            
            trade_record = TradeRecord(
                trade_id=trade_id,
                timestamp=datetime.now(),
                symbol=symbol,
                direction=direction,
                lot_size=lot_size,
                entry_price=entry_price,
                rule_triggered=rule_triggered,
                confidence_level=confidence,
                market_condition=market_condition,
                reasoning=reasoning
            )
            
            self.active_trades[trade_id] = trade_record
            
            print(f"📈 Trade tracking started: {trade_id}")
            print(f"   {direction} {lot_size} {symbol} @ {entry_price}")
            print(f"   Rule: {rule_triggered}, Confidence: {confidence:.1%}")
            
            return trade_id
            
        except Exception as e:
            print(f"❌ Trade tracking start error: {e}")
            return ""
    
    def complete_trade_tracking(self, trade_id: str, exit_price: float,
                              profit: float, commission: float = 0.0,
                              swap: float = 0.0) -> bool:
        """
        Complete trade tracking
        
        Args:
            trade_id: Trade ID
            exit_price: Exit price
            profit: Gross profit
            commission: Commission paid
            swap: Swap paid/received
            
        Returns:
            True if tracking completed successfully
        """
        try:
            if trade_id not in self.active_trades:
                print(f"❌ Trade {trade_id} not found in active trades")
                return False
            
            trade = self.active_trades[trade_id]
            
            # Complete trade record
            trade.exit_price = exit_price
            trade.profit = profit
            trade.commission = commission
            trade.swap = swap
            trade.duration_minutes = int((datetime.now() - trade.timestamp).total_seconds() / 60)
            
            # Determine result
            net_profit = trade.net_profit
            if net_profit > 1.0:
                trade.result = TradeResult.WIN
            elif net_profit < -1.0:
                trade.result = TradeResult.LOSS
            else:
                trade.result = TradeResult.BREAKEVEN
            
            # Move to completed trades
            self.trade_records.append(trade)
            del self.active_trades[trade_id]
            
            # Update system performance
            self._update_system_performance(trade)
            
            # Update equity curve
            self._update_equity_curve(trade)
            
            print(f"📈 Trade tracking completed: {trade_id}")
            print(f"   Result: {trade.result.value}, Net P&L: ${net_profit:.2f}")
            print(f"   Duration: {trade.duration_minutes} minutes")
            
            return True
            
        except Exception as e:
            print(f"❌ Trade tracking completion error: {e}")
            return False
    
    def _update_system_performance(self, trade: TradeRecord):
        """Update system performance metrics"""
        try:
            perf = self.system_performance
            
            # Basic counts
            perf.total_trades += 1
            
            if trade.result == TradeResult.WIN:
                perf.winning_trades += 1
            elif trade.result == TradeResult.LOSS:
                perf.losing_trades += 1
            
            # Profit tracking
            net_profit = trade.net_profit
            perf.total_profit += trade.profit
            perf.total_commission += trade.commission
            perf.total_swap += trade.swap
            
            # Extremes
            perf.max_profit = max(perf.max_profit, net_profit)
            perf.max_loss = min(perf.max_loss, net_profit)
            
            # Update peak balance and drawdown
            current_balance = perf.net_profit
            if current_balance > perf.peak_balance:
                perf.peak_balance = current_balance
                perf.current_drawdown = 0.0
            else:
                perf.current_drawdown = perf.peak_balance - current_balance
                perf.max_drawdown = max(perf.max_drawdown, perf.current_drawdown)
                
                if perf.peak_balance > 0:
                    drawdown_percentage = (perf.current_drawdown / perf.peak_balance) * 100
                    perf.max_drawdown_percentage = max(perf.max_drawdown_percentage, drawdown_percentage)
            
            # Average trade duration
            total_duration = perf.avg_trade_duration * (perf.total_trades - 1) + trade.duration_minutes
            perf.avg_trade_duration = total_duration / perf.total_trades
            
        except Exception as e:
            print(f"❌ System performance update error: {e}")
    
    def _update_equity_curve(self, trade: TradeRecord):
        """Update equity curve"""
        try:
            current_equity = self.system_performance.net_profit
            
            equity_point = {
                "timestamp": datetime.now(),
                "equity": current_equity,
                "trade_id": trade.trade_id,
                "profit": trade.net_profit
            }
            
            self.equity_curve.append(equity_point)
            
        except Exception as e:
            print(f"❌ Equity curve update error: {e}")
    
    def get_decision_outcome(self, decision_result) -> Optional[bool]:
        """
        Get outcome of a previous decision
        
        Args:
            decision_result: RuleResult object
            
        Returns:
            True if successful, False if failed, None if unknown
        """
        try:
            # This would integrate with actual trade tracking
            # For now, return a simplified outcome based on time
            decision_age = datetime.now() - decision_result.timestamp
            
            if decision_age < timedelta(minutes=30):
                return None  # Too recent to evaluate
            
            # Simplified outcome logic
            # In real implementation, this would check actual trade results
            return decision_result.confidence > 0.6
            
        except Exception as e:
            print(f"❌ Decision outcome error: {e}")
            return None
    
    def calculate_performance_analytics(self) -> Dict[str, Any]:
        """Calculate comprehensive performance analytics"""
        try:
            if datetime.now() - self.last_analytics_update < self.analytics_update_interval:
                return self.performance_analytics
            
            analytics = {}
            
            # Basic performance metrics
            analytics.update(self._calculate_basic_metrics())
            
            # Rule performance analytics
            analytics.update(self._calculate_rule_analytics())
            
            # Risk metrics
            analytics.update(self._calculate_risk_metrics())
            
            # Time-based analytics
            analytics.update(self._calculate_time_analytics())
            
            # System health
            analytics.update(self._calculate_system_health())
            
            # Benchmarking
            analytics.update(self._calculate_benchmark_comparison())
            
            self.performance_analytics = analytics
            self.last_analytics_update = datetime.now()
            
            return analytics
            
        except Exception as e:
            print(f"❌ Performance analytics error: {e}")
            return {}
    
    def _calculate_basic_metrics(self) -> Dict[str, Any]:
        """Calculate basic performance metrics"""
        try:
            perf = self.system_performance
            
            if perf.total_trades == 0:
                return {
                    "total_trades": 0,
                    "win_rate": 0.0,
                    "profit_factor": 0.0,
                    "average_trade": 0.0,
                    "net_profit": 0.0
                }
            
            # Calculate metrics
            winning_trades = [t for t in self.trade_records if t.result == TradeResult.WIN]
            losing_trades = [t for t in self.trade_records if t.result == TradeResult.LOSS]
            
            gross_profit = sum([t.net_profit for t in winning_trades])
            gross_loss = abs(sum([t.net_profit for t in losing_trades]))
            
            return {
                "total_trades": perf.total_trades,
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades),
                "win_rate": perf.win_rate,
                "profit_factor": gross_profit / max(gross_loss, 1),
                "average_trade": perf.net_profit / perf.total_trades,
                "net_profit": perf.net_profit,
                "gross_profit": gross_profit,
                "gross_loss": gross_loss,
                "max_profit": perf.max_profit,
                "max_loss": perf.max_loss
            }
            
        except Exception as e:
            print(f"❌ Basic metrics calculation error: {e}")
            return {}
    
    def _calculate_rule_analytics(self) -> Dict[str, Any]:
        """Calculate rule performance analytics"""
        try:
            rule_analytics = {}
            
            for rule_name, rule_perf in self.rule_performances.items():
                rule_analytics[f"rule_{rule_name}"] = {
                    "total_signals": rule_perf.total_signals,
                    "win_rate": rule_perf.win_rate,
                    "profit_factor": rule_perf.profit_factor,
                    "average_profit": rule_perf.average_profit,
                    "avg_confidence": rule_perf.avg_confidence,
                    "best_trade": rule_perf.best_trade,
                    "worst_trade": rule_perf.worst_trade
                }
            
            # Overall rule effectiveness
            if self.rule_performances:
                avg_rule_win_rate = statistics.mean([rp.win_rate for rp in self.rule_performances.values()])
                avg_rule_profit_factor = statistics.mean([rp.profit_factor for rp in self.rule_performances.values()])
                
                rule_analytics["overall_rule_effectiveness"] = {
                    "average_win_rate": avg_rule_win_rate,
                    "average_profit_factor": avg_rule_profit_factor,
                    "total_rules": len(self.rule_performances),
                    "active_rules": sum(1 for rp in self.rule_performances.values() if rp.total_signals > 0)
                }
            
            return rule_analytics
            
        except Exception as e:
            print(f"❌ Rule analytics calculation error: {e}")
            return {}
    
    def _calculate_risk_metrics(self) -> Dict[str, Any]:
        """Calculate risk management metrics"""
        try:
            perf = self.system_performance
            
            # Drawdown metrics
            risk_metrics = {
                "max_drawdown": perf.max_drawdown,
                "max_drawdown_percentage": perf.max_drawdown_percentage,
                "current_drawdown": perf.current_drawdown,
                "current_drawdown_percentage": (perf.current_drawdown / max(perf.peak_balance, 1)) * 100
            }
            
            # Calculate Sharpe ratio (simplified)
            if len(self.trade_records) > 10:
                trade_returns = [t.net_profit for t in self.trade_records[-30:]]  # Last 30 trades
                if trade_returns:
                    avg_return = statistics.mean(trade_returns)
                    return_std = statistics.stdev(trade_returns) if len(trade_returns) > 1 else 1
                    risk_metrics["sharpe_ratio"] = avg_return / max(return_std, 1)
                else:
                    risk_metrics["sharpe_ratio"] = 0.0
            else:
                risk_metrics["sharpe_ratio"] = 0.0
            
            # Risk-reward ratio
            if perf.total_trades > 0:
                avg_win = abs(perf.max_profit) if perf.max_profit > 0 else 1
                avg_loss = abs(perf.max_loss) if perf.max_loss < 0 else 1
                risk_metrics["risk_reward_ratio"] = avg_win / avg_loss
            else:
                risk_metrics["risk_reward_ratio"] = 1.0
            
            return risk_metrics
            
        except Exception as e:
            print(f"❌ Risk metrics calculation error: {e}")
            return {}
    
    def _calculate_time_analytics(self) -> Dict[str, Any]:
        """Calculate time-based analytics"""
        try:
            time_analytics = {}
            
            # System runtime
            runtime = datetime.now() - self.system_performance.start_time
            time_analytics["system_runtime_hours"] = runtime.total_seconds() / 3600
            time_analytics["system_runtime_days"] = runtime.days
            
            # Trading frequency
            if runtime.total_seconds() > 0:
                trades_per_hour = self.system_performance.total_trades / (runtime.total_seconds() / 3600)
                time_analytics["trades_per_hour"] = trades_per_hour
                time_analytics["trades_per_day"] = trades_per_hour * 24
            else:
                time_analytics["trades_per_hour"] = 0.0
                time_analytics["trades_per_day"] = 0.0
            
            # Average trade duration
            time_analytics["avg_trade_duration_minutes"] = self.system_performance.avg_trade_duration
            time_analytics["avg_trade_duration_hours"] = self.system_performance.avg_trade_duration / 60
            
            return time_analytics
            
        except Exception as e:
            print(f"❌ Time analytics calculation error: {e}")
            return {}
    
    def _calculate_system_health(self) -> Dict[str, Any]:
        """Calculate system health metrics"""
        try:
            health_score = 100.0
            health_factors = []
            
            # Performance factor
            if self.system_performance.total_trades > 10:
                if self.system_performance.win_rate < 0.4:
                    health_score -= 20
                    health_factors.append("Low win rate")
                elif self.system_performance.win_rate > 0.7:
                    health_score += 5
                    health_factors.append("High win rate")
            
            # Drawdown factor
            if self.system_performance.max_drawdown_percentage > 15:
                health_score -= 25
                health_factors.append("High drawdown")
            elif self.system_performance.max_drawdown_percentage < 5:
                health_score += 5
                health_factors.append("Low drawdown")
            
            # Profit factor
            basic_metrics = self._calculate_basic_metrics()
            profit_factor = basic_metrics.get("profit_factor", 1.0)
            if profit_factor < 1.0:
                health_score -= 30
                health_factors.append("Negative profit factor")
            elif profit_factor > 1.5:
                health_score += 10
                health_factors.append("Good profit factor")
            
            # System uptime
            uptime_score = self.system_performance.system_uptime_percentage
            if uptime_score < 90:
                health_score -= 15
                health_factors.append("Low system uptime")
            
            # Bound health score
            health_score = max(0, min(100, health_score))
            self.system_health_score = health_score
            
            return {
                "system_health_score": health_score,
                "health_factors": health_factors,
                "system_uptime_percentage": uptime_score,
                "last_health_check": datetime.now()
            }
            
        except Exception as e:
            print(f"❌ System health calculation error: {e}")
            return {"system_health_score": 50.0, "health_factors": ["Calculation error"]}
    
    def _calculate_benchmark_comparison(self) -> Dict[str, Any]:
        """Calculate benchmark comparison"""
        try:
            benchmarks = {}
            
            # Daily performance vs target
            runtime_days = max(1, (datetime.now() - self.system_performance.start_time).days)
            daily_return_percentage = (self.system_performance.net_profit / runtime_days) / 100  # Simplified
            
            benchmarks["daily_return_vs_target"] = {
                "actual": daily_return_percentage,
                "target": self.benchmarks["daily_target"],
                "achievement": (daily_return_percentage / self.benchmarks["daily_target"]) * 100 if self.benchmarks["daily_target"] > 0 else 0
            }
            
            # Win rate vs target
            benchmarks["win_rate_vs_target"] = {
                "actual": self.system_performance.win_rate * 100,
                "target": self.benchmarks["min_win_rate"],
                "achievement": (self.system_performance.win_rate * 100 / self.benchmarks["min_win_rate"]) * 100 if self.benchmarks["min_win_rate"] > 0 else 0
            }
            
            # Drawdown vs limit
            benchmarks["drawdown_vs_limit"] = {
                "actual": self.system_performance.max_drawdown_percentage,
                "limit": self.benchmarks["max_drawdown_limit"],
                "within_limit": self.system_performance.max_drawdown_percentage <= self.benchmarks["max_drawdown_limit"]
            }
            
            # Overall benchmark score
            achievements = [
                benchmarks["daily_return_vs_target"]["achievement"],
                benchmarks["win_rate_vs_target"]["achievement"]
            ]
            benchmark_score = statistics.mean([min(100, max(0, a)) for a in achievements])
            
            benchmarks["overall_benchmark_score"] = benchmark_score
            
            return benchmarks
            
        except Exception as e:
            print(f"❌ Benchmark comparison error: {e}")
            return {}
    
    # === Public Interface Methods ===
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        try:
            analytics = self.calculate_performance_analytics()
            
            summary = {
                "timestamp": datetime.now(),
                "system_runtime_hours": analytics.get("system_runtime_hours", 0),
                "total_trades": self.system_performance.total_trades,
                "win_rate": self.system_performance.win_rate,
                "net_profit": self.system_performance.net_profit,
                "max_drawdown_percentage": self.system_performance.max_drawdown_percentage,
                "system_health_score": self.system_health_score,
                "active_trades": len(self.active_trades),
                "rule_count": len(self.rule_performances),
                "benchmark_score": analytics.get("overall_benchmark_score", 0)
            }
            
            return summary
            
        except Exception as e:
            print(f"❌ Performance summary error: {e}")
            return {}
    
    def get_rule_performance_report(self) -> Dict[str, Any]:
        """Get detailed rule performance report"""
        try:
            report = {}
            
            for rule_name, rule_perf in self.rule_performances.items():
                report[rule_name] = {
                    "total_signals": rule_perf.total_signals,
                    "win_rate": f"{rule_perf.win_rate:.1%}",
                    "profit_factor": f"{rule_perf.profit_factor:.2f}",
                    "average_profit": f"${rule_perf.average_profit:.2f}",
                    "total_profit": f"${rule_perf.total_profit:.2f}",
                    "total_loss": f"${rule_perf.total_loss:.2f}",
                    "avg_confidence": f"{rule_perf.avg_confidence:.1%}",
                    "best_trade": f"${rule_perf.best_trade:.2f}",
                    "worst_trade": f"${rule_perf.worst_trade:.2f}",
                    "last_signal": rule_perf.last_signal_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "recent_signals": len([s for s in rule_perf.signal_history if s["timestamp"] > datetime.now() - timedelta(hours=24)])
                }
            
            # Summary statistics
            if self.rule_performances:
                all_rules = list(self.rule_performances.values())
                report["summary"] = {
                    "total_rules": len(all_rules),
                    "avg_win_rate": f"{statistics.mean([r.win_rate for r in all_rules]):.1%}",
                    "avg_profit_factor": f"{statistics.mean([r.profit_factor for r in all_rules]):.2f}",
                    "total_signals": sum([r.total_signals for r in all_rules]),
                    "best_performing_rule": max(all_rules, key=lambda x: x.average_profit).rule_name,
                    "most_active_rule": max(all_rules, key=lambda x: x.total_signals).rule_name
                }
            
            return report
            
        except Exception as e:
            print(f"❌ Rule performance report error: {e}")
            return {}
    
    def export_performance_data(self, filename: str = None) -> str:
        """Export performance data to JSON file"""
        try:
            if filename is None:
                filename = f"performance_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "system_performance": {
                    "start_time": self.system_performance.start_time.isoformat(),
                    "total_trades": self.system_performance.total_trades,
                    "winning_trades": self.system_performance.winning_trades,
                    "losing_trades": self.system_performance.losing_trades,
                    "net_profit": self.system_performance.net_profit,
                    "max_drawdown": self.system_performance.max_drawdown,
                    "max_drawdown_percentage": self.system_performance.max_drawdown_percentage,
                    "win_rate": self.system_performance.win_rate,
                    "avg_trade_duration": self.system_performance.avg_trade_duration
                },
                "rule_performances": {
                    rule_name: {
                        "total_signals": rule_perf.total_signals,
                        "successful_signals": rule_perf.successful_signals,
                        "win_rate": rule_perf.win_rate,
                        "profit_factor": rule_perf.profit_factor,
                        "total_profit": rule_perf.total_profit,
                        "total_loss": rule_perf.total_loss,
                        "average_profit": rule_perf.average_profit,
                        "avg_confidence": rule_perf.avg_confidence
                    }
                    for rule_name, rule_perf in self.rule_performances.items()
                },
                "recent_trades": [
                    {
                        "trade_id": trade.trade_id,
                        "timestamp": trade.timestamp.isoformat(),
                        "symbol": trade.symbol,
                        "direction": trade.direction,
                        "lot_size": trade.lot_size,
                        "entry_price": trade.entry_price,
                        "exit_price": trade.exit_price,
                        "net_profit": trade.net_profit,
                        "result": trade.result.value,
                        "rule_triggered": trade.rule_triggered,
                        "confidence_level": trade.confidence_level
                    }
                    for trade in self.trade_records[-50:]  # Last 50 trades
                ],
                "performance_analytics": self.calculate_performance_analytics()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"📈 Performance data exported to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return ""

# Mock Performance Tracker for Testing
class MockPerformanceTracker:
    """Mock Performance Tracker for testing purposes"""
    
    def __init__(self):
        self.track_count = 0
        self.trade_count = 0
        self.mock_performance = {
            "total_trades": 25,
            "win_rate": 0.68,
            "net_profit": 450.75,
            "max_drawdown_percentage": 8.5,
            "system_health_score": 85.0
        }
        print("🧪 Mock Performance Tracker initialized for testing")
    
    def track_decision(self, decision_result, success: bool, profit: float = 0.0):
        """Mock decision tracking"""
        self.track_count += 1
        print(f"🧪 Mock tracking: {decision_result.rule_name}, success={success}, profit=${profit:.2f}")
    
    def start_trade_tracking(self, symbol: str, direction: str, lot_size: float,
                           entry_price: float, rule_triggered: str = "", 
                           confidence: float = 0.0, market_condition: str = "",
                           reasoning: str = "") -> str:
        """Mock trade tracking start"""
        self.trade_count += 1
        trade_id = f"T{self.trade_count:06d}"
        print(f"🧪 Mock trade started: {trade_id} - {direction} {lot_size} {symbol}")
        return trade_id
    
    def complete_trade_tracking(self, trade_id: str, exit_price: float,
                              profit: float, commission: float = 0.0,
                              swap: float = 0.0) -> bool:
        """Mock trade tracking completion"""
        net_profit = profit + commission + swap
        print(f"🧪 Mock trade completed: {trade_id}, P&L: ${net_profit:.2f}")
        return True
    
    def get_decision_outcome(self, decision_result) -> Optional[bool]:
        """Mock decision outcome"""
        # Return success based on confidence
        return decision_result.confidence > 0.6
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Mock performance summary"""
        return self.mock_performance.copy()
    
    def calculate_performance_analytics(self) -> Dict[str, Any]:
        """Mock performance analytics"""
        return {
            "total_trades": self.mock_performance["total_trades"],
            "win_rate": self.mock_performance["win_rate"],
            "profit_factor": 1.45,
            "sharpe_ratio": 0.85,
            "system_health_score": self.mock_performance["system_health_score"],
            "benchmark_score": 78.5
        }

# Test function
def test_performance_tracker():
    """Test the performance tracker"""
    print("🧪 Testing Performance Tracker...")
    
    # Test with mock tracker
    mock_tracker = MockPerformanceTracker()
    
    # Mock decision result
    class MockDecisionResult:
        def __init__(self, rule_name, confidence):
            self.rule_name = rule_name
            self.confidence = confidence
            self.timestamp = datetime.now()
            self.decision = type('obj', (object,), {'value': 'BUY'})()
            self.reasoning = "Test decision"
    
    # Test decision tracking
    print("\n--- Testing Decision Tracking ---")
    for i in range(5):
        decision = MockDecisionResult(f"test_rule_{i%3}", 0.5 + i*0.1)
        success = i % 2 == 0
        profit = (-20, 15, -10, 25, 5)[i]
        
        mock_tracker.track_decision(decision, success, profit)
    
    # Test trade tracking
    print("\n--- Testing Trade Tracking ---")
    trade_id = mock_tracker.start_trade_tracking(
        symbol="XAUUSD",
        direction="BUY",
        lot_size=0.01,
        entry_price=2020.50,
        rule_triggered="trend_following",
        confidence=0.8
    )
    
    # Complete the trade
    mock_tracker.complete_trade_tracking(
        trade_id=trade_id,
        exit_price=2025.30,
        profit=48.0,
        commission=-2.0
    )
    
    # Test performance summary
    print("\n--- Performance Summary ---")
    summary = mock_tracker.get_performance_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Test analytics
    print("\n--- Performance Analytics ---")
    analytics = mock_tracker.calculate_performance_analytics()
    for key, value in analytics.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Performance Tracker test completed")

if __name__ == "__main__":
    test_performance_tracker()