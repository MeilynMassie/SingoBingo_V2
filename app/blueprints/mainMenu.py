#OVERVIEW: Login page for user to create username, join lobby, and pick an avatar
from flask import Blueprint, jsonify, request
from app.services.db_lobby_service import (generateLobbyCode, db_create_lobby)
from app.services.game_service import GameState


mainMenu_bp = Blueprint('mainMenu', __name__)

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
    GameState.create_game(lobbyCode)
    print(GameState.get_game(lobbyCode).get_state())
    db_create_lobby(lobby_code=lobbyCode, player_mode=playerMode, playlist_mode=playlistMode)
    return jsonify({"ok": True,
                    "lobby_code": lobbyCode,
                    "player_mode": playerMode,
                    "playlist_mode": playlistMode
                    })

# TODO: Create a test route to bypass lobby and user creation
@mainMenu_bp.route('/db/testGame')
def test_game():
    lobbyCode = "TESTS"
    playerMode = "singleplayer"
    playlistMode = "classic"
    GameState.create_game(lobbyCode)
    print(GameState.get_game(lobbyCode).get_state())
    db_create_lobby(lobby_code=lobbyCode, player_mode=playerMode, playlist_mode=playlistMode)
    return jsonify({"ok": True,
                    "lobby_code": lobbyCode,
                    "player_mode": playerMode,
                    "playlist_mode": playlistMode
                    })