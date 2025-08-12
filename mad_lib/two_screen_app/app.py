from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app, cors_allowed_origins='*')

# Shared state – last selection made
current = {"prompt": None, "code": None}

@app.route("/")
def control():
    return render_template("control.html")

@app.route("/display")
def display():
    return render_template("display.html")

@socketio.on("new_selection")
def handle_selection(data):
    """
    data = {"prompt": "...", "code": "dfsp"}  # 4-letter file code
    """
    current.update(data)
    # Broadcast to every connected display page
    emit("update_display", current, broadcast=True)

@socketio.on("request_latest")
def send_latest():
    # Late-joining display window asks what the current state is
    emit("update_display", current)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
