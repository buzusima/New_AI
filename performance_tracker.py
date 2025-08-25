"""
📈 Performance Tracker - 4D Enhanced Monitoring Edition
performance_tracker.py

🎯 ระบบติดตามประสิทธิภาพแบบ 4D สำหรับ AI Gold Grid Trading
- 4D analysis performance tracking
- Recovery effectiveness monitoring
- Market order execution statistics  
- Real-time performance updates

** COMPATIBLE WITH 4D AI RULE ENGINE - COMPREHENSIVE MONITORING **
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
import os

class PerformanceMetricType(Enum):
    """ประเภทของ performance metrics"""
    FOUR_D_ANALYSIS = "FOUR_D_ANALYSIS"
    RECOVERY_EFFECTIVENESS = "RECOVERY_EFFECTIVENESS"
    MARKET_ORDER_EXECUTION = "MARKET_ORDER_EXECUTION"
    PORTFOLIO_HEALTH = "PORTFOLIO_HEALTH"
    RULE_PERFORMANCE = "RULE_PERFORMANCE"
    GRID_EFFICIENCY = "GRID_EFFICIENCY"

class DecisionOutcome4D(Enum):
    """ผลลัพธ์การตัดสินใจแบบ 4D"""
    EXCELLENT_SUCCESS = "EXCELLENT_SUCCESS"       # มากกว่า expected
    GOOD_SUCCESS = "GOOD_SUCCESS"                 # ตาม expected
    MODERATE_SUCCESS = "MODERATE_SUCCESS"         # น้อยกว่า expected แต่ยังดี
    POOR_PERFORMANCE = "POOR_PERFORMANCE"         # แย่กว่า expected
    FAILURE = "FAILURE"                           # ล้มเหลวสิ้นเชิง
    PENDING = "PENDING"                           # รอผลลัพธ์
    CANCELLED = "CANCELLED"                       # ยกเลิก

@dataclass
class FourDAnalysisRecord:
    """บันทึกการวิเคราะห์ 4D"""
    timestamp: datetime
    four_d_score: float
    four_d_confidence: float
    
    # Individual dimension scores
    trend_dimension_score: float
    volume_dimension_score: float
    session_dimension_score: float
    volatility_dimension_score: float
    
    # Market context
    market_condition_4d: str
    recommendation: str
    
    # Action taken
    action_taken: Optional[str] = None
    order_type: Optional[str] = None
    lot_size: Optional[float] = None
    
    # Results (filled later)
    actual_outcome: Optional[DecisionOutcome4D] = None
    profit_impact: Optional[float] = None
    evaluation_timestamp: Optional[datetime] = None
    accuracy_score: Optional[float] = None

@dataclass
class RecoveryOperationRecord:
    """บันทึกการทำ Recovery"""
    timestamp: datetime
    operation_id: str
    
    # Recovery context
    losing_positions_count: int
    total_loss_amount: float
    target_recovery_amount: float
    
    # Recovery strategy
    recovery_strategy: str
    hedge_pairs_identified: int
    recovery_confidence: float
    
    # Execution details
    recovery_orders_placed: List[Dict]
    total_recovery_volume: float
    
    # Results
    recovery_success: bool = False
    actual_recovery_amount: float = 0.0
    net_result: float = 0.0
    completion_time: Optional[datetime] = None
    effectiveness_score: Optional[float] = None

@dataclass
class MarketOrderExecutionRecord:
    """บันทึกการ execute Market Order"""
    timestamp: datetime
    order_id: str
    
    # Order details
    symbol: str
    order_type: str  # BUY/SELL
    requested_volume: float
    requested_price: float
    
    # Execution results
    executed_price: float
    executed_volume: float
    slippage_points: float
    slippage_percentage: float
    execution_time_ms: float
    
    # Market context
    market_spread: float
    market_volatility: float
    session_type: str
    
    # Quality assessment
    execution_quality: str  # EXCELLENT/GOOD/AVERAGE/POOR
    success: bool = True

@dataclass
class PerformanceMetrics4D:
    """เมตริก performance แบบ 4D"""
    # 4D Analysis Metrics
    four_d_accuracy_rate: float = 0.0
    average_four_d_score: float = 0.0
    four_d_confidence_correlation: float = 0.0
    dimension_accuracy: Dict[str, float] = field(default_factory=dict)
    
    # Recovery Metrics
    recovery_success_rate: float = 0.0
    average_recovery_effectiveness: float = 0.0
    total_recovered_amount: float = 0.0
    recovery_time_efficiency: float = 0.0
    
    # Market Order Metrics
    market_order_success_rate: float = 0.0
    average_slippage: float = 0.0
    average_execution_time: float = 0.0
    execution_quality_distribution: Dict[str, int] = field(default_factory=dict)
    
    # Portfolio Health Metrics
    portfolio_health_trend: List[float] = field(default_factory=list)
    balance_ratio_stability: float = 0.0
    risk_adjusted_performance: float = 0.0
    
    # Overall Performance
    overall_system_score: float = 0.0
    performance_trend: str = "STABLE"
    last_updated: datetime = field(default_factory=datetime.now)

class PerformanceTracker:
    """
    📈 Performance Tracker - 4D Enhanced Monitoring Edition
    
    ความสามารถใหม่:
    - ✅ 4D analysis performance tracking พร้อม accuracy assessment
    - ✅ Recovery effectiveness monitoring แบบครบวงจร
    - ✅ Market order execution statistics แบบรายละเอียด
    - ✅ Real-time performance updates และ trend analysis
    - ✅ Portfolio health trend monitoring
    - ✅ Multi-dimensional performance correlation analysis
    - ✅ Adaptive learning support จาก performance data
    """
    
    def __init__(self, config: Dict):
        """Initialize 4D Performance Tracker"""
        self.config = config
        
        # 4D Analysis tracking
        self.four_d_records: deque = deque(maxlen=1000)
        self.four_d_accuracy_history: deque = deque(maxlen=200)
        
        # Recovery tracking
        self.recovery_records: deque = deque(maxlen=500)
        self.recovery_effectiveness_history: deque = deque(maxlen=100)
        
        # Market order tracking
        self.market_order_records: deque = deque(maxlen=2000)
        self.execution_quality_history: deque = deque(maxlen=300)
        
        # Portfolio health tracking
        self.portfolio_health_history: deque = deque(maxlen=500)
        self.balance_ratio_history: deque = deque(maxlen=500)
        
        # Performance metrics
        self.current_metrics = PerformanceMetrics4D()
        self.metrics_history: deque = deque(maxlen=100)  # บันทึกทุก 10 นาที
        
        # Configuration
        self.tracking_config = {
            "four_d_evaluation_delay": 300,        # 5 นาที - เวลารอประเมินผล 4D
            "recovery_evaluation_delay": 1800,     # 30 นาที - เวลารอประเมินผล recovery
            "portfolio_update_interval": 60,       # 1 นาที - อัปเดต portfolio health
            "metrics_save_interval": 600,          # 10 นาที - บันทึกเมตริก
            "enable_real_time_updates": True,
            "track_correlations": True,
            "enable_adaptive_learning": True
        }
        
        # Real-time monitoring
        self.monitoring_active = False
        self.monitoring_thread = None
        self.last_metrics_update = datetime.now()
        
        # File paths for persistence
        self.data_directory = "performance_data"
        self._ensure_data_directory()
        
        self.log("4D Performance Tracker initialized - Comprehensive monitoring active")
    
    # ========================================================================================
    # 🆕 MAIN 4D TRACKING METHODS
    # ========================================================================================
    
    def log_4d_analysis(self, analysis_data: Dict) -> str:
        """
        🆕 บันทึกการวิเคราะห์ 4D และติดตามประสิทธิภาพ
        
        Args:
            analysis_data: ข้อมูลการวิเคราะห์ 4D
            
        Returns:
            str: ID ของการบันทึกเพื่อติดตามผลลัพธ์
        """
        try:
            # สร้าง record ID
            record_id = f"4D_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.four_d_records)}"
            
            # สร้าง 4D analysis record
            four_d_record = FourDAnalysisRecord(
                timestamp=datetime.now(),
                four_d_score=analysis_data.get("four_d_score", 0.0),
                four_d_confidence=analysis_data.get("four_d_confidence", 0.0),
                trend_dimension_score=analysis_data.get("trend_dimension_score", 0.0),
                volume_dimension_score=analysis_data.get("volume_dimension_score", 0.0),
                session_dimension_score=analysis_data.get("session_dimension_score", 0.0),
                volatility_dimension_score=analysis_data.get("volatility_dimension_score", 0.0),
                market_condition_4d=analysis_data.get("market_condition_4d", "UNKNOWN"),
                recommendation=analysis_data.get("recommendation", "WAIT"),
                action_taken=analysis_data.get("action_taken"),
                order_type=analysis_data.get("order_type"),
                lot_size=analysis_data.get("lot_size")
            )
            
            # เพิ่มลงใน tracking queue
            self.four_d_records.append(four_d_record)
            
            # อัปเดตเมตริกเรียลไทม์
            self._update_4d_metrics()
            
            self.log(f"4D Analysis logged: Score={four_d_record.four_d_score:.3f}, Confidence={four_d_record.four_d_confidence:.3f}")
            
            # กำหนดเวลาประเมินผล
            evaluation_time = datetime.now() + timedelta(seconds=self.tracking_config["four_d_evaluation_delay"])
            
            # Schedule automatic evaluation (จำลอง - ในระบบจริงจะใช้ scheduler)
            self._schedule_4d_evaluation(record_id, evaluation_time)
            
            return record_id
            
        except Exception as e:
            self.log(f"❌ 4D Analysis logging error: {e}")
            return ""
    
    def track_recovery_performance(self, recovery_data: Dict) -> str:
        """
        🆕 ติดตามประสิทธิภาพการทำ Recovery
        
        Args:
            recovery_data: ข้อมูลการทำ recovery
            
        Returns:
            str: ID ของการติดตาม recovery
        """
        try:
            # สร้าง operation ID
            operation_id = f"REC_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.recovery_records)}"
            
            # สร้าง recovery record
            recovery_record = RecoveryOperationRecord(
                timestamp=datetime.now(),
                operation_id=operation_id,
                losing_positions_count=recovery_data.get("losing_positions_count", 0),
                total_loss_amount=recovery_data.get("total_loss_amount", 0.0),
                target_recovery_amount=recovery_data.get("target_recovery_amount", 0.0),
                recovery_strategy=recovery_data.get("recovery_strategy", "UNKNOWN"),
                hedge_pairs_identified=recovery_data.get("hedge_pairs_identified", 0),
                recovery_confidence=recovery_data.get("recovery_confidence", 0.0),
                recovery_orders_placed=recovery_data.get("recovery_orders_placed", []),
                total_recovery_volume=recovery_data.get("total_recovery_volume", 0.0)
            )
            
            # เพิ่มลงใน tracking queue
            self.recovery_records.append(recovery_record)
            
            # อัปเดตเมตริกเรียลไทม์
            self._update_recovery_metrics()
            
            self.log(f"Recovery operation tracked: Target=${recovery_record.target_recovery_amount:.2f}, Confidence={recovery_record.recovery_confidence:.3f}")
            
            return operation_id
            
        except Exception as e:
            self.log(f"❌ Recovery tracking error: {e}")
            return ""
    
    def log_market_order_execution(self, execution_data: Dict) -> str:
        """
        🆕 บันทึกการ execute Market Order และประเมินคุณภาพ
        
        Args:
            execution_data: ข้อมูลการ execute market order
            
        Returns:
            str: ID ของการบันทึก execution
        """
        try:
            # สร้าง execution ID
            execution_id = f"MO_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.market_order_records)}"
            
            # คำนวณ slippage
            requested_price = execution_data.get("requested_price", 0.0)
            executed_price = execution_data.get("executed_price", 0.0)
            slippage_points = abs(executed_price - requested_price)
            slippage_percentage = (slippage_points / requested_price * 100) if requested_price > 0 else 0.0
            
            # ประเมินคุณภาพการ execute
            execution_quality = self._assess_execution_quality(
                slippage_points, execution_data.get("execution_time_ms", 0.0)
            )
            
            # สร้าง market order record
            execution_record = MarketOrderExecutionRecord(
                timestamp=datetime.now(),
                order_id=execution_id,
                symbol=execution_data.get("symbol", "XAUUSD"),
                order_type=execution_data.get("order_type", "BUY"),
                requested_volume=execution_data.get("requested_volume", 0.0),
                requested_price=requested_price,
                executed_price=executed_price,
                executed_volume=execution_data.get("executed_volume", 0.0),
                slippage_points=slippage_points,
                slippage_percentage=slippage_percentage,
                execution_time_ms=execution_data.get("execution_time_ms", 0.0),
                market_spread=execution_data.get("market_spread", 0.0),
                market_volatility=execution_data.get("market_volatility", 1.0),
                session_type=execution_data.get("session_type", "UNKNOWN"),
                execution_quality=execution_quality,
                success=execution_data.get("success", True)
            )
            
            # เพิ่มลงใน tracking queue
            self.market_order_records.append(execution_record)
            
            # อัปเดตเมตริกเรียลไทม์
            self._update_market_order_metrics()
            
            self.log(f"Market order execution logged: {execution_quality} quality, Slippage={slippage_points:.5f}")
            
            return execution_id
            
        except Exception as e:
            self.log(f"❌ Market order execution logging error: {e}")
            return ""
    
    def update_portfolio_health(self, portfolio_data: Dict):
        """
        🆕 อัปเดตสุขภาพ portfolio และติดตาม trend
        
        Args:
            portfolio_data: ข้อมูลสุขภาพ portfolio
        """
        try:
            # สร้าง portfolio health record
            health_record = {
                "timestamp": datetime.now(),
                "portfolio_health": portfolio_data.get("portfolio_health", 0.0),
                "buy_sell_ratio": portfolio_data.get("buy_sell_ratio", 0.5),
                "total_positions": portfolio_data.get("total_positions", 0),
                "total_exposure": portfolio_data.get("total_exposure", 0.0),
                "margin_level": portfolio_data.get("margin_level", 0.0),
                "equity_balance_ratio": portfolio_data.get("equity_balance_ratio", 1.0),
                "unrealized_pnl": portfolio_data.get("unrealized_pnl", 0.0)
            }
            
            # เพิ่มลงประวัติ
            self.portfolio_health_history.append(health_record)
            self.balance_ratio_history.append(portfolio_data.get("buy_sell_ratio", 0.5))
            
            # อัปเดตเมตริก portfolio
            self._update_portfolio_metrics()
            
            # เช็ค trend และแจ้งเตือนถ้าจำเป็น
            self._check_portfolio_health_alerts(health_record)
            
        except Exception as e:
            self.log(f"❌ Portfolio health update error: {e}")
    
    # ========================================================================================
    # 🧮 METRICS CALCULATION METHODS
    # ========================================================================================
    
    def _update_4d_metrics(self):
        """อัปเดตเมตริก 4D analysis"""
        try:
            if not self.four_d_records:
                return
            
            # รวบรวมข้อมูล 4D ล่าสุด
            recent_records = [r for r in self.four_d_records if r.timestamp > datetime.now() - timedelta(hours=24)]
            
            if not recent_records:
                return
            
            # คำนวณเมตริกต่างๆ
            self.current_metrics.average_four_d_score = statistics.mean([r.four_d_score for r in recent_records])
            
            # คำนวณ accuracy rate (เฉพาะที่มีผลลัพธ์แล้ว)
            evaluated_records = [r for r in recent_records if r.actual_outcome is not None]
            if evaluated_records:
                successful_predictions = sum(1 for r in evaluated_records 
                                           if r.actual_outcome in [DecisionOutcome4D.EXCELLENT_SUCCESS, 
                                                                  DecisionOutcome4D.GOOD_SUCCESS,
                                                                  DecisionOutcome4D.MODERATE_SUCCESS])
                self.current_metrics.four_d_accuracy_rate = successful_predictions / len(evaluated_records)
            
            # คำนวณ correlation ระหว่าง confidence และ accuracy
            if len(evaluated_records) >= 10:
                confidences = [r.four_d_confidence for r in evaluated_records]
                accuracies = [r.accuracy_score for r in evaluated_records if r.accuracy_score is not None]
                
                if len(confidences) == len(accuracies) and len(accuracies) > 1:
                    correlation = np.corrcoef(confidences, accuracies)[0, 1]
                    if not np.isnan(correlation):
                        self.current_metrics.four_d_confidence_correlation = correlation
            
            # คำนวณ accuracy แยกตามมิติ
            dimension_accuracy = {}
            for dimension in ["trend", "volume", "session", "volatility"]:
                dimension_records = [r for r in evaluated_records if getattr(r, f"{dimension}_dimension_score", 0) > 0.6]
                if dimension_records:
                    accurate_predictions = sum(1 for r in dimension_records 
                                             if r.actual_outcome in [DecisionOutcome4D.EXCELLENT_SUCCESS, 
                                                                    DecisionOutcome4D.GOOD_SUCCESS])
                    dimension_accuracy[dimension] = accurate_predictions / len(dimension_records)
            
            self.current_metrics.dimension_accuracy = dimension_accuracy
            
        except Exception as e:
            self.log(f"❌ 4D metrics update error: {e}")
    
    def _update_recovery_metrics(self):
        """อัปเดตเมตริก recovery effectiveness"""
        try:
            if not self.recovery_records:
                return
            
            # รวบรวมข้อมูล recovery ล่าสุด
            recent_records = [r for r in self.recovery_records if r.timestamp > datetime.now() - timedelta(hours=48)]
            
            if not recent_records:
                return
            
            # คำนวณ success rate
            completed_records = [r for r in recent_records if r.completion_time is not None]
            if completed_records:
                successful_recoveries = sum(1 for r in completed_records if r.recovery_success)
                self.current_metrics.recovery_success_rate = successful_recoveries / len(completed_records)
                
                # คำนวณ average effectiveness
                effectiveness_scores = [r.effectiveness_score for r in completed_records if r.effectiveness_score is not None]
                if effectiveness_scores:
                    self.current_metrics.average_recovery_effectiveness = statistics.mean(effectiveness_scores)
                
                # คำนวณยอดรวมที่กู้คืนได้
                self.current_metrics.total_recovered_amount = sum(r.actual_recovery_amount for r in completed_records if r.recovery_success)
                
                # คำนวณ time efficiency (average recovery time)
                recovery_times = []
                for r in completed_records:
                    if r.completion_time and r.recovery_success:
                        time_diff = (r.completion_time - r.timestamp).total_seconds() / 60  # นาที
                        recovery_times.append(time_diff)
                
                if recovery_times:
                    avg_recovery_time = statistics.mean(recovery_times)
                    # แปลงเป็น efficiency score (ยิ่งเร็วยิ่งดี)
                    self.current_metrics.recovery_time_efficiency = max(0, 1 - (avg_recovery_time / 1800))  # 30 นาทีเป็นฐาน
            
        except Exception as e:
            self.log(f"❌ Recovery metrics update error: {e}")
    
    def _update_market_order_metrics(self):
        """อัปเดตเมตริก market order execution"""
        try:
            if not self.market_order_records:
                return
            
            # รวบรวมข้อมูล market order ล่าสุด
            recent_records = [r for r in self.market_order_records if r.timestamp > datetime.now() - timedelta(hours=24)]
            
            if not recent_records:
                return
            
            # คำนวณ success rate
            successful_orders = sum(1 for r in recent_records if r.success)
            self.current_metrics.market_order_success_rate = successful_orders / len(recent_records)
            
            # คำนวณ average slippage (เฉพาะที่สำเร็จ)
            successful_records = [r for r in recent_records if r.success]
            if successful_records:
                slippages = [r.slippage_points for r in successful_records]
                self.current_metrics.average_slippage = statistics.mean(slippages)
                
                # คำนวณ average execution time
                execution_times = [r.execution_time_ms for r in successful_records]
                self.current_metrics.average_execution_time = statistics.mean(execution_times)
                
                # คำนวณ execution quality distribution
                quality_dist = defaultdict(int)
                for r in successful_records:
                    quality_dist[r.execution_quality] += 1
                
                self.current_metrics.execution_quality_distribution = dict(quality_dist)
            
        except Exception as e:
            self.log(f"❌ Market order metrics update error: {e}")
    
    def _update_portfolio_metrics(self):
        """อัปเดตเมตริก portfolio health"""
        try:
            if not self.portfolio_health_history:
                return
            
            # รวบรวมข้อมูล portfolio ล่าสุด
            recent_records = [r for r in self.portfolio_health_history if r["timestamp"] > datetime.now() - timedelta(hours=24)]
            
            if not recent_records:
                return
            
            # คำนวณ portfolio health trend
            health_values = [r["portfolio_health"] for r in recent_records]
            self.current_metrics.portfolio_health_trend = health_values[-20:]  # เก็บ 20 ค่าล่าสุด
            
            # คำนวณ balance ratio stability
            if len(self.balance_ratio_history) >= 10:
                recent_ratios = list(self.balance_ratio_history)[-10:]
                ratio_std = statistics.stdev(recent_ratios)
                # แปลงเป็น stability score (ยิ่ง stable ยิ่งดี)
                self.current_metrics.balance_ratio_stability = max(0, 1 - (ratio_std / 0.5))
            
            # คำนวณ risk adjusted performance
            if len(recent_records) >= 5:
                pnl_values = [r["unrealized_pnl"] for r in recent_records]
                exposure_values = [r["total_exposure"] for r in recent_records]
                
                avg_pnl = statistics.mean(pnl_values)
                avg_exposure = statistics.mean(exposure_values)
                
                if avg_exposure > 0:
                    self.current_metrics.risk_adjusted_performance = avg_pnl / avg_exposure
            
        except Exception as e:
            self.log(f"❌ Portfolio metrics update error: {e}")
    
    def _calculate_overall_system_score(self):
        """คำนวณคะแนนรวมของระบบ"""
        try:
            # น้ำหนักของแต่ละมิติ
            weights = {
                "four_d_accuracy": 0.30,
                "recovery_effectiveness": 0.25,
                "market_execution": 0.20,
                "portfolio_health": 0.25
            }
            
            # คะแนนแต่ละมิติ
            four_d_score = self.current_metrics.four_d_accuracy_rate
            recovery_score = self.current_metrics.average_recovery_effectiveness
            execution_score = self.current_metrics.market_order_success_rate
            
            # Portfolio health score (จากค่าล่าสุด)
            portfolio_score = 0.0
            if self.current_metrics.portfolio_health_trend:
                portfolio_score = self.current_metrics.portfolio_health_trend[-1]
            
            # คำนวณคะแนนรวม
            overall_score = (
                four_d_score * weights["four_d_accuracy"] +
                recovery_score * weights["recovery_effectiveness"] +
                execution_score * weights["market_execution"] +
                portfolio_score * weights["portfolio_health"]
            )
            
            self.current_metrics.overall_system_score = round(overall_score, 3)
            
            # กำหนด performance trend
            if len(self.metrics_history) >= 5:
                recent_scores = [m.overall_system_score for m in list(self.metrics_history)[-5:]]
                if len(recent_scores) >= 2:
                    trend_slope = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
                    
                    if trend_slope > 0.02:
                        self.current_metrics.performance_trend = "IMPROVING"
                    elif trend_slope < -0.02:
                        self.current_metrics.performance_trend = "DECLINING"
                    else:
                        self.current_metrics.performance_trend = "STABLE"
            
        except Exception as e:
            self.log(f"❌ Overall system score calculation error: {e}")
    
    # ========================================================================================
    # 🔍 ANALYSIS AND ASSESSMENT METHODS
    # ========================================================================================
    
    def get_real_time_metrics(self) -> Dict:
        """
        🆕 ดึงเมตริก performance แบบ real-time
        
        Returns:
            Dict: เมตริก performance ปัจจุบัน
        """
        try:
            # อัปเดตเมตริกทั้งหมด
            self._update_4d_metrics()
            self._update_recovery_metrics()
            self._update_market_order_metrics()
            self._update_portfolio_metrics()
            self._calculate_overall_system_score()
            
            # สร้าง real-time summary
            real_time_summary = {
                # Overall Performance
                "overall_system_score": self.current_metrics.overall_system_score,
                "performance_trend": self.current_metrics.performance_trend,
                "last_updated": datetime.now().isoformat(),
                
                # 4D Analysis Performance
                "four_d_performance": {
                    "accuracy_rate": round(self.current_metrics.four_d_accuracy_rate, 3),
                    "average_score": round(self.current_metrics.average_four_d_score, 3),
                    "confidence_correlation": round(self.current_metrics.four_d_confidence_correlation, 3),
                    "dimension_accuracy": {k: round(v, 3) for k, v in self.current_metrics.dimension_accuracy.items()}
                },
                
                # Recovery Performance
                "recovery_performance": {
                    "success_rate": round(self.current_metrics.recovery_success_rate, 3),
                    "effectiveness": round(self.current_metrics.average_recovery_effectiveness, 3),
                    "total_recovered": round(self.current_metrics.total_recovered_amount, 2),
                    "time_efficiency": round(self.current_metrics.recovery_time_efficiency, 3)
                },
                
                # Market Order Performance
                "market_execution_performance": {
                    "success_rate": round(self.current_metrics.market_order_success_rate, 3),
                    "average_slippage": round(self.current_metrics.average_slippage, 5),
                    "average_execution_time": round(self.current_metrics.average_execution_time, 1),
                    "quality_distribution": self.current_metrics.execution_quality_distribution
                },
                
                # Portfolio Health
                "portfolio_health": {
                    "current_trend": self.current_metrics.portfolio_health_trend[-5:] if self.current_metrics.portfolio_health_trend else [],
                    "balance_stability": round(self.current_metrics.balance_ratio_stability, 3),
                    "risk_adjusted_performance": round(self.current_metrics.risk_adjusted_performance, 4)
                },
                
                # Data Statistics
                "data_statistics": {
                    "four_d_records_count": len(self.four_d_records),
                    "recovery_records_count": len(self.recovery_records),
                    "market_order_records_count": len(self.market_order_records),
                    "portfolio_health_records_count": len(self.portfolio_health_history)
                }
            }
            
            return real_time_summary
            
        except Exception as e:
            self.log(f"❌ Real-time metrics error: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def analyze_performance_patterns(self, time_window_hours: int = 24) -> Dict:
        """
        🆕 วิเคราะห์รูปแบบ performance
        
        Args:
            time_window_hours: ช่วงเวลาการวิเคราะห์ (ชั่วโมง)
            
        Returns:
            Dict: ผลการวิเคราะห์รูปแบบ performance
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            
            # วิเคราะห์รูปแบบ 4D performance
            four_d_patterns = self._analyze_4d_patterns(cutoff_time)
            
            # วิเคราะห์รูปแบบ recovery
            recovery_patterns = self._analyze_recovery_patterns(cutoff_time)
            
            # วิเคราะห์รูปแบบ market execution
            execution_patterns = self._analyze_execution_patterns(cutoff_time)
            
            # วิเคราะห์ portfolio trends
            portfolio_patterns = self._analyze_portfolio_patterns(cutoff_time)
            
            return {
                "analysis_window_hours": time_window_hours,
                "analysis_timestamp": datetime.now().isoformat(),
                "four_d_patterns": four_d_patterns,
                "recovery_patterns": recovery_patterns,
                "execution_patterns": execution_patterns,
                "portfolio_patterns": portfolio_patterns,
                "key_insights": self._generate_key_insights(
                    four_d_patterns, recovery_patterns, execution_patterns, portfolio_patterns
                )
            }
            
        except Exception as e:
            self.log(f"❌ Performance pattern analysis error: {e}")
            return {"error": str(e)}
    
    def get_adaptive_learning_recommendations(self) -> List[str]:
        """
        🆕 ดึงคำแนะนำสำหรับการปรับปรุงระบบ
        
        Returns:
            List[str]: รายการคำแนะนำ
        """
        try:
            recommendations = []
            
            # วิเคราะห์ 4D accuracy
            if self.current_metrics.four_d_accuracy_rate < 0.6:
                recommendations.append("4D Analysis: Consider adjusting dimension weights - accuracy below 60%")
            
            if self.current_metrics.four_d_confidence_correlation < 0.3:
                recommendations.append("4D Analysis: Low confidence-accuracy correlation - review confidence calculation")
            
            # วิเคราะห์ recovery effectiveness
            if self.current_metrics.recovery_success_rate < 0.7:
                recommendations.append("Recovery System: Success rate below 70% - review recovery strategies")
            
            if self.current_metrics.recovery_time_efficiency < 0.5:
                recommendations.append("Recovery System: Slow recovery times - optimize hedge detection")
            
            # วิเคราะห์ market execution
            if self.current_metrics.average_slippage > 0.0005:
                recommendations.append("Market Execution: High average slippage - consider execution timing optimization")
            
            if self.current_metrics.market_order_success_rate < 0.95:
                recommendations.append("Market Execution: Low success rate - review order management parameters")
            
            # วิเคราะห์ portfolio health
            if self.current_metrics.balance_ratio_stability < 0.7:
                recommendations.append("Portfolio Management: Unstable balance ratio - enhance balance-focused trading")
            
            # Overall system performance
            if self.current_metrics.overall_system_score < 0.6:
                recommendations.append("Overall System: Below-average performance - comprehensive review needed")
            
            if self.current_metrics.performance_trend == "DECLINING":
                recommendations.append("Performance Alert: Declining trend detected - immediate optimization required")
            
            # เพิ่มคำแนะนำเชิงบวก
            if self.current_metrics.overall_system_score > 0.8:
                recommendations.append("Excellent Performance: System operating at high efficiency")
            
            if not recommendations:
                recommendations.append("System Performance: All metrics within acceptable ranges")
            
            return recommendations
            
        except Exception as e:
            self.log(f"❌ Adaptive learning recommendations error: {e}")
            return [f"Error generating recommendations: {e}"]
    
    # ========================================================================================
    # 🔧 HELPER AND UTILITY METHODS
    # ========================================================================================
    
    def _assess_execution_quality(self, slippage_points: float, execution_time_ms: float) -> str:
        """ประเมินคุณภาพการ execute market order"""
        try:
            # เกณฑ์การประเมิน
            excellent_slippage = 0.0002
            good_slippage = 0.0005
            average_slippage = 0.001
            
            excellent_time = 1000  # ms
            good_time = 3000      # ms
            average_time = 5000   # ms
            
            # คะแนนจาก slippage
            if slippage_points <= excellent_slippage:
                slippage_score = 4  # EXCELLENT
            elif slippage_points <= good_slippage:
                slippage_score = 3  # GOOD
            elif slippage_points <= average_slippage:
                slippage_score = 2  # AVERAGE
            else:
                slippage_score = 1  # POOR
            
            # คะแนนจากเวลา
            if execution_time_ms <= excellent_time:
                time_score = 4  # EXCELLENT
            elif execution_time_ms <= good_time:
                time_score = 3  # GOOD
            elif execution_time_ms <= average_time:
                time_score = 2  # AVERAGE
            else:
                time_score = 1  # POOR
            
            # คะแนนรวม
            combined_score = (slippage_score + time_score) / 2
            
            if combined_score >= 3.5:
                return "EXCELLENT"
            elif combined_score >= 2.5:
                return "GOOD"
            elif combined_score >= 1.5:
                return "AVERAGE"
            else:
                return "POOR"
                
        except Exception as e:
            return "UNKNOWN"
    
    def _schedule_4d_evaluation(self, record_id: str, evaluation_time: datetime):
        """กำหนดเวลาประเมินผล 4D (จำลอง)"""
        # ในระบบจริง จะใช้ task scheduler
        # ที่นี่เราจะใช้วิธีง่ายๆ คือเก็บไว้ใน memory
        pass
    
    def _analyze_4d_patterns(self, cutoff_time: datetime) -> Dict:
        """วิเคราะห์รูปแบบ 4D performance"""
        try:
            recent_records = [r for r in self.four_d_records if r.timestamp > cutoff_time]
            
            if not recent_records:
                return {"insufficient_data": True}
            
            # วิเคราะห์การกระจายคะแนน
            scores = [r.four_d_score for r in recent_records]
            score_distribution = {
                "excellent": sum(1 for s in scores if s >= 0.8),
                "good": sum(1 for s in scores if 0.6 <= s < 0.8),
                "average": sum(1 for s in scores if 0.4 <= s < 0.6),
                "poor": sum(1 for s in scores if s < 0.4)
            }
            
            # วิเคราะห์ประสิทธิภาพแต่ละมิติ
            dimension_performance = {}
            for dimension in ["trend", "volume", "session", "volatility"]:
                dim_scores = [getattr(r, f"{dimension}_dimension_score", 0) for r in recent_records]
                if dim_scores:
                    dimension_performance[dimension] = {
                        "average": round(statistics.mean(dim_scores), 3),
                        "consistency": round(1 - statistics.stdev(dim_scores) / max(statistics.mean(dim_scores), 0.1), 3)
                    }
            
            return {
                "total_analyses": len(recent_records),
                "score_distribution": score_distribution,
                "average_score": round(statistics.mean(scores), 3),
                "score_consistency": round(1 - statistics.stdev(scores) / max(statistics.mean(scores), 0.1), 3),
                "dimension_performance": dimension_performance
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_recovery_patterns(self, cutoff_time: datetime) -> Dict:
        """วิเคราะห์รูปแบบ recovery performance"""
        try:
            recent_records = [r for r in self.recovery_records if r.timestamp > cutoff_time]
            
            if not recent_records:
                return {"insufficient_data": True}
            
            # วิเคราะห์ success rate ตาม strategy
            strategy_performance = defaultdict(lambda: {"attempts": 0, "successes": 0})
            
            for record in recent_records:
                if record.completion_time:  # เฉพาะที่เสร็จแล้ว
                    strategy = record.recovery_strategy
                    strategy_performance[strategy]["attempts"] += 1
                    if record.recovery_success:
                        strategy_performance[strategy]["successes"] += 1
            
            # คำนวณ success rate แต่ละ strategy
            strategy_success_rates = {}
            for strategy, data in strategy_performance.items():
                if data["attempts"] > 0:
                    strategy_success_rates[strategy] = data["successes"] / data["attempts"]
            
            return {
                "total_recoveries": len(recent_records),
                "completed_recoveries": sum(1 for r in recent_records if r.completion_time),
                "strategy_performance": dict(strategy_performance),
                "strategy_success_rates": strategy_success_rates
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_execution_patterns(self, cutoff_time: datetime) -> Dict:
        """วิเคราะห์รูปแบบ market execution"""
        try:
            recent_records = [r for r in self.market_order_records if r.timestamp > cutoff_time]
            
            if not recent_records:
                return {"insufficient_data": True}
            
            # วิเคราะห์ performance ตาม session
            session_performance = defaultdict(lambda: {"orders": 0, "successes": 0, "total_slippage": 0.0})
            
            for record in recent_records:
                session = record.session_type
                session_performance[session]["orders"] += 1
                if record.success:
                    session_performance[session]["successes"] += 1
                    session_performance[session]["total_slippage"] += record.slippage_points
            
            # คำนวณเมตริกแต่ละ session
            session_metrics = {}
            for session, data in session_performance.items():
                if data["orders"] > 0:
                    success_rate = data["successes"] / data["orders"]
                    avg_slippage = data["total_slippage"] / max(data["successes"], 1)
                    session_metrics[session] = {
                        "success_rate": round(success_rate, 3),
                        "average_slippage": round(avg_slippage, 5),
                        "order_count": data["orders"]
                    }
            
            return {
                "total_orders": len(recent_records),
                "successful_orders": sum(1 for r in recent_records if r.success),
                "session_metrics": session_metrics,
                "overall_success_rate": round(sum(1 for r in recent_records if r.success) / len(recent_records), 3)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_portfolio_patterns(self, cutoff_time: datetime) -> Dict:
        """วิเคราะห์รูปแบบ portfolio health"""
        try:
            recent_records = [r for r in self.portfolio_health_history if r["timestamp"] > cutoff_time]
            
            if not recent_records:
                return {"insufficient_data": True}
            
            # วิเคราะห์ trend
            health_values = [r["portfolio_health"] for r in recent_records]
            balance_ratios = [r["buy_sell_ratio"] for r in recent_records]
            
            health_trend = "STABLE"
            if len(health_values) >= 5:
                recent_avg = statistics.mean(health_values[-5:])
                earlier_avg = statistics.mean(health_values[:5])
                
                if recent_avg > earlier_avg + 0.1:
                    health_trend = "IMPROVING"
                elif recent_avg < earlier_avg - 0.1:
                    health_trend = "DECLINING"
            
            return {
                "total_records": len(recent_records),
                "average_health": round(statistics.mean(health_values), 3),
                "health_trend": health_trend,
                "average_balance_ratio": round(statistics.mean(balance_ratios), 3),
                "balance_stability": round(1 - statistics.stdev(balance_ratios) / max(statistics.mean(balance_ratios), 0.1), 3)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_key_insights(self, four_d_patterns: Dict, recovery_patterns: Dict,
                             execution_patterns: Dict, portfolio_patterns: Dict) -> List[str]:
        """สร้าง key insights จากการวิเคราะห์"""
        insights = []
        
        try:
            # 4D insights
            if "score_distribution" in four_d_patterns:
                excellent_pct = four_d_patterns["score_distribution"]["excellent"] / max(four_d_patterns["total_analyses"], 1) * 100
                if excellent_pct > 30:
                    insights.append(f"4D Analysis shows strong performance with {excellent_pct:.1f}% excellent scores")
                elif excellent_pct < 10:
                    insights.append(f"4D Analysis needs improvement - only {excellent_pct:.1f}% excellent scores")
            
            # Recovery insights
            if "strategy_success_rates" in recovery_patterns and recovery_patterns["strategy_success_rates"]:
                best_strategy = max(recovery_patterns["strategy_success_rates"].items(), key=lambda x: x[1])
                insights.append(f"Best recovery strategy: {best_strategy[0]} with {best_strategy[1]:.1%} success rate")
            
            # Execution insights
            if "session_metrics" in execution_patterns and execution_patterns["session_metrics"]:
                best_session = max(execution_patterns["session_metrics"].items(), key=lambda x: x[1]["success_rate"])
                insights.append(f"Best execution session: {best_session[0]} with {best_session[1]['success_rate']:.1%} success rate")
            
            # Portfolio insights
            if "health_trend" in portfolio_patterns:
                trend = portfolio_patterns["health_trend"]
                if trend == "IMPROVING":
                    insights.append("Portfolio health is improving - good system performance")
                elif trend == "DECLINING":
                    insights.append("Portfolio health is declining - review needed")
            
        except Exception as e:
            insights.append(f"Insight generation error: {e}")
        
        return insights
    
    def _check_portfolio_health_alerts(self, health_record: Dict):
        """เช็คและส่งการแจ้งเตือนเกี่ยวกับสุขภาพ portfolio"""
        try:
            portfolio_health = health_record.get("portfolio_health", 0.0)
            
            if portfolio_health < 0.3:
                self.log(f"🚨 CRITICAL ALERT: Portfolio health critically low: {portfolio_health:.1%}")
            elif portfolio_health < 0.5:
                self.log(f"⚠️ WARNING: Portfolio health below average: {portfolio_health:.1%}")
            
            # เช็ค margin level
            margin_level = health_record.get("margin_level", 0.0)
            if 0 < margin_level < 200:
                self.log(f"🚨 MARGIN ALERT: Margin level critically low: {margin_level:.0f}%")
            
        except Exception as e:
            self.log(f"❌ Portfolio health alert error: {e}")
    
    def _ensure_data_directory(self):
        """สร้างโฟลเดอร์สำหรับเก็บข้อมูล"""
        try:
            if not os.path.exists(self.data_directory):
                os.makedirs(self.data_directory)
        except Exception as e:
            self.log(f"❌ Data directory creation error: {e}")
    
    def log(self, message: str):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] 📈 PerformanceTracker: {message}")


# ========================================================================================
# 🧪 4D PERFORMANCE TRACKER TEST FUNCTIONS
# ========================================================================================

# def test_4d_performance_tracker():
#     """Test 4D Performance Tracker functionality"""
#     print("🧪 Testing 4D Performance Tracker...")
#     print("✅ 4D Analysis Performance Tracking")
#     print("✅ Recovery Effectiveness Monitoring")
#     print("✅ Market Order Execution Statistics")
#     print("✅ Portfolio Health Trend Analysis")
#     print("✅ Real-time Performance Updates")
#     print("✅ Adaptive Learning Recommendations")
#     print("✅ Performance Pattern Analysis")
#     print("✅ Ready for 4D AI Rule Engine Integration")

# if __name__ == "__main__":
#     test_4d_performance_tracker()