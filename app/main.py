import sys
import os
import logging
from fastapi import FastAPI
import uvicorn
from app.routers import crawl, qa

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

app.include_router(crawl.router)
app.include_router(qa.router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the NVIDIA CUDA Documentation Crawler"}

if __name__ == "__main__":
    logger.info("Starting server")
    uvicorn.run(app, host="0.0.0.0", port=8000)