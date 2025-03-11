

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
		case "getPattern":
			getPattern(data.tournamentId);
			break;
			case "linkMatch":
				linkMatch(data.localMatchId, data.matchId);			
			break;
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
	console.log("UPDATE PLAYER");
    const playersContainer = document.getElementById("players");
	let playerElements = [...playersContainer.children];	
	
	const tournamentsContainer = document.getElementById("tournaments");
	let tournamentElements = [...tournamentsContainer.children];

	tournamentElements.slice().reverse().forEach(tournament => {
		const playersCont = tournament.querySelector("#players-cont");
		[...playersCont.children].slice().reverse().forEach(player =>{
			if (players.every(el => el.playerId != player.id))
				player.remove();
		});
	});
		// findPlayer = searchPlayerInTournaments(player.playerId);
		// console.log("find player: ", findPlayer);
		// if (findPlayer)
		// 	findPlayer.remove();
	
	playerElements = [...playersContainer.children];	
	playerElements.slice().reverse().forEach(player => {	
		if (players.every(el => el.playerId != player.id))		
			playersContainer.removeChild(player);									
	});
	playerElements = [...playersContainer.children];
	players.forEach(player => {	
		if (playerElements.every(el => el.id != player.playerId) &&
			!searchPlayerInTournaments(player.playerId)
		)		
			addPlayerToContainer(socket, playersContainer, player.playerId);		
	});	
}

function searchPlayerInTournaments(playerId) {

	const tournamentsContainer = document.getElementById("tournaments");
	let tournamentElements = [...tournamentsContainer.children];

	for (const tournament of tournamentElements) { 
		const playersCont = tournament.querySelector("#players-cont");       
        for (const player of [...playersCont.children]) {
            if (player.id == playerId) {
                return player; 
            }
        }
    }
	return null
}

function addPlayerToContainer(socket, container, playerId) {

	const div = document.createElement("div");
	div.className = "user";
	div.textContent = `user: ${playerId}`;
	div.id = playerId;	
	if (playerId === window.selfId)
	{
		div.classList.add("self-player");
		div.onclick = event => {
			event.stopPropagation();
			quitTournament(socket);
			// tournamentId = Number(event.currentTarget.parentElement.id)
		}		
	}
	// else	
	// 	div.onclick = event =>	sendPlayerClick(socket, event, div);	
    container.appendChild(div);
}

function quitTournament(socket) {
	console.log("quittournement: ");
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "quitTournament"						
		}));
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
		else			
			tournamentElements.forEach(el => {
				if (el.id == tournament.tournamentId)
				{
					const playersCont = el.querySelector("#players-cont");
					movePlayerInTournament(playersCont, tournament);
				}
			});	
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
	div.onclick = () => enterTournament(socket, tournament.tournamentId);
	const overlayPattern = document.createElement("div");
	overlayPattern.id = "overlay-pattern";
	const playersCont = document.createElement("div");
	playersCont.id = "players-cont";
	div.appendChild(playersCont);
	div.appendChild(overlayPattern);
    tournamentsContainer.appendChild(div);
	movePlayerInTournament(playersCont, tournament);
}

