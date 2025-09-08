from flask import Flask
from application.api.connection import connection
# from application.api.control_DO import control_do
# from application.api.control_DI import control_di
# from application.api.control_DC_Aux import control_aux
# from application.api.sun import sun


def create_app():
    app = Flask(__name__)
    app.register_blueprint(connection, url_prefix=connection.url_prefix)
    # app.register_blueprint(control_do, url_prefix=control_do.url_prefix)
    # app.register_blueprint(control_di, url_prefix=control_di.url_prefix)
    # app.register_blueprint(control_aux, url_prefix=control_aux.url_prefix)

    return app
