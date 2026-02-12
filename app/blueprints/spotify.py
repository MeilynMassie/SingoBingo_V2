#OVERVIEW: All spotiPy related functions
import random
from flask import (
    Blueprint, 
    jsonify, 
    request,
    g
) 
from app.services.db_playlist_service import (
    db_get_playlists,
    db_add_all_songs,
    db_get_songs_for_bingo_card
)
from app.services.db_lobby_service import (
    db_add_playlist_to_lobby
)
from app.services.game_service import GameState
from app.spotify.service import SpotifyService
from app.spotify.decorator import require_spotify


spotify_bp = Blueprint('spotify', __name__)

# Fetch playlists from Spotify and add songs to DB
# Sends 4 playlists to front end for user to select playlist
@spotify_bp.route('/spotify/getplaylists')
def spotify_get_playlists():
    # TODO: Create wheel to display later
    mode = request.args.get("mode")
    list_of_playlists = db_get_playlists(playlist_mode=mode)
    print(f"Playlists from DB: {list_of_playlists}")
    return jsonify(list_of_playlists)


# Get selected playlist from user, save to db, return list of songs
@spotify_bp.route('/spotify/playlists/selectedPlaylist', methods=['POST'])
@require_spotify
def spotify_get_selected_playlist():
    data = request.get_json()
    playlist_id = data.get("playlist_id")
    playlist_uri = data.get("playlist_uri")
    playlist_name = data.get("playlist_name")
    lobby_code = data.get("lobby_code")
    print(f"playlist_id: {playlist_id}, playlist_uri: {playlist_uri}, song_name: {playlist_name}, lobby_code: {lobby_code}")
    if not playlist_id or not playlist_uri or not playlist_name or not lobby_code:
        return jsonify({"ok": False, "error": "Missing something"}), 400
    db_add_playlist_to_lobby(lobby_code=lobby_code, playlist_id=playlist_id)
    spotify = SpotifyService(g.sp)
    playlist_details = spotify.getPlaylistDetails(playlist_id=playlist_id, playlist_uri=playlist_uri)
    print(playlist_details)
    db_add_all_songs(playlist_details, playlist_id)
    return jsonify({"ok": True})  
    

# Returns a randomized playlist of 24 songs to front end
# TODO: Start here tomorrow 
@spotify_bp.route('/spotify/playlists/getSongs', methods=['GET'])
def spotify_get_playlist_songs():
    lobby_code = request.args.get("lobby_code")
    user_type = request.args.get("user_type")
    if not lobby_code:
        return jsonify({"ok": False, "error": "Missing lobby_code"}), 400
    songs = db_get_songs_for_bingo_card(lobby_code)
    songs = [{"song_name": song.song_name, "song_uri": song.song_uri} for song in songs]
    random.shuffle(songs)
    print("After shuffle")
    # TODO: Add game state stuff here later
    if user_type == 'player':
        print(f"Player songs: {songs}")
        songs = [song["song_name"] for song in songs]
        songs = songs[:24]
        print(f"\n\nPlayer songs after slice: {songs}")
        return jsonify({
            "ok": True,
            "songs": songs
        })
    return jsonify({
        "ok": True,
        "songs": songs
    })  

# TODO: Start playing from the most popular parts of the song
@spotify_bp.route('/spotify/playlists/playsong', methods=['GET'])
@require_spotify
def play_song():
    song_uri = request.args.get("song_uri")
    spotify = SpotifyService(g.sp)
    spotify.playSong(song_uri)
    # spotify.playSong('spotify:track:5p9UNx7gLRdRoaEHd8TAnz')
    return jsonify({"ok": True})

@spotify_bp.route('/spotify/playlists/stopsong')
@require_spotify
def stop_song():
    spotify = SpotifyService(g.sp)
    
    spotify.stopSong()
    return jsonify({"ok": True})


#  USE THIS ROUTE FOR TESTING 
@spotify_bp.route('/test/playsong')
@require_spotify
def test_play_song():
    spotify = SpotifyService(g.sp)
    spotify.playSong('spotify:track:28UMEtwyUUy5u0UWOVHwiI')
    return jsonify({"ok": True})

@spotify_bp.route('/getGameState')
def get_game_state():
    lobby_code = request.args.get("lobby_code")
    GameState.create_game_state(lobby_code)

    # GameState.set_playlist(lobby_code, ["song1", "song2", "song3"])
    print(GameState.get_game_state(lobby_code))
    return jsonify({"ok": True, "data": GameState.get_game_state(lobby_code)})


@spotify_bp.route('/test/everything')
def test_ultima():
    # TODO: Test all game state stuff here step by step
    pass