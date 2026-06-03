import streamlit as st

st.set_page_config(
    page_title="Agriculture Analytics Dashboard",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Agriculture Analytics Dashboard")

st.markdown("""
## Enterprise Agriculture Intelligence Platform

Analyze:

- Crop Productivity
- Yield Optimization
- Water Usage
- Fertilizer Consumption
- Pesticide Utilization
- Sustainability Metrics
- ESG Performance
- Statistical Analytics
- Business Intelligence
- Executive Reporting
""")

st.info(
    "Use the navigation menu on the left to access all analytics modules."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Dashboards",
        "13"
    )

with col2:
    st.metric(
        "Analytics Modules",
        "11"
    )

with col3:
    st.metric(
        "Visualizations",
        "100+"
    )

with col4:
    st.metric(
        "Reports",
        "PDF/Excel/CSV"
    )

st.markdown("---")

st.subheader("Available Modules")

modules = [
    "Executive Dashboard",
    "Statistical Analytics",
    "Yield Analytics",
    "Water Analytics",
    "Fertilizer Analytics",
    "Pesticide Analytics",
    "Correlation Analytics",
    "Resource Efficiency",
    "Sustainability Analytics",
    "Seasonal Analytics",
    "Pareto Analytics",
    "Advanced Visualizations",
    "Report Center"
]

for module in modules:
    st.write(f"✅ {module}")

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Streamlit + Plotly + Statistics + Sustainability"
)
