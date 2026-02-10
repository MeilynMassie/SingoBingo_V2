#OVERVIEW: Login page for user to create username, join lobby, and pick an avatar
from flask import Blueprint, jsonify, request
from app.services.db_player_service import (
    db_add_player, 
    db_get_avatars,
    db_assign_avatar_to_player,
    db_mark_avatar_taken
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
    db_add_player(username=username, lobby_code=lobby_code)
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
    db_assign_avatar_to_player(username=username, avatar_id=avatar_id)
    db_mark_avatar_taken(avatar_id=avatar_id)
    return jsonify({"ok": True})  

# Retrieves available avatars from db
@login_bp.route('/db/GetAvatarImages')
def get_avatar_images():
    avatar_list = db_get_avatars()
    print(avatar_list)
    return jsonify(avatar_list)