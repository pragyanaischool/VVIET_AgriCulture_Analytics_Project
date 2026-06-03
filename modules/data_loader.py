import streamlit as st
import pandas as pd
import numpy as np


# ---------------------------------------------------
# LOAD DATASET
# ---------------------------------------------------

@st.cache_data
def load_data(file_path="agriculture_dataset.csv"):
    """
    Load Agriculture Dataset
    """

    try:
        df = pd.read_csv(file_path)

        # Remove duplicate rows
        df = df.drop_duplicates()

        return df

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return pd.DataFrame()


# ---------------------------------------------------
# LOAD EXCEL FILE
# ---------------------------------------------------

@st.cache_data
def load_excel(file_path):
    """
    Load Excel File
    """

    try:
        df = pd.read_excel(file_path)
        return df

    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame()


# ---------------------------------------------------
# DATASET SHAPE
# ---------------------------------------------------

def get_dataset_shape(df):

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1]
    }


# ---------------------------------------------------
# COLUMN TYPES
# ---------------------------------------------------

def get_column_types(df):

    numeric_cols = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    return numeric_cols, categorical_cols


# ---------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------

def missing_values_summary(df):

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (
            df.isnull().sum() / len(df) * 100
        ).round(2).values
    })

    return missing_df.sort_values(
        by="Missing %",
        ascending=False
    )


# ---------------------------------------------------
# DATA TYPES SUMMARY
# ---------------------------------------------------

def datatype_summary(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str)
    })


# ---------------------------------------------------
# DESCRIPTIVE STATISTICS
# ---------------------------------------------------

def get_numeric_summary(df):

    numeric_cols = df.select_dtypes(
        include=np.number
    )

    return numeric_cols.describe().T


# ---------------------------------------------------
# UNIQUE VALUES
# ---------------------------------------------------

def unique_values_summary(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Unique Values": [
            df[col].nunique()
            for col in df.columns
        ]
    })


# ---------------------------------------------------
# FEATURE ENGINEERING
# ---------------------------------------------------

def create_derived_metrics(df):

    data = df.copy()

    # Yield Per Acre

    if (
        "Yield_tons" in data.columns
        and "Farm_Area_acres" in data.columns
    ):

        data["Yield_Per_Acre"] = (
            data["Yield_tons"]
            / data["Farm_Area_acres"]
        )

    # Water Productivity

    if (
        "Yield_tons" in data.columns
        and "Water_Usage_cubic_meters" in data.columns
    ):

        data["Water_Productivity"] = (
            data["Yield_tons"]
            / data["Water_Usage_cubic_meters"]
        )

    # Fertilizer Efficiency

    if (
        "Yield_tons" in data.columns
        and "Fertilizer_Used_tons" in data.columns
    ):

        data["Fertilizer_Efficiency"] = (
            data["Yield_tons"]
            / data["Fertilizer_Used_tons"]
        )

    # Pesticide Efficiency

    if (
        "Yield_tons" in data.columns
        and "Pesticide_Used_kg" in data.columns
    ):

        data["Pesticide_Efficiency"] = (
            data["Yield_tons"]
            / data["Pesticide_Used_kg"]
        )

    # Water Footprint

    if (
        "Water_Usage_cubic_meters" in data.columns
        and "Yield_tons" in data.columns
    ):

        data["Water_Footprint_Per_Ton"] = (
            data["Water_Usage_cubic_meters"]
            / data["Yield_tons"]
        )

    return data


# ---------------------------------------------------
# DATA QUALITY SCORE
# ---------------------------------------------------

def data_quality_score(df):

    total_cells = df.shape[0] * df.shape[1]

    missing_cells = df.isnull().sum().sum()

    completeness = (
        (total_cells - missing_cells)
        / total_cells
    ) * 100

    return round(completeness, 2)


# ---------------------------------------------------
# PROFILE SUMMARY
# ---------------------------------------------------

def dataset_profile(df):

    profile = {

        "Rows":
        df.shape[0],

        "Columns":
        df.shape[1],

        "Numeric Columns":
        len(
            df.select_dtypes(
                include=["number"]
            ).columns
        ),

        "Categorical Columns":
        len(
            df.select_dtypes(
                include=["object", "category"]
            ).columns
        ),

        "Missing Values":
        int(
            df.isnull().sum().sum()
        ),

        "Duplicate Rows":
        int(
            df.duplicated().sum()
        ),

        "Data Quality Score":
        data_quality_score(df)

    }

    return profile


# ---------------------------------------------------
# TOP RECORDS
# ---------------------------------------------------

def preview_data(df, rows=10):

    return df.head(rows)


# ---------------------------------------------------
# BOTTOM RECORDS
# ---------------------------------------------------

def tail_data(df, rows=10):

    return df.tail(rows)


# ---------------------------------------------------
# RANDOM SAMPLE
# ---------------------------------------------------

def sample_data(df, rows=10):

    return df.sample(
        min(rows, len(df)),
        random_state=42
    )


# ---------------------------------------------------
# CORRELATION DATA
# ---------------------------------------------------

def correlation_dataset(df):

    numeric_df = df.select_dtypes(
        include=np.number
    )

    return numeric_df.corr()


# ---------------------------------------------------
# EXPORT CLEAN DATA
# ---------------------------------------------------

def export_clean_data(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")
