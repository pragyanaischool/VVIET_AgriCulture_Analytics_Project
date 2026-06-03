import pandas as pd
import numpy as np


# =====================================================
# TREEMAP DATA
# =====================================================

def crop_soil_treemap(df):

    return (

        df.groupby(

            ["Crop_Type", "Soil_Type"]

        )

        .agg(

            Yield=("Yield_tons", "sum")

        )

        .reset_index()

    )


# =====================================================
# TREEMAP - CROP / IRRIGATION
# =====================================================

def crop_irrigation_treemap(df):

    return (

        df.groupby(

            ["Crop_Type", "Irrigation_Type"]

        )

        .agg(

            Yield=("Yield_tons", "sum")

        )

        .reset_index()

    )


# =====================================================
# SUNBURST DATA
# =====================================================

def crop_season_soil_sunburst(df):

    return (

        df.groupby(

            [

                "Crop_Type",
                "Season",
                "Soil_Type"

            ]

        )

        .agg(

            Yield=("Yield_tons", "sum")

        )

        .reset_index()

    )


# =====================================================
# SUNBURST WATER
# =====================================================

def water_sunburst(df):

    return (

        df.groupby(

            [

                "Crop_Type",
                "Season",
                "Irrigation_Type"

            ]

        )

        .agg(

            Water=(

                "Water_Usage_cubic_meters",

                "sum"

            )

        )

        .reset_index()

    )


# =====================================================
# RADAR CHART DATA
# =====================================================

def crop_radar_metrics(df):

    radar = (

        df.groupby("Crop_Type")

        .agg(

            Yield=("Yield_tons", "mean"),

            Water=(

                "Water_Usage_cubic_meters",

                "mean"

            ),

            Fertilizer=(

                "Fertilizer_Used_tons",

                "mean"

            ),

            Pesticide=(

                "Pesticide_Used_kg",

                "mean"

            )

        )

        .reset_index()

    )

    return radar


# =====================================================
# EFFICIENCY RADAR
# =====================================================

def efficiency_radar(df):

    temp = (

        df.groupby("Crop_Type")

        .agg(

            Yield=("Yield_tons", "sum"),

            Water=(

                "Water_Usage_cubic_meters",

                "sum"

            ),

            Fertilizer=(

                "Fertilizer_Used_tons",

                "sum"

            ),

            Pesticide=(

                "Pesticide_Used_kg",

                "sum"

            )

        )

        .reset_index()

    )

    temp["Water_Productivity"] = (

        temp["Yield"]

        /

        temp["Water"]

    )

    temp["Fertilizer_Efficiency"] = (

        temp["Yield"]

        /

        temp["Fertilizer"]

    )

    temp["Pesticide_Efficiency"] = (

        temp["Yield"]

        /

        temp["Pesticide"]

    )

    return temp


# =====================================================
# BUBBLE CHART DATA
# =====================================================

def bubble_chart_data(df):

    return df[

        [

            "Crop_Type",

            "Yield_tons",

            "Water_Usage_cubic_meters",

            "Farm_Area_acres"

        ]

    ]


# =====================================================
# RESOURCE BUBBLE
# =====================================================

def resource_bubble_data(df):

    return df[

        [

            "Yield_tons",

            "Water_Usage_cubic_meters",

            "Fertilizer_Used_tons",

            "Pesticide_Used_kg",

            "Crop_Type"

        ]

    ]


# =====================================================
# PARETO DATA
# =====================================================

def pareto_yield(df):

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

    pareto["Cumulative"] = (

        pareto["Yield_tons"]

        .cumsum()

    )

    pareto["Cumulative_%"] = (

        pareto["Cumulative"]

        /

        pareto["Yield_tons"].sum()

    ) * 100

    return pareto


# =====================================================
# PARETO WATER
# =====================================================

def pareto_water(df):

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

    pareto["Cumulative"] = (

        pareto["Water_Usage_cubic_meters"]

        .cumsum()

    )

    pareto["Cumulative_%"] = (

        pareto["Cumulative"]

        /

        pareto["Water_Usage_cubic_meters"].sum()

    ) * 100

    return pareto


