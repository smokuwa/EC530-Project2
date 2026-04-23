# Listens for embeddings that have been created from the service, 
# and stores them in vectors that can be accessed by the CLI through queries 

# PUB --> CLI/query service?
# SUB --> embedding service

import json
from systems.broker_and_topics import get_redis, TOPICS

# function to validate event structure

def validate_event(event):
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    payload = event["payload"]
    for field in ["image_id", "path", "embedding"]:
        if field not in payload:
            raise ValueError(f"Missing payload field: {field}")


def handle_embedding(event):
    validate_event(event)
    image_id = event["payload"]["image_id"]
    get_redis().set(f"vector:{image_id}", json.dumps(event["payload"]))
    print(f"Stored vector for {image_id}")

# seperate function to subscribe to necessary event
def listen():
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(TOPICS["EMBEDDING_CREATED"])
    print("Vector service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Vector service received:", event)
        handle_embedding(event)


def main():
    listen()


if __name__ == "__main__":
    main()
