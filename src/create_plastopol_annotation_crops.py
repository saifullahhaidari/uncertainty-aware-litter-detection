import csv
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("data/raw/plastopol")
IMAGE_DIR = ROOT / "images"
ANNOTATION_FILE = ROOT / "annotations" / "full_plastopol.json"

LEDGER = Path("docs/plastopol_annotation_review_ledger.csv")

OUTPUT = Path(
    "docs/plastopol_targeted_geometry_review/batch_01/annotation_crops"
)
OUTPUT.mkdir(parents=True, exist_ok=True)

dataset = json.loads(ANNOTATION_FILE.read_text(encoding="utf-8"))
images = {x["id"]: x for x in dataset["images"]}

annotations_by_image = {}
for ann in dataset["annotations"]:
    annotations_by_image.setdefault(ann["image_id"], []).append(ann)

with LEDGER.open("r", encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

font = ImageFont.load_default()
manifest = []

for row in rows:
    image_id = int(row["image_id"])
    ann_id = int(row["annotation_id"])

    info = images[image_id]
    image_path = IMAGE_DIR / info["file_name"]

    image = Image.open(image_path).convert("RGB")
    W, H = image.size

    target = next(
        a for a in annotations_by_image[image_id]
        if a["id"] == ann_id
    )

    x, y, w, h = target["bbox"]

    # Crop around the target box, retaining surrounding context.
    pad = max(100, int(max(w, h) * 0.30))

    left = max(0, int(x - pad))
    top = max(0, int(y - pad))
    right = min(W, int(x + w + pad))
    bottom = min(H, int(y + h + pad))

    crop = image.crop((left, top, right, bottom))
    draw = ImageDraw.Draw(crop)

    # Draw all annotations visible in this crop.
    for ann in annotations_by_image[image_id]:
        ax, ay, aw, ah = ann["bbox"]

        bx1 = max(0, ax - left)
        by1 = max(0, ay - top)
        bx2 = min(right - left, ax + aw - left)
        by2 = min(bottom - top, ay + ah - top)

        if bx2 <= bx1 or by2 <= by1:
            continue

        is_target = ann["id"] == ann_id
        color = "red" if is_target else "lime"

        draw.rectangle(
            (bx1, by1, bx2, by2),
            outline=color,
            width=4 if is_target else 2
        )

        if is_target:
            draw.text(
                (bx1, max(0, by1 - 16)),
                f"TARGET ID {ann_id}",
                fill="red",
                font=font,
                stroke_width=2,
                stroke_fill="white"
            )

    output_file = OUTPUT / f"image_{image_id}_ann_{ann_id}.jpg"
    crop.save(output_file, quality=95)

    manifest.append({
        "image_id": image_id,
        "annotation_id": ann_id,
        "file_name": info["file_name"],
        "flag_types": row["flag_types"],
        "crop_size": list(crop.size),
        "crop_file": str(output_file)
    })

    print(
        f"CREATED: {output_file.name} | "
        f"crop={crop.size} | flags={row['flag_types']}"
    )

# Save crop manifest.
manifest_path = OUTPUT / "manifest.json"
manifest_path.write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

# Create a contact sheet of all annotation crops.
columns = 4
tile_w = 450
tile_h = 390
header_h = 35
rows_count = math.ceil(len(manifest) / columns)

sheet = Image.new(
    "RGB",
    (columns * tile_w, rows_count * (tile_h + header_h)),
    "white"
)
sheet_draw = ImageDraw.Draw(sheet)

for i, item in enumerate(manifest):
    crop = Image.open(item["crop_file"]).convert("RGB")
    crop.thumbnail((tile_w - 20, tile_h - 20))

    col = i % columns
    r = i // columns
    x0 = col * tile_w
    y0 = r * (tile_h + header_h)

    label = (
        f"Image {item['image_id']} | "
        f"Annotation {item['annotation_id']} | "
        f"{item['flag_types']}"
    )

    sheet_draw.text(
        (x0 + 8, y0 + 8),
        label,
        fill="black",
        font=font
    )

    px = x0 + (tile_w - crop.width) // 2
    py = y0 + header_h + (tile_h - crop.height) // 2
    sheet.paste(crop, (px, py))

contact_path = OUTPUT / "annotation_crops_contact_sheet.jpg"
sheet.save(contact_path, quality=93)

print("\n" + "=" * 60)
print("ANNOTATION CROPS COMPLETE")
print("=" * 60)
print("Unique annotations:", len(manifest))
print("Individual crops:", OUTPUT)
print("Manifest:", manifest_path)
print("Contact sheet:", contact_path)
print("Contact sheet dimensions:", sheet.size)
