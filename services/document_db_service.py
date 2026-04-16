# document db service is where data gets stored
# it takes inference results, stores them as a document, and then publishes annotation.stored
# as of 4/14 we don't have an annotation_service.py, so document_db_service.py should store annotation data and also act as the annotation step within this flow
# it should be inference service --> document db service --> embedding service
# subscribes to inference.completed, publishes annotation.stored

from systems.broker_and_topics import get_redis, TOPICS
import json

def handle_inference(event):
    # logic surrounding  and publishing the annotation
    r = get_redis()

    # publishes info to topics
    r.publish(TOPICS["ANNOTATION_STORED"], json.dumps(event))
    print(f"Published inference.completed")

    # where subscription logic will take place (??)
    pubsub = r.pubsub(ignore_subscribe_messages=True)

    pubsub.subscribe(TOPICS["INFERENCE_COMPLETED"])
    print("Document service listening...")

    for message in pubsub.listen():
        event = json.loads(message["data"])
        print("Document service received:", event)   

def handle_annotation_correction(event):
    # logic surrounding annotation updates
    return

def main():
    # event = annotation.stored() # will have info needed to get payload
    # for now, fake data
    event = {
        "type": "annotation.stored",
        "payload": {
            "image_id": "img_1",
            "path": "/tmp/dog.jpg"
        }
    }
    handle_inference(event)
    

if __name__ == "__main__":
    main()
