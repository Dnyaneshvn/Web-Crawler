# Web Crawler

## Setup Instructions

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Start Milvus server. Follow the [Milvus installation guide](https://milvus.io/docs/v2.0.0/install_standalone-docker.md) to set up the Milvus server.
    ```
    1. curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
    ```
    ```
    2. bash standalone_embed.sh start
    ```

3. Run the FastAPI application:
    ```
    python app/main.py
    ```
    or
    ```
    PYTHONPATH=. python app/main.py
    ```

4. Access the endpoints at `http://0.0.0.0:8000`.

## Endpoints

- `GET /crawl?url={url}`: Start crawling the given URL.
- `POST /qa`: Get an answer to the question based on the retrieved data.


