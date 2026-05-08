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
2. Annotate the uploaded image
3. Repeat the prompt again
4. Safety exit the system

## System Architecture:

```text
CLI
 ↓
upload_service
 publishes image.submitted
 ↓
inference_service
 publishes inference.completed
 ↓
document_db_service
 stores annotation
 publishes annotation.stored
 ↓
embedding_service
 publishes embedding.created
 ↓
vector_index_service
 stores vector:<image_id>
```

## Event Flow:
The system uses Redis Pub/Sub topics to move information between services.

### Topics Used

| Topic                 | Purpose                                 |
| --------------------- | --------------------------------------- |
| `image.submitted`     | Indicates a new image upload            |
| `inference.completed` | Indicates image processing finished     |
| `annotation.stored`   | Indicates annotation data was stored    |
| `embedding.created`   | Indicates embedding generation finished |
| `annotation.correction`| Indicates a manual annotation correction was submitted |

---

## Project Structure

```plaintext
EC530-Project2/
│
├── services/
│   ├── upload_service.py
│   ├── inference_service.py
│   ├── document_db_service.py
│   ├── embedding_service.py
│   ├── vector_index_service.py
│   └── cli_service.py
│
├── shared/
│   └── events.py
│
├── systems/
│   └── broker_and_topics.py
│
├── tests/
│   └── test_services.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
└── README.md
```

---

# How to Run the Project

## 1. Install Dependencies

Make sure Python is installed.

Run the following command:

```bash
pip install redis pytest
```

---

## 2. Start Redis Server

Run Redis locally:

```bash
redis-server
```

In another terminal, verify Redis is running:

```bash
redis-cli ping
```

You should see:

```bash
PONG
```

---

## 3. Start the Services

Open separate terminals for each service.

### Inference Service

```bash
python -m services.inference_service
```

### Document DB Service

```bash
python -m services.document_db_service
```

### Embedding Service

```bash
python -m services.embedding_service
```

### Vector Index Service

```bash
python -m services.vector_index_service
```

---

## 4. Start the CLI

Run:

```bash
python -m services.cli_service
```

You will then see the command menu.

Available commands:

```plaintext
upload --> upload an image
annotate --> manually correct annotations
help   --> display commands
exit   --> exit program
```

---

## 5. Upload an Image

Example:

```plaintext
Please enter a command: upload
Enter image path: /tmp/dog.jpg
```

If testing locally, create a temporary file first:

```bash
touch /tmp/dog.jpg
```

---

## Annotation Correction Workflow

Users can manually correct annotations through the CLI.

Example:

```plaintext
Please enter a command: annotate
Enter image ID to correct: img_1
Enter corrected object label: cat
```

The CLI publishes an `annotation.corrected` event.

The Document DB service listens for this event and updates the stored annotation document in Redis.

Example service output:

```plaintext
Updated annotation for img_1
```

---

## Example Pipeline Output

### CLI

```plaintext
Upload accepted. Image ID: img_1
```

### Inference Service

```plaintext
Inference service received: ...
Published inference.completed for img_1
```

### Document DB Service

```plaintext
Document DB service received: ...
Published annotation.stored for img_1
```

### Embedding Service

```plaintext
Embedding service received: ...
Published embedding.created for img_1
```

### Vector Index Service

```plaintext
Vector index service received: ...
Stored vector for img_1
```

---

# Redis Storage Examples

To inspect stored data:

```bash
redis-cli
```

List keys:

```bash
keys *
```

Example stored keys:

```plaintext
annotation:ann_img_1
vector:img_1
```

Retrieve stored vector:

```bash
get vector:img_1
```

Retrieve stored annotation:

```bash
get annotation:ann_img_1
```

---

# Running Unit Tests

This project uses `pytest` for testing. If everything is working correctly, you should see something like: ```X passed in X.XXs ```

## Run All Tests

```bash
python -m pytest -v
```

## Run Specific Test File

```bash
python -m pytest tests/test_services.py
```

---

# GitHub Actions

The project uses GitHub Actions for automated testing.

Whenever code is pushed to the repository:

* Dependencies are installed
* Redis server is started
* Unit tests are executed automatically

Workflow file location:

```plaintext
.github/workflows/tests.yml
```
