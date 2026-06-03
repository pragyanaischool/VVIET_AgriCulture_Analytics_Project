
import streamlit as st
import pandas as pd

from modules.data_loader import (
    load_data,
    create_derived_metrics
)

from modules.export_reports import (
    export_csv,
    export_excel,
    create_pdf_report,
    create_summary_report
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

st.title("📄 Report Center")

st.markdown("""
Generate and download Agriculture Analytics reports
in CSV, Excel and PDF formats.
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
# SUMMARY
# =====================================================

summary = create_summary_report(
    filtered_df
)

st.subheader("Dataset Summary")

summary_df = pd.DataFrame({

    "Metric": summary.keys(),

    "Value": summary.values()

})

st.dataframe(
    summary_df,
    use_container_width=True
)

# =====================================================
# PREVIEW
# =====================================================

st.subheader("Data Preview")

st.dataframe(
    filtered_df.head(50),
    use_container_width=True
)

# =====================================================
# CSV DOWNLOAD
# =====================================================

csv_data = export_csv(
    filtered_df
)

st.download_button(
    label="📥 Download CSV Report",
    data=csv_data,
    file_name="agriculture_report.csv",
    mime="text/csv"
)

# =====================================================
# EXCEL DOWNLOAD
# =====================================================

excel_data = export_excel(
    filtered_df
)

st.download_button(
    label="📊 Download Excel Report",
    data=excel_data,
    file_name="agriculture_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =====================================================
# PDF DOWNLOAD
# =====================================================

pdf_data = create_pdf_report(

    title="Agriculture Analytics Report",

    summary=summary,

    insights=[
        "Agriculture analytics summary report",
        "Generated from filtered dashboard data",
        f"Total records: {len(filtered_df)}"
    ],

    dataframe=filtered_df

)

st.download_button(
    label="📄 Download PDF Report",
    data=pdf_data,
    file_name="agriculture_report.pdf",
    mime="application/pdf"
)

# =====================================================
# REPORT INFO
# =====================================================

st.subheader("Report Information")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Records",
        len(filtered_df)
    )

with c2:
    st.metric(
        "Columns",
        len(filtered_df.columns)
    )

with c3:
    st.metric(
        "Crop Types",
        filtered_df["Crop_Type"].nunique()
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Agriculture Analytics Dashboard | Report Center"
)

