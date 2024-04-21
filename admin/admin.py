from flask import Flask, render_template, request, jsonify
import os

lock_file = os.path.abspath("transaction.lock")

def change_lock_state(file, new_state):
    if os.path.exists(file) and new_state:
        print("lock released")
        os.remove(file)

    elif not new_state:
        with open(file, "w") as file:
            print("locked")

app = Flask(__name__, template_folder=os.path.abspath("admin/template"))

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        new_state = request.json.get('ServerStartStop')
        print(f"New server state: {new_state}")
        change_lock_state(lock_file, new_state)
        return jsonify({"success": True, "newState": new_state})

    return render_template("admin.html")

# add render_template
@app.route("/update-user-balance", methods=['GET', 'POST'])
def update_user_balance():
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        print(f"Gmail: {email}, Input Value: {number}")
        # You can perform any further processing here
        return jsonify({"message": "Form submitted successfully!", "email": email, "number": number})

    return "Hello, please submit the form."

app.run(debug=True)
