import os
import cv2
import xml.etree.ElementTree as ET

import os
import cv2
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Charger .env
load_dotenv()

# Lire variablesimport os
import cv2
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# Charger .env
load_dotenv()

# Base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lire variables depuis .env
IMAGE_DIR = os.path.join(BASE_DIR, os.getenv("IMAGE_DIR", ""))
ANNOTATION_DIR = os.path.join(BASE_DIR, os.getenv("ANNOTATION_DIR", ""))
OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv("OUTPUT_DIR", ""))
PADDING = int(os.getenv("PADDING", 0))

# Vérification
if not IMAGE_DIR or not ANNOTATION_DIR or not OUTPUT_DIR:
    raise ValueError("Vérifie ton fichier .env : variables manquantes")

# Extensions d'images acceptées
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def parse_bounding_boxes(xml_path: str):
    boxes = []

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for obj in root.findall("object"):
        bbox = obj.find("bndbox")
        if bbox is None:
            continue

        xmin = int(float(bbox.find("xmin").text))
        ymin = int(float(bbox.find("ymin").text))
        xmax = int(float(bbox.find("xmax").text))
        ymax = int(float(bbox.find("ymax").text))

        boxes.append((xmin, ymin, xmax, ymax))

    return boxes


def crop_and_save(image_path: str, xml_path: str, output_dir: str, padding: int = 0):
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Impossible de lire l'image: {image_path}")
        return 0

    h, w = image.shape[:2]
    boxes = parse_bounding_boxes(xml_path)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    saved_count = 0

    for i, (xmin, ymin, xmax, ymax) in enumerate(boxes):
        xmin_p = max(0, xmin - padding)
        ymin_p = max(0, ymin - padding)
        xmax_p = min(w, xmax + padding)
        ymax_p = min(h, ymax + padding)

        if xmin_p >= xmax_p or ymin_p >= ymax_p:
            print(f"[WARNING] Boîte invalide ignorée dans {xml_path}: {(xmin, ymin, xmax, ymax)}")
            continue

        crop = image[ymin_p:ymax_p, xmin_p:xmax_p]

        if crop.size == 0:
            print(f"[WARNING] Crop vide ignoré: {image_path} box {(xmin, ymin, xmax, ymax)}")
            continue

        output_filename = f"{base_name}_{i:02d}.jpg"
        output_path = os.path.join(output_dir, output_filename)

        cv2.imwrite(output_path, crop)
        saved_count += 1

    return saved_count


def main():
    ensure_dir(OUTPUT_DIR)

    print("IMAGE_DIR      =", IMAGE_DIR)
    print("ANNOTATION_DIR =", ANNOTATION_DIR)
    print("OUTPUT_DIR     =", OUTPUT_DIR)
    print("PADDING        =", PADDING)

    total_images = 0
    total_crops = 0
    missing_xml = []

    for filename in os.listdir(IMAGE_DIR):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue

        image_path = os.path.join(IMAGE_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        xml_filename = base_name + ".xml"
        xml_path = os.path.join(ANNOTATION_DIR, xml_filename)

        if not os.path.exists(xml_path):
            missing_xml.append(filename)
            print(f"[WARNING] Annotation manquante pour {filename}")
            continue

        total_images += 1
        count = crop_and_save(
            image_path=image_path,
            xml_path=xml_path,
            output_dir=OUTPUT_DIR,
            padding=PADDING
        )

        total_crops += count
        print(f"[OK] {filename} -> {count} chromosomes extraits")

    print("\n===== TERMINÉ =====")
    print(f"Images traitées : {total_images}")
    print(f"Chromosomes extraits : {total_crops}")

    if missing_xml:
        print(f"Images sans annotation : {len(missing_xml)}")
        for name in missing_xml[:10]:
            print(" -", name)
        if len(missing_xml) > 10:
            print(" ...")


if __name__ == "__main__":
    main()
IMAGE_DIR = os.getenv("IMAGE_DIR")
ANNOTATION_DIR = os.getenv("ANNOTATION_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
PADDING = int(os.getenv("PADDING", 0))

# Vérification
if not IMAGE_DIR or not ANNOTATION_DIR or not OUTPUT_DIR:
    raise ValueError("Vérifie ton fichier .env (variables manquantes)")

os.makedirs(OUTPUT_DIR, exist_ok=True)
# Ajouter une petite marge autour du crop
PADDING = 5

# Extensions d'images acceptées
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def parse_bounding_boxes(xml_path: str):
    """
    Lit un fichier XML Pascal VOC et retourne une liste de bounding boxes.
    Chaque boîte est un tuple: (xmin, ymin, xmax, ymax)
    """
    boxes = []

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for obj in root.findall("object"):
        bbox = obj.find("bndbox")
        if bbox is None:
            continue

        xmin = int(float(bbox.find("xmin").text))
        ymin = int(float(bbox.find("ymin").text))
        xmax = int(float(bbox.find("xmax").text))
        ymax = int(float(bbox.find("ymax").text))

        boxes.append((xmin, ymin, xmax, ymax))

    return boxes


def crop_and_save(image_path: str, xml_path: str, output_dir: str, padding: int = 0):
    """
    Coupe tous les objets annotés dans une image et les sauvegarde.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"[ERROR] Impossible de lire l'image: {image_path}")
        return 0

    h, w = image.shape[:2]
    boxes = parse_bounding_boxes(xml_path)

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    saved_count = 0

    for i, (xmin, ymin, xmax, ymax) in enumerate(boxes):
        # Ajouter marge/padding
        xmin_p = max(0, xmin - padding)
        ymin_p = max(0, ymin - padding)
        xmax_p = min(w, xmax + padding)
        ymax_p = min(h, ymax + padding)

        # Vérification
        if xmin_p >= xmax_p or ymin_p >= ymax_p:
            print(f"[WARNING] Boîte invalide ignorée dans {xml_path}: {(xmin, ymin, xmax, ymax)}")
            continue

        crop = image[ymin_p:ymax_p, xmin_p:xmax_p]

        if crop.size == 0:
            print(f"[WARNING] Crop vide ignoré: {image_path} box {(xmin, ymin, xmax, ymax)}")
            continue

        output_filename = f"{base_name}_{i:02d}.jpg"
        output_path = os.path.join(output_dir, output_filename)

        cv2.imwrite(output_path, crop)
        saved_count += 1

    return saved_count


def main():
    ensure_dir(OUTPUT_DIR)

    total_images = 0
    total_crops = 0
    missing_xml = []

    for filename in os.listdir(IMAGE_DIR):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue

        image_path = os.path.join(IMAGE_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        xml_filename = base_name + ".xml"
        xml_path = os.path.join(ANNOTATION_DIR, xml_filename)

        if not os.path.exists(xml_path):
            missing_xml.append(filename)
            print(f"[WARNING] Annotation manquante pour {filename}")
            continue

        total_images += 1
        count = crop_and_save(
            image_path=image_path,
            xml_path=xml_path,
            output_dir=OUTPUT_DIR,
            padding=PADDING
        )

        total_crops += count
        print(f"[OK] {filename} -> {count} chromosomes extraits")

    print("\n===== TERMINÉ =====")
    print(f"Images traitées : {total_images}")
    print(f"Chromosomes extraits : {total_crops}")

    if missing_xml:
        print(f"Images sans annotation : {len(missing_xml)}")
        for name in missing_xml[:10]:
            print(" -", name)
        if len(missing_xml) > 10:
            print(" ...")


if __name__ == "__main__":
    main()