import json
from systems.broker_and_topics import get_redis, TOPICS
from shared.events import embedding_created

# validate the event once again
def validate_event(event):
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")
    payload = event["payload"]
    for field in ["image_id", "path", "objects"]:
        if field not in payload:
            raise ValueError(f"Missing payload field: {field}")

# build a deterministic placeholder embedding based on how many objects were found
def build_embedding_created_event(event):
    payload = event["payload"]
    objects = payload["objects"]
    scale = max(len(objects), 1)
    embedding = [round((index + 1) / (scale + 1), 2) for index in range(3)]
    return embedding_created(
        image_id=payload["image_id"],
        path=payload["path"],
        embedding=embedding,
    )

# validate the annotation event, then publish the embedding event
def handle_annotation_stored(event):
    validate_event(event)
    next_event = build_embedding_created_event(event)
    get_redis().publish(TOPICS["EMBEDDING_CREATED"], json.dumps(next_event))
    print(f"Published {TOPICS['EMBEDDING_CREATED']} for {next_event['payload']['image_id']}")

# listen for completed annotation events from redis
def listen():
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(TOPICS["ANNOTATION_STORED"])
    print("Embedding service listening...")
    for message in pubsub.listen():
        try:
            # decode each Redis message and pass it through the embedding workflow
            event = json.loads(message["data"])
            print("Embedding service received:", event)
            handle_annotation_stored(event)
        except Exception as e:
            # keep the service running even if one message is bad
            print(f"Embedding service error: {e}")

def main():
    listen()

if __name__ == "__main__":
    main()
