"""
HarvestSaarthi AI - PDF Report Generator
Generates downloadable HarvestSaarthi_Decision_Report.pdf containing
farmer situation, evaluated options matrix, action plan, and disclaimer.
"""

import io
from typing import Dict, Any
from backend.models.schemas import DecisionResult

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_report(result: DecisionResult) -> bytes:
    """Generates PDF report bytes for the decision result."""
    disclaimer_text = (
        "Disclaimer: AI-generated decision support report. Estimates are based on the HarvestSaarthi "
        "prototype/demo benchmark dataset and are not guarantees of market price, profit, or income. "
        "Verify current market prices, buyer terms, transport availability, and other conditions before taking action."
    )

    if not REPORTLAB_AVAILABLE:
        # Fallback simple text-based PDF format if reportlab is missing
        reasons_text = "\n".join([f"- {r}" for r in result.primary_reasons])
        options_text = "\n".join([f"- {o.title}: Rs. {o.expected_net_realization:,.2f} (Risk: {o.risk_level})" for o in result.options])
        action_text = "\n".join([f"{a.priority}. {a.action} ({a.reason})" for a in result.action_plan])

        text_content = f"""
HARVESTSAARTHI AI - DECISION SUPPORT REPORT
Run ID: {result.run_id} | Date: {result.timestamp}
==================================================

RECOMMENDED MOVE: {result.recommendation_title}
EXPECTED NET REALIZATION: Rs. {result.expected_net_realization:,.2f}
CONFIDENCE SCORE: {result.confidence_score}% | RISK: {result.risk_level}

WHY THIS RECOMMENDATION:
{reasons_text}

OPTIONS EVALUATED:
{options_text}

ACTION PLAN:
{action_text}

DISCLAIMER:
{disclaimer_text}
"""
        return text_content.encode("utf-8")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#065F46"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "SubTitle",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4B5563"),
        spaceAfter=10,
    )
    h2_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#047857"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=3,
    )

    # Table Cell Styles to ensure clean text wrapping
    th_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        textColor=colors.white,
        fontName="Helvetica-Bold",
    )
    td_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1F2937"),
    )
    td_bold_style = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#065F46"),
    )

    story = []

    # Header
    story.append(Paragraph("HARVESTSAARTHI AI", title_style))
    story.append(Paragraph(f"Decision Support Report • Run ID: {result.run_id} • Date: {result.timestamp}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#10B981"), spaceAfter=10))

    # Hero Recommendation Box
    rec_text = f"<b>RECOMMENDED ACTION:</b> {result.recommendation_title}<br/>" \
               f"<b>Expected Net Realization:</b> Rs. {result.expected_net_realization:,.2f}<br/>" \
               f"<b>Confidence Score:</b> {result.confidence_score}% &nbsp;|&nbsp; <b>Risk Level:</b> {result.risk_level}"

    rec_table = Table(
        [[Paragraph(rec_text, ParagraphStyle("Rec", parent=body_style, fontSize=10, leading=14, textColor=colors.HexColor("#064E3B")))]],
        colWidths=[540],
    )
    rec_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#D1FAE5")),
            ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor("#10B981")),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )
    story.append(rec_table)
    story.append(Spacer(1, 10))

    # Reasons
    story.append(Paragraph("Why This Recommendation?", h2_style))
    for reason in result.primary_reasons:
        story.append(Paragraph(f"• {reason}", body_style))
    story.append(Spacer(1, 8))

    # Options Matrix Table (540pt total)
    story.append(Paragraph("Evaluated Strategies & Options", h2_style))
    table_data = [[
        Paragraph("Option", th_style),
        Paragraph("Target Market", th_style),
        Paragraph("Gross Rev", th_style),
        Paragraph("Transport", th_style),
        Paragraph("Spoilage", th_style),
        Paragraph("Expected Net", th_style),
        Paragraph("Risk", th_style),
    ]]
    for opt in result.options:
        table_data.append([
            Paragraph(opt.option_id, td_bold_style),
            Paragraph(opt.target_market, td_style),
            Paragraph(f"Rs. {opt.gross_revenue:,.0f}", td_style),
            Paragraph(f"Rs. {opt.transport_cost:,.0f}", td_style),
            Paragraph(f"Rs. {opt.estimated_spoilage_loss:,.0f}", td_style),
            Paragraph(f"Rs. {opt.expected_net_realization:,.0f}", td_bold_style),
            Paragraph(opt.risk_level, td_style),
        ])

    opt_table = Table(table_data, colWidths=[60, 140, 75, 75, 75, 75, 40])
    opt_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#065F46")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F9FAFB")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F9FAFB")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ])
    )
    story.append(opt_table)
    story.append(Spacer(1, 10))

    # Action Plan (540pt total)
    story.append(Paragraph("Executable Action Plan", h2_style))
    action_data = [[
        Paragraph("Prio", th_style),
        Paragraph("Action Step", th_style),
        Paragraph("Reason & Justification", th_style),
    ]]
    for act in result.action_plan:
        action_data.append([
            Paragraph(str(act.priority), td_bold_style),
            Paragraph(act.action, td_style),
            Paragraph(act.reason, td_style),
        ])

    act_table = Table(action_data, colWidths=[30, 270, 240])
    act_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#374151")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F9FAFB")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ])
    )
    story.append(act_table)
    story.append(Spacer(1, 10))

    # Disclaimer
    story.append(Paragraph("<b>Disclaimer:</b> " + disclaimer_text, ParagraphStyle("Disc", parent=body_style, fontSize=7.5, leading=10, textColor=colors.HexColor("#6B7280"))))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
