import json
import os
from datetime import datetime

from reportlab.lib import colors, pagesizes, styles, units
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from .draw import write_text
from .graphics.crop_to_circle import crop_to_circle
from .util.i18n import resolve_string, strings
from .util.styles import get_style, list_style


def draw_left(
    doc: canvas.Canvas,
    data: dict,
    data_path: str,
    face_name: str,
    lang: str,
    include_watermark: bool = True,
):
    y_pos = 0

    def draw_cursor():
        doc.line(0, y_pos, 8 * units.cm, y_pos)

    doc.setStrokeColorRGB(167 / 255, 174 / 255, 177 / 255)
    doc.setFillColorRGB(167 / 255, 174 / 255, 177 / 255)
    doc.rect(0, 0, 8 * units.cm, pagesizes.A4[1], fill=1)

    img = crop_to_circle(os.path.join(os.path.dirname(data_path), data["img"]))
    y = 6 * units.cm + 1 * units.cm
    doc.drawImage(
        img,
        1 * units.cm,
        pagesizes.A4[1] - y,
        width=6 * units.cm,
        height=6 * units.cm,
        mask="auto",
    )

    y_pos += y

    doc.setStrokeColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.setFillColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.rect(
        0,
        pagesizes.A4[1] - y_pos - 2.5 * units.cm,
        7 * units.cm,
        1.5 * units.cm,
        fill=1,
    )

    y_pos += 1.5 * units.cm

    doc.drawImage(
        os.path.join("assets", "icons", "manager.png"),
        0.5 * units.cm,
        pagesizes.A4[1] - y_pos - 0.75 * units.cm,
        width=1 * units.cm,
        height=1 * units.cm,
        mask="auto",
    )

    profile_title = doc.beginText(
        2 * units.cm,
        pagesizes.A4[1] - y_pos - 0.5 * units.cm,
    )
    profile_title.setFillColorRGB(255 / 255, 255 / 255, 255 / 255)
    write_text(
        profile_title,
        resolve_string(strings["profile"], lang),
        face_name,
        22,
        max_width=7 * units.cm,
        style={"small-caps": True},
    )
    doc.drawText(profile_title)

    summary_text = doc.beginText(
        0.5 * units.cm,
        pagesizes.A4[1] - y_pos - 14 - 1.25 * units.cm,
    )
    _, height = write_text(
        summary_text,
        resolve_string(data["summary"], lang),
        face_name,
        14,
        end_right=6.75 * units.cm,
    )
    doc.drawText(summary_text)

    y_pos += height + 0.5 * units.cm

    doc.setStrokeColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.setFillColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.rect(
        0,
        pagesizes.A4[1] - y_pos - 2.5 * units.cm,
        7 * units.cm,
        1.5 * units.cm,
        fill=1,
    )

    y_pos += 1.5 * units.cm

    doc.drawImage(
        os.path.join("assets", "icons", "message.png"),
        0.5 * units.cm,
        pagesizes.A4[1] - y_pos - 0.75 * units.cm,
        width=1 * units.cm,
        height=1 * units.cm,
        mask="auto",
    )

    profile_title = doc.beginText(
        2 * units.cm,
        pagesizes.A4[1] - y_pos - 0.5 * units.cm,
    )
    profile_title.setFillColorRGB(255 / 255, 255 / 255, 255 / 255)
    write_text(
        profile_title,
        resolve_string(strings["contact"], lang),
        face_name,
        22,
        max_width=7 * units.cm,
        style={"small-caps": True},
    )
    doc.drawText(profile_title)

    contact_addresses = list()

    if data.get("phone"):
        contact_addresses.append(data["phone"])
    if data.get("email"):
        contact_addresses.append(data["email"])
    if data.get("website"):
        contact_addresses.append(data["website"])

    paragraph = Paragraph(
        "<br/><br/>".join(
            f"<u>{contact_address}</u>" for contact_address in contact_addresses
        ),
        style=styles.ParagraphStyle(
            "contact",
            fontName=face_name,
            fontSize=14,
            textColor=colors.white,
        ),
    )
    paragraph.wrapOn(doc, 6.75 * units.cm, 0)
    paragraph.drawOn(
        doc,
        0.5 * units.cm,
        pagesizes.A4[1] - y_pos - paragraph.height - 1.25 * units.cm,
    )
    y_pos += paragraph.height + 0.75 * units.cm

    doc.setStrokeColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.setFillColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.rect(
        0,
        pagesizes.A4[1] - y_pos - 2.5 * units.cm,
        7 * units.cm,
        1.5 * units.cm,
        fill=1,
    )

    y_pos += 2.5 * units.cm

    doc.drawImage(
        os.path.join("assets", "icons", "globe.png"),
        0.5 * units.cm,
        pagesizes.A4[1] - y_pos + 0.25 * units.cm,
        width=1 * units.cm,
        height=1 * units.cm,
        mask="auto",
    )

    profile_title = doc.beginText(
        2 * units.cm,
        pagesizes.A4[1] - y_pos + 0.5 * units.cm,
    )
    profile_title.setFillColorRGB(255 / 255, 255 / 255, 255 / 255)
    write_text(
        profile_title,
        resolve_string(strings["languages"], lang),
        face_name,
        22,
        max_width=7 * units.cm,
        style={"small-caps": True},
    )
    doc.drawText(profile_title)

    for language in data["languages"]:
        paragraph = Paragraph(
            f"{resolve_string(strings['language_codes'][language['language']], lang)}: {resolve_string(strings['language_level'][language['fluency']], lang)}".replace(
                "\n", "<br/>"
            ).replace(
                "/", " / "
            ),
            bulletText="•",
            style=styles.ParagraphStyle(
                "language-list",
                **get_style(
                    list_style,
                    fontName=face_name,
                    textColor=colors.white,
                ),
            ),
        )
        paragraph.wrapOn(doc, 6.5 * units.cm, 0)
        paragraph.drawOn(
            doc,
            0.5 * units.cm,
            pagesizes.A4[1] - y_pos - 0.2 * units.cm - paragraph.height,
        )
        y_pos += 0.2 * units.cm + paragraph.height

    if include_watermark:
        watermark = doc.beginText(0.5 * units.cm, 0.75 * units.cm)
        watermark.setFillColorRGB(0 / 255, 0 / 255, 0 / 255)
        write_text(
            watermark,
            resolve_string(strings["watermark"], lang),
            face_name,
            9,
            6 * units.cm,
        )
        doc.drawText(watermark)


