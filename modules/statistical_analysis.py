import pandas as pd
import numpy as np

from scipy.stats import (
    skew,
    kurtosis,
    shapiro,
    t
)

# =====================================================
# HELPER
# =====================================================

def get_numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    )

# =====================================================
# DESCRIPTIVE STATISTICS
# =====================================================

def descriptive_statistics(df):

    numeric_df = get_numeric_columns(df)

    return numeric_df.describe().T

# =====================================================
# MEAN
# =====================================================

def mean_values(df):

    numeric_df = get_numeric_columns(df)

    return numeric_df.mean()

# =====================================================
# MEDIAN
# =====================================================

def median_values(df):

    numeric_df = get_numeric_columns(df)

    return numeric_df.median()

# =====================================================
# MODE
# =====================================================

def mode_values(df):

    numeric_df = get_numeric_columns(df)

    modes = {}

    for col in numeric_df.columns:

        mode_series = numeric_df[col].mode()

        if len(mode_series) > 0:

            modes[col] = mode_series.iloc[0]

        else:

            modes[col] = np.nan

    return pd.Series(modes)

# =====================================================
# VARIANCE
# =====================================================

def variance_values(df):

    numeric_df = get_numeric_columns(df)

    return numeric_df.var()

# =====================================================
# STANDARD DEVIATION
# =====================================================

def std_deviation(df):

    numeric_df = get_numeric_columns(df)

    return numeric_df.std()

# =====================================================
# RANGE
# =====================================================

def range_values(df):

    numeric_df = get_numeric_columns(df)

    return numeric_df.max() - numeric_df.min()

# =====================================================
# IQR
# =====================================================

def iqr_values(df):

    numeric_df = get_numeric_columns(df)

    return (
        numeric_df.quantile(0.75)
        -
        numeric_df.quantile(0.25)
    )

# =====================================================
# SKEWNESS
# =====================================================

def skewness_analysis(df):

    numeric_df = get_numeric_columns(df)

    results = []

    for col in numeric_df.columns:

        results.append({

            "Column": col,

            "Skewness":
            round(
                skew(
                    numeric_df[col].dropna()
                ),
                4
            )

        })

    return pd.DataFrame(results)

# =====================================================
# KURTOSIS
# =====================================================

def kurtosis_analysis(df):

    numeric_df = get_numeric_columns(df)

    results = []

    for col in numeric_df.columns:

        results.append({

            "Column": col,

            "Kurtosis":
            round(
                kurtosis(
                    numeric_df[col].dropna()
                ),
                4
            )

        })

    return pd.DataFrame(results)

# =====================================================
# PERCENTILES
# =====================================================

def percentile_summary(df):

    numeric_df = get_numeric_columns(df)

    summary = pd.DataFrame({

        "Q1":
        numeric_df.quantile(0.25),

        "Median":
        numeric_df.quantile(0.50),

        "Q3":
        numeric_df.quantile(0.75),

        "P90":
        numeric_df.quantile(0.90),

        "P95":
        numeric_df.quantile(0.95)

    })

    return summary

# =====================================================
# CONFIDENCE INTERVALS
# =====================================================

def confidence_interval_table(
    df,
    confidence=0.95
):

    numeric_df = get_numeric_columns(df)

    results = []

    for col in numeric_df.columns:

        data = (
            numeric_df[col]
            .dropna()
        )

        if len(data) < 2:

            continue

        mean = data.mean()

        std = data.std()

        n = len(data)

        margin = (

            t.ppf(
                (1 + confidence) / 2,
                n - 1
            )

            *

            (std / np.sqrt(n))

        )

        results.append({

            "Column": col,

            "Mean":
            round(mean, 4),

            "Lower CI":
            round(
                mean - margin,
                4
            ),

            "Upper CI":
            round(
                mean + margin,
                4
            )

        })

    return pd.DataFrame(results)

# =====================================================
# SHAPIRO TEST
# =====================================================

def shapiro_wilk_test(df):

    numeric_df = get_numeric_columns(df)

    results = []

    for col in numeric_df.columns:

        values = (
            numeric_df[col]
            .dropna()
        )

        if len(values) < 3:

            continue

        sample = values

        if len(values) > 5000:

            sample = values.sample(
                5000,
                random_state=42
            )

        stat, p_value = shapiro(
            sample
        )

        results.append({

            "Column": col,

            "Statistic":
            round(stat, 4),

            "P_Value":
            round(p_value, 4),

            "Normal":

            "Yes"

            if p_value > 0.05

            else "No"

        })

    return pd.DataFrame(results)

# =====================================================
# OUTLIERS
# =====================================================

def outlier_summary(df):

    numeric_df = get_numeric_columns(df)

    results = []

    for col in numeric_df.columns:

        q1 = numeric_df[col].quantile(0.25)

        q3 = numeric_df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers = numeric_df[
            (numeric_df[col] < lower)
            |
            (numeric_df[col] > upper)
        ]

        results.append({

            "Column": col,

            "Outliers":
            len(outliers)

        })

    return pd.DataFrame(results)

# =====================================================
# CORRELATION MATRIX
# =====================================================

def correlation_matrix(df):

    numeric_df = get_numeric_columns(df)

    return numeric_df.corr()

# =====================================================
# DATA QUALITY REPORT
# =====================================================

def data_quality_report(df):

    report = pd.DataFrame({

        "Column":
        df.columns,

        "Data_Type":
        df.dtypes.astype(str),

        "Missing":
        df.isnull().sum(),

        "Missing_%":

        round(

            (
                df.isnull().sum()
                /
                len(df)
            ) * 100,

            2

        ),

        "Unique":
        df.nunique()

    })

    return report
