# OVERVIEW: Contains routes that only render templates for now 
from flask import Blueprint, render_template
from app.services.db import db_get_lobby

main = Blueprint("main", __name__)

# Testing page
@main.route('/testPage')
def test_page():
    return render_template('testPage.html')

## COMPUTER ROUTES ##
# Main Menu
@main.route('/mainMenu')
def main_menu():
    return render_template('mainMenu.html')

@main.route('/lobby/<lobbyCode>')
def lobby(lobbyCode):
    lobbyExists = db_get_lobby(lobbyCode)
    print(lobbyExists)
    if not lobbyExists:
        return "Lobby not found", 404
    # return render_template('bingoCard.html') 
    return render_template('lobby.html',lobbyCode=lobbyCode)

# Starts playing music
@main.route("/startGame")
def start_game():
    return render_template("startGame.html")


## Player Routes (Mobile) ##
# Starting point for players on phones
@main.route('/')
@main.route('/login')
def login():
    return render_template('login.html')

# Render bingo card
@main.route('/bingoCard')   
def generate_bingo_card():
    print("Rendering bingo card...")
    return render_template('bingoCard.html')

