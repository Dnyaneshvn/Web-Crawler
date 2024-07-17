import logging
from fastapi import APIRouter, BackgroundTasks
from app.services.web_crawler import crawl_website
from app.services.chunking import chunk_data
from app.services.vector_db import create_vector_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/crawl")
def crawl(url: str, background_tasks: BackgroundTasks):
    logger.info(f"Received crawl request for URL: {url}")
    data = crawl_website(url)
    logger.info("Crawling completed, starting chunking process")
    chunks = chunk_data(data)
    logger.info("Chunking completed, starting vector database creation")
    background_tasks.add_task(create_vector_db, chunks)
    logger.info("Vector database creation task added to background tasks")
    return {"message": "Crawling and processing started"}