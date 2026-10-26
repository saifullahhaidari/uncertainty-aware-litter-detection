
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

with (DATA / "annotations.json").open("r", encoding="utf-8") as f:
    data = json.load(f)

target_ids = {371, 387, 707, 859, 1621, 1777, 2186}
images = {img["id"]: img for img in data["images"]}

for ann in data["annotations"]:
    if ann["id"] not in target_ids:
        continue

    info = images[ann["image_id"]]
    path = DATA / info["file_name"]

    with Image.open(path) as img:
        orientation = img.getexif().get(274, 1)

        print("-" * 45)
        print("Annotation ID:", ann["id"])
        print("Image:", info["file_name"])
        print("Metadata size:", info["width"], "x", info["height"])
        print("Raw image size:", img.width, "x", img.height)
        print("EXIF orientation:", orientation)

print("-" * 45)
print("Original annotations were not modified.")
