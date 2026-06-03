import pandas as pd
import numpy as np

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_summary(df):

    if df.empty:

        return {

            "Total Yield": 0,
            "Total Water": 0,
            "Total Fertilizer": 0,
            "Total Pesticide": 0,

            "Average Yield": 0,
            "Average Water": 0,
            "Average Fertilizer": 0,
            "Average Pesticide": 0,

            "Maximum Yield": 0,
            "Minimum Yield": 0,

            "Crop Types": 0,
            "Seasons": 0,
            "Records": 0
        }

    return {

        "Total Yield":
        float(df["Yield_tons"].sum()),

        "Total Water":
        float(
            df["Water_Usage_cubic_meters"].sum()
        ),

        "Total Fertilizer":
        float(
            df["Fertilizer_Used_tons"].sum()
        ),

        "Total Pesticide":
        float(
            df["Pesticide_Used_kg"].sum()
        ),

        "Average Yield":
        float(
            df["Yield_tons"].mean()
        ),

        "Average Water":
        float(
            df["Water_Usage_cubic_meters"].mean()
        ),

        "Average Fertilizer":
        float(
            df["Fertilizer_Used_tons"].mean()
        ),

        "Average Pesticide":
        float(
            df["Pesticide_Used_kg"].mean()
        ),

        "Maximum Yield":
        float(
            df["Yield_tons"].max()
        ),

        "Minimum Yield":
        float(
            df["Yield_tons"].min()
        ),

        "Crop Types":
        int(
            df["Crop_Type"].nunique()
        ),

        "Seasons":
        int(
            df["Season"].nunique()
        ),

        "Records":
        int(
            len(df)
        )
    }

# =====================================================
# YIELD KPIs
# =====================================================

def yield_kpis(df):

    return {

        "Total Yield":
        float(df["Yield_tons"].sum()),

        "Average Yield":
        float(df["Yield_tons"].mean()),

        "Maximum Yield":
        float(df["Yield_tons"].max()),

        "Minimum Yield":
        float(df["Yield_tons"].min()),

        "Median Yield":
        float(df["Yield_tons"].median())
    }

# =====================================================
# WATER KPIs
# =====================================================

def water_kpis(df):

    total_yield = df["Yield_tons"].sum()

    total_water = (
        df["Water_Usage_cubic_meters"].sum()
    )

    productivity = 0

    if total_water > 0:

        productivity = (
            total_yield /
            total_water
        )

    return {

        "Total Water":
        float(total_water),

        "Average Water":
        float(
            df[
                "Water_Usage_cubic_meters"
            ].mean()
        ),

        "Maximum Water":
        float(
            df[
                "Water_Usage_cubic_meters"
            ].max()
        ),

        "Water Productivity":
        round(
            productivity,
            4
        )
    }

# =====================================================
# FERTILIZER KPIs
# =====================================================

def fertilizer_kpis(df):

    total_yield = df["Yield_tons"].sum()

    total_fert = (
        df["Fertilizer_Used_tons"].sum()
    )

    efficiency = 0

    if total_fert > 0:

        efficiency = (
            total_yield /
            total_fert
        )

    return {

        "Total Fertilizer":
        float(total_fert),

        "Average Fertilizer":
        float(
            df[
                "Fertilizer_Used_tons"
            ].mean()
        ),

        "Maximum Fertilizer":
        float(
            df[
                "Fertilizer_Used_tons"
            ].max()
        ),

        "Fertilizer Efficiency":
        round(
            efficiency,
            4
        )
    }

# =====================================================
# PESTICIDE KPIs
# =====================================================

def pesticide_kpis(df):

    total_yield = df["Yield_tons"].sum()

    total_pest = (
        df["Pesticide_Used_kg"].sum()
    )

    efficiency = 0

    if total_pest > 0:

        efficiency = (
            total_yield /
            total_pest
        )

    return {

        "Total Pesticide":
        float(total_pest),

        "Average Pesticide":
        float(
            df[
                "Pesticide_Used_kg"
            ].mean()
        ),

        "Maximum Pesticide":
        float(
            df[
                "Pesticide_Used_kg"
            ].max()
        ),

        "Pesticide Efficiency":
        round(
            efficiency,
            4
        )
    }

# =====================================================
# SUSTAINABILITY KPIs
# =====================================================

def sustainability_kpis(df):

    total_yield = df["Yield_tons"].sum()

    total_water = (
        df[
            "Water_Usage_cubic_meters"
        ].sum()
    )

    total_fert = (
        df[
            "Fertilizer_Used_tons"
        ].sum()
    )

    total_pest = (
        df[
            "Pesticide_Used_kg"
        ].sum()
    )

    resource_score = 0

    if total_yield > 0:

        resource_score = (
            total_yield /
            (
                total_water +
                total_fert +
                total_pest
            )
        )

    return {

        "Resource Score":
        round(
            resource_score,
            4
        ),

        "Total Yield":
        float(total_yield),

        "Total Resources":
        float(
            total_water +
            total_fert +
            total_pest
        )
    }

# =====================================================
# KPI DATAFRAME
# =====================================================

def kpi_dataframe(df):

    summary = executive_summary(df)

    return pd.DataFrame({

        "Metric":
        summary.keys(),

        "Value":
        summary.values()

    })

# =====================================================
# TOP KPIs
# =====================================================

def dashboard_kpis(df):

    summary = executive_summary(df)

    return [

        summary["Total Yield"],
        summary["Total Water"],
        summary["Total Fertilizer"],
        summary["Total Pesticide"]

    ]
