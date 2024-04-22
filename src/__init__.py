from flask import Flask
from .database_manager import Database
from os import path

admin_pass = "password"

def start():
    app = Flask(__name__)
    app.secret_key = "siquirity"

    from .views import routes, initialize_login

    initialize_login(app)
    app.register_blueprint(routes, url_prefix="")

    return app
