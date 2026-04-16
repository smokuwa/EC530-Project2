# Listens for embeddings that have been created from the service, 
# and stores them in vectors that can be accessed by the CLI through queries 

# PUB --> CLI/query service?
# SUB --> embedding service

import json
from systems.broker_and_topics import get_redis, TOPICS

def handle_embedding(event):
    # logic to store embeddings
    return

def main():
    # logic for subscribing to embedding
    return

r = get_redis()

r.publish('test_run', json.dumps({
    "type": "",
        'path': "",
        "event_id": "",
        "payload":{
            "image_id": "",
            "path": "",
            "source": "",
            "timestamp": "",
        }
}))

