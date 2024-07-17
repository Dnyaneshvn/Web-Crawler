import logging
from sentence_transformers import SentenceTransformer
from pymilvus import Collection

logger = logging.getLogger(__name__)

def retrieve_data(query: str):
    logger.info(f"Starting data retrieval for query: {query}")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    collection = Collection("cuda_docs")
    
    query_vector = model.encode([query])[0].tolist()
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search([query_vector], "embedding", search_params, limit=10, output_fields=["id"])

    logger.info("Data retrieval completed")
    return results