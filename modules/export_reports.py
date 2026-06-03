import pandas as pd
import numpy as np
import io
from datetime import datetime

from fpdf import FPDF


# =====================================================
# EXPORT DATAFRAME TO CSV
# =====================================================

def dataframe_to_csv(df):

    return df.to_csv(
        index=False
    ).encode("utf-8")


# =====================================================
# EXCEL EXPORT
# =====================================================

def create_excel_report(

    df,

    kpi_summary=None,

    statistics_summary=None,

    crop_summary=None,

    water_summary=None,

    fertilizer_summary=None,

    pesticide_summary=None,

    sustainability_summary=None

):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        # ==========================================
        # RAW DATA
        # ==========================================

        df.to_excel(

            writer,

            sheet_name="Raw Data",

            index=False

        )

        # ==========================================
        # KPI SUMMARY
        # ==========================================

        if kpi_summary is not None:

            pd.DataFrame(

                list(kpi_summary.items()),

                columns=["Metric", "Value"]

            ).to_excel(

                writer,

                sheet_name="KPI Summary",

                index=False

            )

        # ==========================================
        # STATISTICS
        # ==========================================

        if statistics_summary is not None:

            statistics_summary.to_excel(

                writer,

                sheet_name="Statistics"

            )

        # ==========================================
        # CROP SUMMARY
        # ==========================================

        if crop_summary is not None:

            crop_summary.to_excel(

                writer,

                sheet_name="Crop Analytics",

                index=False

            )

        # ==========================================
        # WATER SUMMARY
        # ==========================================

        if water_summary is not None:

            water_summary.to_excel(

                writer,

                sheet_name="Water Analytics",

                index=False

            )

        # ==========================================
        # FERTILIZER SUMMARY
        # ==========================================

        if fertilizer_summary is not None:

            fertilizer_summary.to_excel(

                writer,

                sheet_name="Fertilizer Analytics",

                index=False

            )

        # ==========================================
        # PESTICIDE SUMMARY
        # ==========================================

        if pesticide_summary is not None:

            pesticide_summary.to_excel(

                writer,

                sheet_name="Pesticide Analytics",

                index=False

            )

        # ==========================================
        # SUSTAINABILITY
        # ==========================================

        if sustainability_summary is not None:

            pd.DataFrame(

                list(
                    sustainability_summary.items()
                ),

                columns=[
                    "Metric",
                    "Value"
                ]

            ).to_excel(

                writer,

                sheet_name="Sustainability",

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

            "Arial",

            "B",

            16

        )

        self.cell(

            0,

            10,

            "Agriculture Analytics Report",

            ln=True,

            align="C"

        )

        self.ln(5)

    def footer(self):

        self.set_y(-15)

        self.set_font(

            "Arial",

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
# PDF EXECUTIVE REPORT
# =====================================================

def create_pdf_report(

    executive_summary,

    recommendations=None,

    alerts=None

):

    pdf = AgriculturePDF()

    pdf.add_page()

    pdf.set_font(

        "Arial",

        size=12

    )

    # ==========================================
    # REPORT DATE
    # ==========================================

    pdf.cell(

        0,

        10,

        f"Generated: {datetime.now()}",

        ln=True

    )

    pdf.ln(5)

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    pdf.set_font(

        "Arial",

        "B",

        12

    )

    pdf.cell(

        0,

        10,

        "Executive Summary",

        ln=True

    )

    pdf.set_font(

        "Arial",

        size=11

    )

    pdf.multi_cell(

        0,

        8,

        executive_summary

    )

    pdf.ln(5)

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================

    if recommendations:

        pdf.set_font(

            "Arial",

            "B",

            12

        )

        pdf.cell(

            0,

            10,

            "Recommendations",

            ln=True

        )

        pdf.set_font(

            "Arial",

            size=11

        )

        for item in recommendations:

            pdf.multi_cell(

                0,

                8,

                f"- {item}"

            )

    pdf.ln(5)

    # ==========================================
    # ALERTS
    # ==========================================

    if alerts:

        pdf.set_font(

            "Arial",

            "B",

            12

        )

        pdf.cell(

            0,

            10,

            "Alerts",

            ln=True

        )

        pdf.set_font(

            "Arial",

            size=11

        )

        for item in alerts:

            pdf.multi_cell(

                0,

                8,

                f"- {item}"

            )

    return bytes(
        pdf.output(dest="S")
    )


# =====================================================
# KPI REPORT DATAFRAME
# =====================================================

def create_kpi_dataframe(

    kpi_summary

):

    return pd.DataFrame(

        list(kpi_summary.items()),

        columns=[

            "Metric",

            "Value"

        ]

    )


# =====================================================
# EXECUTIVE REPORT
# =====================================================

def executive_report_dataframe(

    total_farms,

    total_yield,

    total_water,

    total_fertilizer,

    total_pesticide

):

    report = pd.DataFrame({

        "Metric": [

            "Total Farms",

            "Total Yield",

            "Total Water",

            "Total Fertilizer",

            "Total Pesticide"

        ],

        "Value": [

            total_farms,

            total_yield,

            total_water,

            total_fertilizer,

            total_pesticide

        ]

    })

    return report


# =====================================================
# EXPORT SUMMARY TABLE
# =====================================================

def summary_table_to_excel(

    dataframe

):

    output = io.BytesIO()

    with pd.ExcelWriter(

        output,

        engine="xlsxwriter"

    ) as writer:

        dataframe.to_excel(

            writer,

            index=False

        )

    output.seek(0)

    return output.getvalue()


# =====================================================
# REPORT METADATA
# =====================================================

def report_metadata():

    return {

        "Generated On":

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Application":

        "Agriculture Analytics Dashboard",

        "Version":

        "1.0"

    }


# =====================================================
# COMPLETE EXPORT PACKAGE
# =====================================================

def complete_export_package(

    df,

    executive_summary,

    recommendations,

    alerts,

    kpi_summary,

    statistics_summary,

    crop_summary,

    water_summary,

    fertilizer_summary,

    pesticide_summary,

    sustainability_summary

):

    excel_file = create_excel_report(

        df=df,

        kpi_summary=kpi_summary,

        statistics_summary=statistics_summary,

        crop_summary=crop_summary,

        water_summary=water_summary,

        fertilizer_summary=fertilizer_summary,

        pesticide_summary=pesticide_summary,

        sustainability_summary=sustainability_summary

    )

    pdf_file = create_pdf_report(

        executive_summary,

        recommendations,

        alerts

    )

    return {

        "excel": excel_file,

        "pdf": pdf_file

    }
