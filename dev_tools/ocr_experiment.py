import sys
import os
import argparse
import pathlib

from tesserocr import RIL, PSM
from PIL import Image, ImageDraw

import clickpecker.recognition.ocr_engine as engine
import clickpecker.processing.boxes_processing as postprocessing
from clickpecker.configurations import default_config


def configure_parser():
    parser = argparse.ArgumentParser(
        description="OCR engine visualisation tool.")
    parser.add_argument("input_path", help="Input image or directory")
    parser.add_argument("output_dir", help="Directory for output")
    parser.add_argument(
        "--crop",
        help="Crop area in X X Y Y format",
        nargs=4,
        default=[0, 1, 0, 1],
        type=float)
    return parser


def load_images(input_path):
    if (input_path.is_dir()):
        for root, _, files in os.walk(input_path):
            names = [fn for fn in files]
            img_paths = [os.path.join(root, fn) for fn in names]
            imgs = [Image.open(path) for path in img_paths]
            result = dict(zip(names, imgs))
    else:
        img = Image.open(input_path)
        result = {input_path.name: img}
    return result


def perform_ocr(named_images, config):
    ocr_result = {}
    for name, img in named_images.items():
        boxes = engine.parse(img, config)
        ocr_result[name] = boxes
    return ocr_result


def save_parsed_text(ocr_res, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    for name in ocr_res:
        with open(output_dir / "{}.txt".format(name), "wb") as f:
            for box in ocr_res[name]:
                f.write(box.content.encode("utf-8") + b"\n")


def draw_boxes(named_images, ocr_res, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, img in named_images.items():
        width, height = img.size
        d = ImageDraw.Draw(img)
        for box in ocr_res[name]:
            pos = [
                box.position.x * width, box.position.y * height,
                (box.position.x + box.position.w) * width,
                (box.position.y + box.position.h) * height
            ]
            d.rectangle(pos, outline="red")
        img.save(output_dir / name)


if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()
    input_path = pathlib.Path(args.input_path).expanduser()
    output_dir = pathlib.Path(args.output_dir).expanduser()
    imgs = load_images(input_path)
    crop_x_range, crop_y_range = (args.crop[0], args.crop[1]), (args.crop[2],
                                                                args.crop[3])
    config = dict(default_config)
    config["crop_x_range"] = crop_x_range
    config["crop_y_range"] = crop_y_range
    ocr_res = perform_ocr(imgs, config)
    save_parsed_text(ocr_res, output_dir / "txt")
    draw_boxes(imgs, ocr_res, output_dir / "img")
