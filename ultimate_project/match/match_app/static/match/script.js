
function quitMatch()
{
	document.body.classList.remove("match-active");
	window.gameStartTimestamp = undefined; 	
	removeKeyBoardEvent();
	cancelAnimationFrame(window.pongAnim);
	manualCloseMatchWss();
	delMatchScript();
	delMatch();
}

function manualCloseMatchWss()
{
	window.stopFlag = true;
	const closeMatchWs = (socket)=> {
		if (socket && socket.readyState === WebSocket.OPEN)			
			socket.close(3666);		
	};
	closeMatchWs(window.matchSocket);
	closeMatchWs(window.matchSocket2);
}

function delMatchScript()
{
	const scripts = document.querySelectorAll("script.match-script");		
	scripts.forEach(oldScript => oldScript.remove());	
}

function delMatch()
{
	document.getElementById('match')?.remove();    
    const rulesOverlay = document.getElementById('rules-overlay');
	if (rulesOverlay)
		rulesOverlay.style.display = 'none';	 
}

function displayGiveUp(visible)
{
	const giveUp = document.getElementById("quit-match-button");
	if (giveUp)
	{
		if (visible)
			giveUp.style.display = "block";
		else
			giveUp.style.display = "none";	
	}	
}

function stopMatch(matchId)
{	
	if (!matchId)	
		return delMatchScript();			
	removeKeyBoardEvent();
	cancelAnimationFrame(window.pongAnim);	
	displayGiveUp(false);		
	window.gameStartTimestamp = undefined; 	
	if (window.selfMatchId == matchId)	
		sendStopMatch(matchId);	
	setTimeout(closeMatchWebSockets, 1000);		
}

function sendStopMatch(matchId)
{
	fetch(`/match/stop-match/${window.playerId}/${matchId}/`)
		.then(response => {
			if (!response.ok) 
				throw new Error(`Error HTTP! Status: ${response.status}`);		  
			return response.text();
		})
		.catch(error => console.log(error))
}

function removeKeyBoardEvent()
{
	document.removeEventListener("keydown", addKeyBoardEvent.keyDown);
	document.removeEventListener("keyup", addKeyBoardEvent.keyUp);
}

function addKeyBoardEvent()
{
	addKeyBoardEvent.keysPressed = {};   
	addKeyBoardEvent.keyBoardAnim = null;
	addKeyBoardEvent.keyDown = (e)=> {
		e.preventDefault();
        if (!addKeyBoardEvent.keysPressed[e.key])
            addKeyBoardEvent.keysPressed[e.key] = true;  
        if (!addKeyBoardEvent.keyBoardAnim)
            addKeyBoardEvent.keyBoardAnim = requestAnimationFrame(sendCommands);        
	};
	addKeyBoardEvent.keyUp = (e)=> {
		e.preventDefault();
        delete addKeyBoardEvent.keysPressed[e.key];
        if (Object.keys(addKeyBoardEvent.keysPressed).length === 0)
		{
            cancelAnimationFrame(addKeyBoardEvent.keyBoardAnim);
            addKeyBoardEvent.keyBoardAnim = null;
        }
    };
	document.addEventListener("keydown", addKeyBoardEvent.keyDown);
	document.addEventListener("keyup", addKeyBoardEvent.keyUp);
}

function sendCommands()
{
	const socket = window.matchSocket;
	const socket2 = window.matchSocket2; 
	if (socket.readyState === WebSocket.OPEN)
	{
		if (addKeyBoardEvent.keysPressed["ArrowUp"]) 				
			socket.send(JSON.stringify({action: 'move', dir: 'up'}));
		
		if (addKeyBoardEvent.keysPressed["ArrowDown"]) 				
			socket.send(JSON.stringify({action: 'move', dir: 'down'}));            
	}
	if (socket2 && socket2.readyState === WebSocket.OPEN)
	{
		if (addKeyBoardEvent.keysPressed["+"]) 
			socket2.send(JSON.stringify({action: 'move', dir: 'up'}));            
		if (addKeyBoardEvent.keysPressed["Enter"]) 
			socket2.send(JSON.stringify({action: 'move', dir: 'down'}));            
	}
	addKeyBoardEvent.keyBoardAnim = requestAnimationFrame(sendCommands); 
}

