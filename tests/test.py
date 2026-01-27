#OVERVIEW: All spotiPy related functions
import os
from flask import Blueprint, redirect, session, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

spotify_bp = Blueprint('spotify', __name__)
load_dotenv()
spotify_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="playlist-read-private user-read-playback-state user-modify-playback-state",
)

# @spotify_bp.route("/spotify/login")
def spotify_login():
    auth_url = spotify_oauth.get_authorize_url()
    return auth_url
    # return redirect(auth_url)

@spotify_bp.route("/callback")
def spotify_callback():
    code = request.args.get("code")

    token_info = spotify_oauth.get_access_token(code)

    # ✅ Store token per user
    session["spotify_token"] = token_info

    return session["spotify_token"]


print(f"Spotify Login: {spotify_login()}")
print(f"Spotify Callback: {spotify_callback()}")