
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
	const waiting = document.getElementById("waiting");
	let waitingState = true;
	socket.onmessage = (event) => {

		const data = JSON.parse(event.data);
		if (waitingState != data.waiting) 
		{
			console.log("Valeur reçue pour waiting:", data.waiting, typeof data.waiting);
			waitingState = data.waiting;
			if (data.waiting == true)
			{
				console.log("REMOVE:", data.waiting, typeof data.waiting);
				waiting.classList.remove("no-waiting");
			}
			else {
				console.log("ADD:", data.waiting, typeof data.waiting);
				waiting.classList.add("no-waiting");
			}
		}
		p1.style.top = data.yp1 + "vh";
		p2.style.top = data.yp2 + "vh";
	};

	setCommands(socket);
}

