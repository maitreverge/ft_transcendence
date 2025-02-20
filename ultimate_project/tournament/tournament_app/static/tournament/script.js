
// document.getElementById("new-match").addEventListener("click", function(event) {
// 	event.preventDefault();
// 	console.log("ta bien clique man");
// 	fetch('http://localhost:8000/match/new-match/')
// 		.then(response => response.json())
// 		.then(data => console.log(data))
// 		.catch(error => console.error(error))
// });

function sendInvitation(socket, choosenId)
{
	console.log("i will send invitation to choosenId: " + choosenId);
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({type: "invitation", choosenId: choosenId}))
}

function sendConfirmation(socket, applicantId)
{
	console.log("i will send confirmation to applicant: " + applicantId);
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({type: "confirmation", response: "yes", applicantId: applicantId}))
}

function sendMatchId(socket, matchId, choosenId) {
	console.log("i will send matchId: " + matchId + " to choosen: " + choosenId);
	if (socket.readyState === WebSocket.OPEN) 
		socket.send(JSON.stringify({matchId: matchId, choosenId: choosenId}))
}

function updateUsersList(players, socket) {
    const usersContainer = document.getElementById("users");

    usersContainer.innerHTML = "";


    players.forEach(user => {
      const div = document.createElement("div");
      div.className = "user";
      div.textContent = `user: ${user.playerId}`;
    
      div.onclick = function() {
        console.log(`my choice: ${user.playerId}`);
        window.userIdChosen = user.playerId;
        this.style.backgroundColor = 'red';
      };
      
      usersContainer.appendChild(div);
    });
	elements = document.getElementsByClassName("user");
	// console.log("elements: " + elements);
	Array.from(elements).forEach( element => {
		// console.log("element: " + element);
		element.addEventListener("click", event => {
			console.log("ye" + window.userIdChosen);
			sendInvitation(socket, window.userIdChosen);
		});

	});
}

function makeChoice(selfId) {
	window.selfId = selfId;
	document.getElementById("player").innerText = 
	"Je suis le joueur " + window.selfId;
	
  	window.userIdChosen = null;


}

function receiveInvitation(socket, host) {
	console.log("i have had and invitation from: " + host)
	sendConfirmation(socket, host);
}

function askMatchId(choosenId) {
	document.body.addEventListener("htmx:configRequest", function(evt) {
		if (evt.detail.elt.id === "startMatchButton" && window.userIdChosen !== null){
			evt.detail.path = "/tournament/start-match/?selfid=" + window.selfId + "&select=" + choosenId;
		}
	});
}

function receiveConfirmation(choosenId, response) {
	console.log("i have had and confirmation from: " + choosenId
		+ ", the answer is :" + response);
	askMatchId(choosenId);
}


function receiveMatchId(matchId) {
	console.log("i have had and matchId: " + matchId)
	document.body.addEventListener("htmx:configRequest", function(evt) {
		if (evt.detail.elt.id === "startMatchButton"){
			evt.detail.path = `/tournament/start-match/?matchId=${matchId}`;
		}
	});
}

function initWs() {
	console.log("initWs");
	if (window.rasp == "true")
		window.socket = new WebSocket(`wss://${window.pidom}/ws/match/${window.matchId}/`);//!
	else
		window.socket = new WebSocket(`ws://localhost:8000/ws/tournament/`);

	window.socket.onopen = () => {
		console.log("Connexion établie 😊");
	
	};

	// const p1 = document.getElementById("p1");
	// const p2 = document.getElementById("p2");
	
	window.socket.onmessage = (event) => {
		console.log("Message reçu :", event.data);
		const data = JSON.parse(event.data);
		console.log("new message");
		if (data.type == "selfAssign")
		{
			var selfId = data.selfId;
			window.selfId = data.selfId;
			makeChoice(data.selfId);
		}	
				
		// 	document.getElementById("player").innerText = 
		//  "Je suis le joueur " + data.selfId;
		// 		// Assure-toi que userIdChosen est initialisé
		// window.userIdChosen = null;
	
		// // Avant que htmx n'envoie la requête, on modifie l'URL avec le paramètre choisi
		// document.body.addEventListener("htmx:configRequest", function(evt) {
		// 	if(evt.detail.elt.id === "startMatchButton" && window.userIdChosen !== null){
		// 		evt.detail.path = "/tournament/start-match/selfid=?select=" + window.userIdChosen;
		// 	}
		// });
		else if (data.type == "playerList")
			updateUsersList(data.players, window.socket);
		else if (data.type == "invitation")
		{
			console.log("window selfid:", window.selfId);
			console.log("var selfid:", selfId);
			receiveInvitation(window.socket, data.player)
		}
		else if (data.type == "confirmation")
		{
			
			receiveConfirmation(data.choosen, data.response);
		}
		else if (data.matchId)
		{
			
			receiveMatchId(data.matchId);
		}
		// p1.style.top = data.yp1 + "vh";
		// p2.style.top = data.yp2 + "vh";
	};

	document.addEventListener("keydown", function(event) {
		
		if (window.socket.readyState === WebSocket.OPEN) { // Vérifie si le WebSocket est bien connecté
				// socket.send("houlala la fleche du haut est presse daller en haut");//
			if (event.key === "ArrowUp") {
				event.preventDefault(); // Empêche l'action par défaut
				// console.log("Flèche haut pressée !");
				window.socket.send(JSON.stringify({action: 'move', dir: 'up'}));				
			} else if (event.key === "ArrowDown") {
				event.preventDefault();
				// console.log("Flèche bas pressée !");
				window.socket.send(JSON.stringify({action: 'move', dir: 'down'}));
			}
		} else {
			console.log("WebSocket non connecté !");
		}
	});
}

