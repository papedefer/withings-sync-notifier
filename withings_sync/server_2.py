import logging
import queue
import asyncio
from fastapi import FastAPI
from contextlib import  asynccontextmanager

def create_FastAPI_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logging.info("HELLO WORLD!")
        yield
        logging.info("GOODBYE WORLD!")

    app = FastAPI(lifespan=lifespan)

    @app.get("/")
    def serve_root():
        return 

    @app.get("/oauth/token")
    @app.head("/oauth/token")
    def serve_oauth(code: str, state: str):
        logging.info("receiving token !")
        return 

    @app.post("/notify")
    @app.head("/notify")
    def serve_notify():
        logging.info("receiving notify !")
        return 
    return app


def start_server():
    app = create_FastAPI_app()
    uvicorn.run(app, host="0.0.0.0", port=ARGS.port)

