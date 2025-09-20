from flask import Blueprint, request, current_app
from typing import TYPE_CHECKING, cast

from application.modules.climatechamber.status import status_class
from application.api.api_response import ApiResponse

import json

get_status = Blueprint('get_status', __name__)
get_status.url_prefix = '/get_status'

@get_status.route('/')
def index():

    return ApiResponse.success(message="get_status")

@get_status.route('/chamber')
def chamber():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_status()

    return ApiResponse.success(message="Chamber status", data={"status": result})

@get_status.route('/program')
def program():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_program_status()

    return ApiResponse.success(message="Program status", data={"status": result})

@get_status.route('/loops')
def loops():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_actual_loops()

    return ApiResponse.success(message="Loops passed", data={"loops_passed": result})

@get_status.route('/time')
def time():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_program_active_time()

    return ApiResponse.success(message="Program runtime", data={"runtime": result})

@get_status.route('/number')
def number():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_program_number()

    return ApiResponse.success(message="Active program number", data={"program_number": result})

@get_status.route('/reset')
def reset():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.reset_errors()

    return ApiResponse.success(message="Error reset", data={"reset": result})

@get_status.route('/number_of_messages')
def number_of_messages():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_number_of_messages()

    return ApiResponse.success(message="Total number of messages defiened", data={"total_messages": result})

#/status_of_message?number=1
@get_status.route('/status_of_message/<number>')
def status_of_message(number:str):

    number = request.args.get('number', '1')

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_status_of_message(number_of_message=number)

    return ApiResponse.success(message=f"Message {number} status", data={"status": result})

#/status_of_message?number=1
@get_status.route('/message_text/<number>')
def message_text(number:str):

    number = request.args.get('number', '1')

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_message_text(number_of_message=number)

    return ApiResponse.success(message=f"Message {number} text", data={"text": result})

@get_status.route('/message_list')
def message_list():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_list_of_message_text()

    return ApiResponse.success(message="All active messages", data={"messages": result})

@get_status.route('/actual_temperature')
def actual_temperature():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_actual_temperature()

    return ApiResponse.success(message="Actual Temperature", data={"temperature": result})

@get_status.route('/actual_humidity')
def actual_humidity():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_actual_temperature()

    return ApiResponse.success(message="Actual Humidity", data={"humidity": result})

@get_status.route('/list_of_values')
def list_of_values():

    chamber_status = cast('status_class', current_app.config['CONNECT_DATA'].status)

    result = chamber_status.get_available_control_values()

    return ApiResponse.success(message="List of available control values", data={"values": result})