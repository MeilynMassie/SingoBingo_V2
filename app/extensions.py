#  OVERVIEW: Things that will be needed for the entire projects
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis

# from flask_socketio import SocketIO

# socketio = SocketIO(cors_allowed_origins="*")
db = SQLAlchemy()
migrate = Migrate()
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
