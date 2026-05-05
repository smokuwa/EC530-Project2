import json

from systems.broker_and_topics import get_redis, TOPICS
from shared.events import inference_completed

# we want to handle the image submitted event
def handle_image_submitted(event):
    payload = event["payload"]
    completed_event = inference_completed(
        image_id=payload["image_id"],
        path=payload["path"],
        labels=["dog"],
        confidence=0.95,
    )

    get_redis().publish(TOPICS["INFERENCE_COMPLETED"], json.dumps(completed_event))
    print("Published inference.completed")
    return completed_event


def main():
    pubsub = get_redis().pubsub(ignore_subscribe_messages=True)

    pubsub.subscribe(TOPICS["IMAGE_SUBMITTED"])
    print("Inference service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Inference service received:", event)
        handle_image_submitted(event)

if __name__ == "__main__":
    main()
