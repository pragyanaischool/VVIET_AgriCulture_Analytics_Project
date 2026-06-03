import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.water_analytics import (
    crop_water_efficiency
)

from modules.fertilizer_analytics import (
    crop_fertilizer_efficiency
)

from modules.pesticide_analytics import (
    crop_pesticide_efficiency
)

from modules.sustainability_analytics import (

    resource_intensity_score,

    sustainability_score,

    water_sustainability_score,

    fertilizer_sustainability_score,

    pesticide_sustainability_score,

    carbon_footprint,

    carbon_per_yield,

    esg_agriculture_score,

    crop_sustainability_summary

)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Resource Efficiency",
    page_icon="⚡",
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

st.title("⚡ Resource Efficiency Dashboard")

st.markdown("""
Comprehensive analysis of resource utilization,
efficiency, sustainability, productivity,
and ESG performance across agricultural operations.
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
# RESOURCE KPIs
# =====================================================

total_yield = filtered_df["Yield_tons"].sum()

total_water = filtered_df[
    "Water_Usage_cubic_meters"
].sum()

total_fertilizer = filtered_df[
    "Fertilizer_Used_tons"
].sum()

total_pesticide = filtered_df[
    "Pesticide_Used_kg"
].sum()

water_productivity = round(
    total_yield / total_water,
    4
)

fert_efficiency = round(
    total_yield / total_fertilizer,
    4
)

pest_efficiency = round(
    total_yield / total_pesticide,
    4
)

# =====================================================
# KPI SECTION
# =====================================================

st.subheader("📊 Resource Efficiency KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Water Productivity",
        water_productivity
    )

with c2:
    st.metric(
        "Fertilizer Efficiency",
        fert_efficiency
    )

with c3:
    st.metric(
        "Pesticide Efficiency",
        pest_efficiency
    )

with c4:
    st.metric(
        "Yield",
        round(total_yield, 2)
    )

# =====================================================
# SUSTAINABILITY KPIs
# =====================================================

st.subheader("🌱 Sustainability Scorecard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Resource Intensity",
        resource_intensity_score(filtered_df)
    )

with c2:
    st.metric(
        "Sustainability Score",
        sustainability_score(filtered_df)
    )

with c3:
    st.metric(
        "Carbon / Yield",
        carbon_per_yield(filtered_df)
    )

with c4:
    st.metric(
        "ESG Score",
        esg_agriculture_score(filtered_df)
    )

# =====================================================
# RESOURCE SCORECARD
# =====================================================

st.subheader("🏆 Resource Scorecard")

scorecard = pd.DataFrame({

    "Metric": [

        "Water Sustainability",

        "Fertilizer Sustainability",

        "Pesticide Sustainability",

        "Overall Sustainability"

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
        )

    ]
})

st.dataframe(
    scorecard,
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

        total_water,

        total_fertilizer,

        total_pesticide

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
# WATER EFFICIENCY
# =====================================================

st.subheader("💧 Water Efficiency")

water_df = crop_water_efficiency(
    filtered_df
)

st.dataframe(
    water_df,
    use_container_width=True
)

fig_water = px.bar(
    water_df,
    x="Crop_Type",
    y="Water_Efficiency",
    color="Water_Efficiency",
    title="Crop Water Efficiency"
)

st.plotly_chart(
    fig_water,
    use_container_width=True
)

# =====================================================
# FERTILIZER EFFICIENCY
# =====================================================

st.subheader("🧪 Fertilizer Efficiency")

fert_df = crop_fertilizer_efficiency(
    filtered_df
)

st.dataframe(
    fert_df,
    use_container_width=True
)

fig_fert = px.bar(
    fert_df,
    x="Crop_Type",
    y="Fertilizer_Efficiency",
    color="Fertilizer_Efficiency",
    title="Crop Fertilizer Efficiency"
)

st.plotly_chart(
    fig_fert,
    use_container_width=True
)

# =====================================================
# PESTICIDE EFFICIENCY
# =====================================================

st.subheader("☘️ Pesticide Efficiency")

pest_df = crop_pesticide_efficiency(
    filtered_df
)

st.dataframe(
    pest_df,
    use_container_width=True
)

fig_pest = px.bar(
    pest_df,
    x="Crop_Type",
    y="Pesticide_Efficiency",
    color="Pesticide_Efficiency",
    title="Crop Pesticide Efficiency"
)

st.plotly_chart(
    fig_pest,
    use_container_width=True
)

# =====================================================
# SUSTAINABILITY RANKING
# =====================================================

st.subheader("🌾 Crop Sustainability Ranking")

sustain_df = crop_sustainability_summary(
    filtered_df
)

st.dataframe(
    sustain_df,
    use_container_width=True
)

fig_sustain = px.bar(
    sustain_df.head(15),
    x="Crop_Type",
    y="Sustainability_Score",
    color="Sustainability_Score",
    title="Crop Sustainability Ranking"
)

st.plotly_chart(
    fig_sustain,
    use_container_width=True
)

# =====================================================
# RESOURCE HEATMAP
# =====================================================

st.subheader("🔥 Resource Efficiency Heatmap")

heatmap_df = sustain_df[

    [

        "Crop_Type",

        "Water",

        "Fertilizer",

        "Pesticide",

        "Sustainability_Score"

    ]

].set_index("Crop_Type")

fig_heat = px.imshow(
    heatmap_df,
    text_auto=".2f",
    aspect="auto",
    title="Resource Efficiency Heatmap"
)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)

# =====================================================
# ESG ANALYTICS
# =====================================================

st.subheader("🌍 ESG Analytics")

esg_df = pd.DataFrame({

    "Metric": [

        "Carbon Footprint",

        "Carbon / Yield",

        "ESG Score"

    ],

    "Value": [

        carbon_footprint(
            filtered_df
        ),

        carbon_per_yield(
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
    y="Value",
    color="Value",
    title="ESG Indicators"
)

st.plotly_chart(
    fig_esg,
    use_container_width=True
)

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("💡 Executive Insights")

best_water_crop = water_df.iloc[0]["Crop_Type"]

best_fert_crop = fert_df.iloc[0]["Crop_Type"]

best_pest_crop = pest_df.iloc[0]["Crop_Type"]

best_sustain_crop = sustain_df.iloc[0]["Crop_Type"]

st.success(
    f"Highest Water Efficiency Crop: {best_water_crop}"
)

st.success(
    f"Highest Fertilizer Efficiency Crop: {best_fert_crop}"
)

st.success(
    f"Highest Pesticide Efficiency Crop: {best_pest_crop}"
)

st.success(
    f"Most Sustainable Crop: {best_sustain_crop}"
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = sustain_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Resource Efficiency Report",
    data=csv,
    file_name="resource_efficiency.csv",
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
    "Agriculture Analytics Dashboard | Resource Efficiency"
)
