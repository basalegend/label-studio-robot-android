import json
import cv2
from pathlib import Path

def process_label_studio_export(label_studio_export_json, cropped_root):
    """
    Process Label Studio export and crop faces from images.
    
    Args:
        label_studio_export_json (str): Path to Label Studio JSON export
        cropped_root (Path): Where to save cropped faces
    """
    cropped_root = Path(cropped_root)
    cropped_root.mkdir(exist_ok=True)

    with open(label_studio_export_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    face_counter = {}

    for item in data:
        # Get image path
        image_path = Path(item['data']['image'].split("=")[-1])

        # Parse folder name (person name)
        person_name = item['data']['folder']
        person_dir = cropped_root / person_name
        person_dir.mkdir(exist_ok=True)

        # Read image
        img = cv2.imread(str(image_path))
        height, width = img.shape[:2]

        for annotation in item.get("annotations", []):
            for result in annotation.get("result", []):
                value = result.get("value", {})
                x = int(value["x"] / 100 * width)
                y = int(value["y"] / 100 * height)
                w = int(value["width"] / 100 * width)
                h = int(value["height"] / 100 * height)

                # Crop face
                face = img[y:y + h, x:x + w]

                # Count for unique name
                count = face_counter.get(person_name, 0) + 1
                face_counter[person_name] = count

                # Save
                output_path = person_dir / f"{person_name}_{count:02d}.jpg"
                cv2.imwrite(str(output_path), face)

if __name__ == "__main__":
    LABEL_STUDIO_EXPORT_JSON = 'project-2-at-2025-05-07-08-11-5f9a9f5b.json'
    CROPPED_ROOT = Path('../label-studio-files/cropped_dataset')
    process_label_studio_export(LABEL_STUDIO_EXPORT_JSON, CROPPED_ROOT)
