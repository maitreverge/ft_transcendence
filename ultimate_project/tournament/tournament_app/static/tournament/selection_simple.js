
function sendInvitation(socket, choosenId) {
	
	console.log("i will send invitation to choosenId: " + choosenId);

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({type: "invitation", choosenId: choosenId}))
}

function sendConfirmation(socket, applicantId, response) {

	console.log(`i will send ${response} to applicant: ${applicantId}`);

	if (response === "yes") 
	{
		const applicantElement = document.getElementById(applicantId);
		applicantElement.classList.add("invitation-confirmed");	
		applicantElement.confirmed = 'yes';
	}
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({type: "confirmation", response: response, applicantId: applicantId}))
}

function cancelInvitation(socket, choosenId) {
	
	console.log("i will cancel invitation to choosenId: " + choosenId);
	
	const choosenElement = document.getElementById(choosenId);
	choosenElement.classList.remove("invitation-confirmed");
	choosenElement.confirmed = 'no';

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({type: "cancelInvitation", choosenId: choosenId}))
}

function invitationCancelled(applicantId) {

	console.log("invitation is cancelled from: " + applicantId);

	const applicantElement = document.getElementById(applicantId);
	applicantElement.classList.remove("invitation-confirmed");
	applicantElement.confirmed = 'no';
}

function addToPlayers(socket, usersContainer, player) {
  	
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

			console.log("user confirmed: " + div.confirmed + " id: " + div.id);
			if (typeof div.confirmed === 'undefined' || div.confirmed === 'no')
			{
				console.log(`my choice: ${player.playerId}`);
				window.select = player.playerId;//!
				this.classList.add("invitation-waiting");				
				sendInvitation(socket, window.select);
			}
			else				
				cancelInvitation(socket, player.playerId);				
		};
	}
    usersContainer.appendChild(div);
}

function addToMatchs(socket, matchsContainer, match) {
  	
	const div = document.createElement("div");
	div.className = "match";
	div.textContent = `match: ${match.matchId}`;
	div.id = match.matchId;
	// if (match.matchId === window.selfId)
	// {
	// 	div.classList.add("self-match");
	// 	div.onclick = function() {
	// 		alert("you can't choose yourself");
	// 	};
	// }
	// else
	// {
	// 	div.onclick = function() {

	// 		console.log("user confirmed: " + div.confirmed + " id: " + div.id);
	// 		if (typeof div.confirmed === 'undefined' || div.confirmed === 'no')
	// 		{
	// 			console.log(`my choice: ${match.matchId}`);
	// 			window.select = match.matchId;//!
	// 			this.classList.add("invitation-waiting");				
	// 			sendInvitation(socket, window.select);
	// 		}
	// 		else				
	// 			cancelInvitation(socket, match.matchId);				
	// 	};
	// }
    matchsContainer.appendChild(div);
}

function updatePlayers(socket, players) {

    const usersContainer = document.getElementById("users");
	userElements = [...usersContainer.children];
		
    userElements.forEach( player => {	
		if (players.every(el => el.playerId != player.id))		
			usersContainer.removeChild(player);					
	});
	players.forEach( player => {	
		if (userElements.every(el => el.id != player.playerId))		
			addToPlayers(socket, usersContainer, player);		
	});	
}

function updateMatchs(socket, matchs) {
	console.log("new udate " + matchs);
    const matchsContainer = document.getElementById("matchs");
	matchElements = [...matchsContainer.children];
		
    matchElements.forEach( match => {	
		if (matchs.every(el => el.matchId != match.id))		
			matchsContainer.removeChild(match);
		// if (match.id == window.selfMatchId)
		// {
		// 	console.log("in uupdate selfmatchid: " + window.selfMatchId);
		// 	match.classList.add("self-match");					
		// }
	});
	matchs.forEach( match => {	
		if (matchElements.every(el => el.id != match.matchId))		
			addToMatchs(socket, matchsContainer, match);		
	});	
}

function setSelfId(selfId) {
	window.selfId = selfId;
	document.getElementById("player").innerText = 
	"Je suis le joueur " + window.selfId;
	
  	window.select = null;
}

function setSelfMatchId()
{
	const matchsContainer = document.getElementById("matchs");
	matchElements = [...matchsContainer.children];
		
    matchElements.forEach( match => {		
		if (match.id == window.selfMatchId)
		{
			console.log("in uupdate selfmatchid: " + window.selfMatchId);
			match.classList.add("self-match");
			match.onclick = function() {
				fetch(`/match/?matchId=${window.selfMatchId}&playerId=${window.selfId}`)
				.then( response => {
					if (!response.ok) 
						throw new Error(`Erreur HTTP! Statut: ${response.status}`);		  
					return response.text();
				})
				.then( data => {
					overlayMatch = document.getElementById("overlay-match");
					overlayMatch.innerHTML = data;
					let scripts = overlayMatch.getElementsByTagName("script");
					for (let script of scripts) {
                        let newScript = document.createElement("script");
                        if (script.src) {
                            // Si c'est un script externe, on le recharge
                            newScript.src = script.src;
                            newScript.async = true;  // Permet un chargement non bloquant
							newScript.onload = script.onload;
                        } else {
                            // Si c'est un script inline, on copie son contenu
                            newScript.textContent = script.textContent;
                        }
                        document.body.appendChild(newScript); // Exécuter le script
                    }

					// let scripts = overlayMatch.getElementsByTagName("script");
                    // for (let script of scripts) {
                    //     let newScript = document.createElement("script");
                    //     newScript.textContent = script.textContent; // Recharger le script
                    //     document.body.appendChild(newScript); // Exécuter le script
                    // }
					// console.log("data:" + data.matchId);
					// window.selfMatchId = data.matchId;
					// setSelfMatchId();
					// console.log("in ask selfmatchid: " + window.selfMatchId);
					// sendMatchId(socket, data.matchId, choosenId);
				})
				.catch( error => console.log(error))
			};					
		}
	});
}

