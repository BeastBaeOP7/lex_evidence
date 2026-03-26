from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import re
import io


def generate_pdf_report(structured_text):

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    header_style = styles["Heading1"]
    section_style = styles["Heading2"]
    normal_style = styles["BodyText"]

    penalty_style = ParagraphStyle(
        'PenaltyStyle',
        parent=styles['BodyText'],
        textColor=colors.red
    )

    elements.append(Paragraph("StructuraLex – Legal Simplification Report", header_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Split into sections
    sections = re.split(r"\n(?=[A-Z][a-zA-Z ]+:)", structured_text)

    for section in sections:
        if ":" not in section:
            continue

        title, content = section.split(":", 1)
        title = title.strip()
        content = content.strip()

        elements.append(Paragraph(title, section_style))
        elements.append(Spacer(1, 0.2 * inch))

        lines = [line.strip() for line in content.split("\n") if line.strip()]

        bullet_points = []

        for line in lines:
            if title == "Penalties":
                bullet_points.append(ListItem(Paragraph(line, penalty_style)))
            else:
                bullet_points.append(ListItem(Paragraph(line, normal_style)))

        elements.append(ListFlowable(bullet_points, bulletType='bullet'))
        elements.append(Spacer(1, 0.3 * inch))

    doc.build(elements)

    buffer.seek(0)
    return buffer
