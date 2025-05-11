import os
import json
from glob import glob
from pathlib import Path


def generate_label_studio_import(dataset_path: str, output_file: str = "data/label_studio_import.json") -> None:
    """
    Generate Label Studio import file from dataset directory.
    
    Args:
        dataset_path: Path to the dataset directory
        output_file: Path where to save the import file
    """
    tasks = []
    dataset_path = Path(dataset_path)

    for person_folder in dataset_path.iterdir():

        image_files = sorted(
            glob(os.path.join(str(person_folder), "*.jpg")) +
            glob(os.path.join(str(person_folder), "*.png"))
        )

        for img_path in image_files:
            task = {
                "data": {
                    "image": f"/data/local-files/?d={img_path}",
                    "folder": person_folder.name
                }
            }
            tasks.append(task)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    DATASET_PATH = "../label-studio-files/dataset/"
    OUTPUT_FILE = "data/label_studio_import.json"
    generate_label_studio_import(DATASET_PATH, OUTPUT_FILE)
