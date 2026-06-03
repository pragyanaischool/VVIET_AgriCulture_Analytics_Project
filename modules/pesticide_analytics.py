import pandas as pd
import numpy as np


# =====================================================
# TOTAL PESTICIDE
# =====================================================

def total_pesticide(df):

    if "Pesticide_Used_kg" not in df.columns:
        return 0

    return round(
        df["Pesticide_Used_kg"].sum(),
        2
    )


# =====================================================
# AVERAGE PESTICIDE
# =====================================================

def average_pesticide(df):

    if "Pesticide_Used_kg" not in df.columns:
        return 0

    return round(
        df["Pesticide_Used_kg"].mean(),
        2
    )


# =====================================================
# MEDIAN PESTICIDE
# =====================================================

def median_pesticide(df):

    if "Pesticide_Used_kg" not in df.columns:
        return 0

    return round(
        df["Pesticide_Used_kg"].median(),
        2
    )


# =====================================================
# MAXIMUM PESTICIDE
# =====================================================

def maximum_pesticide(df):

    if "Pesticide_Used_kg" not in df.columns:
        return 0

    return round(
        df["Pesticide_Used_kg"].max(),
        2
    )


# =====================================================
# MINIMUM PESTICIDE
# =====================================================

def minimum_pesticide(df):

    if "Pesticide_Used_kg" not in df.columns:
        return 0

    return round(
        df["Pesticide_Used_kg"].min(),
        2
    )


# =====================================================
# PESTICIDE EFFICIENCY
# =====================================================

def pesticide_efficiency(df):

    if (
        "Yield_tons" not in df.columns
        or
        "Pesticide_Used_kg" not in df.columns
    ):
        return 0

    return round(
        (
            df["Yield_tons"].sum()
            /
            df["Pesticide_Used_kg"].sum()
        ),
        6
    )


# =====================================================
# PESTICIDE INTENSITY
# =====================================================

def pesticide_intensity(df):

    if (
        "Farm_Area_acres" not in df.columns
        or
        "Pesticide_Used_kg" not in df.columns
    ):
        return 0

    return round(
        (
            df["Pesticide_Used_kg"].sum()
            /
            df["Farm_Area_acres"].sum()
        ),
        4
    )


# =====================================================
# CREATE PESTICIDE METRICS
# =====================================================

def create_pesticide_metrics(df):

    data = df.copy()

    if (
        "Yield_tons" in data.columns
        and
        "Pesticide_Used_kg" in data.columns
    ):

        data["Pesticide_Efficiency"] = (
            data["Yield_tons"]
            /
            data["Pesticide_Used_kg"]
        )

    return data


# =====================================================
# CROP-WISE PESTICIDE ANALYSIS
# =====================================================

