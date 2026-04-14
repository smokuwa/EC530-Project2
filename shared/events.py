# contains events shared across services
# has all the functions that are at the bottom of class slides, import to respective modules

# this should help with creating or validating events

import time

# defining schema for events
# make functions async
async def create_event():
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