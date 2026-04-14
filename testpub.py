# publisher: embedding service
import json
from systems.broker_and_topics import get_redis

r = get_redis()

def publish_embedding_created(image_id, path, embedding):
    event = {
        "type": "embedding.created",
        "event_id": f"evt_{image_id}",
        "payload": {
            "image_id": image_id,
            "path": path,
            "source": "embedding_service",
            "timestamp": "2026-04-14T12:00:00Z",
            "embedding": embedding,
        },
    }

    delivered = r.publish("embedding.created", json.dumps(event))
    print(f"Published to {delivered} subscriber(s)")