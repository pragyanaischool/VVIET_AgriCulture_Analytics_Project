import pandas as pd
import io
from fpdf import FPDF

# =====================================================
# SAFE TEXT
# =====================================================

def safe_text(value):

    if value is None:
        return "N/A"

    text = str(value)

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")

    return text[:2000]

# =====================================================
# CSV EXPORT
# =====================================================

def export_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")

# =====================================================
# EXCEL EXPORT
# =====================================================

def export_excel(df):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Analytics",
            index=False
        )

    output.seek(0)

    return output.getvalue()

# =====================================================
# PDF CLASS
# =====================================================

class AgriculturePDF(FPDF):

    def header(self):

        self.set_font(
            "Helvetica",
            "B",
            16
        )

        self.cell(
            0,
            10,
            "Agriculture Analytics Report",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )

        self.ln(5)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "I",
            8
        )

        self.cell(
            0,
            10,
            f"Page {self.page_no()}",
            align="C"
        )

# =====================================================
# PDF REPORT
# =====================================================

def create_pdf_report(
    title,
    summary=None,
    insights=None,
    dataframe=None
):

    pdf = AgriculturePDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    # -----------------------------------------
    # Title
    # -----------------------------------------

    pdf.set_font(
        "Helvetica",
        "B",
        14
    )

    pdf.multi_cell(
        180,
        8,
        safe_text(title)
    )

    pdf.ln(3)

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    if summary:

        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Executive Summary",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        if isinstance(summary, dict):

            for k, v in summary.items():

                pdf.multi_cell(
                    180,
                    6,
                    f"{safe_text(k)} : {safe_text(v)}"
                )

        else:

            pdf.multi_cell(
                180,
                6,
                safe_text(summary)
            )

        pdf.ln(3)

    # -----------------------------------------
    # Insights
    # -----------------------------------------

    if insights:

        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Insights",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        if isinstance(insights, list):

            for item in insights:

                pdf.multi_cell(
                    180,
                    6,
                    f"- {safe_text(item)}"
                )

        elif isinstance(insights, dict):

            for k, v in insights.items():

                pdf.multi_cell(
                    180,
                    6,
                    f"{safe_text(k)} : {safe_text(v)}"
                )

        else:

            pdf.multi_cell(
                180,
                6,
                safe_text(insights)
            )

        pdf.ln(3)

    # -----------------------------------------
    # Data Snapshot
    # -----------------------------------------

    if dataframe is not None and len(dataframe) > 0:

        pdf.set_font(
            "Helvetica",
            "B",
            12
        )

        pdf.cell(
            0,
            8,
            "Data Snapshot",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        pdf.set_font(
            "Helvetica",
            "",
            8
        )

        preview = dataframe.head(20)

        for _, row in preview.iterrows():

            row_text = " | ".join(
                [
                    safe_text(v)
                    for v in row.values
                ]
            )

            pdf.multi_cell(
                180,
                5,
                row_text
            )

    pdf_bytes = bytes(
        pdf.output()
    )

    return pdf_bytes

# =====================================================
# REPORT PACKAGE
# =====================================================

def generate_complete_report(
    title,
    summary,
    insights,
    dataframe
):

    return {

        "csv":
        export_csv(dataframe),

        "excel":
        export_excel(dataframe),

        "pdf":
        create_pdf_report(
            title,
            summary,
            insights,
            dataframe
        )

    }

# =====================================================
# KPI REPORT
# =====================================================

def create_kpi_report(
    kpi_dict
):

    return pd.DataFrame({

        "Metric":
        list(kpi_dict.keys()),

        "Value":
        list(kpi_dict.values())

    })

# =====================================================
# SUMMARY REPORT
# =====================================================

def create_summary_report(
    df
):

    return {

        "Rows":
        len(df),

        "Columns":
        len(df.columns),

        "Missing Values":
        int(
            df.isna().sum().sum()
        ),

        "Duplicate Rows":
        int(
            df.duplicated().sum()
        )

    }

