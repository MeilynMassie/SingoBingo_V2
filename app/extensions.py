#  OVERVIEW: Things that will be needed for the entire projects
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_socketio import SocketIO

# socketio = SocketIO(cors_allowed_origins="*")
db = SQLAlchemy()
migrate = Migrate()
