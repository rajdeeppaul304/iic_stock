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

user_id = "dhruvdubey32@gmail.com"

manager = Database("database.json", "stocks.json")

@routes.route("/")
@login_required
def index():
    # stock_names = [val['name'] for (key, val) in manager.get_stocks().items()]
    # print(manager.get_stocks())
    user_data = manager.get_users()[user_id]

    return render_template('index.html', stocks_data=manager.get_stocks(), current_balance=user_data["balance"], name=user_data["name"])

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
    return render_template("about.html")


@routes.route('/buy_sell_stocks', methods=['POST'])
@login_required
def buy_sell_stocks():
    data = request.get_json()
    
    item_id = data['itemId']
    number_of_stocks = data['number_of_stocks']
    action = data['action']  

    if action == "buy":
        success_message = f"Stock purchased for {item_id} with {number_of_stocks} units."
        success = manager.buy_stocks(email=user_id, stock_id=int(item_id), amount=int(number_of_stocks))
    elif action == "sell":
        success_message = f"Stock sold for {item_id} with {number_of_stocks} units."
        success = manager.sell_stocks(email=user_id, stock_id=int(item_id), amount=int(number_of_stocks))
    else:
        return jsonify({"success": 0, "message": "Invalid action."})

    if success:
        return jsonify({
            "success": 1,
            "remaining_balance": manager.get_users()[user_id]["balance"],
            "message": success_message
        })
    else:
        return jsonify({
            "success": 0,
            "message": f"Error {action}ing {item_id} with {number_of_stocks} units."
        })



@routes.route("/owned_stocks")
def owned_stocks():
    user_data = manager.get_users()[user_id]
    items=user_data["stocks"]
    stocks_data=manager.get_stocks()
    dict_to_return = {}
    for i,y in items.items():
        dict_to_return[i] = stocks_data[i]
        dict_to_return[i].update({"owned":y})

    return render_template("owned_stocks.html", stocks_data=dict_to_return, current_balance=user_data["balance"], name=user_data["name"])


# @routes.route("/barter")
# def barter():
#     return render_template("barter.html")

@routes.route("/test")
def test():
    return render_template("test.html")

