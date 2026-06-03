import pandas as pd
import numpy as np


# =====================================================
# BASIC KPIs
# =====================================================

def total_farms(df):
    return len(df)


def total_area(df):
    if "Farm_Area_acres" in df.columns:
        return round(df["Farm_Area_acres"].sum(), 2)
    return 0


def total_yield(df):
    if "Yield_tons" in df.columns:
        return round(df["Yield_tons"].sum(), 2)
    return 0


def total_water_usage(df):
    if "Water_Usage_cubic_meters" in df.columns:
        return round(df["Water_Usage_cubic_meters"].sum(), 2)
    return 0


def total_fertilizer(df):
    if "Fertilizer_Used_tons" in df.columns:
        return round(df["Fertilizer_Used_tons"].sum(), 2)
    return 0


def total_pesticide(df):
    if "Pesticide_Used_kg" in df.columns:
        return round(df["Pesticide_Used_kg"].sum(), 2)
    return 0


# =====================================================
# AVERAGE KPIs
# =====================================================

def average_yield(df):
    if "Yield_tons" in df.columns:
        return round(df["Yield_tons"].mean(), 2)
    return 0


def average_area(df):
    if "Farm_Area_acres" in df.columns:
        return round(df["Farm_Area_acres"].mean(), 2)
    return 0


def average_water_usage(df):
    if "Water_Usage_cubic_meters" in df.columns:
        return round(df["Water_Usage_cubic_meters"].mean(), 2)
    return 0


def average_fertilizer(df):
    if "Fertilizer_Used_tons" in df.columns:
        return round(df["Fertilizer_Used_tons"].mean(), 2)
    return 0


def average_pesticide(df):
    if "Pesticide_Used_kg" in df.columns:
        return round(df["Pesticide_Used_kg"].mean(), 2)
    return 0


# =====================================================
# EFFICIENCY METRICS
# =====================================================

def yield_per_acre(df):

    if (
        "Yield_tons" in df.columns
        and "Farm_Area_acres" in df.columns
    ):
        return round(
            (
                df["Yield_tons"].sum()
                /
                df["Farm_Area_acres"].sum()
            ),
            4
        )

    return 0


def water_productivity(df):

    if (
        "Yield_tons" in df.columns
        and "Water_Usage_cubic_meters" in df.columns
    ):
        return round(
            (
                df["Yield_tons"].sum()
                /
                df["Water_Usage_cubic_meters"].sum()
            ),
            6
        )

    return 0


def fertilizer_efficiency(df):

    if (
        "Yield_tons" in df.columns
        and "Fertilizer_Used_tons" in df.columns
    ):
        return round(
            (
                df["Yield_tons"].sum()
                /
                df["Fertilizer_Used_tons"].sum()
            ),
            4
        )

    return 0


def pesticide_efficiency(df):

    if (
        "Yield_tons" in df.columns
        and "Pesticide_Used_kg" in df.columns
    ):
        return round(
            (
                df["Yield_tons"].sum()
                /
                df["Pesticide_Used_kg"].sum()
            ),
            4
        )

    return 0


# =====================================================
# WATER FOOTPRINT
# =====================================================

def water_footprint(df):

    if (
        "Water_Usage_cubic_meters" in df.columns
        and "Yield_tons" in df.columns
    ):
        return round(
            (
                df["Water_Usage_cubic_meters"].sum()
                /
                df["Yield_tons"].sum()
            ),
            4
        )

    return 0


# =====================================================
# RESOURCE INTENSITY SCORE
# =====================================================

def resource_intensity_score(df):

    try:

        total_resources = (

            df["Water_Usage_cubic_meters"].sum()

            +

            df["Fertilizer_Used_tons"].sum()

            +

            df["Pesticide_Used_kg"].sum()

        )

        score = (
            total_resources
            /
            df["Yield_tons"].sum()
        )

        return round(score, 4)

    except:
        return 0


# =====================================================
# SUSTAINABILITY SCORE
# =====================================================

def sustainability_score(df):

    try:

        intensity = resource_intensity_score(df)

        return round(
            1 / intensity,
            6
        )

    except:
        return 0


# =====================================================
# TOP PERFORMERS
# =====================================================

def best_crop(df):

    if (
        "Crop_Type" in df.columns
        and "Yield_tons" in df.columns
    ):

        crop = (
            df.groupby("Crop_Type")
            ["Yield_tons"]
            .mean()
            .idxmax()
        )

        return crop

    return "N/A"


def best_soil(df):

    if (
        "Soil_Type" in df.columns
        and "Yield_tons" in df.columns
    ):

        soil = (
            df.groupby("Soil_Type")
            ["Yield_tons"]
            .mean()
            .idxmax()
        )

        return soil

    return "N/A"


def best_irrigation(df):

    if (
        "Irrigation_Type" in df.columns
        and "Yield_tons" in df.columns
    ):

        irrigation = (
            df.groupby("Irrigation_Type")
            ["Yield_tons"]
            .mean()
            .idxmax()
        )

        return irrigation

    return "N/A"


def best_season(df):

    if (
        "Season" in df.columns
        and "Yield_tons" in df.columns
    ):

        season = (
            df.groupby("Season")
            ["Yield_tons"]
            .mean()
            .idxmax()
        )

        return season

    return "N/A"


# =====================================================
# DATA QUALITY KPI
# =====================================================

def data_quality_score(df):

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    score = (
        (total_cells - missing_cells)
        /
        total_cells
    ) * 100

    return round(score, 2)


# =====================================================
# EXECUTIVE KPI SUMMARY
# =====================================================

def executive_summary(df):

    summary = {

        "Total Farms":
        total_farms(df),

        "Total Area":
        total_area(df),

        "Total Yield":
        total_yield(df),

        "Total Water Usage":
        total_water_usage(df),

        "Yield Per Acre":
        yield_per_acre(df),

        "Water Productivity":
        water_productivity(df),

        "Fertilizer Efficiency":
        fertilizer_efficiency(df),

        "Pesticide Efficiency":
        pesticide_efficiency(df),

        "Sustainability Score":
        sustainability_score(df),

        "Best Crop":
        best_crop(df),

        "Best Soil":
        best_soil(df),

        "Best Irrigation":
        best_irrigation(df),

        "Best Season":
        best_season(df),

        "Data Quality":
        data_quality_score(df)

    }

    return summary
