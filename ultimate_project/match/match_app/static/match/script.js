
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
}

function setCommands(socket) {

	document.addEventListener("keydown", function(event) {
		if (socket.readyState === WebSocket.OPEN)
		{
			if (event.key === "ArrowUp") 
			{
				event.preventDefault();
				socket.send(JSON.stringify({
					action: 'move', dir: 'up'}));
			} else if (event.key === "ArrowDown") 
			{
				event.preventDefault();
				socket.send(JSON.stringify({
					action: 'move', dir: 'down'}));
			}
		} 
	});
}

function onMatchWsMessage(event, pads, [waiting, end], waitingState) {
		
	const data = JSON.parse(event.data);

	if (data.state == "end")
	{	
		end.innerHTML = "the winner is :" + data.winnerId + end.innerHTML;
		end.classList.add("end");
	}
	if (waitingState[0] != data.state) 
	{
		waitingState[0] = data.state;				
		if (data.state == "waiting")
			waiting.classList.remove("no-waiting");
		else			
			waiting.classList.add("no-waiting");			
	}
	pads[0].style.top = data.yp1 + "vh";
	pads[1].style.top = data.yp2 + "vh";
}

function sequelInitMatchWs(socket) {

	const pads = [
		document.getElementById("p1"), document.getElementById("p2")];
	const [waiting, end] = [		
		document.getElementById("waiting"),	document.getElementById("end")];	
	let waitingState = ["waiting"];
	socket.onmessage = event => onMatchWsMessage(
		event, pads, [waiting, end], waitingState);
	setCommands(socket);
	if (window.selfMatchId != window.matchId)
		document.getElementById("spec").style.display = "block";
}

function initMatchWs() {

	if (window.matchSocket && window.antiLoop)
		return window.matchSocket.close();
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
	window.matchSocket.onclose = () => {	
		console.log("Connexion Match disconnected 😈");		
		window.antiLoop = false;
		initMatchWs();	
	};
	sequelInitMatchWs(window.matchSocket);
}
