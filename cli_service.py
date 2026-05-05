# user input allowing for uploading of files, as well as input natural language to retrieve images
# subscribes to vector index (or query service?) to search for info

# PUB --> image submitted
# SUB --> vector index service (for getting info)

# figure out how to MAKE RELATIVE PATH
from services.upload_service import handle_upload

def handle_image(event):
    image_path = input("Enter image path: ").strip()
    try:
        event = handle_upload(image_path)
        image_id = event["payload"]["image_id"]
        print("Upload accepted. Image ID: " + image_id)
    except FileNotFoundError:
        print("File not Found")
    except ValueError:
        print("Invalid upload")
    

def handle_correction(event):
    # add logic for when user enters annotation 
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
        user_input = input("Please enter a command: ")
        if user_input == "upload":
            handle_image(user_input)
        elif user_input == "annotate":
            handle_correction(user_input)
        elif user_input == "help":
            print(main_prompt)
        elif user_input == "exit":
            print("GOODBYE")
            break
        else:
            print("Invalid entry, please enter a valid command")

if __name__ == "__main__":
    main()
