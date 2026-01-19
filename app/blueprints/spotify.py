#OVERVIEW: All spotiPy related functions
import os
from flask import Blueprint, render_template, jsonify
from spotipy import Spotify
import random
from spotipy.oauth2 import SpotifyOAuth
from app.services.db import db_get_playlist_details
from dotenv import load_dotenv
# import psycopg2

spotify_bp = Blueprint('spotify', __name__)

# Fetch playlists from Spotify and add songs to DB
@spotify_bp.route('/api/playlists')
def spotify_get_playlists():
    print("Fetching playlists from Spotify...")
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
    # track_details = sp.playlist_items(playlist_id, fields='items.track.name, items.track.uri')
    # for item in track_details['items']:
    #     track_name = item['track']['name']
    #     track_uri = item['track']['uri']
    #     # db_add_song(track_name, track_uri, playlist_id)
    #     print(f'TRACK NAME: {track_name}, URI: {track_uri}, PLAYLIST{playlist_id}\n')
    #     playlist.append(track_name)
    playlist = ['A Whole New World', 'Show Yourself', 'Hakuna Matata', 'When Will My Life Begin? - From "Tangled" / Soundtrack Version', 'Kiss the Girl', 
                 'Almost There', "I Wan'na Be Like You (The Monkey Song)", 'When I Am Older', 'Honor To Us All', 'For the First Time in Forever - From "Frozen"/Soundtrack Version', 
                 'Be Our Guest', "I'll Make a Man Out of You", 'Into the Unknown', 'Lost in the Woods', 'Touch The Sky - From "Brave"/Soundtrack', 
                 'One Jump Ahead', 'In Summer - From "Frozen"/Soundtrack Version', "I Just Can't Wait to Be King", 'Reflection', "You'll Be In My Heart", 
                 'The Gospel Truth II', 'Mother Knows Best - From "Tangled"/Soundtrack Version', 'Gaston', 'The Gospel Truth I / Main Titles - Hercules', 'Friend Like Me']
    # Select 25 random songs
    n = random.randint(1, 5)  # LOW number of shuffles
    for _ in range(n):
        random.shuffle(playlist)
    playlist = playlist[:25]

    print(playlist)
    return jsonify(playlist)

# Render bingo card
@spotify_bp.route('/bingocard')
def generate_bingo_card():
    print("Rendering bingo card...")
    return render_template('bingo_card.html')

# Play song from playlist
@spotify_bp.route('/playsong')
def play_song():
    print("Playing song...")
    # sp.start_playback(uris=track_uri)  
    # sp.start_playback(uris='spotify:track:09MvGKcju2jf2ktxDa0s17')  
    # print(f'Playing song: {song}')