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
def spotify_get_playlists():
    # Step 1: DB - Get 4 playlists to choose from (TODO:create wheel to display later)
    list_of_playlists = db_get_playlists()
    print(f"Playlists from DB: {list_of_playlists}")
    # Step 2
    pass 


spotify_get_playlists()







# def test_get_user():
#     user is None
#     assert user is not None