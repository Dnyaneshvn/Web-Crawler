import logging
from sentence_transformers import SentenceTransformer
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility, Index

logger = logging.getLogger(__name__)

def create_vector_db(chunks: dict):
    logger.info("Starting vector database creation")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    connections.connect("default", host="localhost", port="19530")

    collection_name = "cuda_docs"
    
    # Define the schema
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=4096)
    ]
    schema = CollectionSchema(fields, "CUDA Documentation embeddings")

    # Check if the collection already exists
    if utility.has_collection(collection_name):
        collection = Collection(collection_name)
        if collection.schema != schema:
            logger.warning("Existing collection schema does not match the new schema. Dropping the existing collection.")
            utility.drop_collection(collection_name)
            collection = Collection(collection_name, schema)
            logger.info("Created a new collection with the correct schema.")
        else:
            logger.info("Using existing collection with matching schema")
    else:
        collection = Collection(collection_name, schema)
        logger.info("Created a new collection")

    max_length = 4096
    entity_batches = []

    for label, sentences in chunks.items():
        for sentence in sentences:
            if len(sentence) > max_length:
                logger.warning(f"Skipping sentence as it exceeds max length of {max_length}: {sentence[:100]}...")
                continue
            embedding = model.encode([sentence])[0]
            entity_batches.append([len(entity_batches), embedding, sentence])
    
    batch_size = 100  # Adjust batch size if needed
    for i in range(0, len(entity_batches), batch_size):
        batch = entity_batches[i:i+batch_size]
        ids = [x[0] for x in batch]
        embeddings = [x[1] for x in batch]
        contents = [x[2] for x in batch]
        collection.insert([ids, embeddings, contents])
    
    # Create an index
    index_params = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    
    collection.load()
    logger.info("Vector database creation completed")