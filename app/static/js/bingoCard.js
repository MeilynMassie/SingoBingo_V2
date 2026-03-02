loadAvatar();
loadBingoCard();

// TODO: NEXT FRFR - Add visuals for if the guess is wrong
async function verifyClickedTile(event) {
    const clickedTile = event.target;
    const lobbyCode = document.getElementById('lobby-code').value;
    console.log("Clicked tile ID: ", clickedTile.id);
    if (clickedTile.id === 'free-space') {
        clickedTile.classList.add('marked');
        return;
    }
    try {
        const response = await fetch(`/spotify/playlists/verifySong?lobby_code=${lobbyCode}&song_title=${clickedTile.id}`);
        res = await response.json();
        console.log("Response from server: ", res);
        if (res.ok) { clickedTile.classList.add('marked') };
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

async function loadAvatar() {
    const username = document.getElementById("username").value;
    if (!username) {
        console.error("Username not found");
        return;
    }
    console.log("Loading avatar for username:", username);
    try {
        const response = await fetch(`/db/getPlayerAvatar?username=${encodeURIComponent(username)}`);
        const data = await response.json();
        console.log("Avatar response data:", data);
        if (data.ok && data.avatar_file_name) {
            const avatarDisplay = document.getElementById('avatar-display');
            avatarDisplay.className = 'avatar-display';
            avatarDisplay.innerHTML = `<img src="/static/imgs/avatars/${data.avatar_file_name}" alt="Player Avatar" class="avatar-image">`;
        } else {
            console.error("Failed to load player avatar:", data.error);
        }
    } catch (error) {
        console.error("Error loading player avatar:", error);
    }
}