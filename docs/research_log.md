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

## Entry 011 - PlastOPol Geometry-Focused External Annotation Review (Batches 01 and 02)

- Date: 2026-10-30
- Dataset: PlastOPol, version 1.0
- Review scope: Targeted review of images selected by heuristic geometry flags.
- Selection source: `docs/plastopol_bbox_review_candidates.json`
- Review batches: `docs/plastopol_targeted_geometry_review/review_batch_01.json` and `review_batch_02.json`
- Review image-generation script: `src/create_plastopol_geometry_review.py`
- Annotation crop-generation script: `src/create_plastopol_annotation_crops.py`
- Review ledger: `docs/plastopol_annotation_review_ledger.csv`
- Batch 01 external review summary: `docs/plastopol_targeted_geometry_review/batch_01/external_review_summary.json`
- Batch 02 external review summary: `docs/plastopol_targeted_geometry_review/batch_02/external_review_summary.json`
- Total images reviewed externally: 20.
- Total unique annotations reviewed externally: 29.
- Batch 01: 10 images and 19 annotations; Gemini decisions: 19 VALID, 0 INCORRECT_BBOX, 0 UNCERTAIN, and 0 NEEDS_SEMANTIC_REVIEW.
- Batch 02: 10 images and 10 annotations; Gemini decisions: 10 VALID, 0 INCORRECT_BBOX, 0 UNCERTAIN, and 0 NEEDS_SEMANTIC_REVIEW.
- External reviewer confidence: All 29 decisions were reported as High confidence.
- Identity verification: Batch 02 image IDs, filenames, and annotation IDs were cross-checked against the original `full_plastopol.json`; all 10 image-annotation identities passed.
- Identity correction: The initial Gemini response contained incorrect annotation IDs for nine Batch 02 records. The decisions were associated with source annotations only after verifying the image identities and confirming that each selected image contained exactly one flagged annotation. Correct IDs were recorded in the ledger.
- Source-data integrity: No original PlastOPol annotations or bounding boxes were modified.
- Human review status: All 29 records remain pending human review; no human decisions are claimed.
- Limitations: This is external AI-assisted visual review, not independent human ground truth. Only 20 of the 341 geometry-flagged candidate images have been reviewed in these two batches. Visual inspection does not establish semantic completeness or correctness of all dataset annotations.
- Research status: Two targeted external-review batches completed and documented. Geometry review of the remaining candidates is ongoing. Model training and experimental evaluation have not been performed.

## Entry 012 - PlastOPol Geometry-Focused External Review (Batch 03)

- Date: 2026-10-31
- Dataset: PlastOPol, version 1.0
- Review scope: Third targeted batch selected from the geometry-flagged candidate images.
- Batch manifest: `docs/plastopol_targeted_geometry_review/review_batch_03.json`
- Review materials: `docs/plastopol_targeted_geometry_review/batch_03/`
- Review-generation script: `src/create_plastopol_geometry_review.py`
- External review summary: `docs/plastopol_targeted_geometry_review/batch_03/external_review_summary.json`
- Review ledger: `docs/plastopol_annotation_review_ledger.csv`
- Sample size: 10 images and 10 flagged annotations.
- External reviewer: Gemini.
- External decisions: 10 VALID, 0 INCORRECT_BBOX, 0 UNCERTAIN, and 0 NEEDS_SEMANTIC_REVIEW.
- Reported confidence: High for all 10 decisions.
- Source identity verification: All 10 image IDs and filenames matched `full_plastopol.json`; image dimensions matched the source; all 10 flagged annotation IDs were confirmed to belong to their corresponding images.
- Identity verification outcome: PASS; zero failed checks.
- Review material limitation: Gemini reported evaluating the attached image panel named `1a.jpg`. Individual full-resolution review of all 10 images was not independently confirmed.
- Human review status: All 10 records remain pending human review. Gemini decisions are external AI-assisted assessments, not human ground truth.
- Ledger update: 10 records added; total ledger size increased from 29 to 39 records. A pre-update backup was preserved.
- Source-data integrity: Original PlastOPol images and annotations were not modified.
- Cumulative external review across Batches 01-03: 30 images and 39 unique annotations; all 39 external decisions were VALID with High reported confidence.
- Coverage limitation: Only 30 of the 341 geometry-flagged candidate images have received external AI-assisted review. The remaining candidates have not all been reviewed.
- Research status: Batch 03 external review and documentation completed. Human review remains pending. Model training and experimental evaluation have not been performed.

