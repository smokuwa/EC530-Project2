# user input allowing for uploading of files, as well as input natural language to retrieve images
# subscribes to vector index (or query service?) to search for info

# PUB --> image submitted
# SUB --> vector index service (for getting info)

# figure out how to MAKE RELATIVE PATH
import json
from services.upload_service import handle_upload
from systems.broker_and_topics import get_redis, TOPICS
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
    r = get_redis()
    r.publish(TOPICS["ANNOTATION_CORRECTED"], json.dumps(event))
    print(f"Published annotation.corrected for {image_id}")
    return event

main_prompt = """COMMANDS: 
                upload --> use to upload an image
                annotate --> use to annotate uploaded image
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
        elif user_input == "help":
            print(main_prompt)
        elif user_input == "exit":
            print("GOODBYE")
            break
        else:
            print("Invalid entry, please enter a valid command")

if __name__ == "__main__":
    main()
