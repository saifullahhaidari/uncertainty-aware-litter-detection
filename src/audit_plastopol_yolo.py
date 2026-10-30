import json
import math
from pathlib import Path
from PIL import Image

ROOT = Path("data/processed/plastopol/yolo")
REPORT = Path("docs/plastopol_yolo_quality_audit.json")

EXPECTED = {
    "train": {"images": 1547, "boxes": 3326},
    "val":   {"images": 387,  "boxes": 863},
    "test":  {"images": 484,  "boxes": 1111},
}

report = {
    "dataset": "PlastOPol",
    "format": "YOLO",
    "splits": {},
    "total_images": 0,
    "total_label_files": 0,
    "total_boxes": 0,
    "errors": [],
    "warnings": [],
}

for split, expected in EXPECTED.items():
    image_dir = ROOT / "images" / split
    label_dir = ROOT / "labels" / split

    images = sorted(
        p for p in image_dir.iterdir()
        if p.is_file()
    )

    labels = sorted(label_dir.glob("*.txt"))

    image_stems = [p.stem for p in images]
    label_stems = [p.stem for p in labels]

    if len(image_stems) != len(set(image_stems)):
        report["errors"].append(f"{split}: duplicate image stems")

    if len(label_stems) != len(set(label_stems)):
        report["errors"].append(f"{split}: duplicate label stems")

    missing_labels = set(image_stems) - set(label_stems)
    orphan_labels = set(label_stems) - set(image_stems)

    if missing_labels:
        report["errors"].append(
            f"{split}: {len(missing_labels)} images without labels"
        )

    if orphan_labels:
        report["errors"].append(
            f"{split}: {len(orphan_labels)} labels without images"
        )

    box_count = 0
    empty_labels = 0
    invalid_lines = 0
    invalid_geometry = 0
    invalid_classes = 0
    unreadable_images = 0

    for image_path in images:
        try:
            with Image.open(image_path) as image:
                image.verify()
        except Exception:
            unreadable_images += 1
            report["errors"].append(
                f"{split}: unreadable image {image_path.name}"
            )

    for label_path in labels:
        content = label_path.read_text(encoding="utf-8").strip()

        if not content:
            empty_labels += 1
            continue

        for line_number, line in enumerate(content.splitlines(), 1):
            parts = line.split()

            if len(parts) != 5:
                invalid_lines += 1
                report["errors"].append(
                    f"{split}: {label_path.name}, line {line_number}: "
                    "expected 5 columns"
                )
                continue

            try:
                class_id = int(parts[0])
                values = [float(v) for v in parts[1:]]
            except ValueError:
                invalid_lines += 1
                report["errors"].append(
                    f"{split}: {label_path.name}, line {line_number}: "
                    "non-numeric value"
                )
                continue

            if class_id != 0:
                invalid_classes += 1
                report["errors"].append(
                    f"{split}: unexpected class ID {class_id}"
                )

            if not all(math.isfinite(v) for v in values):
                invalid_geometry += 1
                report["errors"].append(
                    f"{split}: non-finite coordinate in {label_path.name}"
                )
                continue

            xc, yc, width, height = values

            if not (
                0 <= xc <= 1
                and 0 <= yc <= 1
                and 0 < width <= 1
                and 0 < height <= 1
                and xc - width / 2 >= -1e-7
                and yc - height / 2 >= -1e-7
                and xc + width / 2 <= 1 + 1e-7
                and yc + height / 2 <= 1 + 1e-7
            ):
                invalid_geometry += 1
                report["errors"].append(
                    f"{split}: invalid normalized geometry "
                    f"in {label_path.name}, line {line_number}"
                )

            box_count += 1

    if len(images) != expected["images"]:
        report["errors"].append(f"{split}: unexpected image count")

    if len(labels) != expected["images"]:
        report["errors"].append(f"{split}: unexpected label count")

    if box_count != expected["boxes"]:
        report["errors"].append(f"{split}: unexpected box count")

    report["splits"][split] = {
        "images": len(images),
        "label_files": len(labels),
        "boxes": box_count,
        "empty_label_files": empty_labels,
        "unreadable_images": unreadable_images,
        "invalid_lines": invalid_lines,
        "invalid_classes": invalid_classes,
        "invalid_geometry": invalid_geometry,
        "missing_labels": len(missing_labels),
        "orphan_labels": len(orphan_labels),
    }

    report["total_images"] += len(images)
    report["total_label_files"] += len(labels)
    report["total_boxes"] += box_count

    print(
        f"{split}: images={len(images)}, labels={len(labels)}, "
        f"boxes={box_count}, empty={empty_labels}, "
        f"invalid_geometry={invalid_geometry}"
    )

report["status"] = "PASS" if not report["errors"] else "FAIL"

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print("\nAUDIT STATUS:", report["status"])
print("Total images:", report["total_images"])
print("Total label files:", report["total_label_files"])
print("Total boxes:", report["total_boxes"])
print("Errors:", len(report["errors"]))
print("Warnings:", len(report["warnings"]))
print("Report:", REPORT)

if report["errors"]:
    for error in report["errors"][:30]:
        print("ERROR:", error)
