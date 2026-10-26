
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

SOURCE_FILE = DATA_DIR / "annotations.json"
CORRECTED_FILE = (
    DATA_DIR / "processed" / "taco" / "annotations_bbox_corrected.json"
)
OUTPUT_FILE = (
    DATA_DIR / "processed" / "taco" / "bbox_review_v2.png"
)

TARGET_IDS = {371, 387, 707, 859, 1621, 1777, 2186}

with SOURCE_FILE.open("r", encoding="utf-8") as f:
    original = json.load(f)

with CORRECTED_FILE.open("r", encoding="utf-8") as f:
    corrected = json.load(f)

original_images = {item["id"]: item for item in original["images"]}
original_annotations = {
    item["id"]: item
    for item in original["annotations"]
    if item["id"] in TARGET_IDS
}
corrected_annotations = {
    item["id"]: item
    for item in corrected["annotations"]
}
categories = {
    item["id"]: item["name"]
    for item in original["categories"]
}

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Six annotations are shown in the usual original/corrected comparison.
# ID 2186 receives two extra panels to compare raw and EXIF-corrected views.
fig, axes = plt.subplots(
    len(TARGET_IDS) + 1, 2, figsize=(14, 32)
)

for row, ann_id in enumerate(sorted(TARGET_IDS)):
    ann_old = original_annotations[ann_id]
    ann_new = corrected_annotations[ann_id]

    image_info = original_images[ann_old["image_id"]]
    image_path = DATA_DIR / image_info["file_name"]

    with Image.open(image_path) as source:
        raw_image = source.convert("RGB")
        display_image = ImageOps.exif_transpose(source).convert("RGB")

    category = categories.get(ann_old["category_id"], "Unknown")

    # For the six ordinary cases, keep the previous comparison.
    if ann_id != 2186:
        for col, ann, label in [
            (0, ann_old, "Original annotation"),
            (1, ann_new, "Corrected annotation"),
        ]:
            ax = axes[row, col]
            ax.imshow(display_image)

            x, y, w, h = ann["bbox"]
            rect = patches.Rectangle(
                (x, y), w, h,
                linewidth=2,
                edgecolor="red",
                facecolor="none",
            )
            ax.add_patch(rect)
            ax.set_title(f"ID {ann_id} | {label}\n{category}")
            ax.axis("off")

    else:
        # Row for ID 2186: raw and EXIF-corrected images.
        for col, image, label in [
            (0, raw_image, "Raw image (EXIF not applied)"),
            (1, display_image, "Display image (EXIF applied)"),
        ]:
            ax = axes[row, col]
            ax.imshow(image)

            x, y, w, h = ann_new["bbox"]
            rect = patches.Rectangle(
                (x, y), w, h,
                linewidth=2,
                edgecolor="red",
                facecolor="none",
            )
            ax.add_patch(rect)
            ax.set_title(
                f"ID {ann_id} | {label}\n"
                f"{category} | bbox={ann_new['bbox']}"
            )
            ax.axis("off")

        # Additional panel row: show the EXIF-corrected view again
        # with the original annotation box for direct comparison.
        extra_row = len(TARGET_IDS)
        ax = axes[extra_row, 0]
        ax.imshow(display_image)

        x, y, w, h = ann_old["bbox"]
        ax.add_patch(
            patches.Rectangle(
                (x, y), w, h,
                linewidth=2,
                edgecolor="red",
                facecolor="none",
            )
        )
        ax.set_title(
            f"ID {ann_id} | Original bbox on EXIF-corrected image"
        )
        ax.axis("off")

        # Show the segmentation polygon to compare its alignment.
        ax = axes[extra_row, 1]
        ax.imshow(display_image)

        segmentation = ann_old.get("segmentation", [])
        for polygon in segmentation:
            if len(polygon) >= 6 and len(polygon) % 2 == 0:
                points = list(zip(polygon[0::2], polygon[1::2]))
                xs = [point[0] for point in points]
                ys = [point[1] for point in points]
                ax.plot(xs + [xs[0]], ys + [ys[0]], color="yellow", linewidth=2)

        x, y, w, h = ann_old["bbox"]
        ax.add_patch(
            patches.Rectangle(
                (x, y), w, h,
                linewidth=2,
                edgecolor="red",
                facecolor="none",
            )
        )
        ax.set_title(
            f"ID {ann_id} | Segmentation (yellow) + bbox (red)"
        )
        ax.axis("off")

plt.tight_layout()
fig.savefig(OUTPUT_FILE, dpi=120)
plt.close(fig)

print("Visual review image saved to:")
print(OUTPUT_FILE)
print("IDs reviewed:", sorted(TARGET_IDS))
print("ID 2186 includes raw, EXIF-corrected, and segmentation views.")
print("This script does not modify the source annotations.")