function receiveInvitation(socket, applicantId) {

	console.log("i have had and invitation from: " + applicantId)

	if (confirm(`you have an invitation from ${applicantId}`))
		sendConfirmation(socket, applicantId, "yes");
	else
		sendConfirmation(socket, applicantId, "no");
}

function sendMatchId(socket, matchId, choosenId) {

	console.log("i will send matchId: " + matchId + " to choosen: " + choosenId);

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({matchId: matchId, choosenId: choosenId}))
}

function initSelfMatch() {
	const matchsContainer = document.getElementsById("matchs");
	matchElements = [...matchsContainer.children];
}

function askMatchId(socket, choosenId) {

	// document.body.addEventListener("htmx:configRequest", function(evt) {

	// 	if (evt.detail.elt.id === "startMatchButton" && window.select !== null){
	// 		evt.detail.path = "/tournament/start-match/?selfid=" + window.selfId + "&select=" + choosenId;
	// 	}
	// });

	fetch(`/tournament/start-match/?selfid=${window.selfId}&select=${choosenId}`)
		.then( response => {
			if (!response.ok) 
				throw new Error(`Erreur HTTP! Statut: ${response.status}`);		  
			return response.json();
		})
		.then( data => {
			console.log("data:" + data.matchId);
			window.selfMatchId = data.matchId;
			setSelfMatchId();
			console.log("in ask selfmatchid: " + window.selfMatchId);
			sendMatchId(socket, data.matchId, choosenId);
		})
		.catch( error => console.log(error))	
}

function receiveConfirmation(socket, choosenId, response) {

	console.log("i have had and confirmation from: " + choosenId
		+ ", the answer is :" + response);
	
	const choosenElement = document.getElementById(choosenId); 
	if (response === "yes")
	{
		choosenElement.classList.remove("invitation-waiting");
		choosenElement.classList.add("invitation-confirmed");
		choosenElement.confirmed = "yes";
		askMatchId(socket, choosenId);		
	}
	else
	{
		choosenElement.classList.remove("invitation-waiting");
		choosenElement.classList.remove("invitation-confirmed");
		alert(`${choosenId} says: fuck you`);
	}
}

function receiveMatchId(matchId) {

	console.log("i have had and matchId: " + matchId)

	// document.body.addEventListener("htmx:configRequest", function(evt) {
	// 	if (evt.detail.elt.id === "startMatchButton"){
	// 		evt.detail.path = `/tournament/start-match/?matchId=${matchId}`;
	// 	}
	// });
	window.selfMatchId = matchId;
	setSelfMatchId();
}

function initTournamentWs() {

	if (window.rasp == "true")
		window.tournamentSocket = new WebSocket(`wss://${window.pidom}/ws/tournament/`);
	else
		window.tournamentSocket = new WebSocket(`ws://localhost:8000/ws/tournament/`);

	window.tournamentSocket.onopen = () => {
		console.log("Connexion Tournament établie 😊");	
	}
	window.tournamentSocket.onclose = () => {
		console.log("Connexion Tournament disconnected 😈");	
	};	
	window.tournamentSocket.onmessage = (event) => {

		console.log("Message reçu :", event.data);

		const data = JSON.parse(event.data);

		switch (data.type)
		{
			case "selfAssign":
				setSelfId(data.selfId);
				break;
			case "playerList":
				updatePlayers(window.tournamentSocket, data.players);
				break;
			case "matchList":
				updateMatchs(window.tournamentSocket, data.matchs);
				break;
			case "invitation":
				receiveInvitation(window.tournamentSocket, data.player);
				break;
			case "cancelInvitation":
				invitationCancelled(data.player);
				break;
			case "confirmation":
				receiveConfirmation(window.tournamentSocket, data.choosen, data.response);
				break;
			default:
				if (data.matchId) 
					receiveMatchId(data.matchId);			
				break;
		}

		// const data = JSON.parse(event.data);
		
		// if (data.type == "selfAssign")			
		// 	setSelfId(data.selfId);		
		// else if (data.type == "playerList")
		// 	updatePlayers(window.tournamentSocket, data.players);
		// else if (data.type == "invitation")		
		// 	receiveInvitation(window.tournamentSocket, data.player);
		// else if (data.type == "cancelInvitation")		
		// 	invitationCancelled(data.player);		
		// else if (data.type == "confirmation")		
		// 	receiveConfirmation(data.choosen, data.response);		
		// else if (data.matchId)		
		// 	receiveMatchId(data.matchId);
	};	
}

