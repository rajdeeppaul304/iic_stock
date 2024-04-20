from flask import Blueprint, send_file, request, render_template, jsonify

routes = Blueprint("views", __name__)
ServerStartStop = False #dhruv dekh lio kya karna hai, isko implement kardio
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

@routes.route("/")
def index():
    items = [f'Item {i + 1}' for i in range(20)]
    print(items)
    return render_template('index.html', items=stocks, current_balance=current_balance, name=name)

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
