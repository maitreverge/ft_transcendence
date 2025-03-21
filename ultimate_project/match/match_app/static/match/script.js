
function stopMatch(matchId)
{
	if (window.selfMatchId == matchId)
	{	
		fetch(`/match/stop-match/${window.selfId}/${matchId}/`)
		.then(response => {
			if (!response.ok) 
				throw new Error(`Error HTTP! Status: ${response.status}`);		  
			return response.text();
		})
		.then(data => console.log(data))
		.catch(error => console.log(error))
	}
	else
		document.getElementById('match').remove()
	console.log("YOUHOUHOUHOU");
	// if (window.selfMatchId != window.matchId)
	// {
		console.log("jypigequeuedalle");
		if (!window.matchSocket)
			console.log("LE WEBSOCKET ETS NULL.");
		else 
		{
			console.log("je sais pas ce qu eje fou la");
			if (window.matchSocket.readyState === WebSocket.OPEN)
			{
				console.log("je vais envoyer 42");
				window.stopFlag = true
				window.matchSocket.close(3666);
				window.matchSocket2.close(3666);
			} 
			else 
			{
				console.log("La WebSocket était déjà fermée.");
			}
			console.log("je nai pas plante");
		}
		console.log("toujours vivant");
		const oldScripts = document.querySelectorAll("script.match-script");
		console.log("olscript len", oldScripts.length);			
		oldScripts.forEach(oldScript =>{console.log("old: ", oldScript.src); oldScript.remove()});
	// }
	// else
	// 	console.log("pas spec!!");
	
}

// function setCommands(socket, socket2) {
	
// 	const keysPressed = {};
// 	document.addEventListener("keydown", function(event) {

// 		keysPressed[event.key] = true;
// 		// console.log("event :", event.key);
// 		if (socket.readyState === WebSocket.OPEN)
// 		{
// 			if (keysPressed[event.key] === true) 
// 			{
// 				event.preventDefault();
// 				socket.send(JSON.stringify({
// 					action: 'move', dir: 'up'}));
// 			} else if (keysPressed[event.key] === true) 
// 			{
// 				event.preventDefault();
// 				socket.send(JSON.stringify({
// 					action: 'move', dir: 'down'}));
// 			}
// 			if (socket2 && socket2.readyState === WebSocket.OPEN)
// 			{
// 				if (keysPressed[event.key] === true) 
// 				{
// 					event.preventDefault();
// 					socket2.send(JSON.stringify({
// 						action: 'move', dir: 'up'}));
// 				} else if (keysPressed[event.key] === true) 
// 				{
// 					event.preventDefault();
// 					socket2.send(JSON.stringify({
// 						action: 'move', dir: 'down'}));
// 				}
// 			}
// 		} 
// 	});
// 	document.addEventListener("keyup", event => {
// 		delete keysPressed[event.key];
// 	});
// }
// function setCommands(socket, socket2) {
//     const keysPressed = {};

//     document.addEventListener("keydown", function(event) {
//         keysPressed[event.key] = true; 

//         if (socket.readyState === WebSocket.OPEN) {
//             if (keysPressed["ArrowUp"]) { 
//                 event.preventDefault();
//                 socket.send(JSON.stringify({ action: 'move', dir: 'up' }));
//             }
//             if (keysPressed["ArrowDown"]) { 
//                 event.preventDefault();
//                 socket.send(JSON.stringify({ action: 'move', dir: 'down' }));
//             }
//         }

//         if (socket2 && socket2.readyState === WebSocket.OPEN) {
//             if (keysPressed["+"]) { 
//                 event.preventDefault();
//                 socket2.send(JSON.stringify({ action: 'move', dir: 'up' }));
//             }
//             if (keysPressed["Enter"]) { 
//                 event.preventDefault();
//                 socket2.send(JSON.stringify({ action: 'move', dir: 'down' }));
//             }
//         }
//     });

//     document.addEventListener("keyup", event => {
//         delete keysPressed[event.key];
//     });
// }

function setCommands(socket, socket2) {
    const keysPressed = {}; // Stocker les touches enfoncées
    let animationFrameId = null; // Stocke l'ID du requestAnimationFrame

    function sendCommands() {
        if (socket.readyState === WebSocket.OPEN) {
            if (keysPressed["ArrowUp"]) {
				
                socket.send(JSON.stringify({ action: 'move', dir: 'up' }));
            }
            if (keysPressed["ArrowDown"]) {
				
                socket.send(JSON.stringify({ action: 'move', dir: 'down' }));
            }
        }

        if (socket2 && socket2.readyState === WebSocket.OPEN) {
            if (keysPressed["+"]) {
                socket2.send(JSON.stringify({ action: 'move', dir: 'up' }));
            }
            if (keysPressed["Enter"]) {
                socket2.send(JSON.stringify({ action: 'move', dir: 'down' }));
            }
        }

        animationFrameId = requestAnimationFrame(sendCommands); // Appelle la fonction en boucle
    }

    document.addEventListener("keydown", function(event) {
		event.preventDefault();
        if (!keysPressed[event.key]) { // Empêche d'ajouter plusieurs fois la même touche
            keysPressed[event.key] = true;
        }
        
        if (!animationFrameId) { // Démarre l'animation seulement si elle n'est pas déjà en cours
            animationFrameId = requestAnimationFrame(sendCommands);
        }
    });

    document.addEventListener("keyup", function(event) {
        delete keysPressed[event.key];

        if (Object.keys(keysPressed).length === 0) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    });
}

