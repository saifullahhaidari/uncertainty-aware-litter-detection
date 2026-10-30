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

- The project repository is connected to GitHub, and the research objectives and planned methodology are documented in `README.md`.
- The Python, PyTorch, Ultralytics, and CUDA environment has been verified.
- TACO source annotations and image integrity have been audited. Its processed copy contains 1,499 images and 4,778 annotations mapped to the target class `Litter`.
- TACO YOLO conversion and automated label-quality auditing are complete: 1,499 label files, 4,778 boxes, zero reported errors, and zero warnings.
- A visual sample of 12 TACO images was inspected; boxes appeared aligned in the reviewed samples.
- PlastOPol source provenance, archive integrity, image integrity, annotation structure, bounding-box geometry, and split integrity have been audited.
- All 2,418 PlastOPol images passed image validation. The dataset contains 5,300 annotations in the source category `Trash`.
- PlastOPol YOLO conversion is complete. The source category `Trash` was mapped to the common target class `Litter`.
- PlastOPol conversion produced 1,547 training images, 387 validation images, and 484 test images, with 5,300 bounding boxes in total.
- Automated PlastOPol YOLO quality auditing passed: 2,418 image files, 2,418 label files, 5,300 boxes, zero empty label files, zero errors, and zero warnings.
- A random visual audit sample of 12 converted PlastOPol images was inspected, with four images from each split. The bounding boxes appeared generally aligned with the visible litter objects in the reviewed samples.
- The 341 images flagged by heuristic geometry checks remain candidates for further targeted human review. These flags are review indicators, not confirmed annotation errors.
- The visual inspection of 12 images does not establish complete visual or semantic correctness across either dataset.
- Cross-dataset split strategy, experimental protocols, and final compatibility decisions still need to be established.
- Model training and experimental evaluation have not yet been performed. No model-performance results are available.

## Next Action

Continue the targeted review of PlastOPol geometry-review candidates and assess cross-dataset annotation compatibility. Then define and document leakage-safe dataset splits and experimental protocols for in-domain and cross-domain evaluation before model training.

## Research Integrity

- Record actual observations and results.
- Distinguish completed work from planned work.
- Document failures, data-quality concerns, methodological changes, and limitations.
- Do not report unverified measurements as experimental findings.
- Preserve the original dataset and annotations; perform corrections in separate processed copies.
- Keep scripts, configuration files, software versions, and processing reports so that the workflow can be reproduced.
- Record training time, computational cost, and evaluation metrics only after they have actually been measured.
- Treat publication in a Q1 or Q2 journal as an aspiration, not a guaranteed outcome.

## Entry 007 — YOLO Label Geometry Quality Audit
- Date: 2026-10-26
- Dataset: Processed TACO
- Label files checked: 1499
- Bounding boxes checked: 4778
- Empty label files: 0
- Geometry/structure errors: 0
- Warnings: 0
- Visual inspection: 12 randomly selected images reviewed; boxes appeared aligned in the reviewed samples.
- Report: docs/taco_yolo_quality_audit.json
- Script: src/audit_yolo_labels.py
- Limitation: Automated geometry checks do not establish complete visual or semantic correctness.

## Entry 008 - PlastOPol Source Review

- Date: 2026-10-28
- Dataset: PlastOPol
- Source reviewed: Wageningen University & Research dataset record and the original 2022 paper.
- Version 1.0 DOI: https://doi.org/10.5281/zenodo.5829156
- All versions DOI: https://doi.org/10.5281/zenodo.5829155
- Published image count: 2418
- Published litter instance count: 5300
- Published target class: Litter (single class)
- Published bounding-box format: x1, y1, width, height
- License: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Status: Source-level review completed; downloaded files and their actual structure have not yet been inspected.
- Next step: Inspect the dataset archive, annotation format, and file structure before downloading or processing the data.

## Entry 009 - PlastOPol Dataset Integrity and Annotation Audit

