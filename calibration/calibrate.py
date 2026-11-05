"""Calibrate the camera from checkerboard images and save the parameters."""
import argparse
import glob

import cv2
import numpy as np

PATTERN = (7, 9)  # inner corners (columns, rows)
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1e-4)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--images", default="calibration/images/*.jpg")
    p.add_argument("--square-mm", type=float, required=True)
    p.add_argument("--out", default="calibration/camera.npz")
    args = p.parse_args()

    grid = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)
    grid[:, :2] = np.mgrid[0:PATTERN[0], 0:PATTERN[1]].T.reshape(-1, 2) * args.square_mm

    obj_pts, img_pts, used = [], [], []
    size = None
    for path in sorted(glob.glob(args.images)):
        gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if size is None:
            size = gray.shape[::-1]
        elif gray.shape[::-1] != size:
            raise SystemExit(f"{path} is {gray.shape[::-1]}, expected {size}: mixed resolutions")
        found, corners = cv2.findChessboardCorners(gray, PATTERN)
        if not found:
            print(f"SKIP (no corners): {path}")
            continue
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), CRITERIA)
        obj_pts.append(grid)
        img_pts.append(corners)
        used.append(path)

    if len(used) < 20:
        raise SystemExit(f"Only {len(used)} usable images; need 20 or more")

    rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(obj_pts, img_pts, size, None, None)

    print(f"images used: {len(used)}  image size: {size}")
    for path, o, i, r, t in zip(used, obj_pts, img_pts, rvecs, tvecs):
        proj, _ = cv2.projectPoints(o, r, t, K, dist)
        err = cv2.norm(i.reshape(-1, 2), proj.reshape(-1, 2), cv2.NORM_L2) / np.sqrt(len(proj))
        print(f"{err:6.3f} px  {path}")
    print(f"RMS reprojection error: {rms:.4f} px")
    print(f"camera matrix:\n{K}\ndistortion (k1 k2 p1 p2 k3): {dist.ravel()}")

    np.savez(args.out, K=K, dist=dist, size=np.array(size), rms=rms,
             square_mm=args.square_mm, pattern=np.array(PATTERN))


if __name__ == "__main__":
    main()