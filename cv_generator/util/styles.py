from reportlab.lib import colors


list_style = {
    "fontSize": 12,
    "textColor": colors.black,
    "bulletIndent": 10,
    "leftIndent": 20,
    "leading": 14,
    "embeddedHyphenation": 1,
}

def get_style(style, **kwargs):
    return {**style, **kwargs}
