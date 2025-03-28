import logging
import uvicorn
import queue
from fastapi import FastAPI, Request, status

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from withings_sync.server_event import ServerEvent, ServerEventMessage, NotifyItem

def generateServer(eventQueue: queue.Queue):
    """This is the server part of the app"""
    app = FastAPI()

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logging.error("detail", exc.errors())
        logging.error("body", exc.body)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    @app.get("/")
    def serve_root():
        return 

    @app.get("/oauth/token")
    @app.head("/oauth/token")
    def serve_oauth(code: str, state: str):
        """This is triggered by the redirect url and shall contains token

        Returns:
            a fake-ass answer for now
        """
        logging.debug("receiving token !")
        try:
            event = ServerEvent(ServerEventMessage.OAUTH_TOKEN, {"code":code, "state":state})
            eventQueue.put_nowait(event)
        except queue.Full:
            logging.error("Queue is full and shouldn't be.")
        return 
    
    @app.post("/notify")
    @app.head("/notify")
    def serve_notify(item : NotifyItem | None = None):
        logging.debug("receiving notify !")
        if item:
            event = ServerEvent(ServerEventMessage.NOTIFY, item.model_dump)
            eventQueue.put(event)
        return item
    
    return app

def run_fastAPI_server(port : int, eventQueue: queue.Queue):
    fastAPI_server = generateServer(eventQueue)
    uvicorn.run(fastAPI_server, host="0.0.0.0", port=port)