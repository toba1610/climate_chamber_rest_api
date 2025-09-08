import json

from application.factory import create_app
# from application.data.data_structure import ConnectData
from application.data.voetsch_data import connection
from application.data.voetsch_data import defines
from application.modules.climatechamber import log_data
from application.modules.climatechamber.connection_handling import Connection_Class

from typing import TYPE_CHECKING, cast

app = create_app()

if TYPE_CHECKING:
    import socket

def define_standard_data():

    defines_data = defines(
        DELIM= b'\xb6',
        CR= b'\r',
        GOOD_COMMAND= b'1\r\n',
        BAD_COMMAND= b''
    )

    app.config['COMMAND_DATA'] = defines_data  
     

if __name__ == '__main__':

    with open('config.json', encoding='utf-8') as config:
        config_data = json.load(config)

    log_file_path = config_data['log_directory']
    logger_setup = log_data.LoggerSetup(name='server_logger', log_file_path=log_file_path, terminal=config_data['terminal_log'])
    logger = logger_setup.get_logger()

    app.config['LOGGER'] = logger

    define_standard_data()

    app.run()
