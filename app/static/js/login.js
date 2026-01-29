// Verify lobby code 
document.getElementById("login-form").addEventListener("submit", function (e) {
    e.preventDefault(); // stop default submission
    const submitLogin = document.getElementById("submit-login");
    const lobbyCodeInput = document.getElementById('lobby-code-input').value;
    const username = document.getElementById('username').value;
    const lobbyCode = document.getElementById('lobby-code').value;
    console.log(`Lobby Code Input: ${lobbyCodeInput}, Expected Lobby Code: ${lobbyCode}`);
    console.log(`Username: ${username}`);
    if (lobbyCode.toLowerCase() === lobbyCodeInput.toLowerCase()) {
        addUser(username, lobbyCode);
        submitLogin.disabled = true;
        showAvatarSelection();
    }
});


function addUser(username, lobbyCode) {
    console.log(`Username: ${username}, Lobby Code: ${lobbyCode}`);

    fetch("/db/createUser", {
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


function addAvatarToUser(avatarId) {
    const username = document.getElementById("username").value;
    console.log(`Selected Avatar ID: ${avatarId} for user: ${username}`);

    fetch("/db/addAvatarSelected", {
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
                console.log("Redirecting to /bingoCard");
                window.location.href = "/bingoCard";
            } else {
                console.error("Error:", data.error);
            }
        });
}


function showAvatarSelection() {
    document.getElementById('join-lobby-container').hidden = true;
    const avatarDiv = document.getElementById('avatar-selection-container')
    avatarDiv.hidden = false;
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
                imgElement.className = 'avatar-image';
                imgElement.addEventListener('click', () => {
                    const username = document.getElementById("username").value;
                    console.log(`Selected Avatar ID: ${avatar.id} for user: ${username}`);

                    fetch("/db/addAvatarSelected", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            username: username,
                            avatar_id: avatar.id
                        })
                    })
                        .then(res => res.json())
                        .then(data => {
                            if (data.ok) {
                                console.log("Avatar saved!");
                                console.log("Redirecting to /bingoCard");
                                window.location.href = "/bingoCard";
                            } else {
                                console.error("Error:", data.error);
                            }
                        });
                });
                avatarDiv.appendChild(imgElement);
            });
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
        });
}