from flask import Blueprint, Response, current_app
from typing import TYPE_CHECKING, cast

from application.modules.climatechamber.automatic_mode import automatic_mode_class
from application.data.voetsch_data import connection

import json

automatic = Blueprint('manual', __name__)
automatic.url_prefix = '/manual'

@automatic.route('/')
def index():

    return Response(json.dumps("manual"), mimetype="application/json")

@automatic.route('/activate')
def activate():

    connection_data = cast('connection', current_app.config['CONNECT_DATA'])

    if connection_data.manual_mode == True:

        return Response(json.dumps("Manual Mode is active, stop manual mode before use of automatic mode"), mimetype="application/json")

    else:

        current_app.config['CONNECT_DATA'].automatic = automatic_mode_class()

        current_app.config['CONNECT_DATA'].automatic_mode = True
        return Response(json.dumps("Automatic Mode activated"), mimetype="application/json")
    
@automatic.route('/deactivate')
def deactivate():

    current_app.config['CONNECT_DATA'].automatic = None

    current_app.config['CONNECT_DATA'].automatic_mode = False

    return Response(json.dumps("Automatic Mode deactivated"), mimetype="application/json")

@automatic.route('/start/<program>')
@automatic.route('/start/<program>/<chamber>')
@automatic.route('/start/<program>/<number_of_repetition>')
@automatic.route('/start/<program>/<chamber>/<number_of_repetition>')

def start_automatic(program: str, chamber: str = '1', number_of_repetions: str = '1'):

    voetsch = cast('automatic_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.start_programm(programm_number=int(program), number_of_repetition=int(number_of_repetions), chamber_number=int(chamber))

    return Response(json.dumps(f"Program {program} started for {number_of_repetions} repitions"), mimetype="application/json")
