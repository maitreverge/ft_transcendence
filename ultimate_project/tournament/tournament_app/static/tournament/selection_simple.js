
function sendInvitation(socket, choosenId) {
	
	console.log("i will send invitation to choosenId: " + choosenId);

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({type: "invitation", choosenId: choosenId}))
}

function sendConfirmation(socket, applicantId, response) {

	console.log(`i will send ${response} to applicant: ${applicantId}`);

	const applicantElement = document.getElementById(applicantId);
	applicantElement.classList.add("invitation-confirmed");	
	applicantElement.confirmed = 'yes';

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({type: "confirmation", response: response, applicantId: applicantId}))
}

function sendMatchId(socket, matchId, choosenId) {

	console.log("i will send matchId: " + matchId + " to choosen: " + choosenId);

	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({matchId: matchId, choosenId: choosenId}))
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

function addToPlayers(usersContainer, player) {
  	
	const div = document.createElement("div");
	div.className = "user";
	div.textContent = `user: ${player.playerId}`;
	div.id = player.playerId;
	if (player.playerId === window.selfId)
	{
		div.style.backgroundColor = 'violet'
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


function updatePlayers(socket, players) {

    const usersContainer = document.getElementById("users");
	userElements = usersContainer.children;
    // usersContainer.innerHTML = "";
	// userElements = document.getElementsByClassName("user");

	// if (!players.includes(element.dataset.id))	

    [...userElements].forEach( player => {
		console.log("il ya un element ds le bazar c le :" + player.id);
		if (players.some(el => el.playerId == player.id))
		{
			console.log("il ya un au moins un element qui sont egaux:" + player.id);
			usersContainer.removeChild(player);
		}
	});

	players.forEach( player => {
		console.log("foreach: playerId: " + player.playerId);
		if (![...userElements].some(el => el.id == player.playerId))	
		{
			console.log("is added");
			addToPlayers(usersContainer, player);
		}
	});

    // 	const div = document.createElement("div");
    // 	div.className = "user";
    // 	div.textContent = `user: ${user.playerId}`;
	// 	div.id = user.playerId;
	// 	if (user.playerId === window.selfId)
	// 	{
	// 		div.style.backgroundColor = 'violet'
	// 		div.onclick = function() {
	// 			alert("you can't choose yourself");
	// 		};
	// 	}
	// 	else
	// 	{
    // 		div.onclick = function() {
	// 			console.log("user confirmed: " + div.confirmed + " id: " + div.id);
	// 			if (typeof div.confirmed === 'undefined' || div.confirmed === 'no')
	// 			{
	// 				console.log(`my choice: ${user.playerId}`);
	// 				window.select = user.playerId;//!
	// 				this.classList.add("invitation-waiting");				
	// 				sendInvitation(socket, window.select);
	// 			}
	// 			else				
	// 				cancelInvitation(socket, user.playerId);				
    // 		};
	// 	}
    // 	usersContainer.appendChild(div);
    // });
	

	// Array.from(elements).forEach( element => {

	// 	element.addEventListener("click", event => {
	// 		console.log("ye" + window.select);
	// 		console.log(`choice: {{user.playerId}}`); window.select ='{{ user.playerId }}';
	// 		this.style.backgroundColor = 'red';
	// 		sendInvitation(socket, window.select);
	// 	});
	// });
	
}

function setSelfId(selfId) {
	window.selfId = selfId;
	document.getElementById("player").innerText = 
	"Je suis le joueur " + window.selfId;
	
  	window.select = null;
}

function receiveInvitation(socket, applicantId) {

	console.log("i have had and invitation from: " + applicantId)

	if (confirm(`you have an invitation from ${applicantId}`))
		sendConfirmation(socket, applicantId, "yes");
	else
		sendConfirmation(socket, applicantId, "no");
}

function askMatchId(choosenId) {

	document.body.addEventListener("htmx:configRequest", function(evt) {

		if (evt.detail.elt.id === "startMatchButton" && window.select !== null){
			evt.detail.path = "/tournament/start-match/?selfid=" + window.selfId + "&select=" + choosenId;
		}
	});
}

function receiveConfirmation(choosenId, response) {

	console.log("i have had and confirmation from: " + choosenId
		+ ", the answer is :" + response);
	
	const choosenElement = document.getElementById(choosenId); 
	if (response === "yes")
	{
		choosenElement.classList.remove("invitation-waiting");
		choosenElement.classList.add("invitation-confirmed");
		choosenElement.confirmed = "yes";
		askMatchId(choosenId);		
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

	document.body.addEventListener("htmx:configRequest", function(evt) {
		if (evt.detail.elt.id === "startMatchButton"){
			evt.detail.path = `/tournament/start-match/?matchId=${matchId}`;
		}
	});
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
		
		if (data.type == "selfAssign")			
			setSelfId(data.selfId);		
		else if (data.type == "playerList")
			updatePlayers(window.tournamentSocket, data.players);
		else if (data.type == "invitation")		
			receiveInvitation(window.tournamentSocket, data.player);
		else if (data.type == "cancelInvitation")		
			invitationCancelled(data.player);		
		else if (data.type == "confirmation")		
			receiveConfirmation(data.choosen, data.response);		
		else if (data.matchId)		
			receiveMatchId(data.matchId);
	};	
}

