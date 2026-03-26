import os
import shutil
from sklearn.model_selection import train_test_split

# paths
IMAGE_DIR = "data/raw/single_chromosomes_object/JPEG"
LABEL_FILE = "data/raw/train"   # your label file

OUTPUT_DIR = "data/processed"

# create folders
def create_dirs(classes):
    for split in ["train", "val", "test"]:
        for cls in classes:
            os.makedirs(os.path.join(OUTPUT_DIR, split, cls), exist_ok=True)

# read labels
def load_labels():
    data = []
    with open(LABEL_FILE, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            img, label = parts[0], parts[1]
            data.append((img, label))
    return data

# main function
def prepare():
    data = load_labels()

    # extract classes
    classes = list(set([label for _, label in data]))
    create_dirs(classes)

    # split
    train_data, temp_data = train_test_split(data, test_size=0.2, random_state=42)
    val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

    # function to copy images
    def copy_files(dataset, split):
        for img, label in dataset:
            src = os.path.join(IMAGE_DIR, img)
            dst = os.path.join(OUTPUT_DIR, split, label, img)

            if os.path.exists(src):
                shutil.copy(src, dst)

    copy_files(train_data, "train")
    copy_files(val_data, "val")
    copy_files(test_data, "test")

    print("Dataset prepared successfully!")

if __name__ == "__main__":
    prepare()