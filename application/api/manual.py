from flask import Blueprint, current_app
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

@manual.route('/start')
@manual.route('/start/<chamber>')
def start(chamber: str = '1'):

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.start_man_mode(chamber_number=int(chamber))

    return ApiResponse.success(message="Chamber started", data={"chamber": True})

@manual.route('/stop')
@manual.route('/stop/<chamber>')
def stop(chamber: str = '1'):

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.stop_man_mode(chamber_number=int(chamber))

    return ApiResponse.success(message="Chamber stoped", data={"chamber": False})

@manual.route('/stop_gradient')
@manual.route('/stop_gradient/<chamber>')
def stop_gradient(chamber: str = '1'):

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.stop_gradient_mode(chamber_number=int(chamber))

    return ApiResponse.success(message="Gradient set to zero", data={"gradient": 0})

@manual.route('/set_gradient/humidity/<setpoint>/<gradiant>')
@manual.route('/set_gradient/humidity/<setpoint>/<gradiant>/<chamber>')
def set_gradient_humidity(setpoint:str, gradiant:str, chamber: str = '1'):

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_gradient_humidity(
        setpoint=float(setpoint), 
        gradient=float(gradiant),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Humidity set target {setpoint} with a gradiant of {gradiant}", data={"setpoint": setpoint, "gradiant": gradiant})

@manual.route('/set_gradient/temperature/<setpoint>/<gradiant>')
@manual.route('/set_gradient/temperature/<setpoint>/<gradiant>/<chamber>')
def set_gradient_temperature(setpoint:str, gradiant:str, chamber: str = '1'):

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_gradient_temperature(
        setpoint=float(setpoint), 
        gradient=float(gradiant),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Temperature set target {setpoint} with a gradiant of {gradiant}", data={"setpoint": setpoint, "gradiant": gradiant})

@manual.route('/setpoint/humidity/<setpoint>/')
@manual.route('/setpoint/humidity/<setpoint>/<chamber>')
def setpoint_humidity(setpoint:str, chamber: str = '1'):

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_setpoint_humidity(
        value=float(setpoint),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Humidity set target {setpoint}", data={"setpoint": setpoint})

@manual.route('/setpoint/temperature/<setpoint>/')
@manual.route('/setpoint/temperature/<setpoint>/<chamber>')
def setpoint_temperature(setpoint:str, chamber: str = '1'):

    voetsch = cast('manual_mode_class', current_app.config['CONNECT_DATA'].manual) 
    voetsch.set_setpoint_temperature(
        value=float(setpoint),
        chamber_number=int(chamber))

    return ApiResponse.success(message=f"Temperature set target {setpoint}", data={"setpoint": setpoint})