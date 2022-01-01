import json
import os

from reportlab.lib import pagesizes, units
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from .graphics.crop_to_circle import crop_to_circle
from .util.i18n import resolve_string


def generate_cv(data_path, font, lang="en"):
    data = json.load(open(data_path))
    print("Loaded data for:", data["name"]["first"])

    print("Generating CV...")

    doc = canvas.Canvas(filename="cv.pdf", pagesize=pagesizes.A4)

    afmFile, pfbFile = font
    justFace = pdfmetrics.EmbeddedType1Face(
        os.path.join("__cache__", "fonts", afmFile),
        os.path.join("__cache__", "fonts", pfbFile),
    )
    faceName, _ = afmFile.split(".")
    pdfmetrics.registerTypeFace(justFace)
    justFont = pdfmetrics.Font(faceName, faceName, "WinAnsiEncoding")
    pdfmetrics.registerFont(justFont)
    doc.setFont(faceName, 32)

    doc.setStrokeColorRGB(167 / 255, 174 / 255, 177 / 255)
    doc.setFillColorRGB(167 / 255, 174 / 255, 177 / 255)
    doc.rect(0, 0, 8 * units.cm, pagesizes.A4[1], fill=1)

    img = crop_to_circle(os.path.join(os.path.dirname(data_path), data["img"]))
    y = pagesizes.A4[1] - 6 * units.cm - 1 * units.cm
    doc.drawImage(
        img,
        1 * units.cm,
        y,
        width=6 * units.cm,
        height=6 * units.cm,
        mask="auto",
    )

    doc.setStrokeColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.setFillColorRGB(42 / 255, 56 / 255, 72 / 255)
    doc.rect(
        8 * units.cm,
        pagesizes.A4[1] - 3.5 * units.cm - 1 * units.cm,
        pagesizes.A4[0] - 8 * units.cm - 1 * units.cm,
        3.5 * units.cm,
        fill=1,
    )

    name_text = doc.beginText(
        8.5 * units.cm,
        pagesizes.A4[1] - 2.5 * units.cm,
    )
    name_text.setFillColorRGB(255 / 255, 255 / 255, 255 / 255)

    for char in data["name"]["first"]:
        if char.upper() == char:
            name_text.setFont(faceName, 34)
            name_text.textOut(char)
        else:
            name_text.setFont(faceName, 28)
            name_text.textOut(char.upper())

    name_text.textOut(" ")

    for char in data["name"]["last"]:
        if char.upper() == char:
            name_text.setFont(faceName, 34)
            name_text.textOut(char)
        else:
            name_text.setFont(faceName, 28)
            name_text.textOut(char.upper())

    doc.drawText(name_text)

    headline_text = doc.beginText(
        8.5 * units.cm,
        pagesizes.A4[1] - 3.75 * units.cm,
    )
    headline_text.setFont(faceName, 22)
    headline_text.setFillColorRGB(210 / 255, 210 / 255, 210 / 255)
    headline_text.textOut(resolve_string(data["headline"], lang))
    doc.drawText(headline_text)

    doc.save()

    print("File saved at: ./cv.pdf")