## Entry 013 — PlastOPol Targeted Geometry Review: Batch 04

- **Date:** 2026-10-31
- **Dataset:** PlastOPol v1.0.
- **Review scope:** The fourth targeted batch, selected from the next unreviewed priority candidates (priority positions 31?40).
- **Batch manifest:** `docs/plastopol_targeted_geometry_review/review_batch_04.json`.
- **Review materials:** `docs/plastopol_targeted_geometry_review/batch_04/`.
- **External response:** `docs/plastopol_targeted_geometry_review/batch_04/gemini_response.json`.
- **External review summary:** `docs/plastopol_targeted_geometry_review/batch_04/external_review_summary.json`.
- **Annotation ledger:** `docs/plastopol_annotation_review_ledger.csv`.

### Results

- 10 images and 13 flagged annotation instances were included.
- All 13 external decisions were `VALID`, with `High` confidence.
- No `INCORRECT`, `UNCERTAIN`, or `SEMANTIC_REVIEW` decisions were returned.
- Image identity, filenames, image dimensions, annotation ownership, and source bounding-box correspondence passed verification.
- The annotation-level ledger increased from 39 to 52 records.
- The 13 new records were added with human review status still `pending` and reviewer decision `not_assessed`.
- A pre-update ledger backup was saved as `docs/plastopol_annotation_review_ledger.before_batch_04.csv`.

### Limitations and research integrity

- Gemini's decisions are external AI review results, not human ground truth.
- The exact visual materials inspected by Gemini were not independently confirmed.
- Citation markers included in the Gemini response were not treated as verified evidence.
- A `VALID` geometric decision does not establish semantic completeness or prove that all litter objects in an image were annotated.
- The original PlastOPol source annotations were not modified.
- Human review remains pending for all 52 externally reviewed annotation records.

### Cumulative status

Across Batches 01?04, 40 unique candidate images and 52 unique flagged annotations have received external AI review. All 52 decisions were `VALID` with `High` confidence. This is a priority-based review sample, not a representative statistical sample of all 341 candidate images. No model training or performance evaluation has been conducted.


## Current Research Status

### Dataset preparation

- **TACO:** The processed one-class dataset contains 1,499 images and 4,778 annotations. Image ID 679 remains excluded pending manual review.
- **PlastOPol:** The one-class YOLO dataset contains 2,418 images and 5,300 annotations across train, validation, and test splits. Automated YOLO quality audit passed with zero errors and zero warnings.
- **PlastOPol geometry review:** Four priority batches have been externally reviewed: 40 unique images and 52 flagged annotations. Gemini returned `VALID` with `High` confidence for all 52.
- **Human review:** All 52 externally reviewed annotation records remain pending human assessment. External AI review must not be interpreted as human ground truth.
- **Review coverage:** The four batches cover 40 of 341 geometry-review candidate images. The sample is priority-based and does not support generalizing an error rate to all candidates.
- **Source integrity:** Original dataset annotations have been preserved; corrections and converted labels are stored separately.

### Model and evaluation

- Model training has not started.
- Cross-dataset performance evaluation has not started.
- Uncertainty estimation and inference/resource measurements remain planned work.


## Next Action

1. Assess whether the current geometry-review coverage is sufficient or whether further priority batches are needed. Consider coverage of different flag types rather than relying only on the number of reviewed images.
2. Plan independent human assessment for the pending records, especially ambiguous geometry and semantic completeness cases.
3. Resolve the remaining dataset-audit decisions, including the TACO image excluded pending manual review.
4. After dataset preparation and review decisions are sufficiently documented, finalize the cross-dataset experimental protocol and leakage-safe evaluation plan.
5. Begin model training only after the dataset versions, splits, class mapping, and evaluation protocol are frozen and documented.


## Research Integrity

- Record actual observations and results.
- Distinguish completed work from planned work.
- Document failures, data-quality concerns, methodological changes, and limitations.
- Do not report unverified measurements as experimental findings.
- Preserve the original dataset and annotations; perform corrections in separate processed copies.
- Keep scripts, configuration files, software versions, and processing reports so that the workflow can be reproduced.
- Record training time, computational cost, and evaluation metrics only after they have actually been measured.
- Treat publication in a Q1 or Q2 journal as an aspiration, not a guaranteed outcome.
