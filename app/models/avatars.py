from app.extensions import db

class Avatar(db.Model):
    __tablename__ = "avatars"

    avatar_id = db.Column(db.Integer, primary_key=True)
    avatar_file_name = db.Column(db.String, nullable=False)
    taken = db.Column(db.Integer, nullable=True)
