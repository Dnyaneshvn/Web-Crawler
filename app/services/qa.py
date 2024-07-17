import logging
from transformers import pipeline
from app.services.retrieval import retrieve_data

logger = logging.getLogger(__name__)

def answer_question(query: str):
    logger.info("Starting question answering process")
    nlp = pipeline("question-answering")
    retrieved_data = retrieve_data(query)
    context = " ".join([item.entity.get("text", "") for item in retrieved_data])
    result = nlp(question=query, context=context)
    logger.info("Question answering completed")
    return result['answer']