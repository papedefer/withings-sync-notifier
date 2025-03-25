from fastapi import FastAPI, Response, Request
from pydantic import BaseModel


class NotifyItem(BaseModel):
    """This fits the notification for appli 1 metrics,
    based of https://developer.withings.com/developer-guide/v3/data-api/keep-user-data-up-to-date#notification-categories
    Args:
        BaseModel (_type_): pydantic input
    """    
    userid: int
    appli: int
    stardate: int
    enddate: int

app = FastAPI()

@app.post("/oauth/access-token")
def serve_oauth(code: str, state: str | None = None):
    """This is triggered by the redirect url and shall contains token

    Returns:
        a fake-ass answer for now
    """
    myresp = Response(content=f"Thanks, ${code}, ${state}");
    return myresp

@app.post("/notify")
def serve_notify(item : NotifyItem):
    return {"Notify": "Route"}