def draw_right(
    doc: canvas.Canvas, data: dict, data_path: str, face_name: str, lang: str
):
    y_pos = 0

    def draw_cursor():
        doc.line(8 * units.cm, y_pos, pagesizes.A4[0], y_pos)

    doc.setStrokeColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.setFillColorRGB(42 / 255, 56 / 255, 72 / 255)
    y = pagesizes.A4[1] - 3.5 * units.cm - 1 * units.cm
    name_rect_width = pagesizes.A4[0] - 8 * units.cm - 1 * units.cm
    doc.rect(
        8 * units.cm,
        y,
        name_rect_width,
        3.5 * units.cm,
        fill=1,
    )

    y_pos = y

    name_text = doc.beginText(
        8.5 * units.cm,
        pagesizes.A4[1] - 2.5 * units.cm,
    )
    name_text.setFillColorRGB(255 / 255, 255 / 255, 255 / 255)
    name_text_width, _ = write_text(
        name_text,
        data["name"]["first"],
        face_name,
        34,
        max_width=name_rect_width - 1 * units.cm,
        style={"small-caps": True},
    )
    name_text.textOut(" ")
    write_text(
        name_text,
        data["name"]["last"],
        face_name,
        34,
        max_width=name_rect_width - 1 * units.cm - name_text_width,
        style={"small-caps": True},
    )
    doc.drawText(name_text)

    headline_text = doc.beginText(
        8.5 * units.cm,
        pagesizes.A4[1] - 3.75 * units.cm,
    )
    headline_text.setFillColorRGB(210 / 255, 210 / 255, 210 / 255)
    write_text(
        headline_text,
        resolve_string(data["headline"], lang),
        face_name,
        20,
        max_width=name_rect_width - 1 * units.cm,
    )
    doc.drawText(headline_text)

    doc.setFillColorRGB(0 / 255, 0 / 255, 0 / 255)
    doc.setStrokeColorRGB(0 / 255, 0 / 255, 0 / 255)
    doc.setLineWidth(1)

    y = y_pos - 0.5 * units.cm - 28
    education_title = doc.beginText(
        8.5 * units.cm,
        y,
    )
    width, _ = write_text(
        education_title,
        resolve_string(strings["experience"], lang),
        face_name,
        28,
        max_width=8 * units.cm,
        style={"small-caps": True},
    )
    doc.drawText(education_title)
    doc.line(
        8.5 * units.cm, y - 0.25 * units.cm, 8.5 * units.cm + width, y - 0.25 * units.cm
    )

    y_pos = y - 0.25 * units.cm

    for entry in data["experience"]:
        y = y_pos - 0.25 * units.cm - 20
        entry_title = doc.beginText(8.5 * units.cm, y)
        write_text(
            entry_title,
            resolve_string(entry["company"], lang),
            face_name,
            20,
            max_width=pagesizes.A4[0] - 8 * units.cm - 1 * units.cm,
            style={"small-caps": True},
        )
        doc.drawText(entry_title)
        y_pos = y

        y = y_pos - 0.25 * units.cm - 11
        entry_field = doc.beginText(8.5 * units.cm, y)
        entry_field.setFont(face_name, 11)
        date = (
            resolve_string(entry["start"], lang)
            if "end" not in entry
            else f"{resolve_string(entry['start'], lang)} - {resolve_string(entry['end'], lang)}"
        )
        entry_field.textOut(f"{resolve_string(entry['position'], lang)} | {date}")
        doc.drawText(entry_field)
        y_pos = y

        y_pos -= 0.2 * units.cm
        for task in entry["tasks"]:
            paragraph = Paragraph(
                resolve_string(task, lang).replace("\n", "<br/>"),
                bulletText="•",
                style=styles.ParagraphStyle(
                    "education-list",
                    **get_style(
                        list_style,
                        fontName=face_name,
                    ),
                ),
            )
            paragraph.wrapOn(doc, pagesizes.A4[0] - 8.5 * units.cm - 1 * units.cm, 0)
            paragraph.drawOn(
                doc, 8.5 * units.cm, y_pos - 0.2 * units.cm - paragraph.height
            )
            y_pos -= 0.2 * units.cm + paragraph.height

    if data["projects"]:
        y = y_pos - 0.25 * units.cm - 20
        entry_title = doc.beginText(8.5 * units.cm, y)
        write_text(
            entry_title,
            resolve_string(strings["projects"], lang),
            face_name,
            20,
            max_width=pagesizes.A4[0] - 8 * units.cm - 1 * units.cm,
            style={"small-caps": True},
        )
        doc.drawText(entry_title)
        y_pos = y

        y_pos -= 0.2 * units.cm
        for project in data["projects"]:
            paragraph = Paragraph(
                resolve_string(project["description"], lang).replace("\n", "<br/>"),
                bulletText="•",
                style=styles.ParagraphStyle(
                    "projects-list",
                    **get_style(
                        list_style,
                        fontName=face_name,
                    ),
                ),
            )
            paragraph.wrapOn(doc, pagesizes.A4[0] - 8.5 * units.cm - 1 * units.cm, 0)
            paragraph.drawOn(
                doc, 8.5 * units.cm, y_pos - 0.2 * units.cm - paragraph.height
            )
            y_pos -= 0.2 * units.cm + paragraph.height

    y = y_pos - 0.5 * units.cm - 28
    education_title = doc.beginText(
        8.5 * units.cm,
        y,
    )
    width, _ = write_text(
        education_title,
        resolve_string(strings["education"], lang),
        face_name,
        28,
        max_width=8 * units.cm,
        style={"small-caps": True},
    )
    doc.drawText(education_title)
    doc.line(
        8.5 * units.cm, y - 0.25 * units.cm, 8.5 * units.cm + width, y - 0.25 * units.cm
    )

    y_pos = y - 0.25 * units.cm

    for entry in data["education"]:
        y = y_pos - 0.25 * units.cm - 20
        entry_title = doc.beginText(8.5 * units.cm, y)
        write_text(
            entry_title,
            resolve_string(entry["institution"], lang),
            face_name,
            20,
            max_width=pagesizes.A4[0] - 8 * units.cm - 1 * units.cm,
            style={"small-caps": True},
        )
        doc.drawText(entry_title)
        y_pos = y

        y = y_pos - 0.25 * units.cm - 11
        entry_field = doc.beginText(8.5 * units.cm, y)
        entry_field.setFont(face_name, 11)
        date = (
            resolve_string(entry["start"], lang)
            if "end" not in entry
            else f"{resolve_string(entry['start'], lang)} - {resolve_string(entry['end'], lang)}"
        )
        entry_field.textOut(f"{resolve_string(entry['field'], lang)} | {date}")
        doc.drawText(entry_field)
        y_pos = y

        y_pos -= 0.2 * units.cm
        for task in entry["tasks"]:
            paragraph = Paragraph(
                resolve_string(task, lang).replace("\n", "<br/>"),
                bulletText="•",
                style=styles.ParagraphStyle(
                    "education-list",
                    **get_style(
                        list_style,
                        fontName=face_name,
                    ),
                ),
            )
            paragraph.wrapOn(doc, pagesizes.A4[0] - 8.5 * units.cm - 1 * units.cm, 0)
            paragraph.drawOn(
                doc, 8.5 * units.cm, y_pos - 0.2 * units.cm - paragraph.height
            )
            y_pos -= 0.2 * units.cm + paragraph.height


