// Button Declarations
document.getElementById('main-menu-container').addEventListener('click', (e) => {
    if (!e.target.matches('button')) return;
    switch (e.target.dataset.action) {
        case 'new':
            hideDiv('main-menu-container');
            showDiv('game-mode-container');
            break;
        case 'options':
            workInProgress()
            break;
        case 'exit':
            window.close();
            break;
    }
});

document.getElementById('game-mode-container').addEventListener('click', (e) => {
    const button = e.target.closest('button');
    if (!button) return;

    switch (button.dataset.action) {
        case 'back':
            window.location.href = '/mainMenu';
            break;
        default:
            playerSelected(button);
            showDiv('playlist-mode-container');
            hideDiv('game-mode-container');
            break;

    }
});

document.getElementById('playlist-mode-container').addEventListener('click', (e) => {
    const button = e.target.closest('button');
    if (!button) return;

    switch (button.dataset.action) {
        case 'back':
            window.location.href = '/mainMenu';
            break;
        default:
            playerSelected(button);
            hideDiv('playlist-mode-container');
            // TODO: Add lobby code to redirect
            window.location.href = '/lobby';

    }
});
