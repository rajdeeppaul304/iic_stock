from flask import Blueprint, send_file, request, render_template, jsonify

routes = Blueprint("views", __name__)
ServerStartStop = False #dhruv dekh lio kya karna hai, isko implement kardio
name= "Rajdeep" #dhruv dekh lio kya karna hai, isko implement kardio
current_balance = 1000.10 #dhruv dekh lio kya karna hai, isko implement kardio


@routes.route("/")
def index():
    items = [f'Item {i + 1}' for i in range(20)]
    return render_template('index.html', items=items, current_balance=current_balance, name=name)

    # return render_template("index.html")

@routes.route("/login")
def login():
    return render_template("login.html")

@routes.route("/admin")
def admin():
    return render_template("admin.html", ServerStartStop=ServerStartStop)

@routes.route('/update-server', methods=['POST'])
def update_server():
    new_state = request.json.get('ServerStartStop')
    print(f"New server state: {new_state}")
    return jsonify({"success": True, "newState": new_state})