def crop_pesticide_summary(df):

    return (
        df.groupby("Crop_Type")
        .agg(
            Total_Pesticide=(
                "Pesticide_Used_kg",
                "sum"
            ),
            Average_Pesticide=(
                "Pesticide_Used_kg",
                "mean"
            ),
            Average_Yield=(
                "Yield_tons",
                "mean"
            ),
            Farms=(
                "Crop_Type",
                "count"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Pesticide",
            ascending=False
        )
    )


# =====================================================
# SOIL-WISE PESTICIDE ANALYSIS
# =====================================================

def soil_pesticide_summary(df):

    return (
        df.groupby("Soil_Type")
        .agg(
            Total_Pesticide=(
                "Pesticide_Used_kg",
                "sum"
            ),
            Average_Pesticide=(
                "Pesticide_Used_kg",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Pesticide",
            ascending=False
        )
    )


# =====================================================
# SEASON-WISE PESTICIDE ANALYSIS
# =====================================================

def season_pesticide_summary(df):

    return (
        df.groupby("Season")
        .agg(
            Total_Pesticide=(
                "Pesticide_Used_kg",
                "sum"
            ),
            Average_Pesticide=(
                "Pesticide_Used_kg",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Pesticide",
            ascending=False
        )
    )


# =====================================================
# IRRIGATION-WISE PESTICIDE ANALYSIS
# =====================================================

def irrigation_pesticide_summary(df):

    return (
        df.groupby("Irrigation_Type")
        .agg(
            Total_Pesticide=(
                "Pesticide_Used_kg",
                "sum"
            ),
            Average_Pesticide=(
                "Pesticide_Used_kg",
                "mean"
            ),
            Average_Yield=(
                "Yield_tons",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Pesticide",
            ascending=False
        )
    )


# =====================================================
# PESTICIDE EFFICIENCY BY CROP
# =====================================================

def crop_pesticide_efficiency(df):

    summary = (
        df.groupby("Crop_Type")
        .agg(
            Total_Yield=("Yield_tons", "sum"),
            Total_Pesticide=(
                "Pesticide_Used_kg",
                "sum"
            )
        )
        .reset_index()
    )

    summary["Pesticide_Efficiency"] = (
        summary["Total_Yield"]
        /
        summary["Total_Pesticide"]
    )

    return summary.sort_values(
        by="Pesticide_Efficiency",
        ascending=False
    )


# =====================================================
# PESTICIDE RANKING
# =====================================================

def pesticide_ranking(df):

    ranking = crop_pesticide_efficiency(df)

    ranking["Rank"] = range(
        1,
        len(ranking) + 1
    )

    return ranking


# =====================================================
# PESTICIDE PARETO ANALYSIS
# =====================================================

def pesticide_pareto_analysis(df):

    pareto = (
        df.groupby("Crop_Type")
        ["Pesticide_Used_kg"]
        .sum()
        .reset_index()
    )

    pareto = pareto.sort_values(
        by="Pesticide_Used_kg",
        ascending=False
    )

    pareto["Cumulative_Pesticide"] = (
        pareto["Pesticide_Used_kg"]
        .cumsum()
    )

    pareto["Cumulative_%"] = (

        pareto["Cumulative_Pesticide"]

        /

        pareto["Pesticide_Used_kg"].sum()

    ) * 100

    return pareto


# =====================================================
# HEATMAP DATA
# =====================================================

def crop_soil_pesticide_heatmap(df):

    return pd.pivot_table(
        df,
        values="Pesticide_Used_kg",
        index="Crop_Type",
        columns="Soil_Type",
        aggfunc="mean"
    )


def crop_irrigation_pesticide_heatmap(df):

    return pd.pivot_table(
        df,
        values="Pesticide_Used_kg",
        index="Crop_Type",
        columns="Irrigation_Type",
        aggfunc="mean"
    )


def season_crop_pesticide_heatmap(df):

    return pd.pivot_table(
        df,
        values="Pesticide_Used_kg",
        index="Season",
        columns="Crop_Type",
        aggfunc="mean"
    )


# =====================================================
# DISTRIBUTION SUMMARY
# =====================================================

def pesticide_distribution_summary(df):

    pesticide = df["Pesticide_Used_kg"]

    summary = {

        "Mean":
        round(pesticide.mean(), 2),

        "Median":
        round(pesticide.median(), 2),

        "Minimum":
        round(pesticide.min(), 2),

        "Maximum":
        round(pesticide.max(), 2),

        "Std Dev":
        round(pesticide.std(), 2),

        "Variance":
        round(pesticide.var(), 2),

        "Q1":
        round(
            pesticide.quantile(0.25),
            2
        ),

        "Q3":
        round(
            pesticide.quantile(0.75),
            2
        )

    }

    return pd.DataFrame(
        summary.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )


# =====================================================
# TOP PESTICIDE CONSUMING CROPS
# =====================================================

def top_pesticide_consumers(
    df,
    top_n=10
):

    return (
        crop_pesticide_summary(df)
        .head(top_n)
    )


# =====================================================
# LOWEST PESTICIDE CONSUMING CROPS
# =====================================================

def lowest_pesticide_consumers(
    df,
    top_n=10
):

    return (
        crop_pesticide_summary(df)
        .tail(top_n)
    )


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_pesticide_summary(df):

    return {

        "Total Pesticide":
        total_pesticide(df),

        "Average Pesticide":
        average_pesticide(df),

        "Median Pesticide":
        median_pesticide(df),

        "Maximum Pesticide":
        maximum_pesticide(df),

        "Minimum Pesticide":
        minimum_pesticide(df),

        "Pesticide Efficiency":
        pesticide_efficiency(df),

        "Pesticide Intensity":
        pesticide_intensity(df)

    }
