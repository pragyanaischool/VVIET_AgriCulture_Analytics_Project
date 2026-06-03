import pandas as pd
import numpy as np

# =====================================================
# EXECUTIVE WATER SUMMARY
# =====================================================

def executive_water_summary(df):

    if df.empty:

        return {
            "Total Water": 0,
            "Average Water": 0,
            "Maximum Water": 0,
            "Water Productivity": 0
        }

    total_water = df["Water_Usage_cubic_meters"].sum()

    total_yield = df["Yield_tons"].sum()

    productivity = 0

    if total_water > 0:

        productivity = (
            total_yield /
            total_water
        )

    return {

        "Total Water":
        round(total_water, 2),

        "Average Water":
        round(
            df["Water_Usage_cubic_meters"].mean(),
            2
        ),

        "Maximum Water":
        round(
            df["Water_Usage_cubic_meters"].max(),
            2
        ),

        "Water Productivity":
        round(
            productivity,
            4
        )

    }


# =====================================================
# CROP WATER SUMMARY
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

            Maximum_Water=(
                "Water_Usage_cubic_meters",
                "max"
            )

        )

        .reset_index()

        .sort_values(
            "Total_Water",
            ascending=False
        )

    )


# =====================================================
# SEASON WATER SUMMARY
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

    )


# =====================================================
# WATER EFFICIENCY
# =====================================================

def crop_water_efficiency(df):

    result = (

        df.groupby("Crop_Type")

        .agg(

            Yield=(
                "Yield_tons",
                "sum"
            ),

            Water=(
                "Water_Usage_cubic_meters",
                "sum"
            )

        )

        .reset_index()

    )

    result["Water_Efficiency"] = np.where(

        result["Water"] > 0,

        result["Yield"] /
        result["Water"],

        0

    )

    return (

        result[

            [

                "Crop_Type",

                "Water_Efficiency"

            ]

        ]

        .sort_values(

            "Water_Efficiency",

            ascending=False

        )

    )


# =====================================================
# WATER PRODUCTIVITY
# =====================================================

def water_productivity(df):

    total_water = (
        df["Water_Usage_cubic_meters"]
        .sum()
    )

    total_yield = (
        df["Yield_tons"]
        .sum()
    )

    if total_water == 0:

        return 0

    return round(

        total_yield /
        total_water,

        4

    )


# =====================================================
# WATER RANKING
# =====================================================

def water_ranking(df):

    result = crop_water_efficiency(df)

    result["Rank"] = (

        result["Water_Efficiency"]

        .rank(

            ascending=False,

            method="dense"

        )

        .astype(int)

    )

    return result


# =====================================================
# TOP WATER CROPS
# =====================================================

def top_water_efficient_crops(
    df,
    top_n=10
):

    return (

        crop_water_efficiency(df)

        .head(top_n)

    )


# =====================================================
# LOW WATER CROPS
# =====================================================

def low_water_efficient_crops(
    df,
    top_n=10
):

    return (

        crop_water_efficiency(df)

        .tail(top_n)

    )


# =====================================================
# WATER HEATMAP
# =====================================================

def water_heatmap(df):

    return pd.pivot_table(

        df,

        values="Water_Usage_cubic_meters",

        index="Crop_Type",

        columns="Season",

        aggfunc="mean",

        fill_value=0

    )


# =====================================================
# WATER DISTRIBUTION
# =====================================================

def water_distribution_summary(df):

    water = df[
        "Water_Usage_cubic_meters"
    ]

    return pd.DataFrame({

        "Metric": [

            "Mean",

            "Median",

            "Minimum",

            "Maximum",

            "Std Dev",

            "Variance",

            "Q1",

            "Q3"

        ],

        "Value": [

            water.mean(),

            water.median(),

            water.min(),

            water.max(),

            water.std(),

            water.var(),

            water.quantile(0.25),

            water.quantile(0.75)

        ]

    })


# =====================================================
# WATER FOOTPRINT
# =====================================================

def water_footprint(df):

    total_water = (
        df["Water_Usage_cubic_meters"]
        .sum()
    )

    total_yield = (
        df["Yield_tons"]
        .sum()
    )

    if total_yield == 0:

        return 0

    return round(

        total_water /
        total_yield,

        4

    )


# =====================================================
# WATER INSIGHTS
# =====================================================

def water_insights(df):

    ranking = crop_water_efficiency(df)

    if ranking.empty:

        return {}

    best_crop = ranking.iloc[0]["Crop_Type"]

    worst_crop = ranking.iloc[-1]["Crop_Type"]

    return {

        "Best Water Efficient Crop":
        best_crop,

        "Lowest Water Efficient Crop":
        worst_crop,

        "Average Water Efficiency":
        round(

            ranking[
                "Water_Efficiency"
            ].mean(),

            4

        )

    }


# =====================================================
# WATER KPI TABLE
# =====================================================

def water_kpi_table(df):

    summary = executive_water_summary(df)

    return pd.DataFrame({

        "Metric":
        summary.keys(),

        "Value":
        summary.values()

    })


# =====================================================
# WATER BENCHMARK
# =====================================================

def water_benchmark(df):

    result = crop_water_efficiency(df)

    avg_efficiency = (
        result[
            "Water_Efficiency"
        ].mean()
    )

    result["Benchmark"] = np.where(

        result[
            "Water_Efficiency"
        ] >= avg_efficiency,

        "Above Average",

        "Below Average"

    )

    return result
    
