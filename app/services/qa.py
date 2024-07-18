import logging
import json
from transformers import pipeline
from pymilvus import Collection, connections

logger = logging.getLogger(__name__)

def answer_question(query: str) -> str:
    logger.info("Starting question answering process")
    nlp = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")
    
    collection_name = "cuda_docs"
    connections.connect("default", host="localhost", port="19530")
    collection = Collection(collection_name)
    
    # Search for relevant documents
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_vector = model.encode([query])[0]
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search([query_vector], "embedding", search_params, limit=5)
    
    context_list = []
    for hit in results[0]:
        try:
            entity = hit.entity
            context = entity["content"]
            if len(context) > 0:
                context_list.append(context)
        except KeyError:
            logger.error(f"Failed to extract content from hit: {hit}")
    
    if not context_list:
        logger.info("No relevant data retrieved. Context is empty.")
        return "No answer found."
    
    context = " ".join(context_list)
    answer = nlp(question=query, context=context)
    return answer["answer"] if answer else "No answer found."