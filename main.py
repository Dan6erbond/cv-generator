import argparse
import os

from cv_generator import generate_cv

parser = argparse.ArgumentParser(description="Generate a CV from a template.")
parser.add_argument(
    "data", nargs="?", default="./assets/cv.json", help="The data file to use."
)
parser.add_argument(
    "title",
    nargs="?",
    default=None,
    help="The title of the CV, will be used as filename if none specified.",
)
parser.add_argument("--filename", "-f", dest="filename", help="The filename to use.")
parser.add_argument(
    "--lang", "-l", dest="lang", default="en", help="Language of the CV."
)
parser.add_argument(
    "--hide-watermark",
    "-hd",
    dest="watermark",
    action="store_false",
    help="Hide the watermark.",
)

if __name__ == "__main__":
    args = parser.parse_args()

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

    """ print(
        args.lang,
        args.title,
        args.filename,
    ) """

    generate_cv(
        args.data or os.path.join("assets", "cv.json"),
        ("SourceSansPro-Regular.afm", "SourceSansPro-Regular.pfb"),
        args.lang,
        args.title,
        args.filename if args.filename else args.title + ".pdf" if args.title else None,
    )
