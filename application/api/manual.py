from flask import Blueprint, current_app, request
from typing import TYPE_CHECKING, cast

from application.modules.climatechamber.manual_mode import manual_mode_class
from application.data.voetsch_data import connection
from application.api.api_response import ApiResponse

import json

manual = Blueprint('manual', __name__)
manual.url_prefix = '/manual'

@manual.route('/')
def index():

    return ApiResponse.success(message="manual")

@manual.route('/activate')
def activate():

    connection_data = cast('connection', current_app.config['CONNECT_DATA'])

    if connection_data.automatic_mode == True:

        return ApiResponse.error(message="Automatic Mode is active, stop automatic mode before use of manual mode", errors={'automatic':True}) 

    else:

        current_app.config['CONNECT_DATA'].manual = manual_mode_class()

        current_app.config['CONNECT_DATA'].manual_mode = True

        return ApiResponse.success(message="Manual Mode activated", data={'manual':True})
    
@manual.route('/deactivate')
def deactivate():

    current_app.config['CONNECT_DATA'].manual = None

    current_app.config['CONNECT_DATA'].manual_mode = False

    return ApiResponse.success(message="Manual Mode deactivated", data={'manual':False})

#/start?chamber=1
@manual.route('/start')
def start(chamber: str):

    chamber = request.args.get('chamber', '1')

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.start_man_mode(chamber_number=int(chamber))

    return ApiResponse.success(message="Chamber started", data={"chamber": True})

@manual.route('/stop')
def stop(chamber: str):

    chamber = request.args.get('chamber', '1')

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.stop_man_mode(chamber_number=int(chamber))

    return ApiResponse.success(message="Chamber stoped", data={"chamber": False})

@manual.route('/stop_gradient')
def stop_gradient(chamber: str):

    chamber = request.args.get('chamber', '1')

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.stop_gradient_mode(chamber_number=int(chamber))

    return ApiResponse.success(message="Gradient set to zero", data={"gradient": 0})

#/set_gradiant/humidity?setpoint=40&gradiant=5&chamber=1
@manual.route('/set_gradient/humidity')
def set_gradient_humidity(setpoint:str, gradiant:str, chamber: str):

    chamber = request.args.get('chamber', '1')
    setpoint = request.args.get('setpoint', '40')
    gradiant = request.args.get('gradiant', '5')

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_gradient_humidity(
        setpoint=float(setpoint), 
        gradient=float(gradiant),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Humidity set target {setpoint} with a gradiant of {gradiant}", data={"setpoint": setpoint, "gradiant": gradiant})

#/set_gradiant/temperature?setpoint=20&gradiant=5&chamber=1
@manual.route('/set_gradient/temperature')
def set_gradient_temperature(setpoint:str, gradiant:str, chamber: str ):

    chamber = request.args.get('chamber', '1')
    setpoint = request.args.get('setpoint', '20')
    gradiant = request.args.get('gradiant', '5')

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_gradient_temperature(
        setpoint=float(setpoint), 
        gradient=float(gradiant),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Temperature set target {setpoint} with a gradiant of {gradiant}", data={"setpoint": setpoint, "gradiant": gradiant})

#/setpoint/humidity?setpoint=40&chamber=1
@manual.route('/setpoint/humidity/')
def setpoint_humidity(setpoint:str, chamber: str):

    chamber = request.args.get('chamber', '1')
    setpoint = request.args.get('setpoint', '40')

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_setpoint_humidity(
        value=float(setpoint),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Humidity set target {setpoint}", data={"setpoint": setpoint})

#/setpoint/temperature?setpoint=20&chamber=1
@manual.route('/setpoint/temperature/')
def setpoint_temperature(setpoint:str, chamber: str):

    chamber = request.args.get('chamber', '1')
    setpoint = request.args.get('setpoint', '20')

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_setpoint_temperature(
        value=float(setpoint),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Temperature set target {setpoint}", data={"setpoint": setpoint})