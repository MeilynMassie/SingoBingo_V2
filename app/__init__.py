import os
from flask import Flask
from app.config import Config
from app.extensions import db, migrate
# from flask_socketio import SocketIO

# socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # Register models
    from app import models
    # Register blueprints
    from app.routes.musicPlayerRoutes import musicPlayerRoutes_bp
    app.register_blueprint(musicPlayerRoutes_bp)

    from app.routes.playerRoutes import playerRoutes_bp
    app.register_blueprint(playerRoutes_bp)

    from app.blueprints.mainMenu import mainMenu_bp
    app.register_blueprint(mainMenu_bp)

    from app.blueprints.login import login_bp
    app.register_blueprint(login_bp)

    from app.blueprints.lobby import lobby_bp
    app.register_blueprint(lobby_bp)

    from app.spotify.oauth import spotifyOAuth_bp
    app.register_blueprint(spotifyOAuth_bp)

    from app.blueprints.spotify import spotify_bp
    app.register_blueprint(spotify_bp)



    # Attach Socket.IO (no sockets running yet)
    # socketio.init_app(app)

    # Import socket handlers AFTER init
    # from app.blueprints import socket_connector

    return app
