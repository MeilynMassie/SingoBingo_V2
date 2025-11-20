# app/routes.py
from flask import Blueprint, render_template, request, jsonify

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/playlists")
def playlists():
    return render_template("spotify.html")

@main.route("/join")
def join():
    return render_template("join.html")

@main.route("/api/test", methods=["POST"])
def test_api():
    data = request.json
    return jsonify({"received": data})
