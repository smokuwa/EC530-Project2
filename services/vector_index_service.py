# Listens for embeddings that have been created from the service, 
# and stores them in vectors that can be accessed by the CLI through queries 

# PUB --> CLI/query service?
# SUB --> embedding service

import json
from systems.broker_and_topics import get_redis, TOPICS

def handle_embedding(event):
    # subscription logic
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)

    pubsub.subscribe(TOPICS["EMBEDDING_CREATED"])
    print("Vector service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Vector service received:", event)


def main():
    # event = embedding_created() # will have info needed to get payload
    # for now, fake data
    event = [0.06, 0.23, 0.67]
    handle_embedding(event)
    
if __name__ == "__main__":
    main()
