
function loadHtml(data, target) {

	const overlay = document.getElementById(target);
	overlay.innerHTML = data;
	const scripts = overlay.getElementsByTagName("script");

	for (const script of scripts) {
		const newScript = document.createElement("script");
		if (script.src) {		
			newScript.src = script.src;
			newScript.async = true;  
			newScript.onload = script.onload;
		} else 			
			newScript.textContent = script.textContent;		
		document.body.appendChild(newScript); 
	}
}

function setSelfMatchId() {

	const matchsContainer = document.getElementById("matchs");
	const matchElements = [...matchsContainer.children];
		
    matchElements.forEach(match => {		
		if (match.id == window.selfMatchId)
			match.classList.add("self-match");					
		match.onclick = function() {
			fetch(`/match/?matchId=${match.id}&playerId=${window.selfId}`)
			.then(response => {
				if (!response.ok) 
					throw new Error(`Error HTTP! Status: ${response.status}`);		  
				return response.text();
			})
			.then(data => loadHtml(data, "overlay-match"))
			.catch(error => console.log(error))
		};					
	});
}

function movePlayerInMatch(socket, matchElement, match) {
	
	const playersContainer = document.getElementById("players");
	const playerElements = [...playersContainer.children];
	const matchPlayerElements = [...matchElement.children];
	console.log("avant ");
	console.log("match ", match);
	console.log("hou ", match.matchId, match.playerId);
	if (match.players)
	{
		// const data = JSON.parse(match.players);
		console.log("il Y A PLAYERS!!");
		console.log("players ",match.players);
		// console.log(data);
		// console.log("lala ",match.players);
		match.players.forEach(p => console.log("foriche ", p.playerId))
		playerElements.forEach(player => {
			if (
				(player.id == match.playerId || player.id == match.otherId ||
				match.players.some(p => p.playerId == player.id)) && matchPlayerElements.every(p => p.id != player.id)
			)
			{
				// player.remove();
				console.log("JE VAIS APPEND CHILD CAR IL Y A PLAYER!!");
				// matchElement.appendChild(player);	
				const clone = player.cloneNode(true)
				matchElement.appendChild(clone);	
			}		
		});
	}
	else
	{

		console.log("pas de players ", match.players);
		console.log("CHROUCROUTE");
		playerElements.forEach(player => {
			if (player.id == match.playerId || player.id == match.otherId)// ||
				// (match.players.some(p => p.playerId == player.id)))// && matchPlayerElements.every(p => p.id != player.id)))
			{
				// player.remove();
				console.log("JE VAIS APPEND CHILD CAR IL Y A CHROUCROUTE!!");
				const clone = player.cloneNode(true)
				matchElement.appendChild(clone);		
			}		
		});
	}
}

// function movePlayerInMatch(socket) {
	

// }

function addToMatchs(socket, matchsContainer, match) {
  	
	const div = document.createElement("div");
	div.className = "match";
	div.textContent = `match: ${match.matchId}`;
	div.id = match.matchId;
    matchsContainer.appendChild(div);
	movePlayerInMatch(socket, div, match)
}

function removeMatchs(socket, matchs, matchsContainer, matchElements) {

	// for (let i = matchElements.lenght - 1; i >= 0; i--)
	// {
	// 	if (matchs.every(el => el.matchId != matchElements[i].id))	
	// 	{
	// 		if (matchElements[i].id == window.selfMatchId)
	// 		{
	// 			if (window.busyElement)
	// 				window.busyElement.classList.remove("invitation-waiting");
	// 			window.busyElement = null;
	// 			window.selectedElement.classList.remove("invitation-confirmed");
	// 			window.selectedElement = null;
	// 			window.selfMatchId = null;
	// 		}
	// 		matchsContainer.removeChild(matchElements[i]);
	// 		updatePlayers(socket, window.players);
	// 	}		
	// }
	matchElements.slice().reverse().forEach(match => {
		if (matchs.every(el => el.matchId != match.id)) {
			if (match.id == window.selfMatchId)
			{
				if (window.busyElement)
					window.busyElement.classList.remove("invitation-waiting");
				window.busyElement = null;
				window.selectedElement.classList.remove("invitation-confirmed");
				window.selectedElement = null;
				window.selfMatchId = null;
			}
			matchsContainer.removeChild(match);
			updatePlayers(socket, window.players);		
		}
	});
	
	// matchElements.forEach(match => {			
	// 	if (matchs.every(el => el.matchId != match.id))		
	// 	{
	// 		if (match.id == window.selfMatchId)
	// 		{
	// 			if (window.busyElement)
	// 				window.busyElement.classList.remove("invitation-waiting");
	// 			window.busyElement = null;
	// 			window.selectedElement.classList.remove("invitation-confirmed");
	// 			window.selectedElement = null;
	// 			window.selfMatchId = null;
	// 		}
	// 		matchsContainer.removeChild(match);
	// 		updatePlayers(socket, window.players);
	// 	}
	// });
}

