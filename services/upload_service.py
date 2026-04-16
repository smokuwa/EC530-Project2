# upload service will be the entry point for new images
# it should accept an upload request from cli.py, assign the image its own id, create the image.submitted event, then send that event to redis.
# should connect to broker_and_topics.py to publish the event, connect to events.py to validate, and connect to cli.py to call the upload_service

from systems.broker_and_topics import get_redis, TOPICS
from shared.events import image_submitted