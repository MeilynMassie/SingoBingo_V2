from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Flask!'

def create_app():

    # Import and register blueprint
    from app.blueprints.spotify import spotify_bp
    app.register_blueprint(spotify_bp)

    return app
