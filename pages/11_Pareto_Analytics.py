import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.yield_analytics import (
    pareto_yield_analysis
)

from modules.water_analytics import (
    water_pareto_analysis
)

from modules.fertilizer_analytics import (
    fertilizer_pareto_analysis
)

from modules.pesticide_analytics import (
    pesticide_pareto_analysis
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Pareto Analytics",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()
df = create_derived_metrics(df)

# =====================================================
# TITLE
# =====================================================

st.title("📈 Pareto Analytics Dashboard")

st.markdown("""
Pareto Analysis helps identify the
critical few contributors responsible
for the majority of agricultural output
and resource consumption.
""")

# =====================================================
# FILTERS
# =====================================================

st.sidebar.header("Filters")

crop_filter = st.sidebar.multiselect(
    "Crop Type",
    sorted(df["Crop_Type"].unique()),
    default=sorted(df["Crop_Type"].unique())
)

season_filter = st.sidebar.multiselect(
    "Season",
    sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

filtered_df = df[
    (df["Crop_Type"].isin(crop_filter))
    &
    (df["Season"].isin(season_filter))
]

# =====================================================
# ANALYSIS TYPE
# =====================================================

analysis_type = st.selectbox(

    "Select Pareto Analysis",

    [

        "Yield",

        "Water",

        "Fertilizer",

        "Pesticide"

    ]

)

# =====================================================
# YIELD PARETO
# =====================================================

if analysis_type == "Yield":

    pareto_df = pareto_yield_analysis(
        filtered_df
    )

    value_col = "Yield_tons"

    title = "Yield Pareto Analysis"

# =====================================================
# WATER PARETO
# =====================================================

elif analysis_type == "Water":

    pareto_df = water_pareto_analysis(
        filtered_df
    )

    value_col = "Total_Water"

    title = "Water Pareto Analysis"

# =====================================================
# FERTILIZER PARETO
# =====================================================

elif analysis_type == "Fertilizer":

    pareto_df = fertilizer_pareto_analysis(
        filtered_df
    )

    value_col = "Total_Fertilizer"

    title = "Fertilizer Pareto Analysis"

# =====================================================
# PESTICIDE PARETO
# =====================================================

else:

    pareto_df = pesticide_pareto_analysis(
        filtered_df
    )

    value_col = "Total_Pesticide"

    title = "Pesticide Pareto Analysis"

# =====================================================
# TABLE
# =====================================================

st.subheader(title)

st.dataframe(
    pareto_df,
    use_container_width=True
)

# =====================================================
# PARETO CHART
# =====================================================

fig = go.Figure()

fig.add_trace(

    go.Bar(

        x=pareto_df["Crop_Type"],

        y=pareto_df[value_col],

        name="Contribution"

    )

)

fig.add_trace(

    go.Scatter(

        x=pareto_df["Crop_Type"],

        y=pareto_df["Cumulative_%"],

        name="Cumulative %",

        yaxis="y2"

    )

)

fig.update_layout(

    title=title,

    xaxis_title="Crop Type",

    yaxis_title=value_col,

    yaxis2=dict(

        title="Cumulative %",

        overlaying="y",

        side="right",

        range=[0, 110]

    ),

    legend=dict(
        orientation="h"
    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# 80-20 ANALYSIS
# =====================================================

st.subheader("🎯 80-20 Analysis")

critical_crops = pareto_df[
    pareto_df["Cumulative_%"] <= 80
]

st.metric(
    "Critical Crops (≈80%)",
    len(critical_crops)
)

st.dataframe(
    critical_crops,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("💡 Insights")

top_crop = pareto_df.iloc[0]["Crop_Type"]

top_contribution = pareto_df.iloc[0][value_col]

st.success(

    f"Top Contributor: {top_crop} "
    f"({top_contribution:,.2f})"

)

st.info(

    f"{len(critical_crops)} crops contribute "
    f"approximately 80% of the total impact."

)

# =====================================================
# DOWNLOAD
# =====================================================

csv = pareto_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    "📥 Download Pareto Analysis",

    csv,

    f"{analysis_type.lower()}_pareto.csv",

    "text/csv"

)

# =====================================================
# RAW DATA
# =====================================================

with st.expander("View Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Pareto Analytics"
)
