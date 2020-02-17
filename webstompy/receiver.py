"""StompReceiver: a STOMP receiver to be run in a thread
"""

import threading
import queue
import logging

from webstompy.transporter import WebSocketTransporter
from webstompy.logging import get_logger
import webstompy


class StompReceiver(threading.Thread):
    """StompReceiver: a STOMP receiver to be run in a thread

    Parameters
    ----------
    connector:
        The connector to communicate over, to be used in `transporter`
    queue_frames: queue.Queue
        The queue to put the frames in this StompReceiver receives
    queue_listener: queue.Queue
        The queue for `webstompy.StompListener` to invoke upon events
    transporter: webstompy.transporter.transporter.BaseTransporter
        The transporter instance to handle the actual communication with the
        connector (in most cases a
        webstompy.transporter.transporter.WebSocketTransporter)
    """

    def __init__(self, transporter, queue_frames, queue_listener):
        """StompReceiver constructor
        """
        self.logger = get_logger(f'{__name__}.{self.__class__.__name__}')
        threading.Thread.__init__(self)
        self._transporter = transporter
        self._queue_frames = queue_frames
        self._queue_listener = queue_listener
        self._listener = []
        if __debug__:
            self.logger.debug('Receiver daemon up and running.')

    def run(self):
        while True:
            try:
                frame_bytes = self._transporter.receive()
            except webstompy.exception.ConnectionClosedException:
                self.logger.error(f'WebSocket connection closed unexpectedly.')
                break
            # TODO: We should get all listeners here (implement a while loop
            # continuing as long as self._queue_listener contains entries)
            try:
                listener = self._queue_listener.get(block=False)
                self._listener.append(listener)
                if __debug__:
                    self.logger.debug(f'Listener {listener.__class__.__name__}'
                                      ' registered in receiver daemon.')
            except queue.Empty:
                pass
            # TODO: Use logging here
            frame = None
            if len(frame_bytes) > 0:
                try:
                    frame = webstompy.StompFrame(payload=frame_bytes)
                    if __debug__:
                        self.logger.debug(f'Receiver daemon received STOMP frame '
                                          f'{frame}')
                    self._queue_frames.put(frame)
                except Exception:
                    # TODO: Give some error here: logging, put garbage into queue
                    self.logger.error(f'Receiver daemon received non-STOMP frame: '
                                      f'"{frame_bytes}"')
                    raise
                if frame is not None:
                    for listener in self._listener:
                        listener.on_message(frame)
        self.logger.debug(f'Quitting WebSocket receiver thread.')
