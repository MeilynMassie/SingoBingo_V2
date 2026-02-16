# OVERVIEW: Routes for music player
from flask import Blueprint, render_template
from app.services.db_lobby_service import db_get_lobby
from app.services.game_service import GameState


musicPlayerRoutes_bp = Blueprint("musicPlayerRoutes", __name__)

# Testing page
@musicPlayerRoutes_bp.route('/testPage')
def test_page():
    return render_template('testPage.html')

## COMPUTER ROUTES ##
# Main Menu - Starting point for computer
@musicPlayerRoutes_bp.route('/mainMenu')
def main_menu():
    return render_template('mainMenu.html')

# Sends players to route with lobby associated with their lobby code
@musicPlayerRoutes_bp.route('/lobby/<lobbyCode>')
def lobby(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    print(GameState.get_game(lobbyCode).get_state())
    if not lobbyExists:
        return "Lobby not found", 404
    return render_template('lobby.html',lobbyCode=lobbyCode)

# Starts playing music
@musicPlayerRoutes_bp.route("/startGame/<lobbyCode>")
def start_game(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    return render_template("startGame.html",lobbyCode=lobbyCode)

# Game Over Bro
@musicPlayerRoutes_bp.route("/gameOver/<lobbyCode>")
def game_over(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    return render_template("gameOver.html",lobbyCode=lobbyCode)