function setCommands2(socket) {

	document.addEventListener("keydown", function(event) {
		// console.log("event :", event.key);
		if (socket.readyState === WebSocket.OPEN)
		{
			if (event.key === "+") 
			{
				event.preventDefault();
				socket.send(JSON.stringify({
					action: 'move', dir: 'up'}));
			} else if (event.key === "Enter") 
			{
				event.preventDefault();
				socket.send(JSON.stringify({
					action: 'move', dir: 'down'}));
			}
		} 
	});
}
let currentX = 0, currentY = 0;
let targetX = 0, targetY = 0;

let actualPads = [0, 0]
let targetPads = [0, 0]
const speed = 0.3; // Ajuste entre 0.05 (lent) et 0.3 (rapide) pour fluidité

function animate(pads) {
    currentX += (targetX - currentX) * speed;
    currentY += (targetY - currentY) * speed;

	actualPads[0] += (targetPads[0] - actualPads[0]) * speed;
	actualPads[1] += (targetPads[1] - actualPads[1]) * speed;
	// console.log("ANIMATION");
    pads[2].style.transform = `translate(${currentX}px, ${currentY}px)`;
	pads[0].style.transform = `translateY(${actualPads[0]}px)`;
	pads[1].style.transform = `translateY(${actualPads[1]}px)`;
	// pads[2].style.left = currentX + "%";
	// pads[2].style.top = currentY + "%";
    requestAnimationFrame(()=>animate(pads));
}

// Appelle animate une seule fois au début


// À chaque message WebSocket :
// function onMatchWsMessage(event, pads, [waiting, end], waitingState) {
//     const data = JSON.parse(event.data);
//     const matchRect = document.getElementById("match").getBoundingClientRect();

//     if (pads[0] && pads[1] && data.yp1 !== undefined && data.yp2 !== undefined) {
//         pads[0].style.top = data.yp1 + "%";
//         pads[1].style.top = data.yp2 + "%";
        
//         targetX = data.ball[0] * (matchRect.width / 100);
//         targetY = data.ball[1] * (matchRect.height / 100);

//         pads[3].innerText = data.score[0] + " | " + data.score[1];
//     }
// }

function onMatchWsMessage(event, pads, [waiting, end], waitingState) {
	
	// requestAnimationFrame(() => {
	const data = JSON.parse(event.data);
	// console.log("match mesage: ", data);
	if (data.state == "end")
	{	
		end.innerHTML = "the winner is :" + data.winnerId + end.innerHTML;
		end.classList.add("end");
	}
	if (waitingState[0] != data.state) 
	{
		waitingState[0] = data.state;	
		if (waiting) 
		{
			if (data.state == "waiting")			
				waiting.classList.remove("no-waiting");
			else			
				waiting.classList.add("no-waiting");			
		}			
	}
	match = document.getElementById("match");
	const matchRect = match.getBoundingClientRect();
	// console.log(" w ", rect.width, " h ", rect.height);
	// console.log(" ball 0 ", data.ball[0], " ball1 ", data.ball[1]);
	// console.log("data: ", `${data.ball[0] * (rect.width / 100)}`, `${data.ball[1] * (rect.height / 100)}}`);
	// if (pads[0] && pads[1] && data.yp1 !== undefined && data.yp2 !== undefined)
	// {
	// 	pads[0].style.top = data.yp1 + "%";
	// 	pads[1].style.top = data.yp2 + "%";
	// 	// pads[2].style.left = data.ball[0] + "%";
	// 	// pads[2].style.top = data.ball[1] + "%";
	// 	// pads[0].style.transform = `translateY(${data.yp1}%)`;
	// 	// pads[1].style.transform = `translateY(${data.yp2}%)`;
	// 	pads[2].style.transform = `translate(${data.ball[0] * (rect.width / 100)}px, ${data.ball[1] * (rect.height / 100)}px)`;
	// 	pads[3].innerText = data.score[0] + " | " + data.score[1];
	// }
	
    if (pads[0] && pads[1] && data.yp1 !== undefined && data.yp2 !== undefined) {
        // pads[0].style.top = data.yp1 + "%";
        // pads[1].style.top = data.yp2 + "%";
        
		targetPads[0] = data.yp1 * (matchRect.height / 100);
		targetPads[1] = data.yp2 * (matchRect.height / 100);

        targetX = data.ball[0] * (matchRect.width / 100);
        targetY = data.ball[1] * (matchRect.height / 100);
		// targetX = data.ball[0];
        // targetY = data.ball[1];
        pads[3].innerText = data.score[0] + " | " + data.score[1];
    }
	// });
		
}

