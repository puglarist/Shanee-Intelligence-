"""
Swarm Monitor
Real-time monitoring and observability for the 500-agent swarm
Tracks: agents, tasks, throughput, failures, recovery
"""

import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MonitorMetrics:
    """Real-time metrics snapshot"""
    timestamp: str
    swarm_health_score: float  # 0-100
    agent_utilization: float  # 0-100
    task_backlog_size: int
    system_latency_ms: float
    validation_success_rate: float  # 0-100
    task_throughput: float  # tasks/second
    error_rate: float  # 0-100
    recovery_cycles: int


class SwarmMonitor:
    """
    Real-time monitoring of 500-agent swarm
    Tracks: health, utilization, throughput, failures
    """

    def __init__(self, window_size: int = 100):
        self.metrics_history: deque = deque(maxlen=window_size)
        self.alert_thresholds = {
            "health_score": 50,
            "agent_utilization": 20,
            "error_rate": 10,
            "latency_ms": 5000
        }
        self.active_alerts: List[str] = []
        self.last_metric = None

    def record_metric(
        self,
        health_score: float,
        utilization: float,
        backlog: int,
        latency: float,
        validation_rate: float,
        throughput: float,
        error_rate: float,
        recovery_cycles: int = 0
    ) -> MonitorMetrics:
        """Record a metrics snapshot"""
        metric = MonitorMetrics(
            timestamp=datetime.utcnow().isoformat(),
            swarm_health_score=health_score,
            agent_utilization=utilization,
            task_backlog_size=backlog,
            system_latency_ms=latency,
            validation_success_rate=validation_rate,
            task_throughput=throughput,
            error_rate=error_rate,
            recovery_cycles=recovery_cycles
        )

        self.metrics_history.append(metric)
        self.last_metric = metric

        # Check thresholds
        self._check_thresholds(metric)

        return metric

    def _check_thresholds(self, metric: MonitorMetrics):
        """Check metrics against alert thresholds"""
        self.active_alerts.clear()

        if metric.swarm_health_score < self.alert_thresholds["health_score"]:
            self.active_alerts.append(
                f"ALERT: Low swarm health ({metric.swarm_health_score:.1f}%)"
            )

        if metric.agent_utilization < self.alert_thresholds["agent_utilization"]:
            self.active_alerts.append(
                f"ALERT: Low agent utilization ({metric.agent_utilization:.1f}%)"
            )

        if metric.error_rate > self.alert_thresholds["error_rate"]:
            self.active_alerts.append(
                f"ALERT: High error rate ({metric.error_rate:.1f}%)"
            )

        if metric.system_latency_ms > self.alert_thresholds["latency_ms"]:
            self.active_alerts.append(
                f"ALERT: High system latency ({metric.system_latency_ms:.1f}ms)"
            )

        for alert in self.active_alerts:
            logger.warning(alert)

    def get_current_status(self) -> Dict:
        """Get current monitoring status"""
        if not self.last_metric:
            return {}

        return {
            "timestamp": self.last_metric.timestamp,
            "health": {
                "score": round(self.last_metric.swarm_health_score, 1),
                "status": self._get_health_status(self.last_metric.swarm_health_score),
                "utilization": round(self.last_metric.agent_utilization, 1)
            },
            "execution": {
                "throughput": round(self.last_metric.task_throughput, 2),
                "backlog": self.last_metric.task_backlog_size,
                "latency_ms": round(self.last_metric.system_latency_ms, 1)
            },
            "quality": {
                "validation_success_rate": round(self.last_metric.validation_success_rate, 1),
                "error_rate": round(self.last_metric.error_rate, 1)
            },
            "recovery": {
                "cycles": self.last_metric.recovery_cycles
            },
            "alerts": self.active_alerts
        }

    def get_metrics_dashboard(self) -> Dict:
        """Get comprehensive metrics dashboard"""
        if not self.metrics_history:
            return {}

        metrics_list = list(self.metrics_history)
        recent = metrics_list[-10:]

        # Calculate trends
        if len(recent) >= 2:
            health_trend = (
                recent[-1].swarm_health_score -
                recent[0].swarm_health_score
            )
            throughput_trend = (
                recent[-1].task_throughput -
                recent[0].task_throughput
            )
        else:
            health_trend = 0
            throughput_trend = 0

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "current_metrics": self.get_current_status(),
            "trends": {
                "health_trend": round(health_trend, 1),
                "throughput_trend": round(throughput_trend, 2)
            },
            "aggregates": {
                "avg_health_score": round(
                    sum(m.swarm_health_score for m in metrics_list) / len(metrics_list), 1
                ),
                "avg_utilization": round(
                    sum(m.agent_utilization for m in metrics_list) / len(metrics_list), 1
                ),
                "avg_throughput": round(
                    sum(m.task_throughput for m in metrics_list) / len(metrics_list), 2
                ),
                "avg_latency_ms": round(
                    sum(m.system_latency_ms for m in metrics_list) / len(metrics_list), 1
                )
            },
            "history_size": len(metrics_list),
            "active_alerts": len(self.active_alerts)
        }

    def get_performance_summary(self) -> Dict:
        """Get performance summary for reporting"""
        if not self.metrics_history:
            return {}

        metrics_list = list(self.metrics_history)

        successful = sum(
            1 for m in metrics_list
            if m.error_rate < 5 and m.swarm_health_score > 70
        )
        success_rate = (successful / len(metrics_list) * 100) if metrics_list else 0

        return {
            "total_observations": len(metrics_list),
            "time_window": f"{len(metrics_list)} snapshots",
            "operational_success_rate": round(success_rate, 1),
            "peak_health": round(max(m.swarm_health_score for m in metrics_list), 1),
            "minimum_health": round(min(m.swarm_health_score for m in metrics_list), 1),
            "peak_throughput": round(max(m.task_throughput for m in metrics_list), 2),
            "average_recovery_cycles": round(
                sum(m.recovery_cycles for m in metrics_list) / len(metrics_list), 1
            ) if metrics_list else 0
        }

    def _get_health_status(self, score: float) -> str:
        """Get human-readable health status"""
        if score >= 90:
            return "🟢 Excellent"
        elif score >= 70:
            return "🟢 Good"
        elif score >= 50:
            return "🟡 Degraded"
        else:
            return "🔴 Critical"

    def set_alert_threshold(self, metric_name: str, threshold: float):
        """Set alert threshold for a metric"""
        if metric_name in self.alert_thresholds:
            self.alert_thresholds[metric_name] = threshold
            logger.info(f"Alert threshold for {metric_name} set to {threshold}")

    def clear_history(self):
        """Clear metrics history"""
        self.metrics_history.clear()
        self.active_alerts.clear()
        self.last_metric = None
        logger.info("Metrics history cleared")

    def export_metrics_json(self, filepath: str) -> bool:
        """Export metrics to JSON file"""
        try:
            data = {
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": [
                    {
                        "timestamp": m.timestamp,
                        "health_score": m.swarm_health_score,
                        "utilization": m.agent_utilization,
                        "backlog": m.task_backlog_size,
                        "latency": m.system_latency_ms,
                        "validation_rate": m.validation_success_rate,
                        "throughput": m.task_throughput,
                        "error_rate": m.error_rate
                    }
                    for m in self.metrics_history
                ],
                "summary": self.get_performance_summary()
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Metrics exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
            return False


if __name__ == "__main__":
    monitor = SwarmMonitor()

    # Simulate metrics
    print("Recording sample metrics...")
    for i in range(5):
        monitor.record_metric(
            health_score=85 + (i * 2),
            utilization=70 + (i * 3),
            backlog=15 - (i * 2),
            latency=45.5 + (i * 5),
            validation_rate=92.5,
            throughput=8.3 + (i * 0.5),
            error_rate=2.1,
            recovery_cycles=i
        )

    # Show dashboard
    dashboard = monitor.get_metrics_dashboard()
    print(f"\nMetrics Dashboard:")
    print(json.dumps(dashboard, indent=2))

    # Show summary
    summary = monitor.get_performance_summary()
    print(f"\nPerformance Summary:")
    print(json.dumps(summary, indent=2))
