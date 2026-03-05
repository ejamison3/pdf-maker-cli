import html
from pygments import lexers, util
from pygments.lexers.special import TextLexer
from pygments.formatters import get_formatter_by_name
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def render_pdf(code: str, filename: str, output_path: str) -> None:
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

    # Lexer setup
    try:
        lexer = lexers.get_lexer_for_filename(filename, stripall=True)
    except util.ClassNotFound:
        lexer = TextLexer(stripall=True)

    # Formatter for color lookup
    formatter = get_formatter_by_name("html", style="monokai")

    code_style = ParagraphStyle(
        "CodeStyle",
        fontName="Courier",
        fontSize=8,
        leading=11,
        wordWrap="CJK",
        backColor=None,
    )

    gutter_style = ParagraphStyle(
        "GutterStyle",
        fontName="Courier",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#888888"),
    )

    lines = code.splitlines()
    line_count = len(lines)
    gutter_width = len(str(max(line_count, 1)))

    paragraphs = []

    for i, line_text in enumerate(lines, 1):
        # Re-create lexer per line to avoid state carryover issues
        try:
            line_lexer = lexers.get_lexer_for_filename(filename, stripall=True)
        except util.ClassNotFound:
            line_lexer = TextLexer(stripall=True)

        tokens = list(line_lexer.get_tokens(line_text))

        formatted_tokens = ""
        for ttype, value in tokens:
            # Remove newlines that pygments appends during single-line tokenization
            val = value.replace("\n", "").replace("\r", "")
            if not val:
                continue

            color = formatter.style.style_for_token(ttype).get("color")
            escaped_val = html.escape(val).replace(" ", "\xa0")

            if color:
                formatted_tokens += f'<font color="#{color}">{escaped_val}</font>'
            else:
                formatted_tokens += escaped_val

        line_num = str(i).rjust(gutter_width)
        gutter_html = f'<font color="#888888">{html.escape(line_num + " | ")}</font>'
        full_line_html = gutter_html + (formatted_tokens if formatted_tokens else "\xa0")

        paragraphs.append([Paragraph(full_line_html, code_style)])

    if paragraphs:
        table = Table(paragraphs, colWidths=["100%"])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#272822")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#f8f8f2")),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(table)

    doc.build(story)
