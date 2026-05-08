import time
import uuid

from systems.broker_and_topics import TOPICS


EVENT_TOPICS = {
    "image.submitted": TOPICS["IMAGE_SUBMITTED"],
    "inference.completed": TOPICS["INFERENCE_COMPLETED"],
    "annotation.stored": TOPICS["ANNOTATION_STORED"],
    "embedding.created": TOPICS["EMBEDDING_CREATED"],
    "annotation.corrected": TOPICS["ANNOTATION_CORRECTED"],
}


def make_event(event_type: str, payload: dict) -> dict:
    return {
        "type": event_type,
        "topic": EVENT_TOPICS[event_type],
        "event_id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "payload": payload,
    }


def image_submitted(image_id: str, path: str) -> dict:
    return make_event(
        "image.submitted",
        {
            "image_id": image_id,
            "path": path,
        },
    )


def inference_completed(
    image_id: str,
    path: str,
    labels: list[str],
    confidence: float,
) -> dict:
    return make_event(
        "inference.completed",
        {
            "image_id": image_id,
            "path": path,
            "labels": labels,
            "confidence": confidence,
        },
    )


def annotation_stored(
    image_id: str,
    path: str,
    annotation_id: str,
    objects: list[dict],
) -> dict:
    return make_event(
        "annotation.stored",
        {
            "image_id": image_id,
            "path": path,
            "annotation_id": annotation_id,
            "objects": objects,
        },
    )


def embedding_created(
    image_id: str,
    path: str,
    embedding: list[float],
) -> dict:
    return make_event(
        "embedding.created",
        {
            "image_id": image_id,
            "path": path,
            "embedding": embedding,
        },
    )


def annotation_corrected(
    image_id: str,
    annotation_id: str,
    objects: list[dict]
) -> dict:
    return make_event(
        "annotation.corrected",
        {
            "image_id": image_id,
            "annotation_id": annotation_id,
            "objects": objects,
        },
    )
