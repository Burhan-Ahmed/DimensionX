# Measure It

A computer-vision project to segment a wooden block in smartphone images and, as future
work, estimate its physical dimensions in millimetres using camera calibration and a
checkerboard reference.

> **Progress:** The camera calibration, fixed annotated dataset, U-Net training/evaluation
> notebook, trained checkpoint, training history, test predictions, and segmentation metrics
> are available. The end-to-end pixel-to-millimetre measurement pipeline is not implemented.

## Setup

From the repository root, create and activate a virtual environment, then install the
dependencies listed in `requirements.txt`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The requirements include the packages used by the calibration and training/evaluation
notebook. PyTorch and torchvision are intentionally not version-pinned; for GPU training,
choose versions compatible with the target CUDA runtime. The notebook is designed for Google
Colab, where PyTorch may already be installed.

## Hardware

| Component | Recorded setup |
|---|---|
| Camera | Xiaomi Redmi Note 13 rear camera |
| Development computer | Windows 11 64-bit, Intel Core i7-4770K, Intel integrated graphics, 14 GB RAM |
| Planned training environment | Google Colab; GPU model not recorded |

The development-computer specifications are from the project notes. The exact Colab GPU used
for the saved training run was not recorded.

## How to run each stage

Run commands from the repository root.

### 1. Camera calibration

Calibration images belong in `calibration/images/`. The calibration script expects a 7 × 9
inner-corner checkerboard. Supply the measured square size in millimetres:

```powershell
python calibration/calibrate.py --square-mm <measured-square-size-mm> --max-err 1.0 --fix-k3
```

The script asks whether to use all detected images (`A`), only images below the reprojection
error threshold (`V`), or quit (`Q`). It writes the resulting camera parameters to
`calibration/camera.npz`. The repository includes calibration images and a calibration
parameter file.

### 2. Dataset and fixed split

The fixed split lists are in `dataset/splits/{train,val,test}.txt`. Treat these lists as the
source of truth; do not regenerate or change them after annotation. The split-specific images
and masks are arranged in `dataset/{train,val,test}/images/` and
`dataset/{train,val,test}/masks/`.

The original Label Studio export is `dataset/Annotation labels/result.json`. The raw capture
images and a dataset-generation script are not included in this repository, so the data
preparation step cannot currently be reproduced from raw images here.

### 3. Labelling

Images were labelled in **Label Studio** and exported in COCO polygon format. The exported
annotations are in `dataset/Annotation labels/result.json`; the corresponding binary masks
are stored alongside each split's images. No relabelling command is needed to use the prepared
dataset.

### 4. Model training and evaluation

The training and evaluation workflow is in `Model/code/Pipeline.ipynb`. To run it in Google
Colab:

1. Upload/open the notebook in Colab and select a runtime. A GPU runtime is recommended.
2. Put the prepared dataset in Google Drive with this structure:
   `Dataset/{train,val,test}/{images,masks}/`.
3. In the notebook, update `DATASET_DIR` to that Drive folder. Review `OUTPUT_DIR` and
   `MODEL_DIR` as well; these paths determine where the run saves its outputs.
4. Run all cells in order. The notebook installs packages, verifies image/mask pairs, trains
   the U-Net, selects a checkpoint by validation IoU, and evaluates on the held-out test set.

The notebook configuration uses a 512-pixel input, batch size 2, at most 30 epochs, learning
rate `1e-4`, seed 42, and early stopping. Do not use the test split to select or tune a model.
The repository includes a saved checkpoint and training/evaluation artifacts under
`Model/results/`; see the results section below. Saved notebook cell outputs may reflect an
earlier run, so rerun the notebook to reproduce them.

### 5. Inference and measurement

Not implemented. There is no command yet for predicting a mask on a new image or converting
the segmented object dimensions to millimetres.

### 6. Evaluation and experiments

The notebook evaluates segmentation on the test split and saves metrics and predicted masks.
Calliper comparisons, raw-versus-undistorted measurement comparisons, and failure-condition
experiments have not been completed.

## Dataset summary

| Field | Details |
|---|---|
| Object | Wooden block; COCO category `Rectangle` |
| Images | 91 annotated images, 3000 × 4000 pixels |
| Split | Train: 63; validation: 19; test: 9 (fixed lists, approximately 70/20/10) |
| Labelling tool | Label Studio; COCO polygon export |
| Prepared data | Each split has matching `images/` and binary `masks/` folders |

## Model and segmentation results

The saved checkpoint is `Model/results/weights/unet_best.pth`. Training history is in
`Model/results/stats/training_history.csv`; test metrics are in
`Model/results/stats/test_metrics.json`; per-image IoU and AP results are in the same `stats/`
folder, and predicted masks are in `Model/results/test_predictions/`.

The saved test metrics report:

| Metric | Result |
|---|---:|
| Pixel-level test IoU | 0.7763 |
| Mean per-image mask IoU | 0.7770 |
| Instance mask AP@0.5 | 1.0000 |
| Instance mask mAP@0.5:0.95 | 0.5920 |
| Precision | 0.7873 |
| Recall | 0.9825 |
| Best epoch (validation IoU) | 17 (0.7238) |

These are the values recorded in the saved results file; rerun the notebook to independently
reproduce them. The 9-image test set is small, so interpret the metrics accordingly. This
segmentation evaluation does not establish accuracy of physical measurements in millimetres.
