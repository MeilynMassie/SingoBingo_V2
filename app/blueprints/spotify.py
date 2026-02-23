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
    if not playlist_id or not playlist_uri or not playlist_name or not lobby_code:
        return jsonify({"ok": False, "error": "Missing something"}), 400
    GameState.set_playlist_id_for_game(lobby_code, playlist_id)
    db_add_playlist_to_lobby(lobby_code=lobby_code, playlist_id=playlist_id)
    spotify = SpotifyService(g.sp)
    playlist_details = spotify.getPlaylistDetails(playlist_id=playlist_id, playlist_uri=playlist_uri)
    db_add_all_songs(playlist_details, playlist_id)
    return jsonify({"ok": True})  


# Returns a randomized playlist of 24 songs to front end
# TODO: Start here tomorrow 
@spotify_bp.route('/spotify/playlists/getPlayersSongs', methods=['GET'])
def spotify_get_playlist_songs():
    lobby_code = request.args.get("lobby_code")
    if not lobby_code:
        return jsonify({"ok": False, "error": "Missing lobby_code"}), 400
    game = GameState.get_game(lobby_code=lobby_code)
    playlist = game.get_playlist()
    print(f"Playlist from game state for lobby {lobby_code}: {playlist}")
    if playlist:
        songs = playlist 
    else:
        songs = db_get_songs_for_bingo_card(lobby_code)
        game.set_playlist_for_game(lobby_code, songs)
        print(f"Game state after setting playlist for lobby {lobby_code}: {game.get_state()}")
    random.shuffle(songs)
    songs = [song["song_name"] for song in songs]
    songs = songs[:24]
    return jsonify({
        "ok": True,
        "songs": songs
    })
 
@spotify_bp.route('/spotify/playlists/getMasterPlaylist', methods=['GET'])
def spotify_get_master_playlist():
    lobby_code = request.args.get("lobby_code")
    if not lobby_code:
        return jsonify({"ok": False, "error": "Missing lobby_code"}), 400
    game = GameState.get_game(lobby_code=lobby_code)
    print(f"Game state after setting playlist for lobby {lobby_code}: {game.get_state()}")
    playlist = game.get_playlist()
    print(f"Playlist from game state for lobby {lobby_code}: {playlist}")
    if playlist:
        songs = playlist 
    else:
        songs = db_get_songs_for_bingo_card(lobby_code)
        random.shuffle(songs)
        game.set_playlist(songs)
    game.reset_song_index_for_game(lobby_code) # TODO: Delete later, only for testing
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

@spotify_bp.route('/spotify/playlists/nextIndex')
@require_spotify
def next_index():
    lobby_code = request.args.get("lobby_code")
    if not lobby_code:
        return jsonify({"ok": False, "error": "Missing lobby_code"}), 400
    game = GameState.get_game(lobby_code=lobby_code)
    next_song = game.get_next_song()
    if not next_song:
        return jsonify({"ok": False, "error": "No more songs in playlist"}), 400
    return jsonify({"ok": True, "next_song": next_song})

@spotify_bp.route('/spotify/playlists/pausesong')
@require_spotify
def pause_song():
    spotify = SpotifyService(g.sp)
    spotify.pauseSong()
    return jsonify({"ok": True})


#  USE THIS ROUTE FOR TESTING 
@spotify_bp.route('/spotify/playlists/verifySong')
def verify_song_clicked():
    lobby_code = request.args.get("lobby_code")
    selected_song = request.args.get("song_title")
    print(f"Verifying song: {selected_song} for lobby: {lobby_code}")
    game = GameState.get_game(lobby_code=lobby_code)
    correct_song = game.get_current_song_for_game(lobby_code=lobby_code)
    print(f"Current song from game state: {correct_song}")
    if correct_song == selected_song:
        print("Song verified successfully!")
        return jsonify({"ok": True})
    else:
        print("Song verification failed.")
        return jsonify({"ok": False, "error": "Incorrect song"})