// function onMatchWsMessage2(event, pads, [waiting, end], waitingState) {
		
// 	const data = JSON.parse(event.data);

// 	if (data.state == "end")
// 	{	
// 		end.innerHTML = "the winner is :" + data.winnerId + end.innerHTML;
// 		end.classList.add("end");
// 	}
// 	if (waitingState[0] != data.state) 
// 	{
// 		waitingState[0] = data.state;	
// 		if (waiting) 
// 		{
// 			if (data.state == "waiting")			
// 				waiting.classList.remove("no-waiting");
// 			else			
// 				waiting.classList.add("no-waiting");			
// 		}			
// 	}
// 	if (pads[0] && pads[1] && data.yp1 !== undefined && data.yp2 !== undefined)
// 	{
// 		pads[0].style.top = data.yp1 + "%";
// 		pads[1].style.top = data.yp2 + "%";
// 		pads[2].style.top = data.ball[0] + "%";
// 		pads[2].style.top = data.ball[1] + "%";
// 		pads[3].innerText = data.score[0] + " | " + data.score[1];
// 	}
// }

function sequelInitMatchWs(socket) {

	const pads = [
		document.getElementById("p1"),
		document.getElementById("p2"),
		document.getElementById("ball"),
		document.getElementById("score")
	];
	match = document.getElementById("match");
	const matchRect = match.getBoundingClientRect();
	pads[2].style.width = (matchRect.width / 100) * 2;
	pads[2].style.height = (matchRect.width / 100) * 2;
	const [waiting, end] = [		
		document.getElementById("waiting"),	document.getElementById("end")];	
	let waitingState = ["waiting"];
	requestAnimationFrame(()=>animate(pads));
	socket.onmessage = event => onMatchWsMessage(
		event, pads, [waiting, end], waitingState);
	
	const spec = document.getElementById("spec")
	if (spec)
	{
		if (window.selfMatchId != window.matchId)
			spec.style.display = "block";
		else
			spec.style.display = "none";
	}
	initSecPlayer();
	setCommands(socket, window.matchSocket2);
}

function initSecPlayer() {

	if (window.rasp == "true")
		window.matchSocket2 = new WebSocket(
			`wss://${window.pidom}/ws/match/${window.matchId}/` +
			`?playerId=${-window.playerId}`);
	else	
		window.matchSocket2 = new WebSocket(
			`ws://localhost:8000/ws/match/${window.matchId}/` +
			`?playerId=${-window.playerId}`);

	window.matchSocket2.onopen = () => {
		console.log("Connexion Match établie 2nd Player😊");
	};
	window.matchSocket2.onclose = (event) => {
		console.log("Connexion Match disconnected 😈 2nd Player");
	};
	// setCommands2(window.matchSocket2);
}

function initMatchWs() {
//si je viens du debut je sui sclosé (et je reviens par boucle) si je viens de onclse je continu normal
	console.log("INIT MATCH 😊😊😊");
	console.log("STOP: " + window.stopFlag);
	console.log("ANTILOPP: " + window.antiLoop);
	if (window.matchSocket && window.antiLoop)
		return window.matchSocket.close();
    // if (window.matchSocket)
	// 	window.matchSocket.close();
	window.antiLoop = true;
	if (window.rasp == "true")
		window.matchSocket = new WebSocket(
			`wss://${window.pidom}/ws/match/${window.matchId}/` +
			`?playerId=${window.playerId}`);
	else	
		window.matchSocket = new WebSocket(
			`ws://localhost:8000/ws/match/${window.matchId}/` +
			`?playerId=${window.playerId}`);
	window.matchSocket.onopen = () => {
		console.log("Connexion Match établie 😊");
	};
	window.matchSocket.onclose = (event) => {	
		console.log("Connexion Match disconnected 😈");		
		window.antiLoop = false;
		console.log("CODE: " + event.code);
		console.log("STOP: " + window.stopFlag);
		if (event.code !== 3000 && !window.stopFlag)
		{			
			console.log("codepas42");
			initMatchWs();	
		}
		else
			console.log("code42");
		window.stopFlag = false;
	};
	sequelInitMatchWs(window.matchSocket);
}
