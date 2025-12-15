from flask import Blueprint, render_template
from faker import Faker
from flask_socketio import SocketIO
from app.services.db import db_add_user

# Define the blueprint
login_bp = Blueprint('login', __name__)

@login_bp.route('/')
@login_bp.route('/login')
def login():
    
    return render_template('join.html', lobby_code=generateLobbyCode())

def generateLobbyCode():
    faker = Faker()
    lobby_code = faker.bothify(text='?????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    print(f'Generated Lobby Code: {lobby_code}')

    return lobby_code

def joinLobby(lobby_code):
    pass