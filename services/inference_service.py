# inference service will react to a new uploaded image and produce a simulated inference result, so it basically processes the image before moving along
# it should subcribe to image.submitted, read the incoming event, validate the event, simulate inference, build the inference.completed event, and then publish that event
# it should connect to broker_and_topics.py, events.py
# image processing

from systems.broker_and_topics import get_redis, TOPICS
from shared.events import inference_completed

def handle_image_submitted(event):
    # logic for publishing
    return

def main():
    # subscription logic
    return