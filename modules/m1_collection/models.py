"""
Pydantic Data Models for Module 1: Telemetry Collection.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone


class MetricSignal(BaseModel):
    service_id: str
    metric_name: str
    value: float
    baseline: float = 0.0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_anomaly: bool = False

    def check_anomaly(self, threshold_multiplier: float = 2.0) -> bool:
        if self.baseline > 0:
            self.is_anomaly = self.value > (self.baseline * threshold_multiplier)
        return self.is_anomaly


class AlertSignal(BaseModel):
    alert_id: str
    severity: str  # P1, P2, P3
    source: str = "Prometheus AlertManager"
    summary: str
    service_id: str
    metric_name: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TelemetryBatch(BaseModel):
    metrics: List[MetricSignal] = []
    alerts: List[AlertSignal] = []
    metadata: Dict[str, Any] = {}
