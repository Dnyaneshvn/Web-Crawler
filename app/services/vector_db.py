import logging
from sentence_transformers import SentenceTransformer
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

logger = logging.getLogger(__name__)

def create_vector_db(chunks: dict):
    logger.info("Starting vector database creation")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    connections.connect("default", host="localhost", port="19530")

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
    ]
    schema = CollectionSchema(fields, "CUDA Documentation embeddings")
    collection = Collection("cuda_docs", schema)

    for label, sentences in chunks.items():
        embeddings = model.encode(sentences)
        ids = list(range(len(embeddings)))
        entities = [ids, embeddings]
        collection.insert(entities)

    collection.load()
    logger.info("Vector database creation completed")