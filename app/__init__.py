from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    # Register blueprints
    # from app.blueprints.routes import main
    # app.register_blueprint(main)

    from app.blueprints.login import login_bp
    app.register_blueprint(login_bp)

    from app.blueprints.spotify import spotify_bp
    app.register_blueprint(spotify_bp)

    # Init SocketIO
    socketio.init_app(app)

    # ---- IMPORT SOCKET HANDLERS HERE (AFTER INIT) ----
    from app.blueprints import socket_connector
    # --------------------------------------------------

    return app
