import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.yield_analytics import (
    pareto_yield_analysis
)

from modules.water_analytics import (
    water_pareto_analysis
)

from modules.fertilizer_analytics import (
    fertilizer_pareto_analysis
)

from modules.pesticide_analytics import (
    pesticide_pareto_analysis
)

from modules.sustainability_analytics import (
    sustainability_pareto_analysis,
    crop_sustainability_summary
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Pareto Analytics",
    page_icon="📈",
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

st.title("📈 Pareto Analytics Dashboard")

st.markdown("""
Identify the critical few crops that contribute
to the majority of yield, water consumption,
fertilizer usage, pesticide usage and sustainability.
Based on the 80/20 Pareto Principle.
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
# PARETO FUNCTION
# =====================================================

def create_pareto_chart(
    dataframe,
    category_col,
    value_col,
    cumulative_col,
    title
):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=dataframe[category_col],
            y=dataframe[value_col],
            name=value_col
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dataframe[category_col],
            y=dataframe[cumulative_col],
            yaxis="y2",
            mode="lines+markers",
            name="Cumulative %"
        )
    )

    fig.add_hline(
        y=80,
        line_dash="dash"
    )

    fig.update_layout(

        title=title,

        yaxis=dict(
            title=value_col
        ),

        yaxis2=dict(
            title="Cumulative %",
            overlaying="y",
            side="right",
            range=[0, 100]
        ),

        height=600
    )

    return fig

# =====================================================
# KPI SUMMARY
# =====================================================

st.subheader("📊 Pareto KPI Summary")

yield_pareto = pareto_yield_analysis(
    filtered_df
)

water_pareto = water_pareto_analysis(
    filtered_df
)

fert_pareto = fertilizer_pareto_analysis(
    filtered_df
)

pest_pareto = pesticide_pareto_analysis(
    filtered_df
)

sustain_pareto = sustainability_pareto_analysis(
    filtered_df
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Crops",
        filtered_df["Crop_Type"].nunique()
    )

with c2:
    st.metric(
        "Yield Leaders",
        len(
            yield_pareto[
                yield_pareto["Cumulative_%"] <= 80
            ]
        )
    )

with c3:
    st.metric(
        "Water Leaders",
        len(
            water_pareto[
                water_pareto["Cumulative_%"] <= 80
            ]
        )
    )

with c4:
    st.metric(
        "Sustainability Leaders",
        len(
            sustain_pareto[
                sustain_pareto["Cumulative_%"] <= 80
            ]
        )
    )

# =====================================================
# YIELD PARETO
# =====================================================

st.subheader("🌾 Yield Pareto Analysis")

st.plotly_chart(
    create_pareto_chart(
        yield_pareto,
        "Crop_Type",
        "Yield_tons",
        "Cumulative_%",
        "Yield Pareto Analysis"
    ),
    use_container_width=True
)

st.dataframe(
    yield_pareto,
    use_container_width=True
)

# =====================================================
# WATER PARETO
# =====================================================

st.subheader("💧 Water Pareto Analysis")

st.plotly_chart(
    create_pareto_chart(
        water_pareto,
        "Crop_Type",
        "Water_Usage_cubic_meters",
        "Cumulative_%",
        "Water Pareto Analysis"
    ),
    use_container_width=True
)

st.dataframe(
    water_pareto,
    use_container_width=True
)

# =====================================================
# FERTILIZER PARETO
# =====================================================

st.subheader("🧪 Fertilizer Pareto Analysis")

st.plotly_chart(
    create_pareto_chart(
        fert_pareto,
        "Crop_Type",
        "Fertilizer_Used_tons",
        "Cumulative_%",
        "Fertilizer Pareto Analysis"
    ),
    use_container_width=True
)

st.dataframe(
    fert_pareto,
    use_container_width=True
)

# =====================================================
# PESTICIDE PARETO
# =====================================================

st.subheader("☘️ Pesticide Pareto Analysis")

st.plotly_chart(
    create_pareto_chart(
        pest_pareto,
        "Crop_Type",
        "Pesticide_Used_kg",
        "Cumulative_%",
        "Pesticide Pareto Analysis"
    ),
    use_container_width=True
)

st.dataframe(
    pest_pareto,
    use_container_width=True
)

# =====================================================
# SUSTAINABILITY PARETO
# =====================================================

st.subheader("🌱 Sustainability Pareto Analysis")

st.plotly_chart(
    create_pareto_chart(
        sustain_pareto,
        "Crop_Type",
        "Sustainability_Score",
        "Cumulative_%",
        "Sustainability Pareto Analysis"
    ),
    use_container_width=True
)

st.dataframe(
    sustain_pareto,
    use_container_width=True
)

# =====================================================
# TOP CONTRIBUTORS
# =====================================================

st.subheader("🏆 Top Contributing Crops")

leaderboard = pd.DataFrame({

    "Yield Leader":
    yield_pareto.iloc[0]["Crop_Type"],

    "Water Leader":
    water_pareto.iloc[0]["Crop_Type"],

    "Fertilizer Leader":
    fert_pareto.iloc[0]["Crop_Type"],

    "Pesticide Leader":
    pest_pareto.iloc[0]["Crop_Type"],

    "Sustainability Leader":
    sustain_pareto.iloc[0]["Crop_Type"]

}, index=[0])

st.dataframe(
    leaderboard,
    use_container_width=True
)

# =====================================================
# RESOURCE OPTIMIZATION
# =====================================================

st.subheader("⚡ Resource Optimization Insights")

top_yield_crop = yield_pareto.iloc[0]["Crop_Type"]

top_sustain_crop = sustain_pareto.iloc[0]["Crop_Type"]

highest_water_crop = water_pareto.iloc[0]["Crop_Type"]

highest_fert_crop = fert_pareto.iloc[0]["Crop_Type"]

highest_pest_crop = pest_pareto.iloc[0]["Crop_Type"]

st.success(
    f"Highest Yield Contributor: {top_yield_crop}"
)

st.success(
    f"Most Sustainable Crop: {top_sustain_crop}"
)

st.warning(
    f"Highest Water Consumer: {highest_water_crop}"
)

st.warning(
    f"Highest Fertilizer Consumer: {highest_fert_crop}"
)

st.warning(
    f"Highest Pesticide Consumer: {highest_pest_crop}"
)

# =====================================================
# EXECUTIVE RECOMMENDATIONS
# =====================================================

st.subheader("💡 Executive Recommendations")

recommendations = [

    "Focus on top 20% crops generating 80% of total yield.",

    "Optimize water allocation to high-yield crops.",

    "Reduce fertilizer usage on low-performing crops.",

    "Monitor pesticide-heavy crops for sustainability improvements.",

    "Expand cultivation of highly sustainable crops.",

    "Use Pareto analysis regularly for resource optimization."

]

for rec in recommendations:
    st.success(rec)

# =====================================================
# SUSTAINABILITY VS YIELD
# =====================================================

st.subheader("🎯 Yield vs Sustainability")

crop_sustain = crop_sustainability_summary(
    filtered_df
)

fig = px.scatter(
    crop_sustain,
    x="Total_Yield",
    y="Sustainability_Score",
    color="Crop_Type",
    size="Total_Yield",
    hover_name="Crop_Type",
    title="Yield vs Sustainability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = yield_pareto.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Pareto Report",
    data=csv,
    file_name="pareto_analytics.csv",
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
    "Agriculture Analytics Dashboard | Pareto Analytics"
)
