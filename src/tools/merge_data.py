import os
import json
import random

prefix = "../../data/football/"
file_annot_train = prefix + "annotations/instances_train_football_coco.json"
file_annot_val = prefix + "annotations/instances_val_football_coco.json"
images_train = prefix + "train/"
image_names_train = [f.strip(".jpg") for f in os.listdir(images_train)]
images_val = prefix + "val/"

with open(file_annot_train, "r") as fr:
    train_annot = json.load(fr)
with open(file_annot_val, "r") as fr:
    val_annot = json.load(fr)

new_images = prefix + "new_images/"
with open(prefix + "new_annotations.json", "r") as fr:
    new_annotations = json.load(fr)

uid = len(image_names_train)
category_map = {"person": 1, "ball": 2}
for i, image in enumerate(new_annotations):
    image_annot = {"file_name": image["image_id"] + ".jpg", "id": image["image_id"]}
    annotations = []
    for obj in image["objects"]:
        annotation = {
            "bbox": obj["bbox"],
            "category_id": category_map[obj["label"]],
            "image_id": image["image_id"],
            "id": uid
        }
        annotations.append(annotation)
        uid += 1
    if i % 10:
        train_annot["annotations"].extend(annotations)
        train_annot["images"].append(image_annot)
        os.rename(new_images + image["image_id"] + ".jpg", "train/" + image["image_id"] + ".jpg")
    else:
        val_annot["annotations"].extend(annotations)
        val_annot["images"].append(image_annot)
        os.rename(new_images + image["image_id"] + ".jpg", "val/" + image["image_id"] + ".jpg")

with open(file_annot_train, "w+") as fw:
    json.dump(train_annot, fw, indent=2)
with open(file_annot_val, "w+") as fw:
    json.dump(val_annot, fw, indent=2)

print("train annot:", len(train_annot["images"]))
print("valid annot:", len(val_annot["images"]))
print("train images:", len(os.listdir("train/")))
print("valid images:", len(os.listdir("val/")))
