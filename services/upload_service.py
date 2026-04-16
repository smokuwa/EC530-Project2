# upload service will be the entry point for new images
# it should accept an upload request from cli.py, assign the image its own id, create the image.submitted event, then send that event to redis.
# should connect to broker_and_topics.py to publish the event, connect to events.py to validate, and connect to cli.py to call the upload_service

from systems.broker_and_topics import get_redis, TOPICS
import json

def handle_upload(event):
    r = get_redis()    
    # publishes info to topics
    r.publish(TOPICS["IMAGE_SUBMITTED"], json.dumps(event))
    print(f"Published image.submitted")

def main():
    # event = image_submitted() # will have info needed to get payload
    # for now, fake data
    event = {
            "type": "image.submitted",
            "payload": {
                "image_id": "img_1",
                "path": "/tmp/dog.jpg"
            }
        }
    handle_upload(event)

if __name__ == "__main__":
    main()