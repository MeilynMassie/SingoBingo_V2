# Overview: Any DB logic revolving around the player (i.e. players, avatar, player_stats tables)
from sqlalchemy import func
from app.extensions import db
from app.models.players import Player
from app.models.player_stats import PlayerStat
from app.models.avatars import Avatar


""" Add a new player to players db """
def db_add_player(username: str, lobby_code: str) -> Player:
    player = Player(username=username, lobby_code=lobby_code)
    db.session.add(player)
    db.session.commit()

""" Select all avatars and return them """
def db_get_avatars():
    avatars = Avatar.query.all()
    avatar_list = [{'id': avatar.avatar_id, 'filePath': 'static/imgs/avatars/'+avatar.avatar_file_name} for avatar in avatars]
    return avatar_list

""" Add chosen avatar to existing player in players db """
def db_assign_avatar_to_player(username: str, avatar_id: int):
    player = Player.query.filter(func.lower(Player.username) == username.lower()).first()
    if player:
        player.avatar_id = avatar_id
        db.session.commit()

""" Mark avatar as chosen """
def db_mark_avatar_taken(avatar_id: int):
    avatar = Avatar.query.get(avatar_id)
    if avatar:
        avatar.taken = 1
        db.session.commit()