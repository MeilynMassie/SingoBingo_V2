# OVERVIEW: Contains routes that only render templates for now 
from flask import Blueprint, render_template
from app.blueprints.login import generateLobbyCode

main = Blueprint("main", __name__)
lobbyCode = generateLobbyCode()

# Testing page
@main.route('/testPage')
def test_page():
    return render_template('test_page.html')

# Starting point for the computer
@main.route('/welcome')
def welcome():
    return render_template('welcome.html', lobby_code=lobbyCode)

# Starting point for players on phones
# @main.route('/')
@main.route('/login')
def login():
    return render_template('login.html', lobby_code=lobbyCode)

# Render bingo card
@main.route('/bingocard')
def generate_bingo_card():
    print("Rendering bingo card...")
    return render_template('bingo_card.html')

# Starts playing music
@main.route('/')
@main.route("/startGame")
def start_game():
    return render_template("start_game.html")