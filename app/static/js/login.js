// Verify lobby code 
document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault(); // stop default submission
    const submitLogin = document.getElementById("submit_login");
    const lobbyCodeInput = document.getElementById('lobby_code_input').value;
    const username = document.getElementById('username').value;
    const lobbyCode = document.getElementById('lobby_code').value;
    console.log(`Lobby Code Input: ${lobbyCodeInput}, Expected Lobby Code: ${lobbyCode}`);
    console.log(`Username: ${username}`);
    if (lobbyCode.toLowerCase() === lobbyCodeInput.toLowerCase()) {
        addUser(username, lobbyCode);
        submitLogin.disabled = true;
        showAvatarSelection();
    }
});

function addAvatarToUser(avatarId) {
    const username = document.getElementById("username").value;
    console.log(`Selected Avatar ID: ${avatarId} for user: ${username}`);

    fetch("/db/add-avatar-selected", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username,
            avatar_id: avatarId
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.ok) {
                console.log("Avatar saved!");
                console.log("Redirecting to /bingocard");
                window.location.href = "/bingocard";
            } else {
                console.error("Error:", data.error);
            }
        });
}

function addUser(username, lobbyCode) {
    console.log(`Username: ${username}, Lobby Code: ${lobbyCode}`);

    fetch("/db/create-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            username: username,
            lobby_code: lobbyCode
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.ok) {
                console.log("User added!");
            } else {
                console.error("Error:", data.error);
            }
        });
}

function showAvatarSelection() {
    document.getElementById('joinLobbyContainer').hidden = true;
    document.getElementById('avatarSelectionContainer').hidden = false;
    const avatarDiv = document.getElementById('avatarSelection')
    // Fetches avatar images from server
    fetch('/db/GetAvatarImages')
        .then(response => response.json())
        .then(avatars => {
            avatars.forEach(avatar => {
                console.log(avatar);
                const imgElement = document.createElement('img');
                console.log(`URL: ${avatar.filePath}`);
                imgElement.src = avatar.filePath;
                imgElement.id = avatar.id;
                imgElement.className = 'avatarImage';
                imgElement.onclick = function () { addAvatarToUser(avatar.id); };
                avatarDiv.appendChild(imgElement);
            });
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
        });
}