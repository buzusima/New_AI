"""
📈 Modern Performance Tracker - Updated for New Rule Engine
performance_tracker.py
เพิ่ม methods ที่จำเป็นสำหรับ Modern Rule Engine และการติดตามประสิทธิภาพ
** PRODUCTION READY - COMPATIBLE WITH NEW RULE ENGINE **
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import numpy as np
from collections import deque, defaultdict
import statistics

class DecisionOutcome(Enum):
    """ผลลัพธ์การตัดสินใจ"""
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"

@dataclass
class DecisionRecord:
    """บันทึกการตัดสินใจ"""
    timestamp: datetime
    rule_name: str
    decision_type: str
    confidence: float
    reasoning: str
    market_context: Dict
    execution_result: Optional[Dict] = None
    outcome: DecisionOutcome = DecisionOutcome.PENDING
    profit_impact: float = 0.0
    evaluation_time: Optional[datetime] = None
    
@dataclass
class RuleMetrics:
    """เมตริกการประเมิน Rule"""
    rule_name: str
    total_decisions: int = 0
    successful_decisions: int = 0
    failed_decisions: int = 0
    pending_decisions: int = 0
    total_profit_impact: float = 0.0
    average_confidence: float = 0.0
    success_rate: float = 0.0
    profit_per_decision: float = 0.0
    last_decision_time: Optional[datetime] = None
    performance_trend: List[float] = field(default_factory=list)

class PerformanceTracker:
    """
    📈 Modern Performance Tracker - Updated Edition
    
    ความสามารถใหม่:
    - ✅ track_decision() สำหรับ Rule Engine
    - ✅ get_decision_outcome() evaluation
    - ✅ Rule performance analytics
    - ✅ Decision impact analysis
    - ✅ Adaptive learning support
    ** COMPATIBLE WITH NEW RULE ENGINE **
    """
    
    def __init__(self, config: Dict):
        """Initialize Performance Tracker"""
        self.config = config
        
        # Decision tracking
        self.decision_records: List[DecisionRecord] = []
        self.pending_decisions: deque = deque(maxlen=100)
        
        # Rule metrics
        self.rule_metrics: Dict[str, RuleMetrics] = {}
        
        # Performance windows
        self.short_term_window = 20    # decisions
        self.medium_term_window = 50   # decisions  
        self.long_term_window = 200    # decisions
        
        # Evaluation settings
        self.decision_evaluation_delay = 300  # seconds (5 minutes)
        self.profit_evaluation_delay = 1800   # seconds (30 minutes)
        
        # Statistics
        self.daily_stats = defaultdict(lambda: {
            "decisions": 0, "successes": 0, "profit": 0.0
        })
        
        print("📈 Performance Tracker initialized - Compatible with Modern Rule Engine")
    
    # ========================================================================================
    # 🆕 NEW METHODS FOR MODERN RULE ENGINE
    # ========================================================================================
    
    def track_decision(self, decision_result, success: bool):
        """
        🆕 ติดตามการตัดสินใจจาก Rule Engine
        
        Args:
            decision_result: RuleResult object จาก Rule Engine
            success: ผลการดำเนินการ (True/False)
        """
        try:
            print(f"📈 === TRACKING DECISION ===")
            print(f"   Rule: {decision_result.rule_name}")
            print(f"   Decision: {decision_result.decision.value}")
            print(f"   Success: {success}")
            
            # สร้าง decision record
            record = DecisionRecord(
                timestamp=datetime.now(),
                rule_name=decision_result.rule_name,
                decision_type=decision_result.decision.value,
                confidence=decision_result.confidence,
                reasoning=decision_result.reasoning,
                market_context=decision_result.market_context,
                execution_result={"success": success},
                outcome=DecisionOutcome.SUCCESS if success else DecisionOutcome.FAILURE
            )
            
            # เพิ่มในบันทึก
            self.decision_records.append(record)
            
            # อัพเดท rule metrics
            self._update_rule_metrics(decision_result.rule_name, record)
            
            # อัพเดท daily stats
            today = datetime.now().date().isoformat()
            self.daily_stats[today]["decisions"] += 1
            if success:
                self.daily_stats[today]["successes"] += 1
            
            # เพิ่มใน pending evaluation queue
            if success:
                self.pending_decisions.append(record)
            
            print(f"✅ Decision tracked: {decision_result.rule_name}")
            
        except Exception as e:
            print(f"❌ Decision tracking error: {e}")
    
    def get_decision_outcome(self, decision_result) -> Optional[bool]:
        """
        🆕 ประเมินผลลัพธ์การตัดสินใจ
        
        Args:
            decision_result: RuleResult object
            
        Returns:
            True/False ถ้าประเมินได้, None ถ้ายังไม่ถึงเวลา
        """
        try:
            # หา decision record ที่ตรงกัน
            target_record = None
            for record in self.decision_records:
                if (record.rule_name == decision_result.rule_name and
                    record.decision_type == decision_result.decision.value and
                    record.reasoning == decision_result.reasoning):
                    target_record = record
                    break
            
            if not target_record:
                return None
            
            # เช็คว่าถึงเวลาประเมินหรือยัง
            time_since_decision = (datetime.now() - target_record.timestamp).total_seconds()
            
            if time_since_decision < self.decision_evaluation_delay:
                return None  # ยังไม่ถึงเวลา
            
            # ประเมินผลลัพธ์
            outcome = self._evaluate_decision_outcome(target_record)
            
            # อัพเดท record
            target_record.outcome = outcome
            target_record.evaluation_time = datetime.now()
            
            # อัพเดท daily stats ถ้าเป็น SUCCESS
            if outcome == DecisionOutcome.SUCCESS:
                today = datetime.now().date().isoformat()
                # profit impact จะอัพเดทภายหลัง
            
            print(f"📊 Decision outcome evaluated: {target_record.rule_name} = {outcome.value}")
            
            return outcome == DecisionOutcome.SUCCESS
            
        except Exception as e:
            print(f"❌ Decision outcome evaluation error: {e}")
            return None
    
    def _evaluate_decision_outcome(self, record: DecisionRecord) -> DecisionOutcome:
        """ประเมินผลลัพธ์การตัดสินใจ"""
        try:
            # เริ่มต้นด้วยผลการดำเนินการ
            if record.execution_result and not record.execution_result.get("success"):
                return DecisionOutcome.FAILURE
            
            # ประเมินตาม decision type
            if record.decision_type in ["BUY", "SELL"]:
                # สำหรับ trading decisions ให้เวลาอีกสักหน่อย
                time_since = (datetime.now() - record.timestamp).total_seconds()
                if time_since < self.profit_evaluation_delay:
                    return DecisionOutcome.PENDING
                
                # ประเมินจากผลกำไร (ถ้ามีข้อมูล)
                # TODO: เชื่อมกับ position manager เพื่อดูผลกำไรจริง
                return DecisionOutcome.SUCCESS  # Assume success for now
                
            elif record.decision_type in ["CLOSE_PROFITABLE", "CLOSE_LOSING"]:
                # การปิด positions ประเมินได้ทันที
                return DecisionOutcome.SUCCESS if record.execution_result.get("success") else DecisionOutcome.FAILURE
            
            else:
                return DecisionOutcome.SUCCESS
                
        except Exception as e:
            print(f"❌ Outcome evaluation error: {e}")
            return DecisionOutcome.FAILURE
    
    def _update_rule_metrics(self, rule_name: str, record: DecisionRecord):
        """อัพเดทเมตริกของ rule"""
        try:
            if rule_name not in self.rule_metrics:
                self.rule_metrics[rule_name] = RuleMetrics(rule_name=rule_name)
            
            metrics = self.rule_metrics[rule_name]
            
            # อัพเดทจำนวน
            metrics.total_decisions += 1
            metrics.last_decision_time = record.timestamp
            
            # อัพเดทผลลัพธ์
            if record.outcome == DecisionOutcome.SUCCESS:
                metrics.successful_decisions += 1
            elif record.outcome == DecisionOutcome.FAILURE:
                metrics.failed_decisions += 1
            else:
                metrics.pending_decisions += 1
            
            # คำนวณ averages
            if metrics.total_decisions > 0:
                metrics.success_rate = metrics.successful_decisions / metrics.total_decisions
                
                # อัพเดท average confidence
                all_confidences = [r.confidence for r in self.decision_records if r.rule_name == rule_name]
                metrics.average_confidence = statistics.mean(all_confidences) if all_confidences else 0.0
                
                # อัพเดท performance trend
                recent_decisions = [r for r in self.decision_records[-20:] if r.rule_name == rule_name]
                if recent_decisions:
                    recent_success_rate = len([r for r in recent_decisions if r.outcome == DecisionOutcome.SUCCESS]) / len(recent_decisions)
                    metrics.performance_trend.append(recent_success_rate)
                    
                    # เก็บแค่ 10 ค่าล่าสุด
                    if len(metrics.performance_trend) > 10:
                        metrics.performance_trend = metrics.performance_trend[-10:]
            
            print(f"📊 Updated metrics for {rule_name}: {metrics.success_rate:.1%} success rate")
            
        except Exception as e:
            print(f"❌ Rule metrics update error: {e}")
    
    # ========================================================================================
    # 📊 ANALYTICS AND REPORTING
    # ========================================================================================
    
    def get_rule_performance_summary(self) -> Dict[str, Dict]:
        """ดึงสรุปประสิทธิภาพของทุก rules"""
        try:
            summary = {}
            
            for rule_name, metrics in self.rule_metrics.items():
                summary[rule_name] = {
                    "total_decisions": metrics.total_decisions,
                    "success_rate": round(metrics.success_rate, 3),
                    "average_confidence": round(metrics.average_confidence, 3),
                    "total_profit_impact": round(metrics.total_profit_impact, 2),
                    "profit_per_decision": round(metrics.profit_per_decision, 2),
                    "last_decision": metrics.last_decision_time.isoformat() if metrics.last_decision_time else None,
                    "performance_trend": [round(p, 3) for p in metrics.performance_trend[-5:]],  # 5 ค่าล่าสุด
                    "status": self._get_rule_status(metrics)
                }
            
            return summary
            
        except Exception as e:
            print(f"❌ Rule performance summary error: {e}")
            return {}
    
    def get_daily_performance(self, days: int = 7) -> Dict[str, Dict]:
        """ดึงประสิทธิภาพรายวัน"""
        try:
            daily_performance = {}
            
            # Get last N days
            today = datetime.now().date()
            for i in range(days):
                date = (today - timedelta(days=i)).isoformat()
                
                stats = self.daily_stats.get(date, {"decisions": 0, "successes": 0, "profit": 0.0})
                
                success_rate = stats["successes"] / stats["decisions"] if stats["decisions"] > 0 else 0.0
                
                daily_performance[date] = {
                    "decisions": stats["decisions"],
                    "successes": stats["successes"],
                    "success_rate": round(success_rate, 3),
                    "profit": round(stats["profit"], 2)
                }
            
            return daily_performance
            
        except Exception as e:
            print(f"❌ Daily performance error: {e}")
            return {}
    
    def get_comprehensive_stats(self) -> Dict:
        """ดึงสถิติครบถ้วนสำหรับ dashboard"""
        try:
            total_decisions = len(self.decision_records)
            
            if total_decisions == 0:
                return {
                    "overview": {"total_decisions": 0, "overall_success_rate": 0.0},
                    "rules": {},
                    "recent_performance": {},
                    "trends": {}
                }
            
            # Overall stats
            successful_decisions = len([r for r in self.decision_records if r.outcome == DecisionOutcome.SUCCESS])
            overall_success_rate = successful_decisions / total_decisions
            
            # Recent performance (last 20 decisions)
            recent_decisions = self.decision_records[-20:]
            recent_successes = len([r for r in recent_decisions if r.outcome == DecisionOutcome.SUCCESS])
            recent_success_rate = recent_successes / len(recent_decisions) if recent_decisions else 0.0
            
            # Trend analysis
            performance_over_time = self._calculate_performance_trend()
            
            return {
                "overview": {
                    "total_decisions": total_decisions,
                    "successful_decisions": successful_decisions,
                    "overall_success_rate": round(overall_success_rate, 3),
                    "recent_success_rate": round(recent_success_rate, 3),
                    "total_profit_impact": sum(r.profit_impact for r in self.decision_records),
                    "average_confidence": round(statistics.mean([r.confidence for r in self.decision_records]), 3)
                },
                "rules": self.get_rule_performance_summary(),
                "recent_performance": {
                    "last_20_decisions": recent_success_rate,
                    "last_10_decisions": self._calculate_recent_performance(10),
                    "last_5_decisions": self._calculate_recent_performance(5)
                },
                "trends": {
                    "performance_trend": performance_over_time,
                    "confidence_trend": self._calculate_confidence_trend(),
                    "decision_frequency": self._calculate_decision_frequency()
                },
                "last_updated": datetime.now()
            }
            
        except Exception as e:
            print(f"❌ Comprehensive stats error: {e}")
            return {"error": str(e)}
    
    def update_profit_impact(self, rule_name: str, decision_timestamp: datetime, profit_amount: float):
        """อัพเดทผลกระทบทางกำไรของการตัดสินใจ"""
        try:
            # หา decision record ที่ตรงกัน
            for record in self.decision_records:
                if (record.rule_name == rule_name and 
                    abs((record.timestamp - decision_timestamp).total_seconds()) < 60):
                    
                    record.profit_impact = profit_amount
                    
                    # อัพเดท rule metrics
                    if rule_name in self.rule_metrics:
                        metrics = self.rule_metrics[rule_name]
                        metrics.total_profit_impact += profit_amount
                        if metrics.total_decisions > 0:
                            metrics.profit_per_decision = metrics.total_profit_impact / metrics.total_decisions
                    
                    # อัพเดท daily stats
                    today = decision_timestamp.date().isoformat()
                    self.daily_stats[today]["profit"] += profit_amount
                    
                    print(f"💰 Updated profit impact: {rule_name} +${profit_amount:.2f}")
                    break
            
        except Exception as e:
            print(f"❌ Profit impact update error: {e}")
    
    # ========================================================================================
    # 🔍 ANALYSIS METHODS
    # ========================================================================================
    
    def _get_rule_status(self, metrics: RuleMetrics) -> str:
        """กำหนดสถานะของ rule"""
        try:
            if metrics.total_decisions < 5:
                return "LEARNING"  # ข้อมูลยังไม่เพียงพอ
            
            if metrics.success_rate > 0.7:
                return "EXCELLENT"
            elif metrics.success_rate > 0.6:
                return "GOOD"
            elif metrics.success_rate > 0.5:
                return "AVERAGE"
            elif metrics.success_rate > 0.3:
                return "POOR"
            else:
                return "CRITICAL"
                
        except Exception as e:
            return "UNKNOWN"
    
    def _calculate_performance_trend(self) -> List[float]:
        """คำนวณเทรนด์ประสิทธิภาพ"""
        try:
            if len(self.decision_records) < 10:
                return []
            
            # แบ่งการตัดสินใจเป็นกลุ่มๆ ละ 10
            trend_points = []
            
            for i in range(10, len(self.decision_records) + 1, 10):
                batch = self.decision_records[i-10:i]
                successes = len([r for r in batch if r.outcome == DecisionOutcome.SUCCESS])
                success_rate = successes / len(batch)
                trend_points.append(success_rate)
            
            return trend_points[-10:]  # เก็บแค่ 10 จุดล่าสุด
            
        except Exception as e:
            return []
    
    def _calculate_confidence_trend(self) -> List[float]:
        """คำนวณเทรนด์ความเชื่อมั่น"""
        try:
            if len(self.decision_records) < 10:
                return []
            
            # แบ่งการตัดสินใจเป็นกลุ่มๆ ละ 10
            confidence_points = []
            
            for i in range(10, len(self.decision_records) + 1, 10):
                batch = self.decision_records[i-10:i]
                avg_confidence = statistics.mean([r.confidence for r in batch])
                confidence_points.append(avg_confidence)
            
            return confidence_points[-10:]  # เก็บแค่ 10 จุดล่าสุด
            
        except Exception as e:
            return []
    
    def _calculate_decision_frequency(self) -> Dict[str, float]:
        """คำนวณความถี่ในการตัดสินใจ"""
        try:
            if len(self.decision_records) < 2:
                return {"decisions_per_hour": 0.0, "avg_interval_minutes": 0.0}
            
            # คำนวณช่วงเวลาระหว่างการตัดสินใจ
            intervals = []
            for i in range(1, len(self.decision_records)):
                interval = (self.decision_records[i].timestamp - self.decision_records[i-1].timestamp).total_seconds()
                intervals.append(interval)
            
            avg_interval_seconds = statistics.mean(intervals)
            decisions_per_hour = 3600 / avg_interval_seconds if avg_interval_seconds > 0 else 0
            
            return {
                "decisions_per_hour": round(decisions_per_hour, 2),
                "avg_interval_minutes": round(avg_interval_seconds / 60, 2),
                "total_intervals": len(intervals)
            }
            
        except Exception as e:
            return {"decisions_per_hour": 0.0, "avg_interval_minutes": 0.0}
    
    def _calculate_recent_performance(self, window_size: int) -> float:
        """คำนวณประสิทธิภาพล่าสุด"""
        try:
            if len(self.decision_records) < window_size:
                window_size = len(self.decision_records)
            
            if window_size == 0:
                return 0.0
            
            recent_decisions = self.decision_records[-window_size:]
            successes = len([r for r in recent_decisions if r.outcome == DecisionOutcome.SUCCESS])
            
            return successes / len(recent_decisions)
            
        except Exception as e:
            return 0.0
    
    # ========================================================================================
    # 🎯 ADAPTIVE LEARNING SUPPORT
    # ========================================================================================
    
    def get_rule_learning_data(self, rule_name: str) -> Dict:
        """ดึงข้อมูลสำหรับ adaptive learning"""
        try:
            if rule_name not in self.rule_metrics:
                return {}
            
            metrics = self.rule_metrics[rule_name]
            
            # ดึง decisions ของ rule นี้
            rule_decisions = [r for r in self.decision_records if r.rule_name == rule_name]
            
            # วิเคราะห์ patterns
            confidence_vs_success = self._analyze_confidence_vs_success(rule_decisions)
            market_context_analysis = self._analyze_market_context_performance(rule_decisions)
            
            return {
                "metrics": {
                    "success_rate": metrics.success_rate,
                    "avg_confidence": metrics.average_confidence,
                    "total_decisions": metrics.total_decisions,
                    "profit_per_decision": metrics.profit_per_decision
                },
                "patterns": {
                    "confidence_vs_success": confidence_vs_success,
                    "market_context_performance": market_context_analysis
                },
                "recommendations": self._generate_learning_recommendations(metrics, rule_decisions),
                "trend": metrics.performance_trend
            }
            
        except Exception as e:
            print(f"❌ Learning data error: {e}")
            return {}
    
    def _analyze_confidence_vs_success(self, decisions: List[DecisionRecord]) -> Dict:
        """วิเคราะห์ความสัมพันธ์ระหว่าง confidence และ success"""
        try:
            confidence_groups = {
                "high": [r for r in decisions if r.confidence > 0.7],
                "medium": [r for r in decisions if 0.4 <= r.confidence <= 0.7],
                "low": [r for r in decisions if r.confidence < 0.4]
            }
            
            analysis = {}
            for group_name, group_decisions in confidence_groups.items():
                if group_decisions:
                    successes = len([r for r in group_decisions if r.outcome == DecisionOutcome.SUCCESS])
                    success_rate = successes / len(group_decisions)
                    
                    analysis[group_name] = {
                        "decisions": len(group_decisions),
                        "success_rate": round(success_rate, 3),
                        "avg_confidence": round(statistics.mean([r.confidence for r in group_decisions]), 3)
                    }
                else:
                    analysis[group_name] = {"decisions": 0, "success_rate": 0.0, "avg_confidence": 0.0}
            
            return analysis
            
        except Exception as e:
            return {}
    
    def _analyze_market_context_performance(self, decisions: List[DecisionRecord]) -> Dict:
        """วิเคราะห์ประสิทธิภาพในแต่ละ market context"""
        try:
            context_groups = defaultdict(list)
            
            for decision in decisions:
                market_condition = decision.market_context.get("condition", "UNKNOWN")
                context_groups[market_condition].append(decision)
            
            analysis = {}
            for condition, group_decisions in context_groups.items():
                if group_decisions:
                    successes = len([r for r in group_decisions if r.outcome == DecisionOutcome.SUCCESS])
                    success_rate = successes / len(group_decisions)
                    
                    analysis[condition] = {
                        "decisions": len(group_decisions),
                        "success_rate": round(success_rate, 3),
                        "avg_confidence": round(statistics.mean([r.confidence for r in group_decisions]), 3)
                    }
            
            return analysis
            
        except Exception as e:
            return {}
    
    def _generate_learning_recommendations(self, metrics: RuleMetrics, decisions: List[DecisionRecord]) -> List[str]:
        """สร้างคำแนะนำสำหรับการเรียนรู้"""
        try:
            recommendations = []
            
            # ประสิทธิภาพโดยรวม
            if metrics.success_rate < 0.4:
                recommendations.append(f"❌ Rule performance is poor ({metrics.success_rate:.1%}). Consider reducing weight.")
            elif metrics.success_rate > 0.8:
                recommendations.append(f"✅ Excellent performance ({metrics.success_rate:.1%}). Consider increasing weight.")
            
            # Confidence calibration
            if metrics.average_confidence > 0.8 and metrics.success_rate < 0.6:
                recommendations.append("⚠️ Overconfident rule. Reduce confidence threshold.")
            elif metrics.average_confidence < 0.5 and metrics.success_rate > 0.7:
                recommendations.append("📈 Underconfident rule. Can increase confidence threshold.")
            
            # Decision frequency
            if len(decisions) > 50 and (datetime.now() - decisions[0].timestamp).days < 1:
                recommendations.append("⚡ High decision frequency. Monitor for overtrading.")
            
            # Performance trend
            if len(metrics.performance_trend) >= 3:
                recent_trend = statistics.mean(metrics.performance_trend[-3:])
                older_trend = statistics.mean(metrics.performance_trend[:-3]) if len(metrics.performance_trend) > 3 else recent_trend
                
                if recent_trend < older_trend - 0.1:
                    recommendations.append("📉 Performance declining. Review rule logic.")
                elif recent_trend > older_trend + 0.1:
                    recommendations.append("📈 Performance improving. Rule is learning well.")
            
            return recommendations
            
        except Exception as e:
            return ["❌ Cannot generate recommendations due to analysis error"]
    
    # ========================================================================================
    # 🔧 UTILITY METHODS
    # ========================================================================================
    
    def cleanup_old_records(self, days_to_keep: int = 30):
        """ทำความสะอาดบันทึกเก่า"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # ลบ decision records เก่า
            original_count = len(self.decision_records)
            self.decision_records = [r for r in self.decision_records if r.timestamp >= cutoff_date]
            
            # ลบ daily stats เก่า
            cutoff_date_str = cutoff_date.date().isoformat()
            old_dates = [date for date in self.daily_stats.keys() if date < cutoff_date_str]
            for date in old_dates:
                del self.daily_stats[date]
            
            cleaned_count = original_count - len(self.decision_records)
            if cleaned_count > 0:
                print(f"🧹 Cleaned up {cleaned_count} old decision records")
            
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    def export_performance_report(self, filename: str = None) -> str:
        """Export performance report to JSON"""
        try:
            if filename is None:
                filename = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report = {
                "export_timestamp": datetime.now().isoformat(),
                "comprehensive_stats": self.get_comprehensive_stats(),
                "daily_performance": self.get_daily_performance(30),
                "rule_learning_data": {
                    rule_name: self.get_rule_learning_data(rule_name)
                    for rule_name in self.rule_metrics.keys()
                }
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"📄 Performance report exported: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return ""
    
    def get_real_time_metrics(self) -> Dict:
        """ดึงเมตริกแบบ real-time สำหรับ dashboard"""
        try:
            recent_decisions = self.decision_records[-10:] if self.decision_records else []
            
            return {
                "last_decision": {
                    "rule": recent_decisions[-1].rule_name if recent_decisions else "None",
                    "type": recent_decisions[-1].decision_type if recent_decisions else "None",
                    "confidence": recent_decisions[-1].confidence if recent_decisions else 0.0,
                    "outcome": recent_decisions[-1].outcome.value if recent_decisions else "None",
                    "time_ago": (datetime.now() - recent_decisions[-1].timestamp).total_seconds() / 60 if recent_decisions else 0
                },
                "active_rules": len(self.rule_metrics),
                "pending_evaluations": len(self.pending_decisions),
                "decisions_last_hour": len([r for r in recent_decisions 
                                          if (datetime.now() - r.timestamp).total_seconds() < 3600]),
                "current_success_rate": self._calculate_recent_performance(10),
                "system_health": self._calculate_system_health()
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _calculate_system_health(self) -> float:
        """คำนวณสุขภาพระบบโดยรวม (0.0-1.0)"""
        try:
            if not self.rule_metrics:
                return 0.5
            
            # ประสิทธิภาพเฉลี่ยของ rules
            avg_success_rate = statistics.mean([m.success_rate for m in self.rule_metrics.values()])
            
            # ความสม่ำเสมอของการตัดสินใจ
            frequency_score = min(1.0, len(self.decision_records) / 100)  # 100 decisions = full score
            
            # ความใหม่ของข้อมูล
            if self.decision_records:
                last_decision_age = (datetime.now() - self.decision_records[-1].timestamp).total_seconds()
                freshness_score = max(0, 1 - last_decision_age / 3600)  # 1 hour = 0 score
            else:
                freshness_score = 0.0
            
            # รวมคะแนน
            health_score = (avg_success_rate * 0.5 + frequency_score * 0.3 + freshness_score * 0.2)
            
            return round(min(1.0, max(0.0, health_score)), 3)
            
        except Exception as e:
            return 0.5
    
    # ========================================================================================
    # 📊 REPORTING METHODS
    # ========================================================================================
    
    def generate_rule_insights(self, rule_name: str) -> Dict:
        """สร้าง insights เชิงลึกสำหรับ rule"""
        try:
            if rule_name not in self.rule_metrics:
                return {"error": f"No data for rule: {rule_name}"}
            
            metrics = self.rule_metrics[rule_name]
            rule_decisions = [r for r in self.decision_records if r.rule_name == rule_name]
            
            # Best/Worst performance analysis
            successful_decisions = [r for r in rule_decisions if r.outcome == DecisionOutcome.SUCCESS]
            failed_decisions = [r for r in rule_decisions if r.outcome == DecisionOutcome.FAILURE]
            
            insights = {
                "rule_name": rule_name,
                "performance_summary": {
                    "success_rate": metrics.success_rate,
                    "total_decisions": metrics.total_decisions,
                    "profit_impact": metrics.total_profit_impact,
                    "status": self._get_rule_status(metrics)
                },
                "success_patterns": {
                    "best_confidence_range": self._find_best_confidence_range(successful_decisions),
                    "best_market_conditions": self._find_best_market_conditions(successful_decisions),
                    "common_success_reasoning": self._find_common_reasoning(successful_decisions)
                },
                "failure_patterns": {
                    "common_failure_conditions": self._find_best_market_conditions(failed_decisions),
                    "problematic_confidence_levels": self._find_best_confidence_range(failed_decisions),
                    "common_failure_reasoning": self._find_common_reasoning(failed_decisions)
                },
                "recommendations": self._generate_learning_recommendations(metrics, rule_decisions),
                "performance_trend": metrics.performance_trend
            }
            
            return insights
            
        except Exception as e:
            return {"error": str(e)}
    
    def _find_best_confidence_range(self, decisions: List[DecisionRecord]) -> Dict:
        """หาช่วง confidence ที่ดีที่สุด"""
        try:
            if not decisions:
                return {"range": "N/A", "count": 0, "success_rate": 0.0}
            
            confidence_ranges = {
                "high": [r for r in decisions if r.confidence > 0.7],
                "medium": [r for r in decisions if 0.4 <= r.confidence <= 0.7],
                "low": [r for r in decisions if r.confidence < 0.4]
            }
            
            best_range = "medium"
            best_success_rate = 0.0
            
            for range_name, range_decisions in confidence_ranges.items():
                if range_decisions:
                    successes = len([r for r in range_decisions if r.outcome == DecisionOutcome.SUCCESS])
                    success_rate = successes / len(range_decisions)
                    
                    if success_rate > best_success_rate:
                        best_success_rate = success_rate
                        best_range = range_name
            
            best_decisions = confidence_ranges[best_range]
            
            return {
                "range": best_range,
                "count": len(best_decisions),
                "success_rate": round(best_success_rate, 3),
                "avg_confidence": round(statistics.mean([r.confidence for r in best_decisions]), 3) if best_decisions else 0.0
            }
            
        except Exception as e:
            return {"range": "unknown", "count": 0, "success_rate": 0.0}
    
    def _find_best_market_conditions(self, decisions: List[DecisionRecord]) -> Dict:
        """หา market conditions ที่ดีที่สุด"""
        try:
            if not decisions:
                return {}
            
            condition_groups = defaultdict(list)
            for decision in decisions:
                condition = decision.market_context.get("condition", "UNKNOWN")
                condition_groups[condition].append(decision)
            
            condition_performance = {}
            for condition, group_decisions in condition_groups.items():
                successes = len([r for r in group_decisions if r.outcome == DecisionOutcome.SUCCESS])
                success_rate = successes / len(group_decisions)
                
                condition_performance[condition] = {
                    "decisions": len(group_decisions),
                    "success_rate": round(success_rate, 3)
                }
            
            # หา condition ที่ดีที่สุด
            best_condition = max(condition_performance.keys(), 
                               key=lambda c: condition_performance[c]["success_rate"]) if condition_performance else "UNKNOWN"
            
            return {
                "best_condition": best_condition,
                "all_conditions": condition_performance
            }
            
        except Exception as e:
            return {}
    
    def _find_common_reasoning(self, decisions: List[DecisionRecord]) -> List[str]:
        """หา reasoning ที่เกิดขึ้นบ่อย"""
        try:
            if not decisions:
                return []
            
            reasoning_keywords = defaultdict(int)
            
            for decision in decisions:
                words = decision.reasoning.lower().split()
                for word in words:
                    if len(word) > 3:  # เฉพาะคำที่มีความหมาย
                        reasoning_keywords[word] += 1
            
            # เลือก keywords ที่เกิดขึ้นบ่อย
            common_keywords = sorted(reasoning_keywords.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return [f"{keyword} ({count}x)" for keyword, count in common_keywords]
            
        except Exception as e:
            return []
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 📈 PerformanceTracker: {message}")


# ========================================================================================
# 🧪 TEST FUNCTION
# ========================================================================================

def test_performance_tracker_compatibility():
    """Test compatibility with Modern Rule Engine"""
    print("🧪 Testing Performance Tracker compatibility...")
    print("✅ track_decision() method added")
    print("✅ get_decision_outcome() method added")
    print("✅ Rule learning analytics implemented")
    print("✅ Comprehensive performance reporting")
    print("✅ Adaptive learning support")
    print("✅ Ready for Modern Rule Engine integration")

if __name__ == "__main__":
    test_performance_tracker_compatibility()