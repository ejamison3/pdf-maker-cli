import html
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def render_pdf(code: str, filename: str, output_path: str, no_color: bool = False) -> None:
    """
    Renders code to a PDF file with syntax highlighting and line numbers.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceAfter=12,
    )
    story.append(Paragraph(html.escape(filename), title_style))

    code_style = ParagraphStyle(
        "CodeStyle",
        fontName="Courier",
        fontSize=8,
        leading=11,
        wordWrap="CJK",
        textColor=colors.black,
        backColor=None,
    )

    lines = code.splitlines()
    line_count = len(lines)
    gutter_width = len(str(max(line_count, 1)))

    paragraphs = []

    for i, line_text in enumerate(lines, 1):
        escaped_line = html.escape(line_text).replace(" ", "\xa0")
        line_num = str(i).rjust(gutter_width)
        
        # Black text for both gutter and code
        full_line_html = f"{html.escape(line_num + ' | ')}{escaped_line if escaped_line else r'\xa0'}"

        paragraphs.append([Paragraph(full_line_html, code_style)])

    if paragraphs:
        table = Table(paragraphs, colWidths=["100%"])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.white),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(table)

    doc.build(story)
