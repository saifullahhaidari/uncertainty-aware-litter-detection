
import json
import math
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ANNOTATIONS_FILE = PROJECT_ROOT / "data" / "annotations.json"

with ANNOTATIONS_FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)

images = {img["id"]: img for img in data["images"]}
categories = {
    cat["id"]: cat["name"]
    for cat in data["categories"]
}

invalid_count = 0

for ann in data["annotations"]:
    bbox = ann.get("bbox")
    image = images.get(ann.get("image_id"))
    problems = []

    if not isinstance(bbox, list) or len(bbox) != 4:
        problems.append("Invalid bbox format")
    else:
        try:
            x, y, w, h = bbox
            values = [x, y, w, h]

            if not all(
                isinstance(v, (int, float))
                and not isinstance(v, bool)
                for v in values
            ):
                problems.append("Non-numeric coordinate")

            elif not all(math.isfinite(v) for v in values):
                problems.append("Non-finite coordinate")

            else:
                if w <= 0 or h <= 0:
                    problems.append("Width or height <= 0")

                if x < 0 or y < 0:
                    problems.append("Negative x or y")

                if image is not None:
                    iw = image.get("width")
                    ih = image.get("height")

                    if iw is not None and ih is not None:
                        if x + w > iw or y + h > ih:
                            problems.append("Box outside image")

        except (TypeError, ValueError, OverflowError):
            problems.append("Could not validate bbox")

    if problems:
        invalid_count += 1

        category_name = categories.get(
            ann.get("category_id"), "Unknown"
        )

        print("-" * 50)
        print("Annotation ID:", ann.get("id"))
        print("Image ID:", ann.get("image_id"))
        print(
            "Image file:",
            image.get("file_name") if image else "Missing"
        )
        print("Category:", category_name)
        print("Bounding box:", bbox)
        print("Problems:", ", ".join(problems))

print("=" * 50)
print("Total problematic annotations:", invalid_count)
