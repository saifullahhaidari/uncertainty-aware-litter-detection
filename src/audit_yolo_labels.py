import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABEL_DIR = ROOT / "data" / "processed" / "taco" / "yolo" / "labels"
REPORT_FILE = ROOT / "docs" / "taco_yolo_quality_audit.json"

# جعبه‌های کوچک‌تر از این آستانه فقط مشکوک علامت می‌خورند.
MIN_BOX_AREA_RATIO = 1e-6


def main():
    if not LABEL_DIR.is_dir():
        raise FileNotFoundError(f"Label directory not found: {LABEL_DIR}")

    label_files = sorted(LABEL_DIR.rglob("*.txt"))

    total_boxes = 0
    errors = []
    warnings = []
    empty_files = 0

    for label_file in label_files:
        relative_path = label_file.relative_to(LABEL_DIR)
        lines = label_file.read_text(encoding="utf-8").splitlines()

        if not any(line.strip() for line in lines):
            empty_files += 1
            continue

        for line_number, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            total_boxes += 1
            parts = line.split()

            if len(parts) != 5:
                errors.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "problem": "Expected 5 values",
                })
                continue

            try:
                class_id = int(parts[0])
                x_center, y_center, width, height = map(float, parts[1:])
            except ValueError:
                errors.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "problem": "Non-numeric or invalid values",
                })
                continue

            values = [x_center, y_center, width, height]

            if class_id != 0:
                errors.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "problem": f"Unexpected class ID: {class_id}",
                })

            if not all(math.isfinite(value) for value in values):
                errors.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "problem": "NaN or infinite coordinate",
                })
                continue

            if width <= 0 or height <= 0:
                errors.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "problem": "Zero or negative width/height",
                })
                continue

            x1 = x_center - width / 2
            y1 = y_center - height / 2
            x2 = x_center + width / 2
            y2 = y_center + height / 2

            if (
                x1 < -1e-6 or y1 < -1e-6
                or x2 > 1 + 1e-6 or y2 > 1 + 1e-6
            ):
                errors.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "problem": "Bounding box extends outside image",
                    "coordinates": values,
                })

            if width * height < MIN_BOX_AREA_RATIO:
                warnings.append({
                    "file": str(relative_path),
                    "line": line_number,
                    "problem": "Extremely small normalized box area",
                    "area_ratio": width * height,
                })

    report = {
        "dataset": "TACO",
        "label_files_checked": len(label_files),
        "empty_label_files": empty_files,
        "bounding_boxes_checked": total_boxes,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
        "small_box_area_threshold": MIN_BOX_AREA_RATIO,
        "note": (
            "Small boxes are warnings for review, not automatic proof "
            "of incorrect annotations. This audit checks label geometry, "
            "not visual correctness."
        ),
    }

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Label files checked: {len(label_files)}")
    print(f"Bounding boxes checked: {total_boxes}")
    print(f"Empty label files: {empty_files}")
    print(f"Errors found: {len(errors)}")
    print(f"Warnings found: {len(warnings)}")
    print(f"Report saved to: {REPORT_FILE}")

    if errors:
        print("\nFirst 10 errors:")
        for error in errors[:10]:
            print(error)

    if warnings:
        print("\nFirst 10 warnings:")
        for warning in warnings[:10]:
            print(warning)


if __name__ == "__main__":
    main()