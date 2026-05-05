import json

from systems.broker_and_topics import get_redis, TOPICS
import json
from datetime import datetime, timezone

# validate the image again
def validate_image_submitted_event(event):
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")
    if "image_id" not in event["payload"]:
        raise ValueError("Missing payload field: image_id")
    if "path" not in event["payload"]:
        raise ValueError("Missing payload field: path")

# this pretends to process an image and returns fake detection results so the rest of the system can work, useful for debugging
def simulate_inference(payload):
    """
    Fake image processing result.
    """
    return {
        "image_id": payload["image_id"],
        "path": payload["path"],
        "objects": [
            {"label": "dog", "bbox": [10, 20, 120, 180], "conf": 0.95},
            {"label": "person", "bbox": [150, 30, 250, 200], "conf": 0.88}
        ],
        "model_version": "sim_v1"
    }

# takes the processed image result and wraps it into a proper inference.completed event so it can be sent to the next service
def build_inference_completed_event(processed_result, original_event_id):
    r = get_redis()
    event = {
        "type": "publish",
        "topic": TOPICS["INFERENCE_COMPLETED"],
        "event_id": f"evt_{r.incr('event_id_counter')}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": processed_result,
        "parent_event_id": original_event_id
    }
    return event

def process_image_submitted_event(event):
    r = get_redis()
    validate_image_submitted_event(event)
    processed_result = simulate_inference(event["payload"])
    completed_event = build_inference_completed_event(
        processed_result,
        event["event_id"]
    )
    r.publish(TOPICS["INFERENCE_COMPLETED"], json.dumps(completed_event))
    print(f"Published {TOPICS['INFERENCE_COMPLETED']} for {processed_result['image_id']}")

def listen_for_uploaded_images():
    r = get_redis()
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(TOPICS["IMAGE_SUBMITTED"])
    print("Inference service listening for image.submitted...")
    for message in pubsub.listen():
        try:
            event = json.loads(message["data"])
            print("Inference service received:", event)
            process_image_submitted_event(event)
        except Exception as e:
            print(f"Inference service error: {e}")

def main():
    listen_for_uploaded_images()

if __name__ == "__main__":
    main()