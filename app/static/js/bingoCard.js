function songTileClicked(event) {
    console.log("Song tile clicked: ", event.target.id);
    event.target.classList.toggle('marked');
}

// Fetch Playlist JSON and build bingo card
fetch('/api/playlists')
    .then(response => response.json())
    .then(playlist => {
        console.log(playlist);
        // Create a 6x5 bingo card
        const bingoCard = document.getElementById('bingo-card');
        const headerRow = document.getElementById('bingo-header-row');
        // Create header
        const title = ['B', 'I', 'N', 'G', 'O'];
        title.forEach(letter => {
            const headerCell = document.createElement('div');
            headerCell.className = 'bingo-letter';
            headerCell.textContent = letter;
            headerRow.appendChild(headerCell);
        });
        // Add songs to bingo grid
        const card = document.getElementById('bingo-grid');
        playlist.forEach(song => {
            const tile = document.createElement('div');
            tile.className = 'song-tile';
            tile.id = song;
            tile.textContent = song;
            tile.addEventListener('click', songTileClicked);
            card.appendChild(tile);
        });
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });
