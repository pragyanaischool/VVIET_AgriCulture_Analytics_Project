import pandas as pd
import numpy as np

from scipy.stats import (
    skew,
    kurtosis,
    shapiro,
    normaltest,
    t
)

# =====================================================
# NUMERIC DATA
# =====================================================

def get_numeric_data(df):

    return df.select_dtypes(
        include=np.number
    )

# =====================================================
# DESCRIPTIVE STATISTICS
# =====================================================

def descriptive_statistics(df):

    numeric_df = get_numeric_data(df)

    return numeric_df.describe().T

# =====================================================
# ADVANCED DESCRIPTIVE STATISTICS
# =====================================================

def advanced_statistics(df):

    numeric_df = get_numeric_data(df)

    results = []

    for col in numeric_df.columns:

        series = numeric_df[col].dropna()

        results.append({

            "Column": col,

            "Count": len(series),

            "Mean": series.mean(),

            "Median": series.median(),

            "Std": series.std(),

            "Variance": series.var(),

            "Min": series.min(),

            "Max": series.max(),

            "Range": series.max() - series.min(),

            "Q1": series.quantile(0.25),

            "Q3": series.quantile(0.75),

            "IQR":
            series.quantile(0.75)
            -
            series.quantile(0.25)

        })

    return pd.DataFrame(results)

# =====================================================
# SKEWNESS
# =====================================================

def skewness_analysis(df):

    numeric_df = get_numeric_data(df)

    results = []

    for col in numeric_df.columns:

        results.append({

            "Column": col,

            "Skewness":
            skew(
                numeric_df[col].dropna()
            )

        })

    return pd.DataFrame(results)

# =====================================================
# KURTOSIS
# =====================================================

def kurtosis_analysis(df):

    numeric_df = get_numeric_data(df)

    results = []

    for col in numeric_df.columns:

        results.append({

            "Column": col,

            "Kurtosis":
            kurtosis(
                numeric_df[col].dropna()
            )

        })

    return pd.DataFrame(results)

# =====================================================
# VARIANCE
# =====================================================

def variance_analysis(df):

    numeric_df = get_numeric_data(df)

    return pd.DataFrame({

        "Column":
        numeric_df.columns,

        "Variance":
        numeric_df.var().values

    })

# =====================================================
# STANDARD DEVIATION
# =====================================================

def standard_deviation_analysis(df):

    numeric_df = get_numeric_data(df)

    return pd.DataFrame({

        "Column":
        numeric_df.columns,

        "Standard_Deviation":
        numeric_df.std().values

    })

# =====================================================
# MISSING VALUES
# =====================================================

def missing_value_analysis(df):

    return pd.DataFrame({

        "Column":
        df.columns,

        "Missing Values":
        df.isna().sum().values,

        "Missing %":
        (
            df.isna().sum()
            /
            len(df)
            * 100
        ).values

    })

# =====================================================
# OUTLIERS
# =====================================================

def outlier_analysis(df):

    numeric_df = get_numeric_data(df)

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
# NORMALITY TEST
# =====================================================

def normality_test(df):

    numeric_df = get_numeric_data(df)

    results = []

    for col in numeric_df.columns:

        data = (
            numeric_df[col]
            .dropna()
        )

        if len(data) > 3:

            stat, p = shapiro(data)

            results.append({

                "Column": col,

                "Statistic": stat,

                "P_Value": p,

                "Normal":

                "Yes"

                if p > 0.05

                else "No"

            })

    return pd.DataFrame(results)

# =====================================================
# D'AGOSTINO TEST
# =====================================================

def dagostino_test(df):

    numeric_df = get_numeric_data(df)

    results = []

    for col in numeric_df.columns:

        data = (
            numeric_df[col]
            .dropna()
        )

        if len(data) > 8:

            stat, p = normaltest(data)

            results.append({

                "Column": col,

                "Statistic": stat,

                "P_Value": p

            })

    return pd.DataFrame(results)

# =====================================================
# CONFIDENCE INTERVALS
# =====================================================

def confidence_intervals(
    df,
    confidence=0.95
):

    numeric_df = get_numeric_data(df)

    results = []

    for col in numeric_df.columns:

        data = (
            numeric_df[col]
            .dropna()
        )

        n = len(data)

        mean = data.mean()

        std = data.std()

        margin = (
            t.ppf(
                (1 + confidence) / 2,
                n - 1
            )
            *
            std
            /
            np.sqrt(n)
        )

        results.append({

            "Column": col,

            "Mean": mean,

            "Lower CI":
            mean - margin,

            "Upper CI":
            mean + margin

        })

    return pd.DataFrame(results)

# =====================================================
# CORRELATION
# =====================================================

def correlation_matrix(df):

    numeric_df = get_numeric_data(df)

    return numeric_df.corr()

# =====================================================
# PEARSON
# =====================================================

def pearson_correlation(df):

    numeric_df = get_numeric_data(df)

    return numeric_df.corr(
        method="pearson"
    )

# =====================================================
# SPEARMAN
# =====================================================

def spearman_correlation(df):

    numeric_df = get_numeric_data(df)

    return numeric_df.corr(
        method="spearman"
    )

# =====================================================
# KENDALL
# =====================================================

def kendall_correlation(df):

    numeric_df = get_numeric_data(df)

    return numeric_df.corr(
        method="kendall"
    )

# =====================================================
# SUMMARY
# =====================================================

def statistical_summary(df):

    numeric_df = get_numeric_data(df)

    return {

        "Rows":
        int(len(df)),

        "Columns":
        int(len(df.columns)),

        "Numeric Columns":
        int(len(numeric_df.columns)),

        "Missing Values":
        int(
            df.isna().sum().sum()
        ),

        "Duplicate Rows":
        int(
            df.duplicated().sum()
        )

    }

# =====================================================
# DATA QUALITY
# =====================================================

def data_quality_report(df):

    return pd.DataFrame({

        "Column":
        df.columns,

        "Data Type":
        df.dtypes.astype(str),

        "Missing":
        df.isna().sum(),

        "Unique":
        df.nunique()

    })

# =====================================================
# EXPORT SUMMARY
# =====================================================

def statistical_dashboard_summary(df):

    stats = statistical_summary(df)

    return pd.DataFrame({

        "Metric":
        stats.keys(),

        "Value":
        stats.values()

    })
