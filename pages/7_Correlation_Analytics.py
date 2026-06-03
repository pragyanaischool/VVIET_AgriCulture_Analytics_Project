import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.data_loader import load_data

from modules.correlation_analysis import (

    pearson_correlation,

    spearman_correlation,

    kendall_correlation,

    pairwise_pearson,

    pairwise_spearman,

    pairwise_kendall,

    correlation_pvalues,

    strong_positive_correlations,

    strong_negative_correlations,

    top_correlations,

    yield_dependency_analysis,

    resource_dependency_analysis,

    crop_correlation_analysis,

    correlation_summary

)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Correlation Analytics",
    page_icon="🔗",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = load_data()

numeric_df = df.select_dtypes(
    include="number"
)

# =====================================================
# TITLE
# =====================================================

st.title("🔗 Correlation Analytics Dashboard")

st.markdown("""
Analyze relationships between yield,
water usage, fertilizer consumption,
pesticide utilization and other
agricultural variables.
""")

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

summary = correlation_summary(df)

st.subheader("📊 Correlation KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Numeric Variables",
        summary["Numeric Variables"]
    )

with c2:
    st.metric(
        "Average Correlation",
        summary["Average Correlation"]
    )

with c3:
    st.metric(
        "Strong Positive Pairs",
        summary["Strong Positive Pairs"]
    )

with c4:
    st.metric(
        "Strong Negative Pairs",
        summary["Strong Negative Pairs"]
    )

# =====================================================
# CORRELATION METHOD
# =====================================================

analysis_type = st.selectbox(
    "Select Correlation Method",
    [
        "Pearson",
        "Spearman",
        "Kendall"
    ]
)

# =====================================================
# CORRELATION MATRIX
# =====================================================

if analysis_type == "Pearson":
    corr_matrix = pearson_correlation(df)

elif analysis_type == "Spearman":
    corr_matrix = spearman_correlation(df)

else:
    corr_matrix = kendall_correlation(df)

# =====================================================
# HEATMAP
# =====================================================

st.subheader(
    f"🔥 {analysis_type} Correlation Heatmap"
)

fig_heat = px.imshow(
    corr_matrix,
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="RdBu_r"
)

fig_heat.update_layout(
    height=700
)

st.plotly_chart(
    fig_heat,
    use_container_width=True
)

# =====================================================
# CORRELATION MATRIX TABLE
# =====================================================

st.subheader(
    f"📋 {analysis_type} Correlation Matrix"
)

st.dataframe(
    corr_matrix.round(4),
    use_container_width=True
)

# =====================================================
# PAIRWISE CORRELATIONS
# =====================================================

st.subheader(
    "📈 Pairwise Correlation Analysis"
)

if analysis_type == "Pearson":
    pairwise_df = pairwise_pearson(df)

elif analysis_type == "Spearman":
    pairwise_df = pairwise_spearman(df)

else:
    pairwise_df = pairwise_kendall(df)

st.dataframe(
    pairwise_df,
    use_container_width=True
)

# =====================================================
# TOP CORRELATIONS
# =====================================================

st.subheader(
    "🏆 Top Correlated Variables"
)

top_corr_df = top_correlations(
    df,
    top_n=20
)

st.dataframe(
    top_corr_df,
    use_container_width=True
)

# =====================================================
# STRONG POSITIVE
# =====================================================

st.subheader(
    "📈 Strong Positive Correlations"
)

positive_df = strong_positive_correlations(
    df,
    threshold=0.70
)

if len(positive_df) > 0:

    st.dataframe(
        positive_df,
        use_container_width=True
    )

else:

    st.info(
        "No strong positive correlations found."
    )

# =====================================================
# STRONG NEGATIVE
# =====================================================

st.subheader(
    "📉 Strong Negative Correlations"
)

negative_df = strong_negative_correlations(
    df,
    threshold=-0.70
)

if len(negative_df) > 0:

    st.dataframe(
        negative_df,
        use_container_width=True
    )

else:

    st.info(
        "No strong negative correlations found."
    )

# =====================================================
# P-VALUE ANALYSIS
# =====================================================

st.subheader(
    "🧪 Statistical Significance (P-Values)"
)

