from flask import Blueprint, Response, current_app
from typing import TYPE_CHECKING, cast

from application.modules.climatechamber.manual_mode import manual_mode_class
from application.data.voetsch_data import connection

import json

manual = Blueprint('manual', __name__)
manual.url_prefix = '/manual'

@manual.route('/')
def index():

    return Response(json.dumps("manual"), mimetype="application/json")

@manual.route('/activate')
def activate():

    connection_data = cast('connection', current_app.config['CONNECT_DATA'])

    if connection_data.automatic_mode == True:

        return Response(json.dumps("Automatic Mode is active, stop automatic mode before use of manual mode"), mimetype="application/json")

    else:

        current_app.config['CONNECT_DATA'].manual = manual_mode_class()

        current_app.config['CONNECT_DATA'].manual_mode = True
        return Response(json.dumps("Manual Mode activated"), mimetype="application/json")
    
@manual.route('/deactivate')
def deactivate():

    current_app.config['CONNECT_DATA'].manual = None

    current_app.config['CONNECT_DATA'].manual_mode = False

    return Response(json.dumps("Manual Mode deactivated"), mimetype="application/json")

@manual.route('/start')
def start():

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.start_man_mode()
    #b'14001\xb61\xb61\xb61\xb61\r'
    #b'14001\xb61\xb61\xb61\xb60\r'

    return Response(json.dumps("Chamber started"), mimetype="application/json")

@manual.route('/stop')
def stop():

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.stop_man_mode()
    #b'14001\xb61\xb61\xb61\xb60\r' TODO Das stoppen funktioniert nicht

    return Response(json.dumps("Chamber stoped"), mimetype="application/json")