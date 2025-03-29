import logging
import asyncio
import uvicorn
from typing import Annotated

from fastapi import FastAPI, Request, status, Form
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import  asynccontextmanager

from withings_sync.cli_parser import ARGS
from withings_sync.withings2 import WithingsOAuth2, WithingsAccount, WithingsException
from withings_sync.sync import sync

class WithingsServer:
    withings_oauth : WithingsOAuth2 | None = None
    withings_manager : WithingsAccount | None = None
    
    def __init__(self):
        self.app = FastAPI(lifespan=self.lifespan)

        self.app.add_api_route("/", self.serve_root, methods=["GET"])
        self.app.add_api_route("/oauth/token", self.serve_oauth, methods=["GET", "HEAD"])
        self.app.add_api_route("/notify", self.serve_notify, methods=["POST", "HEAD"])
        self.app.add_exception_handler(RequestValidationError, self.validation_exception_handler)

    def __del__(self):
        if self.withings_manager:
            logging.info("closing withings oauth !")
            self.withings_manager.revoke_notify()
            
    async def validation_exception_handler(self, request: Request, exc: RequestValidationError):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        logging.error(f"{request}: {exc_str}")
        content = {'status_code': 10422, 'message': exc_str, 'data': None}
        return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def startOAuth2(self):
        logging.info("starting OAuth2 !")
        self.withings_oauth = WithingsOAuth2(server_mode=True)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        self.startOAuth2()
        yield

    def serve_root(self):
        logging.debug(f"receiving root !")
        return 

    def serve_oauth(self, code: str | None = None, state: str | None = None):
        logging.debug("receiving token !")
        if not code:
            return
        self.withings_oauth.server_wrapper(code)
        self.withings_manager = WithingsAccount(self.withings_oauth)
        self.withings_manager.subscribe_notify()
        return

    def serve_notify(self, userid : Annotated[str | None, Form()] = None, 
                            appli : Annotated[int | None, Form()] = None, 
                            startdate : Annotated[int | None, Form()] = None, 
                            enddate : Annotated[int | None, Form()] = None):
        logging.debug("receiving notify !")
        if userid:
            sync(self.withings_manager, startdate, enddate)
        return

def start_server():
    server = WithingsServer()
    uvicorn.run(server.app, host="0.0.0.0", port=ARGS.port)

