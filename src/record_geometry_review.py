import csv
from pathlib import Path

path = Path("docs/plastopol_bbox_review_ledger.csv")

decisions = {
    "1": "valid",
    "2": "incorrect_bbox",
    "3": "uncertain",
    "4": "needs_semantic_review",
}

print("DECISION OPTIONS")
for key, value in decisions.items():
    print(f"{key}. {value}")

print("\nEnter image IDs and review decisions.")
print("Press Enter on an empty image ID to finish.")

with path.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

by_id = {row["image_id"]: row for row in rows}
updates = []

while True:
    image_id = input("\nImage ID: ").strip()

    if not image_id:
        break

    if image_id not in by_id:
        print("ERROR: Image ID not found.")
        continue

    row = by_id[image_id]

    print("Image:", row["file_name"])
    print("Flags:", row["flag_types"])

    choice = input("Decision (1-4): ").strip()

    if choice not in decisions:
        print("Invalid choice.")
        continue

    notes = input("Review notes: ").strip()

    updates.append({
        "image_id": image_id,
        "decision": decisions[choice],
        "notes": notes,
    })

if updates:
    for item in updates:
        row = by_id[item["image_id"]]
        row["review_status"] = "completed"
        row["reviewer_decision"] = item["decision"]
        row["review_notes"] = item["notes"]

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

print("\nREVIEW LEDGER UPDATED")
print("Updated records:", len(updates))
print("File:", path)