function movePlayerInTournament(tournamentElement, tournament) {
	
	const playersContainer = document.getElementById("players");
	const playerElements = [...playersContainer.children];
	const tournamentPlayerElements = [...tournamentElement.children];
	const tournamentsContainer = document.getElementById("tournaments");
	const tournamentElements = [...tournamentsContainer.children];

	if (tournament.players)
	{
		playerElements.slice().reverse().forEach(player => { // je met le joueur ds le bon tournois depuis cont player si ny est pas deja 
			if (tournament.players.some(p => p.playerId == player.id) &&
				tournamentPlayerElements.every(p => p.id != player.id))
			{
				console.log("appendchild to tournois; id:", player.id," ", tournamentElement.id);
				tournamentElement.appendChild(player);
			}			
			else
			{
				tournamentElements.slice().reverse().forEach(tourn => {
					console.log("type: ", typeof(tourn));
					[...tourn.children].slice().reverse().forEach(player2 =>{

						if (tournament.players.some(p => p.playerId == player2.id) &&
						tournamentPlayerElements.every(p => p.id != player2.id))			
						{
							console.log("appendchild to tournois; id:", player2.id," ", tournamentElement.id);
							tournamentElement.appendChild(player2);
						}
					});									
				});
			}						
		});
		if (playerElements.length === 0)
		{
			console.log("player est faux");
			tournamentElements.slice().reverse().forEach(tourn => {
				console.log("type: ", typeof(tourn));
				[...tourn.children].slice().reverse().forEach(player2 =>{
					
					if (tournament.players.some(p => p.playerId == player2.id) &&
					tournamentPlayerElements.every(p => p.id != player2.id))			
				{
					console.log("appendchild to tournois; id:", player2.id," ", tournamentElement.id);
					tournamentElement.appendChild(player2);
				}
			});									
		});
		}


		tournamentPlayerElements.slice().reverse().forEach(player => { // je met le joueur du tournois ds cont player 
			if (tournament.players.every(el => el.playerId != player.id))// && player.id != "overlay-pattern"))
			{
				console.log("appendchild to cont player; id:", player.id, " ", tournamentElement.id);
				playersContainer.appendChild(player);	// ou alors le bon tournois!				
			}			
		});
	}
	else // si le tournois est vide
	{
		tournamentPlayerElements.slice().reverse().forEach(player => {	// je met tous les joueur du tournois ds cont player 					
			// if (player.id != "overlay-pattern")
			// {
				console.log("appendchild to cont player from void; id:", player.id, " ", tournamentElement.id);
				playersContainer.appendChild(player);	// ou alors le bon tournois!				
			// }
				// ou alors le bon tournois!				
		});
	}
}

function newTournament(socket) {

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "newTournament"			
		}));
}

function enterTournament(socket, tournamentId) {
	console.log("entertournement: ", tournamentId);
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "enterTournament",
			tournamentId: tournamentId			
		}));
}

function getPattern(tournamentId) {
	console.log("getpattern: ", tournamentId);
	const tournament = document.getElementById("tournaments").querySelector(
		`[id='${tournamentId}']`
	);
	if (!tournament)
		return;
	const overlay = tournament.querySelector("#overlay-pattern");
	fetch(`/tournament/tournament-pattern/${tournamentId}/`)
	.then(response => {
		if (!response.ok) 
			throw new Error(`Error HTTP! Status: ${response.status}`);		  
		return response.text();
	})
	.then(data => loadHtml(data, overlay))
	.catch(error => console.log(error));		
}

function linkMatch(localMatchId, matchId) {
	console.log("localid: ", localMatchId, " matchid ", matchId);
	const overlay = document.getElementById("overlay-match");
	const localMatch = document.getElementById(localMatchId);
	localMatch.onclick = function() {
		fetch(`/match/?matchId=${matchId}&playerId=${window.selfId}`)
		.then(response => {
			if (!response.ok) 
				throw new Error(`Error HTTP! Status: ${response.status}`);		  
			return response.text();
		})
		.then(data => loadHtml(data, overlay))
		.catch(error => console.log(error))
	};
}

function loadHtml(data, overlay) {
	
	// newDiv = document.createElement("div");
	// newDiv.style.width = "77px";
	// newDiv.style.height = "77px";
	// newDiv.style.color = "blue";
	// newDiv.innerHTML += data;
	// overlay.appendChild(newDiv);
	// overlay.insertAdjacentHTML("beforeend", data); // ✅ Ajoute sans supprimer les événements

	overlay.innerHTML = data;
	// overlay.innerHTML += data;
	// overlay.appendChild(data);
	// overlay.replaceChildren(data);

	const scripts = overlay.getElementsByTagName("script");
	
	for (const script of scripts) {
		
		const newScript = document.createElement("script");
		newScript.className = script.className;
		if (script.src) {	
			newScript.src = script.src + "?t=" + Date.now();
			newScript.async = true;  
			newScript.onload = script.onload;
		} else 			
		newScript.textContent = script.textContent;		
		document.body.appendChild(newScript); 
	}
	const oldScripts = document.querySelectorAll("script.pattern-script");			
	oldScripts.forEach(oldScript => oldScript.remove());	
}