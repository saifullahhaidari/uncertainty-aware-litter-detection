import json
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

ROOT = Path("data/processed/plastopol/yolo")
OUTPUT = Path("docs/plastopol_yolo_visual_audit")

SEED = 42
SAMPLES_PER_SPLIT = 4
COLUMNS = 3
CARD_W = 640
CARD_H = 500

random.seed(SEED)

OUTPUT.mkdir(parents=True, exist_ok=True)

manifest = {
    "dataset": "PlastOPol",
    "seed": SEED,
    "samples_per_split": SAMPLES_PER_SPLIT,
    "samples": [],
}

cards = []

for split in ("train", "val", "test"):
    image_dir = ROOT / "images" / split
    label_dir = ROOT / "labels" / split

    images = sorted(image_dir.glob("*"))

    if len(images) < SAMPLES_PER_SPLIT:
        raise ValueError(f"Not enough images in {split}")

    selected = random.sample(images, SAMPLES_PER_SPLIT)

    for image_path in selected:
        label_path = label_dir / f"{image_path.stem}.txt"

        if not label_path.is_file():
            raise FileNotFoundError(label_path)

        with Image.open(image_path) as source:
            image = source.convert("RGB")

        width, height = image.size
        draw = ImageDraw.Draw(image)

        lines = label_path.read_text(
            encoding="utf-8"
        ).strip().splitlines()

        box_count = 0

        for line in lines:
            if not line.strip():
                continue

            parts = line.split()

            if len(parts) != 5:
                raise ValueError(
                    f"Invalid label line: {label_path}"
                )

            class_id = int(parts[0])
            xc, yc, bw, bh = map(float, parts[1:])

            x1 = (xc - bw / 2) * width
            y1 = (yc - bh / 2) * height
            x2 = (xc + bw / 2) * width
            y2 = (yc + bh / 2) * height

            draw.rectangle(
                (x1, y1, x2, y2),
                outline="red",
                width=max(3, round(width / 1000))
            )

            draw.text(
                (x1, max(0, y1 - 20)),
                f"Class {class_id}",
                fill="red",
                stroke_width=1,
                stroke_fill="white"
            )

            box_count += 1

        card = Image.new("RGB", (CARD_W, CARD_H), "white")
        thumbnail = ImageOps.contain(
            image,
            (CARD_W - 20, CARD_H - 65)
        )

        card.paste(thumbnail, (
            (CARD_W - thumbnail.width) // 2,
            35 + (CARD_H - 65 - thumbnail.height) // 2
        ))

        card_draw = ImageDraw.Draw(card)
        card_draw.text(
            (10, 10),
            f"{split.upper()} | {image_path.name} | Boxes: {box_count}",
            fill="black"
        )

        cards.append(card)

        manifest["samples"].append({
            "split": split,
            "image": image_path.name,
            "boxes": box_count,
            "label_file": str(label_path),
        })

rows = (len(cards) + COLUMNS - 1) // COLUMNS

sheet = Image.new(
    "RGB",
    (COLUMNS * CARD_W, rows * CARD_H),
    "white"
)

for index, card in enumerate(cards):
    x = (index % COLUMNS) * CARD_W
    y = (index // COLUMNS) * CARD_H
    sheet.paste(card, (x, y))

sheet_path = OUTPUT / "plastopol_yolo_visual_audit.png"
sheet.save(sheet_path)

manifest_path = OUTPUT / "manifest.json"
manifest_path.write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8"
)

print("VISUAL AUDIT SAMPLE CREATED")
print("Samples:", len(cards))
print("Train:", SAMPLES_PER_SPLIT)
print("Validation:", SAMPLES_PER_SPLIT)
print("Test:", SAMPLES_PER_SPLIT)
print("Image:", sheet_path)
print("Manifest:", manifest_path)
