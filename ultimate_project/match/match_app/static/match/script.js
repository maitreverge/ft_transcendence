
function setCommands(socket) {

	document.addEventListener("keydown", function(event) {
	
		if (socket.readyState === WebSocket.OPEN)
		{		
			if (event.key === "ArrowUp") 
			{
				event.preventDefault();				
				socket.send(JSON.stringify({action: 'move', dir: 'up'}));				
			} else if (event.key === "ArrowDown") 
			{
				event.preventDefault();				
				socket.send(JSON.stringify({action: 'move', dir: 'down'}));
			}
		} 
		else 
			console.log("WebSocket non connecté !");		
	});
}

function initMatchWs() {

	if (window.rasp == "true")
		socket = new WebSocket(`wss://${window.pidom}/ws/match/${window.matchId}/`);
	else	
		socket = new WebSocket(`ws://localhost:8000/ws/match/${window.matchId}/?playerId=${window.playerId}`);
	
	socket.onopen = () => {
		console.log("Connexion Match établie 😊");
	};
	socket.onclose = () => {
		console.log("Connexion Match disconnected 😈");	
	};

	const p1 = document.getElementById("p1");
	const p2 = document.getElementById("p2");
	socket.onmessage = (event) => {

		const data = JSON.parse(event.data);
		p1.style.top = data.yp1 + "vh";
		p2.style.top = data.yp2 + "vh";
	};

	setCommands(socket);
}

