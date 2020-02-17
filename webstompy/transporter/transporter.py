"""All transporter objects (WebSocket et al.) to transport the STOMP messages.
"""

from abc import ABC, abstractmethod

import time
import threading
import websocket
from websocket._exceptions import WebSocketConnectionClosedException
import webstompy

OPCODE_DATA = (websocket.ABNF.OPCODE_TEXT, websocket.ABNF.OPCODE_BINARY)


class BaseTransporter(ABC):
    """Abstract transporter class to adapt to various connection types
    """

    @abstractmethod
    def receive(self):
        """Receive a message from the transporter connection (blocking)
        """
        pass

    @abstractmethod
    def send(self, frame):
        """Send a message to the transporter connection
        """
        pass

    @abstractmethod
    def alive(self):
        """Check transporter connection status
        """
        pass


class WebSocketPinger(threading.Thread):
    """Helper class for WebSocketTransporter to to regular WebSocket pings as
    connection keepalive.
    """
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            time.sleep(10)
            self.socket.ping()


class WebSocketTransporter(BaseTransporter):
    """webstompty transporter class through WebSockets
    """

    def __init__(self, socket):
        # TODO: Check if socket is valid, throw up if not
        self.socket = socket
        self._alive = True
        self._pinger = WebSocketPinger(self.socket)
        self._pinger.daemon = True
        self._pinger.start()

    def receive(self):
        """Receive a message from the transporter connection (blocking)
        """
        try:
            frame = self.socket.recv_frame()
        except WebSocketConnectionClosedException:
            self._alive = False
            raise webstompy.exception.ConnectionClosedException(
                'Connection closed unexpectedly!')
        except websocket.WebSocketException:
            self.socket = None
            raise
            return None
        if not frame:
            raise websocket.WebSocketException("Not a valid frame %s" % frame)
        elif frame.opcode in OPCODE_DATA:
            return frame.data
        elif frame.opcode == websocket.ABNF.OPCODE_PONG:
            return frame.data
        elif frame.opcode == websocket.ABNF.OPCODE_CLOSE:
            self.socket.send_close()
            self.socket = None
            self._alive = False
            return None
        elif frame.opcode == websocket.ABNF.OPCODE_PING:
            self.socket.pong(frame.data)
            return frame.data

    def send(self, frame):
        """Send a message to the transporter connection
        """
        self.socket.send(frame)

    @property
    def alive(self):
        """Check transporter connection status
        """
        return self._alive
