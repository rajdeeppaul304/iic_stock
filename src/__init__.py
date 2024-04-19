from flask import Flask
from os import path
from .database_manager import Database

manager = Database("database.json")


def start():
    app = Flask(__name__)

    from .views import routes
    app.register_blueprint(routes, url_prefix="")

    return app
