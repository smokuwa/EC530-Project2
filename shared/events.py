# contains events shared across services
# has all the functions that are at the bottom of class slides, import to respective modules

# this should help with creating or validating events

from systems.broker_and_topics import get_redis, TOPICS

import json

r = get_redis()

def image_submitted(image_id:str, path:str):
    return {
       "payload":{
            "image_id": image_id,
            "path": path,
        } 
    }

def inference_completed(image_id:str, path:str, labels:list[str], confidence:int):
   return {
       "payload":{
            "image_id": image_id,
            "path": path,
            "labels": labels,
            "confidence": confidence,
        } 
    }

def annotation_stored(image_id:str, annotation_id:str, labels:list[str]):
   return {
       "payload":{
            "image_id": image_id,
            "annotion_id": annotation_id,
            "labels": labels,
        } 
    }

def embedding_created(image_id:str, path:str, embedding:list[int]):
   return {
       "payload":{
            "image_id": image_id,
            "path": path,
            "embedding": embedding,
        } 
    }

def annotation_corrected(image_id:str, annotation_id:int, corrected_labels:list[str]):
   return {
       "payload":{
            "image_id": image_id,
            "annotation_id": annotation_id,
            "corrected_labels": corrected_labels,
        } 
    }

