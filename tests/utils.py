import os
import glob

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

from collections import namedtuple

Configuration = namedtuple(
    "Configuration", ["font_size", "screen_size", "bg_color", "text_color"])


def acc_lines():
    font_path = Path(__file__).resolve().parent / "roboto_font"
    font_pattern = font_path / "*.ttf"
    fonts = glob.glob(str(font_pattern))
    lines = [Path(font_path).name for font_path in fonts]
    return lines


def acc_images():
    font_path = Path(__file__).resolve().parent / "roboto_font"
    font_pattern = font_path / "*.ttf"
    fonts = glob.glob(str(font_pattern))
    lines = acc_lines()
    text_n_font = list(zip(lines, fonts))
    configurations = [
        Configuration(12, (240, 320), (255, 255, 255), (0, 0, 0)),
        Configuration(14, (240, 400), (255, 255, 255), (0, 0, 0)),
        Configuration(16, (240, 432), (255, 255, 255), (0, 0, 0)),
        Configuration(18, (480, 854), (255, 255, 255), (0, 0, 0)),
        Configuration(26, (320, 480), (255, 255, 255), (0, 0, 0)),
        Configuration(28, (480, 640), (255, 255, 255), (0, 0, 0)),
        Configuration(30, (600, 1024), (255, 255, 255), (0, 0, 0)),
        Configuration(32, (1280, 768), (255, 255, 255), (0, 0, 0)),
        Configuration(36, (2560, 1600), (255, 255, 255), (0, 0, 0)),
        Configuration(12, (240, 320), (0, 0, 0), (255, 255, 255)),
        Configuration(16, (240, 432), (0, 0, 0), (255, 255, 255)),
        Configuration(18, (480, 854), (0, 0, 0), (255, 255, 255)),
        Configuration(28, (480, 640), (0, 0, 0), (255, 255, 255)),
        Configuration(32, (1280, 768), (0, 0, 0), (255, 255, 255))
    ]

    for conf in configurations:
        img = Image.new("RGB", conf.screen_size, conf.bg_color)
        draw = ImageDraw.Draw(img)
        dy = conf.screen_size[1] / len(text_n_font)
        x = 15
        y = 10
        for i, (line, font_path) in enumerate(text_n_font):
            font = ImageFont.truetype(font_path, conf.font_size)
            draw.text((x, y + i * dy), line, fill=conf.text_color, font=font)
        yield img


def save_images(dir):
    for i, img in enumerate(acc_images()):
        img.save("{}/{}.png".format(dir, i))


if __name__ == "__main__":
    dir = Path(__file__).resolve().parent / "resoruces"
    print("Images are saved to:", dir)
    if not dir.is_dir():
        os.mkdir(dir)
    save_images(dir)
