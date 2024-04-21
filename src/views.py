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

manager = Database("database.json", "stocks.json")

@routes.route("/")
def index():
    items = [f'Item {i + 1}' for i in range(20)]
    print(items)
    return render_template('index.html',title="IIC", items=stocks, current_balance=current_balance, name=name)

@routes.route("/login")
def login():
    return render_template("login.html")

@routes.route("/about")
def about():
    return render_template("about.html", title="About Us")

@routes.route("/owned_stocks")
def owned_stocks():
    return render_template("owned_stocks.html",title="Owned Stocs", items=stocks, current_balance=current_balance, name=name)

@routes.route("/test")
def test():
    return render_template("test.html", data=data)

@routes.route("/admin")
def admin():
    return render_template("admin.html", data=data)

@routes.route("/barter")
def barter():
    return render_template("barter.html",title="Barter - Round 2", data=data)

# your-backend-endpoint
@routes.route("/update-user-balance", methods=['GET', 'POST'])
def update_user_balance():
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        print(f"Gmail: {email}, Input Value: {number}")
        # You can perform any further processing here
        return jsonify({"message": "Form submitted successfully!", "email": email, "number": number})
    return "Hello, please submit the form."
