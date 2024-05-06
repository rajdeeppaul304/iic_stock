from flask import Flask, render_template, request, jsonify
import database_manager
import fd_manager
import stocks_manager
import os

manager = database_manager.Database("database.json", "stocks.json", "round_match_info.json")
ipo_manager = fd_manager.Ipo("requested_lots.json", manager)
stocks_manager = stocks_manager.Stocks("stocks.json", manager)
# interest is in fraction
manager_fd = fd_manager.FD("fds.json", 0.06)
lock_file = os.path.abspath("transaction.lock")

for i in range(20):
    print(f"mail{i}@gmail.com")
    manager.add_user("your_name", f"mail{i}@gmail.com", "pass", 10_00_000)


def change_lock_state(file, new_state):
    if os.path.exists(file) and new_state:
        print("lock released")
        os.remove(file)

    elif not new_state:
        with open(file, "w") as file:
            print("locked")

def get_lock_state(file) -> bool:
    return not os.path.exists(file)

app = Flask(__name__, template_folder=os.path.abspath("admin/templates"))

@app.route("/", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        new_state = request.get_json().get('ServerStartStop')
        print(f"New server state: {new_state}")
        change_lock_state(lock_file, new_state)
        return jsonify({"success": True, "newState": new_state})

    return render_template("admin.html", server_state=get_lock_state(lock_file), stocks_data=manager.get_stocks(), users_data=manager.get_users())

@app.route("/stock_submit", methods=["POST"])
def stock_submit():
    data = request.get_json()
    print(data)
    manager.update_stocks(data["stock_id"], float(data["price"]))
    return jsonify({"message": "Form submitted successfully"})

# updation of round and match
@app.route("/get_current_values", methods=["GET"])
def get_current_values():
    return jsonify({"current_round": manager.round(), "current_match": manager.match()})

@app.route("/update_round_match", methods=["POST"])
def update_round_match():
    data = request.get_json()
    print(data)
    if data['id'] == 'increment-round':
        if manager.round() == 1:
            print("distributing lots")
            ipo_manager.distribute_lots()

        manager.round(increment=True)

    elif data['id'] == 'increment-match':
        manager_fd.increase_interest()
        stocks_manager.on_match_increment(manager.match())
        manager.match(increment=True)

    print(f"round: {manager.round()} match:{manager.match()}")
    return jsonify({"message": "Form submitted successfully", "current_round":manager.round(), "current_match":manager.match()})

@app.route("/update-user-balance", methods=["POST"])
def update_user_balance():
    data = request.get_json()
    email = data.get('email')
    number = data.get('add_balance')

    print(f"Gmail: {email}, Input Value: {number}")
    # You can perform any further processing here
    
    manager.add_balance(email, int(number))

    return jsonify({"message": "Form submitted successfully!", "email": email, "add_balance": number})

app.run(debug=True, port=5000)
