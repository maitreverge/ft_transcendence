
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
	const end = document.getElementById("end");

	let waitingState = "waiting";
	socket.onmessage = (event) => {
		const data = JSON.parse(event.data);
		console.log("Valeur reçue pour waiting:", data.state, typeof data.state, " ", data.winner, typeof data.winner);
		if (data.state == "end")
		{
			console.log("Valeur reçue pour waiting:", data.state, typeof data.state, "", data.winner, typeof data.winner);
			end.innerText += data.winner;
			end.classList.add("end");
		}
		if (waitingState != data.state) 
		{
			console.log("Valeur reçue pour waiting:", data.state, typeof data.state);
			waitingState = data.state;
			if (data.state == "waiting")
			{
				console.log("REMOVE:", data.state, typeof data.state);
				waiting.classList.remove("no-waiting");
			}
			else {
				console.log("ADD:", data.state, typeof data.state);
				waiting.classList.add("no-waiting");
			}
		}
		p1.style.top = data.yp1 + "vh";
		p2.style.top = data.yp2 + "vh";
	};

	setCommands(socket);
}

