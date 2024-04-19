from flask import Flask
from os import path
from .database_manager import Database

manager = Database("database.json")
manager.add_user("rajdeep", "rajdeep@gmail.com", "password", 10000)

# siquirity
admin_pass = "password"

manager.buy_stocks("dhruvdubey32@gmail.com", 104, 10)
manager.dump_data()

def start():
    app = Flask(__name__)

    from .views import routes
    app.register_blueprint(routes, url_prefix="")

    return app
