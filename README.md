# Event-Driven Image Annotation and Retrieval System: Project 2

## System Overview:

In this project, our goals are to build a system that:
- Accept image uploads through a command-line interface (CLI)
- Process uploaded images through a simulated inference service
- Store annotation metadata in a document database service
- Generate embeddings from annotation data
- Store vector embeddings for future querying and retrieval
- Demonstrate asynchronous event-driven communication between services
- Validate events safely across the system
- Handle malformed events without crashing services

Our project implements a command-line interface system that allows users to:
1. Upload an image
2. Annotate the uploaded image (not yet fully implemented as of 05/08/2026)
3. Repeat the prompt again
4. Safety exit the system
