loadBingoCard();

// TODO: NEXT
async function verifyClickedTile(event) {
    const clickedTileId = event.target.id;
    const lobbyCode = document.getElementById('lobby-code').value;
    console.log("Clicked tile ID: ", clickedTileId);
    try {
        fetch(`/spotify/playlists/verifySong?lobby_code=${lobbyCode}&song_title=${clickedTileId}`)
    } catch (error) {
        console.error('Error verifying clicked tile:', error);
    }

}

// Fetch Playlist JSON and build bingo card
async function loadBingoCard() {
    try {
        const lobbyCode = document.getElementById('lobby-code').value;
        const response = await fetch(`/spotify/playlists/getPlayersSongs?lobby_code=${lobbyCode}`);
        const songs = await response.json();

        // Create header
        const headerRow = document.getElementById('bingo-header-row');
        const title = ['B', 'I', 'N', 'G', 'O'];

        title.forEach(letter => {
            const headerCell = document.createElement('div');
            headerCell.className = 'bingo-letter';
            headerCell.textContent = letter;
            headerRow.appendChild(headerCell);
        });

        // Add songs to bingo grid
        const card = document.getElementById('bingo-grid');

        songs.songs.forEach((song, i) => {
            // Add free space in center (index 12 of 25)
            if (i === 12) {
                const tile = document.createElement('div');
                tile.id = 'free-space';
                tile.textContent = 'FREE SPACE';
                tile.className = 'song-tile';
                tile.addEventListener('click', verifyClickedTile);
                card.appendChild(tile);
            }

            const tile = document.createElement('div');
            tile.id = song;
            tile.textContent = song;
            tile.className = 'song-tile';
            tile.addEventListener('click', verifyClickedTile);
            card.appendChild(tile);
        });

    } catch (error) {
        console.error('Error fetching JSON:', error);
    }
}