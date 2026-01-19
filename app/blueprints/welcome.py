from flask import Blueprint, render_template
from faker import Faker
from flask_socketio import SocketIO
from app.services.db import db_add_user

# Define the blueprint
welcome_bp = Blueprint('welcome', __name__)

@welcome_bp.route('/')
@welcome_bp.route('/welcome')
def welcome():
    
    return render_template('welcome.html', lobby_code=generateLobbyCode())

def generateLobbyCode():
    faker = Faker()
    lobby_code = faker.bothify(text='?????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    print(f'Generated Lobby Code: {lobby_code}')

    return lobby_code

def joinLobby(lobby_code):
    pass