function updateMatchs(socket, matchs) {

	console.log("new update " + matchs);
    const matchsContainer = document.getElementById("matchs");
	let matchElements = [...matchsContainer.children];
		
	removeMatchs(socket, matchs, matchsContainer, matchElements);
	matchElements = [...matchsContainer.children];
	matchs.forEach(match => {	
		if (matchElements.every(el => el.id != match.matchId))		
			addToMatchs(socket, matchsContainer, match);
		else
			// movePlayerInMatch(socket, el, match);
			matchElements.forEach(el => {
				if (el.id == match.matchId)
					movePlayerInMatch(socket, el, match);
			});	
	});
	setSelfMatchId();	
}

function sendConfirmation(socket, applicantId, response) {

	console.log(`i will send ${response} to applicant: ${applicantId}`);

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "confirmation",
			response: response,
			applicantId: applicantId
		}));
}

function receiveInvitation(socket, applicantId) {

	console.log("i have had and invitation from: " + applicantId)

	confirm(`you have an invitation from ${applicantId}`)
	? sendConfirmation(socket, applicantId, true)	
	: sendConfirmation(socket, applicantId, false);
}

function invitationCancelled(targetId) {

	console.log(`invitation with ${targetId} is cancelled`);

	alert(`invitation with ${targetId} is cancelled`);
	if (window.busyElement)	
		window.busyElement.classList.remove("invitation-waiting");
	window.busyElement = null;
	if (window.selectedElement)		
		window.selectedElement.classList.remove("invitation-confirmed");	
	window.selectedElement = null;
	window.selfMatchId = null;	
}

function selectedBusy() {

	alert("selectedBusy");
	if (window.busyElement)
		window.busyElement.classList.remove("invitation-waiting");
	window.busyElement = null;
}

function invitationRefused(targetId) {

	alert("refuse from target: "+ targetId + " " + window.busyElement.id);
	if (window.busyElement)
		window.busyElement.classList.remove("invitation-waiting");
	window.busyElement = null;
}

function invitationConfirmed(matchId, targetId) {

	window.selectedElement = document.getElementById("players")
		.querySelector(`[id='${targetId}']`);
	if (window.selectedElement)
	{
		window.busyElement = window.selectedElement
		window.busyElement.classList.remove("invitation-waiting");
		window.selectedElement.classList.add("invitation-confirmed")	
	}
	window.selfMatchId = matchId;
}

function sendPlayerClick(socket, selected)
{
	if (!window.busyElement)
		window.busyElement = selected;
	window.busyElement.classList.add("invitation-waiting")
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "playerClick",
			selectedId: Number(selected.id)
		}));
}

function addPlayerToContainer(socket, container, playerId) {

	const div = document.createElement("div");
	div.className = "user";
	div.textContent = `user: ${playerId}`;
	div.id = playerId;	
	if (playerId === window.selfId)
	{
		div.classList.add("self-player");
		div.onclick = ()=> alert("you can't choose yourself");		
	}
	else	
		div.onclick = () =>	sendPlayerClick(socket, div);	
    container.appendChild(div);
}

function updatePlayers(socket, players) {

    const playersContainer = document.getElementById("players");
	let playerElements = [...playersContainer.children];	

    // playerElements.forEach(player => {	
	// 	if (players.every(el => el.playerId != player.id))		
	// 		playersContainer.removeChild(player);					
	// });
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

function setSelfId(selfId) {

	window.selfId = selfId;	
	document.getElementById("player").innerText = 
		"Je suis le joueur " + window.selfId;	
}

function invitation(socket, data) {

	switch (data.subtype)
	{
		case "back":				
			if (data.response === "selfBusy")
				alert("selfBusy");
			else if (data.response === "selectedBusy")
				selectedBusy();	
			break;
		case "demand":
			receiveInvitation(socket, data.applicantId);
			break;
		case "cancel":
			invitationCancelled(data.targetId);
			break;
		case "confirmation":		
			if (data.response)
				invitationConfirmed(data.matchId, data.targetId)
			else if (data.applicantId == window.selfId)		
				invitationRefused(data.targetId)
			break;	
		default:
			break;	
	}
}

function onTournamentWsMessage(event, socket) {

	console.log("Message reçu :", event.data);
	const data = JSON.parse(event.data);
	
	switch (data.type)
	{
		case "selfAssign":
			setSelfId(data.selfId);
			break;
		case "playerList":
			window.players = data.players;
			updatePlayers(socket, data.players);
			break;
		case "matchList":
			updateMatchs(socket, data.matchs);
			break;
		case "invitation":
			invitation(socket, data)
			break;
		default:				
			break;
	}
}

function initTournamentWs() {
	
    if (window.tournamentSocket)
        window.tournamentSocket.close();
	if (window.rasp == "true")
		window.tournamentSocket = new WebSocket(`wss://${window.pidom}/ws/tournament/`);
	else
		window.tournamentSocket = new WebSocket(`ws://localhost:8000/ws/tournament/${window.user_id}/`);
	window.tournamentSocket.onopen = () => {
		console.log("Connexion Tournament établie 😊");	
	}
	window.tournamentSocket.onclose = () => {
		console.log("Connexion Tournament disconnected 😈");
		// initTournamentWs();	
	};	
	window.tournamentSocket.onmessage = event => onTournamentWsMessage(event, window.tournamentSocket);
}
