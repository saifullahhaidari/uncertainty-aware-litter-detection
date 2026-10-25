# Research Log

## Project

**Title:** Uncertainty-Aware Cross-Domain Evaluation of Lightweight Outdoor Litter Detectors

## Purpose

This log records project activities, decisions, evidence, problems, and next steps. Entries reflect work that has actually been performed. Planned work is clearly distinguished from completed work.

## Entry 001 — Project Repository Setup

- **Date:** 2026-10-23
- **Activity:** Created the public GitHub repository.
- **Repository:** https://github.com/saifullahhaidari/uncertainty-aware-litter-detection
- **Outcome:** The repository and initial README.md were created.
- **Evidence:** Initial repository commit and README.md in GitHub.
- **Status:** Completed.

## Entry 002 — Hardware Verification

- **Date:** 2026-10-23
- **Activity:** Checked the main computer's hardware specifications.
- **CPU:** Intel Core i7-12700.
- **GPU:** NVIDIA GeForce GTX 1660 SUPER.
- **GPU Memory:** 6 GB dedicated VRAM.
- **RAM:** 16 GB.
- **Storage:** Approximately 350 GB free on drive D: and approximately 15 GB free on drive C: at the time of checking.
- **Outcome:** Hardware specifications were recorded for planning future experiments.
- **Limitation:** Hardware suitability depends on the selected model, image size, batch size, and software requirements.
- **Status:** Completed.

## Entry 003 — Software Environment Verification

- **Date:** 2026-10-23
- **Activity:** Verified the Python machine-learning environment and GPU availability.
- **Python:** 3.10.11.
- **PyTorch:** 2.6.0+cu124.
- **Torchvision:** 0.21.0+cu124.
- **CUDA Availability in PyTorch:** True.
- **GPU Detected by PyTorch:** NVIDIA GeForce GTX 1660 SUPER.
- **Ultralytics:** 8.4.188.
- **Outcome:** The core software environment and GPU access were verified.
- **Limitation:** Successful environment verification does not establish model-training performance.
- **Status:** Completed.

## Entry 004 — TACO Annotation Inspection

- **Date:** 2026-10-25
- **Activity:** Downloaded and inspected the official TACO annotation file.
- **Annotation File:** `data/annotations.json`.
- **Images Listed:** 1,500.
- **Annotations:** 4,784.
- **Categories:** 60.
- **Structural Checks:** No missing image references or category references were found in the checks performed.
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

## Current Research Status

- The project repository has been created.
- The research objectives and planned methodology are documented in README.md.
- The main computer's hardware has been checked.
- The Python, PyTorch, torchvision, Ultralytics, and GPU environment has been verified.
- The TACO annotation file has been structurally inspected.
- The 1,500 listed TACO image files passed the initial file-integrity validation.
- TACO annotation quality, duplicate images, category distribution, and environmental diversity still require further investigation.
- Compatibility with PlastOPol has not yet been fully assessed.
- Model training and experimental evaluation have not yet been performed.
- No experimental model-performance results are available yet.

## Next Action

Audit the TACO dataset for annotation quality, category distribution, duplicate images, and environmental diversity before deciding how to prepare the dataset for model training.

## Research Integrity

Record actual observations and results. Distinguish completed work from planned work. Document failures, data-quality concerns, methodological changes, and limitations. Do not report unverified measurements as experimental findings.
