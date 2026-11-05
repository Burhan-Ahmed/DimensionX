# Definition of Done

## 1. Purpose

This document defines the acceptance criteria for the computer vision-based wooden object measurement project.

A task will be considered complete only when its implementation, verification, and supporting evidence are available in the project repository.

The completion criteria are divided into individual engineering components to ensure that the final system is reproducible, measurable, and properly documented.

## 2. Acceptance Criteria

### 2.1 Camera Calibration

- [x] At least 20 checkerboard calibration images have been captured.
- [x] Calibration images cover different positions, orientations, and viewing angles.
- [x] Camera intrinsic matrix and distortion coefficients have been calculated.
- [x] Calibration reprojection error has been recorded.
- [x] Undistorted images have been generated.
- [x] Raw and undistorted images have been compared and documented.

**Evidence:** Calibration images, calibration parameters, reprojection error, and before/after image comparisons.

### 2.2 Dataset Preparation

- [x] At least 70 original object images have been collected.
- [x] Each image has a corresponding binary segmentation mask.
- [x] All masks have been visually inspected for annotation errors.
- [x] Image-mask dimensions and filename correspondence have been verified.
- [x] A fixed 70/20/10 dataset split has been created.
- [x] Split assignments have been committed to version control.

**Evidence:** Dataset directory, annotation masks, dataset verification results, and split files.

### 2.3 Segmentation Model Development

- [x] Custom U-Net architecture implemented using PyTorch.
- [ ] Training pipeline implemented and executed.
- [ ] Training and validation loss recorded.
- [ ] Best model checkpoint saved.
- [ ] Early stopping or an equivalent training termination strategy implemented.
- [ ] Model predictions generated on unseen test images.

**Evidence:** Model source code, training history, saved checkpoint, and predicted segmentation masks.

### 2.4 Model Evaluation

- [ ] Test-set mask IoU calculated.
- [ ] mAP\@0.5 calculated using a documented mask-based evaluation protocol.
- [ ] mAP\@0.5:0.95 calculated using IoU thresholds from 0.50 to 0.95.
- [ ] Precision calculated.
- [ ] Recall calculated.
- [ ] Quantitative evaluation results saved.
- [ ] Predicted masks visually compared with ground-truth masks.

**Evidence:** Evaluation report, metric tables, CSV/JSON results, and visual comparisons.

### 2.5 Physical Measurement Pipeline

- [ ] Known-size reference object or calibration reference established.
- [ ] Pixel-to-millimetre conversion implemented.
- [ ] Segmented object dimensions extracted.
- [ ] Measurements reported in millimetres.
- [ ] At least 10 physical instances measured using digital callipers.
- [ ] Computer vision estimates compared against calliper measurements.
- [ ] Mean Absolute Error (MAE) and mean absolute percentage error calculated.

**Evidence:** Measurement outputs, calliper readings, comparison table, and error analysis.

### 2.6 Reliability and Failure Analysis

- [ ] Raw-image and undistorted-image measurement results compared.
- [ ] At least one failure experiment conducted and documented.
- [ ] Factors affecting segmentation and measurement accuracy identified.
- [ ] Confidence-based rejection mechanism implemented.
- [ ] Unreliable measurements are rejected instead of being reported as valid.
- [ ] Engineering decisions and limitations documented.

**Evidence:** Failure experiment, comparison results, confidence/rejection examples, and decision record.

### 2.7 Repository and Documentation

- [ ] README.md provides project overview and setup instructions.
- [ ] Objectives.md documents project objectives and expected outcomes.
- [ ] Plan.md documents the development plan.
- [ ] Definition_of_Done.md documents acceptance criteria.
- [ ] Source code is organized and committed to the repository.
- [ ] Dataset split files and relevant configuration files are included.
- [ ] Generated outputs and model checkpoints are referenced or made accessible.
- [ ] Repository instructions allow another developer to reproduce the workflow.

**Evidence:** GitHub repository containing source code, documentation, configurations, and available experimental results.

## 3. Overall Completion Criteria

The project will be considered complete when:

1. Camera calibration and image undistortion have been verified.
2. The annotated dataset and fixed data split are available.
3. The segmentation model has been trained and evaluated on the independent test set.
4. The measurement pipeline produces physical dimensions in millimetres.
5. Estimated measurements have been validated against digital calliper measurements.
6. Reliability and failure conditions have been investigated.
7. All relevant implementation details and experimental evidence are documented.

## 4. Current Development Status

| Component                           | Current status    |
| ----------------------------------- | ----------------- |
| Project objectives and scope        | Documented        |
| Custom PyTorch U-Net architecture   | Implemented       |
| Training pipeline                   | Pending execution |
| Model evaluation                    | Pending           |
| Camera calibration verification     | Pending evidence  |
| Dataset and annotation verification | Pending evidence  |
| Pixel-to-mm conversion              | Pending           |
| Calliper validation                 | Pending           |
| Failure and confidence analysis     | Pending           |
| Final documentation                 | In progress       |

**Status note:** 
## Not finished
- Items 4-10 (see unticked lines above): I can complete it but time ran out after the model stage.