# service listens for image submission or annotation, converts it into vector embeddings, 
# and publishes the embedding to Vector Index Service

# PUB --> vector index
# SUB --> upload service

from systems.broker_and_topics import get_redis, TOPICS
import json

def handle_image_submitted(event):
    # logic surrounding image uploading event
    r = get_redis()     

    # publishes info to topics
    r.publish(TOPICS["EMBEDDING_CREATED"], json.dumps(event))
    print(f"Published embedding.created")

    # where subscription logic will take place (??)
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)

    pubsub.subscribe(TOPICS["IMAGE_SUBMITTED"])
    print("Embedding service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Embedding service received:", event)


def main():
    # event = embedding_created() # will have info needed to get payload
    # for now, fake data
    event = {
            "type": "embedding.created",
            "payload": {
                "image_id": "img_1",
                "path": "/tmp/dog.jpg"
            }
        }
    handle_image_submitted(event)


if __name__ == "__main__":
    main()