- Date: 2026-10-30
- Dataset: PlastOPol, version 1.0
- Source DOI: https://doi.org/10.5281/zenodo.5829156
- Dataset license: Creative Commons Attribution 4.0 International (CC BY 4.0)
- Archive integrity: The downloaded outer archive passed its recorded MD5 checksum verification.
- Dataset contents: The image archive and annotation-fold archive were preserved; 2,418 images and 13 annotation JSON files were extracted and inspected.
- Full annotation file: 2,418 images and 5,300 annotations in one source category, `Trash`.
- Image validation: All 2,418 annotated images were extracted and fully readable. No missing images, corrupt images, unreadable files, or image-dimension mismatches were reported.
- Annotation structure: No duplicate image IDs, filenames, or annotation IDs; no missing image/category references; no invalid bounding-box formats or invalid numerical values were detected.
- Bounding-box geometry: 5,300 annotations passed the numerical geometry checks. No invalid geometry was reported.
- Heuristic geometry review: 322 boundary-touching, 27 very-small, 87 very-large, and 10 extreme-aspect-ratio flags were reported. These categories may overlap and are review indicators, not confirmed annotation errors.
- Review candidates: 341 unique images and 412 unique flagged annotations were selected for further inspection; 39 images had more than one flag type.
- Split integrity: The train/validation and test partitions had no overlap and their union matched the full dataset.
- Fold integrity: All five train/validation folds passed the checks for zero overlap and complete coverage of the train/validation dataset.
- YOLO coordinate readiness: All 5,300 bounding boxes passed numerical checks for conversion to normalized YOLO coordinates. This was a pre-conversion validation, not a completed YOLO conversion.
- Visual review materials: A random sample contact sheet and targeted review materials were generated. Manual visual and semantic review remains incomplete.
- Reports: `docs/plastopol_image_validation.json`, `docs/plastopol_fold_integrity_audit.json`, `docs/plastopol_bbox_geometry_audit.json`, `docs/plastopol_bbox_review_candidates.json`, and `docs/plastopol_visual_audit_manifest.json`.
- Limitation: Automated structural and geometric checks cannot establish that every litter item has been annotated correctly or that every bounding box is semantically accurate.
- Next step: Complete the targeted human review, finalize cross-dataset class harmonization, and generate and audit PlastOPol YOLO labels.

## Entry 010 - PlastOPol YOLO Conversion and Quality Audit

- Date: 2026-10-30
- Dataset: PlastOPol, version 1.0
- Source annotations: `data/raw/plastopol/annotations/`
- Source image directory: `data/raw/plastopol/images/`
- Target class: `Litter` (class ID 0)
- Source-to-target mapping: `Trash` -> `Litter`
- Conversion script: `src/convert_plastopol_to_yolo.py`
- Conversion report: `docs/plastopol_yolo_conversion_report.json`
- Output dataset configuration: `data/processed/plastopol/yolo/dataset.yaml`
- Processed output: `data/processed/plastopol/yolo/`
- Training split: 1,547 images, 1,547 label files, 3,326 bounding boxes.
- Validation split: 387 images, 387 label files, 863 bounding boxes.
- Test split: 484 images, 484 label files, 1,111 bounding boxes.
- Total converted data: 2,418 images, 2,418 label files, and 5,300 bounding boxes.
- Empty label files: 0.
- Automated audit script: `src/audit_plastopol_yolo.py`
- Automated audit report: `docs/plastopol_yolo_quality_audit.json`
- Automated audit outcome: PASS; zero errors and zero warnings. All three splits passed the implemented image-label pairing, label structure, class ID, numerical, and normalized bounding-box geometry checks.
- Visual audit script: `src/create_plastopol_yolo_visual_audit.py`
- Visual audit image: `docs/plastopol_yolo_visual_audit/plastopol_yolo_visual_audit.png`
- Visual audit manifest: `docs/plastopol_yolo_visual_audit/manifest.json`
- Visual audit sampling: 12 randomly selected images using seed 42, with four images from each of the training, validation, and test splits.
- Visual review outcome: Bounding boxes appeared generally aligned with the visible litter objects in the reviewed sample.
- Limitations: Visual inspection covered only 12 images and does not establish complete annotation correctness. The 341 images previously flagged by heuristic geometry checks remain candidates for targeted review. Automated checks cannot establish semantic completeness or detect every missed litter object.
- Research status: PlastOPol YOLO conversion and post-conversion automated auditing completed. Model training and experimental evaluation have not been performed.
