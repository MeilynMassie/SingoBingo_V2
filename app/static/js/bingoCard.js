console.log("Bingo Card JS Loaded");

// Fetch JSON data from the server (spotify.py)
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
            tile.textContent = song; // adjust fields as necessary
            card.appendChild(tile);
        });
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });
