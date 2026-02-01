#OVERVIEW: All DB related stuff
import os
import psycopg2
from dotenv import load_dotenv


# CONNECTION QUERY
def db_get_connection():
    print("Establishing DB connection...")
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT'),
    )
    return conn.cursor()
    
# PLAYLISTS QUERIES
def db_get_playlists():
    print("Fetching all playlists from DB...")
    cur = db_get_connection()
    cur.execute("""
    SELECT * FROM playlists;
    """)
    result = cur.fetchall()
    cur.close()
    cur.connection.close()
    return result

def db_get_playlist_by_id(playlist_id):
    print("Fetching playlist by ID from DB...")
    cur = db_get_connection()
    cur.execute("""
    SELECT * FROM playlists WHERE id = %s;
    """, (playlist_id,))
    result = cur.fetchone()
    cur.close()
    cur.connection.close()
    return result

def db_get_playlist_details(column_name):
    print("Fetching playlist details from DB...")
    cur = db_get_connection()
    query = f"SELECT {column_name} FROM playlists;" # DON'T CHANGE THIS (COLUMN NAMES HAVE TO BE A STRING AND NOT INJECTED)
    cur.execute(query)
    result = [row[0] for row in cur.fetchall()]
    cur.close()
    return result

# PLAYERS QUERIES
def db_add_user(username, lobby_code):
    print("Adding user to DB...")
    print(f"Username: {username}, Lobby Code: {lobby_code}")
    cur = db_get_connection()
    cur.execute("""
    INSERT INTO players (username, lobby_code) VALUES (%s, %s);
    """, (username, lobby_code))
    cur.connection.commit()
    cur.close()
    cur.connection.close() 

# LOBBIES QUERIES
def db_get_lobby(lobbyCode):
    cur = db_get_connection()
    cur.execute("""
    select lobby_code from lobbies where lobby_code=%s;
    """, (lobbyCode,))
    results = cur.fetchall()
    cur.close()
    cur.connection.close()
    return results

def db_create_lobby(lobbyCode, playerMode, playlistMode):
    playerMode = 1 if playerMode == "singleplayer" else 8
    print("Adding lobby code to db...")
    print(f"(IN DB) Creating lobby: {lobbyCode}, Playlist Mode: {playlistMode}, Player Mode {playerMode}")
    # cur = db_get_connection()
    # cur.execute("""
    # INSERT INTO lobbies (lobby_code, player_mode, playlist_mode) VALUES (%s, %s, %s);
    # """, (lobbyCode, playerMode, playlistMode))
    # cur.connection.commit()
    # cur.close()
    # cur.connection.close() 

# PLAYERS AND AVATARS UPDATE
def db_add_user_avatar(username, avatar_id):
    cur = db_get_connection()
    print("Updating avatar taken status in DB...")
    print(f"Avatar ID: {avatar_id}")
    cur.execute("""
    UPDATE avatars SET taken = 1 WHERE avatar_id = %s;
    """, (avatar_id,))
    cur.connection.commit()

    print("Adding user with avatar to DB...")
    cur.execute("""
    UPDATE players SET avatar_id=%s
        WHERE LOWER(username) = LOWER(%s);
    """, (avatar_id, username))
    cur.connection.commit()
    cur.close()
    cur.connection.close()

# AVATAR QUERIES
# TODO: Ignore taken for now
def db_get_avatars():
    print("Fetching all avatars from DB...")
    cur = db_get_connection()
    cur.execute("""
        SELECT * FROM avatars
        --WHERE taken = 0;
    """)
    results = cur.fetchall()
    cur.close()
    cur.connection.close()
    return results

# TODO: Add a trigger to know when a user is added to that lobby for the circle of avatars to display