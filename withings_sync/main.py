import logging
import sys
from threading import Thread
from importlib.metadata import version

from withings_sync.cli_parser import ARGS
from withings_sync.sync import manual_sync, continuous_sync
from withings_sync.server import start_server

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
        try:
            server = Thread(target=start_server, args=[ARGS.port])
            server.start()
            continuous_sync()
        except KeyboardInterrupt:
            logging.info("Shutting down server")
        server.join()
        sys.exit(0)
