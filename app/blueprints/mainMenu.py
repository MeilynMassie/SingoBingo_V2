#OVERVIEW: Login page for user to create username, join lobby, and pick an avatar
from faker import Faker
from flask import Blueprint, jsonify, request
from app.services.db import (
    db_create_lobby
)

mainMenu_bp = Blueprint('mainMenu', __name__)

def generateLobbyCode():
    faker = Faker()
    lobby_code = faker.bothify(text='?????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    print(f'Generated Lobby Code: {lobby_code}')
    return lobby_code


# Create lobby in db
@mainMenu_bp.route('/db/createLobby', methods=['POST'])
def create_lobby():
    data = request.get_json()
    playerMode = data.get("player_mode")
    playlistMode = data.get("playlist_mode")
    lobbyCode = generateLobbyCode()
    print(f"Creating lobby: {lobbyCode}, Playlist Mode: {playlistMode}, Player Mode {playerMode}")
    if not lobbyCode or not playlistMode or not playerMode:
        return jsonify({"ok": False, "error": "Missing something"}), 400
    db_create_lobby(lobbyCode, playerMode, playlistMode)
    return jsonify({"ok": True,
                    "lobby_code": lobbyCode,
                    "player_mode": playerMode,
                    "playlist_mode": playlistMode
                    })