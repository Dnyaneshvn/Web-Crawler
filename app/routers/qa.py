from fastapi import APIRouter, Request
from app.services.qa import answer_question

router = APIRouter()

@router.post("/qa")
async def qa(request: Request):
    query = request.query_params.get("query")
    answer = answer_question(query)
    return {"query": query, "answer": answer}