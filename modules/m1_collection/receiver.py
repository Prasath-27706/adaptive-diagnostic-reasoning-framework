"""
Receiver Service for Module 1: Telemetry Collection.
"""

from typing import List, Dict, Any
from .models import MetricSignal, AlertSignal, TelemetryBatch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("m1_collection")


class TelemetryReceiver:
    """
    Ingests and buffers telemetry signals and alerts.
    """

    def __init__(self):
        self.metric_buffer: List[MetricSignal] = []
        self.alert_buffer: List[AlertSignal] = []

    def ingest_metrics(self, metrics: List[MetricSignal]) -> int:
        anomalous_count = 0
        for m in metrics:
            if m.check_anomaly():
                anomalous_count += 1
            self.metric_buffer.append(m)
        logger.info(f"Ingested {len(metrics)} metrics ({anomalous_count} anomalous).")
        return anomalous_count

    def ingest_alert(self, alert: AlertSignal):
        self.alert_buffer.append(alert)
        logger.info(f"Alert received: {alert.alert_id} - {alert.summary}")

    def get_active_anomalies(self) -> List[MetricSignal]:
        return [m for m in self.metric_buffer if m.is_anomaly]

    def clear_buffers(self):
        self.metric_buffer.clear()
        self.alert_buffer.clear()
