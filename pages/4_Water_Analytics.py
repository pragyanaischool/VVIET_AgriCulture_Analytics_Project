import streamlit as st
import pandas as pd
import plotly.express as px

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.water_analytics import (

    executive_water_summary,

    crop_water_summary,

    season_water_summary,

    crop_water_efficiency,

    water_ranking,

    top_water_efficient_crops,

    low_water_efficient_crops,

    water_distribution_summary,

    water_heatmap,

    water_productivity,

    water_footprint,

    water_insights,

    water_kpi_table,

    water_benchmark

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
df = create_derived_metrics(df)

# =====================================================
# TITLE
# =====================================================

st.title("💧 Water Analytics Dashboard")

st.markdown("""
Comprehensive Water Usage, Productivity,
Efficiency, Sustainability and Benchmarking Analytics.
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
# EXECUTIVE KPIs
# =====================================================

summary = executive_water_summary(
    filtered_df
)

st.subheader("📊 Water KPI Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Water",
        summary["Total Water"]
    )

with c2:
    st.metric(
        "Average Water",
        summary["Average Water"]
    )

with c3:
    st.metric(
        "Maximum Water",
        summary["Maximum Water"]
    )

with c4:
    st.metric(
        "Water Productivity",
        summary["Water Productivity"]
    )

# =====================================================
# WATER PRODUCTIVITY
# =====================================================

st.subheader("⚡ Water Productivity")

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Water Productivity",
        water_productivity(filtered_df)
    )

with c2:

    st.metric(
        "Water Footprint",
        water_footprint(filtered_df)
    )

# =====================================================
# CROP WATER SUMMARY
# =====================================================

st.subheader("🌾 Crop Water Summary")

crop_summary = crop_water_summary(
    filtered_df
)

st.dataframe(
    crop_summary,
    use_container_width=True
)

fig_crop = px.bar(

    crop_summary,

    x="Crop_Type",

    y="Total_Water",

    color="Total_Water",

    title="Water Usage by Crop"

)

st.plotly_chart(
    fig_crop,
    use_container_width=True
)

# =====================================================
# SEASON WATER SUMMARY
# =====================================================

st.subheader("📅 Season Water Usage")

season_summary = season_water_summary(
    filtered_df
)

st.dataframe(
    season_summary,
    use_container_width=True
)

fig_season = px.bar(

    season_summary,

    x="Season",

    y="Total_Water",

    color="Total_Water",

    title="Season Water Consumption"

)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

# =====================================================
# WATER EFFICIENCY
# =====================================================

st.subheader("💧 Water Efficiency")

eff_df = crop_water_efficiency(
    filtered_df
)

st.dataframe(
    eff_df,
    use_container_width=True
)

fig_eff = px.bar(

    eff_df,

    x="Crop_Type",

    y="Water_Efficiency",

    color="Water_Efficiency",

    title="Water Efficiency by Crop"

)

st.plotly_chart(
    fig_eff,
    use_container_width=True
)

# =====================================================
# RANKING
# =====================================================

st.subheader("🏆 Water Efficiency Ranking")

ranking = water_ranking(
    filtered_df
)

st.dataframe(
    ranking,
    use_container_width=True
)

# =====================================================
# TOP CROPS
# =====================================================

st.subheader("🥇 Top Water Efficient Crops")

top_df = top_water_efficient_crops(
    filtered_df,
    top_n=10
)

st.dataframe(
    top_df,
    use_container_width=True
)

# =====================================================
# LOW CROPS
# =====================================================

st.subheader("⚠️ Low Water Efficient Crops")

low_df = low_water_efficient_crops(
    filtered_df,
    top_n=10
)

st.dataframe(
    low_df,
    use_container_width=True
)

# =====================================================
# HEATMAP
# =====================================================

st.subheader("🔥 Water Heatmap")

heatmap_df = water_heatmap(
    filtered_df
)

fig_heat = px.imshow(

    heatmap_df,

    text_auto=".2f",

    aspect="auto",

    title="Crop vs Season Water Usage"

)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)

# =====================================================
# DISTRIBUTION
# =====================================================

st.subheader("📈 Water Distribution")

dist_df = water_distribution_summary(
    filtered_df
)

st.dataframe(
    dist_df,
    use_container_width=True
)

# =====================================================
# KPI TABLE
# =====================================================

st.subheader("📋 KPI Table")

kpi_table = water_kpi_table(
    filtered_df
)

st.dataframe(
    kpi_table,
    use_container_width=True
)

# =====================================================
# BENCHMARK
# =====================================================

st.subheader("🎯 Water Benchmark")

benchmark_df = water_benchmark(
    filtered_df
)

st.dataframe(
    benchmark_df,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader("💡 Water Insights")

insights = water_insights(
    filtered_df
)

if len(insights) > 0:

    st.success(
        f"Best Water Efficient Crop: {insights['Best Water Efficient Crop']}"
    )

    st.warning(
        f"Lowest Water Efficient Crop: {insights['Lowest Water Efficient Crop']}"
    )

# =====================================================
# DOWNLOAD
# =====================================================

csv = benchmark_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    "📥 Download Water Analytics",

    csv,

    "water_analytics.csv",

    "text/csv"

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
    "Agriculture Analytics Dashboard | Water Analytics"
)
