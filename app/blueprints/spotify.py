#OVERVIEW: All spotiPy related functions
import os
from flask import Blueprint, render_template, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from app.services.db import db_get_playlist_details
from dotenv import load_dotenv
# import psycopg2


# Define the blueprint
spotify_bp = Blueprint('spotify', __name__)

@spotify_bp.route('/api/playlists')
def spotify_get_playlists():
    load_dotenv()

    # Initialize Spotify client
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="playlist-read-private"
    ))
    print("Spotify client initialized.")

    # Fetch playlists from db
    details = db_get_playlist_details('playlist_uri')
    playlist_id = details[0]
    print(f"Fetched playlist ID from DB: {playlist_id}")
    playlist = []
    # TODO: Fix playlist id retrieval
    # playlist_id = db_get_playlist_where('playlist_id', 'playlist_uri', playlist)

    # Add songs to db
    track_details = sp.playlist_items(playlist_id, fields='items.track.name, items.track.uri')
    for item in track_details['items']:
        track_name = item['track']['name']
        track_uri = item['track']['uri']
        # db_add_song(track_name, track_uri, playlist_id)
        print(f'TRACK NAME: {track_name}, URI: {track_uri}, PLAYLIST{playlist_id}\n')
        playlist.append(track_name)
    # Play song from playlist
    # sp.start_playback(uris=track_uri)  
    sp.start_playback(uris='spotify:track:09MvGKcju2jf2ktxDa0s17')  
    # print(f'Playing song: {song}')
    print(playlist)
    return jsonify(playlist)

@spotify_bp.route('/bingocard')
def generate_bingo_card():
    return render_template('bingo_card.html')