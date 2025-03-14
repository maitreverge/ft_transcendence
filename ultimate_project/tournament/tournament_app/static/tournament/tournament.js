
window.players = []

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
			window.tournamentList = data.tournaments; 
			updateTournaments(socket, data.tournaments);
			break;
		case "getPattern":
			getPattern(data.tournamentId);
			break;
			case "linkMatch":
			console.log("case linkmatch");
			linkMatch(data.tournamentId, data.localMatchId, data.matchId, data.p1Id, data.p2Id);			
			break;
		case "matchResult":
			console.log("case matchresult");
			matchResult(socket, data);			
			break;
		case "matchPlayersUpdate":
			console.log("case matchPlayersUpdate");
			matchPlayersUpdate(socket, data);			
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

function updatePlayers(socket, playersUp)
{
	updateWinPlayers(playersUp);
	updatePlayersCont(playersUp);
}

function updateWinPlayers(playersUp)
{
	playersUp.forEach(plyUp => {
		if (window.players.every(el => el.id != plyUp.playerId))
		{
			const newPlayerEl = create_player_element(plyUp.playerId);
			window.players.push(newPlayerEl);
		}	
	});
	window.players = window.players.filter(winPly => {
		if (playersUp.every(el => el.playerId != winPly.id))				
			return winPly.remove(), false
		else
			return true;				
	});
}

function create_player_element(playerId) {
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
		}		
	}
	return div;
}

function quitTournament(socket) {
	
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "quitTournament"						
		}));
}

function updatePlayersCont(playersUp) {

	const playersCont = document.getElementById("players");
	const playerElements = [...playersCont.children];

	playersUp.forEach(plyUp => {
		if (playerElements.every(el => el.id != plyUp.playerId))
		{
			const winPly = window.players.find(el => el.id == plyUp.playerId);
			playersCont.appendChild(winPly);
		}	
	});
}

function updateTournaments(socket, tournamentsUp) {

	const tournamentsCont = document.getElementById("tournaments");
	const tournamentEls = [...tournamentsCont.children];
	let patternExist;
	tournamentsUp.forEach(tourUp => {
		if (tournamentEls.every(el => el.id != tourUp.tournamentId))
		{
			addToTournaments(socket, tournamentsCont, tourUp);
			if (tourUp.matchs.length > 0)			
				patternExist = getPattern(tourUp.tournamentId);			
		}
	});
	tournamentEls.slice().reverse().forEach(tourEl => {
		if (tournamentsUp.every(el => el.tournamentId != tourEl.id)) {
			tournamentsCont.removeChild(tourEl);		
		}
	});
	updateTournamentsPlayers(tournamentsUp);
	if (patternExist)
		updateLinkMatchAndResult(tournamentsUp);	
	else
		setTimeout(()=>{
			updateLinkMatchAndResult(tournamentsUp);
		}, 3000);
}

function updateTournamentsPlayers(tournamentsUp) {

	const tournamentsCont = document.getElementById("tournaments");
	const tournamentEls = [...tournamentsCont.children];

	tournamentsUp.forEach(tourUp => {
		const tourEl = tournamentEls.find(el => el.id == tourUp.tournamentId)
		if (tourEl)
		{
			const playersCont = tourEl.querySelector("#players-cont");
			const playerElements = [...playersCont.children];
			tourUp.players.forEach(plyUp => {
				if (playerElements.every(el => el.id != plyUp.playerId))
				{
					const winplayer = window.players.find(
						el => el.id == plyUp.playerId);
					if (winplayer)
						playersCont.appendChild(winplayer);
				}
			});
		}	
	});
}

function updateLinkMatchAndResult(tournamentsUp) {
	
	tournamentsUp.forEach(tourUp => {
		tourUp.matchs.forEach(matchUp => {
			if (matchUp.linkMatch)			
				linkMatch(matchUp.linkMatch);
			if (matchUp.matchResult)				
				matchResult(matchUp.matchResult);
		});
	});
}
// function updatePlayers2(socket, players) {
// 	console.log("UPDATE PLAYER");
//     const playersContainer = document.getElementById("players");
// 	let playerElements = [...playersContainer.children];	
	
// 	const tournamentsContainer = document.getElementById("tournaments");
// 	let tournamentElements = [...tournamentsContainer.children];

// 	tournamentElements.slice().reverse().forEach(tournament => {
// 		const playersCont = tournament.querySelector("#players-cont");
// 		[...playersCont.children].slice().reverse().forEach(player =>{
// 			if (players.every(el => el.playerId != player.id))
// 			{
// 				window.players = window.players.filter(el => {
// 					if (el.id === player.id)				
// 						return el.remove(), false
// 					else
// 						return true;				
// 				});			
// 			}
// 		});
// 	});
// 		// findPlayer = searchPlayerInTournaments(player.playerId);
// 		// console.log("find player: ", findPlayer);
// 		// if (findPlayer)
// 		// 	findPlayer.remove();
	
