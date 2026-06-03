import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.sustainability_analytics import (

    executive_sustainability_summary,

    resource_intensity_score,

    sustainability_score,

    water_sustainability_score,

    fertilizer_sustainability_score,

    pesticide_sustainability_score,

    carbon_footprint,

    carbon_per_yield,

    esg_agriculture_score,

    crop_sustainability_summary,

    soil_sustainability_summary,

    season_sustainability_summary,

    irrigation_sustainability_summary,

    sustainability_ranking,

    sustainability_pareto_analysis,

    crop_soil_sustainability_heatmap,

    crop_irrigation_sustainability_heatmap,

    season_crop_sustainability_heatmap

)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Sustainability Analytics",
    page_icon="🌱",
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

st.title("🌱 Sustainability Analytics Dashboard")

st.markdown("""
Analyze agricultural sustainability,
resource efficiency, carbon footprint,
ESG indicators, and sustainability rankings.
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
# KPI SECTION
# =====================================================

summary = executive_sustainability_summary(
    filtered_df
)

st.subheader("📊 Sustainability KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Resource Intensity",
        summary["Resource Intensity"]
    )

with c2:
    st.metric(
        "Sustainability Score",
        summary["Sustainability Score"]
    )

with c3:
    st.metric(
        "Carbon Footprint",
        summary["Carbon Footprint"]
    )

with c4:
    st.metric(
        "ESG Score",
        summary["ESG Score"]
    )

c5, c6, c7, c8 = st.columns(4)

with c5:
    st.metric(
        "Water Sustainability",
        summary["Water Sustainability"]
    )

with c6:
    st.metric(
        "Fertilizer Sustainability",
        summary["Fertilizer Sustainability"]
    )

with c7:
    st.metric(
        "Pesticide Sustainability",
        summary["Pesticide Sustainability"]
    )

with c8:
    st.metric(
        "Carbon / Yield",
        summary["Carbon Per Yield"]
    )

# =====================================================
# ESG SCORECARD
# =====================================================

st.subheader("🌍 ESG Sustainability Scorecard")

esg_df = pd.DataFrame({

    "Metric": [

        "Water Sustainability",

        "Fertilizer Sustainability",

        "Pesticide Sustainability",

        "Overall Sustainability",

        "ESG Score"

    ],

    "Score": [

        water_sustainability_score(
            filtered_df
        ),

        fertilizer_sustainability_score(
            filtered_df
        ),

        pesticide_sustainability_score(
            filtered_df
        ),

        sustainability_score(
            filtered_df
        ),

        esg_agriculture_score(
            filtered_df
        )

    ]

})

fig_esg = px.bar(
    esg_df,
    x="Metric",
    y="Score",
    color="Score",
    title="ESG Sustainability Scorecard"
)

st.plotly_chart(
    fig_esg,
    use_container_width=True
)

# =====================================================
# CARBON ANALYTICS
# =====================================================

st.subheader("🌎 Carbon Footprint Analysis")

carbon_df = pd.DataFrame({

    "Metric": [

        "Carbon Footprint",

        "Carbon Per Yield"

    ],

    "Value": [

        carbon_footprint(
            filtered_df
        ),

        carbon_per_yield(
            filtered_df
        )

    ]

})

fig_carbon = px.bar(
    carbon_df,
    x="Metric",
    y="Value",
    color="Value",
    title="Carbon Indicators"
)

st.plotly_chart(
    fig_carbon,
    use_container_width=True
)

# =====================================================
# RESOURCE INTENSITY
# =====================================================

st.subheader("⚡ Resource Intensity")

resource_df = pd.DataFrame({

    "Metric": [

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
    names="Metric",
    values="Usage",
    hole=0.4,
    title="Resource Consumption Mix"
)

st.plotly_chart(
    fig_resource,
    use_container_width=True
)

# =====================================================
# CROP SUSTAINABILITY
# =====================================================

st.subheader("🌾 Crop Sustainability Ranking")

crop_df = crop_sustainability_summary(
    filtered_df
)

st.dataframe(
    crop_df,
    use_container_width=True
)

fig_crop = px.bar(
    crop_df,
    x="Crop_Type",
    y="Sustainability_Score",
    color="Sustainability_Score",
    title="Crop Sustainability Ranking"
)

st.plotly_chart(
    fig_crop,
    use_container_width=True
)

# =====================================================
# SOIL SUSTAINABILITY
# =====================================================

st.subheader("🌱 Soil Sustainability")

soil_df = soil_sustainability_summary(
    filtered_df
)

fig_soil = px.bar(
    soil_df,
    x="Soil_Type",
    y="Sustainability_Score",
    color="Sustainability_Score"
)

st.plotly_chart(
    fig_soil,
    use_container_width=True
)

st.dataframe(
    soil_df,
    use_container_width=True
)

# =====================================================
# SEASON SUSTAINABILITY
# =====================================================

st.subheader("📅 Season Sustainability")

season_df = season_sustainability_summary(
    filtered_df
)

fig_season = px.bar(
    season_df,
    x="Season",
    y="Sustainability_Score",
    color="Sustainability_Score"
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)

st.dataframe(
    season_df,
    use_container_width=True
)

# =====================================================
# IRRIGATION SUSTAINABILITY
# =====================================================

st.subheader("💧 Irrigation Sustainability")

irrigation_df = irrigation_sustainability_summary(
    filtered_df
)

fig_irrigation = px.bar(
    irrigation_df,
    x="Irrigation_Type",
    y="Sustainability_Score",
    color="Sustainability_Score"
)

st.plotly_chart(
    fig_irrigation,
    use_container_width=True
)

st.dataframe(
    irrigation_df,
    use_container_width=True
)

# =====================================================
# PARETO ANALYSIS
# =====================================================

st.subheader("📈 Sustainability Pareto Analysis")

pareto_df = sustainability_pareto_analysis(
    filtered_df
)

fig_pareto = go.Figure()

fig_pareto.add_trace(
    go.Bar(
        x=pareto_df["Crop_Type"],
        y=pareto_df["Sustainability_Score"],
        name="Sustainability"
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
        title="Score"
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

st.subheader("🔥 Crop × Soil Sustainability")

heat1 = crop_soil_sustainability_heatmap(
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

st.subheader("🔥 Crop × Irrigation Sustainability")

heat2 = crop_irrigation_sustainability_heatmap(
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

st.subheader("🔥 Season × Crop Sustainability")

heat3 = season_crop_sustainability_heatmap(
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
# SUSTAINABILITY LEADERBOARD
# =====================================================

st.subheader("🏆 Sustainability Leaderboard")

ranking_df = sustainability_ranking(
    filtered_df
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("💡 Sustainability Insights")

best_crop = crop_df.iloc[0]["Crop_Type"]

best_soil = soil_df.iloc[0]["Soil_Type"]

best_season = season_df.iloc[0]["Season"]

best_irrigation = irrigation_df.iloc[0]["Irrigation_Type"]

st.success(
    f"Most Sustainable Crop: {best_crop}"
)

st.success(
    f"Most Sustainable Soil: {best_soil}"
)

st.success(
    f"Most Sustainable Season: {best_season}"
)

st.success(
    f"Most Sustainable Irrigation Method: {best_irrigation}"
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = crop_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Sustainability Report",
    data=csv,
    file_name="sustainability_analytics.csv",
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
    "Agriculture Analytics Dashboard | Sustainability Analytics"
)
