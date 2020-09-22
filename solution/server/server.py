import atexit
import os
import signal
import socket
import logging

import config
from solution.server.handler import BaseHandler


class Server:
    def __init__(self, handler: BaseHandler):
        self.handler = handler

        self.socket = None

        self.workers = []

        self.ADDRESS = config.ADDRESS
        self.PORT = config.PORT
        self.MAX_CONNECTIONS = config.MAX_CONNECTIONS

        self.THREAD_LIMIT = config.THREAD_LIMIT

    def _prepare_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ADDRESS, self.PORT))
        self.socket.listen(self.MAX_CONNECTIONS)
        logging.info("socket started to listen")

    def _wait(self):
        for worker in self.workers:
            os.waitpid(worker, 0)

    def _kill_all(self):
        # kill all child processes before exiting program
        atexit.register(self._kill_all())

        for worker in self.workers:
            os.kill(worker, signal.SIGTERM)

    def serve(self):
        self._prepare_socket()

        for i in range(self.THREAD_LIMIT):
            pid = os.fork()

            if pid == 0:
                logging.info(f"Starting new fork: {i}")

                while True:
                    conn, addr = self.socket.accept()
                    logging.info(f'Accepted new connection {addr}')

                    try:
                        self.handler.handle(conn)
                    except Exception as e:
                        logging.error(f'error, while proccessing connection: {str(e)}')

                    conn.close()
                    logging.info(f'connection closed {addr}')
            else:
                self.workers.append(pid)

        self._wait()
