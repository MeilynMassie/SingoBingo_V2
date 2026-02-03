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