import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

if len(sys.argv) != 2:
    raise SystemExit(
        "Usage: python create_plastopol_geometry_review.py BATCH_NUMBER"
    )

batch_number = int(sys.argv[1])

if batch_number < 1:
    raise ValueError("Batch number must be positive.")

ROOT = Path("data/raw/plastopol")
IMAGE_DIR = ROOT / "images"
ANNOTATION_FILE = ROOT / "annotations" / "full_plastopol.json"

REVIEW_ROOT = Path("docs/plastopol_targeted_geometry_review")
BATCH_FILE = REVIEW_ROOT / f"review_batch_{batch_number:02d}.json"
OUTPUT_DIR = REVIEW_ROOT / f"batch_{batch_number:02d}"

if not BATCH_FILE.exists():
    raise FileNotFoundError(BATCH_FILE)

if OUTPUT_DIR.exists() and any(OUTPUT_DIR.iterdir()):
    raise FileExistsError(
        f"Output directory is not empty: {OUTPUT_DIR}. "
        "Refusing to overwrite existing review materials."
    )

batch = json.loads(BATCH_FILE.read_text(encoding="utf-8"))
dataset = json.loads(ANNOTATION_FILE.read_text(encoding="utf-8"))

images_by_id = {item["id"]: item for item in dataset["images"]}

annotations_by_image = {}
for ann in dataset["annotations"]:
    annotations_by_image.setdefault(ann["image_id"], []).append(ann)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

font = ImageFont.load_default()
manifest = []
contact_tiles = []

for candidate in batch["images"]:
    image_id = candidate["image_id"]

    if image_id not in images_by_id:
        raise ValueError(f"Image {image_id} missing from source JSON.")

    image_info = images_by_id[image_id]
    file_name = image_info["file_name"]

    if file_name != candidate["file_name"]:
        raise ValueError(f"Filename mismatch for image {image_id}.")

    image_path = IMAGE_DIR / file_name

    if not image_path.exists():
        raise FileNotFoundError(image_path)

    image = Image.open(image_path).convert("RGB")
    original_width, original_height = image.size

    if (original_width, original_height) != (
        image_info["width"], image_info["height"]
    ):
        raise ValueError(f"Dimension mismatch for image {image_id}.")

    draw = ImageDraw.Draw(image)

    flagged_ids = {
        flag["annotation_id"] for flag in candidate["flags"]
    }

    flags_by_annotation = {}
    for flag in candidate["flags"]:
        flags_by_annotation.setdefault(
            flag["annotation_id"], []
        ).append(flag["type"])

    annotations = annotations_by_image.get(image_id, [])
    source_ids = {ann["id"] for ann in annotations}

    if not flagged_ids.issubset(source_ids):
        raise ValueError(
            f"Flagged annotation missing in image {image_id}."
        )

    for ann in annotations:
        x, y, w, h = ann["bbox"]

        x1 = max(0, x)
        y1 = max(0, y)
        x2 = min(original_width, x + w)
        y2 = min(original_height, y + h)

        is_flagged = ann["id"] in flagged_ids
        color = "red" if is_flagged else "lime"

        draw.rectangle(
            [x1, y1, x2, y2],
            outline=color,
            width=max(3, round(min(original_width, original_height) / 700))
        )

        label = (
            f"ID {ann['id']}: "
            + ",".join(flags_by_annotation[ann["id"]])
            if is_flagged else f"ID {ann['id']}"
        )

        draw.text(
            (x1, max(0, y1 - 14)),
            label,
            fill=color,
            font=font,
            stroke_width=1,
            stroke_fill="black"
        )

    canvas = Image.new(
        "RGB", (original_width, original_height + 45), "black"
    )
    canvas.paste(image, (0, 45))

    header = (
        f"Image {image_id} | {original_width}x{original_height} | "
        f"Annotations: {len(annotations)} | "
        f"Flagged: {len(flagged_ids)}"
    )

    ImageDraw.Draw(canvas).text(
        (12, 12), header, fill="white", font=font
    )

    output_path = OUTPUT_DIR / f"{image_id}_review.jpg"
    canvas.save(output_path, quality=95)

    # Thumbnail for contact sheet.
    thumbnail = ImageOps.contain(canvas, (850, 590))
    tile = Image.new("RGB", (900, 640), "black")
    tile.paste(
        thumbnail,
        ((900 - thumbnail.width) // 2, 35)
    )
    ImageDraw.Draw(tile).text(
        (12, 10),
        f"Image {image_id} | {file_name}",
        fill="white",
        font=font
    )
    contact_tiles.append(tile)

    manifest.append({
        "image_id": image_id,
        "file_name": file_name,
        "original_width": original_width,
        "original_height": original_height,
        "annotation_count": len(annotations),
        "flagged_annotation_ids": sorted(flagged_ids),
        "flag_types": candidate["flag_counts"],
        "review_image": str(output_path)
    })

    print(
        f"CREATED: {output_path.name} | "
        f"annotations={len(annotations)} | "
        f"flagged={len(flagged_ids)}"
    )

manifest_path = OUTPUT_DIR / "manifest.json"
manifest_path.write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

columns = 2
rows = (len(contact_tiles) + columns - 1) // columns

contact_sheet = Image.new(
    "RGB", (columns * 900, rows * 640), "black"
)

for index, tile in enumerate(contact_tiles):
    x = (index % columns) * 900
    y = (index // columns) * 640
    contact_sheet.paste(tile, (x, y))

contact_path = OUTPUT_DIR / f"batch_{batch_number:02d}_contact_sheet.jpg"
contact_sheet.save(contact_path, quality=92)

print("\n" + "=" * 60)
print("GEOMETRY REVIEW IMAGES CREATED")
print("=" * 60)
print("Batch:", batch_number)
print("Images:", len(manifest))
print("Output:", OUTPUT_DIR)
print("Manifest:", manifest_path)
print("Contact sheet:", contact_path)
