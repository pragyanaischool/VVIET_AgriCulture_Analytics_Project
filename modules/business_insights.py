import pandas as pd
import numpy as np


# =====================================================
# TOP PERFORMING CROP
# =====================================================

def top_performing_crop(df):

    crop = (

        df.groupby("Crop_Type")

        ["Yield_tons"]

        .mean()

        .idxmax()

    )

    value = (

        df.groupby("Crop_Type")

        ["Yield_tons"]

        .mean()

        .max()

    )

    return crop, round(value, 2)


# =====================================================
# LOWEST PERFORMING CROP
# =====================================================

def lowest_performing_crop(df):

    crop = (

        df.groupby("Crop_Type")

        ["Yield_tons"]

        .mean()

        .idxmin()

    )

    value = (

        df.groupby("Crop_Type")

        ["Yield_tons"]

        .mean()

        .min()

    )

    return crop, round(value, 2)


# =====================================================
# BEST SOIL
# =====================================================

def best_soil(df):

    soil = (

        df.groupby("Soil_Type")

        ["Yield_tons"]

        .mean()

        .idxmax()

    )

    value = (

        df.groupby("Soil_Type")

        ["Yield_tons"]

        .mean()

        .max()

    )

    return soil, round(value, 2)


# =====================================================
# BEST IRRIGATION
# =====================================================

def best_irrigation(df):

    irrigation = (

        df.groupby("Irrigation_Type")

        ["Yield_tons"]

        .mean()

        .idxmax()

    )

    value = (

        df.groupby("Irrigation_Type")

        ["Yield_tons"]

        .mean()

        .max()

    )

    return irrigation, round(value, 2)


# =====================================================
# BEST SEASON
# =====================================================

def best_season(df):

    season = (

        df.groupby("Season")

        ["Yield_tons"]

        .mean()

        .idxmax()

    )

    value = (

        df.groupby("Season")

        ["Yield_tons"]

        .mean()

        .max()

    )

    return season, round(value, 2)


# =====================================================
# WATER PRODUCTIVITY INSIGHT
# =====================================================

def water_productivity_insight(df):

    productivity = (

        df["Yield_tons"].sum()

        /

        df["Water_Usage_cubic_meters"].sum()

    )

    if productivity > 0.002:

        return (
            "Excellent water productivity observed. "
            "Water resources are being utilized efficiently."
        )

    elif productivity > 0.001:

        return (
            "Moderate water productivity observed. "
            "Further irrigation optimization may improve results."
        )

    else:

        return (
            "Low water productivity detected. "
            "Consider adopting efficient irrigation methods."
        )


# =====================================================
# FERTILIZER INSIGHT
# =====================================================

def fertilizer_efficiency_insight(df):

    efficiency = (

        df["Yield_tons"].sum()

        /

        df["Fertilizer_Used_tons"].sum()

    )

    if efficiency > 5:

        return (
            "High fertilizer efficiency achieved."
        )

    elif efficiency > 3:

        return (
            "Moderate fertilizer efficiency."
        )

    else:

        return (
            "Low fertilizer efficiency detected."
        )


# =====================================================
# PESTICIDE INSIGHT
# =====================================================

def pesticide_efficiency_insight(df):

    efficiency = (

        df["Yield_tons"].sum()

        /

        df["Pesticide_Used_kg"].sum()

    )

    if efficiency > 0.20:

        return (
            "Pesticide utilization appears efficient."
        )

    elif efficiency > 0.10:

        return (
            "Moderate pesticide utilization."
        )

    else:

        return (
            "High pesticide dependency observed."
        )


# =====================================================
# SUSTAINABILITY INSIGHT
# =====================================================

def sustainability_insight(df):

    resources = (

        df["Water_Usage_cubic_meters"].sum()

        +

        df["Fertilizer_Used_tons"].sum()

        +

        df["Pesticide_Used_kg"].sum()

    )

    score = (

        df["Yield_tons"].sum()

        /

        resources

    )

    if score > 0.005:

        return (
            "Agricultural operations demonstrate "
            "strong sustainability performance."
        )

    elif score > 0.002:

        return (
            "Moderate sustainability performance."
        )

    else:

        return (
            "Resource consumption is relatively high."
        )


