# user input allowing for uploading of files, as well as input natural language to retrieve images
# subscribes to vector index (or query service?) to search for info

# PUB --> image submitted
# SUB --> vector index service (for getting info)

# figure out how to MAKE RELATIVE PATH
from systems.broker_and_topics import get_redis, TOPICS
from shared.events import image_submitted
import json

def handle_image(event):
    # add logic here
    return event

def handle_correction(event):
    # add logic for when user enters annotation 
    return event

def main():
    # r = get_redis()
    # #event = image_submitted() # will have info needed to get payload

    # # for now, fake data
    # event = {
    #         "type": "image.submitted",
    #         "payload": {
    #             "image_id": "img_1",
    #             "path": "/tmp/dog.jpg"
    #         }
    #     }

    # # publishes info to topics
    # r.publish(TOPICS["IMAGE_SUBMITTED"], json.dumps(event))
    # print(f"Published image.submitted")

    # start of connecting the CLI
    
    while True:
        user_input = input("Please enter a respective command: ")
        if user_input == "upload":
            handle_image(user_input)
        elif user_input == "correction":
            handle_correction(user_input)
        elif user_input == "exit":
            print("GOODBYE")
            break
        else:
            print("Invalid entry, please enter a valid command")

if __name__ == "__main__":
    main()
