from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import socket

@dataclass
class defines:

    DELIM:bytes
    CR:bytes
    GOOD_COMMAND:bytes
    BAD_COMMAND:bytes

@dataclass
class connection:

    client_socket: socket.socket