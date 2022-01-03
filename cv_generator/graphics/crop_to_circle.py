import os
import sys

from PIL import Image, ImageDraw, ImageOps


def crop_to_circle(file, size=None, bg_color=(255, 255, 255)):
    path = os.path.join(
        "__cache__",
        "images",
        (os.path.splitext(os.path.basename(file))[0] + "_circle.png"),
    )

    _img = Image.open(file)
    if _img.mode == "RGBA":
        img = Image.new("RGBA", _img.size, bg_color)
        img.paste(_img, (0, 0), _img)
        img.convert("RGB")
    else:
        img = _img

    if not size:
        size = img.size[0] if img.size[0] < img.size[1] else img.size[1]

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + mask.size, fill=255)

    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    output.save(path)
    return path


if __name__ == "__main__":
    path = crop_to_circle(sys.argv[1])
    print("Saved at:", path)
