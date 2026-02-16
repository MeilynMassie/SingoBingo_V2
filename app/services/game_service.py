"""
OVERVIEW: GameState: Used to store information needed between frontend and backend (so not all details)
Includes: Lobby code, lobby status (if players can join or not), players' username, 
          playlist, index of current song, name of current song
"""

class GameState:
    _games = {}

    def __init__(self, lobby_code: str):
        self.lobby_code = lobby_code
        self.status = "waiting"
        self.players = []
        self.playlist_id = None
        self.playlist = []
        self.index = 0
        self.current_song = None

        # Store this instance in the class-level dictionary
        GameState._games[lobby_code] = self


    # ---------------------------------------
    # General GameState - Setters and Getters 
    # ---------------------------------------
    def get_state(self):
        """Return the current state as a dictionary."""
        state = {
            "lobby_code": self.lobby_code,
            "status": self.status,
            "players": self.players,
            "playlist": self.playlist,
            "index": self.index,
            "current_song": self.current_song,
        }
        return state


    # ---------------------------
    # Lobby - Setters and Getters 
    # ---------------------------
    def set_lobby_status(self, status: str):
        """Set the lobby status (waiting: players can join (default)
                                 active: game has started, no more players can join, or max players have joined
                                 inactive: game has ended)
        """
        self.status = status


    # ---------------------------
    # Players - Setters and Getters 
    # ---------------------------
    def add_player(self, username: str):
        """Add a player to the game."""
        if len(self.players) == 8:
            raise ValueError("Lobby is full")
        elif username not in self.players:
            self.players.append(username)
            if len(self.players) == 8:
                self.set_lobby_status("active")


    # ------------------------------------
    # Playlist/Songs - Setters and Getters 
    # ------------------------------------
    def set_playlist_id(self, playlist_id):
        """ Set playlist id"""
        self.playlist_id = playlist_id

    def set_playlist(self, songs: list):
        """Set the playlist for this game and start from the first song."""
        self.playlist = songs
        self.index = 0
        self.current_song = songs[0] if songs else None

    def get_next_song(self):
        """Return the next song in the playlist, or None if at the end."""
        next_index = self.index + 1
        if next_index < len(self.playlist):
            self.index = next_index
            self.current_song = self.playlist[next_index]
            return self.current_song
        return None
    

    # -----------------------------
    # Class Methods
    # -----------------------------
    @classmethod
    def get_game(cls, lobby_code: str):
        """Return the GameState instance for a lobby code."""
        game = cls._games.get(lobby_code)
        if not game:
            raise ValueError("Game not found")
        return game

    @classmethod
    def create_game(cls, lobby_code: str):
        """Create a new game state for the lobby."""
        if lobby_code in cls._games:
            raise ValueError("Game already exists")
        # Default is "waiting" so players can join until the host starts the game
        return cls(lobby_code)
    
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