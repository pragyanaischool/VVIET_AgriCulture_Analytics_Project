import pandas as pd
import numpy as np
import streamlit as st

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    try:

        df = pd.read_csv(
            "agriculture_dataset.csv"
        )

    except Exception as e:

        st.error(
            f"Error loading dataset: {e}"
        )

        return pd.DataFrame()

    # =================================================
    # CLEAN COLUMN NAMES
    # =================================================

    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("/", "_")
    )

    # =================================================
    # DISPLAY COLUMNS FOR DEBUGGING
    # =================================================

    # Uncomment once for debugging

    # st.write(df.columns.tolist())

    # =================================================
    # STANDARDIZE COLUMN NAMES
    # =================================================

    rename_dict = {

        # Crop

        "Crop": "Crop_Type",
        "Crop_Type": "Crop_Type",

        # Soil

        "Soil": "Soil_Type",
        "Soil_Type": "Soil_Type",

        # Season

        "Season": "Season",

        # Irrigation

        "Irrigation": "Irrigation_Type",
        "Irrigation_Type": "Irrigation_Type",

        # Yield

        "Yield": "Yield_tons",
        "Yield_tons": "Yield_tons",
        "Production": "Yield_tons",

        # Water

        "Water": "Water_Usage_cubic_meters",
        "Water_Usage": "Water_Usage_cubic_meters",
        "Water_Usage_cubic_meters":
        "Water_Usage_cubic_meters",

        # Fertilizer

        "Fertilizer": "Fertilizer_Used_tons",
        "Fertilizer_Used":
        "Fertilizer_Used_tons",
        "Fertilizer_Used_tons":
        "Fertilizer_Used_tons",

        # Pesticide

        "Pesticide": "Pesticide_Used_kg",
        "Pesticide_Used":
        "Pesticide_Used_kg",
        "Pesticide_Used_kg":
        "Pesticide_Used_kg",

        # Farm Area

        "Area": "Farm_Area_acres",
        "Farm_Area": "Farm_Area_acres",
        "Farm_Area_acres":
        "Farm_Area_acres"

    }

    df = df.rename(
        columns=rename_dict
    )

    # =================================================
    # CREATE MISSING COLUMNS
    # =================================================

    if "Crop_Type" not in df.columns:

        df["Crop_Type"] = "Unknown"

    if "Season" not in df.columns:

        df["Season"] = "Unknown"

    if "Soil_Type" not in df.columns:

        df["Soil_Type"] = "Unknown"

    if "Irrigation_Type" not in df.columns:

        df["Irrigation_Type"] = "Unknown"

    if "Yield_tons" not in df.columns:

        df["Yield_tons"] = 0

    if "Water_Usage_cubic_meters" not in df.columns:

        df["Water_Usage_cubic_meters"] = 0

    if "Fertilizer_Used_tons" not in df.columns:

        df["Fertilizer_Used_tons"] = 0

    if "Pesticide_Used_kg" not in df.columns:

        df["Pesticide_Used_kg"] = 0

    if "Farm_Area_acres" not in df.columns:

        df["Farm_Area_acres"] = 1

    # =================================================
    # NUMERIC CONVERSION
    # =================================================

    numeric_cols = [

        "Yield_tons",

        "Water_Usage_cubic_meters",

        "Fertilizer_Used_tons",

        "Pesticide_Used_kg",

        "Farm_Area_acres"

    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        df[col] = df[col].fillna(0)

    return df


# =====================================================
# DERIVED METRICS
# =====================================================

def create_derived_metrics(df):

    df = df.copy()

    # ===============================================
    # Yield Per Acre
    # ===============================================

    df["Yield_Per_Acre"] = np.where(

        df["Farm_Area_acres"] > 0,

        df["Yield_tons"]
        /
        df["Farm_Area_acres"],

        0

    )

    # ===============================================
    # Water Productivity
    # ===============================================

    df["Water_Productivity"] = np.where(

        df["Water_Usage_cubic_meters"] > 0,

        df["Yield_tons"]
        /
        df["Water_Usage_cubic_meters"],

        0

    )

    # ===============================================
    # Fertilizer Efficiency
    # ===============================================

    df["Fertilizer_Efficiency"] = np.where(

        df["Fertilizer_Used_tons"] > 0,

        df["Yield_tons"]
        /
        df["Fertilizer_Used_tons"],

        0

    )

    # ===============================================
    # Pesticide Efficiency
    # ===============================================

    df["Pesticide_Efficiency"] = np.where(

        df["Pesticide_Used_kg"] > 0,

        df["Yield_tons"]
        /
        df["Pesticide_Used_kg"],

        0

    )

    # ===============================================
    # Sustainability Score
    # ===============================================

    df["Sustainability_Score"] = (

        df["Water_Productivity"] * 0.40 +

        df["Fertilizer_Efficiency"] * 0.30 +

        df["Pesticide_Efficiency"] * 0.30

    )

    return df


# =====================================================
# DATA PROFILE
# =====================================================

def dataset_profile(df):

    return {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Crop Types":
        df["Crop_Type"].nunique(),

        "Seasons":
        df["Season"].nunique(),

        "Soil Types":
        df["Soil_Type"].nunique(),

        "Irrigation Types":
        df["Irrigation_Type"].nunique()

    }
    
