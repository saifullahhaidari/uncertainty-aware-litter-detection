
import json
import os
import sys
import time
from pathlib import Path

import requests

ANNOTATIONS_PATH = Path("data/annotations.json")
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3

def main():
    if not ANNOTATIONS_PATH.is_file():
        sys.exit(f"Annotations file not found: {ANNOTATIONS_PATH}")

    with ANNOTATIONS_PATH.open("r", encoding="utf-8") as f:
        dataset = json.load(f)

    images = dataset["images"]
    total = len(images)
    downloaded = 0
    skipped = 0
    failed = []

    with requests.Session() as session:
        for index, image in enumerate(images, start=1):
            file_path = ANNOTATIONS_PATH.parent / image["file_name"]
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Existing non-empty files are skipped.
            if file_path.is_file() and file_path.stat().st_size > 0:
                skipped += 1
                status = "existing"
            else:
                url = image.get("flickr_url")
                if not url:
                    failed.append((image["file_name"], "No image URL"))
                    status = "failed"
                else:
                    temp_path = Path(str(file_path) + ".part")
                    status = "failed"

                    for attempt in range(1, MAX_RETRIES + 1):
                        try:
                            with session.get(
                                url, timeout=TIMEOUT_SECONDS
                            ) as response:
                                response.raise_for_status()
                                content = response.content

                            if not content:
                                raise ValueError("Empty response")

                            temp_path.write_bytes(content)
                            os.replace(temp_path, file_path)
                            downloaded += 1
                            status = "downloaded"
                            break

                        except (requests.RequestException, OSError, ValueError) as exc:
                            try:
                                temp_path.unlink(missing_ok=True)
                            except OSError:
                                pass

                            if attempt < MAX_RETRIES:
                                time.sleep(attempt * 2)
                            else:
                                failed.append(
                                    (image["file_name"], str(exc))
                                )

            print(
                f"[{index}/{total}] {status}: {image['file_name']}",
                flush=True,
            )

    print("\nDownload summary")
    print(f"Images listed: {total}")
    print(f"Downloaded this run: {downloaded}")
    print(f"Skipped existing files: {skipped}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed images:")
        for filename, reason in failed:
            print(f"- {filename}: {reason}")
        print("\nRun the script again later to retry missing images.")

if __name__ == "__main__":
    main()
