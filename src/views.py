<<<<<<< HEAD
from flask import Blueprint, send_file, request, render_template, jsonify
from .database_manager import Database

routes = Blueprint("views", __name__)
name= "Rajdeep" #dhruv dekh lio kya karna hai, isko implement kardio
current_balance = 1000.10 #dhruv dekh lio kya karna hai, isko implement kardio
stocks = [
    "AAPL",  # Apple Inc.
    "TSLA",  # Tesla, Inc.
    "AMZN",  # Amazon.com, Inc.
    "GOOGL", # Alphabet Inc.
    "MSFT",  # Microsoft Corporation
    "FB",     # Facebook, Inc.
    "NVDA",  # NVIDIA Corporation
    "JNJ",    # Johnson & Johnson
    "PFE",    # Pfizer Inc.
    "KO",     # Coca-Cola Company
    "NFLX",  # Netflix, Inc.
    "DIS",    # Walt Disney Company
    "BAC",    # Bank of America Corporation
    "V",       # Visa Inc.
    "PG",     # Procter & Gamble Company
    "T",       # AT&T Inc.
    "BRK.B", # Berkshire Hathaway Inc.
    "GE",     # General Electric Company
    "XOM",   # Exxon Mobil Corporation
    "BABA"  # Alibaba Group Holding Limited
]
data = [
        {"email": "example1@gmail.com", "name": "John Doe"},
        {"email": "example2@gmail.com", "name": "Jane Smith"},
        {"email": "example3@gmail.com", "name": "Alice Johnson"}
        # Add more data as needed
    ]
=======
from flask import Blueprint, redirect, request, render_template, jsonify, url_for
from .database_manager import Database, User
from flask_login import LoginManager, login_manager, login_user, logout_user, current_user, login_required
from os import path

routes = Blueprint("views", __name__)

database_file = path.abspath("database.json")
stocks_file = path.abspath("stocks.json")

manager = Database(database_file, stocks_file)

login_manager = LoginManager()
login_manager.login_view = 'views.login'
def initialize_login(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = manager.get_users().get(user_id)
    if user_data:
        return User(user_id)

    return None

# name= "Rajdeep" #dhruv dekh lio kya karna hai, isko implement kardio
# current_balance = 1000.10 #dhruv dekh lio kya karna hai, isko implement kardio
# stocks = [
#     "AAPL",  # Apple Inc.
#     "TSLA",  # Tesla, Inc.
#     "AMZN",  # Amazon.com, Inc.
#     "GOOGL", # Alphabet Inc.
#     "MSFT",  # Microsoft Corporation
#     "FB",     # Facebook, Inc.
#     "NVDA",  # NVIDIA Corporation
#     "JNJ",    # Johnson & Johnson
#     "PFE",    # Pfizer Inc.
#     "KO",     # Coca-Cola Company
#     "NFLX",  # Netflix, Inc.
#     "DIS",    # Walt Disney Company
#     "BAC",    # Bank of America Corporation
#     "V",       # Visa Inc.
#     "PG",     # Procter & Gamble Company
#     "T",       # AT&T Inc.
#     "BRK.B", # Berkshire Hathaway Inc.
#     "GE",     # General Electric Company
#     "XOM",   # Exxon Mobil Corporation
#     "BABA"  # Alibaba Group Holding Limited
# ]
# data = [
#         {"email": "example1@gmail.com", "name": "John Doe"},
#         {"email": "example2@gmail.com", "name": "Jane Smith"},
#         {"email": "example3@gmail.com", "name": "Alice Johnson"}
#         # Add more data as needed
#     ]

user_id = "dhruvdubey32@gmail.com"
>>>>>>> e24d7e013ce3f766e126d1620ee4ae9c5b2bf904

manager = Database("database.json", "stocks.json")

@routes.route("/")
@login_required
def index():
    items = [f'Item {i + 1}' for i in range(20)]
<<<<<<< HEAD
    print(items)
    return render_template('index.html',title="IIC", items=stocks, current_balance=current_balance, name=name)
=======
    stock_names = [val['name'] for (key, val) in manager.get_stocks().items()]
    user_data = manager.get_users()[user_id]

    return render_template('index.html', items=stock_names, current_balance=user_data["balance"], name=user_data["name"])
>>>>>>> e24d7e013ce3f766e126d1620ee4ae9c5b2bf904

@routes.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_pass = manager.get_users(no_pass=False)[email]["password"]

        # print(f"email: {email}, password: {password}, user_pass: {user_pass}")
        
        if user_pass == password:
            login_user(User(email))
            print(f"{email} logged in")

            return redirect(url_for("views.index"))

    return render_template("login.html")

@routes.route("/about")
def about():
<<<<<<< HEAD
    return render_template("about.html", title="About Us")

@routes.route("/owned_stocks")
def owned_stocks():
    return render_template("owned_stocks.html",title="Owned Stocs", items=stocks, current_balance=current_balance, name=name)
=======
    return render_template("about.html")

@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login"))

# @routes.route("/owned_stocks")
# def owned_stocks():
#     return render_template("owned_stocks.html", items=stocks, current_balance=current_balance, name=name)
#

# @routes.route("/barter")
# def barter():
#     return render_template("barter.html", data=data)
>>>>>>> e24d7e013ce3f766e126d1620ee4ae9c5b2bf904

@routes.route("/test")
def test():
    return render_template("test.html", data=data)

