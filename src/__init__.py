from flask import Flask
from os import path
from .database_manager import Database

manager = Database("database.json", "stocks.json")
manager.add_user("rajdeep", "rajdeep@gmail.com", "password", 10000)

# siquirity
admin_pass = "password"

print("brrr", manager.buy_stocks("dhruvdubey32@gmail.com", 1001, 5))
manager.dump_data()

def start():
    app = Flask(__name__)

    from .views import routes
    app.register_blueprint(routes, url_prefix="")

    return app
