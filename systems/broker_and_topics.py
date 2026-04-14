# broker sets up the REDIS connection that is shared across services
# topics defines the topic names

import redis

def get_redis():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)

TOPICS = {
    'IMAGE_SUBMITTED':      'image.submitted',
    'INFERENCE_COMPLETED':  'inference.completed',
    'ANNOTATION_STORED':    'annotation.stored',
    'EMBEDDING_CREATED':    'embedding.created',
    'ANNOTATION_CORRECTED': 'annotation.corrected'
}