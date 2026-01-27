# OVERVIEW: All socketio related things
from app import socketio
from flask_socketio import emit

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    emit("connected", {"msg": "Hello client!"})
