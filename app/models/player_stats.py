from app.extensions import db


class PlayerStat(db.Model):
    __tablename__ = "player_stats"

    user_id = db.Column(db.Integer, db.ForeignKey("players.player_id"), primary_key=True)
    total_games = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer, nullable=True)
    losses = db.Column(db.Integer, nullable=True)
    win_rate = db.Column(db.Integer, nullable=True)
