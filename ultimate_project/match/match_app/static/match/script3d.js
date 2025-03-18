const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const textureLoader = new THREE.TextureLoader();

const rgeo = new THREE.BoxGeometry(5, 1, 1);
const sgeo = new THREE.SphereGeometry(1, 32, 32);

const rmat = [
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') })
];

const smat = new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') });

const r1 = new THREE.Mesh(rgeo, rmat);
const r2 = new THREE.Mesh(rgeo, rmat);

const ball = new THREE.Mesh(sgeo, smat);

scene.add(ball);
scene.add(r1);
scene.add(r2);

r1.position.z = 10;
r2.position.z = -10;

var angle = 0;

// fonction appelée lors du clic sur le bouton
function actionClick() {
    ball.material.color.setHex(0x00ff00);
}

function otherClick() {
    // change r1 images
    r1.material = [
        new THREE.MeshBasicMaterial({ map: textureLoader.load('/img1.png') }),
        new THREE.MeshBasicMaterial({ map: textureLoader.load('/img1.png') }),
        new THREE.MeshBasicMaterial({ map: textureLoader.load('/img1.png') }),
        new THREE.MeshBasicMaterial({ map: textureLoader.load('/img1.png') }),
        new THREE.MeshBasicMaterial({ map: textureLoader.load('/img1.png') }),
        new THREE.MeshBasicMaterial({ map: textureLoader.load('/img1.png') })
    ];
}

function change_zoom(width, height) {
    // change fov
    
    r = height / width;
    camera.position.z = 15 + 2 * r;
    camera.position.y = 2 + 10 * r;

    camera.lookAt(0, 0, 0);
    camera.updateProjectionMatrix();
}

// resize window when resizing
window.addEventListener('resize', () => {
    w = window.innerWidth;
    h = window.innerHeight;
    renderer.setSize(w, h);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    change_zoom(w, h);
});

function animate() {
    requestAnimationFrame(animate);

    ball.rotation.z += 0.1;

    renderer.render(scene, camera);
}

animate();

change_zoom(window.innerWidth, window.innerHeight);

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
		document.getElementById('container').remove()
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
			} 
			else 
			{
				console.log("La WebSocket était déjà fermée.");
			}
			console.log("je nai pas plante");
		}
		const oldScripts = document.querySelectorAll("script.match-script");			
		oldScripts.forEach(oldScript => oldScript.remove());
	// }
	// else
	// 	console.log("pas spec!!");
	
}

function setCommands(socket) {

	document.addEventListener("keydown", function(event) {
		console.log("event :", event.key);
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

function onMatchWsMessage(event, [waiting, end], waitingState) {
		
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
	if (data.yp1 !== undefined && data.yp2 !== undefined)
{
		r1.position.x = data.yp1;
		r2.position.x = data.yp2;
		ball.position.x = data.ball[0];
		ball.position.y = data.ball[1];
	}
}

function sequelInitMatchWs(socket) {

	const [waiting, end] = [		
		document.getElementById("waiting"),	document.getElementById("end")];	
	let waitingState = ["waiting"];
	socket.onmessage = event => onMatchWsMessage(
		event, [waiting, end], waitingState);
	setCommands(socket);
	const spec = document.getElementById("spec")
	if (spec)
	{
		if (window.selfMatchId != window.matchId)
			spec.style.display = "block";
		else
			spec.style.display = "none";
	}
	initSecPlayer();
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
	setCommands2(window.matchSocket2);
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

initMatchWs();