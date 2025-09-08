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