from flask import Flask
from application.api.connection import connection
from application.api.get_status import get_status
from application.api.manual import manual
from application.api.automatic import automatic


def create_app():
    app = Flask(__name__)
    app.register_blueprint(connection, url_prefix=connection.url_prefix)
    app.register_blueprint(get_status, url_prefix=get_status.url_prefix)
    app.register_blueprint(manual, url_prefix=manual.url_prefix)
    app.register_blueprint(automatic, url_preset=automatic)

    return app
