
// document.getElementById("new-match").addEventListener("click", function(event) {
// 	event.preventDefault();
// 	console.log("ta bien clique man");
// 	fetch('http://localhost:8000/match/new-match/')
// 		.then(response => response.json())
// 		.then(data => console.log(data))
// 		.catch(error => console.error(error))
// });
function updateUsersList(players) {
    const usersContainer = document.getElementById("users");
    // Efface ce qui existe déjà
    usersContainer.innerHTML = "";

    // Pour chaque user de la liste côté client
    players.forEach(user => {
      const div = document.createElement("div");
      div.className = "user";
      div.textContent = `user: ${user.playerId}`;
      
      // Onclick personnalisable
      div.onclick = function() {
        console.log(`my choice: ${user.playerId}`);
        window.userIdChosen = user.playerId;
        this.style.backgroundColor = 'red';
      };
      
      usersContainer.appendChild(div);
    });
}

function initWs() {
	console.log("initWs");
	if (window.rasp == "true")
		socket = new WebSocket(`wss://${window.pidom}/ws/match/${window.matchId}/`);//!
	else
		socket = new WebSocket(`ws://localhost:8000/ws/tournament/`);

	socket.onopen = () => {
		console.log("Connexion établie 😊");
	};

	// const p1 = document.getElementById("p1");
	// const p2 = document.getElementById("p2");
	socket.onmessage = (event) => {
		console.log("Message reçu :", event.data);
		const data = JSON.parse(event.data);
		updateUsersList(data);
		// p1.style.top = data.yp1 + "vh";
		// p2.style.top = data.yp2 + "vh";
	};

	document.addEventListener("keydown", function(event) {
		
		if (socket.readyState === WebSocket.OPEN) { // Vérifie si le WebSocket est bien connecté
				// socket.send("houlala la fleche du haut est presse daller en haut");//
			if (event.key === "ArrowUp") {
				event.preventDefault(); // Empêche l'action par défaut
				// console.log("Flèche haut pressée !");
				socket.send(JSON.stringify({action: 'move', dir: 'up'}));				
			} else if (event.key === "ArrowDown") {
				event.preventDefault();
				// console.log("Flèche bas pressée !");
				socket.send(JSON.stringify({action: 'move', dir: 'down'}));
			}
		} else {
			console.log("WebSocket non connecté !");
		}
	});
}

