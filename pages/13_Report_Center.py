import streamlit as st
import pandas as pd
from datetime import datetime

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.kpi_metrics import (
    executive_summary
)

from modules.statistical_analysis import (
    descriptive_statistics
)

from modules.yield_analytics import (
    crop_yield_summary
)

from modules.water_analytics import (
    crop_water_summary
)

from modules.fertilizer_analytics import (
    crop_fertilizer_summary
)

from modules.pesticide_analytics import (
    crop_pesticide_summary
)

from modules.sustainability_analytics import (
    executive_sustainability_summary
)

from modules.business_insights import (
    complete_business_report
)

from modules.export_reports import (

    create_excel_report,

    create_pdf_report,

    complete_export_package,

    create_kpi_dataframe

)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Report Center",
    page_icon="📄",
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

st.title("📄 Agriculture Report Center")

st.markdown("""
Generate executive reports,
export analytics,
download KPI reports,
and share agriculture intelligence insights.
""")

# =====================================================
# FILTERS
# =====================================================

st.sidebar.header("Report Filters")

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
# REPORT OVERVIEW
# =====================================================

st.subheader("📊 Report Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Records",
        len(filtered_df)
    )

with c2:
    st.metric(
        "Crop Types",
        filtered_df["Crop_Type"].nunique()
    )

with c3:
    st.metric(
        "Seasons",
        filtered_df["Season"].nunique()
    )

with c4:
    st.metric(
        "Generated",
        datetime.now().strftime("%H:%M")
    )

# =====================================================
# KPI SUMMARY
# =====================================================

st.subheader("📈 KPI Summary")

kpi_summary = executive_summary(
    filtered_df
)

kpi_df = create_kpi_dataframe(
    kpi_summary
)

st.dataframe(
    kpi_df,
    use_container_width=True
)

# =====================================================
# STATISTICAL REPORT
# =====================================================

st.subheader("📊 Statistical Summary")

statistics_summary = descriptive_statistics(
    filtered_df
)

st.dataframe(
    statistics_summary,
    use_container_width=True
)

# =====================================================
# ANALYTICS TABLES
# =====================================================

crop_summary = crop_yield_summary(
    filtered_df
)

water_summary = crop_water_summary(
    filtered_df
)

fertilizer_summary = crop_fertilizer_summary(
    filtered_df
)

pesticide_summary = crop_pesticide_summary(
    filtered_df
)

sustainability_summary = (
    executive_sustainability_summary(
        filtered_df
    )
)

# =====================================================
# BUSINESS REPORT
# =====================================================

st.subheader("💡 Executive Insights")

report = complete_business_report(
    filtered_df
)

st.success(
    report["Yield Insight"]
)

st.info(
    report["Water Insight"]
)

st.warning(
    report["Sustainability"]
)

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.subheader("📄 Executive Summary")

st.write(
    report["Executive Summary"]
)

# =====================================================
# RECOMMENDATIONS
# =====================================================

st.subheader("✅ Recommendations")

for rec in report["Recommendations"]:

    st.markdown(
        f"- {rec}"
    )

# =====================================================
# ALERTS
# =====================================================

if len(report["Alerts"]) > 0:

    st.subheader("🚨 Alerts")

    for alert in report["Alerts"]:

        st.error(alert)

# =====================================================
# REPORT TYPE
# =====================================================

st.subheader("📦 Generate Report")

report_type = st.selectbox(

    "Select Report",

    [

        "Executive Report",

        "KPI Report",

        "Statistical Report",

        "Crop Analytics",

        "Water Analytics",

        "Fertilizer Analytics",

        "Pesticide Analytics",

        "Sustainability Analytics",

        "Complete Enterprise Package"

    ]

)

# =====================================================
# KPI REPORT DOWNLOAD
# =====================================================

if report_type == "KPI Report":

    csv = kpi_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download KPI Report",

        csv,

        "kpi_report.csv",

        "text/csv"

    )

# =====================================================
# STATISTICS REPORT
# =====================================================

