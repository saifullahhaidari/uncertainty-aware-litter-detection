# Uncertainty-Aware Cross-Domain Evaluation of Lightweight Outdoor Litter Detectors

## 1. Project Overview

This research investigates the performance and reliability of lightweight object detection models for outdoor litter detection across different datasets and environments.

The project focuses on cross-domain generalization and explores whether uncertainty estimation can help identify unreliable model predictions.

## 2. Research Objectives

- Evaluate lightweight object detection models for outdoor litter detection.
- Investigate performance changes when a model is evaluated on a different dataset from the one used for training.
- Examine whether uncertainty estimation can help identify potentially incorrect or unreliable predictions.
- Consider computational efficiency, including inference speed and resource requirements.

## 3. Research Questions

1. How well does a lightweight litter detector generalize across different datasets?
2. How do environmental and dataset differences affect detection performance?
3. Can uncertainty estimation help distinguish reliable predictions from potentially incorrect ones?
4. What trade-offs exist between detection performance, reliability, and computational cost?

## 4. Planned Methodology

The planned workflow includes:

1. Review candidate datasets and their licenses.
2. Audit annotation quality, class definitions, image diversity, and potential data overlap.
3. Select a suitable lightweight detection baseline.
4. Prepare and document reproducible dataset splits.
5. Train and evaluate the baseline under controlled conditions.
6. Conduct cross-domain evaluation without retraining on the target test domain.
7. Investigate suitable uncertainty estimation methods.
8. Report detection metrics, reliability results, computational cost, and limitations.

TACO and PlastOPol are candidate datasets. Their suitability and compatibility must be assessed before final selection. YOLOv8n is a candidate baseline, not yet a confirmed experimental choice.

## 5. Evaluation Plan

Potential evaluation measures include:

- Precision and Recall
- Average Precision (AP) and mean Average Precision (mAP)
- False Positives (FP) and False Negatives (FN)
- Suitable measures for evaluating uncertainty-based error detection
- Inference latency and Frames Per Second (FPS)

The final metrics will depend on the validated experimental design and available annotations.

## 6. Current Status

- [x] Created the GitHub repository.
- [x] Recorded the initial project description.
- [x] Checked the main computer's hardware specifications.
- [ ] Document and verify the software environment.
- [ ] Audit candidate datasets and their licenses.
- [ ] Finalize the dataset selection and experimental protocol.
- [ ] Implement the baseline detector.
- [ ] Conduct cross-domain experiments.
- [ ] Evaluate uncertainty estimation methods.
- [ ] Analyze results and document limitations.

No model training results or experimental findings are claimed at this stage.

## 7. Reproducibility and Research Integrity

Experimental configurations, dataset versions, code changes, evaluation procedures, and limitations will be documented as the project progresses.

Datasets, model weights, and other third-party resources will be used in accordance with their licenses. Large datasets and files that should not be redistributed will not be committed to this repository.

## 8. Research Goal

The long-term goal is to investigate whether lightweight outdoor litter detection can become more reliable when evaluated across different environments, while accounting for uncertainty and computational constraints.
