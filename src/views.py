import re
from flask import Blueprint, redirect, request, render_template, jsonify, url_for
from .database_manager import Database, User
from flask_login import LoginManager, login_manager, login_user, logout_user, current_user, login_required
from os import path
from .barter import Barter
import json
routes = Blueprint("views", __name__)

database_file = path.abspath("database.json")
stocks_file = path.abspath("stocks.json")
active_trades = path.abspath("active_trades.json")

manager = Database(database_file, stocks_file)
barter_manager = Barter(active_trades, stocks_file)

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

manager = Database("database.json", "stocks.json")

@routes.route("/")
@login_required
def index():
    # stock_names = [val['name'] for (key, val) in manager.get_stocks().items()]
    # print(manager.get_stocks())
    user_data = manager.get_users()[current_user.id]

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

@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login"))

@routes.route('/buy_sell_stocks', methods=['POST'])
@login_required
def buy_sell_stocks():
    data = request.get_json()
    
    item_id = data['itemId']
    number_of_stocks = data['number_of_stocks']
    action = data['action']  

    if action == "buy":
        success_message = f"Stock purchased for {item_id} with {number_of_stocks} units."
        success = manager.buy_stocks(email=current_user.id, stock_id=int(item_id), amount=int(number_of_stocks))
    elif action == "sell":
        success_message = f"Stock sold for {item_id} with {number_of_stocks} units."
        success = manager.sell_stocks(email=current_user.id, stock_id=int(item_id), amount=int(number_of_stocks))
    else:
        return jsonify({"success": 0, "message": "Invalid action."})

    if success:
        return jsonify({
            "success": 1,
            "remaining_balance": manager.get_users()[current_user.id]["balance"],
            "message": success_message
        })
    else:
        return jsonify({
            "success": 0,
            "message": f"Error {action}ing {item_id} with {number_of_stocks} units."
        })



@routes.route("/owned_stocks")
@login_required
def owned_stocks():
    user_data = manager.get_users()[current_user.id]
    items=user_data["stocks"]
    stocks_data=manager.get_stocks()
    dict_to_return = {}
    for i,y in items.items():
        dict_to_return[i] = stocks_data[i]
        dict_to_return[i].update({"owned":y})

    return render_template("owned_stocks.html", stocks_data=dict_to_return, current_balance=user_data["balance"], name=user_data["name"])


@routes.route("/barter/start_trade", methods=['GET','POST'])
@login_required
def barter_start_trade():
    if request.method == "POST":
        barter_manager.start_trade(current_user.id, request.form)
        return jsonify(success=True, message="Trade started successfully")

    return render_template("tradebarter.html", stocks_data=manager.get_stocks(), current_user_stocks=current_user.data(manager).get("stocks"))

@routes.route("/barter", methods=['GET','POST'])
@login_required
def barter():
    if request.method == "POST":
        returned_request = request.get_json()
        confirmation = returned_request['confirmation']
        trade_status = [False, ""]

        if confirmation == "Yes":
            trade_status = barter_manager.confirm_trade(current_user.id, returned_request["trader"], manager)

        else:
            trade_status = barter_manager.deny_trade(current_user.id, returned_request["trader"])

        return jsonify({
            "success": trade_status[0],
            "message": trade_status[1]
        })

    current_active_trades = barter_manager.get_active_trades(current_user.id)
    stocks_data=manager.get_stocks()
    transformed_stocks = {key: value['name'] for key, value in stocks_data.items()}
    sent_trade = barter_manager.get_active_trades(current_user.id, current_user.id)
    return render_template("barter.html", stocks_data=stocks_data,transformed_stocks=transformed_stocks, current_active_trades=current_active_trades, current_user=current_user.id, sent_trade=sent_trade) 

@routes.route("/delete_current_trade_request", methods=['POST'])
@login_required
def delete_current_trade_request():
    deletionoftradewith = request.form['deletion-current-request']
    trade_status = barter_manager.deny_trade(deletionoftradewith, current_user.id)

    print(request.form['deletion-current-request'], trade_status)
    return redirect('/barter')
    


@routes.route("/ipo", methods=['GET','POST'])
@login_required
def ipo():
    user_data = manager.get_users()[current_user.id]
    return render_template("ipo.html", stocks_data=manager.get_stocks(only_ipos=True), current_balance=user_data["balance"], name=user_data["name"])




