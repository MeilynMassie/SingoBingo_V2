#OVERVIEW: All spotiPy related functions
import random
from flask import Blueprint, jsonify, session, render_template
from app.services.db import db_get_playlist_details
from app.blueprints.spotifyOAuth import get_spotify_client
# import psycopg2

spotify_bp = Blueprint('spotify', __name__)

# Fetch playlists from Spotify and add songs to DB
@spotify_bp.route('/spotify/playlists')
def spotify_get_playlists():
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

# TODO NEXT: Play song from playlist (NOT HARDCOODED)
# TODO: Start playing from the most popular parts of the song
@spotify_bp.route('/spotify/playsong')
def play_song():
    songName = "Takedown - Instrumental"
    sp = get_spotify_client(session.get("spotify_token"))
    sp.start_playback(
        uris=["spotify:track:0SdkWJzc4T1ck7tD6lV2Kw"]
    )
    return render_template('start_game.html', song=songName)