pvalue_df = correlation_pvalues(df)

st.dataframe(
    pvalue_df,
    use_container_width=True
)

# =====================================================
# YIELD DEPENDENCY
# =====================================================

st.subheader(
    "🌾 Yield Dependency Analysis"
)

yield_df = yield_dependency_analysis(df)

st.dataframe(
    yield_df,
    use_container_width=True
)

fig_yield = px.bar(
    yield_df,
    x="Feature",
    y="Correlation_With_Yield",
    color="Correlation_With_Yield",
    title="Feature Correlation With Yield"
)

st.plotly_chart(
    fig_yield,
    use_container_width=True
)

# =====================================================
# RESOURCE DEPENDENCY
# =====================================================

st.subheader(
    "💧 Resource Dependency Analysis"
)

resource_df = resource_dependency_analysis(df)

fig_resource = px.imshow(
    resource_df,
    text_auto=".2f",
    aspect="auto"
)

st.plotly_chart(
    fig_resource,
    use_container_width=True
)

st.dataframe(
    resource_df,
    use_container_width=True
)

# =====================================================
# SCATTER MATRIX
# =====================================================

st.subheader(
    "🔍 Scatter Matrix Analysis"
)

scatter_columns = st.multiselect(
    "Select Variables",
    numeric_df.columns.tolist(),
    default=numeric_df.columns.tolist()[:4]
)

if len(scatter_columns) >= 2:

    fig_scatter = px.scatter_matrix(
        numeric_df,
        dimensions=scatter_columns
    )

    fig_scatter.update_layout(
        height=800
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# =====================================================
# FEATURE RELATIONSHIP
# =====================================================

st.subheader(
    "📊 Variable Relationship Explorer"
)

col1, col2 = st.columns(2)

with col1:

    x_axis = st.selectbox(
        "X Variable",
        numeric_df.columns,
        index=0
    )

with col2:

    y_axis = st.selectbox(
        "Y Variable",
        numeric_df.columns,
        index=1
    )

fig_relation = px.scatter(
    df,
    x=x_axis,
    y=y_axis,
    trendline="ols",
    title=f"{x_axis} vs {y_axis}"
)

st.plotly_chart(
    fig_relation,
    use_container_width=True
)

# =====================================================
# CROP-WISE CORRELATION
# =====================================================

st.subheader(
    "🌾 Crop-wise Correlation Analysis"
)

crop_results = crop_correlation_analysis(df)

selected_crop = st.selectbox(
    "Select Crop",
    list(crop_results.keys())
)

if selected_crop in crop_results:

    crop_corr = crop_results[
        selected_crop
    ]

    fig_crop = px.imshow(
        crop_corr,
        text_auto=".2f",
        aspect="auto",
        title=f"{selected_crop} Correlation Matrix"
    )

    st.plotly_chart(
        fig_crop,
        use_container_width=True
    )

# =====================================================
# CORRELATION NETWORK
# =====================================================

st.subheader(
    "🕸 Correlation Network Table"
)

network_df = top_correlations(
    df,
    top_n=50
)

network_df = network_df[
    network_df["Abs"] >= 0.30
]

st.dataframe(
    network_df,
    use_container_width=True
)

# =====================================================
# INSIGHTS
# =====================================================

st.subheader(
    "💡 Correlation Insights"
)

highest_corr = top_corr_df.iloc[0]

st.success(
    f"""
Strongest relationship detected between
{highest_corr['Variable 1']}
and
{highest_corr['Variable 2']}
with correlation
{round(highest_corr['Correlation'],4)}
"""
)

if len(negative_df) > 0:

    lowest_corr = negative_df.iloc[0]

    st.warning(
        f"""
Strong negative relationship detected between
{lowest_corr['Variable 1']}
and
{lowest_corr['Variable 2']}
with correlation
{lowest_corr['Correlation']}
"""
    )

# =====================================================
# DOWNLOAD
# =====================================================

csv = pairwise_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Correlation Report",
    data=csv,
    file_name="correlation_analysis.csv",
    mime="text/csv"
)

# =====================================================
# RAW DATA
# =====================================================

with st.expander(
    "View Dataset"
):

    st.dataframe(
        df,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Correlation Analytics"
)
