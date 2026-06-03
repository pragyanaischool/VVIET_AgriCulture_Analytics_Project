import pandas as pd
import numpy as np


# =====================================================
# RESOURCE INTENSITY SCORE
# =====================================================

def resource_intensity_score(df):

    required_cols = [
        "Water_Usage_cubic_meters",
        "Fertilizer_Used_tons",
        "Pesticide_Used_kg",
        "Yield_tons"
    ]

    if not all(
        col in df.columns
        for col in required_cols
    ):
        return 0

    total_resources = (

        df["Water_Usage_cubic_meters"].sum()

        +

        df["Fertilizer_Used_tons"].sum()

        +

        df["Pesticide_Used_kg"].sum()

    )

    total_yield = df["Yield_tons"].sum()

    if total_yield == 0:
        return 0

    return round(
        total_resources / total_yield,
        4
    )


# =====================================================
# SUSTAINABILITY SCORE
# =====================================================

def sustainability_score(df):

    intensity = resource_intensity_score(df)

    if intensity == 0:
        return 0

    return round(
        1 / intensity,
        6
    )


# =====================================================
# WATER SUSTAINABILITY
# =====================================================

def water_sustainability_score(df):

    if (
        "Water_Usage_cubic_meters" not in df.columns
        or
        "Yield_tons" not in df.columns
    ):
        return 0

    water_per_yield = (

        df["Water_Usage_cubic_meters"].sum()

        /

        df["Yield_tons"].sum()

    )

    return round(
        1 / water_per_yield,
        6
    )


# =====================================================
# FERTILIZER SUSTAINABILITY
# =====================================================

def fertilizer_sustainability_score(df):

    if (
        "Fertilizer_Used_tons" not in df.columns
        or
        "Yield_tons" not in df.columns
    ):
        return 0

    fert_per_yield = (

        df["Fertilizer_Used_tons"].sum()

        /

        df["Yield_tons"].sum()

    )

    return round(
        1 / fert_per_yield,
        6
    )


# =====================================================
# PESTICIDE SUSTAINABILITY
# =====================================================

def pesticide_sustainability_score(df):

    if (
        "Pesticide_Used_kg" not in df.columns
        or
        "Yield_tons" not in df.columns
    ):
        return 0

    pest_per_yield = (

        df["Pesticide_Used_kg"].sum()

        /

        df["Yield_tons"].sum()

    )

    return round(
        1 / pest_per_yield,
        6
    )


# =====================================================
# CARBON FOOTPRINT ESTIMATION
# =====================================================

def carbon_footprint(df):

    if not all(col in df.columns for col in [
        "Fertilizer_Used_tons",
        "Pesticide_Used_kg",
        "Water_Usage_cubic_meters"
    ]):
        return 0

    carbon = (

        df["Fertilizer_Used_tons"].sum() * 0.70

        +

        df["Pesticide_Used_kg"].sum() * 0.20

        +

        df["Water_Usage_cubic_meters"].sum() * 0.10

    )

    return round(carbon, 2)


# =====================================================
# CARBON PER TON OF YIELD
# =====================================================

def carbon_per_yield(df):

    if "Yield_tons" not in df.columns:
        return 0

    total_yield = df["Yield_tons"].sum()

    if total_yield == 0:
        return 0

    return round(
        carbon_footprint(df)
        /
        total_yield,
        4
    )


# =====================================================
# CREATE SUSTAINABILITY METRICS
# =====================================================

def create_sustainability_metrics(df):

    data = df.copy()

    if all(
        col in data.columns
        for col in [
            "Yield_tons",
            "Water_Usage_cubic_meters",
            "Fertilizer_Used_tons",
            "Pesticide_Used_kg"
        ]
    ):

        data["Resource_Intensity"] = (

            data["Water_Usage_cubic_meters"]

            +

            data["Fertilizer_Used_tons"]

            +

            data["Pesticide_Used_kg"]

        ) / data["Yield_tons"]

        data["Sustainability_Score"] = (

            1 /

            data["Resource_Intensity"]

        )

    return data


# =====================================================
# CROP SUSTAINABILITY
# =====================================================

def crop_sustainability_summary(df):

    summary = (

        df.groupby("Crop_Type")

        .agg(

            Total_Yield=("Yield_tons", "sum"),

            Water=("Water_Usage_cubic_meters", "sum"),

            Fertilizer=("Fertilizer_Used_tons", "sum"),

            Pesticide=("Pesticide_Used_kg", "sum")

        )

        .reset_index()

    )

    summary["Resource_Intensity"] = (

        summary["Water"]

        +

        summary["Fertilizer"]

        +

        summary["Pesticide"]

    ) / summary["Total_Yield"]

    summary["Sustainability_Score"] = (

        1 /

        summary["Resource_Intensity"]

    )

    return summary.sort_values(
        by="Sustainability_Score",
        ascending=False
    )


# =====================================================
# SOIL SUSTAINABILITY
# =====================================================

