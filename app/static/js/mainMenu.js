let modeSelected = [];

document.addEventListener('DOMContentLoaded', () => {
    const mainMenu = document.getElementById('main-menu-container');
    if (mainMenu) {
        mainMenu.addEventListener('click', (e) => {
            if (!e.target.matches('button')) return;

            switch (e.target.dataset.action) {
                case 'new':
                    hideDiv('main-menu-container');
                    showDiv('game-mode-container');
                    break;
                case 'options':
                    workInProgress();
                    break;
                case 'exit':
                    window.close();
                    break;
            }
        });
    }

    const gameMode = document.getElementById('game-mode-container');
    if (gameMode) {
        gameMode.addEventListener('click', (e) => {
            const button = e.target.closest('button');
            if (!button) return;

            switch (button.dataset.action) {
                case 'back':
                    window.location.href = '/mainMenu';
                    break;
                default:
                    modeSelected.push(playerSelected(button));
                    showDiv('playlist-mode-container');
                    hideDiv('game-mode-container');
                    break;
            }
        });
    }

    const playlistMode = document.getElementById('playlist-mode-container');
    if (playlistMode) {
        playlistMode.addEventListener('click', (e) => {
            const button = e.target.closest('button');
            if (!button) return;

            switch (button.dataset.action) {
                case 'back':
                    window.location.href = '/mainMenu';
                    break;
                default:
                    modeSelected.push(playerSelected(button));
                    addLobby(modeSelected)
            }
        });
    }
});

// Fetch user input and make db call to create lobby code
function addLobby(modeSelected) {
    console.log(`player_mode: ${modeSelected[0]},
            playlist_mode: ${modeSelected[1]}`)
    fetch("/db/createLobby", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            player_mode: modeSelected[0],
            playlist_mode: modeSelected[1]
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.ok) {
                console.log("Lobby saved!");
                console.log(`Redirecting to /lobby/${data.lobby_code}`)
                window.location.href = `/lobby/${data.lobby_code}`;
            } else {
                console.error("Error:", data.error);
            }
        });
}