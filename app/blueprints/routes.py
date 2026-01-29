# OVERVIEW: Contains routes that only render templates for now 
from flask import Blueprint, render_template
from app.blueprints.login import generateLobbyCode

main = Blueprint("main", __name__)
lobbyCode = generateLobbyCode()

# Testing page
@main.route('/testPage')
def test_page():
    return render_template('testPage.html')

## COMPUTER ROUTES ##
# Main Menu
@main.route('/mainMenu')
def main_menu():
    return render_template('mainMenu.html', lobbyCode=lobbyCode)

@main.route('/lobby')
def lobby():
    return render_template('lobby.html')

# Starts playing music
@main.route("/startGame")
def start_game():
    return render_template("startGame.html")


## Player Routes (Mobile) ##
# Starting point for players on phones
@main.route('/')
@main.route('/login')
def login():
    return render_template('login.html', lobbyCode=lobbyCode)

# Render bingo card
@main.route('/bingoCard')   
def generate_bingo_card():
    print("Rendering bingo card...")
    return render_template('bingoCard.html')

