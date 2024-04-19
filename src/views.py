from flask import Blueprint, send_file, request, render_template

routes = Blueprint("views", __name__)


@routes.route("/")
def index():
    return render_template("index.html")

@routes.route("/login")
def login():
    return render_template("login.html")

@routes.route("/admin")
def admin():
    return render_template("admin.html")
