lobbyCode = document.getElementById('lobby-code').value;
someoneHasBingo = false;

// Starting point for startGame
loadClassicModePlaylists();

// Displays 4 playlists for the user to choose from (TODO: Will be a wheel later)
async function loadClassicModePlaylists() {
    try {
        const res = await fetch('/spotify/playlists/classicMode');
        const playlists = await res.json();
        const container = document.getElementById('playlist-selection-container');

        playlists.forEach(playlist => {
            const playlistCell = document.createElement('div');
            playlistCell.textContent = playlist.playlist_name;
            playlistCell.addEventListener('click', async () => {
                const res = await fetch("/spotify/playlists/selectedPlaylist", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        playlist_id: playlist.id,
                        playlist_uri: playlist.playlist_id,
                        playlist_name: playlist.playlist_name,
                        lobby_code: lobbyCode
                    })
                });
                const data = await res.json();
                if (data.ok) {
                    hideDiv('playlist-selection-container');
                    showDiv('playlist-visual-container');
                    const playlistVisualContainer = document.getElementById('playlist-visual-container');
                    const playlistTitle = document.createElement('h2');
                    playlistTitle.textContent = `Playlist Chosen: ${playlist.playlist_name}`;
                    playlistVisualContainer.appendChild(playlistTitle);
                    displaySongCurrentlyPlaying();
                }
            });
            container.appendChild(playlistCell);
        });
    } catch (err) {
        console.error(err);
    }
}

// Delay timer 
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Shows which song is playing (mostly used to debug)
async function displaySongCurrentlyPlaying() {
    try {
        // Step 1: Retrieve playlist
        const response = await fetch(
            `/spotify/playlists/getSongs?lobby_code=${lobbyCode}&user_type=spotifyPlayer`
        );
        const data = await response.json();
        const songDetails = data.songs;
        console.log(songDetails);
        showDiv('song-visual-container');
        const songVisualContainer = document.getElementById('song-visual-container');

        // Plays songs until someone gets bingo
        for (const song of songDetails) {
            const songTitle = song[0];
            const songUri = song[1];
            // Step 2: Tell backend to play song
            await fetch(`/spotify/playlists/playsong?song_uri=${encodeURIComponent(songUri)}`);
            // Step 3: Display currently playing song (debugging purposes)
            songVisualContainer.innerHTML = ""; // clear previous song
            const songEl = document.createElement('p');
            songEl.textContent = `Song Currently Playing: ${songTitle}`;
            songVisualContainer.appendChild(songEl);
            // Step 4: Play 20 seconds and silence for 5 
            await delay(15000); // Play song for 15
            // TODO: Add fetch to stop song
            await fetch('/spotify/playlists/stopsong');
            await delay(5000); // Stop song for 5
            // Step 5: Check for bingo
            if (someoneHasBingo) {
                console.log(`/gameOver/${lobbyCode}`)
                window.location.href = `/gameOver/${lobbyCode}`;
                return;
            }
        }
    } catch (error) {
        console.error('Error fetching songs:', error);
    }
}