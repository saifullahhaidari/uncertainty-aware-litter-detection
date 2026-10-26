# Research Log — Uncertainty-Aware Cross-Domain Evaluation of Lightweight Outdoor Litter Detectors

## Project Overview

- **Project Title:** Uncertainty-Aware Cross-Domain Evaluation of Lightweight Outdoor Litter Detectors
- **Research Domain:** Computer Vision, Deep Learning, Object Detection, Uncertainty Estimation, and Cross-Domain Generalization
- **Primary Dataset Under Inspection:** TACO
- **Potential Second Dataset:** PlastOPol
- **Planned Baseline:** A lightweight pretrained object detector, with YOLOv8n as the initial candidate
- **Current Phase:** Environment setup, dataset inspection, annotation auditing, and data preparation
- **Research Integrity:** No model training or experimental performance evaluation has been completed yet.

## Entry 001 — Repository Setup

- **Date:** 2026-10-23
- **Activity:** Created the local project repository and initialized Git version control.
- **Project Directory:** `D:\saifullah\uncertainty-aware-litter-detection`
- **Remote Repository:** `https://github.com/saifullahhaidari/uncertainty-aware-litter-detection`
- **Research Log:** `docs/research_log.md`
- **README:** `README.md`
- **Outcome:** The local Git repository and GitHub remote were configured.
- **Status:** Initial repository setup completed.

## Entry 002 — Hardware Verification

- **Date:** 2026-10-23
- **Activity:** Inspected the main computer's hardware and GPU availability.
- **Operating System:** Windows 11 Home Single Language.
- **Processor:** Intel Core i7-12700, 12 cores and 20 logical processors.
- **GPU:** NVIDIA GeForce GTX 1660 SUPER.
- **GPU Memory:** 6 GB VRAM.
- **System RAM:** 16 GB.
- **Storage Note:** Previously reported free space was approximately 15 GB on the C: SSD and 350 GB on the D: HDD. These figures may change and should be rechecked before large experiments.
- **Outcome:** The computer was identified as the primary development and experimentation machine.
- **Limitation:** Actual training feasibility and batch-size selection must be tested before large-scale experiments.
- **Status:** Initial hardware verification completed.

## Entry 003 — Software Environment Verification

- **Date:** 2026-10-23
- **Activity:** Verified the Python environment, deep-learning libraries, and GPU access.
- **Python:** 3.10.11.
- **PyTorch:** 2.6.0+cu124.
- **Torchvision:** 0.21.0+cu124.
- **CUDA Availability in PyTorch:** True.
- **Detected GPU:** NVIDIA GeForce GTX 1660 SUPER.
- **Ultralytics:** 8.4.188.
- **Virtual Environment:** `.venv`
- **Outcome:** The main Python and deep-learning components imported successfully, and PyTorch detected the GPU.
- **Limitation:** Successful environment verification does not establish training speed, memory requirements, or model performance.
- **Status:** Initial software environment verification completed.

## Entry 004 — TACO Annotation Inspection

- **Date:** 2026-10-25
- **Activity:** Downloaded and inspected the official TACO annotation file.
- **Annotation File:** `data/annotations.json`.
- **Images Listed:** 1,500.
- **Annotations:** 4,784.
- **Categories:** 60.
- **Structural Checks:** No missing image references or invalid category references were found in the checks performed.
- **Outcome:** The annotation file was successfully parsed and its basic structure inspected.
- **Limitation:** These checks do not establish annotation correctness, image diversity, duplicate frequency, or suitability for the final research task.
- **Status:** Initial structural inspection completed.

## Entry 005 — TACO Image Download and Validation

- **Date:** 2026-10-25
- **Activity:** Downloaded the images listed in the TACO annotation file and ran image-file validation.
- **Images Listed:** 1,500.
- **Downloaded During the Final Download Run:** 1,303.
- **Existing Files Skipped During That Run:** 197.
- **Download Failures Reported:** 0.
- **Validation Script:** `src/validate_images.py`.
- **Validation Report:** `docs/taco_image_validation.json`.
- **Images Checked:** 1,500.
- **Valid Image Files:** 1,500.
- **Missing Image Files:** 0.
- **Invalid Image Files:** 0.
- **Outcome:** All 1,500 listed image files passed the implemented file-integrity validation.
- **Limitation:** File-integrity validation does not verify image content, label accuracy, duplicate images, or environmental diversity.
- **Status:** Download and initial image validation completed.

## Entry 006 — TACO Bounding-Box Processing and Image Exclusion

- **Date:** 2026-10-26
- **Activity:** Created a processed copy of the TACO annotations, clipped six bounding boxes, and excluded one image pending manual review.
- **Source Annotation File:** `data/annotations.json` (preserved without modification).
- **Processed Annotation File:** `data/processed/taco/annotations_bbox_corrected.json`.
- **Processing Script:** `src/correct_taco_bboxes.py`.
- **Processing Report:** `docs/taco_bbox_corrections.json`.
- **Source Images:** 1,500.
- **Processed Images:** 1,499.
- **Source Annotations:** 4,784.
- **Processed Annotations:** 4,778.
- **Bounding Boxes Corrected:** 6.
- **Excluded Image:** ID 679, `batch_15/000078.jpg`.
- **Annotations Excluded With Image:** 6.
- **Reason for Exclusion:** The alignment of annotation 2186 with the actual litter object could not be confidently verified from the available visual review. The image was excluded pending manual review.
- **Structural Validation:** Confirmed that the original source counts remained unchanged, the excluded image and its annotations were absent from the processed copy, and no processed annotations referenced missing images.
- **Limitations:** Segmentation and area fields were not recalculated. The remaining annotations have not all undergone visual review. The processed copy is not yet a final training dataset.
- **Status:** Initial bounding-box processing and structural validation completed.

## Current Research Status

- The project repository has been created and connected to GitHub.
- The research objectives and planned methodology are documented in `README.md`.
- The main computer's hardware has been checked.
- The Python, PyTorch, torchvision, Ultralytics, and GPU environment has been verified.
- The TACO annotation file has been structurally inspected.
- All 1,500 listed TACO image files passed the initial file-integrity validation.
- A processed TACO annotation copy has been created and structurally validated.
- Six bounding boxes were clipped to the verified image boundaries in the processed copy.
- Image ID 679 (`batch_15/000078.jpg`) and its six annotations were excluded from the processed copy pending manual review.
- The original TACO annotation file remains unchanged.
- Structural validation confirmed that no processed annotations reference missing images.
- TACO annotation quality, category distribution, duplicate images, and environmental diversity still require further investigation.
- Compatibility with PlastOPol has not yet been fully assessed.
- The final single-class `Litter` annotation mapping and dataset split strategy have not yet been finalized.
- Model training and experimental evaluation have not yet been performed.
- No experimental model-performance results are available yet.

## Next Action

Continue auditing TACO annotation quality, including visual inspection of bounding-box and segmentation alignment, category distribution, duplicate images, and environmental diversity. Then assess compatibility with PlastOPol before finalizing annotation conversion, dataset preparation, and training splits.

## Research Integrity

- Record actual observations and results.
- Distinguish completed work from planned work.
- Document failures, data-quality concerns, methodological changes, and limitations.
- Do not report unverified measurements as experimental findings.
- Preserve the original dataset and annotations; perform corrections in separate processed copies.
- Keep scripts, configuration files, software versions, and processing reports so that the workflow can be reproduced.
- Record training time, computational cost, and evaluation metrics only after they have actually been measured.
- Treat publication in a Q1 or Q2 journal as an aspiration, not a guaranteed outcome.
