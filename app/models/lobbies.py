from app.extensions import db
from sqlalchemy.sql import func


class Lobby(db.Model):
    __tablename__ = "lobbies"

    lobby_id = db.Column(db.Integer, primary_key=True)
    lobby_code = db.Column(db.String, nullable=False)
    host_user_id = db.Column(db.Integer, db.ForeignKey("players.player_id"))
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"))
    playlist_mode = db.Column(db.String, nullable=True)
    player_mode = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False, default="waiting")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
