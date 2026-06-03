import pandas as pd
import numpy as np

from scipy.stats import (
    pearsonr,
    spearmanr,
    kendalltau
)


# =====================================================
# NUMERIC COLUMNS
# =====================================================

def numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


# =====================================================
# PEARSON CORRELATION
# =====================================================

def pearson_correlation(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    return numeric_df.corr(
        method="pearson"
    )


# =====================================================
# SPEARMAN CORRELATION
# =====================================================

def spearman_correlation(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    return numeric_df.corr(
        method="spearman"
    )


# =====================================================
# KENDALL CORRELATION
# =====================================================

def kendall_correlation(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    return numeric_df.corr(
        method="kendall"
    )


# =====================================================
# CORRELATION STRENGTH
# =====================================================

def correlation_strength(value):

    value = abs(value)

    if value >= 0.90:
        return "Very Strong"

    elif value >= 0.70:
        return "Strong"

    elif value >= 0.50:
        return "Moderate"

    elif value >= 0.30:
        return "Weak"

    else:
        return "Very Weak"


# =====================================================
# PAIRWISE PEARSON
# =====================================================

def pairwise_pearson(df):

    cols = numeric_columns(df)

    results = []

    for i in range(len(cols)):

        for j in range(i + 1, len(cols)):

            col1 = cols[i]
            col2 = cols[j]

            corr, p = pearsonr(
                df[col1],
                df[col2]
            )

            results.append([

                col1,
                col2,

                round(corr, 4),

                round(p, 6),

                correlation_strength(corr)

            ])

    return pd.DataFrame(

        results,

        columns=[

            "Variable 1",
            "Variable 2",
            "Pearson Correlation",
            "P Value",
            "Strength"

        ]

    )


# =====================================================
# PAIRWISE SPEARMAN
# =====================================================

def pairwise_spearman(df):

    cols = numeric_columns(df)

    results = []

    for i in range(len(cols)):

        for j in range(i + 1, len(cols)):

            col1 = cols[i]
            col2 = cols[j]

            corr, p = spearmanr(
                df[col1],
                df[col2]
            )

            results.append([

                col1,
                col2,

                round(corr, 4),

                round(p, 6),

                correlation_strength(corr)

            ])

    return pd.DataFrame(

        results,

        columns=[

            "Variable 1",
            "Variable 2",
            "Spearman Correlation",
            "P Value",
            "Strength"

        ]

    )


# =====================================================
# PAIRWISE KENDALL
# =====================================================

def pairwise_kendall(df):

    cols = numeric_columns(df)

    results = []

    for i in range(len(cols)):

        for j in range(i + 1, len(cols)):

            col1 = cols[i]
            col2 = cols[j]

            corr, p = kendalltau(
                df[col1],
                df[col2]
            )

            results.append([

                col1,
                col2,

                round(corr, 4),

                round(p, 6),

                correlation_strength(corr)

            ])

    return pd.DataFrame(

        results,

        columns=[

            "Variable 1",
            "Variable 2",
            "Kendall Correlation",
            "P Value",
            "Strength"

        ]

    )


# =====================================================
# CORRELATION P VALUE MATRIX
# =====================================================

def correlation_pvalues(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    cols = numeric_df.columns

    p_matrix = pd.DataFrame(
        np.ones(
            (len(cols), len(cols))
        ),
        columns=cols,
        index=cols
    )

    for i in range(len(cols)):

        for j in range(len(cols)):

            if i != j:

                _, p = pearsonr(
                    numeric_df.iloc[:, i],
                    numeric_df.iloc[:, j]
                )

                p_matrix.iloc[i, j] = p

    return p_matrix.round(6)


# =====================================================
# STRONG POSITIVE CORRELATIONS
# =====================================================

def strong_positive_correlations(
    df,
    threshold=0.70
):

    corr = pearson_correlation(df)

    pairs = []

    for i in range(len(corr.columns)):

        for j in range(i + 1, len(corr.columns)):

            value = corr.iloc[i, j]

            if value >= threshold:

                pairs.append([

                    corr.columns[i],
                    corr.columns[j],
                    round(value, 4)

                ])

    return pd.DataFrame(

        pairs,

        columns=[
            "Variable 1",
            "Variable 2",
            "Correlation"
        ]

    )


# =====================================================
# STRONG NEGATIVE CORRELATIONS
# =====================================================

def strong_negative_correlations(
    df,
    threshold=-0.70
):

    corr = pearson_correlation(df)

    pairs = []

    for i in range(len(corr.columns)):

        for j in range(i + 1, len(corr.columns)):

            value = corr.iloc[i, j]

            if value <= threshold:

                pairs.append([

                    corr.columns[i],
                    corr.columns[j],
                    round(value, 4)

                ])

    return pd.DataFrame(

        pairs,

        columns=[
            "Variable 1",
            "Variable 2",
            "Correlation"
        ]

    )


# =====================================================
# TOP CORRELATIONS
# =====================================================

def top_correlations(
    df,
    top_n=20
):

    corr = pearson_correlation(df)

    corr_pairs = (

        corr.unstack()

        .reset_index()

    )

    corr_pairs.columns = [

        "Variable 1",
        "Variable 2",
        "Correlation"

    ]

    corr_pairs = corr_pairs[
        corr_pairs["Variable 1"]
        !=
        corr_pairs["Variable 2"]
    ]

    corr_pairs["Abs"] = (
        corr_pairs["Correlation"]
        .abs()
    )

    corr_pairs = corr_pairs.sort_values(
        by="Abs",
        ascending=False
    )

    return corr_pairs.head(top_n)


# =====================================================
# YIELD DEPENDENCY ANALYSIS
# =====================================================

def yield_dependency_analysis(df):

    if "Yield_tons" not in df.columns:
        return pd.DataFrame()

    corr = pearson_correlation(df)

    yield_corr = corr[
        ["Yield_tons"]
    ].reset_index()

    yield_corr.columns = [
        "Feature",
        "Correlation_With_Yield"
    ]

    yield_corr["Strength"] = (

        yield_corr[
            "Correlation_With_Yield"
        ]

        .apply(
            correlation_strength
        )

    )

    return yield_corr.sort_values(

        by="Correlation_With_Yield",

        ascending=False

    )


# =====================================================
# RESOURCE DEPENDENCY
# =====================================================

def resource_dependency_analysis(df):

    resource_cols = [

        "Water_Usage_cubic_meters",

        "Fertilizer_Used_tons",

        "Pesticide_Used_kg",

        "Yield_tons"

    ]

    existing = [

        col

        for col in resource_cols

        if col in df.columns

    ]

    return df[
        existing
    ].corr().round(4)


# =====================================================
# CROP-WISE CORRELATION
# =====================================================

def crop_correlation_analysis(df):

    if "Crop_Type" not in df.columns:
        return {}

    results = {}

    for crop in df["Crop_Type"].unique():

        crop_df = df[
            df["Crop_Type"] == crop
        ]

        numeric_df = crop_df.select_dtypes(
            include=np.number
        )

        if len(numeric_df) > 2:

            results[crop] = (
                numeric_df.corr()
            )

    return results


# =====================================================
# CORRELATION SUMMARY
# =====================================================

def correlation_summary(df):

    pearson = pearson_correlation(df)

    avg_corr = (

        pearson.abs()

        .mean()

        .mean()

    )

    return {

        "Average Correlation":
        round(avg_corr, 4),

        "Numeric Variables":
        len(
            numeric_columns(df)
        ),

        "Strong Positive Pairs":
        len(
            strong_positive_correlations(df)
        ),

        "Strong Negative Pairs":
        len(
            strong_negative_correlations(df)
        )

    }


# =====================================================
# EXECUTIVE CORRELATION REPORT
# =====================================================

def executive_correlation_report(df):

    return {

        "Pearson Matrix":
        pearson_correlation(df),

        "Spearman Matrix":
        spearman_correlation(df),

        "Kendall Matrix":
        kendall_correlation(df),

        "Top Correlations":
        top_correlations(df),

        "Yield Dependency":
        yield_dependency_analysis(df),

        "Resource Dependency":
        resource_dependency_analysis(df),

        "Summary":
        correlation_summary(df)

    }
  
