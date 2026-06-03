import pandas as pd
import numpy as np


# =====================================================
# TOTAL WATER USAGE
# =====================================================

def total_water_usage(df):

    if "Water_Usage_cubic_meters" not in df.columns:
        return 0

    return round(
        df["Water_Usage_cubic_meters"].sum(),
        2
    )


# =====================================================
# AVERAGE WATER USAGE
# =====================================================

def average_water_usage(df):

    if "Water_Usage_cubic_meters" not in df.columns:
        return 0

    return round(
        df["Water_Usage_cubic_meters"].mean(),
        2
    )


# =====================================================
# MEDIAN WATER USAGE
# =====================================================

def median_water_usage(df):

    if "Water_Usage_cubic_meters" not in df.columns:
        return 0

    return round(
        df["Water_Usage_cubic_meters"].median(),
        2
    )


# =====================================================
# MAX WATER USAGE
# =====================================================

def maximum_water_usage(df):

    if "Water_Usage_cubic_meters" not in df.columns:
        return 0

    return round(
        df["Water_Usage_cubic_meters"].max(),
        2
    )


# =====================================================
# MIN WATER USAGE
# =====================================================

def minimum_water_usage(df):

    if "Water_Usage_cubic_meters" not in df.columns:
        return 0

    return round(
        df["Water_Usage_cubic_meters"].min(),
        2
    )


# =====================================================
# WATER PRODUCTIVITY
# =====================================================

def water_productivity(df):

    if (
        "Yield_tons" not in df.columns
        or
        "Water_Usage_cubic_meters" not in df.columns
    ):
        return 0

    return round(
        (
            df["Yield_tons"].sum()
            /
            df["Water_Usage_cubic_meters"].sum()
        ),
        6
    )


# =====================================================
# WATER FOOTPRINT
# =====================================================

def water_footprint(df):

    if (
        "Yield_tons" not in df.columns
        or
        "Water_Usage_cubic_meters" not in df.columns
    ):
        return 0

    return round(
        (
            df["Water_Usage_cubic_meters"].sum()
            /
            df["Yield_tons"].sum()
        ),
        4
    )


# =====================================================
# WATER INTENSITY
# =====================================================

def water_intensity(df):

    if (
        "Farm_Area_acres" not in df.columns
        or
        "Water_Usage_cubic_meters" not in df.columns
    ):
        return 0

    return round(
        (
            df["Water_Usage_cubic_meters"].sum()
            /
            df["Farm_Area_acres"].sum()
        ),
        4
    )


# =====================================================
# CREATE WATER PRODUCTIVITY COLUMN
# =====================================================

def create_water_metrics(df):

    data = df.copy()

    if (
        "Yield_tons" in data.columns
        and
        "Water_Usage_cubic_meters" in data.columns
    ):

        data["Water_Productivity"] = (
            data["Yield_tons"]
            /
            data["Water_Usage_cubic_meters"]
        )

        data["Water_Footprint"] = (
            data["Water_Usage_cubic_meters"]
            /
            data["Yield_tons"]
        )

    return data


# =====================================================
# CROP-WISE WATER ANALYSIS
# =====================================================

