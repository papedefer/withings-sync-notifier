import logging
import sys
from threading import Thread
from importlib.metadata import version
import queue
import signal

from withings_sync.cli_parser import ARGS
from withings_sync.server_event import ServerEvent, ServerEventMessage
from withings_sync.sync import manual_sync, continuous_sync
from withings_sync.server_2 import run_fastAPI_server


def start_server(eventQueue : queue.Queue):
    thread = Thread(target=run_fastAPI_server, args={ARGS.port, eventQueue}, daemon=True)
    thread.start()
    continuous_sync(eventQueue)
    
def main():
    """Main"""
    logging.basicConfig(
        level=logging.DEBUG if ARGS.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    # logging.debug("withings-sync script version %s", version("withings-sync"))
    logging.debug("Script invoked with the following arguments: %s", ARGS)

    if sys.version_info < (3, 7):
        print("Sorry, requires at least Python3.7 to avoid issues with SSL.")
        sys.exit(1)

    if (ARGS.mode != "server"):
        manual_sync()
    elif (ARGS.mode == "server"):
        eventQueue = queue.Queue()
        def gracefull_shutdown(errno, frame):
            event = ServerEvent(ServerEventMessage.SHUTDOWN, {})
            eventQueue.put(event)
        signal.signal(signal.SIGINT, gracefull_shutdown)
        start_server(eventQueue)