// 	playerElements = [...playersContainer.children];	
// 	playerElements.slice().reverse().forEach(player => {	
// 		if (players.every(el => el.playerId != player.id))	
// 		{
// 			window.players = window.players.filter(el => {
// 				if (el.id === player.id)				
// 					return el.remove(), false
// 				else
// 					return true;				
// 			});
// 			// playersContainer.removeChild(player);									
// 		}	
// 	});
// 	playerElements = [...playersContainer.children];
// 	players.forEach(player => {	
// 		if (playerElements.every(el => el.id != player.playerId) &&
// 			!searchPlayerInTournaments(player.playerId)
// 		)		
// 			addPlayerToContainer(socket, playersContainer, player.playerId);		
// 	});	
// }

// function searchPlayerInTournaments(playerId) {

// 	const tournamentsContainer = document.getElementById("tournaments");
// 	let tournamentElements = [...tournamentsContainer.children];

// 	for (const tournament of tournamentElements) { 
// 		const playersCont = tournament.querySelector("#players-cont");       
//         for (const player of [...playersCont.children]) {
//             if (player.id == playerId) {
//                 return player; 
//             }
//         }
//     }
// 	return null
// }

// function addPlayerToContainer(socket, container, playerId) {

// 	const div = document.createElement("div");
// 	div.className = "user";
// 	div.textContent = `user: ${playerId}`;
// 	div.id = playerId;	
// 	if (playerId === window.selfId)
// 	{
// 		div.classList.add("self-player");
// 		div.onclick = event => {
// 			event.stopPropagation();
// 			quitTournament(socket);
// 			// tournamentId = Number(event.currentTarget.parentElement.id)
// 		}		
// 	}
// 	// else	
// 	// 	div.onclick = event =>	sendPlayerClick(socket, event, div);	
//     container.appendChild(div);
// 	window.players.push(div);
// }



// function updateTournaments2(socket, tournamentListUpdate) {
// 	console.log("UPDATE TOURNAMENT");
//     const tournamentsContainer = document.getElementById("tournaments");
// 	let tournamentElements = [...tournamentsContainer.children];
		
// 	removeTournaments(
// 		socket, tournamentListUpdate, tournamentsContainer, tournamentElements);

// 	tournamentListUpdate.forEach(tourUp => {

// 		if (tournamentElements.every(el => el.id != tourUp.tournamentId))		
// 			addToTournaments(socket, tournamentsContainer, tourUp);

// 		// tournamentElements = [...tournamentsContainer.children];		
// 		// tournamentElements.forEach(tourEl => {
// 		// 	if (tourEl.id == tourUp.tournamentId)
// 		// 	{
// 		// 		const playersCont = tourEl.querySelector("#players-cont");			
// 				movePlayersInTournaments(tournamentsContainer, tourUp);
// 		// 	}
// 		// });
		
// 		if (tourUp.matchs.length > 0)
// 		{
// 			getPattern(tourUp.tournamentId);
// 			setTimeout(()=>{
// 				tourUp.matchs.forEach(match => {
// 					if (match.linkMatch)
// 					{
// 						console.log("MATCHSSS ", match)				
// 						lk = match.linkMatch;
// 						linkMatch(lk.tournamentId, lk.localMatchId, lk.matchId, lk.p1Id, lk.p2Id);
// 					}
// 					if (match.matchResult)
// 					{
// 						console.log("match Reuslt EXISTE mouquate");
// 						// mres = match.matchResult;
// 						matchResult(match.matchResult);			
		
// 					}
// 					else {
// 						console.log("match Reuslt nexiste pas mouquate");
// 					}
// 				});
// 			}, 3000);		
// 		}	
// 	});
// 	// setSelfMatchId();	
// }

// function removeTournaments(socket, tournaments, tournamentsContainer, tournamentElements) {

// 	// const playersContainer = document.getElementById("players");

// 	tournamentElements.slice().reverse().forEach(tournament => {
// 		if (tournaments.every(el => el.tournamentId != tournament.id)) {
// 			// if (match.id == window.selfMatchId)
// 			// {
// 			// 	if (window.busyElement)
// 			// 		window.busyElement.classList.remove("invitation-waiting");
// 			// 	window.busyElement = null;
// 			// 	window.selectedElement.classList.remove("invitation-confirmed");
// 			// 	window.selectedElement = null;
// 			// 	window.selfMatchId = null;
// 			// }
// 			// [...match.children].forEach(player => {
// 			// 	playersContainer.appendChild(player);
// 			// });
// 			tournamentsContainer.removeChild(tournament);		
// 		}
// 	});
// }

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
}

