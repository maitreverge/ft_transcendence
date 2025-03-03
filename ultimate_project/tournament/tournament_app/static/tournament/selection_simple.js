
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

function addToMatchs(matchsContainer, match) {
  	
	const div = document.createElement("div");
	div.className = "match";
	div.textContent = `match: ${match.matchId}`;
	div.id = match.matchId;
    matchsContainer.appendChild(div);
}

function updateMatchs(matchs) {

	console.log("new update " + matchs);
    const matchsContainer = document.getElementById("matchs");
	const matchElements = [...matchsContainer.children];
		
    matchElements.forEach(match => {	
		if (matchs.every(el => el.matchId != match.id))		
		{
			if (match.id === window.selfMatchId)
			{
				window.selectedElement.classList.remove("invitation-confirmed");
				window.selectedElement = null;
				window.selfMatchId = null;
			}
			matchsContainer.removeChild(match);
		}
	});
	matchs.forEach(match => {	
		if (matchElements.every(el => el.id != match.matchId))		
			addToMatchs(matchsContainer, match);		
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
	if (window.selectedElement)
		window.selectedElement.classList.remove("invitation-confirmed");
	window.selectedElement = null;
	window.selfMatchId = null;	
}

function invitationConfirmed(matchId, targetId) {

	window.selectedElement = document.getElementById("players")
		.querySelector(`[id='${targetId}']`);
	if (window.selectedElement)
		window.selectedElement.classList.add("invitation-confirmed")	
	window.selfMatchId = matchId;
}

function sendPlayerClick(socket, selected)
{
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "playerClick",
			selectedId: Number(selected.id)
		}));
}

function addToPlayers(socket, playersContainer, player) {
  	
	const div = document.createElement("div");
	div.className = "user";
	div.textContent = `user: ${player.playerId}`;
	div.id = player.playerId;	
	if (player.playerId === window.selfId)
	{
		div.classList.add("self-player");
		div.onclick = ()=> alert("you can't choose yourself");		
	}
	else	
		div.onclick = () =>	sendPlayerClick(socket, div);	
    playersContainer.appendChild(div);
}

function updatePlayers(socket, players) {

    const playersContainer = document.getElementById("players");
	const playerElements = [...playersContainer.children];	

    playerElements.forEach( player => {	
		if (players.every(el => el.playerId != player.id))		
			playersContainer.removeChild(player);					
	});
	players.forEach( player => {	
		if (playerElements.every(el => el.id != player.playerId))		
			addToPlayers(socket, playersContainer, player);		
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
				alert("selectedBusy");	
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
				alert("refuse from target: "+ data.targetId);
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
			updatePlayers(socket, data.players);
			break;
		case "matchList":
			updateMatchs(data.matchs);
			break;
		case "invitation":
			invitation(socket, data)
			break;
		default:				
			break;
	}
}

function initTournamentWs() {
	
	if (window.rasp == "true")
		var socket = new WebSocket(`wss://${window.pidom}/ws/tournament/`);
	else
		var socket = new WebSocket(`ws://localhost:8000/ws/tournament/`);
	socket.onopen = () => {
		console.log("Connexion Tournament établie 😊");	
	}
	socket.onclose = () => {
		console.log("Connexion Tournament disconnected 😈");
		initTournamentWs();	
	};	
	socket.onmessage = event => onTournamentWsMessage(event, socket);
}