elif report_type == "Statistical Report":

    csv = statistics_summary.to_csv().encode(
        "utf-8"
    )

    st.download_button(

        "📥 Download Statistics Report",

        csv,

        "statistics_report.csv",

        "text/csv"

    )

# =====================================================
# CROP REPORT
# =====================================================

elif report_type == "Crop Analytics":

    csv = crop_summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Crop Report",

        csv,

        "crop_report.csv",

        "text/csv"

    )

# =====================================================
# WATER REPORT
# =====================================================

elif report_type == "Water Analytics":

    csv = water_summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Water Report",

        csv,

        "water_report.csv",

        "text/csv"

    )

# =====================================================
# FERTILIZER REPORT
# =====================================================

elif report_type == "Fertilizer Analytics":

    csv = fertilizer_summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Fertilizer Report",

        csv,

        "fertilizer_report.csv",

        "text/csv"

    )

# =====================================================
# PESTICIDE REPORT
# =====================================================

elif report_type == "Pesticide Analytics":

    csv = pesticide_summary.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Pesticide Report",

        csv,

        "pesticide_report.csv",

        "text/csv"

    )

# =====================================================
# SUSTAINABILITY REPORT
# =====================================================

elif report_type == "Sustainability Analytics":

    sustain_df = pd.DataFrame(
        list(
            sustainability_summary.items()
        ),
        columns=["Metric", "Value"]
    )

    csv = sustain_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Sustainability Report",

        csv,

        "sustainability_report.csv",

        "text/csv"

    )

# =====================================================
# EXECUTIVE PDF REPORT
# =====================================================

elif report_type == "Executive Report":

    pdf_data = create_pdf_report(

        executive_summary=
        report["Executive Summary"],

        recommendations=
        report["Recommendations"],

        alerts=
        report["Alerts"]

    )

    st.download_button(

        "📄 Download Executive PDF",

        pdf_data,

        "executive_report.pdf",

        "application/pdf"

    )

# =====================================================
# COMPLETE PACKAGE
# =====================================================

elif report_type == "Complete Enterprise Package":

    package = complete_export_package(

        df=filtered_df,

        executive_summary=
        report["Executive Summary"],

        recommendations=
        report["Recommendations"],

        alerts=
        report["Alerts"],

        kpi_summary=
        kpi_summary,

        statistics_summary=
        statistics_summary,

        crop_summary=
        crop_summary,

        water_summary=
        water_summary,

        fertilizer_summary=
        fertilizer_summary,

        pesticide_summary=
        pesticide_summary,

        sustainability_summary=
        sustainability_summary

    )

    st.download_button(

        "📊 Download Complete Excel Package",

        package["excel"],

        "Agriculture_Enterprise_Report.xlsx",

        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )

    st.download_button(

        "📄 Download Executive PDF",

        package["pdf"],

        "Agriculture_Executive_Report.pdf",

        "application/pdf"

    )

# =====================================================
# EXCEL EXPORT
# =====================================================

st.subheader("📊 Excel Export")

excel_data = create_excel_report(

    df=filtered_df,

    kpi_summary=kpi_summary,

    statistics_summary=
    statistics_summary,

    crop_summary=
    crop_summary,

    water_summary=
    water_summary,

    fertilizer_summary=
    fertilizer_summary,

    pesticide_summary=
    pesticide_summary,

    sustainability_summary=
    sustainability_summary

)

st.download_button(

    "📥 Download Complete Excel Report",

    excel_data,

    "Agriculture_Report.xlsx",

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

)

# =====================================================
# DATA PREVIEW
# =====================================================

with st.expander(
    "View Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =====================================================
# REPORT AUDIT
# =====================================================

st.subheader("🕒 Report Audit")

audit_df = pd.DataFrame({

    "Item": [

        "Generated Date",

        "Rows",

        "Columns",

        "Crop Types",

        "Seasons"

    ],

    "Value": [

        datetime.now(),

        filtered_df.shape[0],

        filtered_df.shape[1],

        filtered_df["Crop_Type"].nunique(),

        filtered_df["Season"].nunique()

    ]

})

st.dataframe(
    audit_df,
    use_container_width=True
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Enterprise Report Center"
)
