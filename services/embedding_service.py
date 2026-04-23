import json

from systems.broker_and_topics import get_redis, TOPICS
from shared.events import embedding_created


def validate_event(event):
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    payload = event["payload"]
    for field in ["image_id", "path", "labels"]:
        if field not in payload:
            raise ValueError(f"Missing payload field: {field}")


def build_embedding_created_event(event):
    payload = event["payload"]
    labels = payload["labels"]
    scale = max(len(labels), 1)
    embedding = [round((index + 1) / (scale + 1), 2) for index in range(3)]
    return embedding_created(
        image_id=payload["image_id"],
        path=payload["path"],
        embedding=embedding,
    )


def handle_annotation_stored(event):
    validate_event(event)
    next_event = build_embedding_created_event(event)
    get_redis().publish(TOPICS["EMBEDDING_CREATED"], json.dumps(next_event))
    print(f"Published {TOPICS['EMBEDDING_CREATED']} for {next_event['payload']['image_id']}")


def listen():
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(TOPICS["ANNOTATION_STORED"])
    print("Embedding service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Embedding service received:", event)
        handle_annotation_stored(event)


def main():
    listen()


if __name__ == "__main__":
    main()
