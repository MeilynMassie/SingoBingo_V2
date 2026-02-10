from app.extensions import db

class Song(db.Model):
    __tablename__ = "songs"

    song_id = db.Column(db.Integer, primary_key=True)
    song_uri = db.Column(db.String, nullable=False)
    song_name = db.Column(db.String, nullable=False)
    playlist_id = db.Column(db.String, db.ForeignKey("playlists.playlist_id"))
