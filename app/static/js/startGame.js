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
                console.log(`Playlist Name: ${playlist.id}`);
                console.log(`Playlist Name: ${playlist.playlist_id}`);
                console.log(`Playlist Name: ${playlist.playlist_name}`);
            });
            playlistSelectionContainer.appendChild(playlistCell);
        });
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });