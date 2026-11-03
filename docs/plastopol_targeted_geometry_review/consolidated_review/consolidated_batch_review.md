# PlastOPol Consolidated Batch Review

## Batch-level evidence

Blank decision counts mean NR: no supported individual batch allocation.

| Batch | Manifest annotations | AI valid | Incorrect bbox | Uncertain | Semantic review | Evidence status |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 19 | 19 | 0 | 0 | 0 | SAVED_AGGREGATE_OR_INDIVIDUAL |
| 2 | 10 | 10 | 0 | 0 | 0 | SAVED_AGGREGATE_OR_INDIVIDUAL |
| 3 | 10 | 10 | 0 | 0 | 0 | SAVED_AGGREGATE_OR_INDIVIDUAL |
| 4 | 13 | 13 | 0 | 0 | 0 | SAVED_AGGREGATE_OR_INDIVIDUAL |
| 6 | 32 | NR | NR | NR | NR | INCOMPLETE_DETAILS |
| 7 | 21 | 20 | 0 | 0 | 1 | AI_REVIEW_RECORDED |
| 8 | 20 | 20 | 0 | 0 | 0 | AI_REVIEW_RECORDED |
| 9 | 20 | NR | NR | NR | NR | NOT_RECORDED |
| 10 | 16 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 11 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 12 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 13 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 14 | 10 | NR | NR | NR | NR | MIXED_EVIDENCE |
| 15 | 10 | NR | NR | NR | NR | MIXED_EVIDENCE |
| 16 | 10 | NR | NR | NR | NR | MIXED_EVIDENCE |
| 17 | 10 | NR | NR | NR | NR | MIXED_EVIDENCE |
| 18 | 10 | NR | NR | NR | NR | MIXED_EVIDENCE |
| 19 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 20 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 21 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 22 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 23 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 24 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 25 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 26 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 27 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 28 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 29 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 30 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 31 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 32 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 33 | 10 | NR | NR | NR | NR | GROUP_RESULT_ONLY |
| 34 | 10 | 10 | 0 | 0 | 0 | FULL_RESOLUTION_FOLLOWUP |
| 35 | 10 | 10 | 0 | 0 | 0 | FULL_RESOLUTION_FOLLOWUP |

## Combined group-level AI findings

| Group | Images | Annotations | AI findings | Evidence |
|---|---:|---:|---|---|
| Batches 10-13 | 40 | 46 | 34 assessed; 32 initial pass; 2 adjustment; 12 pending | conversation_recorded |
| Batches 19-23 | 50 | 50 | 50/50 valid | conversation_recorded |
| Batches 24-28 | 50 | 50 | 45 valid; 1 incorrect bbox; 4 semantic review | conversation_recorded |
| Batches 29-33 | 50 | 50 | 45 valid; 1 incorrect bbox; 1 uncertain; 3 semantic review | conversation_recorded |

## Research limitations

- Gemini results are AI-assisted evidence, not human ground truth.
- Human review remains pending.
- Geometry warnings are not proof of incorrect annotations.
- Combined results are not distributed across individual batches.
- The difference between 412 initial flagged annotations and 411 manifest IDs remains unresolved.
- Source annotations, review ledger and research log were not modified.


## Batch 34-35: Full-Resolution Follow-up and Identity Verification

### AI-assisted follow-up

- Batch 34: 10 AI-valid, 0 incorrect bounding boxes, 0 uncertain, and 0 semantic-review outcomes.
- Batch 35: 10 AI-valid, 0 incorrect bounding boxes, 0 uncertain, and 0 semantic-review outcomes.
- The follow-up reported High confidence. The four initial concerns (Annotation IDs 4652, 4732, 5165, and 5210) were subsequently reported as `VALID`.
- The follow-up also reported that the identified missing-object candidates were already covered.
- These findings are conversation-recorded AI-assisted evidence, not independent human ground truth.

### Source identity verification

- Result: `PASS`.
- Eight images were checked against the original PlastOPol source; all eight passed.
- Evidence: `docs/plastopol_targeted_geometry_review/batches_34_35_full_resolution/source_consistency_check.csv`.
- Verified mappings:
  - Annotation 4652 ? image 2208 ? `263767.jpg`.
  - Annotation 4732 ? image 2225 ? `412201.jpg`.
  - Annotation 5165 ? image 2375 ? `135720.jpg`.
  - Annotation 5210 ? image 2392 ? `204405.jpg`.
  - Annotation 5225 ? image 2394 ? `135900.jpg`.

### Interpretation and limitations

- Source identity verification confirms the correspondence of image IDs, filenames, and annotation records. It does not prove that bounding boxes or semantic labels are correct.
- The eight-image consistency check and the 20-annotation AI follow-up are separate evidence records.
- Human review for these batches remains pending.
- No original source annotations or review ledgers were modified by this documentation update.