// function movePlayersInTournaments(tournamentsContainer, tourUp) {
// 	tournamentElements = [...tournamentsContainer.children];		
// 	tournamentElements.forEach(tourEl => {
// 		if (tourEl.id == tourUp.tournamentId)
// 		{
// 			const playersCont = tourEl.querySelector("#players-cont");			
// 			const playerElements = [...playersCont.children];
// 			tourUp.players.forEach(plyUp => {
// 				if (playerElements.every(el => el.id != plyUp.playerId))
// 				{
// 					const winplayer = window.players.find(el => el.id == plyUp.playerId);
// 					if (winplayer)
// 						playersCont.appendChild(winplayer);
// 				}
// 			});	
// 		}
// 	});

// }

// function movePlayerInTournament2(tournamentElement, tournament) {
	
// 	const playersContainer = document.getElementById("players");
// 	const playerElements = [...playersContainer.children];
// 	const tournamentPlayerElements = [...tournamentElement.children];
// 	const tournamentsContainer = document.getElementById("tournaments");
// 	const tournamentElements = [...tournamentsContainer.children];

// 	if (tournament.players)
// 	{
// 		playerElements.slice().reverse().forEach(player => { // je met le joueur ds le bon tournois depuis cont player si ny est pas deja 
// 			if (tournament.players.some(p => p.playerId == player.id) &&
// 				tournamentPlayerElements.every(p => p.id != player.id))
// 			{
// 				console.log("appendchild to tournois; id:", player.id," ", tournamentElement.id);
// 				tournamentElement.appendChild(player);
// 			}			
// 			else
// 			{
				
// 				tournamentElements.slice().reverse().forEach(tourn => {
// 					const playersCont = tourn.querySelector("#players-cont");
// 					console.log("type: ", typeof(tourn));
// 					[...playersCont.children].slice().reverse().forEach(player2 =>{

// 						if (tournament.players.some(p => p.playerId == player2.id) &&
// 						tournamentPlayerElements.every(p => p.id != player2.id))			
// 						{
// 							console.log("appendchild to tournois; id:", player2.id," ", tournamentElement.id);
// 							tournamentElement.appendChild(player2);
// 						}
// 					});									
// 				});
// 			}						
// 		});
// 		if (playerElements.length === 0)
// 		{
// 			console.log("player est faux");
// 			tournamentElements.slice().reverse().forEach(tourn => {
// 				console.log("type: ", typeof(tourn));
// 				const playersCont = tourn.querySelector("#players-cont");
// 				[...playersCont.children].slice().reverse().forEach(player2 =>{
					
// 					if (tournament.players.some(p => p.playerId == player2.id) &&
// 					tournamentPlayerElements.every(p => p.id != player2.id))			
// 				{
// 					console.log("appendchild to tournois; id:", player2.id," ", tournamentElement.id);
// 					tournamentElement.appendChild(player2);
// 				}
// 			});									
// 		});
// 		}


// 		tournamentPlayerElements.slice().reverse().forEach(player => { // je met le joueur du tournois ds cont player 
// 			if (tournament.players.every(el => el.playerId != player.id))// && player.id != "overlay-pattern"))
// 			{
// 				console.log("appendchild to cont player; id:", player.id, " ", tournamentElement.id);
// 				playersContainer.appendChild(player);	// ou alors le bon tournois!				
// 			}			
// 		});
// 	}
// 	else // si le tournois est vide
// 	{
// 		tournamentPlayerElements.slice().reverse().forEach(player => {	// je met tous les joueur du tournois ds cont player 					
// 			// if (player.id != "overlay-pattern")
// 			// {
// 				console.log("appendchild to cont player from void; id:", player.id, " ", tournamentElement.id);
// 				playersContainer.appendChild(player);	// ou alors le bon tournois!				
// 			// }
// 				// ou alors le bon tournois!				
// 		});
// 	}
// }

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
		return false;
	const overlay = tournament.querySelector("#overlay-pattern");
	if (overlay.innerHTML.trim() !== "")
		return false;
	fetch(`/tournament/tournament-pattern/${tournamentId}/`)
	.then(response => {
		if (!response.ok) 
			throw new Error(`Error HTTP! Status: ${response.status}`);		  
		return response.text();
	})
	.then(data => loadHtml(data, overlay))
	.catch(error => console.log(error));
	return true;		
}

