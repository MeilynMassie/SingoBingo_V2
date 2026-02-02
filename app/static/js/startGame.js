lobbyCode = document.getElementById('lobby-code').value;

// Fetch Playlist JSON and build bingo card
fetch('/spotify/playlists/classicMode')
    .then(response => response.json())
    .then(playlists => {
        // Display lists of playlist options for user to select
        const playlistSelectionContainer = document.getElementById('playlist-selection-container');
        playlists.forEach(playlist => {
            const playlistCell = document.createElement('div');
            playlistCell.dataset.id = playlist.id;
            playlistCell.dataset.playlistId = playlist.playlist_id;
            playlistCell.dataset.name = playlist.playlist_name;
            playlistCell.textContent = playlist.playlist_name;
            playlistCell.addEventListener('click', () => {
                fetch("/spotify/playlists/selectedPlaylist", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        playlist_id: playlist.id,
                        playlist_uri: playlist.playlist_id,
                        playlist_name: playlist.playlist_name,
                        lobby_code: lobbyCode
                    })
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.ok) {
                            console.log("Playlist saved to db!");
                            displaySelectedPlaylist(playlist.playlist_name);
                        } else {
                            console.error("Error:", data.error);
                        }
                    });
            });
            playlistSelectionContainer.appendChild(playlistCell);
        });
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });


function displaySelectedPlaylist(playlistName) {
    hideDiv('playlist-selection-container');
    showDiv('playlist-visual-container');
    const playlistVisualContainer = document.getElementById('playlist-visual-container');
    const playlistTitle = document.createElement('h2');
    playlistTitle.textContent = playlistName;
    playlistVisualContainer.appendChild(playlistTitle);
}