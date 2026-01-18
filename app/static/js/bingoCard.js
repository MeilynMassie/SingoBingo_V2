console.log("Bingo Card JS Loaded");

// Fetch JSON data from the server (spotify.py)
fetch('/api/playlists')
    .then(response => response.json())
    .then(playlist => {
        console.log(playlist);
        const ul = document.getElementById('playlist-list');

        playlist.forEach(p => {
            console.log(p);
            const li = document.createElement('li');
            li.textContent = p;
            ul.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });
