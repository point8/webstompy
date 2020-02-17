"""StompConnection: a STOMP connection
"""

import queue
import logging

from webstompy.transporter import WebSocketTransporter
from webstompy.receiver import StompReceiver
from webstompy.logging import get_logger
import webstompy


class StompConnection(object):
    """StompConnection: a STOMP connection

    Parameters
    ----------
    connector:
        The connector to communicate over, to be used in `transporter`
    transporter: webstompy.transporter.transporter.BaseTransporter
        The transporter to handle the actual communication with the
        connector (in most cases a
        `webstompy.transporter.transporter.WebSocketTransporter`)
    """

    def __init__(self, connector=None, transporter=WebSocketTransporter):
        """StompConnection constructor
        """
        self.logger = get_logger(f'{__name__}.{self.__class__.__name__}')
        # TODO: Add logging
        # TODO: Check if transporter is valid, throw up if not
        self._connector = connector
        self._transporter = transporter(self._connector)
        self._queue_frames = queue.Queue()
        self._queue_listener = queue.Queue()
        self._receiver = StompReceiver(transporter=self._transporter,
                                       queue_frames=self._queue_frames,
                                       queue_listener=self._queue_listener)
        self.logger.info('New webstompy connection initializing. '
                         'Starting receiver daemon.')
        self._receiver.daemon = True
        self._receiver.start()
        self._frame_connected = None

    def _send_frame(self, frame):
        """Send a StompFrame to the server

        Parameters
        ----------
        frame: webstompy.StompFrame
            Frame to send to the server via the transporter.
        """
        if __debug__:
            self.logger.debug(f'Sending frame to server: {frame}')
        self._transporter.send(frame.payload)

    def add_listener(self, listener):
        """Add a listener to be invoked in case of events.

        Parameters
        ----------
        listener: webstompy.StompListener
            Listener to be derived from `webstompy.StompListener`.
        """
        self.logger.info(f'Adding listener {listener.__class__.__name__} to '
                         'StompConnection.')
        self._queue_listener.put(listener)

    def connect(self, login=None, passcode=None, timeout=None):
        """Connect to the STOMP server

        Parameters
        ----------
        login: str
            The user id used to authenticate against a secured STOMP server
            (None to login without user id).
        passcode: str
            The password used to authenticate against a secured STOMP server
            (None to login without password).
        timeout: int
            Timeout to wait for the confirmation of the connection from the
            server (None means: wait forever).

        Returns
        -------
        frame_connected: webstompy.StompFrame
            The CONNECTED frame upon success.
        """
        header = [('accept-version', '1.1')]
        if login is not None:
            header.append(('login', login))
        if passcode is not None:
            header.append(('passcode', passcode))
        frame = webstompy.StompFrame('CONNECT', header, None)
        self._send_frame(frame)
        frame_connected = self._queue_frames.get(timeout=timeout)
        if frame_connected.command == b'CONNECTED':
            self._frame_connected = frame_connected
            self.logger.info(f'Connection successfully initialized.')
            return frame_connected
        else:
            raise webstompy.exception.ConnectFailedException(
                'Did not receive a valid CONNECTED response!')

    def send(self, destination, message='', content_type='text/plain',
             content_length=None):
        """Send a message to the STOMP server

        Parameters
        ----------
        destination str
            The destination to send this message to (required).
        message str
            The message body to send.
        content_type str
            Content type of the message body.
        content_length: int
            Content length of the message body (byte count).
        """
        header = [('destination', destination),
                  ('content-type', content_type)]
        if content_length is not None:
            header.append(('content-length', content_length))
        frame = webstompy.StompFrame('SEND', header, message)
        self._send_frame(frame)

    def subscribe(self, destination, id):
        """Subscribe to messages under a given destination/topic.

        Parameters
        ----------
        destination str
            The destination to subscribe to (required).
        id str
            The id to subscribe under (must be unique for each subscription).
        """
        self.logger.info(f'Subscribing to destination {destination}.')
        header = [('destination', destination),
                  ('id', id)]
        frame = webstompy.StompFrame('SUBSCRIBE', header, None)
        self._send_frame(frame)

    @property
    def alive(self):
        """Detect whether connection is still alive.

        Returns
        -------
        is_alive: bool
            Whether connection is still alive.
        """
        return self._transporter.alive
