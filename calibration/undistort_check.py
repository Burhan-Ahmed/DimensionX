"""Show one image before and after undistortion with a straight-line grid."""
import argparse

import cv2
import numpy as np


def undistort(img, K, dist):
    return cv2.undistort(img, K, dist, None, K)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--params", default="calibration/camera.npz")
    p.add_argument("--out", default="calibration/undistort_check.jpg")
    args = p.parse_args()

    cal = np.load(args.params)
    raw = cv2.imread(args.image)
    fixed = undistort(raw, cal["K"], cal["dist"])
    panels = []
    for im in (raw, fixed):
        im = im.copy()
        for x in range(0, im.shape[1], im.shape[1] // 10):
            cv2.line(im, (x, 0), (x, im.shape[0]), (0, 255, 0), 2)
        for y in range(0, im.shape[0], im.shape[0] // 10):
            cv2.line(im, (0, y), (im.shape[1], y), (0, 255, 0), 2)
        panels.append(im)
    cv2.imwrite(args.out, np.hstack(panels))


if __name__ == "__main__":
    main()