def soil_sustainability_summary(df):

    summary = (

        df.groupby("Soil_Type")

        .agg(

            Yield=("Yield_tons", "sum"),

            Water=("Water_Usage_cubic_meters", "sum"),

            Fertilizer=("Fertilizer_Used_tons", "sum"),

            Pesticide=("Pesticide_Used_kg", "sum")

        )

        .reset_index()

    )

    summary["Sustainability_Score"] = (

        summary["Yield"]

        /

        (

            summary["Water"]

            +

            summary["Fertilizer"]

            +

            summary["Pesticide"]

        )

    )

    return summary.sort_values(
        by="Sustainability_Score",
        ascending=False
    )


# =====================================================
# SEASON SUSTAINABILITY
# =====================================================

def season_sustainability_summary(df):

    summary = (

        df.groupby("Season")

        .agg(

            Yield=("Yield_tons", "sum"),

            Water=("Water_Usage_cubic_meters", "sum"),

            Fertilizer=("Fertilizer_Used_tons", "sum"),

            Pesticide=("Pesticide_Used_kg", "sum")

        )

        .reset_index()

    )

    summary["Sustainability_Score"] = (

        summary["Yield"]

        /

        (

            summary["Water"]

            +

            summary["Fertilizer"]

            +

            summary["Pesticide"]

        )

    )

    return summary.sort_values(
        by="Sustainability_Score",
        ascending=False
    )


# =====================================================
# IRRIGATION SUSTAINABILITY
# =====================================================

def irrigation_sustainability_summary(df):

    summary = (

        df.groupby("Irrigation_Type")

        .agg(

            Yield=("Yield_tons", "sum"),

            Water=("Water_Usage_cubic_meters", "sum"),

            Fertilizer=("Fertilizer_Used_tons", "sum"),

            Pesticide=("Pesticide_Used_kg", "sum")

        )

        .reset_index()

    )

    summary["Sustainability_Score"] = (

        summary["Yield"]

        /

        (

            summary["Water"]

            +

            summary["Fertilizer"]

            +

            summary["Pesticide"]

        )

    )

    return summary.sort_values(
        by="Sustainability_Score",
        ascending=False
    )


# =====================================================
# SUSTAINABILITY RANKING
# =====================================================

def sustainability_ranking(df):

    ranking = crop_sustainability_summary(df)

    ranking["Rank"] = range(
        1,
        len(ranking) + 1
    )

    return ranking


# =====================================================
# PARETO ANALYSIS
# =====================================================

def sustainability_pareto_analysis(df):

    pareto = crop_sustainability_summary(df)

    pareto = pareto.sort_values(
        by="Sustainability_Score",
        ascending=False
    )

    pareto["Cumulative"] = (
        pareto["Sustainability_Score"]
        .cumsum()
    )

    pareto["Cumulative_%"] = (

        pareto["Cumulative"]

        /

        pareto["Sustainability_Score"].sum()

    ) * 100

    return pareto


# =====================================================
# HEATMAP DATA
# =====================================================

def crop_soil_sustainability_heatmap(df):

    sustainability_df = create_sustainability_metrics(df)

    return pd.pivot_table(
        sustainability_df,
        values="Sustainability_Score",
        index="Crop_Type",
        columns="Soil_Type",
        aggfunc="mean"
    )


def crop_irrigation_sustainability_heatmap(df):

    sustainability_df = create_sustainability_metrics(df)

    return pd.pivot_table(
        sustainability_df,
        values="Sustainability_Score",
        index="Crop_Type",
        columns="Irrigation_Type",
        aggfunc="mean"
    )


def season_crop_sustainability_heatmap(df):

    sustainability_df = create_sustainability_metrics(df)

    return pd.pivot_table(
        sustainability_df,
        values="Sustainability_Score",
        index="Season",
        columns="Crop_Type",
        aggfunc="mean"
    )


# =====================================================
# ESG SCORE
# =====================================================

def esg_agriculture_score(df):

    sustainability = sustainability_score(df)

    water_score = water_sustainability_score(df)

    fertilizer_score = fertilizer_sustainability_score(df)

    pesticide_score = pesticide_sustainability_score(df)

    esg_score = (

        sustainability * 0.40

        +

        water_score * 0.25

        +

        fertilizer_score * 0.20

        +

        pesticide_score * 0.15

    )

    return round(esg_score, 4)


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_sustainability_summary(df):

    return {

        "Resource Intensity":
        resource_intensity_score(df),

        "Sustainability Score":
        sustainability_score(df),

        "Water Sustainability":
        water_sustainability_score(df),

        "Fertilizer Sustainability":
        fertilizer_sustainability_score(df),

        "Pesticide Sustainability":
        pesticide_sustainability_score(df),

        "Carbon Footprint":
        carbon_footprint(df),

        "Carbon Per Yield":
        carbon_per_yield(df),

        "ESG Score":
        esg_agriculture_score(df)

    }
  
