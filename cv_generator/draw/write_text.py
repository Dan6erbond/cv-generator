from typing import overload

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas, textobject


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
                        or font_size * 0.08
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
