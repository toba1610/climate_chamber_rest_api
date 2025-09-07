from flask import Blueprint, Response, current_app
from typing import TYPE_CHECKING, cast

import json


connection = Blueprint('XXXXXXXXXXX', __name__)
connection.url_prefix = '/XXXXXXXXXXX'

@connection.route('/')
def index():
    return Response(json.dumps("XXXXXXXXXXX"), mimetype="application/json")