"""Undistort every raw image with the saved camera parameters."""
import argparse
import glob
import os

import cv2
import numpy as np


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--src", default="dataset/raw")
    p.add_argument("--dst", default="dataset/images")
    p.add_argument("--params", default="calibration/camera.npz")
    args = p.parse_args()

    cal = np.load(args.params)
    K, dist, size = cal["K"], cal["dist"], tuple(int(v) for v in cal["size"])
    os.makedirs(args.dst, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(args.src, "*.jpg"))):
        img = cv2.imread(path, cv2.IMREAD_COLOR | cv2.IMREAD_IGNORE_ORIENTATION)
        if img.shape[1::-1] != size:
            raise SystemExit(f"{path} is {img.shape[1::-1]}, calibration is {size}")
        out = cv2.undistort(img, K, dist, None, K)
        name = os.path.basename(path)
        cv2.imwrite(os.path.join(args.dst, name), out, [cv2.IMWRITE_JPEG_QUALITY, 95])
        print(name)


if __name__ == "__main__":
    main()