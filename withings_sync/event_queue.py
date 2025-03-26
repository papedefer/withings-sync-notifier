import queue
from pydantic import BaseModel
from dataclasses import dataclass
from enum import Enum

class ServerEventMessage(Enum):
    NOTIFY = "notify"
    OAUTH_TOKEN = "oauth_token"

@dataclass
class ServerEvent:
    message: ServerEventMessage
    payload: dict

class EventQueue():
    def __init__(self):
        self.queue=queue.Queue(10) # arbitrary 10 events for now
    
    def push(self, event : ServerEvent):
        self.queue.put(event)

    def pop(self, block : bool = True, timeout : float | None =None) -> ServerEvent:
        return self.queue.get()

    def empty(self):
        return self.queue.empty()

server_queue = EventQueue()