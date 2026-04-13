# contains events shared across services

import time

# defining schema for events
def create_event():
    return {
        "type": "",
        'path': "",
        "event_id": "",
        "payload":{
            "image_id": "",
            "path": "",
            "source": "",
            "timestamp": time.time(),
        }
    }