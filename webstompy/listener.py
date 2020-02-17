"""StompListener: base class for a listener which will be invoked upon message
arrival
"""


class StompListener(object):
    """StompListener: base class for a listener which will be invoked upon message
    arrival
    """

    def on_message(self, frame):
        """Called by the STOMP receiver thread upon message arrival.

        Parameters
        ----------
        frame: webstompy.StompFrame
            The frame containing the headers and the message
        """
        pass
