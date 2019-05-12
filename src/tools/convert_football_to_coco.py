import os
import json

images_folder = "../../data/football/images/"
folder = "../../data/football/"
annotation_file = folder + "annotations_20190515T110534.json"

with open(annotation_file, "r") as f:
    football_annotations = json.load(f)
images_available = [f.strip(".jpg") for f in os.listdir(images_folder)]

coco_annotations = {
    "categories": [
        {"id": 1, "name": "person", "supercategory": "person"},
        {"id": 2, "name": "sports ball", "supercategory": "sports"}
    ]
}
category_map = {"person": 1, "ball": 2}
images = [{"file_name": x["image_id"] + ".jpg", "id": x["image_id"]} for x in football_annotations
          if x["image_id"] in images_available]
annotations = []
uid = 0
for image in football_annotations:
    if image["image_id"] not in images_available:
        continue
    for obj in image["objects"]:
        annotation = {
            "bbox": obj["bbox"],
            "category_id": category_map[obj["label"]],
            "image_id": image["image_id"],
            "id": uid
        }
        annotations.append(annotation)
        uid += 1

coco_annotations["images"] = images
coco_annotations["annotations"] = annotations

with open(folder + "annotations_video10_6.json", "w") as f:
    json.dump(coco_annotations, f, indent=2)
print(f"Saved annotations for {len(coco_annotations['images'])} images")
