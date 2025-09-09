from dataclasses import dataclass
from application.modules.climatechamber.connection_handling import Connection_Class
from application.modules.climatechamber.status import status_class
from application.modules.climatechamber.manual_mode import manual_mode_class
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
    manual_mode: bool
    automatic_mode: bool
    status: Optional[status_class] = None
    manual: Optional[manual_mode_class] = None
    