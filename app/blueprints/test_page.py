import os
from flask import Blueprint, render_template
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from app.services.db import db_get_playlist_details

# Define the blueprint
test_page_bp = Blueprint('testPage', __name__)

@test_page_bp.route('/testPage')
def testPage():
    details = db_get_playlist_details('playlist_name')
    print(f'Playlist Names from details function: {details}')

    return render_template('test_page.html', playlists=details)