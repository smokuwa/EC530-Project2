import json

from systems.broker_and_topics import get_redis, TOPICS
from shared.events import inference_completed


def validate_event(event):
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    payload = event["payload"]
    for field in ["image_id", "path"]:
        if field not in payload:
            raise ValueError(f"Missing payload field: {field}")


def build_inference_completed_event(event):
    payload = event["payload"]
    return inference_completed(
        image_id=payload["image_id"],
        path=payload["path"],
        labels=["dog"],
        confidence=0.98,
    )


def handle_image_submitted(event):
    validate_event(event)
    next_event = build_inference_completed_event(event)
    get_redis().publish(TOPICS["INFERENCE_COMPLETED"], json.dumps(next_event))
    print(f"Published {TOPICS['INFERENCE_COMPLETED']} for {next_event['payload']['image_id']}")


def listen():
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(TOPICS["IMAGE_SUBMITTED"])
    print("Inference service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Inference service received:", event)
        handle_image_submitted(event)


def main():
    listen()


if __name__ == "__main__":
    main()
