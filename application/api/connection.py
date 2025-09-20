from flask import Blueprint, request, current_app
from typing import TYPE_CHECKING, cast

from application.modules.climatechamber.connection_handling import Connection_Class
from application.data.voetsch_data import connection as con_data
from application.modules.climatechamber.status import status_class
from application.api.api_response import ApiResponse

import json


connection = Blueprint('connection', __name__)
connection.url_prefix = '/connection'

@connection.route('/')
def index():
    
    return ApiResponse.success(message="Connection")

def connect(ip:str, port:str):

    port_int = int(port)

    if  hasattr(current_app.config, 'CONNECT_DATA'):

        status = current_app.config['CONNECT_DATA'].connection_status

        if status == False:

            voetsch = cast('Connection_Class', current_app.config['CONNECT_DATA'].client_socket)

            voetsch.connect_to_chamber(adress=ip,port=port_int)

            current_app.config['CONNECT_DATA'].status = True

            return ApiResponse.success(message=f"Connected  to {ip}:{port_int}", data={'IP':ip, 'Port': port_int})

        else:

            return ApiResponse.error(message="Connection already established")

    else:

        logger = current_app.config['LOGGER']
        defines = current_app.config['COMMAND_DATA']

        connect_data = con_data(
            client_socket=Connection_Class(logger=logger, defines_data=defines),
            connection_status= False,
            manual_mode= False,
            automatic_mode= False,
            status=None,
            manual=None
        )

        connect_data.client_socket.connect_to_chamber(adress=ip,port=port_int)
        connect_data.connection_status =True

        current_app.config['CONNECT_DATA'] = connect_data

        current_app.config['CONNECT_DATA'].status = status_class()
        
        return ApiResponse.success(message=f"Connected  to {ip}:{port_int}", data={'IP':ip, 'Port': port_int})
    
@connection.route('/disconnect')
def disconnect():

    if  'CONNECT_DATA' in current_app.config:

        status = current_app.config['CONNECT_DATA'].connection_status

        if status == True:

            voetsch = cast('Connection_Class', current_app.config['CONNECT_DATA'].client_socket)

            voetsch.close_connection()

            current_app.config['CONNECT_DATA'].connection_status = False

            return ApiResponse.success(message="Connection closed")
        
        else:
            
            return ApiResponse.error(message="No connection to close")

    else:

        return ApiResponse.error(message="No connection to close")