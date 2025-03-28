import queue
from pydantic import BaseModel
from dataclasses import dataclass
from enum import Enum

class ServerEventMessage(Enum):
    SHUTDOWN = 1
    NOTIFY = 2
    OAUTH_TOKEN = 3

@dataclass
class ServerEvent:
    message: ServerEventMessage
    payload: BaseModel
    
class NotifyItem(BaseModel): 
    userid: int | None
    appli: int | None
    startdate: int | None
    enddate: int | None
