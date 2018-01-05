import sys
import os
import argparse
import pathlib

from functools import partial
import numpy as np
from PIL import Image, ImageDraw
from skimage.measure import compare_ssim as ssim
from skimage.measure import compare_mse as mse


def configure_parser():
    parser = argparse.ArgumentParser(
        description="Similarity metrics test")
    parser.add_argument("path_a", help="Input image or directory")
    parser.add_argument("path_b", help="Input image or directory")
    return parser



def compare(path_a, path_b, metric):
    if (path_a.is_dir()):
        for root, _, files in os.walk(path_a):
            names = [f for f in files if os.path.splitext(f)[1] in [".jpg", ".png"]]
            for n in names:
                a_path = os.path.join(root, n)
                b_path = os.path.join(path_b, n)
                a_img = Image.open(a_path)
                b_img = Image.open(b_path)
                metric_val = metric(np.array(a_img), np.array(b_img))
                print(f"{a_path} : {b_path} : similarity = {metric_val}")

if __name__ == "__main__":
    parser = configure_parser()
    args = parser.parse_args()
    path_a = pathlib.Path(args.path_a).expanduser()
    path_b = pathlib.Path(args.path_b).expanduser()

    print("==== SSIM ====")
    compare(path_a, path_b, partial(ssim, multichannel=True))
    print("==== MSE  ====")
    compare(path_a, path_b, mse)