# =====================================================
# CORRELATION HEATMAP DATA
# =====================================================

def correlation_heatmap(df):

    numeric_df = df.select_dtypes(

        include=np.number

    )

    return numeric_df.corr()


# =====================================================
# CROP SOIL HEATMAP
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
# CROP IRRIGATION HEATMAP
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
# WATER HEATMAP
# =====================================================

def water_heatmap(df):

    return pd.pivot_table(

        df,

        values="Water_Usage_cubic_meters",

        index="Crop_Type",

        columns="Season",

        aggfunc="mean"

    )


# =====================================================
# FERTILIZER HEATMAP
# =====================================================

def fertilizer_heatmap(df):

    return pd.pivot_table(

        df,

        values="Fertilizer_Used_tons",

        index="Crop_Type",

        columns="Season",

        aggfunc="mean"

    )


# =====================================================
# PESTICIDE HEATMAP
# =====================================================

def pesticide_heatmap(df):

    return pd.pivot_table(

        df,

        values="Pesticide_Used_kg",

        index="Crop_Type",

        columns="Season",

        aggfunc="mean"

    )


# =====================================================
# KPI COMPARISON
# =====================================================

def crop_kpi_comparison(df):

    summary = (

        df.groupby("Crop_Type")

        .agg(

            Yield=("Yield_tons", "mean"),

            Water=(

                "Water_Usage_cubic_meters",

                "mean"

            ),

            Fertilizer=(

                "Fertilizer_Used_tons",

                "mean"

            ),

            Pesticide=(

                "Pesticide_Used_kg",

                "mean"

            ),

            Area=(

                "Farm_Area_acres",

                "mean"

            )

        )

        .reset_index()

    )

    return summary


# =====================================================
# WATERFALL DATA
# =====================================================

def waterfall_contributors(df):

    return pd.DataFrame({

        "Factor": [

            "Farm Area",

            "Water Usage",

            "Fertilizer",

            "Pesticide"

        ],

        "Value": [

            df["Farm_Area_acres"].sum(),

            df["Water_Usage_cubic_meters"].sum(),

            df["Fertilizer_Used_tons"].sum(),

            df["Pesticide_Used_kg"].sum()

        ]

    })


# =====================================================
# SCATTER MATRIX DATA
# =====================================================

def scatter_matrix_data(df):

    return df.select_dtypes(

        include=np.number

    )


# =====================================================
# RESOURCE UTILIZATION
# =====================================================

def resource_utilization(df):

    total_water = (

        df["Water_Usage_cubic_meters"]

        .sum()

    )

    total_fertilizer = (

        df["Fertilizer_Used_tons"]

        .sum()

    )

    total_pesticide = (

        df["Pesticide_Used_kg"]

        .sum()

    )

    return pd.DataFrame({

        "Resource": [

            "Water",

            "Fertilizer",

            "Pesticide"

        ],

        "Usage": [

            total_water,

            total_fertilizer,

            total_pesticide

        ]

    })


# =====================================================
# SANKEY DATA
# =====================================================

def sankey_source_target(df):

    sankey_df = (

        df.groupby(

            [

                "Season",

                "Crop_Type"

            ]

        )

        .agg(

            Yield=("Yield_tons", "sum")

        )

        .reset_index()

    )

    return sankey_df


# =====================================================
# EXECUTIVE VISUAL SUMMARY
# =====================================================

def executive_visual_summary(df):

    return {

        "Treemap":
        crop_soil_treemap(df),

        "Sunburst":
        crop_season_soil_sunburst(df),

        "Radar":
        crop_radar_metrics(df),

        "Bubble":
        bubble_chart_data(df),

        "Pareto":
        pareto_yield(df),

        "Heatmap":
        correlation_heatmap(df),

        "Resource":
        resource_utilization(df)

    }
  