def generate_cv(
    data_path: str,
    font: tuple[str, str],
    lang: str = "en",
    title: str = None,
    filename: str = None,
    output_path: str = "./",
    include_watermark: bool = True,
):
    data = json.load(open(data_path, encoding="utf8"))
    print("Loaded data for:", data["name"]["first"])

    print("Generating CV...")

    today = datetime.today()
    if not title:
        if data.get("title", None):
            title = data["title"].format(
                firstname=data["name"]["first"],
                lastname=data["name"]["first"],
                date=today.strftime("%Y-%m-%d"),
                lang=lang,
            )
        else:
            title = f"CV_{data['name']['first']}_{data['name']['last']}"
    if not filename:
        if data.get("filename", None):
            filename = data["filename"].format(
                title=title,
                firstname=data["name"]["first"],
                lastname=data["name"]["first"],
                date=today.strftime("%Y-%m-%d"),
                lang=lang,
            )
        else:
            filename = (
                f"{today.year}_{today.month:02d}_{today.day:02d}_{title}_{lang}.pdf"
            )
    doc = canvas.Canvas(
        filename=os.path.abspath(os.path.join(output_path, filename)),
        pagesize=pagesizes.A4,
    )
    doc.setTitle(title)

    afm_file, pfb_file = font
    just_face = pdfmetrics.EmbeddedType1Face(
        os.path.join("__cache__", "fonts", afm_file),
        os.path.join("__cache__", "fonts", pfb_file),
    )
    face_name, _ = afm_file.split(".")
    pdfmetrics.registerTypeFace(just_face)
    just_font = pdfmetrics.Font(face_name, face_name, "WinAnsiEncoding")
    pdfmetrics.registerFont(just_font)
    doc.setFont(face_name, 32)

    draw_left(doc, data, data_path, face_name, lang, include_watermark)
    draw_right(doc, data, data_path, face_name, lang)

    doc.save()

    print(f"File saved at: ./{filename}")

    return filename
