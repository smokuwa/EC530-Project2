# inference service will react to a new uploaded image and produce a simulated inference result, so it basically processes the image before moving along
# it should subcribe to image.submitted, read the incoming event, validate the event, simulate inference, build the inference.completed event, and then publish that event
# it should connect to broker_and_topics.py, events.py
# image processing

from systems.broker_and_topics import get_redis, TOPICS
from shared.events import inference_completed
import json

def handle_image_submitted(event):
    r = get_redis()

    # publishes info to topics
    r.publish(TOPICS["INFERENCE_COMPLETED"], json.dumps(event))
    print(f"Published inference.completed")

    # subscription logic
    pubsub = r.pubsub(ignore_subscribe_messages=True)

    pubsub.subscribe(TOPICS["IMAGE_SUBMITTED"])
    print("Inference service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Inference service received:", event)

def main():
    # event = inference_completed() # will have info needed to get payload
    # for now, fake data
    event = {
            "type": "inference.completed",
            "payload": {
                "image_id": "img_1",
                "path": "/tmp/dog.jpg"
            }
        }
    handle_image_submitted(event)

    

if __name__ == "__main__":
    main()
