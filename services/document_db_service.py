# document db service is where data gets stored
# it takes inference results, stores them as a document, and then publishes annotation.stored
# as of 4/14 we don't have an annotation_service.py, so document_db_service.py should store annotation data and also act as the annotation step within this flow
# it should be inference service --> document db service --> embedding service
# subscribes to inference.completed, publishes annotation.stored