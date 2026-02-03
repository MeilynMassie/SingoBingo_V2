# OVERVIEW: Contains routes that only render templates for now 
from flask import Blueprint, render_template
from app.services.db import db_get_lobby

main = Blueprint("main", __name__)

# Testing page
@main.route('/testPage')
def test_page():
    return render_template('testPage.html')

## COMPUTER ROUTES ##
# Main Menu - Starting point for computer
@main.route('/mainMenu')
def main_menu():
    return render_template('mainMenu.html')

# Sends players to route with lobby associated with their lobby code
@main.route('/lobby/<lobbyCode>')
def lobby(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    return render_template('lobby.html',lobbyCode=lobbyCode)

# Starts playing music
@main.route("/startGame/<lobbyCode>")
def start_game(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    return render_template("startGame.html",lobbyCode=lobbyCode)

# Game Over Bro
@main.route("/gameOver/<lobbyCode>")
def game_over(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    return render_template("gameOver.html",lobbyCode=lobbyCode)


## PLAYER ROUTES (MOBILE) ##
# Starting point for players on phones
@main.route('/')
@main.route('/login')
def login():
    return render_template('login.html')

# Render bingo card
@main.route('/bingoCard/<lobbyCode>')   
def generate_bingo_card(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    print("Rendering bingo card...")
    return render_template('bingoCard.html', lobbyCode=lobbyCode)

