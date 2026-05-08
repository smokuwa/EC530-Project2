import json
from pathlib import Path

from shared.events import image_submitted
from systems.broker_and_topics import TOPICS, get_redis
from systems.database import save_image


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


def validate_image_path(image_path, require_exists=True):
    """
    Validate the user-provided image path and return a normalized path string.
    """
    if not isinstance(image_path, str) or not image_path.strip():
        raise ValueError("Image path must be a non-empty string")

    path = Path(image_path).expanduser()
    if path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValueError("Image path must point to a supported image file")

    if require_exists:
        if not path.exists():
            raise FileNotFoundError(f"Image file does not exist: {image_path}")
        if not path.is_file():
            raise ValueError(f"Image path is not a file: {image_path}")
        return str(path.resolve())

    return str(path)


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

    if event["type"] != "image.submitted":
        raise ValueError("Invalid event type for upload service")
    if event["topic"] != TOPICS["IMAGE_SUBMITTED"]:
        raise ValueError("Invalid topic for upload service")
    if "image_id" not in event["payload"]:
        # throw an error if the payload does not contain an image_id
        raise ValueError("Missing payload field: image_id")
    if "path" not in event["payload"]:
        # throw an error if the payload does not contain a path
        raise ValueError("Missing payload field: path")
    
# we want to build a properly formatted event that will represent a new image that will enter the system
def build_image_submitted_event(image_path, redis_client=None):
    """
    Build a standard image.submitted event.
    """
    redis_client = redis_client or get_redis()
    image_id = f"img_{redis_client.incr('image_id_counter')}"
    return image_submitted(image_id=image_id, path=image_path)

# the main function that the cli wil call when a user uploads an image
# should connect to redis, build a image.submitted event, validate that event, publish it to the redis topic, then return the event
def handle_upload(image_path, require_exists=True):
    """
    Entry point used by the CLI.
    Creates the event, validates it, and publishes it to Redis.
    """
    normalized_path = validate_image_path(image_path, require_exists=require_exists)
    redis_client = get_redis()
    # create the event using the build_event function every time this handle_upload function is called
    event = build_image_submitted_event(normalized_path, redis_client=redis_client)
    # validate that event and ensure its not messed up before we publush it
    validate_event(event)
    save_image(event["payload"]["image_id"], event["payload"]["path"])
    # publish the event into redis. give the string image.submitted and convert the python dictionary into a json string since redis publishes strings
    redis_client.publish(TOPICS["IMAGE_SUBMITTED"], json.dumps(event))
    print(f"Published {TOPICS['IMAGE_SUBMITTED']} for {event['payload']['image_id']}")
    return event
