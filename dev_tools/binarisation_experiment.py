import cv2
import PIL
import os
import pathlib
import argparse
import numpy as np

from PIL import Image
from clickpecker.processing import utils
from clickpecker.processing.image_processing import basic_binarisation


def configure_parser():
    parser = argparse.ArgumentParser(
        description="TM engine visualisation tool")
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


def binarize(named_images, x_range=(0, 1), y_range=(0, 1)):
    preproc = basic_binarisation()
    res = {}
    for name, img in named_images.items():
        img = preproc(img)
        w, h = img.size
        img = img.crop((x_range[0] * w, y_range[0] * h, x_range[1] * w,
                                y_range[1] * h))
        res[name] = img
    return res


def invert(pil_image):
    cv2_img = np.array(pil_image)
    cv2_img = cv2.bitwise_not(cv2_img)
    return PIL.Image.fromarray(cv2_img)


def save(named_images, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, img in named_images.items():
        img.save(output_dir / name)


if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()
    input_path = pathlib.Path(args.input_path).expanduser()
    output_dir = pathlib.Path(args.output_dir).expanduser()
    imgs = load_images(input_path)
    crop_x_range, crop_y_range = (args.crop[0], args.crop[1]), (args.crop[2],args.crop[3])
    res = binarize(imgs, crop_x_range, crop_y_range)
    save(res, output_dir)
