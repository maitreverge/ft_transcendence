
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
			if (match.id == window.selfMatchId)
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

function sendMatchId(socket, matchId, selectedId) {

	console.log("i will send matchId: " + matchId + " to selected: "
		+ selectedId);

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			matchId: matchId,
			selectedId: selectedId
		}));
}

function receiveMatchId(matchId) {

	console.log("i have had and matchId: " + matchId)

	window.selfMatchId = matchId;
	setSelfMatchId();
}

function askMatchId(socket, selectedId) {

	fetch(
		"/tournament/start-match?" +
		`selfId=${window.selfId}&` +
		`selectedId=${selectedId}`
	)
		.then(response => {
			if (!response.ok) 
				throw new Error(`Error HTTP! Status: ${response.status}`);		  
			return response.json();
		})
		.then(data => {		
			window.selfMatchId = data.matchId;
			setSelfMatchId();
			sendMatchId(socket, data.matchId, selectedId);
		})
		.catch(error => console.log(error))	
}

function receiveConfirmation(socket, selectedId, response) {

	console.log("i have had and confirmation from: " + selectedId
		+ ", the answer is :" + response);
	
	const selectedElement = document.getElementById("players")
		.querySelector(`[id='${selectedId}']`); 
	if (selectedElement)
	{
		if (response === "yes")
		{
			window.selectedElement = selectedElement;
			selectedElement.classList.remove("invitation-waiting");
			selectedElement.classList.add("invitation-confirmed");
			askMatchId(socket, selectedId);		
		}
		else
		{
			selectedElement.classList.remove("invitation-waiting");
			selectedElement.classList.remove("invitation-confirmed");
			alert(`${selectedId} says: fuck you`);
		}
	}
}
//!
function sendConfirmation(socket, applicantId, response) {

	console.log(`i will send ${response} to applicant: ${applicantId}`);

	if (response === "yes") 
	{		
		const applicantElement = document.getElementById("players")
			.querySelector(`[id='${applicantId}']`);
		if (applicantElement)
		{
			window.selectedElement = applicantElement;
			applicantElement.classList.add("invitation-confirmed");	
		}
	}	
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
		? sendConfirmation(socket, applicantId, "yes")	
		: sendConfirmation(socket, applicantId, "no");
}
//!
function invitationCancelled(applicantId) {

	console.log("invitation is cancelled from: " + applicantId);

	window.selectedElement.classList.remove("invitation-confirmed");
	fetch(`/tournament/stop-match/${window.selfId}/${window.selfMatchId}/`)
	.then(response => {
		if (!response.ok) 
			throw new Error(`Error HTTP! Status: ${response.status}`);		  
		return response.text();
	})
	.then(data => console.log(data))
	.catch(error => console.log(error))
}
//!
function cancelInvitation(socket, selected) {
	
	console.log("i will cancel invitation to selected: " + selected.id);

	selected.classList.remove("invitation-confirmed");	

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "cancelInvitation",
			selectedId: Number(selected.id)
		}));
}

function sendInvitation(socket, selected) {
	
	console.log("i will send invitation to selected: " + selected.id);
	selected.classList.add("invitation-waiting");

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({
			type: "invitation",
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
		div.onclick = function() {
			alert("you can't choose yourself");
		};
	}
	else
	{
		div.onclick = function() {			
			!window.selectedElement
				? sendInvitation(socket, this)
				: cancelInvitation(socket, this);				
		};
	}
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
			receiveInvitation(socket, data.playerId);
			break;
		case "cancelInvitation":
			invitationCancelled(data.playerId);
			break;
		case "confirmation":
			receiveConfirmation(socket,	data.selectedId, data.response);
			break;
		default:
			if (data.matchId) 
				receiveMatchId(data.matchId);			
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
