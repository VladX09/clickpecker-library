import cv2
import math
import os
import pathlib
import argparse

from PIL import Image, ImageDraw
import numpy as np

import clickpecker.recognition.tm_engine as engine


def configure_parser():
    parser = argparse.ArgumentParser(
        description="TM engine visualisation tool")
    parser.add_argument("input_path", help="Input image or directory")
    parser.add_argument("template_path", help="Template image")
    parser.add_argument("output_dir", help="Directory for output")
    parser.add_argument(
        "--crop",
        help="Crop area in X X Y Y format [WIP]",
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


def draw_boxes(named_images, tm_res, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, img in named_images.items():
        width, height = img.size
        d = ImageDraw.Draw(img)
        box = tm_res[name]
        pos = [
            box.x * width, box.y * height,
            (box.x + box.w) * width,
            (box.y + box.h) * height
        ]
        d.rectangle(pos, outline="red")
        img.save(output_dir / name)


def perform_tm(named_images,
               template,
               crop_x_range=(0, 1),
               crop_y_range=(0, 1)):
    tm_result = {}
    for name, img in named_images.items():
        box = engine.get_match(img, template)
        tm_result[name] = box
    return tm_result


if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()
    input_path = pathlib.Path(args.input_path).expanduser()
    output_dir = pathlib.Path(args.output_dir).expanduser()
    template_path = pathlib.Path(args.template_path).expanduser()
    imgs = load_images(input_path)
    template = engine.load_template(str(template_path))
    crop_x_range, crop_y_range = (args.crop[0], args.crop[1]), (args.crop[2],
                                                                args.crop[3])
    tm_res = perform_tm(imgs, template, crop_x_range, crop_y_range)
    draw_boxes(imgs, tm_res, output_dir)
