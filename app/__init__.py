# app/__init__.py
from flask import Flask
# from flask_socketio import SocketIO

# socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    # Register blueprints
    from app.blueprints.welcome import welcome_bp
    app.register_blueprint(welcome_bp)

    from app.blueprints.login import login_bp
    app.register_blueprint(login_bp)

    from app.blueprints.spotify import spotify_bp
    app.register_blueprint(spotify_bp)


    # Attach Socket.IO (no sockets running yet)
    # socketio.init_app(app)

    # Import socket handlers AFTER init
    # from app.blueprints import socket_connector

    return app