// function setCommands(socket, socket2) {
//     const keysPressed = {}; // Stocker les touches enfoncées
//     let keyBoardAnim = null; // Stocke l'ID du requestAnimationFrame

    // function sendCommands() {
    //     if (socket.readyState === WebSocket.OPEN)
	// 	{
    //         if (keysPressed["ArrowUp"]) 				
    //             socket.send(JSON.stringify({action: 'move', dir: 'up'}));
            
    //         if (keysPressed["ArrowDown"]) 				
    //             socket.send(JSON.stringify({action: 'move', dir: 'down'}));            
    //     }
    //     if (socket2 && socket2.readyState === WebSocket.OPEN)
	// 	{
    //         if (keysPressed["+"]) 
    //             socket2.send(JSON.stringify({action: 'move', dir: 'up'}));            
    //         if (keysPressed["Enter"]) 
    //             socket2.send(JSON.stringify({action: 'move', dir: 'down'}));            
    //     }
    //     keyBoardAnim = requestAnimationFrame(sendCommands); // Appelle la fonction en boucle
    // }

	// const keyDown = (e)=> {
	// 	e.preDefault();
    //     if (!keysPressed[e.key])
    //         keysPressed[e.key] = true;  
    //     if (!keyBoardAnim)
    //         keyBoardAnim = requestAnimationFrame(sendCommands);        
	// };
	// const keyUp = (e)=> {
	// 	e.preDefault();
    //     delete keysPressed[e.key];
    //     if (Object.keys(keysPressed).length === 0)
	// 	{
    //         cancelAnimationFrame(keyBoardAnim);
    //         keyBoardAnim = null;
    //     }
    // };
	// document.addEventListener("keydown", keyDown);
	// document.addEventListener("keyup", keyUp);


    // document.addEventListener("keydown", function(event) {
	// 	event.preventDefault();
    //     if (!keysPressed[event.key]) { // Empêche d'ajouter plusieurs fois la même touche
    //         keysPressed[event.key] = true;
    //     }
        
    //     if (!keyBoardAnim) { // Démarre l'animation seulement si elle n'est pas déjà en cours
    //         keyBoardAnim = requestAnimationFrame(sendCommands);
    //     }
    // });

    // document.addEventListener("keyup", function(event) {
    //     delete keysPressed[event.key];

    //     if (Object.keys(keysPressed).length === 0) {
    //         cancelAnimationFrame(keyBoardAnim); //! penser a cancel aussi lanimation de la balle!!!!!!!!!!!!!!!!!!!!!!!!!!!1111111
    //         keyBoardAnim = null;
    //     }
    // });
// }

window.window.newTargetX = window.window.newTargetX || 0
window.window.newTargetY = window.window.window.newTargetY || 0;

window.targetPads = window.targetPads || [0, 0];

function animate2D(pads) {

	pads[2].style.transform = `translate(${window.newTargetX}px, ${window.newTargetY}px)`;
	pads[0].style.transform = `translateY(${targetPads[0]}px)`;
	pads[1].style.transform = `translateY(${targetPads[1]}px)`;
	window.pongAnim = requestAnimationFrame(() => animate2D(pads));
}

function startCountdown(delay)
{
	loaderElement = document.querySelector(".loader");
	if (loaderElement)
		loaderElement.style.opacity = "1";

    const countdownEl = document.querySelector('.countdown');
    const countdownEndsAt = window.gameStartTimestamp * 1000 + delay * 1000;

	function updateCountdown() {
        const now = Date.now();
        const remaining = Math.ceil((countdownEndsAt - now) / 1000);

        if (remaining > 0) {
            countdownEl.textContent = remaining;
            requestAnimationFrame(updateCountdown);
        } else if (remaining > -1) {
            countdownEl.textContent = "GO!";
            requestAnimationFrame(updateCountdown);
        } else {
            loaderElement.style.opacity = "0";
            window.gameStartTimestamp = undefined;
        }
    }
	updateCountdown();
}

function displayPlayersInfos(data, pads)
{
	if (!data.names)
		return;
	pads[3].innerText = data.score[0] + " | " + data.score[1];	
	const leftName = document.getElementById("inst-left");
	const rightName = document.getElementById("inst-right");
	if (window.selfMatchId != window.matchId)
	{
		leftName.innerHTML = data.names[0];
		rightName.innerHTML = data.names[1];		
	}			
	else if (window.player2Id != 0)
	{			
		leftName.innerHTML = data.names[0] + "<br> keys: ↑ / ↓";
		rightName.innerHTML = data.names[1] + "<br> keys: enter / +";	
	}			
	else if (data.plyIds)
	{
		if (window.playerId == data.plyIds[0])
		{
			leftName.innerHTML = data.names[0] + "<br> keys: ↑ / ↓";
			rightName.innerHTML = data.names[1];
		}
		else
		{
			leftName.innerHTML = data.names[0];
			rightName.innerHTML = data.names[1] + "<br> keys: ↑ / ↓";
		} 
	}	
}

