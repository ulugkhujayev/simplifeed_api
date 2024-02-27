# from reportlab.platypus import Table, Paragraph, SimpleDocTemplate
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.units import inch
# from django.http import HttpResponse


# def generate_pdf(posts):
#     title_style = ParagraphStyle(name="Title", fontSize=18)
#     header_style = ParagraphStyle(name="Header", fontSize=14, bold=True)
#     data_style = ParagraphStyle(name="Data", fontSize=10)

#     doc = SimpleDocTemplate("recent_posts.pdf")
#     elements = []

#     # elements.append(Paragraph("Recent Posts (Last 24 Hours)", style=title_style))
#     # elements.append(Paragraph("\n"))

#     headers = ["Author", "Body", "Created At"]
#     table_data = [headers]

#     for post in posts:
#         author_username = post["author"]
#         body_text = post["body"]
#         created_at = post["created_at"]

#         table_row = [
#             Paragraph(author_username, style=header_style),
#             Paragraph(body_text, style=data_style),
#             Paragraph(created_at, style=data_style),
#         ]
#         table_data.append(table_row)

#     table = Table(
#         data=table_data,
#         colWidths=[1.5 * inch, 3 * inch, 1 * inch],
#         style=[
#             ("ALIGN", (0, 0), (-1, -1), "LEFT"),
#             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
#             ("INNERGRID", (0, 0), (-1, -1), 1, "gray"),
#             ("BOX", (0, 0), (-1, -1), 0.5, "black"),
#             ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
#         ],
#     )

#     table.setStyle(
#         [
#             ("ALIGN", (1, 0), (-1, -1), "LEFT"),
#             ("VALIGN", (1, 0), (-1, -1), "MIDDLE"),
#             ("FONT", (1, 0), (-1, -1), "Helvetica"),
#         ]
#     )

#     elements.append(table)

#     doc.build(elements)

#     with open("recent_posts.pdf", "rb") as f:
#         pdf = f.read()
#     response = HttpResponse(pdf, content_type="application/pdf")
#     response["Content-Disposition"] = 'attachment; filename="recent_posts.pdf"'
#     return response


from io import BytesIO
from reportlab.platypus import Table, Paragraph, SimpleDocTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from django.http import HttpResponse


def generate_pdf(posts):
    title_style = ParagraphStyle(name="Title", fontSize=18)
    header_style = ParagraphStyle(name="Header", fontSize=14, bold=True)
    data_style = ParagraphStyle(name="Data", fontSize=10)

    # Create a BytesIO buffer to store the PDF content
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    elements = []

    headers = ["Author", "Body", "Created At"]
    table_data = [headers]
    print(posts)

    for post in posts:
        author_username = str(post.author)
        body_text = str(post.body)
        created_at = str(post.created_at)

        table_row = [
            Paragraph(author_username, style=header_style),
            Paragraph(body_text, style=data_style),
            Paragraph(created_at, style=data_style),
        ]
        table_data.append(table_row)

    table = Table(
        data=table_data,
        colWidths=[1.5 * inch, 3 * inch, 1 * inch],
        style=[
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("INNERGRID", (0, 0), (-1, -1), 1, "gray"),
            ("BOX", (0, 0), (-1, -1), 0.5, "black"),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ],
    )

    table.setStyle(
        [
            ("ALIGN", (1, 0), (-1, -1), "LEFT"),
            ("VALIGN", (1, 0), (-1, -1), "MIDDLE"),
            ("FONT", (1, 0), (-1, -1), "Helvetica"),
        ]
    )

    elements.append(table)

    doc.build(elements)

    # Reset the buffer position to the beginning
    buffer.seek(0)

    # Return the response with the PDF content
    response = HttpResponse(buffer.read(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="recent_posts.pdf"'
    return response