# =====================================================
# RESOURCE ALERTS
# =====================================================

def resource_alerts(df):

    alerts = []

    if (

        df["Water_Usage_cubic_meters"].mean()

        >

        df["Water_Usage_cubic_meters"].median()

        * 1.5

    ):

        alerts.append(
            "High water consumption detected."
        )

    if (

        df["Fertilizer_Used_tons"].mean()

        >

        df["Fertilizer_Used_tons"].median()

        * 1.5

    ):

        alerts.append(
            "High fertilizer dependency detected."
        )

    if (

        df["Pesticide_Used_kg"].mean()

        >

        df["Pesticide_Used_kg"].median()

        * 1.5

    ):

        alerts.append(
            "High pesticide usage detected."
        )

    return alerts


# =====================================================
# BUSINESS RECOMMENDATIONS
# =====================================================

def business_recommendations(df):

    recommendations = []

    irrigation = best_irrigation(df)[0]

    recommendations.append(

        f"Promote {irrigation} irrigation practices "
        "across farms."

    )

    crop = top_performing_crop(df)[0]

    recommendations.append(

        f"Expand cultivation of {crop} "
        "to maximize yield potential."

    )

    soil = best_soil(df)[0]

    recommendations.append(

        f"Prioritize farming practices "
        f"suited for {soil} soil."

    )

    recommendations.append(

        "Monitor water productivity regularly."
    )

    recommendations.append(

        "Optimize fertilizer allocation "
        "to improve resource efficiency."
    )

    return recommendations


# =====================================================
# YIELD INSIGHTS
# =====================================================

def yield_insights(df):

    top_crop, value = top_performing_crop(df)

    return (

        f"The highest yielding crop is "
        f"{top_crop} with an average yield "
        f"of {value} tons."

    )


# =====================================================
# WATER INSIGHTS
# =====================================================

def water_insights(df):

    irrigation, value = best_irrigation(df)

    return (

        f"{irrigation} irrigation delivers "
        f"the highest average yield of "
        f"{value} tons."

    )


# =====================================================
# SEASONAL INSIGHTS
# =====================================================

def seasonal_insights(df):

    season, value = best_season(df)

    return (

        f"{season} season demonstrates the "
        f"highest average productivity "
        f"with {value} tons of yield."

    )


# =====================================================
# SOIL INSIGHTS
# =====================================================

def soil_insights(df):

    soil, value = best_soil(df)

    return (

        f"{soil} soil provides the highest "
        f"average crop productivity "
        f"at {value} tons."

    )


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_summary(df):

    total_yield = round(
        df["Yield_tons"].sum(),
        2
    )

    total_water = round(
        df["Water_Usage_cubic_meters"].sum(),
        2
    )

    total_fertilizer = round(
        df["Fertilizer_Used_tons"].sum(),
        2
    )

    total_pesticide = round(
        df["Pesticide_Used_kg"].sum(),
        2
    )

    crop, _ = top_performing_crop(df)

    soil, _ = best_soil(df)

    season, _ = best_season(df)

    summary = f"""
Agricultural operations generated a total yield of
{total_yield:,.2f} tons.

Total water consumption reached
{total_water:,.2f} cubic meters.

Fertilizer utilization amounted to
{total_fertilizer:,.2f} tons.

Pesticide consumption totaled
{total_pesticide:,.2f} kg.

The highest-performing crop was {crop},
while {soil} soil demonstrated the best
yield performance.

The most productive season was {season}.
"""

    return summary


# =====================================================
# COMPLETE BUSINESS REPORT
# =====================================================

def complete_business_report(df):

    return {

        "Executive Summary":
        executive_summary(df),

        "Yield Insight":
        yield_insights(df),

        "Water Insight":
        water_insights(df),

        "Soil Insight":
        soil_insights(df),

        "Season Insight":
        seasonal_insights(df),

        "Water Productivity":
        water_productivity_insight(df),

        "Fertilizer Efficiency":
        fertilizer_efficiency_insight(df),

        "Pesticide Efficiency":
        pesticide_efficiency_insight(df),

        "Sustainability":
        sustainability_insight(df),

        "Alerts":
        resource_alerts(df),

        "Recommendations":
        business_recommendations(df)

    }
