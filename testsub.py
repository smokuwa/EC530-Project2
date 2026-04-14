# subscriber: vector index service
import json
from systems.broker_and_topics import get_redis

r = get_redis()
pubsub = r.pubsub(ignore_subscribe_messages=True)
pubsub.subscribe("embedding.created")

def save_to_vector_index(image_id, embedding, metadata):
    print(f"Indexing {image_id}")
    # actual vector DB write goes here

print("Listening for embedding.created...")

for message in pubsub.listen():
    if message["type"] != "message":
        continue

    event = json.loads(message["data"].decode("utf-8"))
    payload = event["payload"]

    save_to_vector_index(
        image_id=payload["image_id"],
        embedding=payload["embedding"],
        metadata={
            "path": payload["path"],
            "source": payload["source"],
            "timestamp": payload["timestamp"],
        },
    )