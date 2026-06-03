import streamlit as st
import plotly.express as px
import pandas as pd

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.kpi_metrics import (
    executive_summary
)

from modules.business_insights import (
    complete_business_report
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()
df = create_derived_metrics(df)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Dashboard Filters")

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

soil_filter = st.sidebar.multiselect(
    "Soil Type",
    sorted(df["Soil_Type"].unique()),
    default=sorted(df["Soil_Type"].unique())
)

filtered_df = df[
    (df["Crop_Type"].isin(crop_filter))
    &
    (df["Season"].isin(season_filter))
    &
    (df["Soil_Type"].isin(soil_filter))
]

# =====================================================
# TITLE
# =====================================================

st.title("🌾 Agriculture Executive Dashboard")

st.markdown(
    """
    Enterprise Agriculture Intelligence Dashboard

    Monitor:
    - Yield Performance
    - Water Consumption
    - Fertilizer Utilization
    - Pesticide Usage
    - Sustainability Metrics
    - ESG Indicators
    """
)

# =====================================================
# EXECUTIVE KPI SUMMARY
# =====================================================

summary = executive_summary(filtered_df)

st.subheader("📊 Executive KPI Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Yield",
        f"{summary['Total Yield']:,.2f}"
    )

with c2:
    st.metric(
        "Total Water",
        f"{summary['Total Water']:,.2f}"
    )

with c3:
    st.metric(
        "Total Fertilizer",
        f"{summary['Total Fertilizer']:,.2f}"
    )

with c4:
    st.metric(
        "Total Pesticide",
        f"{summary['Total Pesticide']:,.2f}"
    )

# =====================================================
# SECOND KPI ROW
# =====================================================

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.metric(
        "Avg Yield",
        round(summary["Average Yield"], 2)
    )

with c6:
    st.metric(
        "Avg Water",
        round(summary["Average Water"], 2)
    )

with c7:
    st.metric(
        "Avg Fertilizer",
        round(summary["Average Fertilizer"], 2)
    )

with c8:
    st.metric(
        "Avg Pesticide",
        round(summary["Average Pesticide"], 2)
    )

# =====================================================
# YIELD OVERVIEW
# =====================================================

st.subheader("🌾 Yield by Crop")

yield_df = (
    filtered_df
    .groupby("Crop_Type", as_index=False)
    .agg(
        Total_Yield=("Yield_tons", "sum")
    )
    .sort_values(
        "Total_Yield",
        ascending=False
    )
)

fig_yield = px.bar(
    yield_df,
    x="Crop_Type",
    y="Total_Yield",
    color="Total_Yield",
    title="Crop Yield Contribution"
)

st.plotly_chart(
    fig_yield,
    use_container_width=True
)

# =====================================================
# RESOURCE UTILIZATION
# =====================================================

st.subheader("📦 Resource Utilization")

resource_df = pd.DataFrame({

    "Resource": [
        "Water",
        "Fertilizer",
        "Pesticide"
    ],

    "Usage": [

        filtered_df[
            "Water_Usage_cubic_meters"
        ].sum(),

        filtered_df[
            "Fertilizer_Used_tons"
        ].sum(),

        filtered_df[
            "Pesticide_Used_kg"
        ].sum()
    ]
})

fig_resource = px.pie(
    resource_df,
    names="Resource",
    values="Usage",
    hole=0.4
)

st.plotly_chart(
    fig_resource,
    use_container_width=True
)

# =====================================================
# SEASON ANALYSIS
# =====================================================

st.subheader("📅 Season-wise Yield")

season_df = (
    filtered_df
    .groupby("Season", as_index=False)
    .agg(
        Total_Yield=("Yield_tons", "sum")
    )
)

fig_season = px.bar(
    season_df,
    x="Season",
    y="Total_Yield",
    color="Total_Yield"
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

# =====================================================
# SUSTAINABILITY OVERVIEW
# =====================================================

st.subheader("🌱 Sustainability Overview")

sustainability_df = (
    filtered_df
    .groupby("Crop_Type", as_index=False)
    .agg(
        Yield=("Yield_tons", "sum"),
        Water=("Water_Usage_cubic_meters", "sum"),
        Fertilizer=("Fertilizer_Used_tons", "sum"),
        Pesticide=("Pesticide_Used_kg", "sum")
    )
)

fig_bubble = px.scatter(
    sustainability_df,
    x="Water",
    y="Yield",
    size="Fertilizer",
    color="Crop_Type",
    hover_name="Crop_Type"
)

st.plotly_chart(
    fig_bubble,
    use_container_width=True
)

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("💡 Executive Insights")

try:

    insights = complete_business_report(
        filtered_df
    )

    if isinstance(insights, dict):

        if "Executive Summary" in insights:
            st.success(
                insights["Executive Summary"]
            )

        if "Recommendations" in insights:

            st.markdown(
                "### Recommendations"
            )

            for rec in insights["Recommendations"]:
                st.write(f"✅ {rec}")

except Exception as e:

    st.warning(
        f"Business insights unavailable: {e}"
    )

# =====================================================
# DATA PREVIEW
# =====================================================

with st.expander(
    "View Filtered Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# DOWNLOAD DATA
# =====================================================

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "executive_dashboard_data.csv",
    "text/csv"
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Executive Dashboard"
)
