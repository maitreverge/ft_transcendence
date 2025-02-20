
function init() {

	if (window.rasp == "true")
		socket = new WebSocket(`wss://${window.pidom}/ws/match/${window.matchId}/`);
	else
	{
		console.log(`playerId: ${window.playerId}`)
		socket = new WebSocket(`ws://localhost:8000/ws/match/${window.matchId}/?playerId=${window.playerId}`);
	}

	socket.onopen = () => {
		console.log("Connexion Match établie 😊");
	};
	socket.onclose = () => {
		console.log("Connexion Match disconnected 😈");
	
	};
	const p1 = document.getElementById("p1");
	const p2 = document.getElementById("p2");
	socket.onmessage = (event) => {
		// console.log("Message reçu :", event.data);
		const data = JSON.parse(event.data);
		p1.style.top = data.yp1 + "vh";
		p2.style.top = data.yp2 + "vh";
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

function launch() {
	
	init();
	console.log("le match est lancé hého");
}
