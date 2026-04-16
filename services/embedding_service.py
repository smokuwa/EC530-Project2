# service listens for image submission or annotation, converts it into vector embeddings, 
# and publishes the embedding to Vector Index Service

# PUB --> vector index
# SUB --> upload service

from systems.broker_and_topics import get_redis, TOPICS