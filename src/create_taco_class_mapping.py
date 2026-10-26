import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = (
    ROOT / "data" / "processed" / "taco"
    / "annotations_bbox_corrected.json"
)
OUTPUT_FILE = ROOT / "docs" / "taco_class_mapping.json"

with DATA_FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)

counts = Counter(
    ann["category_id"] for ann in data["annotations"]
)
categories = sorted(data["categories"], key=lambda c: c["id"])

mapping = {
    "source": "data/processed/taco/annotations_bbox_corrected.json",
    "task": "single-class litter object detection",
    "mapping_policy": (
        "Map every TACO category to class_id 0 (Litter). "
        "Categories with zero annotations contribute no training instances."
    ),
    "classes": [
        {"class_id": 0, "class_name": "Litter"}
    ],
    "categories": [
        {
            "source_category_id": c["id"],
            "source_category_name": c["name"],
            "target_class_id": 0,
            "target_class_name": "Litter",
            "annotation_count": counts[c["id"]],
            "has_instances": counts[c["id"]] > 0,
        }
        for c in categories
    ],
    "processed_image_count": len(data["images"]),
    "processed_annotation_count": len(data["annotations"]),
    "source_category_count": len(categories),
    "categories_with_instances": sum(
        counts[c["id"]] > 0 for c in categories
    ),
    "categories_without_instances": sum(
        counts[c["id"]] == 0 for c in categories
    ),
}

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text(
    json.dumps(mapping, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("Class mapping report saved:", OUTPUT_FILE)
print("Processed images:", mapping["processed_image_count"])
print("Processed annotations:", mapping["processed_annotation_count"])
print("Source categories:", mapping["source_category_count"])
print("Categories with instances:", mapping["categories_with_instances"])
print("Categories without instances:", mapping["categories_without_instances"])
print("Target class: 0 = Litter")
