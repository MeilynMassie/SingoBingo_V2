# OVERVIEW: Contains all game state logic

class GameState:
    """Represents the state of a single game/lobby."""

    _games = {}  # class-level storage for all games

    def __init__(self, lobby_code: str):
        self.lobby_code = lobby_code
        self.status = "lobby"
        self.players = []
        self.playlist = []
        self.index = 0
        self.current_song = None

        # Store this instance in the class-level dictionary
        GameState._games[lobby_code] = self

    # -----------------------------
    # Playlist management
    # -----------------------------
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
    # Utility
    # -----------------------------
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
        print(f"Game state for {self.lobby_code}: {state}")
        return state

    # -----------------------------
    # Class-level accessors
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
        return cls(lobby_code)