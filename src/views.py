from flask import Blueprint, send_file, request

routes = Blueprint("views", __name__)


@routes.route("/")
def index():
    return "I hate my life"
