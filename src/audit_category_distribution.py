import json
from collections import Counter, defaultdict
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / "data" / "annotations.json"
output = root / "docs" / "taco_category_distribution.json"

with source.open("r", encoding="utf-8") as f:
    data = json.load(f)

categories = {c["id"]: c["name"] for c in data["categories"]}
annotation_counts = Counter()
image_ids_by_category = defaultdict(set)

for ann in data["annotations"]:
    category_id = ann["category_id"]
    annotation_counts[category_id] += 1
    image_ids_by_category[category_id].add(ann["image_id"])

report = {
    "source": "data/annotations.json",
    "total_images": len(data["images"]),
    "total_annotations": len(data["annotations"]),
    "total_categories": len(categories),
    "categories": [
        {
            "category_id": category_id,
            "category_name": name,
            "annotation_count": annotation_counts[category_id],
            "image_count": len(image_ids_by_category[category_id]),
        }
        for category_id, name in sorted(
            categories.items(), key=lambda item: item[1].lower()
        )
    ],
}

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("Category distribution report saved:", output)
print("Images:", report["total_images"])
print("Annotations:", report["total_annotations"])
print("Categories:", report["total_categories"])
print("\nCategories with the most annotations:")

for item in sorted(
    report["categories"],
    key=lambda x: x["annotation_count"],
    reverse=True,
)[:15]:
    print(
        f'{item["category_name"]}: '
        f'{item["annotation_count"]} annotations, '
        f'{item["image_count"]} images'
    )