def crop_water_summary(df):

    return (
        df.groupby("Crop_Type")
        .agg(
            Total_Water=(
                "Water_Usage_cubic_meters",
                "sum"
            ),
            Average_Water=(
                "Water_Usage_cubic_meters",
                "mean"
            ),
            Farms=(
                "Crop_Type",
                "count"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Water",
            ascending=False
        )
    )


# =====================================================
# SOIL-WISE WATER ANALYSIS
# =====================================================

def soil_water_summary(df):

    return (
        df.groupby("Soil_Type")
        .agg(
            Total_Water=(
                "Water_Usage_cubic_meters",
                "sum"
            ),
            Average_Water=(
                "Water_Usage_cubic_meters",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Water",
            ascending=False
        )
    )


# =====================================================
# IRRIGATION-WISE WATER ANALYSIS
# =====================================================

def irrigation_water_summary(df):

    return (
        df.groupby("Irrigation_Type")
        .agg(
            Total_Water=(
                "Water_Usage_cubic_meters",
                "sum"
            ),
            Average_Water=(
                "Water_Usage_cubic_meters",
                "mean"
            ),
            Average_Yield=(
                "Yield_tons",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Water",
            ascending=False
        )
    )


# =====================================================
# SEASON-WISE WATER ANALYSIS
# =====================================================

def season_water_summary(df):

    return (
        df.groupby("Season")
        .agg(
            Total_Water=(
                "Water_Usage_cubic_meters",
                "sum"
            ),
            Average_Water=(
                "Water_Usage_cubic_meters",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            by="Total_Water",
            ascending=False
        )
    )


# =====================================================
# WATER EFFICIENCY BY CROP
# =====================================================

def crop_water_efficiency(df):

    summary = (
        df.groupby("Crop_Type")
        .agg(
            Total_Yield=(
                "Yield_tons",
                "sum"
            ),
            Total_Water=(
                "Water_Usage_cubic_meters",
                "sum"
            )
        )
        .reset_index()
    )

    summary["Water_Productivity"] = (
        summary["Total_Yield"]
        /
        summary["Total_Water"]
    )

    return summary.sort_values(
        by="Water_Productivity",
        ascending=False
    )


# =====================================================
# WATER RANKING
# =====================================================

def water_ranking(df):

    ranking = crop_water_efficiency(df)

    ranking["Rank"] = range(
        1,
        len(ranking) + 1
    )

    return ranking


# =====================================================
# WATER PARETO ANALYSIS
# =====================================================

def water_pareto_analysis(df):

    pareto = (
        df.groupby("Crop_Type")
        ["Water_Usage_cubic_meters"]
        .sum()
        .reset_index()
    )

    pareto = pareto.sort_values(
        by="Water_Usage_cubic_meters",
        ascending=False
    )

    pareto["Cumulative_Water"] = (
        pareto["Water_Usage_cubic_meters"]
        .cumsum()
    )

    pareto["Cumulative_%"] = (

        pareto["Cumulative_Water"]

        /

        pareto["Water_Usage_cubic_meters"].sum()

    ) * 100

    return pareto


# =====================================================
# WATER HEATMAPS
# =====================================================

def crop_irrigation_water_heatmap(df):

    return pd.pivot_table(
        df,
        values="Water_Usage_cubic_meters",
        index="Crop_Type",
        columns="Irrigation_Type",
        aggfunc="mean"
    )


def crop_soil_water_heatmap(df):

    return pd.pivot_table(
        df,
        values="Water_Usage_cubic_meters",
        index="Crop_Type",
        columns="Soil_Type",
        aggfunc="mean"
    )


def season_crop_water_heatmap(df):

    return pd.pivot_table(
        df,
        values="Water_Usage_cubic_meters",
        index="Season",
        columns="Crop_Type",
        aggfunc="mean"
    )


# =====================================================
# WATER DISTRIBUTION SUMMARY
# =====================================================

def water_distribution_summary(df):

    water = df["Water_Usage_cubic_meters"]

    summary = {

        "Mean":
        round(water.mean(), 2),

        "Median":
        round(water.median(), 2),

        "Minimum":
        round(water.min(), 2),

        "Maximum":
        round(water.max(), 2),

        "Std Dev":
        round(water.std(), 2),

        "Variance":
        round(water.var(), 2),

        "Q1":
        round(water.quantile(0.25), 2),

        "Q3":
        round(water.quantile(0.75), 2)

    }

    return pd.DataFrame(
        summary.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )


# =====================================================
# EXECUTIVE WATER SUMMARY
# =====================================================

def executive_water_summary(df):

    return {

        "Total Water":
        total_water_usage(df),

        "Average Water":
        average_water_usage(df),

        "Median Water":
        median_water_usage(df),

        "Maximum Water":
        maximum_water_usage(df),

        "Minimum Water":
        minimum_water_usage(df),

        "Water Productivity":
        water_productivity(df),

        "Water Footprint":
        water_footprint(df),

        "Water Intensity":
        water_intensity(df)

    }
