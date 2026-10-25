from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DIRS = [
    "src",
    "data",
    "docs",
]

print("Project structure check")
print("-" * 30)

for folder in REQUIRED_DIRS:
    folder_path = PROJECT_ROOT / folder

    if folder_path.exists():
        print(f"{folder}: OK")
    else:
        print(f"{folder}: MISSING")