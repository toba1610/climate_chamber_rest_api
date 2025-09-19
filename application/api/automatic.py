from flask import Blueprint, Response, current_app, request
from typing import TYPE_CHECKING, cast

from application.modules.climatechamber.automatic_mode import automatic_mode_class
from application.data.voetsch_data import connection

import json

automatic = Blueprint('automatic', __name__)
automatic.url_prefix = '/automatic'

@automatic.route('/')
def index():

    return Response(json.dumps("automatic"), mimetype="application/json")

@automatic.route('/activate', methods=['PUT'])
def activate():

    connection_data = cast('connection', current_app.config['CONNECT_DATA'])

    if connection_data.manual_mode == True:

        return Response(json.dumps("Manual Mode is active, stop manual mode before use of automatic mode"), mimetype="application/json")

    else:

        current_app.config['CONNECT_DATA'].automatic = automatic_mode_class()

        current_app.config['CONNECT_DATA'].automatic_mode = True
        return Response(json.dumps("Automatic Mode activated"), mimetype="application/json")
    
@automatic.route('/deactivate', methods=['PUT'])
def deactivate():

    current_app.config['CONNECT_DATA'].automatic = None

    current_app.config['CONNECT_DATA'].automatic_mode = False

    return Response(json.dumps("Automatic Mode deactivated"), mimetype="application/json")

#/start?test_program=1&chamber=2&number_of_repetitions=5
@automatic.route('/start', methods=['PUT'])
def start_automatic():
    program = request.args.get('program', '1')
    chamber = request.args.get('chamber', '1')
    number_of_repetition = request.args.get('number_of_repetitions', '1')

    voetsch = cast('automatic_mode_class', current_app.config['CONNECT_DATA'].automatic) 
    voetsch.start_program(program_number=int(program), number_of_repetition=int(number_of_repetition), chamber_number=int(chamber))

    return Response(json.dumps(f"Program {program} started for {number_of_repetition} repitions"), mimetype="application/json")

#/start/pause?chamber=2
@automatic.route('start/pause', methods=['PUT'])
def pause_automatic():
    chamber = request.args.get('chamber', '1')

    voetsch = cast('automatic_mode_class', current_app.config['CONNECT_DATA'].automatic) 
    voetsch.pause_program(chamber_number=int(chamber))

    return Response(json.dumps(f"Program paused"), mimetype="application/json")

#/start/resume?chamber=2
@automatic.route('start/resume', methods=['PUT'])
def resume_automatic():
    chamber = request.args.get('chamber', '1')

    voetsch = cast('automatic_mode_class', current_app.config['CONNECT_DATA'].automatic) 
    voetsch.resume_program(chamber_number=int(chamber))

    return Response(json.dumps(f"Program resumed"), mimetype="application/json")

#/start/change_repetition?chamber=2&repetition=10
@automatic.route('start/change_repetition', methods=['PUT'])
def change_repetition():
    chamber = request.args.get('chamber', '1')
    repetition = request.args.get('repetition', '1')
    
    voetsch = cast('automatic_mode_class', current_app.config['CONNECT_DATA'].automatic) 
    voetsch.change_number_of_repetition(chamber_number=int(chamber), number_of_repitition=int(repetition))

    return Response(json.dumps(f"Program repetition changed to {repetition}"), mimetype="application/json")

#?program=1&year=2025&month=9&day=11&hour=14&minute=30&second=45
@automatic.route('start/at_date/', methods=['PUT'])
def start_at_date():
    chamber = request.args.get('chamber', '1')
    program = request.args.get('programm', '1')
    year = int(request.args.get('year',0))
    month = int(request.args.get('month',0))
    day = int(request.args.get('day',0))
    hour = int(request.args.get('hour',0))
    minute = int(request.args.get('minute',0))
    second = int(request.args.get('second',0))

    connection = cast('connection', current_app.config['CONNECT_DATA'].client_socket)
    date_string = connection.client_socket.formater.format_date_string(
                                                                    year=year,
                                                                    month=month,
                                                                    day= day,
                                                                    hour= hour,
                                                                    minute=minute,
                                                                    second=second
                                                                    )
    
    voetsch = cast('automatic_mode_class', current_app.config['CONNECT_DATA'].automatic)
    voetsch.set_program(int(program))
    voetsch.start_program_at_given_date(date= date_string, chamber_number=int(chamber))
    
    return Response(json.dumps(f"Program: {program} will start at {date_string}"), mimetype="application/json")

#?program=1&time=10&chamber=1
@automatic.route('start/after', methods=['PUT'])
def start_after():
    chamber = request.args.get('chamber', '1')
    program = request.args.get('program', '1')
    time = request.args.get('time', '100')

    voetsch = cast('automatic_mode_class', current_app.config['CONNECT_DATA'].automatic)
    voetsch.set_program(int(program))
    voetsch.start_program_after_give_time(time=int(time), chamber_number=int(chamber))

    return Response(json.dumps(f"Program: {program} will start in {time} seconds"), mimetype="application/json")


