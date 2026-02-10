# OVERVIEW: Routes for players
from flask import Blueprint, render_template
from app.services.db_lobby_service import db_get_lobby

playerRoutes_bp = Blueprint("playerRoutes", __name__)
@playerRoutes_bp.route('/')
@playerRoutes_bp.route('/login')
def login():
    return render_template('login.html')

# Render bingo card
@playerRoutes_bp.route('/bingoCard/<lobbyCode>')   
def generate_bingo_card(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    print("Rendering bingo card...")
    return render_template('bingoCard.html', lobbyCode=lobbyCode)
