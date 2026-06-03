import pandas as pd
import numpy as np


# =====================================================
# TOTAL YIELD
# =====================================================

def total_yield(df):

    if "Yield_tons" not in df.columns:
        return 0

    return round(
        df["Yield_tons"].sum(),
        2
    )


# =====================================================
# AVERAGE YIELD
# =====================================================

def average_yield(df):

    if "Yield_tons" not in df.columns:
        return 0

    return round(
        df["Yield_tons"].mean(),
        2
    )


# =====================================================
# MEDIAN YIELD
# =====================================================

def median_yield(df):

    if "Yield_tons" not in df.columns:
        return 0

    return round(
        df["Yield_tons"].median(),
        2
    )


# =====================================================
# MAXIMUM YIELD
# =====================================================

def maximum_yield(df):

    if "Yield_tons" not in df.columns:
        return 0

    return round(
        df["Yield_tons"].max(),
        2
    )


# =====================================================
# MINIMUM YIELD
# =====================================================

def minimum_yield(df):

    if "Yield_tons" not in df.columns:
        return 0

    return round(
        df["Yield_tons"].min(),
        2
    )


# =====================================================
# YIELD PER ACRE
# =====================================================

def yield_per_acre(df):

    if (
        "Yield_tons" not in df.columns
        or
        "Farm_Area_acres" not in df.columns
    ):
        return 0

    return round(
        (
            df["Yield_tons"].sum()
            /
            df["Farm_Area_acres"].sum()
        ),
        4
    )


# =====================================================
# ADD YIELD PER ACRE COLUMN
# =====================================================

def create_yield_efficiency(df):

    data = df.copy()

    if (
        "Yield_tons" in data.columns
        and
        "Farm_Area_acres" in data.columns
    ):

        data["Yield_Per_Acre"] = (
            data["Yield_tons"]
            /
            data["Farm_Area_acres"]
        )

    return data


# =====================================================
# CROP-WISE YIELD
# =====================================================

def crop_yield_summary(df):

    return (
        df.groupby("Crop_Type")
        .agg(
            Total_Yield=("Yield_tons", "sum"),
            Average_Yield=("Yield_tons", "mean"),
            Max_Yield=("Yield_tons", "max"),
            Min_Yield=("Yield_tons", "min"),
            Farms=("Crop_Type", "count")
        )
        .reset_index()
        .sort_values(
            by="Total_Yield",
            ascending=False
        )
    )


# =====================================================
# SEASON-WISE YIELD
# =====================================================

def season_yield_summary(df):

    return (
        df.groupby("Season")
        .agg(
            Total_Yield=("Yield_tons", "sum"),
            Average_Yield=("Yield_tons", "mean"),
            Farms=("Season", "count")
        )
        .reset_index()
        .sort_values(
            by="Total_Yield",
            ascending=False
        )
    )


# =====================================================
# SOIL-WISE YIELD
# =====================================================

def soil_yield_summary(df):

    return (
        df.groupby("Soil_Type")
        .agg(
            Total_Yield=("Yield_tons", "sum"),
            Average_Yield=("Yield_tons", "mean"),
            Farms=("Soil_Type", "count")
        )
        .reset_index()
        .sort_values(
            by="Total_Yield",
            ascending=False
        )
    )


# =====================================================
# IRRIGATION-WISE YIELD
# =====================================================

def irrigation_yield_summary(df):

    return (
        df.groupby("Irrigation_Type")
        .agg(
            Total_Yield=("Yield_tons", "sum"),
            Average_Yield=("Yield_tons", "mean"),
            Farms=("Irrigation_Type", "count")
        )
        .reset_index()
        .sort_values(
            by="Total_Yield",
            ascending=False
        )
    )


# =====================================================
# TOP CROPS
# =====================================================

def top_crops(df, top_n=10):

    crop_df = crop_yield_summary(df)

    return crop_df.head(top_n)


# =====================================================
# BOTTOM CROPS
# =====================================================

def bottom_crops(df, top_n=10):

    crop_df = crop_yield_summary(df)

    return crop_df.tail(top_n)


# =====================================================
# BEST CROP
# =====================================================

def best_crop(df):

    crop_df = crop_yield_summary(df)

    return crop_df.iloc[0]["Crop_Type"]


# =====================================================
# BEST SEASON
# =====================================================

