# Project Plan — Measure It

## Objective
Develop a computer vision system to segment a rectangular wooden object and estimate its physical width and height in millimetres using a calibrated smartphone camera.

## Approach

1. **Camera Calibration (2 hour)**
   - Capture at least 20 checkerboard images using a smartphone.
   - Measure the actual checkerboard square size.
   - Estimate camera intrinsic parameters and distortion coefficients using OpenCV.
   - Validate calibration using reprojection error.

2. **Dataset Collection and Annotation (1.5 hours)**
   - Capture at least 70 images of the wooden object.
   - Undistort images using calibration parameters.
   - Annotate object boundaries using Label Studio.
   - Create fixed 70/20/10 train/validation/test splits.

3. **Segmentation Model (1.5 hours)**
   - Use PyTorch Mask R-CNN with a pretrained ResNet50-FPN backbone.
   - Fine-tune on the collected dataset.
   - Evaluate using mask IoU, mAP@0.5, mAP@0.5:0.95, precision and recall.

4. **Measurement Pipeline (2 hours)**
   - Undistort incoming images.
   - Segment the wooden object.
   - Detect checkerboard reference corners.
   - Use planar geometric mapping to convert pixel coordinates into millimetres.
   - Generate a mask overlay and measurement output.
   - Handle missing object and missing reference cases.

5. **Accuracy Validation (1 hour)**
   - Measure at least 10 instances using a calliper.
   - Compare system measurements against physical measurements.
   - Calculate mean absolute error and mean percentage error.

6. **Additional Experiments and Documentation (1 hours)**
   - Compare measurements from raw and undistorted images.
   - Evaluate one challenging imaging condition.
   - Implement confidence-based measurement rejection where feasible.
   - Complete documentation and recording.

## Constraints and Decisions

- Use only self-captured images.
- Do not use Ultralytics YOLO or Roboflow models.
- Keep the test dataset isolated from training and model selection.
- Use a fixed random seed and record dependency versions.
- No decision to leave any feature/compoenent of the pipeline.

## Technical Decisions

- Selected Mask R-CNN because it provides instance segmentation and supports transfer learning.
- Selected OpenCV for camera calibration and geometric transformations.
- Use checkerboard geometry as I am already fimilar with it during my Final Year Project.
