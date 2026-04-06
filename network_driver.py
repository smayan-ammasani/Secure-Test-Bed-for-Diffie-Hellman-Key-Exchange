
'''
DO NOT MAKE ANY CHANGES TO THIS FILE!
This file contains the code needed to establish a network connection between
the two instances of the program.
'''

import socket
import threading
import pickle
from classes import Message

class NetworkDriver:
    def __init__(self, mode, host, port, on_message):
        self.mode = mode
        self.host = host
        self.port = port
        self.conn = None
        self.on_message = on_message

    def start(self):
        if self.mode == "listen":
            self._start_listen()
        elif self.mode == "connect":
            self._start_connect()
        else:
            raise ValueError("Mode must be 'listen' or 'connect'")

        threading.Thread(target=self._handle_receive, daemon=True).start()

    def _start_listen(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(1)
        print(f"Listening on {self.host}:{self.port}...")
        self.conn, addr = server.accept()
        print(f"Connected by {addr}")

    def _start_connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
        self.conn = client

    def _handle_receive(self):
        while True:
            try:
                data = self.conn.recv(4096)
                if not data:
                    break
                msg = pickle.loads(data)
                self.on_message(msg)
            except:
                print("Connection closed.")
                break

    def send(self, message_obj):
        try:
            data = pickle.dumps(message_obj)
            self.conn.sendall(data)
        except Exception as e:
            print("Send failed:", e)

    def close(self):
        if self.conn:
            self.conn.close()
