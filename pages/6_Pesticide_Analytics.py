import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data
)

from modules.pesticide_analytics import (

    executive_pesticide_summary,

    crop_pesticide_summary,

    soil_pesticide_summary,

    season_pesticide_summary,

    irrigation_pesticide_summary,

    crop_pesticide_efficiency,

    pesticide_ranking,

    pesticide_pareto_analysis,

    crop_soil_pesticide_heatmap,

    crop_irrigation_pesticide_heatmap,

    season_crop_pesticide_heatmap,

    pesticide_distribution_summary,

    top_pesticide_consumers,

    lowest_pesticide_consumers

)

from modules.business_insights import (
    pesticide_efficiency_insight
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Pesticide Analytics",
    page_icon="☘️",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# TITLE
# =====================================================

st.title("☘️ Pesticide Analytics Dashboard")

st.markdown("""
Analyze pesticide consumption,
efficiency, intensity,
crop dependency,
and sustainability metrics.
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
# KPIs
# =====================================================

summary = executive_pesticide_summary(
    filtered_df
)

st.subheader("📊 Pesticide KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Pesticide",
        f"{summary['Total Pesticide']:,.2f}"
    )

with c2:
    st.metric(
        "Average Pesticide",
        summary["Average Pesticide"]
    )

with c3:
    st.metric(
        "Pesticide Efficiency",
        summary["Pesticide Efficiency"]
    )

with c4:
    st.metric(
        "Pesticide Intensity",
        summary["Pesticide Intensity"]
    )

# =====================================================
# INSIGHT
# =====================================================

st.subheader("💡 Pesticide Insight")

st.info(
    pesticide_efficiency_insight(
        filtered_df
    )
)

# =====================================================
# CROP ANALYSIS
# =====================================================

st.subheader("🌾 Crop-wise Pesticide Usage")

crop_df = crop_pesticide_summary(
    filtered_df
)

fig_crop = px.bar(
    crop_df,
    x="Crop_Type",
    y="Total_Pesticide",
    color="Average_Pesticide",
    title="Pesticide Consumption by Crop"
)

st.plotly_chart(
    fig_crop,
    use_container_width=True
)

# =====================================================
# SOIL ANALYSIS
# =====================================================

st.subheader("🌱 Soil-wise Pesticide Usage")

soil_df = soil_pesticide_summary(
    filtered_df
)

fig_soil = px.pie(
    soil_df,
    names="Soil_Type",
    values="Total_Pesticide",
    title="Pesticide Usage by Soil Type"
)

st.plotly_chart(
    fig_soil,
    use_container_width=True
)

# =====================================================
# SEASON ANALYSIS
# =====================================================

st.subheader("📅 Season-wise Pesticide Usage")

season_df = season_pesticide_summary(
    filtered_df
)

fig_season = px.bar(
    season_df,
    x="Season",
    y="Total_Pesticide",
    color="Average_Pesticide"
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

# =====================================================
# IRRIGATION ANALYSIS
# =====================================================

st.subheader("🚿 Irrigation-wise Pesticide Usage")

irrigation_df = irrigation_pesticide_summary(
    filtered_df
)

fig_irrigation = px.bar(
    irrigation_df,
    x="Irrigation_Type",
    y="Total_Pesticide",
    color="Average_Pesticide"
)

st.plotly_chart(
    fig_irrigation,
    use_container_width=True
)

# =====================================================
# EFFICIENCY RANKING
# =====================================================

st.subheader("🏆 Pesticide Efficiency Ranking")

ranking_df = pesticide_ranking(
    filtered_df
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# =====================================================
# EFFICIENCY TABLE
# =====================================================

st.subheader("📈 Pesticide Efficiency by Crop")

efficiency_df = crop_pesticide_efficiency(
    filtered_df
)

st.dataframe(
    efficiency_df,
    use_container_width=True
)

# =====================================================
# TOP CONSUMERS
# =====================================================

st.subheader("🔝 Highest Pesticide Consuming Crops")

st.dataframe(
    top_pesticide_consumers(
        filtered_df
    ),
    use_container_width=True
)

# =====================================================
# LOWEST CONSUMERS
# =====================================================

st.subheader("🔽 Lowest Pesticide Consuming Crops")

st.dataframe(
    lowest_pesticide_consumers(
        filtered_df
    ),
    use_container_width=True
)

# =====================================================
# DISTRIBUTION
# =====================================================

st.subheader("📊 Pesticide Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="Pesticide_Used_kg",
    nbins=30,
    marginal="box"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# =====================================================
# PARETO ANALYSIS
# =====================================================

st.subheader("📈 Pareto Pesticide Analysis")

pareto_df = pesticide_pareto_analysis(
    filtered_df
)

fig_pareto = go.Figure()

fig_pareto.add_trace(
    go.Bar(
        x=pareto_df["Crop_Type"],
        y=pareto_df["Pesticide_Used_kg"],
        name="Pesticide"
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
        title="Pesticide Usage"
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

st.subheader("🔥 Crop vs Soil Heatmap")

heat1 = crop_soil_pesticide_heatmap(
    filtered_df
)

fig_heat1 = px.imshow(
    heat1,
    text_auto=".2f",
    aspect="auto"
)

st.plotly_chart(
    fig_heat1,
    use_container_width=True
)

st.subheader("🔥 Crop vs Irrigation Heatmap")

heat2 = crop_irrigation_pesticide_heatmap(
    filtered_df
)

fig_heat2 = px.imshow(
    heat2,
    text_auto=".2f",
    aspect="auto"
)

st.plotly_chart(
    fig_heat2,
    use_container_width=True
)

st.subheader("🔥 Season vs Crop Heatmap")

heat3 = season_crop_pesticide_heatmap(
    filtered_df
)

fig_heat3 = px.imshow(
    heat3,
    text_auto=".2f",
    aspect="auto"
)

st.plotly_chart(
    fig_heat3,
    use_container_width=True
)

# =====================================================
# TREEMAP
# =====================================================

st.subheader("🗺 Pesticide Treemap")

fig_tree = px.treemap(
    crop_df,
    path=["Crop_Type"],
    values="Total_Pesticide",
    color="Average_Pesticide"
)

st.plotly_chart(
    fig_tree,
    use_container_width=True
)

# =====================================================
# SUNBURST
# =====================================================

st.subheader("🌞 Pesticide Allocation")

fig_sunburst = px.sunburst(
    crop_df,
    path=["Crop_Type"],
    values="Total_Pesticide"
)

st.plotly_chart(
    fig_sunburst,
    use_container_width=True
)

# =====================================================
# STATISTICS
# =====================================================

st.subheader("📋 Pesticide Statistical Summary")

stats_df = pesticide_distribution_summary(
    filtered_df
)

st.dataframe(
    stats_df,
    use_container_width=True
)

# =====================================================
# RESOURCE UTILIZATION
# =====================================================

st.subheader("📦 Pesticide Resource Allocation")

resource_df = crop_df[
    [
        "Crop_Type",
        "Total_Pesticide"
    ]
]

fig_resource = px.bar(
    resource_df,
    x="Crop_Type",
    y="Total_Pesticide",
    color="Total_Pesticide"
)

st.plotly_chart(
    fig_resource,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = crop_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Pesticide Analytics",
    data=csv,
    file_name="pesticide_analytics.csv",
    mime="text/csv"
)

# =====================================================
# RAW DATA
# =====================================================

with st.expander(
    "View Dataset"
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
    "Agriculture Analytics Dashboard | Pesticide Analytics"
)
