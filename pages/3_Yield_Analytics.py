import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.yield_analytics import (

    executive_yield_summary,

    crop_yield_summary,

    season_yield_summary,

    soil_yield_summary,

    irrigation_yield_summary,

    crop_ranking,

    top_crops,

    bottom_crops,

    pareto_yield_analysis,

    crop_soil_heatmap,

    crop_irrigation_heatmap,

    season_crop_heatmap,

    yield_distribution_summary,

    farm_performance

)

from modules.business_insights import (
    yield_insights
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Yield Analytics",
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

st.title("🌾 Yield Analytics Dashboard")

st.markdown(
    """
    Analyze crop productivity, yield efficiency,
    crop rankings, seasonal performance,
    and farm-level yield analytics.
    """
)

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
# EXECUTIVE KPI
# =====================================================

summary = executive_yield_summary(
    filtered_df
)

st.subheader("📊 Yield KPIs")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Total Yield",
        summary["Total Yield"]
    )

with c2:
    st.metric(
        "Average Yield",
        summary["Average Yield"]
    )

with c3:
    st.metric(
        "Maximum Yield",
        summary["Maximum Yield"]
    )

with c4:
    st.metric(
        "Yield Per Acre",
        summary["Yield Per Acre"]
    )

with c5:
    st.metric(
        "Best Crop",
        summary["Best Crop"]
    )

# =====================================================
# YIELD INSIGHT
# =====================================================

st.subheader("💡 Yield Insight")

st.success(
    yield_insights(filtered_df)
)

# =====================================================
# CROP YIELD ANALYSIS
# =====================================================

st.subheader("🌾 Crop-wise Yield")

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

st.subheader("📅 Season-wise Yield")

season_df = season_yield_summary(
    filtered_df
)

fig_season = px.bar(
    season_df,
    x="Season",
    y="Total_Yield",
    color="Average_Yield",
    title="Season-wise Yield"
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

# =====================================================
# SOIL ANALYSIS
# =====================================================

st.subheader("🌱 Soil-wise Yield")

soil_df = soil_yield_summary(
    filtered_df
)

fig_soil = px.pie(
    soil_df,
    names="Soil_Type",
    values="Total_Yield",
    title="Yield Contribution by Soil"
)

st.plotly_chart(
    fig_soil,
    use_container_width=True
)

# =====================================================
# IRRIGATION ANALYSIS
# =====================================================

st.subheader("💧 Irrigation-wise Yield")

irrigation_df = irrigation_yield_summary(
    filtered_df
)

fig_irrigation = px.bar(
    irrigation_df,
    x="Irrigation_Type",
    y="Total_Yield",
    color="Average_Yield",
    title="Yield by Irrigation Type"
)

st.plotly_chart(
    fig_irrigation,
    use_container_width=True
)

# =====================================================
# TREEMAP
# =====================================================

st.subheader("🗺 Yield Treemap")

fig_treemap = px.treemap(
    crop_df,
    path=["Crop_Type"],
    values="Total_Yield",
    color="Average_Yield"
)

st.plotly_chart(
    fig_treemap,
    use_container_width=True
)

# =====================================================
# CROP RANKING
# =====================================================

st.subheader("🏆 Crop Ranking")

ranking_df = crop_ranking(
    filtered_df
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# =====================================================
# TOP CROPS
# =====================================================

st.subheader("🥇 Top Performing Crops")

top_df = top_crops(
    filtered_df,
    top_n=10
)

st.dataframe(
    top_df,
    use_container_width=True
)

# =====================================================
# BOTTOM CROPS
# =====================================================

st.subheader("📉 Lowest Performing Crops")

bottom_df = bottom_crops(
    filtered_df,
    top_n=10
)

st.dataframe(
    bottom_df,
    use_container_width=True
)

# =====================================================
# YIELD DISTRIBUTION
# =====================================================

st.subheader("📊 Yield Distribution")

fig_hist = px.histogram(
    filtered_df,
    x="Yield_tons",
    nbins=30,
    marginal="box",
    title="Yield Distribution"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# =====================================================
# PARETO ANALYSIS
# =====================================================

st.subheader("📈 Pareto Yield Analysis")

pareto_df = pareto_yield_analysis(
    filtered_df
)

fig_pareto = go.Figure()

fig_pareto.add_trace(
    go.Bar(
        x=pareto_df["Crop_Type"],
        y=pareto_df["Yield_tons"],
        name="Yield"
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
        title="Yield"
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

heatmap1 = crop_soil_heatmap(
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

st.subheader("🔥 Crop vs Irrigation Heatmap")

heatmap2 = crop_irrigation_heatmap(
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

st.subheader("🔥 Season vs Crop Heatmap")

heatmap3 = season_crop_heatmap(
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
# FARM PERFORMANCE
# =====================================================

st.subheader("🚜 Farm Performance")

farm_df = farm_performance(
    filtered_df
)

st.dataframe(
    farm_df,
    use_container_width=True
)

# =====================================================
# DISTRIBUTION SUMMARY
# =====================================================

st.subheader("📋 Yield Statistical Summary")

summary_df = yield_distribution_summary(
    filtered_df
)

st.dataframe(
    summary_df,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = crop_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Crop Yield Report",
    data=csv,
    file_name="crop_yield_analysis.csv",
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
    "Agriculture Analytics Dashboard | Yield Analytics"
)
