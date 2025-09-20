from dataclasses import dataclass
from application.modules.climatechamber.connection_handling import ConnectionClass
from application.modules.climatechamber.status import StatusClass
from application.modules.climatechamber.manual_mode import ManualModeClass
from application.modules.climatechamber.automatic_mode import AutomaticModeClass
from typing import Optional    

@dataclass
class defines:

    DELIM:bytes
    CR:bytes
    GOOD_COMMAND:bytes
    BAD_COMMAND:bytes

@dataclass
class connection:

    client_socket: ConnectionClass
    connection_status: bool
    manual_mode: bool
    automatic_mode: bool
    status: Optional[StatusClass] = None
    manual: Optional[ManualModeClass] = None
    automatic: Optional[AutomaticModeClass] = None
    