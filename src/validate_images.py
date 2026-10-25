
import json
from pathlib import Path
from datetime import datetime
from PIL import Image

PROJECT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT / "data"
ANNOTATIONS_FILE = DATA_DIR / "annotations.json"
REPORT_DIR = PROJECT / "docs"

def main():
    print("Starting TACO image validation...")

    with ANNOTATIONS_FILE.open("r", encoding="utf-8") as f:
        annotations = json.load(f)

    images = annotations["images"]
    valid = []
    missing = []
    invalid = []

    for i, item in enumerate(images, start=1):
        path = DATA_DIR / item["file_name"]

        if not path.is_file():
            missing.append(item["file_name"])
        else:
            try:
                with Image.open(path) as img:
                    img.verify()
                valid.append(item["file_name"])
            except Exception as exc:
                invalid.append({
                    "file": item["file_name"],
                    "error": str(exc)
                })

        if i % 100 == 0 or i == len(images):
            print(f"Checked {i}/{len(images)}")

    report = {
        "checked_at": datetime.now().astimezone().isoformat(),
        "images_listed": len(images),
        "valid_images": len(valid),
        "missing_images": len(missing),
        "invalid_images": len(invalid),
        "missing_files": missing,
        "invalid_files": invalid
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "taco_image_validation.json"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n--- Validation Summary ---")
    print(f"Images listed: {len(images)}")
    print(f"Valid images: {len(valid)}")
    print(f"Missing images: {len(missing)}")
    print(f"Invalid images: {len(invalid)}")
    print(f"Report saved: {report_path}")

if __name__ == "__main__":
    main()
