#OVERVIEW: Login page for user to create username, join lobby, and pick an avatar
from pathlib import Path
from flask import Blueprint, render_template, jsonify, request
from app.services.db import db_add_user, db_get_avatars, db_add_user_avatar
from app.blueprints.welcome import generateLobbyCode

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
@login_bp.route('/login')
def login():
    return render_template('login.html', lobby_code=generateLobbyCode())

@login_bp.route('/db/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get("username")
    lobbyCode = data.get("lobby_code")
    print(f"Creating user: {username}, Lobby Code: {lobbyCode}")
    if not username or not lobbyCode:
        return jsonify({"ok": False, "error": "Missing something"}), 400
    db_add_user(username, lobbyCode)
    return jsonify({"ok": True})

@login_bp.route('/db/add-avatar-selected', methods=['POST'])
def add_avatar_selected():
    data = request.get_json()
    username = data.get("username")
    avatar_id = data.get("avatar_id")
    print(f"Avatar selected: {avatar_id}")
    if not username or not avatar_id:
        return jsonify({"ok": False, "error": "Missing username or avatar_id"}), 400
    db_add_user_avatar(username, avatar_id)
    return jsonify({"ok": True})  

@login_bp.route('/db/GetAvatarImages')
def get_avatar_images():
    avatars = db_get_avatars()
    avatar_list = [{'id': avatar[0], 'filePath': 'static/imgs/avatars/'+avatar[1]} for avatar in avatars]
    return jsonify(avatar_list)

# def getStaticImagesPath(filename):
#     # Get base directory of the project
#     baseDir = Path(__file__).resolve().parent.parent.parent
#     staticDir = baseDir / 'app' / 'static' / 'imgs' / 'avatars'
#     path = staticDir / filename
#     return str(path)