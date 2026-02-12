import random
from app.models.playlists import Playlist
from psycopg2.extras import execute_values
from sqlalchemy import text
from app.extensions import db 


""" Returns a list of playlists depending on what mode is put in param
    DEFAULT: Return all
"""
# TODO: Add different modes as fit
def db_get_playlists(playlist_mode: str = None):
    playlists = Playlist.query.all()
    playlists_list = [{"id": playlist.playlist_id, 
                       "playlist_uri": playlist.playlist_uri,
                       "playlist_name": playlist.playlist_name
                       }for playlist in playlists]
    if playlist_mode == 'classic':
        random.shuffle(playlists_list)
        playlists_list = playlists_list[:4]
    return playlists_list


""" Adding songs to song db if it does not exist already """
def db_add_all_songs(playlist_details, playlist_id):
    # Check if playlist already exists
    result = db.session.execute(
        text("SELECT 1 FROM songs WHERE playlist_id = :playlist_id LIMIT 1;"),
        {"playlist_id": playlist_id}
        ).fetchone()    

    if result is None:
        conn = db.session.connection().connection
        with conn.cursor() as cur:
            data_to_insert = [(uri, name, playlist_id) for (uri, name) in playlist_details]
            query = """
                INSERT INTO songs (song_uri, song_name, playlist_id)
                VALUES %s;
            """
            execute_values(cur, query, data_to_insert)
        conn.commit()
    else:
        print("Songs already exist for this playlist.")

"""  """
def db_get_songs_for_bingo_card(lobby_code):
    result = db.session.execute(
        text("""
             SELECT song_name, song_uri FROM lobbies 
             join songs on lobbies.playlist_id = songs.playlist_id
             where lobby_code = :lobby_code;"""),
        {"lobby_code": lobby_code}
        ).fetchall() 
    if result is None: 
        print("Error retrieving songs for bingo")
    return result