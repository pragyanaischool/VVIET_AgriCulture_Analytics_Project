import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

from modules.yield_analytics import (
    crop_yield_summary,
    season_yield_summary,
    soil_yield_summary
)

from modules.water_analytics import (
    crop_water_summary
)

from modules.fertilizer_analytics import (
    crop_fertilizer_summary
)

from modules.pesticide_analytics import (
    crop_pesticide_summary
)

from modules.sustainability_analytics import (
    executive_sustainability_summary
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
# TITLE
# =====================================================

st.title("🌾 Agriculture Executive Dashboard")

st.markdown(
    """
    Executive overview of agricultural productivity,
    resource utilization, sustainability, and business insights.
    """
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Dashboard Filters")

crop_filter = st.sidebar.multiselect(
    "Select Crop",
    sorted(df["Crop_Type"].unique()),
    default=sorted(df["Crop_Type"].unique())
)

season_filter = st.sidebar.multiselect(
    "Select Season",
    sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

soil_filter = st.sidebar.multiselect(
    "Select Soil Type",
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
# KPI SUMMARY
# =====================================================

summary = executive_summary(filtered_df)

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Farms",
        summary["Total Farms"]
    )

with col2:
    st.metric(
        "Total Area",
        f"{summary['Total Area']:,.2f}"
    )

with col3:
    st.metric(
        "Total Yield",
        f"{summary['Total Yield']:,.2f}"
    )

with col4:
    st.metric(
        "Total Water",
        f"{summary['Total Water Usage']:,.2f}"
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Yield Per Acre",
        summary["Yield Per Acre"]
    )

with col2:
    st.metric(
        "Water Productivity",
        summary["Water Productivity"]
    )

with col3:
    st.metric(
        "Fertilizer Efficiency",
        summary["Fertilizer Efficiency"]
    )

with col4:
    st.metric(
        "Pesticide Efficiency",
        summary["Pesticide Efficiency"]
    )

# =====================================================
# SUSTAINABILITY KPIs
# =====================================================

st.subheader("🌱 Sustainability Overview")

sustainability = executive_sustainability_summary(
    filtered_df
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Sustainability Score",
        sustainability["Sustainability Score"]
    )

with c2:
    st.metric(
        "Resource Intensity",
        sustainability["Resource Intensity"]
    )

with c3:
    st.metric(
        "Carbon Footprint",
        sustainability["Carbon Footprint"]
    )

with c4:
    st.metric(
        "ESG Score",
        sustainability["ESG Score"]
    )

# =====================================================
# CROP DISTRIBUTION
# =====================================================

st.subheader("🌾 Crop Yield Analysis")

crop_df = crop_yield_summary(
    filtered_df
)

fig_crop = px.bar(
    crop_df,
    x="Crop_Type",
    y="Total_Yield",
    color="Average_Yield",
    title="Total Yield by Crop"
)

st.plotly_chart(
    fig_crop,
    use_container_width=True
)

# =====================================================
# SEASON ANALYSIS
# =====================================================

season_df = season_yield_summary(
    filtered_df
)

fig_season = px.pie(
    season_df,
    names="Season",
    values="Total_Yield",
    title="Yield Contribution by Season"
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

# =====================================================
# SOIL ANALYSIS
# =====================================================

soil_df = soil_yield_summary(
    filtered_df
)

fig_soil = px.treemap(
    soil_df,
    path=["Soil_Type"],
    values="Total_Yield",
    color="Average_Yield",
    title="Yield by Soil Type"
)

st.plotly_chart(
    fig_soil,
    use_container_width=True
)

# =====================================================
# WATER ANALYSIS
# =====================================================

st.subheader("💧 Water Consumption Analysis")

water_df = crop_water_summary(
    filtered_df
)

fig_water = px.bar(
    water_df,
    x="Crop_Type",
    y="Total_Water",
    color="Average_Water",
    title="Water Usage by Crop"
)

st.plotly_chart(
    fig_water,
    use_container_width=True
)

# =====================================================
# FERTILIZER ANALYSIS
# =====================================================

st.subheader("🧪 Fertilizer Usage")

fert_df = crop_fertilizer_summary(
    filtered_df
)

fig_fert = px.bar(
    fert_df,
    x="Crop_Type",
    y="Total_Fertilizer",
    color="Average_Fertilizer",
    title="Fertilizer Usage by Crop"
)

st.plotly_chart(
    fig_fert,
    use_container_width=True
)

# =====================================================
# PESTICIDE ANALYSIS
# =====================================================

st.subheader("☘️ Pesticide Usage")

pest_df = crop_pesticide_summary(
    filtered_df
)

fig_pest = px.bar(
    pest_df,
    x="Crop_Type",
    y="Total_Pesticide",
    color="Average_Pesticide",
    title="Pesticide Usage by Crop"
)

st.plotly_chart(
    fig_pest,
    use_container_width=True
)

# =====================================================
# RESOURCE UTILIZATION
# =====================================================

st.subheader("📈 Resource Utilization")

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
    hole=0.4,
    title="Resource Utilization Mix"
)

st.plotly_chart(
    fig_resource,
    use_container_width=True
)

# =====================================================
# BUSINESS INSIGHTS
# =====================================================

st.subheader("💡 Business Insights")

report = complete_business_report(
    filtered_df
)

st.success(
    report["Yield Insight"]
)

st.info(
    report["Water Insight"]
)

st.warning(
    report["Sustainability"]
)

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.subheader("✅ Recommendations")

for rec in report["Recommendations"]:

    st.markdown(
        f"- {rec}"
    )

# =====================================================
# ALERTS
# =====================================================

if len(report["Alerts"]) > 0:

    st.subheader("🚨 Alerts")

    for alert in report["Alerts"]:

        st.error(alert)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📄 Executive Summary")

st.write(
    report["Executive Summary"]
)

# =====================================================
# RAW DATA
# =====================================================

with st.expander(
    "View Filtered Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Executive Dashboard"
)
