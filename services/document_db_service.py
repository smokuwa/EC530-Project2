import json

from systems.broker_and_topics import get_redis, TOPICS
from shared.events import annotation_stored

# function to validate structure of event input
def validate_event(event):
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    payload = event["payload"]
    for field in ["image_id", "path", "labels"]:
        if field not in payload:
            raise ValueError(f"Missing payload field: {field}")

# formatting of event
def build_annotation_stored_event(event):
    payload = event["payload"]
    return annotation_stored(
        image_id=payload["image_id"],
        path=payload["path"],
        annotation_id=f"ann_{payload['image_id']}",
        labels=payload["labels"],
    )

# seperate function for publishing information
def handle_inference(event):
    validate_event(event)
    stored_event = build_annotation_stored_event(event)
    r = get_redis()
    r.set(f"annotation:{stored_event['payload']['annotation_id']}", json.dumps(stored_event))
    r.publish(TOPICS["ANNOTATION_STORED"], json.dumps(stored_event))
    print(f"Published {TOPICS['ANNOTATION_STORED']} for {stored_event['payload']['image_id']}")

# have yet to figure this one out, use llm to generate?
def handle_annotation_correction(event):
    return

# seperate function to subscribe to events
def listen():
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(TOPICS["INFERENCE_COMPLETED"])
    print("Document service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Document service received:", event)
        handle_inference(event)


def main():
    listen()


if __name__ == "__main__":
    main()
