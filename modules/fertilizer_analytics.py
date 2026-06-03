import pandas as pd
import numpy as np


# =====================================================
# TOTAL FERTILIZER
# =====================================================

def total_fertilizer(df):

    if "Fertilizer_Used_tons" not in df.columns:
        return 0

    return round(
        df["Fertilizer_Used_tons"].sum(),
        2
    )


# =====================================================
# AVERAGE FERTILIZER
# =====================================================

def average_fertilizer(df):

    if "Fertilizer_Used_tons" not in df.columns:
        return 0

    return round(
        df["Fertilizer_Used_tons"].mean(),
        2
    )


# =====================================================
# MEDIAN FERTILIZER
# =====================================================

def median_fertilizer(df):

    if "Fertilizer_Used_tons" not in df.columns:
        return 0

    return round(
        df["Fertilizer_Used_tons"].median(),
        2
    )


# =====================================================
# MAX FERTILIZER
# =====================================================

def maximum_fertilizer(df):

    if "Fertilizer_Used_tons" not in df.columns:
        return 0

    return round(
        df["Fertilizer_Used_tons"].max(),
        2
    )


# =====================================================
# MIN FERTILIZER
# =====================================================

def minimum_fertilizer(df):

    if "Fertilizer_Used_tons" not in df.columns:
        return 0

    return round(
        df["Fertilizer_Used_tons"].min(),
        2
    )


# =====================================================
# FERTILIZER EFFICIENCY
# =====================================================

def fertilizer_efficiency(df):

    if (
        "Yield_tons" not in df.columns
        or
        "Fertilizer_Used_tons" not in df.columns
    ):
        return 0

    return round(
        (
            df["Yield_tons"].sum()
            /
            df["Fertilizer_Used_tons"].sum()
        ),
        4
    )


# =====================================================
# FERTILIZER INTENSITY
# =====================================================

def fertilizer_intensity(df):

    if (
        "Farm_Area_acres" not in df.columns
        or
        "Fertilizer_Used_tons" not in df.columns
    ):
        return 0

    return round(
        (
            df["Fertilizer_Used_tons"].sum()
            /
            df["Farm_Area_acres"].sum()
        ),
        4
    )


# =====================================================
# CREATE FERTILIZER METRICS
# =====================================================

def create_fertilizer_metrics(df):

    data = df.copy()

    if (
        "Yield_tons" in data.columns
        and
        "Fertilizer_Used_tons" in data.columns
    ):

        data["Fertilizer_Efficiency"] = (
            data["Yield_tons"]
            /
            data["Fertilizer_Used_tons"]
        )

    return data


# =====================================================
# CROP-WISE FERTILIZER
# =====================================================

