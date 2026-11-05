# Measure It

Photograph a wooden block and report its real width and height in millimetres.
Pipeline: camera calibration -> undistortion -> segmentation mask -> checkerboard homography -> mm.

Work is on branch `dev-test01`. Planning documents are in `docs/` (`plan`, `objectives`, `definition_of_done`).

> **Status:** work in progress. Sections marked `TODO` do not exist yet. Anything unfinished at submission is listed in `docs/definition_of_done.tex`.

## Setup

```bash
git clone <TODO: repo URL>
cd <TODO: repo name>
git checkout dev-test01
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell; on Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

- Python: `<TODO: version>`
- Versions are pinned in `requirements.txt` (OpenCV `5.0.0` was used for calibration).
- Random seed: `<TODO: value>`; the split uses seed `0` in `dataset/make_split.py`.
- Every image is read with `cv2.IMREAD_IGNORE_ORIENTATION`, so pixels always match the camera matrix.

## Hardware

| Item | Value |
|---|---|
| Camera | Redmi Note 13, main 1x camera, focus and zoom locked, `<TODO: WxH>` px, `<TODO: portrait/landscape>` |
| Laptop (calibration, labelling, inference) | `<TODO: CPU>`, `<TODO: RAM>`, `<TODO: OS>` |
| Training | Google Colab, `<TODO: GPU>`, `<TODO: date>` |

## Physical setup

- **Object:** rectangular wooden block, `<TODO: W x H>` mm (calliper).
- **Reference:** printed checkerboard, 7 x 9 inner corners, square size `<TODO>` mm (calliper, 8 squares / 8), mounted flat on a rigid board.
- The block lies flat on the same surface as the board, next to it. The whole pattern is visible in every photo.

## How to run each stage

### 1. Calibration
Put 20+ checkerboard photos in `calibration/images/`.

```bash
python calibration/calibrate.py --square-mm <TODO> --max-err 1.0 --use valid --fix-k3
python calibration/undistort_check.py calibration/images/<image>.jpg
```

Writes `calibration/camera.npz` (camera matrix, distortion, RMS, image lists). Result: `<TODO: N images used, RMS px>`, details in `docs/objectives.tex`.

### 2. Dataset
Original photos go in `dataset/raw/` (not committed).

```bash
python dataset/check_raw.py                    # size and full-board check
python dataset/makeSplit.py                    # initial split; writes lists and dataset/split/
```

The split lists in `dataset/splits/` are authoritative. Do not regenerate them after labelling:
each image and its mask must remain in the split named by its list. The `dataset/split/`
folders are copies of raw images from split creation; they are not the undistorted training
images.

The current dataset is organized as follows:

| Path | Contents |
|---|---|
| `dataset/raw/` | Original camera images annotated in Label Studio |
| `dataset/labels/result.json` | Original COCO polygon export, in raw-image coordinates |
| `dataset/splits/{train,val,test}.txt` | Fixed split membership by image filename |
| `dataset/images/{train,val,test}/` | Undistorted images used for training and evaluation |
| `dataset/masks/{train,val,test}/` | Binary PNG masks, matching image filenames |
| `dataset/labels/{train,val,test}.json` | COCO polygons transformed to undistorted image coordinates |
| `dataset/check/` | Sample overlays for manually checking mask alignment |

Once undistorted images are in `dataset/images/{train,val,test}/`, create the split-specific
masks and labels with:

```bash
python convert_masks.py
```

The converter matches Label Studio's UUID-prefixed COCO filenames to the split lists by the
original image filename suffix. Review the overlays in `dataset/check/` before training.

### 3. Labelling
`<TODO: tool, export format, folder>`.

### 4. Training
`<TODO: command, config file, Colab notebook link>`. Checkpoint selected on the validation split only.

### 5. Inference (image to millimetres)
`<TODO: single command>`. Handles "object not found" and "reference not found".

### 6. Accuracy and experiments
`<TODO: scripts in measurement/ for the calliper table, raw vs undistorted, item 8, item 9>`.

## Dataset summary

| Field | Value |
|---|---|
| Object | wooden block, one class (`block`) |
| Images | `<TODO: 90>` own photos, taken with the calibrated camera and undistorted |
| Capture | camera fixed; block and checkerboard moved between shots |
| Split | train `<TODO>` / val `<TODO>` / test `<TODO>`, grouped by placement (time gap `<TODO>` s) |
| Labelling tool | `<TODO>` |
| Extra images (not in split) | negatives for not-found cases `<TODO: N>`, tilt series `<TODO: N>` |

Images are not stored in Git. `<TODO: link to images>`.

## Model weights

- File: `<TODO: name>`, link: `<TODO>`
- SHA-256: `<TODO: hash>` (`certutil -hashfile <file> SHA256` on Windows, `sha256sum <file>` on Linux)

## Results
See `docs/objectives.tex` for every table and raw output.