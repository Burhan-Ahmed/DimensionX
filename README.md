# Measure It

A computer-vision project to segment a wooden block in smartphone images and, as future
work, estimate its physical dimensions in millimetres using camera calibration and a
checkerboard reference.

> **Progress:** The camera calibration parameters, fixed dataset split, Label Studio COCO
> annotations, and split-specific images and masks are present. Model training was the next
> stage, but the run was not completed before time ran out. This repository currently has no
> runnable training script or saved model checkpoint. Evaluation and the measurement
> pipeline are also unfinished.

## Setup

The checked-in `requirements.txt` pins the dependencies used by the calibration script.
From the repository root, create and activate a virtual environment and install them:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The segmentation plan uses PyTorch, but no training code is present yet, so PyTorch is not
included in the current requirements. Add a PyTorch version appropriate for the target runtime
when implementing training. The repository does not pin a Python version.

## Hardware

| Component | Recorded setup |
|---|---|
| Camera | Xiaomi Redmi Note 13 rear camera |
| Development computer | Windows 11 64-bit, Intel Core i7-4770K, Intel integrated graphics, 14 GB RAM |
| Planned training environment | Google Colab; GPU model not recorded |

The development-computer specifications are from the project notes. Record the actual Colab
runtime details if training is resumed.

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
and masks are already arranged in `dataset/{train,val,test}/images/` and
`dataset/{train,val,test}/masks/`.

The original Label Studio export is `dataset/Annotation labels/result.json`. The raw capture
images and a dataset-generation script are not included in this repository, so the data
preparation step cannot currently be reproduced from raw images here.

### 3. Labelling

Images were labelled in **Label Studio** and exported in COCO polygon format. The exported
annotations are in `dataset/Annotation labels/result.json`; the corresponding binary masks
are stored alongside each split's images. No relabelling command is needed to use the prepared
dataset.

### 4. Model training

Training was not completed before the available time ran out. Although training was the next
planned step, this repository does not currently contain a model/training script, training
configuration, recorded training history, or saved checkpoint. There is therefore no
reproducible training command yet. The dataset is ready to be used by a future training
pipeline; keep the test split out of training and model selection.

### 5. Inference and measurement

Not implemented. There is no command yet for predicting a mask on a new image or converting
the segmented object dimensions to millimetres.

### 6. Evaluation and experiments

Not completed. Test-set segmentation metrics, calliper comparisons, and raw-versus-undistorted
or failure-condition experiments have not been recorded.

## Dataset summary

| Field | Details |
|---|---|
| Object | Wooden block; COCO category `Rectangle` |
| Images | 91 annotated images, 3000 × 4000 pixels |
| Split | Train: 63; validation: 19; test: 9 (fixed lists, approximately 70/20/10) |
| Labelling tool | Label Studio; COCO polygon export |
| Prepared data | Each split has matching `images/` and binary `masks/` folders |

## Model and results

No trained model checkpoint or evaluation results are currently available. Add the training
configuration, results, and checkpoint location here if those stages are completed.
