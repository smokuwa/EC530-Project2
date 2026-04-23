# inference service will react to a new uploaded image and produce a simulated inference result, so it basically processes the image before moving along
# it should subcribe to image.submitted, read the incoming event, validate the event, simulate inference, build the inference.completed event, and then publish that event
# it should connect to broker_and_topics.py, events.py
# image processing

from systems.broker_and_topics import get_redis, TOPICS
import json
from datetime import datetime, timezone

# we want to handle the image submitted event
def handle_image_submitted(event):
    processed_result = {
        "image_id": event["payload"]["image_id"],
        "path": event["payload"]["path"],
        "objects": [
            {"label": "dog", "bbox": [10, 20, 120, 180], "conf": 0.95}
        ]
    }

    completed_event = {
        "type": "publish",
        "topic": TOPICS["INFERENCE_COMPLETED"],
        "event_id": f"evt_{get_redis().incr('event_id_counter')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": processed_result
    }

    get_redis().publish(TOPICS["INFERENCE_COMPLETED"], json.dumps(completed_event))
    print("Published inference.completed")


def main():
    pubsub = get_redis.pubsub(ignore_subscribe_messages=True)

    pubsub.subscribe(TOPICS["IMAGE_SUBMITTED"])
    print("Inference service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Inference service received:", event)
        handle_image_submitted(event)


if __name__ == "__main__":
    main()