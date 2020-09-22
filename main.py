import logging

from solution.server import server
from solution.server.handler import StaticHandler


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    logging.info("Starting server")

    server = server.Server(handler=StaticHandler())
    server.serve()
