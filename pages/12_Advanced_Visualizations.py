import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.advanced_visualizations import (

    crop_soil_treemap,

    crop_irrigation_treemap,

    crop_season_soil_sunburst,

    water_sunburst,

    crop_radar_metrics,

    efficiency_radar,

    bubble_chart_data,

    resource_bubble_data,

    pareto_yield,

    pareto_water,

    correlation_heatmap,

    crop_soil_heatmap,

    crop_irrigation_heatmap,

    water_heatmap,

    fertilizer_heatmap,

    pesticide_heatmap,

    crop_kpi_comparison,

    waterfall_contributors,

    scatter_matrix_data,

    resource_utilization,

    sankey_source_target

)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Advanced Visualizations",
    page_icon="📊",
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

st.title("📊 Advanced Visualization Studio")

st.markdown("""
Interactive visual analytics for
Agriculture Intelligence,
Resource Optimization,
and Sustainability Analytics.
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
# VISUALIZATION SELECTOR
# =====================================================

visual_type = st.selectbox(

    "Select Visualization",

    [

        "Treemap",

        "Sunburst",

        "Radar",

        "Bubble",

        "Scatter Matrix",

        "Heatmaps",

        "Sankey",

        "Waterfall",

        "Executive Dashboard"

    ]

)

# =====================================================
# TREEMAP
# =====================================================

if visual_type == "Treemap":

    st.subheader("🌳 Crop vs Soil Treemap")

    treemap_df = crop_soil_treemap(
        filtered_df
    )

    fig = px.treemap(

        treemap_df,

        path=[
            "Crop_Type",
            "Soil_Type"
        ],

        values="Yield"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "🌾 Crop vs Irrigation Treemap"
    )

    tree2 = crop_irrigation_treemap(
        filtered_df
    )

    fig2 = px.treemap(

        tree2,

        path=[
            "Crop_Type",
            "Irrigation_Type"
        ],

        values="Yield"

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# SUNBURST
# =====================================================

elif visual_type == "Sunburst":

    st.subheader("☀️ Yield Sunburst")

    sunburst_df = (
        crop_season_soil_sunburst(
            filtered_df
        )
    )

    fig = px.sunburst(

        sunburst_df,

        path=[
            "Crop_Type",
            "Season",
            "Soil_Type"
        ],

        values="Yield"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "💧 Water Sunburst"
    )

    water_df = water_sunburst(
        filtered_df
    )

    fig2 = px.sunburst(

        water_df,

        path=[
            "Crop_Type",
            "Season",
            "Irrigation_Type"
        ],

        values="Water"

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# RADAR
# =====================================================

elif visual_type == "Radar":

    st.subheader(
        "🎯 Crop Radar Analysis"
    )

    radar_df = crop_radar_metrics(
        filtered_df
    )

    crop = st.selectbox(
        "Select Crop",
        radar_df["Crop_Type"]
    )

    row = radar_df[
        radar_df["Crop_Type"] == crop
    ].iloc[0]

    fig = go.Figure()

    fig.add_trace(

        go.Scatterpolar(

            r=[

                row["Yield"],

                row["Water"],

                row["Fertilizer"],

                row["Pesticide"]

            ],

            theta=[

                "Yield",

                "Water",

                "Fertilizer",

                "Pesticide"

            ],

            fill="toself"

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "⚡ Efficiency Radar"
    )

    eff_df = efficiency_radar(
        filtered_df
    )

    st.dataframe(
        eff_df,
        use_container_width=True
    )

# =====================================================
# BUBBLE
# =====================================================

elif visual_type == "Bubble":

    st.subheader(
        "🫧 Yield Bubble Chart"
    )

    bubble_df = bubble_chart_data(
        filtered_df
    )

    fig = px.scatter(

        bubble_df,

        x="Water_Usage_cubic_meters",

        y="Yield_tons",

        size="Farm_Area_acres",

        color="Crop_Type",

        hover_name="Crop_Type"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader(
        "🌍 Resource Bubble Analysis"
    )

    resource_df = resource_bubble_data(
        filtered_df
    )

    fig2 = px.scatter(

        resource_df,

        x="Water_Usage_cubic_meters",

        y="Yield_tons",

        size="Fertilizer_Used_tons",

        color="Crop_Type"

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# SCATTER MATRIX
# =====================================================

elif visual_type == "Scatter Matrix":

    st.subheader(
        "📈 Scatter Matrix"
    )

    scatter_df = scatter_matrix_data(
        filtered_df
    )

    selected = st.multiselect(

        "Variables",

        scatter_df.columns,

        default=list(
            scatter_df.columns[:5]
        )

    )

    if len(selected) >= 2:

        fig = px.scatter_matrix(

            scatter_df,

            dimensions=selected

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =====================================================
# HEATMAPS
# =====================================================

elif visual_type == "Heatmaps":

    heatmap_choice = st.selectbox(

        "Select Heatmap",

        [

            "Correlation",

            "Crop Soil",

            "Crop Irrigation",

            "Water",

            "Fertilizer",

            "Pesticide"

        ]

    )

    if heatmap_choice == "Correlation":

        data = correlation_heatmap(
            filtered_df
        )

    elif heatmap_choice == "Crop Soil":

        data = crop_soil_heatmap(
            filtered_df
        )

    elif heatmap_choice == "Crop Irrigation":

        data = crop_irrigation_heatmap(
            filtered_df
        )

    elif heatmap_choice == "Water":

        data = water_heatmap(
            filtered_df
        )

    elif heatmap_choice == "Fertilizer":

        data = fertilizer_heatmap(
            filtered_df
        )

    else:

        data = pesticide_heatmap(
            filtered_df
        )

    fig = px.imshow(

        data,

        text_auto=".2f",

        aspect="auto"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# SANKEY
# =====================================================

elif visual_type == "Sankey":

    st.subheader(
        "🔄 Season → Crop Flow"
    )

    sankey_df = sankey_source_target(
        filtered_df
    )

    st.dataframe(
        sankey_df,
        use_container_width=True
    )

    st.info(
        """
        Sankey data prepared.
        You can extend this section using
        plotly Sankey nodes and links.
        """
    )

# =====================================================
# WATERFALL
# =====================================================

elif visual_type == "Waterfall":

    st.subheader(
        "🌊 Resource Waterfall"
    )

    waterfall_df = waterfall_contributors(
        filtered_df
    )

    fig = go.Figure(

        go.Waterfall(

            x=waterfall_df["Factor"],

            y=waterfall_df["Value"]

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================

elif visual_type == "Executive Dashboard":

    st.subheader(
        "📊 Executive Visualization Dashboard"
    )

    kpi_df = crop_kpi_comparison(
        filtered_df
    )

    fig1 = px.bar(

        kpi_df,

        x="Crop_Type",

        y="Yield",

        color="Yield"

    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.line(

        kpi_df,

        x="Crop_Type",

        y=[
            "Water",
            "Fertilizer",
            "Pesticide"
        ],

        markers=True

    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    resource = resource_utilization(
        filtered_df
    )

    fig3 = px.pie(

        resource,

        names="Resource",

        values="Usage"

    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# =====================================================
# DOWNLOAD SECTION
# =====================================================

st.markdown("---")

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Visualization Dataset",
    csv,
    "advanced_visualization_data.csv",
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
    "Agriculture Analytics Dashboard | Advanced Visualization Studio"
)
