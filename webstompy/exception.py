"""webstompy exceptions
"""


class WebstompyException(Exception):
    """
    Common exception class. All specific webstompy exceptions are subclasses
    of WebstompyException, allowing the library user to catch all current and
    future library exceptions.
    """


class ConnectFailedException(WebstompyException):
    """
    Raised by StompConnection.connect when no connection could be established.
    """

    def __init__(self, message):
        self.message = message


class ConnectionClosedException(WebstompyException):
    """
    Raised when no connection was closed.
    """

    def __init__(self, message):
        self.message = message


class NoDestinationException(WebstompyException):
    """
    Raised when no STOMP destination was specified where it was required.
    """

    def __init__(self):
        self.message = "No destination specified!"


class NoIdException(WebstompyException):
    """
    Raised when no STOMP id was specified where it was required.
    """

    def __init__(self):
        self.message = "No id specified!"
