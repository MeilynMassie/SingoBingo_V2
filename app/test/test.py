# OVERVIEW: Only for testing purposes
import random
# import psycopg2
from flask import (
    Blueprint, 
    jsonify, 
    session, 
    render_template
)
from app.services.db import (
    db_get_playlists, 
    db_get_playlist_details
)  

# Fetch playlists from Spotify and add songs to DB
# DB or Spotify
def spotify_get_four_playlists():
    list_of_playlists = db_get_playlists()
    # Step 2 Shuffle playlists and select 4 randomly
    random.shuffle(list_of_playlists)
    list_of_playlists = list_of_playlists[:4]
    list_of_playlists = [{'id': playlist[0], 'playlist_id': playlist[1], 'playlist_name': playlist[2]} for playlist in list_of_playlists]
    print(f"Playlists from DB: {list_of_playlists}")
    selected_playlist = list_of_playlists[0]['playlist_name']
    print(f"Selected playlist: {selected_playlist}")
    return selected_playlist


spotify_get_four_playlists()



















def spotify_add_songs_to_db(playlist_id):
    # if playlist_id not in db
    track_details = sp.playlist_items(playlist_id, fields='items.track.name, items.track.uri')
    for item in track_details['items']:
        track_name = item['track']['name']
        track_uri = item['track']['uri']
        # db_add_song(track_name, track_uri, playlist_id)
        print(f'TRACK NAME: {track_name}, URI: {track_uri}, PLAYLIST{playlist_id}\n')
        playlist.append(track_name)

def spotify_play_song(playlist_id):
    # Step 3: Player selects a playlist (TODO: Implement player selection, add different game modes)
    print(f"Playlists from DB: {playlist_id}")
    # Step 4: Display playlist selected
    # return render_template('start_game.html', selected_playlist=selected_playlist)
    pass 