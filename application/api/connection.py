from flask import Blueprint, Response, current_app
from typing import TYPE_CHECKING, cast

from application.modules.climatechamber.connection_handling import Connection_Class
from application.data.voetsch_data import connection as con_data

import json


connection = Blueprint('connection', __name__)
connection.url_prefix = '/connection'

@connection.route('/')
def index():
    return Response(json.dumps("Connection"), mimetype="application/json")

@connection.route('/connect/<ip>:<port>')
def connect(ip:str, port:str):

    port_int = int(port)

    if  hasattr(current_app.config, 'CONNECT_DATA'):

        status = current_app.config['CONNECT_DATA'].status

        if status == False:

            voetsch = cast('Connection_Class', current_app.config['CONNECT_DATA'].client_socket)

            voetsch.connect_to_chamber(adress=ip,port=port_int)

            current_app.config['CONNECT_DATA'].status = True

            return Response(json.dumps(f"Connected  to {ip}:{port_int}"), mimetype="application/json")

        else:

            return Response(json.dumps("Connection already established"), mimetype="application/json")

    else:

        logger = current_app.config['LOGGER']
        defines = current_app.config['COMMAND_DATA']

        connect_data = con_data(
            client_socket=Connection_Class(logger=logger, defines_data=defines),
            status = False
        )

        connect_data.client_socket.connect_to_chamber(adress=ip,port=port_int)
        connect_data.status =True

        current_app.config['CONNECT_DATA'] = connect_data
        
        return Response(json.dumps(f"Connected  to {ip}:{port_int}"), mimetype="application/json")
    
@connection.route('/disconnect')
def disconnect():

    if  'CONNECT_DATA' in current_app.config:

        status = current_app.config['CONNECT_DATA'].status

        if status == True:

            voetsch = cast('Connection_Class', current_app.config['CONNECT_DATA'].client_socket)

            voetsch.close_connection()

            current_app.config['CONNECT_DATA'].status = False

            return Response(json.dumps("Connection closed"), mimetype="application/json")
        
        else:
            
            return Response(json.dumps("No connection to close"), mimetype="application/json")
        
    else:

        return Response(json.dumps("No connection to close"), mimetype="application/json")