def best_season(df):

    season_df = season_yield_summary(df)

    return season_df.iloc[0]["Season"]


# =====================================================
# BEST SOIL
# =====================================================

def best_soil(df):

    soil_df = soil_yield_summary(df)

    return soil_df.iloc[0]["Soil_Type"]


# =====================================================
# BEST IRRIGATION
# =====================================================

def best_irrigation(df):

    irrigation_df = irrigation_yield_summary(df)

    return irrigation_df.iloc[0]["Irrigation_Type"]


# =====================================================
# CROP RANKING
# =====================================================

def crop_ranking(df):

    ranking = crop_yield_summary(df)

    ranking["Rank"] = range(
        1,
        len(ranking) + 1
    )

    return ranking[
        [
            "Rank",
            "Crop_Type",
            "Total_Yield",
            "Average_Yield"
        ]
    ]


# =====================================================
# YIELD PARETO ANALYSIS
# =====================================================

def pareto_yield_analysis(df):

    pareto = (
        df.groupby("Crop_Type")
        ["Yield_tons"]
        .sum()
        .reset_index()
    )

    pareto = pareto.sort_values(
        by="Yield_tons",
        ascending=False
    )

    pareto["Cumulative_Yield"] = (
        pareto["Yield_tons"]
        .cumsum()
    )

    pareto["Cumulative_%"] = (

        pareto["Cumulative_Yield"]

        /

        pareto["Yield_tons"].sum()

    ) * 100

    return pareto


# =====================================================
# CROP VS SOIL HEATMAP DATA
# =====================================================

def crop_soil_heatmap(df):

    return pd.pivot_table(
        df,
        values="Yield_tons",
        index="Crop_Type",
        columns="Soil_Type",
        aggfunc="mean"
    )


# =====================================================
# CROP VS IRRIGATION HEATMAP DATA
# =====================================================

def crop_irrigation_heatmap(df):

    return pd.pivot_table(
        df,
        values="Yield_tons",
        index="Crop_Type",
        columns="Irrigation_Type",
        aggfunc="mean"
    )


# =====================================================
# SEASON VS CROP HEATMAP DATA
# =====================================================

def season_crop_heatmap(df):

    return pd.pivot_table(
        df,
        values="Yield_tons",
        index="Season",
        columns="Crop_Type",
        aggfunc="mean"
    )


# =====================================================
# YIELD DISTRIBUTION SUMMARY
# =====================================================

def yield_distribution_summary(df):

    yield_col = df["Yield_tons"]

    summary = {

        "Mean":
        round(yield_col.mean(), 2),

        "Median":
        round(yield_col.median(), 2),

        "Minimum":
        round(yield_col.min(), 2),

        "Maximum":
        round(yield_col.max(), 2),

        "Standard Deviation":
        round(yield_col.std(), 2),

        "Variance":
        round(yield_col.var(), 2),

        "Q1":
        round(
            yield_col.quantile(0.25),
            2
        ),

        "Q3":
        round(
            yield_col.quantile(0.75),
            2
        )

    }

    return pd.DataFrame(
        summary.items(),
        columns=["Metric", "Value"]
    )


# =====================================================
# FARM PERFORMANCE TABLE
# =====================================================

def farm_performance(df):

    columns = [
        "Farm_ID",
        "Crop_Type",
        "Yield_tons"
    ]

    if "Farm_Area_acres" in df.columns:

        temp = create_yield_efficiency(df)

        columns.append(
            "Yield_Per_Acre"
        )

        return temp[
            columns
        ].sort_values(
            by="Yield_tons",
            ascending=False
        )

    return df[
        columns
    ].sort_values(
        by="Yield_tons",
        ascending=False
    )


# =====================================================
# EXECUTIVE YIELD SUMMARY
# =====================================================

def executive_yield_summary(df):

    return {

        "Total Yield":
        total_yield(df),

        "Average Yield":
        average_yield(df),

        "Median Yield":
        median_yield(df),

        "Maximum Yield":
        maximum_yield(df),

        "Minimum Yield":
        minimum_yield(df),

        "Yield Per Acre":
        yield_per_acre(df),

        "Best Crop":
        best_crop(df),

        "Best Season":
        best_season(df),

        "Best Soil":
        best_soil(df),

        "Best Irrigation":
        best_irrigation(df)

    }
    }
