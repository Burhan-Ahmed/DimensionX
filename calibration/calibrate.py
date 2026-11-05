
"""Calibrate a camera using checkerboard images and save parameters."""
import argparse
import glob
from pathlib import Path

import cv2
import numpy as np

PATTERN = (7, 9)  # Inner corners: columns, rows
FLAGS_SB = cv2.CALIB_CB_EXHAUSTIVE | cv2.CALIB_CB_ACCURACY


def image_errors(obj_pts, img_pts, rvecs, tvecs, K, dist):
    """Calculate per-image RMS reprojection errors in pixels."""
    errors = []

    for obj, img, r, t in zip(obj_pts, img_pts, rvecs, tvecs):
        projected, _ = cv2.projectPoints(obj, r, t, K, dist)

        error = cv2.norm(
            img.reshape(-1, 2),
            projected.reshape(-1, 2),
            cv2.NORM_L2
        ) / np.sqrt(len(projected))

        errors.append(error)

    return np.array(errors)


def calibrate(obj_pts, img_pts, size, flags):
    """Run camera calibration and return parameters and image errors."""
    rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
        obj_pts, img_pts, size, None, None, flags=flags
    )

    errors = image_errors(obj_pts, img_pts, rvecs, tvecs, K, dist)

    return rms, K, dist, errors


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--images", default="calibration/images/*.jpg")
    parser.add_argument("--square-mm", type=float, required=True)
    parser.add_argument("--out", default="calibration/camera.npz")

    parser.add_argument(
        "--max-err",
        type=float,
        default=1.0,
        help="Maximum per-image RMS reprojection error in pixels"
    )

    parser.add_argument("--min-images", type=int, default=20)

    parser.add_argument(
        "--fix-k3",
        action="store_true",
        help="Fix k3 and tangential distortion coefficients to zero"
    )

    args = parser.parse_args()

    # Create the 3D checkerboard coordinates.
    grid = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)

    grid[:, :2] = (
        np.mgrid[0:PATTERN[0], 0:PATTERN[1]]
        .T.reshape(-1, 2) * args.square_mm
    )

    obj_pts, img_pts, used = [], [], []
    size = None

    # Detect checkerboard corners in every image.
    image_paths = sorted(glob.glob(args.images))

    if not image_paths:
        raise SystemExit("ERROR: No calibration images found.")

    for path in image_paths:

        gray = cv2.imread(
            path,
            cv2.IMREAD_GRAYSCALE | cv2.IMREAD_IGNORE_ORIENTATION
        )

        if gray is None:
            print(f"SKIP (cannot read image): {path}")
            continue

        if size is None:
            size = gray.shape[::-1]

        elif gray.shape[::-1] != size:
            raise SystemExit(
                f"ERROR: {path} has resolution {gray.shape[::-1]}, "
                f"expected {size}."
            )

        found, corners = cv2.findChessboardCornersSB(
            gray, PATTERN, FLAGS_SB
        )

        if not found:
            print(f"SKIP (checkerboard not detected): {path}")
            continue

        obj_pts.append(grid.copy())
        img_pts.append(corners)
        used.append(path)

    total = len(used)

    if total < args.min_images:
        raise SystemExit(
            f"ERROR: Only {total} images detected successfully. "
            f"Minimum required: {args.min_images}."
        )

    # Configure calibration flags.
    flags = (
        cv2.CALIB_FIX_K3 | cv2.CALIB_ZERO_TANGENT_DIST
        if args.fix_k3 else 0
    )

    # First calibration: use every successfully detected image.
    rms, K, dist, errors = calibrate(
        obj_pts, img_pts, size, flags
    )

    # Classify images according to the selected error threshold.
    valid_indices = np.where(errors <= args.max_err)[0]
    high_error_indices = np.where(errors > args.max_err)[0]

    valid_count = len(valid_indices)
    high_error_count = len(high_error_indices)

    print("\n" + "=" * 55)
    print("INITIAL CALIBRATION ASSESSMENT")
    print("=" * 55)

    print(f"Total detected images       : {total}")
    print(f"Images within threshold     : {valid_count}")
    print(f"Images above threshold      : {high_error_count}")
    print(f"Maximum allowed error       : {args.max_err:.2f} px")
    print(f"Initial calibration RMS     : {rms:.4f} px")

    print("\nIMAGE-WISE RESULTS")
    print("-" * 55)

    for path, error in zip(used, errors):

        status = "PASS" if error <= args.max_err else "ABOVE THRESHOLD"

        print(f"{error:7.3f} px | {status:16} | {path}")

    print("\n" + "=" * 55)
    print("DATASET ASSESSMENT")
    print("=" * 55)

    print(
        f"{valid_count} out of {total} images meet the "
        f"{args.max_err:.2f} px error threshold."
    )

    print(
        f"{high_error_count} images have reprojection errors "
        f"greater than {args.max_err:.2f} px."
    )

    if valid_count < args.min_images:
        print(
            f"\nWARNING: Only {valid_count} images meet the threshold. "
            f"At least {args.min_images} are required for "
            f"threshold-only calibration."
        )

    print("\nWhat would you like to do?")
    print("[A] Continue using ALL detected images.")
    print("[V] Continue using ONLY images within the error threshold.")
    print("[Q] Quit without saving calibration.")

    choice = input("\nEnter your choice (A/V/Q): ").strip().upper()

    if choice == "Q":
        print("\nCalibration cancelled. No parameters were saved.")
        return

    elif choice == "V":

        if valid_count < args.min_images:
            raise SystemExit(
                f"\nCannot continue: only {valid_count} images "
                f"meet the threshold, but {args.min_images} are required.\n"
                "Please capture additional calibration images."
            )

        # Select only images that passed the initial assessment.
        obj_pts = [obj_pts[i] for i in valid_indices]
        img_pts = [img_pts[i] for i in valid_indices]

        selected = [used[i] for i in valid_indices]
        dropped = [used[i] for i in high_error_indices]

    elif choice == "A":

        # Retain every successfully detected image.
        selected = used.copy()
        dropped = []

    else:
        raise SystemExit("Invalid choice. Run the script again.")

    # Recalibrate using the selected images.
    rms, K, dist, final_errors = calibrate(
        obj_pts, img_pts, size, flags
    )

    final_valid = np.sum(final_errors <= args.max_err)
    final_high = np.sum(final_errors > args.max_err)

    print("\n" + "=" * 55)
    print("FINAL CALIBRATION RESULTS")
    print("=" * 55)

    print(f"Images used                 : {len(selected)}")
    print(f"Images excluded             : {len(dropped)}")
    print(f"Images within threshold     : {final_valid}")
    print(f"Images above threshold      : {final_high}")
    print(f"Final RMS reprojection error: {rms:.4f} px")

    print("\nFINAL IMAGE-WISE ERRORS")
    print("-" * 55)

    for path, error in zip(selected, final_errors):
        status = "PASS" if error <= args.max_err else "ABOVE THRESHOLD"
        print(f"{error:7.3f} px | {status:16} | {path}")

    print("\nCAMERA MATRIX:")
    print(K)

    print("\nDISTORTION COEFFICIENTS (k1, k2, p1, p2, k3):")
    print(dist.ravel())

    if final_high > 0:
        print(
            "\nWARNING: Some selected images still exceed the "
            "reprojection error threshold. Inspect the dataset."
        )

    # Save the calibration parameters.
    output_path = Path(args.out)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    np.savez(
        output_path,
        K=K,
        dist=dist,
        size=np.array(size),
        rms=rms,
        square_mm=args.square_mm,
        pattern=np.array(PATTERN),
        used=np.array(selected),
        dropped=np.array(dropped)
    )

    print(f"\nCalibration parameters saved to: {output_path}")


if __name__ == "__main__":
    main()

