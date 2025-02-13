
function init() {

	if (window.rasp == "true")
		socket = new WebSocket(`wss://${window.pidom}/ws/match/${window.matchId}/`);
	else
	socket = new WebSocket(`ws://localhost:8000/ws/match/${window.matchId}/`);

	socket.onopen = () => {
		console.log("Connexion établie 😊");
	};

	socket.onmessage = (event) => {
	console.log("Message reçu :", event.data);
	};

	document.addEventListener("keydown", function(event) {
		if (event.key === "ArrowUp") {
			event.preventDefault(); // Empêche l'action par défaut
			console.log("Flèche haut pressée !");
			if (socket.readyState === WebSocket.OPEN) { // Vérifie si le WebSocket est bien connecté
				// socket.send("houlala la fleche du haut est presse daller en haut");//
				socket.send(JSON.stringify({action: 'move', direction: 'hight'}));
				console.log("Message envoyé !");
			} else {
				console.log("WebSocket non connecté !");
			}
		}
	});
}

function launch() {
	
	init();
	console.log("le match est lancé hého");
}
