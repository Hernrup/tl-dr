#!/usr/bin/env python
from app import api
import logging
import sys
import signal
from cherrypy import wsgiserver
import cherrypy
import os

logger = None
server = None


def main():
    global logger
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # logger
    logger = api.logger

    # Set exit handler
    set_exit_handler(on_exit)

    # Start server
    if os.environ.get('PORT') is None:
        start_server(5000)
    else:
        start_server(os.environ.get('PORT'))


# Start server
def start_server(port):
    global server
    # Ready to serve
    logger.info("Server is starting on port {}".format(port))

    cherrypy.config.update({
        'log.screen': True
    })

    d = wsgiserver.WSGIPathInfoDispatcher({'/': api})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', port), d)

    server.start()


# Define Exit handler
def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    logger.info("Exit handler triggered")
    server.stop()
    sys.exit(0)


if __name__ == '__main__':
    main()
