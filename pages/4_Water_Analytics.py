import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data
)

from modules.water_analytics import (

    executive_water_summary,

    crop_water_summary,

    soil_water_summary,

    irrigation_water_summary,

    season_water_summary,

    crop_water_efficiency,

    water_ranking,

    water_pareto_analysis,

    crop_irrigation_water_heatmap,

    crop_soil_water_heatmap,

    season_crop_water_heatmap,

    water_distribution_summary

)

from modules.business_insights import (
    water_insights
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Water Analytics",
    page_icon="💧",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# TITLE
# =====================================================

st.title("💧 Water Analytics Dashboard")

st.markdown("""
Analyze water consumption,
water productivity,
water footprint,
water efficiency,
and irrigation performance.
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
# WATER KPIs
# =====================================================

summary = executive_water_summary(
    filtered_df
)

st.subheader("📊 Water KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Water",
        f"{summary['Total Water']:,.2f}"
    )

with c2:
    st.metric(
        "Average Water",
        summary["Average Water"]
    )

with c3:
    st.metric(
        "Water Productivity",
        summary["Water Productivity"]
    )

with c4:
    st.metric(
        "Water Footprint",
        summary["Water Footprint"]
    )

c5, c6 = st.columns(2)

with c5:
    st.metric(
        "Water Intensity",
        summary["Water Intensity"]
    )

with c6:
    st.metric(
        "Maximum Water Usage",
        summary["Maximum Water"]
    )

# =====================================================
# WATER INSIGHT
# =====================================================

st.subheader("💡 Water Insight")

st.info(
    water_insights(filtered_df)
)

# =====================================================
# CROP WATER ANALYSIS
# =====================================================

st.subheader("🌾 Crop-wise Water Usage")

crop_df = crop_water_summary(
    filtered_df
)

fig_crop = px.bar(
    crop_df,
    x="Crop_Type",
    y="Total_Water",
    color="Average_Water",
    title="Water Consumption by Crop"
)

st.plotly_chart(
    fig_crop,
    use_container_width=True
)

# =====================================================
# SOIL WATER ANALYSIS
# =====================================================

st.subheader("🌱 Soil-wise Water Usage")

soil_df = soil_water_summary(
    filtered_df
)

fig_soil = px.pie(
    soil_df,
    names="Soil_Type",
    values="Total_Water",
    title="Water Usage by Soil Type"
)

st.plotly_chart(
    fig_soil,
    use_container_width=True
)

# =====================================================
# IRRIGATION ANALYSIS
# =====================================================

st.subheader("🚿 Irrigation-wise Water Usage")

irrigation_df = irrigation_water_summary(
    filtered_df
)

fig_irrigation = px.bar(
    irrigation_df,
    x="Irrigation_Type",
    y="Total_Water",
    color="Average_Yield",
    title="Water Usage by Irrigation Type"
)

st.plotly_chart(
    fig_irrigation,
    use_container_width=True
)

# =====================================================
# SEASON ANALYSIS
# =====================================================

st.subheader("📅 Season-wise Water Usage")

season_df = season_water_summary(
    filtered_df
)

fig_season = px.bar(
    season_df,
    x="Season",
    y="Total_Water",
    color="Average_Water",
    title="Season-wise Water Usage"
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

# =====================================================
# WATER PRODUCTIVITY RANKING
# =====================================================

st.subheader("🏆 Water Efficiency Ranking")

ranking_df = water_ranking(
    filtered_df
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# =====================================================
# WATER PRODUCTIVITY TABLE
# =====================================================

st.subheader("📈 Water Productivity by Crop")

efficiency_df = crop_water_efficiency(
    filtered_df
)

st.dataframe(
    efficiency_df,
    use_container_width=True
)

# =====================================================
# WATER DISTRIBUTION
# =====================================================

st.subheader("📊 Water Usage Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="Water_Usage_cubic_meters",
    nbins=30,
    marginal="box",
    title="Water Usage Distribution"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# =====================================================
# PARETO ANALYSIS
# =====================================================

st.subheader("📈 Pareto Water Analysis")

pareto_df = water_pareto_analysis(
    filtered_df
)

fig_pareto = go.Figure()

fig_pareto.add_trace(
    go.Bar(
        x=pareto_df["Crop_Type"],
        y=pareto_df["Water_Usage_cubic_meters"],
        name="Water Usage"
    )
)

fig_pareto.add_trace(
    go.Scatter(
        x=pareto_df["Crop_Type"],
        y=pareto_df["Cumulative_%"],
        yaxis="y2",
        name="Cumulative %"
    )
)

fig_pareto.update_layout(

    yaxis=dict(
        title="Water Usage"
    ),

    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right"
    )

)

st.plotly_chart(
    fig_pareto,
    use_container_width=True
)

# =====================================================
# HEATMAPS
# =====================================================

st.subheader("🔥 Crop vs Irrigation Water Heatmap")

heatmap1 = crop_irrigation_water_heatmap(
    filtered_df
)

fig_heat1 = px.imshow(
    heatmap1,
    text_auto=".1f",
    aspect="auto"
)

st.plotly_chart(
    fig_heat1,
    use_container_width=True
)

st.subheader("🔥 Crop vs Soil Water Heatmap")

heatmap2 = crop_soil_water_heatmap(
    filtered_df
)

fig_heat2 = px.imshow(
    heatmap2,
    text_auto=".1f",
    aspect="auto"
)

st.plotly_chart(
    fig_heat2,
    use_container_width=True
)

st.subheader("🔥 Season vs Crop Water Heatmap")

heatmap3 = season_crop_water_heatmap(
    filtered_df
)

fig_heat3 = px.imshow(
    heatmap3,
    text_auto=".1f",
    aspect="auto"
)

st.plotly_chart(
    fig_heat3,
    use_container_width=True
)

# =====================================================
# WATER STATISTICS
# =====================================================

st.subheader("📋 Water Statistical Summary")

water_stats = water_distribution_summary(
    filtered_df
)

st.dataframe(
    water_stats,
    use_container_width=True
)

# =====================================================
# RESOURCE FLOW
# =====================================================

st.subheader("🔄 Water Resource Flow")

flow_df = pd.DataFrame({

    "Stage": [
        "Water Usage",
        "Crop Yield"
    ],

    "Value": [

        filtered_df[
            "Water_Usage_cubic_meters"
        ].sum(),

        filtered_df[
            "Yield_tons"
        ].sum()

    ]
})

fig_flow = px.funnel(
    flow_df,
    x="Value",
    y="Stage"
)

st.plotly_chart(
    fig_flow,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = crop_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Water Analytics",
    data=csv,
    file_name="water_analytics.csv",
    mime="text/csv"
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
    "Agriculture Analytics Dashboard | Water Analytics"
)
