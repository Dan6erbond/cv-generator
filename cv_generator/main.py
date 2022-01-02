import json
import os

from reportlab.lib import pagesizes, units, styles, colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas, textobject
from reportlab.platypus import Paragraph

from .graphics.crop_to_circle import crop_to_circle
from .util.i18n import resolve_string


def write_small_caps(
    text_object: textobject.PDFTextObject, text: str, face_name: str, font_size: int
):
    for char in text:
        if char.upper() == char:
            text_object.setFont(face_name, font_size)
            text_object.textOut(char)
        else:
            text_object.setFont(face_name, font_size * 0.8)
            text_object.textOut(char.upper())


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

    lines = list()
    space_width = pdfmetrics.stringWidth(
        " ", text_object._fontname, text_object._fontsize
    )
    for line in text.splitlines():
        if not line:
            lines.append("")
        else:
            words = list()
            width = 0
            for word in line.split(" "):
                word_width = pdfmetrics.stringWidth(
                    word, text_object._fontname, text_object._fontsize
                )

                if width + word_width >= max_width:
                    l = " ".join(words)
                    lines.append(l)
                    words = list()
                    width = 0

                words.append(word)
                width += word_width + space_width
            if words:
                l = " ".join(words)
                lines.append(l)

    text_object.textLines(lines)

    height = start_y - text_object.getY()
    return max_width, height


def draw_left(
    doc: canvas.Canvas, data: dict, data_path: str, face_name: str, lang: str
):
    y_pos = 0

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
    write_small_caps(profile_title, "Profile", face_name, 22)
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
    write_small_caps(profile_title, "Contact", face_name, 22)
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
    write_small_caps(profile_title, "Languages", face_name, 22)
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

    doc.setStrokeColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.setFillColorRGB(42 / 255, 56 / 255, 72 / 255)
    y = pagesizes.A4[1] - 3.5 * units.cm - 1 * units.cm
    doc.rect(
        8 * units.cm,
        y,
        pagesizes.A4[0] - 8 * units.cm - 1 * units.cm,
        3.5 * units.cm,
        fill=1,
    )

    y_pos += y

    name_text = doc.beginText(
        8.5 * units.cm,
        pagesizes.A4[1] - 2.5 * units.cm,
    )
    name_text.setFillColorRGB(255 / 255, 255 / 255, 255 / 255)
    write_small_caps(name_text, data["name"]["first"], face_name, 34)
    name_text.textOut(" ")
    write_small_caps(name_text, data["name"]["last"], face_name, 34)
    doc.drawText(name_text)

    headline_text = doc.beginText(
        8.5 * units.cm,
        pagesizes.A4[1] - 3.75 * units.cm,
    )
    headline_text.setFont(face_name, 22)
    headline_text.setFillColorRGB(210 / 255, 210 / 255, 210 / 255)
    headline_text.textOut(resolve_string(data["headline"], lang))
    doc.drawText(headline_text)


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

    print(f"File saved at: ./{filename}.pdf")
