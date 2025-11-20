from flask import Blueprint, render_template
from faker import Faker
from flask_socketio import SocketIO
import psycopg2




# Define the blueprint
login_bp = Blueprint('login', __name__)

@login_bp.route('/')
@login_bp.route('/login')
def login():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM playlists;
    """)
    print(cur.fetchall())


    faker = Faker()
    # # = random digit (0–9)
    # ? = random letter (A–Z)
    code = faker.bothify(text='??##??')
    print(code)

    return render_template('login.html')

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="singoBingo",
        user="postgres",
        password="Lightkorra@11",
        port=5432
    )
