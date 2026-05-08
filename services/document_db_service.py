import json
from systems.broker_and_topics import get_redis, TOPICS
from shared.events import annotation_stored

# validate again
def validate_event(event):
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")
    payload = event["payload"]
    for field in ["image_id", "path", "objects"]:
        if field not in payload:
            raise ValueError(f"Missing payload field: {field}")

# convert inference.completed event into annotation.stored event
def build_annotation_stored_event(event):
    payload = event["payload"]
    return annotation_stored(
        image_id=payload["image_id"],
        path=payload["path"],
        annotation_id=f"ann_{payload['image_id']}",
        objects=payload["objects"],
    )

# store annotation document and publish annotation.stored
def handle_inference(event):
    validate_event(event)
    stored_event = build_annotation_stored_event(event)
    r = get_redis()
    annotation_id = stored_event["payload"]["annotation_id"]
    r.set(f"annotation:{annotation_id}", json.dumps(stored_event))
    r.publish(TOPICS["ANNOTATION_STORED"], json.dumps(stored_event))
    print(
        f"Published {TOPICS['ANNOTATION_STORED']} "
        f"for {stored_event['payload']['image_id']}"
    )

# processes a manual correction to an annotation
def handle_annotation_correction(event):
    payload = event["payload"]
    annotation_id = payload["annotation_id"]
    image_id = payload["image_id"]
    objects = payload["objects"]
    corrected_document = {
        "image_id": image_id,
        "annotation_id": annotation_id,
        "objects": objects,
        "status": "corrected"
    }
    r = get_redis()
    r.set(f"annotation:{annotation_id}", json.dumps(corrected_document))
    print(f"Updated annotation for {image_id}")

# subscribe to inference.completed and annotated.completed events
def listen():
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(TOPICS["INFERENCE_COMPLETED"],TOPICS["ANNOTATION_CORRECTED"])
    print("Document DB service listening...")
    for message in pubsub.listen():
        try:
            event = json.loads(message["data"])
            topic = message["channel"]
            print("Document DB service received:", event)
            if topic == TOPICS["INFERENCE_COMPLETED"]:
                handle_inference(event)
            elif topic == TOPICS["ANNOTATION_CORRECTED"]:
                handle_annotation_correction(event)
        except Exception as e:
            print(f"Document DB service error: {e}")

def main():
    listen()

if __name__ == "__main__":
    main()