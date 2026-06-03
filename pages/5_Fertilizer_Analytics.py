import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data
)

from modules.fertilizer_analytics import (

    executive_fertilizer_summary,

    crop_fertilizer_summary,

    soil_fertilizer_summary,

    season_fertilizer_summary,

    irrigation_fertilizer_summary,

    crop_fertilizer_efficiency,

    fertilizer_ranking,

    fertilizer_pareto_analysis,

    crop_soil_fertilizer_heatmap,

    crop_irrigation_fertilizer_heatmap,

    season_crop_fertilizer_heatmap,

    fertilizer_distribution_summary

)

from modules.business_insights import (
    fertilizer_efficiency_insight
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fertilizer Analytics",
    page_icon="🧪",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

# =====================================================
# TITLE
# =====================================================

st.title("🧪 Fertilizer Analytics Dashboard")

st.markdown("""
Comprehensive fertilizer utilization,
efficiency, intensity, sustainability,
and optimization analytics.
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

summary = executive_fertilizer_summary(
    filtered_df
)

st.subheader("📊 Fertilizer KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Fertilizer",
        summary["Total Fertilizer"]
    )

with c2:
    st.metric(
        "Average Fertilizer",
        summary["Average Fertilizer"]
    )

with c3:
    st.metric(
        "Fertilizer Efficiency",
        summary["Fertilizer Efficiency"]
    )

with c4:
    st.metric(
        "Fertilizer Intensity",
        summary["Fertilizer Intensity"]
    )

# =====================================================
# INSIGHT
# =====================================================

st.subheader("💡 Fertilizer Insight")

st.info(
    fertilizer_efficiency_insight(
        filtered_df
    )
)

# =====================================================
# CROP ANALYSIS
# =====================================================

st.subheader("🌾 Crop-wise Fertilizer Usage")

crop_df = crop_fertilizer_summary(
    filtered_df
)

fig_crop = px.bar(
    crop_df,
    x="Crop_Type",
    y="Total_Fertilizer",
    color="Average_Fertilizer",
    title="Fertilizer Consumption by Crop"
)

st.plotly_chart(
    fig_crop,
    use_container_width=True
)

# =====================================================
# SOIL ANALYSIS
# =====================================================

st.subheader("🌱 Soil-wise Fertilizer Usage")

soil_df = soil_fertilizer_summary(
    filtered_df
)

fig_soil = px.pie(
    soil_df,
    names="Soil_Type",
    values="Total_Fertilizer",
    title="Fertilizer Usage by Soil Type"
)

st.plotly_chart(
    fig_soil,
    use_container_width=True
)

# =====================================================
# SEASON ANALYSIS
# =====================================================

st.subheader("📅 Season-wise Fertilizer Usage")

season_df = season_fertilizer_summary(
    filtered_df
)

fig_season = px.bar(
    season_df,
    x="Season",
    y="Total_Fertilizer",
    color="Average_Fertilizer"
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

# =====================================================
# IRRIGATION ANALYSIS
# =====================================================

st.subheader("🚿 Irrigation-wise Fertilizer Usage")

irrigation_df = irrigation_fertilizer_summary(
    filtered_df
)

fig_irrigation = px.bar(
    irrigation_df,
    x="Irrigation_Type",
    y="Total_Fertilizer",
    color="Average_Fertilizer"
)

st.plotly_chart(
    fig_irrigation,
    use_container_width=True
)

# =====================================================
# EFFICIENCY RANKING
# =====================================================

st.subheader("🏆 Fertilizer Efficiency Ranking")

ranking_df = fertilizer_ranking(
    filtered_df
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# =====================================================
# EFFICIENCY TABLE
# =====================================================

st.subheader("📈 Fertilizer Efficiency by Crop")

efficiency_df = crop_fertilizer_efficiency(
    filtered_df
)

st.dataframe(
    efficiency_df,
    use_container_width=True
)

# =====================================================
# DISTRIBUTION
# =====================================================

st.subheader("📊 Fertilizer Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="Fertilizer_Used_tons",
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

st.subheader("📈 Pareto Fertilizer Analysis")

pareto_df = fertilizer_pareto_analysis(
    filtered_df
)

fig_pareto = go.Figure()

fig_pareto.add_trace(
    go.Bar(
        x=pareto_df["Crop_Type"],
        y=pareto_df["Fertilizer_Used_tons"],
        name="Fertilizer"
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
        title="Fertilizer"
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

heat1 = crop_soil_fertilizer_heatmap(
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

heat2 = crop_irrigation_fertilizer_heatmap(
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

heat3 = season_crop_fertilizer_heatmap(
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

st.subheader("🗺 Fertilizer Treemap")

fig_tree = px.treemap(
    crop_df,
    path=["Crop_Type"],
    values="Total_Fertilizer",
    color="Average_Fertilizer"
)

st.plotly_chart(
    fig_tree,
    use_container_width=True
)

# =====================================================
# STATISTICS
# =====================================================

st.subheader("📋 Fertilizer Statistical Summary")

stats_df = fertilizer_distribution_summary(
    filtered_df
)

st.dataframe(
    stats_df,
    use_container_width=True
)

# =====================================================
# RESOURCE ALLOCATION
# =====================================================

st.subheader("📦 Fertilizer Resource Allocation")

resource_df = crop_df[
    [
        "Crop_Type",
        "Total_Fertilizer"
    ]
]

fig_resource = px.sunburst(
    resource_df,
    path=["Crop_Type"],
    values="Total_Fertilizer"
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
    label="📥 Download Fertilizer Analytics",
    data=csv,
    file_name="fertilizer_analytics.csv",
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
    "Agriculture Analytics Dashboard | Fertilizer Analytics"
)
