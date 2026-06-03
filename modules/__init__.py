"""
Agriculture Analytics Dashboard

Author: Sateesh Ambesange
Project: Agriculture Analytics Dashboard
Version: 1.0

This package contains all analytics,
visualization, reporting, and business
intelligence modules used by the
Agriculture Analytics Dashboard.
"""

# =====================================================
# DATA LOADER
# =====================================================

from .data_loader import *

# =====================================================
# KPI METRICS
# =====================================================

from .kpi_metrics import *

# =====================================================
# STATISTICAL ANALYSIS
# =====================================================

from .statistical_analysis import *

# =====================================================
# YIELD ANALYTICS
# =====================================================

from .yield_analytics import *

# =====================================================
# WATER ANALYTICS
# =====================================================

from .water_analytics import *

# =====================================================
# FERTILIZER ANALYTICS
# =====================================================

from .fertilizer_analytics import *

# =====================================================
# PESTICIDE ANALYTICS
# =====================================================

from .pesticide_analytics import *

# =====================================================
# SUSTAINABILITY ANALYTICS
# =====================================================

from .sustainability_analytics import *

# =====================================================
# CORRELATION ANALYSIS
# =====================================================

from .correlation_analysis import *

# =====================================================
# ADVANCED VISUALIZATIONS
# =====================================================

from .advanced_visualizations import *

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

from .business_insights import *

# =====================================================
# REPORTING
# =====================================================

from .export_reports import *

# =====================================================
# PACKAGE VERSION
# =====================================================

__version__ = "1.0.0"

# =====================================================
# PACKAGE AUTHOR
# =====================================================

__author__ = "Sateesh Ambesange"

# =====================================================
# MODULE LIST
# =====================================================

__all__ = [

    # Data Loader
    "load_data",
    "create_derived_metrics",

    # KPI Metrics
    "executive_summary",

    # Statistical
    "descriptive_statistics",

    # Yield
    "crop_yield_summary",

    # Water
    "crop_water_summary",

    # Fertilizer
    "crop_fertilizer_summary",

    # Pesticide
    "crop_pesticide_summary",

    # Sustainability
    "executive_sustainability_summary",

    # Correlation
    "pearson_correlation",

    # Business
    "complete_business_report",

    # Reporting
    "create_excel_report",
    "create_pdf_report"
]
