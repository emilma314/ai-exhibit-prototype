from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app, cors_allowed_origins='*')

# ---------------- Exhibit 1 state ----------------
# (if Exhibit 1 also uses sockets, you may need its own state)
current_ex1 = {}
@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/exhibit1/control")
def exhibit1_control():
    return render_template("exhibit1/control1.html")

# @app.route("/exhibit1/display")
# def exhibit1_display():
#     return render_template("exhibit1/display1.html")
@app.route("/match/<difficulty>")
def match(difficulty):
    return render_template("exhibit1/match.html", difficulty=difficulty)

# ---------------- Exhibit 2 state ----------------
current_ex2 = {"prompt": None, "code": None}

@app.route("/exhibit2/control")
def exhibit2_control():
    return render_template("exhibit2/control2.html")   # your new control.html

@app.route("/exhibit2/display")
def exhibit2_display():
    return render_template("exhibit2/display2.html")   # your new display.html


# ---------------- Exhibit 2 sockets ----------------
@socketio.on("new_selection")
def handle_selection(data):
    # Update state for Exhibit 2
    current_ex2.update(data)
    emit("update_display", current_ex2, broadcast=True)

@socketio.on("request_latest")
def send_latest():
    emit("update_display", current_ex2)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)