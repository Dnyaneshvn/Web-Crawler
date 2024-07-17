import logging
from fastapi import APIRouter
from app.services.qa import answer_question

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/qa")
def qa(query: str):
    logger.info(f"Received QA request for query: {query}")
    answer = answer_question(query)
    logger.info("QA process completed")
    return {"message": "Answer generated", "answer": answer}