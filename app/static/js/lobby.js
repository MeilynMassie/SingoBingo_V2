const lobbyCode = document.getElementById('lobby-code').value;
console.log(lobbyCode);
document.getElementById('readyToStartGame').addEventListener('click', () => {
    console.log(`Redirecting to /startGame/${lobbyCode}`)
    window.location.href = `/startGame/${lobbyCode}`;
})