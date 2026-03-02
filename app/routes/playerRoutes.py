# OVERVIEW: Routes for players
from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect
from app.services.db_lobby_service import db_get_lobby

playerRoutes_bp = Blueprint("playerRoutes", __name__)
@playerRoutes_bp.route('/')
@playerRoutes_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# Render bingo card
@playerRoutes_bp.route('/bingoCard/<lobbyCode>')   
def generate_bingo_card(lobbyCode):
    username = session.get("username")
    sessionLobby = session.get("lobbyCode")
    if not username or sessionLobby != lobbyCode:
        return redirect(url_for("playerRoutes.login"))
    return render_template(
        "bingoCard.html",
        lobbyCode=lobbyCode,
        username=username
    )
