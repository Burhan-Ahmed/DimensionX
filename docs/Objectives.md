# Project Objectives

## 1. Project Overview

The objective of this project is to develop a computer vision-based measurement system capable of segmenting a rectangular wooden object and estimating its physical dimensions from smartphone camera images.

The system combines camera calibration, image undistortion, semantic segmentation using a custom PyTorch U-Net, and pixel-to-millimetre conversion.

The primary focus is not simply identifying the object, but producing reliable physical measurements and evaluating their accuracy against independent measurements obtained using digital callipers.

## 2. Measurable Objectives

### MO-1: Physical Measurement Accuracy

| Field | Entry |
|---|---|
| **ID** | MO-1 |
| **What is measured** | Mean Absolute Percentage Error (MAPE) between computer vision-based measurements and reference measurements obtained using digital callipers. Both length and width are evaluated. |
| **How** | Measure at least 10 physical wooden object instances using digital callipers. Run the measurement system on corresponding images and calculate the absolute percentage error for each measured dimension. Report every instance, followed by the mean, median, and worst-case error. |
| **Target** | MAPE of 5% or less across all evaluated dimensions. |
| **Conditions** | Smartphone camera, calibrated and undistorted images, controlled indoor lighting, a fixed camera-to-object distance, a known-size reference for pixel-to-millimetre conversion, and the object positioned within the calibrated measurement plane. |
| **Not included** | Heavily occluded objects, severe motion blur, images with insufficient illumination, and objects outside the calibrated measurement plane. |

**Target justification:**

I selected a 5% MAPE target as an initial engineering acceptance criterion because the system is intended to provide useful approximate physical measurements rather than merely identify objects. This target allows a measurable tolerance while requiring the system to remain reasonably close to independent calliper measurements. All individual measurement errors will be reported so that the average does not conceal significant failures.

### MO-2: Segmentation Quality

| Field | Entry |
|---|---|
| **ID** | MO-2 |
| **What is measured** | Mean mask Intersection over Union (IoU) between predicted segmentation masks and their corresponding ground-truth masks. |
| **How** | Evaluate the trained custom PyTorch U-Net on every image in the held-out test split. Convert predicted probabilities into binary masks using a fixed threshold of 0.5. Calculate mask IoU for each test image and report the mean. |
| **Target** | Mean mask IoU of at least 0.80 across the held-out test dataset. |
| **Conditions** | Images captured using the specified smartphone camera, consistent image preprocessing, 512 × 512 model input resolution, binary ground-truth masks, and a fixed independent test split. |
| **Not included** | Images containing objects outside the defined target category, severely corrupted images, and images where the target object is completely obscured. |

**Target justification:**

I selected a mean mask IoU of 0.80 as the target because the measurement pipeline depends on accurately identifying the object's boundaries. Poor segmentation can directly affect the extracted dimensions and introduce errors into the pixel-to-millimetre conversion. A higher overlap between predicted and ground-truth masks provides evidence that the segmentation component is suitable for subsequent measurement experiments.

## 3. Experimental Environment and Reproducibility

To ensure that experimental results can be reproduced and independently verified, I will document the following configuration:

| Parameter | Recorded configuration |
|---|---|
| Operating system | Windows 11 64-bit |
| CPU | Core i7 4th Generation 4770k processor |
| GPU | Intel built-in GPU |
| RAM | 14 GB RAM |
| Camera model | Xiaomi Redmi Note 13 (108 MP Rear Camera) |
| Original image resolution | 3000 x 4000 |
| Model input resolution | 512 × 512 |
| Deep learning framework | PyTorch |
| Segmentation architecture | Custom U-Net |
| Random seed | 42 |
| Dataset split | 70% training / 20% validation / 10% testing |
| Prediction threshold | 0.5 |

The actual hardware and software configuration will be recorded from the execution environment rather than assumed.

## 4. Reporting and Evidence Requirements

For every quantitative result, I will provide the corresponding experimental evidence.

### Physical Measurement Accuracy

- Reference calliper measurement for every evaluated instance.
- Corresponding computer vision measurement.
- Absolute error in millimetres.
- Absolute percentage error.
- Mean, median, and worst-case error.
- Raw experimental output.

### Segmentation Quality

- Ground-truth and predicted mask comparisons.
- Individual test-image IoU values.
- Overall mean mask IoU.
- Raw evaluation output.
- Saved evaluation results.

### Experimental Integrity

- Training, validation, and test data remain separate.
- The test split is not used for model selection or hyperparameter tuning.
- Measurement targets and evaluation procedures are defined before examining final test results.
- Reported values must originate from actual machine execution, not estimates or manually fabricated results.

## 5. Expected Outcome

The expected outcome is a reproducible computer vision measurement pipeline that can:

1. Correct smartphone camera distortion.
2. Segment a wooden object from its background.
3. Estimate its physical dimensions in millimetres.
4. Evaluate segmentation performance against ground-truth masks.
5. Validate physical measurements against digital callipers.
6. Identify unreliable measurement conditions and document system limitations.

The project will be evaluated against MO-1 and MO-2 using the specified experimental procedures and acceptance targets. Failing to meet a target will be reported transparently with supporting evidence and analysis.