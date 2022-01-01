import os

from cv_generator import generate_cv

if __name__ == "__main__":
    if not os.path.exists("__cache__"):
        os.mkdir("__cache__")
    if not os.path.exists(os.path.join("__cache__", "fonts")):
        os.mkdir(os.path.join("__cache__", "fonts"))
    if not os.path.exists(os.path.join("__cache__", "images")):
        os.mkdir(os.path.join("__cache__", "images"))

    """ # Convert TTF to AFM/PFB
    font = TTFont(
        os.path.join("assets", "Source_Sans_Pro", "SourceSansPro-Regular.ttf")
    )
    font.save(os.path.join("__cache__", "fonts", "SourceSansPro-Regular.afm"))
    font.save(os.path.join("__cache__", "fonts", "SourceSansPro-Regular.pfb")) """

    generate_cv(
        os.path.join("assets", "cv.json"),
        ("SourceSansPro-Regular.afm", "SourceSansPro-Regular.pfb"),
    )
