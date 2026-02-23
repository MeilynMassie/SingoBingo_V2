"""
OVERVIEW: GameState: Used to store information needed between frontend and backend (so not all details)
Includes: Lobby code, lobby status (if players can join or not), players' username, 
          playlist, index of current song, name of current song
"""

import json
from app.extensions import redis_client

class GameState:
    def __init__(self, lobby_code: str):
        self.lobby_code = lobby_code

    # ---------------------------------------
    # General GameState - Setters and Getters 
    # ---------------------------------------
    def get_state(self):
        """Return the current state as a dictionary."""
        state_str = redis_client.get(f"game:{self.lobby_code}")
        if not state_str:
            raise ValueError("Game not found")
        state = json.loads(state_str)
        state["lobby_code"] = self.lobby_code  # Add lobby_code to the state
        return state


    # ---------------------------
    # Lobby - Setters and Getters 
    # ---------------------------
    def set_lobby_status(self, status: str):
        """Set the lobby status (waiting: players can join (default)
                                 active: game has started, no more players can join, or max players have joined
                                 inactive: game has ended)
        """
        state = self.get_state()
        state["status"] = status
        redis_client.set(f"game:{self.lobby_code}", json.dumps(state))


    # ---------------------------
    # Players - Setters and Getters 
    # ---------------------------
    def add_player(self, username: str):
        """Add a player to the game."""
        state = self.get_state()
        if len(state["players"]) == 8:
            raise ValueError("Lobby is full")
        elif username not in state["players"]:
            state["players"].append(username)
            if len(state["players"]) == 8:
                state["status"] = "active"
            redis_client.set(f"game:{self.lobby_code}", json.dumps(state))


    # ------------------------------------
    # Playlist/Songs - Setters and Getters 
    # ------------------------------------
    def set_playlist_id(self, playlist_id):
        """ Set playlist id"""
        state = self.get_state()
        state["playlist_id"] = playlist_id
        redis_client.set(f"game:{self.lobby_code}", json.dumps(state))

    def set_playlist(self, songs: list):
        """Set the playlist for this game and start from the first song."""
        state = self.get_state()
        print(songs)
        state["playlist"] = songs
        state["index"] = 0
        state["current_song"] = songs[0]["song_name"] if songs else None
        redis_client.set(f"game:{self.lobby_code}", json.dumps(state))

    def get_playlist(self):
        state = self.get_state()
        return state["playlist"]

    def get_next_song(self):
        """Return the next song in the playlist, or None if at the end."""
        state = self.get_state()
        next_index = state["index"] + 1
        if next_index < len(state["playlist"]):
            state["index"] = next_index
            state["current_song"] = state["playlist"][next_index]
            redis_client.set(f"game:{self.lobby_code}", json.dumps(state))
            return state["current_song"]
        return None
    

    # -----------------------------
    # Class Methods
    # -----------------------------
    @classmethod
    def get_game(cls, lobby_code: str):
        """Return the GameState instance for a lobby code."""
        state_str = redis_client.get(f"game:{lobby_code}")
        if not state_str:
            raise ValueError("Game not found")
        return cls(lobby_code)  # Return instance, but state is in Redis

    @classmethod
    def create_game(cls, lobby_code: str):
        if redis_client.exists(f"game:{lobby_code}"):
            raise ValueError("Game already exists")

        initial_state = {
            "status": "waiting",
            "players": [],
            "playlist_id": None,
            "playlist": [],
            "index": 0,
            "current_song": None
        }

        redis_client.set(f"game:{lobby_code}", json.dumps(initial_state))

        return cls(lobby_code)
    
    @classmethod
    def delete_game(cls, lobby_code: str):
        if not redis_client.exists(f"game:{lobby_code}"):
            raise ValueError("Game does not exist")

        redis_client.delete(f"game:{lobby_code}")
        print("Game deleted successfully")
        return "Game deleted successfully"
    
    @classmethod
    def set_playlist_id_for_game(cls, lobby_code, playlist_id):
        game = cls.get_game(lobby_code)
        game.set_playlist_id(playlist_id)

    @classmethod
    def set_playlist_for_game(cls, lobby_code, songs):
        game = cls.get_game(lobby_code)
        game.set_playlist(songs)

    @classmethod
    def add_player_for_game(cls, lobby_code, username):
        game = cls.get_game(lobby_code)
        game.add_player(username)

    @classmethod
    def get_current_song_for_game(cls, lobby_code):
        game = cls.get_game(lobby_code)
        state = game.get_state()
        return state["current_song"]["song_name"]
    
    @classmethod
    def reset_song_index_for_game(cls, lobby_code):
        game = cls.get_game(lobby_code)
        state = game.get_state()
        state["index"] = 0
        state["current_song"] = state["playlist"][0]
        redis_client.set(f"game:{lobby_code}", json.dumps(state))