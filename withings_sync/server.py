import uvicorn
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel

from withings_sync.event_queue import *

class NotifyItem(BaseModel):
    """This fits the notification for appli 1 metrics,
    based of https://developer.withings.com/developer-guide/v3/data-api/keep-user-data-up-to-date#notification-categories
    Args:
        BaseModel (_type_): pydantic input
    """    
    userid: int
    appli: int
    startdate: int
    enddate: int

def server():
    """This is the server part of the app"""
    app = FastAPI()

    @app.get("/")
    def serve_root():
        return 

    @app.get("/oauth/token")
    def serve_oauth(code: str, state: str | None = None):
        """This is triggered by the redirect url and shall contains token

        Returns:
            a fake-ass answer for now
        """
        event = ServerEvent(ServerEventMessage.OAUTH_TOKEN, {"code":code, "state":state})
        server_queue.push(event)
        return 

    @app.post("/notify")
    def serve_notify(item : NotifyItem):
        ServerEvent(ServerEventMessage.NOTIFY, item.model_dump)
        return {"Notify": "Route"}
    
    return app

def start_server(port : int):
    fast_server = server()
    uvicorn.run(fast_server, host="0.0.0.0", port=port)