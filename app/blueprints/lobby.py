from flask import Blueprint, jsonify, request
from app.services.db_lobby_service import ( 
    db_get_all_active_lobbies
)

lobby_bp = Blueprint('lobby', __name__)

# Retrieves all active lobby codes
@lobby_bp.route('/db/getLobbyCode')
def get_lobby_code():
    listOfLobbies = db_get_all_active_lobbies()
    print(listOfLobbies)
    return jsonify(listOfLobbies)