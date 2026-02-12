from app.extensions import db
from sqlalchemy.sql import func


class Player(db.Model):
    __tablename__ = "players"

    player_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    avatar_id = db.Column(db.Integer, db.ForeignKey("avatars.avatar_id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    lobby_code = db.Column(db.String, db.ForeignKey("lobbies.lobby_id"))
    status = db.Column(db.String, nullable=True, default="active")