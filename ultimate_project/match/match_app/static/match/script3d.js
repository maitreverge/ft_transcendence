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

function onMatchWsMessage(event, [waiting, end], waitingState) {
	const data = JSON.parse(event.data);

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

	if (data.yp1 !== undefined && data.yp2 !== undefined) {
        console.log("data.yp1: ", data.yp1);
		window.r1.position.x = data.yp1 - 20;
		window.r2.position.x = data.yp2 - 20;
		window.ball.position.z = data.ball[0] / 4 - 10;
		window.ball.position.x = data.ball[1] / 4 - 6;
	}
}

function sequelInitMatchWs(socket) {
	const [waiting, end] = [		
		document.getElementById("waiting"),	document.getElementById("end")];	
	let waitingState = ["waiting"];

	socket.onmessage = event => onMatchWsMessage(
		event, [waiting, end], waitingState);

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

    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
        window.pidom = "localhost:8443";
	else
		window.pidom = window.location.hostname + ":8443";

    window.matchSocket2 = new WebSocket(
        `wss://${window.pidom}/ws/match/${window.matchId}/` +
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
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
        window.pidom = "localhost:8443";
	else
		window.pidom = window.location.hostname + ":8443";

//si je viens du debut je sui sclosé (et je reviens par boucle) si je viens de onclse je continu normal
	console.log("INIT MATCH 😊😊😊");
	console.log("STOP: " + window.stopFlag);
	console.log("ANTILOPP: " + window.antiLoop);
	if (window.matchSocket && window.antiLoop)
		return window.matchSocket.close();
    // if (window.matchSocket)
	// 	window.matchSocket.close();
	window.antiLoop = true;
    window.matchSocket = new WebSocket(
        `wss://${window.pidom}/ws/match/${window.matchId}/` +
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
