#OVERVIEW: All spotiPy related functions
import random
# import psycopg2
from flask import (Blueprint, 
    jsonify, 
    session, 
    render_template,
    request,
    redirect,
    url_for
)
from app.services.db import (
    db_get_playlists, 
    db_add_playlist_to_lobby,
    db_add_all_songs,
    db_get_songs_for_player
)  
from app.blueprints.spotifyOAuth import get_spotify_client


spotify_bp = Blueprint('spotify', __name__)


# Fetch playlists from Spotify and add songs to DB
# Sends 4 playlists to front end for user to select playlist
@spotify_bp.route('/spotify/playlists/classicMode')
def spotify_get_four_playlists():
    # Step 1: DB - Get 4 playlists to choose from (TODO:create wheel to display later)
    list_of_playlists = db_get_playlists()
    # Step 2 Shuffle playlists and select 4 randomly
    random.shuffle(list_of_playlists)
    list_of_playlists = list_of_playlists[:4]
    list_of_playlists = [{'id': playlist[0], 'playlist_id': playlist[1], 'playlist_name': playlist[2]} for playlist in list_of_playlists]
    print(f"Playlists from DB: {list_of_playlists}")
    return jsonify(list_of_playlists)


# Get selected playlist from user, save to db, return list of songs
@spotify_bp.route('/spotify/playlists/selectedPlaylist', methods=['POST'])
def spotify_get_selected_playlist():
    # Step 1: Read player selected playlist 
    data = request.get_json()
    playlist_id = data.get("playlist_id")
    playlist_uri = data.get("playlist_uri")
    playlist_name = data.get("playlist_name")
    lobby_code = data.get("lobby_code")
    print(f"playlist_id: {playlist_id}, playlist_uri: {playlist_uri}, song_name: {playlist_name}, lobby_code: {lobby_code}")
    if not playlist_id or not playlist_uri or not playlist_name or not lobby_code:
        return jsonify({"ok": False, "error": "Missing something"}), 400
    # Step 2: Add playlist to lobby table
    db_add_playlist_to_lobby(lobby_code, playlist_id)
    # Step 3: Add songs from playlist to db
    sp = get_spotify_client(session.get("spotify_token"))
    playlist = sp.playlist(playlist_id=playlist_uri, fields="tracks.items(track(name,uri))")
    playlist_details = [(item["track"]["uri"],item["track"]["name"],playlist_id) for item in playlist["tracks"]["items"] if item["track"] is not None]
    print(f"Playlist Length: {len(playlist_details)}")
    db_add_all_songs(playlist_details, playlist_id)
    return jsonify({"ok": True})  
    
# Returns a randomized playlist of 24 songs to front end
@spotify_bp.route('/spotify/playlists/songs', methods=['GET'])
def spotify_get_playlist_songs():
    lobby_code = request.args.get("lobby_code")
    user_type = request.args.get("user_type")
    if not lobby_code:
        return jsonify({"ok": False, "error": "Missing lobby_code"}), 400
    songs = db_get_songs_for_player(lobby_code)
    random.shuffle(songs)
    if user_type == 'player':
        songs = [song[0] for song in songs]
        songs = songs[:24]
        print(songs)
        return jsonify({
            "ok": True,
            "songs": songs
        })
    else: # TODO: This will be for when the computer playing the music request the order the songs will play in 
        return jsonify({
            "ok": True,
            "songs": songs
        })
    

# TODO NEXT: Play song from playlist (NOT HARDCOODED)
# TODO: Start playing from the most popular parts of the song
@spotify_bp.route('/spotify/playsong')
def play_song():
    songName = "Takedown - Instrumental"
    token = session.get("spotify_token")
    if not token:
        return redirect(url_for('spotifyOAuth.spotify_login'))
    sp = get_spotify_client(token)
    if not sp:
        return redirect(url_for('spotifyOAuth.spotify_login'))
    sp.start_playback(
        uris=["spotify:track:0SdkWJzc4T1ck7tD6lV2Kw"]
    )
    return render_template('startGame.html', song=songName)