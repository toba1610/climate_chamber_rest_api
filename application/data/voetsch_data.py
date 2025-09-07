from dataclasses import dataclass
from application.modules.climatechamber.connection_handling import Connection_Class
    

@dataclass
class defines:

    DELIM:bytes
    CR:bytes
    GOOD_COMMAND:bytes
    BAD_COMMAND:bytes

@dataclass
class connection:

    client_socket: Connection_Class