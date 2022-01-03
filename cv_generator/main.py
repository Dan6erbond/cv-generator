import json
import os
from typing import overload

from reportlab.lib import colors, pagesizes, styles, units
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas, textobject
from reportlab.platypus import Paragraph

from .graphics.crop_to_circle import crop_to_circle
from .util.i18n import resolve_string, strings


@overload
def write_text(
    text_object: textobject.PDFTextObject,
    text: str,
    face_name: str,
    size: int,
    max_width: int,
    style: dict = None,
) -> tuple[int, int]:
    ...


@overload
def write_text(
    text_object: textobject.PDFTextObject,
    text: str,
    face_name: str,
    size: int,
    end_right: int,
    style: dict = None,
) -> tuple[int, int]:
    ...


def write_text(
    text_object: textobject.PDFTextObject,
    text: str,
    face_name: str,
    font_size: int,
    max_width: int = None,
    end_right: int = None,
    style: dict = {},
):
    if not max_width and not end_right:
        raise Exception("Either width or end_right must be set.")

    max_width = max_width if max_width else end_right - text_object.getX()

    start_y = text_object.getY()

    text_object.setFont(face_name, font_size)

    space_width = pdfmetrics.stringWidth(
        " ", text_object._fontname, text_object._fontsize
    )
    max_line_width = 0
    for line in text.splitlines():
        if not line:
            text_object.textLine("")
        else:
            words = list()
            width = 0
            for word in line.split(" "):
                if style.get("small-caps", False):
                    word_width = 0
                    for char in word:
                        if char == char.upper():
                            word_width += pdfmetrics.stringWidth(
                                char, face_name, font_size
                            )
                        else:
                            word_width += pdfmetrics.stringWidth(
                                char, face_name, font_size * 0.8
                            )
                    word_width += (
                        getattr(
                            text_object,
                            "_charSpace",
                            text_object._canvas._charSpace,
                        )
                        or 1.25
                    ) * len(word) - 1
                else:
                    word_width = pdfmetrics.stringWidth(
                        word, text_object._fontname, text_object._fontsize
                    )

                if width + word_width >= max_width:
                    l = " ".join(words)
                    if style.get("small-caps", False):
                        for char in l:
                            if char.upper() == char:
                                text_object.setFont(face_name, font_size)
                                text_object.textOut(char)
                            else:
                                text_object.setFont(face_name, font_size * 0.8)
                                text_object.textOut(char.upper())
                    else:
                        text_object.textLine(l)
                    words = list()
                    if width >= max_line_width:
                        max_line_width = width
                    width = 0

                words.append(word)
                width += word_width + space_width
            if words:
                l = " ".join(words)
                if style.get("small-caps", False):
                    for char in l:
                        if char.upper() == char:
                            text_object.setFont(face_name, font_size)
                            text_object.textOut(char)
                        else:
                            text_object.setFont(face_name, font_size * 0.8)
                            text_object.textOut(char.upper())
                else:
                    text_object.textLine(l)
                if width >= max_line_width:
                    max_line_width = width

    height = start_y - text_object.getY()
    return max_line_width, height


def draw_left(
    doc: canvas.Canvas, data: dict, data_path: str, face_name: str, lang: str
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

    paragraph = Paragraph(
        f"""<u>{data['phone']}</u>
                          <br/><br/>
                          <u>{data['email']}</u>""",
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

    summary_text = doc.beginText(
        0.5 * units.cm,
        pagesizes.A4[1] - y_pos - 0.75 * units.cm,
    )
    _, height = write_text(
        summary_text,
        resolve_string(data["summary"], lang),
        face_name,
        14,
        end_right=6.75 * units.cm,
    )
    doc.drawText(summary_text)

    y_pos += height


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
        22,
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
                    fontName=face_name,
                    fontSize=12,
                    textColor=colors.black,
                    bulletIndent=10,
                    leftIndent=20,
                    leading=14,
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
                    fontName=face_name,
                    fontSize=12,
                    textColor=colors.black,
                    bulletIndent=10,
                    leftIndent=20,
                    leading=14,
                ),
            )
            paragraph.wrapOn(doc, pagesizes.A4[0] - 8.5 * units.cm - 1 * units.cm, 0)
            paragraph.drawOn(
                doc, 8.5 * units.cm, y_pos - 0.2 * units.cm - paragraph.height
            )
            y_pos -= 0.2 * units.cm + paragraph.height


def generate_cv(data_path: str, font: str, lang: str = "en"):
    data = json.load(open(data_path))
    print("Loaded data for:", data["name"]["first"])

    print("Generating CV...")

    title = f"CV_{data['name']['first']}_{data['name']['last']}"
    filename = f"{title}.pdf"
    doc = canvas.Canvas(filename=filename, pagesize=pagesizes.A4)
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

    draw_left(doc, data, data_path, face_name, lang)
    draw_right(doc, data, data_path, face_name, lang)

    doc.save()

    print(f"File saved at: ./{filename}")
