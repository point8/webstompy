"""StompFrame: a STOMP data frame
"""

import json


class StompFrame(object):
    """StompFrame: a STOMP data frame

    A StompFrame can either be constructed from command, header, and message.
    Or from the complete byte payload of e.g. a server response.

    Parameters
    ----------
    command: str
        The command of this STOMP frame.
    header: list
        The headers of this STOMP frame as list of key, value tuples (string).
    message: str
        The message of this STOMP frame.
    payload: bytes
        The complete byte payload of this STOMP frame.
    """

    def __init__(self, command=None, header=None, message=None, payload=None):
        # TODO: Add __str__ and __repr__ members
        if command is not None:
            self._command = command.encode("UTF-8")
        else:
            self._command = None
        if header is not None:
            self._header = [
                (entry[0].encode("UTF-8"), entry[1].encode("UTF-8"))
                for entry in header
            ]
        else:
            self._header = None
        if message is not None:
            self._message = message.encode("UTF-8")
        else:
            self._message = None
        if payload is not None:
            lines = payload.splitlines()
            self._command = lines[0]
            self._header = [
                tuple(entry.split(b":"))
                for entry in lines[1 : lines.index(b"")]
            ]
            self._message = b"\n".join(lines[lines.index(b"") + 1 :])[:-1]

    def __repr__(self):
        s_headers = [
            option[0].decode("utf-8") + ":" + option[1].decode("utf-8")
            for option in self._header
        ].__repr__()
        s_repr = (
            f'<StompFrame: command="{self._command.decode("utf-8")}", '
            f'headers="{s_headers}", '
            f'message="{self._message}">'
        )
        return s_repr

    @property
    def command(self):
        """The command of this STOMP frame.
        """
        return self._command

    @property
    def header(self):
        """The headers of this STOMP frame as list of key, value tuples
        """
        return self._header

    @property
    def message(self):
        """The message of this STOMP frame.
        """
        return self._message

    @property
    def json(self):
        """The message of this STOMP frame as JSON data
        """
        return json.loads(self.message)

    @property
    def payload(self):
        """The complete byte payload of this STOMP frame.
        """
        payload = [
            self._command,
            b"\n".join([entry[0] + b":" + entry[1] for entry in self._header]),
            b"",
        ]
        if self._message is not None:
            payload.append(self._message)
        payload_str = b"\n".join(payload)
        # payload_str.encode('UTF-8')
        payload_str += b"\n\0"
        return payload_str
