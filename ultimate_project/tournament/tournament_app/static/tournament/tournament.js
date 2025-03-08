

function initTournament() {
	
	console.log("INIT TOURNAMENT");
    if (window.tournamentSocket)
        window.tournamentSocket.close();
	if (window.rasp == "true")
		window.tournamentSocket = new WebSocket(
			`wss://${window.pidom}/ws/tournament/tournament/${window.user_id}/`
		);
	else
		window.tournamentSocket = new WebSocket(
			`ws://localhost:8000/ws/tournament/tournament/${window.user_id}/`
		);
	window.tournamentSocket.onopen = () => {
		console.log("Connexion Tournament établie 😊");	
	}
	window.tournamentSocket.onclose = () => {
		console.log("Connexion Tournament disconnected 😈");
	};	
	window.tournamentSocket.onmessage = event =>
		onTournamentMessage(event, window.tournamentSocket);
}

function onTournamentMessage(event, socket) {

	console.log("Message reçu :", event.data);
	const data = JSON.parse(event.data);
	
	switch (data.type)
	{
		case "selfAssign":
			setSelfId(data.selfId);
			break;
		case "playerList":
			// window.players = data.players;
			updatePlayers(socket, data.players);
		// 	break;
		// case "matchList":
		// 	updateMatchs(socket, data.matchs);
		// 	break;
		// case "invitation":
		// 	invitation(socket, data)
		// 	break;
		default:				
			break;
	}
}

function setSelfId(selfId) {

	window.selfId = selfId;	
	document.getElementById("player").innerText = 
		"Je suis le joueur " + window.selfId;	
}

function updatePlayers(socket, players) {

    const playersContainer = document.getElementById("players");
	let playerElements = [...playersContainer.children];	
  
	playerElements.slice().reverse().forEach(player => {	
		if (players.every(el => el.playerId != player.id))		
			playersContainer.removeChild(player);					
	});
	playerElements = [...playersContainer.children];
	players.forEach(player => {	
		if (playerElements.every(el => el.id != player.playerId))		
			addPlayerToContainer(socket, playersContainer, player.playerId);		
	});	
}

function addPlayerToContainer(socket, container, playerId) {

	const div = document.createElement("div");
	div.className = "user";
	div.textContent = `user: ${playerId}`;
	div.id = playerId;	
	if (playerId === window.selfId)
	{
		div.classList.add("self-player");
		// div.onclick = event => {
		// 	event.stopPropagation();
		// 	alert("you can't choose yourself");
		// }		
	}
	// else	
	// 	div.onclick = event =>	sendPlayerClick(socket, event, div);	
    container.appendChild(div);
}