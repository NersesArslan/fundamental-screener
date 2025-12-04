"""
Metrics Package - Universal core metrics + industry-specific overrides

Architecture:
- core.py: 7 universal metrics that work across all industries
- Industry overrides: Add specialized metrics for specific sectors
  - semis_overrides.py: Semiconductor-specific metrics
  - tech_overrides.py: Big tech-specific metrics
  - (more as you expand)

Usage:
    from metrics.core import get_core_metrics
    from metrics.semis_overrides import get_semis_metrics
    
    # For semiconductors
    metrics = get_core_metrics() + get_semis_metrics()
"""

from metrics.core import (
    get_core_metrics,
    EVToFCFMetric,
    ROICMetric,
    RevenueCagrMetric,
    OperatingMarginMetric,
    FCFMarginMetric,
    NetDebtToEBITDAMetric,
    InterestCoverageMetric,
)

__all__ = [
    'get_core_metrics',
    'EVToFCFMetric',
    'ROICMetric',
    'RevenueCagrMetric',
    'OperatingMarginMetric',
    'FCFMarginMetric',
    'NetDebtToEBITDAMetric',
    'InterestCoverageMetric',
]
