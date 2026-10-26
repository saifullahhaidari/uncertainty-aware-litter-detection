
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILE = ROOT / "data" / "processed" / "taco" / "annotations_bbox_corrected.json"
MAPPING_FILE = ROOT / "docs" / "taco_class_mapping.json"
OUTPUT_DIR = ROOT / "data" / "processed" / "taco" / "yolo"
LABEL_DIR = OUTPUT_DIR / "labels"
REPORT_FILE = ROOT / "docs" / "taco_yolo_conversion_report.json"


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data = load_json(SOURCE_FILE)
    mapping_data = load_json(MAPPING_FILE)

    images = data["images"]
    annotations = data["annotations"]

    # Source category ID -> target class ID
    category_map = {
        int(item["source_category_id"]): int(item["target_class_id"])
        for item in mapping_data["categories"]
    }

    target_classes = mapping_data["classes"]
    if target_classes != [{"class_id": 0, "class_name": "Litter"}]:
        raise ValueError("Unexpected target-class definition.")

    image_by_id = {int(img["id"]): img for img in images}
    if len(image_by_id) != len(images):
        raise ValueError("Duplicate image IDs found.")

    annotations_by_image = defaultdict(list)

    for ann in annotations:
        image_id = int(ann["image_id"])
        category_id = int(ann["category_id"])

        if image_id not in image_by_id:
            raise ValueError(
                f"Annotation {ann['id']} references missing image {image_id}."
            )

        if category_id not in category_map:
            raise ValueError(
                f"Annotation {ann['id']} has unmapped category {category_id}."
            )

        annotations_by_image[image_id].append(ann)

    # Validate and convert all boxes before writing output.
    converted = {}
    class_counts = Counter()
    empty_images = 0

    for image_id, img in image_by_id.items():
        image_width = float(img["width"])
        image_height = float(img["height"])

        if image_width <= 0 or image_height <= 0:
            raise ValueError(f"Invalid image dimensions: {img['file_name']}")

        lines = []

        for ann in annotations_by_image[image_id]:
            x, y, box_width, box_height = map(float, ann["bbox"])

            values = [x, y, box_width, box_height]
            if not all(map(lambda v: __import__("math").isfinite(v), values)):
                raise ValueError(f"Non-finite bbox in annotation {ann['id']}.")

            if box_width <= 0 or box_height <= 0:
                raise ValueError(f"Non-positive bbox in annotation {ann['id']}.")

            # Do not silently clip boxes; invalid coordinates need investigation.
            tolerance = 1e-6
            if (
                x < -tolerance
                or y < -tolerance
                or x + box_width > image_width + tolerance
                or y + box_height > image_height + tolerance
            ):
                raise ValueError(
                    f"Out-of-bounds bbox in annotation {ann['id']}: "
                    f"{ann['bbox']} for image {img['file_name']}"
                )

            # Convert COCO [x_min, y_min, width, height]
            # to YOLO [x_center, y_center, width, height].
            x_center = (x + box_width / 2) / image_width
            y_center = (y + box_height / 2) / image_height
            normalized_width = box_width / image_width
            normalized_height = box_height / image_height

            box = [
                x_center,
                y_center,
                normalized_width,
                normalized_height,
            ]

            if not all(0 <= value <= 1 for value in box):
                raise ValueError(
                    f"Invalid normalized bbox in annotation {ann['id']}: {box}"
                )

            class_id = category_map[int(ann["category_id"])]
            lines.append(
                f"{class_id} " + " ".join(f"{value:.8f}" for value in box)
            )
            class_counts[class_id] += 1

        if not lines:
            empty_images += 1

        # Preserve the image's relative folders to avoid filename collisions.
        relative_label = Path(img["file_name"]).with_suffix(".txt")
        converted[relative_label] = lines

    # Write only after every annotation passes validation.
    LABEL_DIR.mkdir(parents=True, exist_ok=True)

    for relative_path, lines in converted.items():
        output_path = LABEL_DIR / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            "\n".join(lines) + ("\n" if lines else ""),
            encoding="utf-8",
        )

    report = {
        "source_file": str(SOURCE_FILE.relative_to(ROOT)),
        "mapping_file": str(MAPPING_FILE.relative_to(ROOT)),
        "output_directory": str(LABEL_DIR.relative_to(ROOT)),
        "processed_image_count": len(images),
        "processed_annotation_count": len(annotations),
        "label_files_written": len(converted),
        "empty_label_files": empty_images,
        "class_counts": dict(class_counts),
        "class_definition": target_classes,
        "conversion": "COCO bbox to normalized YOLO bbox",
        "validation": "All annotations passed coordinate and mapping checks",
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("YOLO conversion completed.")
    print(f"Images: {len(images)}")
    print(f"Annotations converted: {len(annotations)}")
    print(f"Label files written: {len(converted)}")
    print(f"Empty label files: {empty_images}")
    print(f"Class counts: {dict(class_counts)}")
    print(f"Labels: {LABEL_DIR}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
