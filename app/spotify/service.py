# Overview: All Spotify logic
class SpotifyService:
    def __init__(self, sp):
        self.sp = sp

    # TODO - Add logic to determine if there is an active device (and start one if not?)
    def isActiveDevice(self):
        pass

    def playSong(self, song_uri):
        self.sp.start_playback(uris=[song_uri])

    def stopSong(self):
        self.sp.pause_playback()

    def getPlaylistDetails(self, playlist_uri, playlist_id):
        print(f"playlist_uri: {playlist_uri}, playlist_id: {playlist_id}")
        playlist = self.sp.playlist(playlist_uri, fields="tracks.items(track(name,uri))")

        return [
            (item["track"]["uri"], item["track"]["name"], playlist_id)
            for item in playlist["tracks"]["items"]
            if item.get("track")
        ]