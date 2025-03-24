var container = document.getElementById('scene-container');

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
var renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

var textureLoader = new THREE.TextureLoader();

var rgeo = new THREE.BoxGeometry(5, 1, 1);
var sgeo = new THREE.SphereGeometry(1, 32, 32);

var rmat = [
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') }),
    new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') })
];

var smat = new THREE.MeshBasicMaterial({ map: textureLoader.load('https://threejs.org/examples/textures/crate.gif') });

var r1 = new THREE.Mesh(rgeo, rmat);
var r2 = new THREE.Mesh(rgeo, rmat);

var ball = new THREE.Mesh(sgeo, smat);

scene.add(ball);
scene.add(r1);
scene.add(r2);

r1.position.z = 10;
r2.position.z = -10;

var upgrade = {
	user_lvl: 0,
	points: 0,
	cooldown: 5,
}

function actionCooldownUpdate() {
	// update the html button
	if (!upgrade.cooldown) {
		document.getElementById("upgrade").innerHTML = `Upgrade (+${upgrade.points})`;
	} else if (upgrade.points) {
		document.getElementById("upgrade").innerHTML = `Upgrade (+${upgrade.points}) ${upgrade.cooldown}s`;
	} else {
		document.getElementById("upgrade").innerHTML = `Upgrade ${upgrade.cooldown}s`;
	}
}

// function call on button click
function actionUpgrade() {
	if (upgrade.points < 1) {
		return;
	}
	upgrade.points--;
	switch (upgrade.user_lvl) {
		case 0:
    		ball.material.color.setHex(0x00ff00);
			break;
		case 1:
			ball.material.color.setHex(0xff0000);
			break;
		case 2:
			ball.material.color.setHex(0x0000ff);
			break;
		case 3:
			// reset the color
			ball.material.color.setHex(0xffffff);
			ball.material.map = textureLoader.load('https://media.tenor.com/YkyhmCCJd_0AAAAM/aaaa.gif');
			// print the image size in the console
			console.log("Image size: " + ball.material.map.image.width + "x" + ball.material.map.image.height);
			break;
		default:
			break;
	}
	upgrade.user_lvl++;
	actionCooldownUpdate();
}

// function call each seconds
function actionCooldown() {
	if (upgrade.cooldown > 0) {
		upgrade.cooldown--;
	} else {
		upgrade.cooldown = 5;
	}
	if (upgrade.cooldown == 0) {
		upgrade.points++;
	}
	actionCooldownUpdate();
}

actionCooldownUpdate();
setInterval(actionCooldown, 1000);

let isDragging = false;
let previousMousePosition = { x: 0, y: 0 };

let radius = 15;

let theta = 0; 			// horizontal angle
let phi = Math.PI / 2;  // vertical angle

container.onmousedown = function (e) {
	isDragging = true;
	previousMousePosition = { x: e.clientX, y: e.clientY };
};

container.onmouseup = function () {
	isDragging = false;
};

container.onmousemove = function (e) {
	if (!isDragging) return;

	let sensitivity = 0.005;

	// update angles based on mouse movement
	theta -= (e.clientX - previousMousePosition.x) * sensitivity;
	phi   -= (e.clientY - previousMousePosition.y) * sensitivity;

	phi = Math.max(0.1, Math.min(Math.PI - 0.1, phi));

	// calculate new camera position
	camera.position.x = radius * Math.sin(phi) * Math.sin(theta);
	camera.position.z = radius * Math.sin(phi) * Math.cos(theta);
	camera.position.y = radius * Math.cos(phi);

	camera.lookAt(0, 0, 0);

	previousMousePosition = { x: e.clientX, y: e.clientY };
};

// if mouse is inside the container and scrolling
container.onwheel = function (e) {
	radius -= e.deltaY * 0.01;
	radius = Math.max(10, Math.min(50, radius));

	camera.position.x = radius * Math.sin(phi) * Math.sin(theta);
	camera.position.z = radius * Math.sin(phi) * Math.cos(theta);
	camera.position.y = radius * Math.cos(phi);

	camera.lookAt(0, 0, 0);
};

container.addEventListener('wheel', function (event) {
    event.preventDefault();
}, { passive: false });

container.addEventListener('touchmove', function (event) {
    event.preventDefault();
}, { passive: false });

// resize canvas on window resize
window.addEventListener('resize', function () {
	renderer.setSize(container.clientWidth, container.clientHeight);
	camera.aspect = container.clientWidth / container.clientHeight;
	camera.updateProjectionMatrix();
});

function animate() {
    requestAnimationFrame(animate);

    ball.rotation.z += 0.1;

    renderer.render(scene, camera);
}

camera.position.z = 15;
camera.position.y = 2;
camera.lookAt(0, 0, 0);

animate();

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
		var oldScripts = document.querySelectorAll("script.match-script");
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
	var data = JSON.parse(event.data);
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
		ball.position.x = data.ball[0] / 5 - 10;
		ball.position.z = data.ball[1] / 5 - 10;
	}
}

function sequelInitMatchWs(socket) {
	var [waiting, end] = [
		document.getElementById("waiting"),	document.getElementById("end")];
	let waitingState = ["waiting"];
	socket.onmessage = event => onMatchWsMessage(
		event, [waiting, end], waitingState);
	setCommands(socket);
	var spec = document.getElementById("spec")
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
