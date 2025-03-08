

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
			break;
		case "tournamentList":
			updateTournaments(socket, data.tournaments);
			break;
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

function updateTournaments(socket, tournaments) {

    const tournamentsContainer = document.getElementById("tournaments");
	let tournamentElements = [...tournamentsContainer.children];
		
	removeTournaments(
		socket, tournaments, tournamentsContainer, tournamentElements);
	tournamentElements = [...tournamentsContainer.children];
	tournaments.forEach(tournament => {	
		if (tournamentElements.every(el => el.id != tournament.tournamentId))		
			addToTournaments(socket, tournamentsContainer, tournament);
		// else			
		// 	matchElements.forEach(el => {
		// 		if (el.id == match.matchId)
		// 			movePlayerInMatch(socket, el, match);
		// 	});	
	});
	// setSelfMatchId();	
}

function removeTournaments(socket, tournaments, tournamentsContainer, tournamentElements) {

	// const playersContainer = document.getElementById("players");

	tournamentElements.slice().reverse().forEach(tournament => {
		if (tournaments.every(el => el.tournamentId != tournament.id)) {
			// if (match.id == window.selfMatchId)
			// {
			// 	if (window.busyElement)
			// 		window.busyElement.classList.remove("invitation-waiting");
			// 	window.busyElement = null;
			// 	window.selectedElement.classList.remove("invitation-confirmed");
			// 	window.selectedElement = null;
			// 	window.selfMatchId = null;
			// }
			// [...match.children].forEach(player => {
			// 	playersContainer.appendChild(player);
			// });
			tournamentsContainer.removeChild(tournament);		
		}
	});
}

function addToTournaments(socket, tournamentsContainer, tournament) {
  	
	const div = document.createElement("div");
	div.className = "tournament";
	div.textContent = `tournament: ${tournament.tournamentId}`;
	div.id = tournament.tournamentId;
    tournamentsContainer.appendChild(div);
	// movePlayerInMatch(socket, div, match)
}

function newTournament(socket) {

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "newTournament",
			applicantId: Number(window.selfId)
		}));
}

