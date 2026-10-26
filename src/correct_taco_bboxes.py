
import json
import math
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SOURCE_FILE = DATA_DIR / "annotations.json"

OUTPUT_DIR = DATA_DIR / "processed" / "taco"
OUTPUT_FILE = OUTPUT_DIR / "annotations_bbox_corrected.json"
REPORT_FILE = ROOT / "docs" / "taco_bbox_corrections.json"

# This image is excluded from the processed dataset pending review.
EXCLUDED_IMAGE_ID = 679
EXCLUDED_ANNOTATION_ID = 2186
EXCLUSION_REASON = (
    "Annotation alignment with the actual litter object has not "
    "been verified; excluded pending manual review."
)

with SOURCE_FILE.open("r", encoding="utf-8") as f:
    original = json.load(f)

corrected = json.loads(json.dumps(original))
images = {img["id"]: img for img in corrected["images"]}

changes = []
review_required = []
skipped = []

# Exclude the entire image and all its annotations in the processed copy.
excluded_image = images.get(EXCLUDED_IMAGE_ID)
if excluded_image is None:
    raise ValueError(f"Image ID {EXCLUDED_IMAGE_ID} was not found.")

excluded_annotations = [
    ann for ann in corrected["annotations"]
    if ann.get("image_id") == EXCLUDED_IMAGE_ID
]

corrected["images"] = [
    img for img in corrected["images"]
    if img["id"] != EXCLUDED_IMAGE_ID
]
corrected["annotations"] = [
    ann for ann in corrected["annotations"]
    if ann.get("image_id") != EXCLUDED_IMAGE_ID
]

review_required.append({
    "annotation_id": EXCLUDED_ANNOTATION_ID,
    "image_id": EXCLUDED_IMAGE_ID,
    "file_name": excluded_image["file_name"],
    "annotations_in_image_excluded": len(excluded_annotations),
    "reason": EXCLUSION_REASON,
    "action": "Image and all its annotations excluded from processed copy"
})

for ann in corrected["annotations"]:
    bbox = ann.get("bbox")

    if (
        not isinstance(bbox, list)
        or len(bbox) != 4
        or any(
            isinstance(v, bool)
            or not isinstance(v, (int, float))
            or not math.isfinite(v)
            for v in bbox
        )
    ):
        skipped.append({
            "annotation_id": ann.get("id"),
            "reason": "Invalid bbox structure or non-finite value"
        })
        continue

    x, y, w, h = bbox

    if w <= 0 or h <= 0:
        skipped.append({
            "annotation_id": ann.get("id"),
            "reason": "Non-positive bbox width or height",
            "original_bbox": bbox
        })
        continue

    image_info = images.get(ann.get("image_id"))
    if image_info is None:
        skipped.append({
            "annotation_id": ann.get("id"),
            "reason": "Image reference missing"
        })
        continue

    image_path = DATA_DIR / image_info["file_name"]

    with Image.open(image_path) as img:
        raw_w, raw_h = img.size
        orientation = img.getexif().get(274, 1)

    metadata_w = image_info["width"]
    metadata_h = image_info["height"]

    if orientation in (5, 6, 7, 8):
        display_w, display_h = raw_h, raw_w
    else:
        display_w, display_h = raw_w, raw_h

    if (metadata_w, metadata_h) != (display_w, display_h):
        review_required.append({
            "annotation_id": ann["id"],
            "image_id": ann["image_id"],
            "file_name": image_info["file_name"],
            "metadata_size": [metadata_w, metadata_h],
            "raw_size": [raw_w, raw_h],
            "exif_orientation": orientation,
            "display_size": [display_w, display_h],
            "original_bbox": bbox,
            "reason": "Image dimensions and annotation coordinates need review"
        })
        continue

    x1 = max(0.0, float(x))
    y1 = max(0.0, float(y))
    x2 = min(float(metadata_w), float(x + w))
    y2 = min(float(metadata_h), float(y + h))

    if x2 <= x1 or y2 <= y1:
        skipped.append({
            "annotation_id": ann["id"],
            "reason": "Box has no positive area after clipping",
            "original_bbox": bbox
        })
        continue

    new_bbox = [x1, y1, x2 - x1, y2 - y1]

    if all(
        math.isclose(
            float(a), float(b), rel_tol=1e-9, abs_tol=1e-7
        )
        for a, b in zip(new_bbox, bbox)
    ):
        continue

    if x < 0 or y < 0 or x + w > metadata_w or y + h > metadata_h:
        changes.append({
            "annotation_id": ann["id"],
            "image_id": ann["image_id"],
            "file_name": image_info["file_name"],
            "image_size": [metadata_w, metadata_h],
            "original_bbox": bbox,
            "corrected_bbox": new_bbox,
            "reason": "Bounding box clipped to verified image boundaries"
        })
        ann["bbox"] = new_bbox

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(corrected, f, ensure_ascii=False, indent=2)

report = {
    "source_file": str(SOURCE_FILE.relative_to(ROOT)),
    "output_file": str(OUTPUT_FILE.relative_to(ROOT)),
    "source_images": len(original["images"]),
    "processed_images": len(corrected["images"]),
    "source_annotations": len(original["annotations"]),
    "processed_annotations": len(corrected["annotations"]),
    "excluded_image_id": EXCLUDED_IMAGE_ID,
    "excluded_annotation_id": EXCLUDED_ANNOTATION_ID,
    "excluded_annotations_in_image": len(excluded_annotations),
    "bounding_boxes_corrected": len(changes),
    "annotations_requiring_review": len(review_required),
    "annotations_skipped": len(skipped),
    "changes": changes,
    "review_required": review_required,
    "skipped": skipped,
    "limitations": [
        "The original annotation file was not modified.",
        "The excluded image remains in the source dataset.",
        "Segmentation and area fields were not recalculated.",
        "Visual inspection of the remaining dataset is still required.",
        "The processed copy is not yet a final training split."
    ]
}

with REPORT_FILE.open("w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("Processing completed.")
print("Source images:", len(original["images"]))
print("Processed images:", len(corrected["images"]))
print("Source annotations:", len(original["annotations"]))
print("Processed annotations:", len(corrected["annotations"]))
print("Excluded image:", EXCLUDED_IMAGE_ID, excluded_image["file_name"])
print("Annotations in excluded image:", len(excluded_annotations))
print("Bounding boxes corrected:", len(changes))
print("Annotations requiring review:", len(review_required))
print("Annotations skipped:", len(skipped))
print("Processed file:", OUTPUT_FILE)
print("Report:", REPORT_FILE)
print("Original source annotations were not modified.")
