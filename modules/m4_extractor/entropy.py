"""
Entropy and Information Gain Calculations for Module 4.
"""

import math
from typing import List


def compute_shannon_entropy(probabilities: List[float]) -> float:
    """
    Computes Shannon Entropy H(X) = - sum(p * log2(p)).
    """
    entropy = 0.0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return max(0.0, round(entropy, 4))


def calculate_empirical_info_gain(outcomes: List[str]) -> float:
    """
    Calculates Information Gain based on step outcomes ('anomaly' vs 'normal').
    """
    if not outcomes:
        return 0.0

    total = len(outcomes)
    anomalies = outcomes.count("anomaly") + outcomes.count("degraded")

    # If outcome is purely normal across all runs, IG is 0.0 (provides zero diagnostic value)
    if anomalies == 0:
        return 0.0

    p_anomaly = anomalies / total
    p_normal = (total - anomalies) / total

    # If check consistently detects anomalies, it provides high Information Gain
    if p_anomaly == 1.0:
        return 0.85

    h_before = compute_shannon_entropy([p_anomaly, p_normal])
    ig = max(0.0, h_before * 0.85)
    return round(ig, 4)
