import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data
)

from modules.statistical_analysis import (

    descriptive_statistics,

    mean_values,

    median_values,

    mode_values,

    variance_values,

    std_deviation,

    range_values,

    iqr_values,

    skewness_analysis,

    kurtosis_analysis,

    percentile_summary,

    confidence_interval_table,

    shapiro_wilk_test,

    outlier_summary,

    correlation_matrix,

    data_quality_report

)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Statistical Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# TITLE
# =====================================================

st.title("📊 Statistical Analytics")

st.markdown(
    """
    Comprehensive statistical analysis of
    agricultural operations, productivity,
    resources, and sustainability indicators.
    """
)

# =====================================================
# COLUMN SELECTION
# =====================================================

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

selected_column = st.sidebar.selectbox(
    "Select Numeric Feature",
    numeric_columns
)

# =====================================================
# DATASET OVERVIEW
# =====================================================

st.subheader("📋 Dataset Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Rows",
        df.shape[0]
    )

with c2:
    st.metric(
        "Columns",
        df.shape[1]
    )

with c3:
    st.metric(
        "Numeric Features",
        len(numeric_columns)
    )

# =====================================================
# DESCRIPTIVE STATISTICS
# =====================================================

st.subheader("📈 Descriptive Statistics")

st.dataframe(
    descriptive_statistics(df),
    use_container_width=True
)

# =====================================================
# CENTRAL TENDENCY
# =====================================================

st.subheader("🎯 Central Tendency")

mean_df = pd.DataFrame({
    "Mean": mean_values(df)
})

median_df = pd.DataFrame({
    "Median": median_values(df)
})

mode_df = pd.DataFrame({
    "Mode": mode_values(df)
})

central_df = pd.concat(
    [
        mean_df,
        median_df,
        mode_df
    ],
    axis=1
)

st.dataframe(
    central_df,
    use_container_width=True
)

# =====================================================
# DISPERSION
# =====================================================

st.subheader("📉 Dispersion Statistics")

dispersion_df = pd.DataFrame({

    "Variance":
    variance_values(df),

    "Std Deviation":
    std_deviation(df),

    "Range":
    range_values(df),

    "IQR":
    iqr_values(df)

})

st.dataframe(
    dispersion_df,
    use_container_width=True
)

# =====================================================
# SKEWNESS
# =====================================================

st.subheader("🔄 Skewness Analysis")

st.dataframe(
    skewness_analysis(df),
    use_container_width=True
)

# =====================================================
# KURTOSIS
# =====================================================

st.subheader("📐 Kurtosis Analysis")

st.dataframe(
    kurtosis_analysis(df),
    use_container_width=True
)

# =====================================================
# PERCENTILES
# =====================================================

st.subheader("📊 Percentile Summary")

st.dataframe(
    percentile_summary(df),
    use_container_width=True
)

# =====================================================
# CONFIDENCE INTERVALS
# =====================================================

st.subheader("🎯 Confidence Intervals")

st.dataframe(
    confidence_interval_table(df),
    use_container_width=True
)

# =====================================================
# NORMALITY TEST
# =====================================================

st.subheader("🧪 Shapiro-Wilk Normality Test")

normality_df = shapiro_wilk_test(df)

st.dataframe(
    normality_df,
    use_container_width=True
)

# =====================================================
# OUTLIER SUMMARY
# =====================================================

st.subheader("🚨 Outlier Summary")

outlier_df = outlier_summary(df)

st.dataframe(
    outlier_df,
    use_container_width=True
)

# =====================================================
# HISTOGRAM
# =====================================================

st.subheader("📊 Distribution Histogram")

fig_hist = px.histogram(
    df,
    x=selected_column,
    nbins=30,
    marginal="box",
    title=f"{selected_column} Distribution"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# =====================================================
# BOXPLOT
# =====================================================

st.subheader("📦 Box Plot")

fig_box = px.box(
    df,
    y=selected_column,
    title=f"{selected_column} Boxplot"
)

st.plotly_chart(
    fig_box,
    use_container_width=True
)

# =====================================================
# VIOLIN PLOT
# =====================================================

st.subheader("🎻 Violin Plot")

fig_violin = px.violin(
    df,
    y=selected_column,
    box=True,
    title=f"{selected_column} Violin Plot"
)

st.plotly_chart(
    fig_violin,
    use_container_width=True
)

# =====================================================
# FEATURE DISTRIBUTION SUMMARY
# =====================================================

st.subheader("📋 Selected Feature Summary")

feature_summary = pd.DataFrame({

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

        round(
            df[selected_column].mean(),
            4
        ),

        round(
            df[selected_column].median(),
            4
        ),

        round(
            df[selected_column].min(),
            4
        ),

        round(
            df[selected_column].max(),
            4
        ),

        round(
            df[selected_column].std(),
            4
        ),

        round(
            df[selected_column].var(),
            4
        ),

        round(
            df[selected_column].quantile(0.25),
            4
        ),

        round(
            df[selected_column].quantile(0.75),
            4
        )

    ]

})

st.dataframe(
    feature_summary,
    use_container_width=True
)

# =====================================================
# CORRELATION HEATMAP
# =====================================================

st.subheader("🔥 Correlation Heatmap")

corr = correlation_matrix(df)

fig_heatmap = px.imshow(

    corr,

    text_auto=".2f",

    aspect="auto",

    title="Correlation Matrix"

)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)

# =====================================================
# DATA QUALITY REPORT
# =====================================================

st.subheader("✅ Data Quality Report")

quality_df = data_quality_report(df)

st.dataframe(
    quality_df,
    use_container_width=True
)

# =====================================================
# RAW DATA
# =====================================================

with st.expander(
    "View Dataset"
):

    st.dataframe(
        df,
        use_container_width=True
    )

# =====================================================
# DOWNLOAD SECTION
# =====================================================

csv_data = descriptive_statistics(
    df
).to_csv().encode("utf-8")

st.download_button(

    label="📥 Download Statistics",

    data=csv_data,

    file_name="statistical_analysis.csv",

    mime="text/csv"

)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Statistical Analytics"
)