function onMatchWsMessage(
	event, pads, [waiting, endCont, end, spec], waitingState) 
{	
	const data = JSON.parse(event.data);
	startDelay(data);
	displayPlayersInfos(data, pads);	
	setEnd(data, endCont, end, spec);
	setWaiting(data, waiting, waitingState);
	match = document.getElementById("match");
	const matchRect = match.getBoundingClientRect();
	const ballRect = pads[2].getBoundingClientRect();
	pads[2].style.top = -(matchRect.width / 100);
	pads[2].style.width = (matchRect.width / 100) * 2;
	pads[2].style.height = (matchRect.height / 100) * 2;	
    if (pads[0] && pads[1] && data.yp1 !== undefined && data.yp2 !== undefined)
	{        
		window.targetPads[0] = data.yp1 * (matchRect.height / 100);
		window.targetPads[1] = data.yp2 * (matchRect.height / 100);

		window.newTargetX = data.ball[0] * (matchRect.width / 100);
		window.newTargetY = data.ball[1] * (matchRect.height / 100);	
    }
}

function startDelay(data)
{
	if (data.timestamp && !data.state)
	{
		if (window.gameStartTimestamp === undefined)
		{
			window.gameStartTimestamp = data.timestamp;           
			console.log("✅ Premier timestamp enregistré:", data.timestamp);	
            startCountdown(data.delay);
		}
		else 
			console.log("⏩ Timestamp déjà reçu, ignoré.");		
		return;
	}
}

function setEnd(data, endCont, end, spec)
{
	if (data.state == "end")
	{	
        let url;
        if (window.selfName == data.winnerName)
            url = "https://dansylvain.github.io/pictures/sdurif.webp";
		else if (spec.style.display != "none")
		{
			url = "https://dansylvain.github.io/pictures/tennis.webp";
			spec.style.display = "none";
		}
		else 
			url = "https://dansylvain.github.io/pictures/MacronExplosion.webp";
		end.innerHTML = `The winner is: ${data.winnerName} <br> 
		Score: ${data.score[0]} : ${data.score[1]} <br> 
		<img src="${url}" 
		alt="Winner GIF" 
		class="winner-gif">
		`;		
		endCont.classList.add("end-cont");
		endCont.style.display = "block";
		console.log("🏁 Match terminé, reset du timestamp");
		window.gameStartTimestamp = undefined;	
	}
}

function setWaiting(data, waiting, waitingState)
{
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
}

function setSpec(spec)
{	
	if (spec)
	{
		if (window.selfMatchId != window.matchId)
		{
			spec.style.display = "block";
			displayGiveUp(false);			
		}
		else
		{
			spec.style.display = "none";
			displayGiveUp(true);		
		}
	}
}

function initSecPlayer()
{
	if (window.player2Id != 0)
	{
		window.matchSocket2 = createWebSocket(window.player2Id);
		window.matchSocket2.onopen = () => {
			console.log("Connexion Match établie 2nd Player😊");
		};
		window.matchSocket2.onclose = () => {
			console.log("Connexion Match disconnected 😈 2nd Player");
		};	
	}
}

function initDomain()
{
	if (window.location.hostname === "localhost" ||
		window.location.hostname === "127.0.0.1")
        window.pidom = "localhost:8443";
	else
		window.pidom = window.location.hostname + ":8443";
}

function createWebSocket(playerId)
{
	return new WebSocket(
        `wss://${window.pidom}/ws/match/${window.matchId}/` +
        `?playerId=${playerId}`);
}

function closeMatchWssOnEnter()
{
	const socket = window.matchSocket;
	const socket2 = window.matchSocket2;	

	const closeMatchWsOnEnter = (socket)=> {
		if (socket && socket.readyState === WebSocket.OPEN && window.antiLoop)	
			return socket.close(), true;
		return false;			
	};
	const ret = closeMatchWsOnEnter(socket); 
	const ret2 = closeMatchWsOnEnter(socket2);
	return (ret || ret2); 
}

function initMatchWs()
{
    initDomain();
	if (closeMatchWssOnEnter())
		return;    
	window.antiLoop = true;
    window.matchSocket = createWebSocket(window.playerId);
	window.matchSocket.onopen = ()=> console.log("Connexion Match établie 😊");
	window.matchSocket.onclose = event => matchWsDisconnectStrategy(event);
	sequelInitMatchWs(window.matchSocket);
}

function matchWsDisconnectStrategy(event)
{
	console.log("Connexion Match disconnected 😈");	
	
	removeKeyBoardEvent();
	window.antiLoop = false;	
	if (event.code !== 3000 && !window.stopFlag)		
		initMatchWs();	
	window.stopFlag = false;
}

function sequelInitMatchWs(socket)
{
	const pads = [
		document.getElementById("p1"),
		document.getElementById("p2"),
		document.getElementById("ball"),
		document.getElementById("score"),		
	];
	const [waiting, endCont, end] = [		
		document.getElementById("waiting"),
		document.getElementById("end-cont"),
		document.getElementById("end")];	
	let waitingState = ["waiting"];
	requestAnimationFrame(()=>animate2D(pads));
	const spec = document.getElementById("spec");
	setSpec(spec);
	socket.onmessage = event => onMatchWsMessage(
		event, pads, [waiting, endCont, end, spec], waitingState);		
	initSecPlayer();	
	addKeyBoardEvent();
}
