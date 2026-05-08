import json
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "data" / "local_db.json"


def empty_database():
    return {
        "images": {},
        "annotations": {},
        "vectors": {},
    }


def load_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists():
        return empty_database()

    with DB_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_database(database):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with DB_PATH.open("w", encoding="utf-8") as file:
        json.dump(database, file, indent=2)


def save_image(image_id, path):
    database = load_database()
    database["images"][image_id] = {
        "image_id": image_id,
        "path": path,
    }
    save_database(database)


def get_image(image_id):
    database = load_database()
    return database["images"].get(image_id)


def list_images():
    database = load_database()
    results = []

    for image_id in sorted(database["images"]):
        image = database["images"][image_id]
        results.append(
            {
                "image_id": image_id,
                "path": image["path"],
            }
        )

    return results


def save_annotation(annotation_id, image_id, objects, status="stored"):
    database = load_database()
    database["annotations"][image_id] = {
        "annotation_id": annotation_id,
        "image_id": image_id,
        "objects": objects,
        "status": status,
    }
    save_database(database)


def get_annotation_by_image(image_id):
    database = load_database()
    return database["annotations"].get(image_id)


def save_vector(image_id, path, embedding):
    database = load_database()
    database["vectors"][image_id] = {
        "image_id": image_id,
        "path": path,
        "embedding": embedding,
    }
    save_database(database)


def get_vector(image_id):
    database = load_database()
    return database["vectors"].get(image_id)
