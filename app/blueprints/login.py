#OVERVIEW: Login page for user to create username, join lobby, and pick an avatar
from faker import Faker
from flask import Blueprint, jsonify, request
from app.services.db import (
    db_add_user, 
    db_get_avatars, 
    db_add_user_avatar,
    db_get_all_active_lobbies
)

login_bp = Blueprint('login', __name__)

# Adds user in db
@login_bp.route('/db/createUser', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get("username")
    lobby_code = data.get("lobby_code")
    print(f"Creating user: {username}, Lobby Code: {lobby_code}")
    if not username or not lobby_code:
        return jsonify({"ok": False, "error": "Missing something"}), 400
    db_add_user(username, lobby_code)
    return jsonify({"ok": True})

# Adds selected avatar to user in db
@login_bp.route('/db/addAvatarSelected', methods=['POST'])
def add_avatar_selected():
    data = request.get_json()
    username = data.get("username")
    avatar_id = data.get("avatar_id")
    print(f"Avatar selected: {avatar_id}")
    if not username or not avatar_id:
        return jsonify({"ok": False, "error": "Missing username or avatar_id"}), 400
    db_add_user_avatar(username, avatar_id)
    return jsonify({"ok": True})  

# Retrieves available avatars from db
@login_bp.route('/db/GetAvatarImages')
def get_avatar_images():
    avatars = db_get_avatars()
    print(avatars)
    avatar_list = [{'id': avatar[0], 'filePath': 'static/imgs/avatars/'+avatar[1]} for avatar in avatars]
    return jsonify(avatar_list)

# Retrieves all active lobby codes
@login_bp.route('/db/getLobbyCode')
def get_lobby_code():
    lobbies = db_get_all_active_lobbies()
    listOfLobbies = [lobby[0] for lobby in lobbies]
    print(listOfLobbies)
    return jsonify(listOfLobbies)