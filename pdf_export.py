import sqlite3
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

DB_PATH = "musings.db"

def export_to_pdf(pdf_path="musings.pdf"):
    """Fetch thoughts from database and export them to PDF."""
    # Fetch thoughts.
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "SELECT id, timestamp, content FROM musings ORDER BY id ASC"
        )
        thoughts = cursor.fetchall()

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)  # create new PDF
    styles = getSampleStyleSheet()                      # load styles
    story = []                                          # list for holding pdf elements

    # Loop through each thought to format them for pdf
    for idx, (thought_id, timestamp, content) in enumerate(thoughts):
        # Try to parse timestamp into datetime
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.fromisoformat(timestamp)
        formatted_time = dt.strftime("%B %d, %Y @ %I:%M %p")    # custom format for timestamp

        # Elements
        header = Paragraph(f"{thought_id}", styles["Heading1"])            # ID header
        body = Paragraph(content.replace("\n", "<br/>"), styles["BodyText"])    # thought body
        timestamp = Paragraph(formatted_time, styles["Italic"])                 # timestamp
        story.extend([header, Spacer(1, 12),                       # add to pdf element story
                      body, Spacer(1, 24),
                      timestamp])

        # Add a page break if not the last thought
        if idx < len(thoughts) - 1:
            story.append(PageBreak())

    # Build the pdf
    doc.build(story)