def crop_fertilizer_summary(df):

    return (
        df.groupby("Crop_Type")
        .agg(
            Total_Fertilizer=(
                "Fertilizer_Used_tons",
                "sum"
            ),
            Average_Fertilizer=(
                "Fertilizer_Used_tons",
                "mean"
            ),
            Average_Yield=(
                "Yield_tons",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Fertilizer",
            ascending=False
        )
    )


# =====================================================
# SOIL-WISE FERTILIZER
# =====================================================

def soil_fertilizer_summary(df):

    return (
        df.groupby("Soil_Type")
        .agg(
            Total_Fertilizer=(
                "Fertilizer_Used_tons",
                "sum"
            ),
            Average_Fertilizer=(
                "Fertilizer_Used_tons",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Fertilizer",
            ascending=False
        )
    )


# =====================================================
# SEASON-WISE FERTILIZER
# =====================================================

def season_fertilizer_summary(df):

    return (
        df.groupby("Season")
        .agg(
            Total_Fertilizer=(
                "Fertilizer_Used_tons",
                "sum"
            ),
            Average_Fertilizer=(
                "Fertilizer_Used_tons",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Fertilizer",
            ascending=False
        )
    )


# =====================================================
# IRRIGATION-WISE FERTILIZER
# =====================================================

def irrigation_fertilizer_summary(df):

    return (
        df.groupby("Irrigation_Type")
        .agg(
            Total_Fertilizer=(
                "Fertilizer_Used_tons",
                "sum"
            ),
            Average_Fertilizer=(
                "Fertilizer_Used_tons",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Fertilizer",
            ascending=False
        )
    )


# =====================================================
# FERTILIZER EFFICIENCY BY CROP
# =====================================================

def crop_fertilizer_efficiency(df):

    summary = (
        df.groupby("Crop_Type")
        .agg(
            Total_Yield=("Yield_tons", "sum"),
            Total_Fertilizer=(
                "Fertilizer_Used_tons",
                "sum"
            )
        )
        .reset_index()
    )

    summary["Fertilizer_Efficiency"] = (
        summary["Total_Yield"]
        /
        summary["Total_Fertilizer"]
    )

    return summary.sort_values(
        by="Fertilizer_Efficiency",
        ascending=False
    )


# =====================================================
# FERTILIZER RANKING
# =====================================================

def fertilizer_ranking(df):

    ranking = crop_fertilizer_efficiency(df)

    ranking["Rank"] = range(
        1,
        len(ranking) + 1
    )

    return ranking


# =====================================================
# FERTILIZER PARETO ANALYSIS
# =====================================================

def fertilizer_pareto_analysis(df):

    pareto = (
        df.groupby("Crop_Type")
        ["Fertilizer_Used_tons"]
        .sum()
        .reset_index()
    )

    pareto = pareto.sort_values(
        by="Fertilizer_Used_tons",
        ascending=False
    )

    pareto["Cumulative_Fertilizer"] = (
        pareto["Fertilizer_Used_tons"]
        .cumsum()
    )

    pareto["Cumulative_%"] = (

        pareto["Cumulative_Fertilizer"]

        /

        pareto["Fertilizer_Used_tons"].sum()

    ) * 100

    return pareto


# =====================================================
# HEATMAP DATA
# =====================================================

def crop_soil_fertilizer_heatmap(df):

    return pd.pivot_table(
        df,
        values="Fertilizer_Used_tons",
        index="Crop_Type",
        columns="Soil_Type",
        aggfunc="mean"
    )


def crop_irrigation_fertilizer_heatmap(df):

    return pd.pivot_table(
        df,
        values="Fertilizer_Used_tons",
        index="Crop_Type",
        columns="Irrigation_Type",
        aggfunc="mean"
    )


def season_crop_fertilizer_heatmap(df):

    return pd.pivot_table(
        df,
        values="Fertilizer_Used_tons",
        index="Season",
        columns="Crop_Type",
        aggfunc="mean"
    )


# =====================================================
# DISTRIBUTION SUMMARY
# =====================================================

def fertilizer_distribution_summary(df):

    fert = df["Fertilizer_Used_tons"]

    summary = {

        "Mean": round(fert.mean(), 2),
        "Median": round(fert.median(), 2),
        "Minimum": round(fert.min(), 2),
        "Maximum": round(fert.max(), 2),
        "Std Dev": round(fert.std(), 2),
        "Variance": round(fert.var(), 2),
        "Q1": round(fert.quantile(0.25), 2),
        "Q3": round(fert.quantile(0.75), 2)

    }

    return pd.DataFrame(
        summary.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_fertilizer_summary(df):

    return {

        "Total Fertilizer":
        total_fertilizer(df),

        "Average Fertilizer":
        average_fertilizer(df),

        "Median Fertilizer":
        median_fertilizer(df),

        "Maximum Fertilizer":
        maximum_fertilizer(df),

        "Minimum Fertilizer":
        minimum_fertilizer(df),

        "Fertilizer Efficiency":
        fertilizer_efficiency(df),

        "Fertilizer Intensity":
        fertilizer_intensity(df)

    }
