import json
import math
import shutil
from pathlib import Path
from collections import defaultdict

from PIL import Image

ROOT = Path("data/raw/plastopol")
ANNOTATION_DIR = ROOT / "annotations"
IMAGE_DIR = ROOT / "images"

OUTPUT = Path("data/processed/plastopol/yolo")
REPORT = Path("docs/plastopol_yolo_conversion_report.json")

SPLITS = {
    "train": "plastopol_train_fold-1.json",
    "val": "plastopol_val_fold-1.json",
    "test": "plastopol_test.json",
}

CLASS_ID = 0
CLASS_NAME = "Litter"


def load_and_validate(split, filename):
    annotation_path = ANNOTATION_DIR / filename
    data = json.loads(annotation_path.read_text(encoding="utf-8"))

    images = data["images"]
    annotations = data["annotations"]
    categories = data["categories"]

    if len(categories) != 1 or categories[0]["name"] != "Trash":
        raise ValueError(f"{split}: unexpected category structure")

    image_map = {}

    for image in images:
        image_id = image["id"]
        filename = image["file_name"]

        if image_id in image_map:
            raise ValueError(f"{split}: duplicate image ID {image_id}")

        if Path(filename).name != filename:
            raise ValueError(f"{split}: unsafe filename: {filename}")

        if filename in [item["file_name"] for item in image_map.values()]:
            raise ValueError(f"{split}: duplicate filename {filename}")

        if image["width"] <= 0 or image["height"] <= 0:
            raise ValueError(f"{split}: invalid image dimensions: {filename}")

        image_path = IMAGE_DIR / filename

        if not image_path.is_file():
            raise FileNotFoundError(image_path)

        image_map[image_id] = image

    labels = defaultdict(list)

    for ann in annotations:
        image_id = ann["image_id"]

        if image_id not in image_map:
            raise ValueError(f"{split}: unknown image ID {image_id}")

        if ann["category_id"] != categories[0]["id"]:
            raise ValueError(f"{split}: unexpected category ID")

        bbox = ann["bbox"]

        if len(bbox) != 4:
            raise ValueError(f"{split}: invalid bbox length")

        if not all(
            isinstance(v, (int, float)) and
            not isinstance(v, bool) and
            math.isfinite(v)
            for v in bbox
        ):
            raise ValueError(f"{split}: non-numeric bbox")

        x, y, w, h = bbox
        image = image_map[image_id]
        image_width = image["width"]
        image_height = image["height"]

        if w <= 0 or h <= 0:
            raise ValueError(f"{split}: non-positive bbox")

        if x < 0 or y < 0:
            raise ValueError(f"{split}: negative bbox origin")

        if x + w > image_width or y + h > image_height:
            raise ValueError(f"{split}: bbox outside image")

        x_center = (x + w / 2) / image_width
        y_center = (y + h / 2) / image_height
        width = w / image_width
        height = h / image_height

        values = [x_center, y_center, width, height]

        if not all(0 <= value <= 1 for value in values):
            raise ValueError(f"{split}: normalized bbox outside [0, 1]")

        labels[image_id].append(
            f"{CLASS_ID} " + " ".join(f"{v:.8f}" for v in values)
        )

    return images, labels, len(annotations)


def main():
    if OUTPUT.exists() and any(OUTPUT.iterdir()):
        raise FileExistsError(
            f"Output directory is not empty: {OUTPUT}\n"
            "Do not overwrite existing conversion."
        )

    prepared = {}
    all_filenames = {}
    total_annotations = 0

    print("STEP 1: Loading and validating source annotations")

    for split, json_file in SPLITS.items():
        images, labels, annotation_count = load_and_validate(
            split, json_file
        )

        prepared[split] = (images, labels, annotation_count)
        all_filenames[split] = {img["file_name"] for img in images}
        total_annotations += annotation_count

        print(
            f"{split}: {len(images)} images, "
            f"{annotation_count} annotations"
        )

    print("\nSTEP 2: Checking split overlap")

    for first, second in [
        ("train", "val"),
        ("train", "test"),
        ("val", "test"),
    ]:
        overlap = all_filenames[first] & all_filenames[second]

        if overlap:
            raise ValueError(
                f"Image overlap between {first} and {second}: "
                f"{len(overlap)}"
            )

    print("No filename overlap found.")

    print("\nSTEP 3: Checking actual image dimensions")

    for split, (images, _, _) in prepared.items():
        for item in images:
            image_path = IMAGE_DIR / item["file_name"]

            with Image.open(image_path) as image:
                actual_width, actual_height = image.size

            if (
                actual_width != item["width"]
                or actual_height != item["height"]
            ):
                raise ValueError(
                    f"Dimension mismatch: {item['file_name']}"
                )

        print(f"{split}: image dimensions verified ({len(images)})")

    print("\nSTEP 4: Creating YOLO dataset")

    summary = {}

    for split, (images, labels, annotation_count) in prepared.items():
        image_output = OUTPUT / "images" / split
        label_output = OUTPUT / "labels" / split

        image_output.mkdir(parents=True, exist_ok=True)
        label_output.mkdir(parents=True, exist_ok=True)

        empty_labels = 0
        copied_images = 0
        written_boxes = 0

        for item in images:
            filename = item["file_name"]
            image_source = IMAGE_DIR / filename
            image_target = image_output / filename

            shutil.copy2(image_source, image_target)
            copied_images += 1

            label_lines = labels.get(item["id"], [])

            label_path = label_output / f"{Path(filename).stem}.txt"

            label_path.write_text(
                "\n".join(label_lines) + ("\n" if label_lines else ""),
                encoding="utf-8"
            )

            if not label_lines:
                empty_labels += 1

            written_boxes += len(label_lines)

        if written_boxes != annotation_count:
            raise RuntimeError(f"{split}: annotation count mismatch")

        summary[split] = {
            "images": copied_images,
            "annotations": written_boxes,
            "label_files": len(images),
            "empty_label_files": empty_labels,
        }

        print(
            f"{split}: copied={copied_images}, "
            f"labels={len(images)}, boxes={written_boxes}, "
            f"empty_labels={empty_labels}"
        )

    print("\nSTEP 5: Writing dataset.yaml")

    yaml_text = (
        "path: .\n"
        "train: images/train\n"
        "val: images/val\n"
        "test: images/test\n"
        "names:\n"
        "  0: Litter\n"
    )

    (OUTPUT / "dataset.yaml").write_text(
        yaml_text, encoding="utf-8"
    )

    report = {
        "dataset": "PlastOPol",
        "source_category": "Trash",
        "target_class": CLASS_NAME,
        "target_class_id": CLASS_ID,
        "conversion": "COCO xywh pixels to normalized YOLO xywh",
        "splits": summary,
        "total_images": sum(v["images"] for v in summary.values()),
        "total_annotations": total_annotations,
        "source_images_modified": False,
    }

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    print("\nCONVERSION COMPLETE")
    print("Output:", OUTPUT)
    print("Dataset YAML:", OUTPUT / "dataset.yaml")
    print("Report:", REPORT)
    print("Total images:", report["total_images"])
    print("Total annotations:", report["total_annotations"])


if __name__ == "__main__":
    main()