function linkMatch(lk) {
	console.log("LINK MATCH tournId ", lk.tournamentId, " localid: ", lk.localMatchId, " matchid ", lk.matchId, " p1 ", lk.p1Id, " p2 ", lk.p2Id, " selfmatchid ", window.selfMatchId, " selfid ", window.selfId);
	const tournament = document.getElementById("tournaments").querySelector(
		`[id='${lk.tournamentId}']`
	);
	if (!tournament)
		return;
	const overlay = tournament.querySelector("#overlay-match");
	// const matchs_cont = tournament.querySelector("#matchs-cont");
	const localMatch = tournament.querySelector(`#${lk.localMatchId}`);

	const localP1 = localMatch.querySelector(`#pl1`);
	const localP2 = localMatch.querySelector(`#pl2`);
	localP1.innerText = lk.p1Id;
	localP2.innerText = lk.p2Id;
	// const overlay = document.getElementById("overlay-match");
	// const localMatch = document.getElementById(localMatchId);
	if (window.selfId == lk.p1Id || window.selfId == lk.p2Id)
	{
		window.selfMatchId = lk.matchId;
		localMatch.classList.add("next-match");
	}

	localMatch.onclick = function() {
		fetch(`/match/?matchId=${lk.matchId}&playerId=${window.selfId}`)
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
	
	for (const script of scripts) 
	{		
		const newScript = document.createElement("script");
		newScript.className = script.className;
		if (script.src)
		{	
			newScript.src = script.src + "?t=" + Date.now();
			newScript.async = true;  
			newScript.onload = script.onload;
		} 
		else 			
			newScript.textContent = script.textContent;		
		document.body.appendChild(newScript); 
	}
	const oldScripts = document.querySelectorAll("script.pattern-script");			
	oldScripts.forEach(oldScript => oldScript.remove());	
}

function matchResult(socket, rsl) {
	console.log("MATCH RESULT tournId ", rsl.tournamentId, " localid: ", rsl.localMatchId, " matchid ", rsl.matchId, " winner ", rsl.winnerId, " looser ", rsl.looserId, " selfmatchid ", window.selfMatchId, " selfid ", window.selfId);

	const tournament = document.getElementById("tournaments").querySelector(
		`[id='${rsl.tournamentId}']`
	);
	if (!tournament)
		return;
	const overlay = tournament.querySelector("#overlay-match");
	const localMatch = tournament.querySelector(`#${rsl.localMatchId}`);
	const localP1 = localMatch.querySelector(`#pl1`);
	const localP2 = localMatch.querySelector(`#pl2`);
	if (rsl.winnerId === rsl.p1Id)
	{
		localP1.classList.add("winner");
		localP2.classList.add("looser");
	}
	else if (rsl.winnerId === rsl.p2Id)
	{
		localP2.classList.add("winner");
		localP1.classList.add("looser");
	}
	
	// const playersCont = tournament.querySelector("#players-cont");
	// const winplayer1 = window.players.find(el => el.id == rsl.winnerId);
	// const winplayer2 = window.players.find(el => el.id == rsl.looserId);
	// // const localMatch = tournament.querySelector(`#${plys.localMatchId}`);
	// // const localP1 = localMatch.querySelector(`#pl1`);
	// // const localP2 = localMatch.querySelector(`#pl2`);
	// const specCont = localMatch.querySelector(`#spec`);
	// const specs = [...specCont.children]
	// const playersContainer = document.getElementById("players");
	// if (winplayer1)
	// 	playersCont.appendChild(winplayer1);
	// if (winplayer2)
	// playersCont.appendChild(winplayer2);
	// specs.forEach(el => {
	// 	playersCont.appendChild(el)
	// });

	// localP1.innerText = p1Id;
	// localP2.innerText = p2Id;
	// overlay.innerHTML = "";
	// localMatch.innerText = winnerId
}

function matchPlayersUpdate(socket, plys) {
	console.log("plys: ", plys);
	

	const tournament = document.getElementById("tournaments").querySelector(
		`[id='${plys.tournamentId}']`
	);
	if (!tournament)
		return;

	const localMatch = tournament.querySelector(`#${plys.localMatchId}`);
	const localP1 = localMatch.querySelector(`#pl1`);
	const localP2 = localMatch.querySelector(`#pl2`);
	const specCont = localMatch.querySelector(`#spec`);
	const specs = [...specCont.children]
	const playersContainer = document.getElementById("players");
	plys.players.forEach(player => {

		if (specs.every(el => el.id != player.playerId))
		{
			const winplayer = window.players.find(el => el.id == player.playerId)
			if (plys.p1Id == winplayer.id)
				localP1.appendChild(winplayer);
			else if (plys.p2Id == winplayer.id)
				localP2.appendChild(winplayer);
			else
				specCont.appendChild(winplayer);
		}


		// specs.forEach(spec => {
		// 	if (plys.every(el => el.playerId != spec.id))
		// 		playersContainer.appendChild(spec);
		// 	if (specs.every(el => el.id != player.playerId))
		// 		specCont.appendChild(player);
		// });
	});
}

