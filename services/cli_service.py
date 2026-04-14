# user input allowing for uploading of files, as well as input natural language to retrieve images
# subscribes to vector index (or query service?) to search for info

# PUB --> upload service
# SUB --> vector index service (for getting info)

from systems.broker_and_topics import get_redis
import json

r = get_redis()
pubsub = r.pubsub()

# define what to do when message arrives
def handle_message(message):
    data = json.loads(message['data'])
    print(f"Received: {data}")

# subscribe to topic with handler
pubsub.subscribe(**{'test_run': handle_message})

pubsub.listen()