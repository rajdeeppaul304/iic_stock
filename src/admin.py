from flask import Flask, render_template

app = Flask(__name__)

@app.route("/admin")
def admin():
    return render_template("")

app.run(debug=True)
