from functools import wraps
from flask import session, jsonify, g
from app.spotify.oauth import get_spotify_client

def require_spotify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = session.get("spotify_token")
        if not token:
            return jsonify({"auth_required": True}), 401

        try:
            g.sp = get_spotify_client(token)
        except Exception:
            return jsonify({"auth_required": True}), 401

        return f(*args, **kwargs)
    return wrapper
