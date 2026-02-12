loadBingoCard();

function songTileClicked(event) {
    console.log("Song tile clicked: ", event.target.id);
    event.target.classList.toggle('marked');
}

// Fetch Playlist JSON and build bingo card
async function loadBingoCard() {
    try {
        const lobbyCode = document.getElementById('lobby-code').value;
        const response = await fetch(`/spotify/playlists/getSongs?lobby_code=${lobbyCode}&user_type=player`);
        const songs = await response.json();

        console.log(songs.songs);

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
                tile.addEventListener('click', songTileClicked);
                card.appendChild(tile);
            }

            const tile = document.createElement('div');
            tile.id = song;
            tile.textContent = song;
            tile.className = 'song-tile';
            tile.addEventListener('click', songTileClicked);
            card.appendChild(tile);
        });

    } catch (error) {
        console.error('Error fetching JSON:', error);
    }
}