from dataclasses import dataclass


@dataclass
class ConnectData:
    
    serial: str
    status: bool