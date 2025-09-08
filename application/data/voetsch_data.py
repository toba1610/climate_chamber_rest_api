from dataclasses import dataclass
from application.modules.climatechamber.connection_handling import Connection_Class
from application.modules.climatechamber.status import status_class
from typing import Optional    

@dataclass
class defines:

    DELIM:bytes
    CR:bytes
    GOOD_COMMAND:bytes
    BAD_COMMAND:bytes

@dataclass
class connection:

    client_socket: Connection_Class
    connection_status: bool
    status: Optional[status_class] = None
    