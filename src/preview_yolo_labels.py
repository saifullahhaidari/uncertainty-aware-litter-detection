
import json
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ANNOTATION_FILE = DATA_DIR / "processed" / "taco" / "annotations_bbox_corrected.json"
LABEL_DIR = DATA_DIR / "processed" / "taco" / "yolo" / "labels"
OUTPUT_FILE = DATA_DIR / "processed" / "taco" / "yolo" / "visual_audit.jpg"

SAMPLE_COUNT = 12
COLUMNS = 3
CELL_WIDTH = 480
CELL_HEIGHT = 380
SEED = 42


def main():
    with ANNOTATION_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    candidates = []

    for item in data["images"]:
        relative_image = Path(item["file_name"])
        image_path = DATA_DIR / relative_image
        label_path = LABEL_DIR / relative_image.with_suffix(".txt")

        if not image_path.is_file():
            raise FileNotFoundError(f"Missing image: {image_path}")

        if not label_path.is_file():
            raise FileNotFoundError(f"Missing label: {label_path}")

        if label_path.read_text(encoding="utf-8").strip():
            candidates.append((item, image_path, label_path))

    if len(candidates) < SAMPLE_COUNT:
        raise ValueError(
            f"Only {len(candidates)} labeled images available."
        )

    rng = random.Random(SEED)
    samples = rng.sample(candidates, SAMPLE_COUNT)

    rows = (SAMPLE_COUNT + COLUMNS - 1) // COLUMNS
    sheet = Image.new(
        "RGB",
        (COLUMNS * CELL_WIDTH, rows * CELL_HEIGHT),
        "white",
    )
    draw_sheet = ImageDraw.Draw(sheet)

    for index, (item, image_path, label_path) in enumerate(samples):
        with Image.open(image_path) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")

        draw = ImageDraw.Draw(image)
        width, height = image.size

        for line in label_path.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            if len(parts) != 5:
                raise ValueError(f"Malformed label: {label_path}")

            class_id = int(parts[0])
            x_center, y_center, box_width, box_height = map(
                float, parts[1:]
            )

            x1 = (x_center - box_width / 2) * width
            y1 = (y_center - box_height / 2) * height
            x2 = (x_center + box_width / 2) * width
            y2 = (y_center + box_height / 2) * height

            draw.rectangle((x1, y1, x2, y2), outline="red", width=4)
            draw.text((x1, max(0, y1 - 18)), f"class {class_id}", fill="red")

        image.thumbnail((CELL_WIDTH - 20, CELL_HEIGHT - 45))

        column = index % COLUMNS
        row = index // COLUMNS
        x_offset = column * CELL_WIDTH
        y_offset = row * CELL_HEIGHT

        sheet.paste(image, (x_offset + 10, y_offset + 30))
        draw_sheet.text(
            (x_offset + 10, y_offset + 8),
            f"{item['file_name']}",
            fill="black",
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT_FILE, quality=92)

    print(f"Sample images checked: {SAMPLE_COUNT}")
    print(f"Preview saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
