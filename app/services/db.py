import os
import psycopg2
from dotenv import load_dotenv


# Connection Query
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
    
# Playlists Queries
def db_get_playlists():
    print("Fetching all playlists from DB...")
    cur = db_get_connection()
    cur.execute("""
    SELECT * FROM playlists;
    """)
    return cur.fetchall()

def db_get_playlist_by_id(playlist_id):
    print("Fetching playlist by ID from DB...")
    cur = db_get_connection()
    cur.execute("""
    SELECT * FROM playlists WHERE id = %s;
    """, (playlist_id,))
    return cur.fetchone()

def db_get_playlist_details(column_name):
    print("Fetching playlist details from DB...")
    cur = db_get_connection()
    query = f"SELECT {column_name} FROM playlists;"
    cur.execute(query)
    return [row[0] for row in cur.fetchall()]

# Users Queries
def db_add_user(user_id, lobby_code):
    print("Adding user to DB...")
    cur = db_get_connection()
    cur.execute("""
    INSERT INTO users (id, lobby_code) VALUES (%s, %s);
    """, (user_id, lobby_code))
    cur.connection.commit()

# def db_get_users_by_lobby_code(lobby_code):
#     print("Fetching users by lobby code from DB...")
#     cur = db_get_connection()
#     cur.execute("""
#     SELECT * FROM users WHERE id = %s;
#     """, (lobby_code,))
#     return cur.fetchall()