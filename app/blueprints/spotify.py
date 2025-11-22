import os
from flask import Blueprint, render_template, session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Define the blueprint
spotify_bp = Blueprint('spotify', __name__)

@spotify_bp.route('/playlists')
def get_playlists():
    print("TOKEN:", session.get("spotify_token"))

    load_dotenv()  # Make sure .env is loaded

    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="playlist-read-private"
    ))
    print("Spotify client initialized.")

    user = sp.current_user()
    print(f"User ID: {user['id']}, User Display Name: {user['display_name']}")

    playlists = sp.current_user_playlists()
    playlist_data = []

    while playlists:
        items = playlists.get('items', [])
        for playlist in items:
            playlist_data.append({
                'name': playlist['name'],
                'uri': playlist['uri'],
                'url': playlist['external_urls']['spotify']
            })
        # Move to next page after processing all items
        if playlists.get('next'):
            playlists = sp.next(playlists)
        else:
            playlists = None

    return render_template('spotify.html', playlists=playlist_data)
