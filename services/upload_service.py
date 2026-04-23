# upload service will be the entry point for new images
# it should accept an upload request from cli.py, assign the image its own id, create the image.submitted event, then send that event to redis.
# should connect to broker_and_topics.py to publish the event, connect to events.py to validate, and connect to cli.py to call the upload_service

from systems.broker_and_topics import get_redis, TOPICS
import json
from datetime import datetime, timezone

# validation exists so that bad events cannot crash the systen, so we throw an error if it's a bad event
def validate_event(event):
    """
    Basic validation for required event fields.
    """
    # create a list of everything that a valid event needs
    required_top_level = ["type", "topic", "event_id", "timestamp", "payload"]
    for field in required_top_level:
        if field not in event:
            # throw an error if a specific field is not in the event
            raise ValueError(f"Missing required field: {field}")
    if "image_id" not in event["payload"]:
        # throw an error if the payload does not contain an image_id
        raise ValueError("Missing payload field: image_id")
    if "path" not in event["payload"]:
        # throw an error if the payload does not contain a path
        raise ValueError("Missing payload field: path")
    
# we want to build a properly formatted event that will represent a new image that will enter the system
def build_image_submitted_event(image_path):
    """
    Build a standard image.submitted event.
    """
    # generate a random unique ID using redis
    image_id = f"img_{get_redis().incr('image_id_counter')}"
    event_id = f"evt_{get_redis().incr('event_id_counter')}"
    # build the proper event format
    event = {
        # identify the event for downstream consumers
        "type": "image.submitted",
        # submit which topic the event goes to
        "topic": TOPICS["IMAGE_SUBMITTED"],
        "event_id": event_id,
        # time the event was created and convert it to string
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": image_id,
            "path": image_path,

        }
    }
    return event

# the main function that the cli wil call when a user uploads an image
# should connect to redis, build a image.submitted event, validate that event, publish it to the redis topic, then return the event
def handle_upload(image_path):
    """
    Entry point used by the CLI.
    Creates the event, validates it, and publishes it to Redis.
    """
    # create the event using the build_event function every time this handle_upload function is called
    event = build_image_submitted_event(image_path)
    # validate that event and ensure its not messed up before we publush it
    validate_event(event)
    # publish the event into redis. give the string image.submitted and convert the python dictionary into a json string since redis publishes strings
    get_redis().publish(TOPICS["IMAGE_SUBMITTED"], json.dumps(event))
    print(f"Published {TOPICS['IMAGE_SUBMITTED']} for {event['payload']['image_id']}")
    return event
