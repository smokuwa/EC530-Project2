# user input allowing for uploading of files, as well as input natural language to retrieve images
# subscribes to vector index (or query service?) to search for info

# PUB --> image submitted
# SUB --> vector index service (for getting info)

# figure out how to MAKE RELATIVE PATH
import json
from services.upload_service import handle_upload
from systems.broker_and_topics import get_redis, TOPICS
from systems.database import get_annotation_by_image, get_image, get_vector, list_images
from shared.events import annotation_corrected

def handle_image():
    image_path = input("Enter image path: ").strip()
    try:
        event = handle_upload(image_path)
        image_id = event["payload"]["image_id"]
        print(f"Upload accepted. Image ID: {image_id}")
        return event
    except FileNotFoundError:
        print("Upload failed: I could not find that file.")
    except ValueError:
        print("Upload failed: please enter a valid image file path.")
    
# logic for when user enters annotation
def handle_correction():
    image_id = input("Enter image ID to correct: ").strip()
    annotation_id = f"ann_{image_id}"
    label = input("Enter corrected object label: ").strip()
    r = get_redis()

    if not image_id or not label:
        print("Annotation failed: please enter an image ID and label.")
        return None

    if get_image(image_id) is None:
        print("Annotation failed: that image does not exist yet.")
        return None

    corrected_object = {
        "label": label,
        "bbox": [0, 0, 100, 100],
        "conf": 1.0,
        "source": "manual_correction"
    }
    event = annotation_corrected(
        image_id=image_id,
        annotation_id=annotation_id,
        objects=[corrected_object]
    )
    r.publish(TOPICS["ANNOTATION_CORRECTED"], json.dumps(event))
    print(f"Published annotation.corrected for {image_id}")
    return event


def handle_query():
    # fix so it can look at existing data
    image_id = input("Enter image ID to query: ").strip()
    if not image_id:
        print("Query failed: please enter an image ID.")
        return None

    image = get_image(image_id)
    annotation = get_annotation_by_image(image_id)
    vector = get_vector(image_id)

    if image is None and annotation is None and vector is None:
        print(f"No results found for {image_id}.")
        return None

    print(f"Results for {image_id}:")
    if image:
        print(f"Image path: {image['path']}")

    if annotation:
        objects = annotation.get("objects", [])
        if objects:
            labels = [obj.get("label", "unknown") for obj in objects]
            print("Labels: " + ", ".join(labels))
        print(f"Annotation status: {annotation['status']}")

    if vector:
        embedding = vector.get("embedding", [])
        print(f"Embedding: {embedding}")

    return {
        "annotation": annotation,
        "vector": vector,
    }


def handle_list():
    images = list_images()

    if not images:
        print("No uploaded images found.")
        return []

    print("Stored images:")
    results = []
    for image in images:
        image_id = image["image_id"]
        path = image["path"]
        has_annotation = bool(image["has_annotation"])
        has_vector = bool(image["has_vector"])
        annotation = get_annotation_by_image(image_id)
        vector = get_vector(image_id)
        payload = {
            "image_id": image_id,
            "path": path,
            "annotation": annotation,
            "vector": vector,
        }

        annotation_status = "annotation: yes" if has_annotation else "annotation: no"
        vector_status = "vector: yes" if has_vector else "vector: no"
        print(f"- {image_id} | {path} | {annotation_status} | {vector_status}")
        print(json.dumps(payload, indent=2))

        results.append(
            {
                "image_id": image_id,
                "path": path,
                "has_annotation": has_annotation,
                "has_vector": has_vector,
                "payload": payload,
            }
        )

    return results


main_prompt = """COMMANDS: 
                upload --> use to upload an image
                annotate --> use to annotate uploaded image
                list --> allows you to see stored images
                query --> use to look up an uploaded image
                help --> use to view this prompt once more
                exit --> use to exit program
              """

def main():
    # start of connecting the CLI 
    print("\nWELCOME TO OUR PROGRAM!\n")
    print(main_prompt)
    while True:
        user_input = input("Please enter a command: ").strip().lower()
        if user_input == "upload":
            handle_image()
        elif user_input == "annotate":
            handle_correction()
        elif user_input == "list":
            handle_list()
        elif user_input == "query":
            handle_query()
        elif user_input == "help":
            print(main_prompt)
        elif user_input == "exit":
            print("GOODBYE")
            break
        else:
            print("Invalid entry, please enter a valid command")

if __name__ == "__main__":
    main()
