from flask import Blueprint, Response, current_app
from typing import TYPE_CHECKING, cast

# from application.modules.climatechamber.connection_handling import Connection_Class
from application.modules.climatechamber.status import status_class
# from application.data.voetsch_data import connection as con_data

import json

get_status = Blueprint('get_status', __name__)
get_status.url_prefix = '/get_status'

@get_status.route('/')
def index():

    return Response(json.dumps("get_status"), mimetype="application/json")

@get_status.route('/chamber')
def chamber():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_status()

    return Response(json.dumps({'Chamber status': result}), mimetype="application/json")

@get_status.route('/program')
def program():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_program_status()

    return Response(json.dumps({'Program status': result}), mimetype="application/json")

@get_status.route('/loops')
def loops():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_actual_loops()

    return Response(json.dumps({'Loops passed': result}), mimetype="application/json")

@get_status.route('/time')
def time():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_program_active_time()

    return Response(json.dumps({'Program runtime [s]': result}), mimetype="application/json")

@get_status.route('/number')
def number():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_program_number()

    return Response(json.dumps({'Active program number': result}), mimetype="application/json")

@get_status.route('/reset')
def reset():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.reset_errors()

    return Response(json.dumps({'Error reset': result}), mimetype="application/json")

@get_status.route('/number_of_messages')
def number_of_messages():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_number_of_messages()

    return Response(json.dumps({'Total number of messages defiened': result}), mimetype="application/json")

@get_status.route('/status_of_message/<number>')
def status_of_message(number:str):

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_status_of_message(number_of_message=number)

    return Response(json.dumps({f'Message {number} status': result}), mimetype="application/json")

@get_status.route('/message_text/<number>')
def message_text(number:str):

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_message_text(number_of_message=number)

    return Response(json.dumps({f'Message {number} test': result}), mimetype="application/json")

@get_status.route('/message_list')
def message_list():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_list_of_message_text()

    return Response(json.dumps({'All active messages': result}), mimetype="application/json")