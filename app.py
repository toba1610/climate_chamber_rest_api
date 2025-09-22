import json
import os
from dotenv import load_dotenv, dotenv_values 

from application.factory import create_app
from application.data.voetsch_data import defines
from application.modules.climatechamber import log_data
from application.modules.user_handling import LoginHandling

app = create_app()

def define_standard_data():

    load_dotenv() 

    defines_data = defines(
        DELIM= b'\xb6',
        CR= b'\r',
        GOOD_COMMAND= b'1\r\n',
        BAD_COMMAND= b''
    )

    app.config['LOGIN_HANDLER'] = LoginHandling()
    app.config['COMMAND_DATA'] = defines_data
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', './application/data/udb.db')
    app.config['ALLOWED_TOKEN'] = {}

if __name__ == '__main__':

    with open('config.json', encoding='utf-8') as config:
        config_data = json.load(config)

    log_file_path = config_data['log_directory']
    logger_setup = log_data.LoggerSetup(name='server_logger', log_file_path=log_file_path, terminal=config_data['terminal_log'])
    logger = logger_setup.get_logger()

    app.config['LOGGER'] = logger

    define_standard_data()

    app.run()
