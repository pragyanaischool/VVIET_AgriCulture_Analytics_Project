import pandas as pd
import numpy as np

# =====================================================
# EXECUTIVE YIELD SUMMARY
# =====================================================

def executive_yield_summary(df):

    if df.empty:

        return {

            "Total Yield": 0,

            "Average Yield": 0,

            "Maximum Yield": 0,

            "Yield Per Acre": 0,

            "Best Crop": "N/A"

        }

    total_yield = df["Yield_tons"].sum()

    avg_yield = df["Yield_tons"].mean()

    max_yield = df["Yield_tons"].max()

    total_area = df["Farm_Area_acres"].sum()

    yield_per_acre = 0

    if total_area > 0:

        yield_per_acre = total_yield / total_area

    crop_summary = (
        df.groupby("Crop_Type")["Yield_tons"]
        .sum()
        .reset_index()
    )

    best_crop = crop_summary.loc[
        crop_summary["Yield_tons"].idxmax(),
        "Crop_Type"
    ]

    return {

        "Total Yield":
        round(total_yield, 2),

        "Average Yield":
        round(avg_yield, 2),

        "Maximum Yield":
        round(max_yield, 2),

        "Yield Per Acre":
        round(yield_per_acre, 2),

        "Best Crop":
        best_crop

    }

# =====================================================
# CROP YIELD SUMMARY
# =====================================================

def crop_yield_summary(df):

    return (

        df.groupby("Crop_Type")

        .agg(

            Total_Yield=(
                "Yield_tons",
                "sum"
            ),

            Average_Yield=(
                "Yield_tons",
                "mean"
            ),

            Maximum_Yield=(
                "Yield_tons",
                "max"
            )

        )

        .reset_index()

        .sort_values(
            "Total_Yield",
            ascending=False
        )

    )

# =====================================================
# SEASON YIELD SUMMARY
# =====================================================

def season_yield_summary(df):

    return (

        df.groupby("Season")

        .agg(

            Total_Yield=(
                "Yield_tons",
                "sum"
            ),

            Average_Yield=(
                "Yield_tons",
                "mean"
            )

        )

        .reset_index()

    )

# =====================================================
# SOIL YIELD SUMMARY
# =====================================================

def soil_yield_summary(df):

    return (

        df.groupby("Soil_Type")

        .agg(

            Total_Yield=(
                "Yield_tons",
                "sum"
            ),

            Average_Yield=(
                "Yield_tons",
                "mean"
            )

        )

        .reset_index()

    )

# =====================================================
# IRRIGATION YIELD SUMMARY
# =====================================================

def irrigation_yield_summary(df):

    return (

        df.groupby("Irrigation_Type")

        .agg(

            Total_Yield=(
                "Yield_tons",
                "sum"
            ),

            Average_Yield=(
                "Yield_tons",
                "mean"
            )

        )

        .reset_index()

    )

# =====================================================
# CROP RANKING
# =====================================================

def crop_ranking(df):

    ranking = crop_yield_summary(df)

    ranking["Rank"] = (

        ranking["Total_Yield"]

        .rank(

            ascending=False,

            method="dense"

        )

        .astype(int)

    )

    return ranking.sort_values("Rank")

# =====================================================
# TOP CROPS
# =====================================================

def top_crops(
    df,
    top_n=10
):

    return crop_yield_summary(
        df
    ).head(top_n)

# =====================================================
# BOTTOM CROPS
# =====================================================

def bottom_crops(
    df,
    top_n=10
):

    return crop_yield_summary(
        df
    ).tail(top_n)

# =====================================================
# PARETO ANALYSIS
# =====================================================

def pareto_yield_analysis(df):

    pareto = (

        df.groupby("Crop_Type")

        ["Yield_tons"]

        .sum()

        .reset_index()

        .sort_values(

            "Yield_tons",

            ascending=False

        )

    )

    pareto["Cumulative_%"] = (

        pareto["Yield_tons"]

        .cumsum()

        /

        pareto["Yield_tons"].sum()

        * 100

    )

    return pareto

# =====================================================
# CROP SOIL HEATMAP
# =====================================================

def crop_soil_heatmap(df):

    return pd.pivot_table(

        df,

        values="Yield_tons",

        index="Crop_Type",

        columns="Soil_Type",

        aggfunc="mean",

        fill_value=0

    )

# =====================================================
# CROP IRRIGATION HEATMAP
# =====================================================

def crop_irrigation_heatmap(df):

    return pd.pivot_table(

        df,

        values="Yield_tons",

        index="Crop_Type",

        columns="Irrigation_Type",

        aggfunc="mean",

        fill_value=0

    )

# =====================================================
# SEASON CROP HEATMAP
# =====================================================

def season_crop_heatmap(df):

    return pd.pivot_table(

        df,

        values="Yield_tons",

        index="Season",

        columns="Crop_Type",

        aggfunc="mean",

        fill_value=0

    )

# =====================================================
# YIELD DISTRIBUTION SUMMARY
# =====================================================

def yield_distribution_summary(df):

    yield_data = df["Yield_tons"]

    return pd.DataFrame({

        "Metric": [

            "Mean",

            "Median",

            "Minimum",

            "Maximum",

            "Standard Deviation",

            "Variance",

            "Q1",

            "Q3"

        ],

        "Value": [

            yield_data.mean(),

            yield_data.median(),

            yield_data.min(),

            yield_data.max(),

            yield_data.std(),

            yield_data.var(),

            yield_data.quantile(0.25),

            yield_data.quantile(0.75)

        ]

    })

# =====================================================
# FARM PERFORMANCE
# =====================================================

def farm_performance(df):

    if "Farm_Area_acres" not in df.columns:

        return pd.DataFrame()

    result = (

        df.groupby("Crop_Type")

        .agg(

            Total_Yield=(
                "Yield_tons",
                "sum"
            ),

            Total_Farm_Area=(
                "Farm_Area_acres",
                "sum"
            )

        )

        .reset_index()

    )

    result["Yield_Per_Acre"] = np.where(

        result["Total_Farm_Area"] > 0,

        result["Total_Yield"]
        /
        result["Total_Farm_Area"],

        0

    )

    return result.sort_values(

        "Yield_Per_Acre",

        ascending=False

    )
    
