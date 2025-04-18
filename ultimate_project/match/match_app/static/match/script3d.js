// ! ====================================================== SEB DIFFERENCE ======================================================
var tjs_keyup = null;
var tjs_keydown = null;
var is_towplayer = false;
// ! ====================================================== SEB DIFFERENCE ======================================================

function stopEventListener3D() {
    if (tjs_keyup)
        document.removeEventListener("keyup", tjs_keyup);
    if (tjs_keydown)
        document.removeEventListener("keydown", tjs_keydown);
    tjs_keyup = null;
    tjs_keydown = null;
}

function quitMatch3D()
{
    stopEventListener3D();
	document.body.classList.remove("match-active");
	cancelAnimationFrame(window.pongAnim);	
	closeWebSocket3D(window.matchSocket);
	closeWebSocket3D(window.matchSocket2);
	delMatchScript3D();
	delMatch3D();
}

function closeWebSocket3D(socket)
{
	if (socket && socket.readyState === WebSocket.OPEN)
	{		
		window.stopFlag = true
		socket.close(3666);		
	} 
}

function delMatchScript3D()
{
	const scripts = document.querySelectorAll("script.match-script");		
	scripts.forEach(oldScript => oldScript.remove());	
}

function delMatch3D()
{
	const matchDiv = document.getElementById('match');
    if (matchDiv)
		matchDiv.remove();
    const rulesOverlay = document.getElementById('rules-overlay');
    if (rulesOverlay)
		rulesOverlay.style.display = 'none';
}

function stopMatch3D(matchId) {
    // unregister the event listeners
    window.gameInProgress = false;
	document.body.classList.remove("match-active");
	cancelAnimationFrame(window.pong3DAnim);
	const input = document.getElementById("match-player-name");
	
    if (tjs_keyup)
        document.removeEventListener("keyup", tjs_keyup);
    if (tjs_keydown)
        document.removeEventListener("keydown", tjs_keydown);

    stopEventListener3D();
	document.body.classList.remove("match-active");

    if (!matchId)
    {
        console.log("matchID EST NULLE");
        const oldScripts = document.querySelectorAll("script.match-script");
        console.log("olscript len", oldScripts.length);
        oldScripts.forEach(oldScript =>{console.log("old: ", oldScript.src); oldScript.remove()});
        return;
    }

    if (window.selfMatchId == matchId)
    {
        fetch(`/match/stop-match/${window.playerId}/${matchId}/`)
        .then(response => {
            if (!response.ok)
                throw new Error(`Error HTTP! Status: ${response.status}`);
            return response.text();
        })
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
				setTimeout(()=> {
					console.log("je sais pas ce qu eje fou la");
					if (window.matchSocket.readyState === WebSocket.OPEN)
					{
						console.log("je vais envoyer 42");
						window.stopFlag = true
						window.matchSocket.close(3666);
						if (window.matchSocket2)
							window.matchSocket2.close(3666);
					} 
					else 
					{
						console.log("La WebSocket était déjà fermée.");
					}
					console.log("je nai pas plante");
				}, 1000);
				// console.log("je sais pas ce qu eje fou la");
				// if (window.matchSocket.readyState === WebSocket.OPEN)
				// {
				// 	console.log("je vais envoyer 42");
				// 	window.stopFlag = true
				// 	window.matchSocket.close(3666);
				// 	if (window.matchSocket2)
				// 		window.matchSocket2.close(3666);
				// } 
				// else 
				// {
				// 	console.log("La WebSocket était déjà fermée.");
				// }
				// console.log("je nai pas plante");
			}
        console.log("toujours vivant");
        const oldScripts = document.querySelectorAll("script.match-script");
        console.log("olscript len", oldScripts.length);
        oldScripts.forEach(oldScript =>{console.log("old: ", oldScript.src); oldScript.remove()});
    // }
    // else
    //  console.log("pas spec!!");
}


// ? =============================== THREE JS ============================
window.tjs_container = document.getElementById('scene-container');

window.tjs_scene = new THREE.Scene();
window.tjs_camera = new THREE.PerspectiveCamera(75, window.tjs_container.clientWidth / window.tjs_container.clientHeight, 0.1, 1000);
window.tjs_renderer = window.tjs_renderer || new THREE.WebGLRenderer({ antialias: true });
window.tjs_renderer.setSize(window.tjs_container.clientWidth, window.tjs_container.clientHeight);
window.tjs_container.appendChild(window.tjs_renderer.domElement);

window.tjs_textureLoader = window.tjs_textureLoader || new THREE.TextureLoader();

window.tjs_rgeo = window.tjs_rgeo || new THREE.BoxGeometry(5, 5, 20 * (60 / 100));
window.tjs_sgeo = window.tjs_sgeo || new THREE.SphereGeometry(2, 32, 32);
window.tjs_tgeo = window.tjs_tgeo || new THREE.BoxGeometry(95, 5, 60);

function tjs_loadfull(url) {
    return [
        new THREE.MeshBasicMaterial({ map: window.tjs_textureLoader.load(url) }),
        new THREE.MeshBasicMaterial({ map: window.tjs_textureLoader.load(url) }),
        new THREE.MeshBasicMaterial({ map: window.tjs_textureLoader.load(url) }),
        new THREE.MeshBasicMaterial({ map: window.tjs_textureLoader.load(url) }),
        new THREE.MeshBasicMaterial({ map: window.tjs_textureLoader.load(url) }),
        new THREE.MeshBasicMaterial({ map: window.tjs_textureLoader.load(url) }),
    ]
}

window.tjs_tmat = tjs_loadfull('https://threejs.org/examples/textures/terrain/grasslight-big.jpg');
window.tjs_rmat = tjs_loadfull('https://threejs.org/examples/textures/hardwood2_diffuse.jpg');

window.tjs_smat = window.tjs_smat || new THREE.MeshBasicMaterial({ map: window.tjs_textureLoader.load('https://threejs.org/examples/textures/sprite.png') });

window.tjs_r1 = new THREE.Mesh(window.tjs_rgeo, window.tjs_rmat);
window.tjs_r2 = new THREE.Mesh(window.tjs_rgeo, window.tjs_rmat);

window.tjs_table = new THREE.Mesh(window.tjs_tgeo, window.tjs_tmat);
window.tjs_table.position.x = 48.75;
window.tjs_table.position.y = -5;
window.tjs_table.position.z = 30;

window.tjs_ball = new THREE.Mesh(window.tjs_sgeo, window.tjs_smat);

window.tjs_scene.add(window.tjs_ball);
window.tjs_scene.add(window.tjs_r1);
window.tjs_scene.add(window.tjs_r2);
window.tjs_scene.add(window.tjs_table);

window.tjs_r1.position.z = 0;
window.tjs_r1.position.y = 0;
window.tjs_r1.position.x = 5;

window.tjs_r2.position.z = 0;
window.tjs_r2.position.y = 0;
window.tjs_r2.position.x = 92.5;

window.tjs_ball.position.x = -1;
window.tjs_ball.position.z = -1;

window.tjs_upgrade = {
    user_lvl: 0,
    points: 0,
    cooldown: 10,
}

// ? =============================== THREE JS ============================


function actionCooldownUpdate() {
    const u = document.getElementById('upgrade');

    if (!u)
        return 0;

    // update the html button
    if (!window.tjs_upgrade.cooldown) {
        u.innerHTML = `Upgrade (+${window.tjs_upgrade.points})`;
    } else if (window.tjs_upgrade.points) {
        u.innerHTML = `Upgrade (+${window.tjs_upgrade.points}) ${window.tjs_upgrade.cooldown}s`;
    } else {
        u.innerHTML = `Upgrade ${window.tjs_upgrade.cooldown}s`;
    }

    return 1;
}

// function call on button click
function actionUpgrade() {
    if (window.tjs_upgrade.points < 1) {
        return;
    }
    window.tjs_upgrade.points--;
    switch (window.tjs_upgrade.user_lvl) {
        case 0:
            window.tjs_ball.material.color.setHex(0x00ff00);
            break;
        case 1:
            window.tjs_ball.material.color.setHex(0xffffff);
            window.tjs_ball.material.map = window.tjs_textureLoader.load('https://media.tenor.com/YkyhmCCJd_0AAAAM/aaaa.gif');
            break;
        case 2:
            window.tjs_table.material = tjs_loadfull('https://threejs.org/examples/textures/jade.jpg');
            break;
        case 3:
            window.tjs_table.material = tjs_loadfull('https://threejs.org/examples/textures/land_ocean_ice_cloud_2048.jpg');
            break;
        case 4:
            window.tjs_r1.material = tjs_loadfull('https://threejs.org/examples/textures/disturb.jpg');
            window.tjs_r2.material = tjs_loadfull('https://threejs.org/examples/textures/disturb.jpg');
            break;
        default:
            break;
    }
    window.tjs_upgrade.user_lvl++;
    actionCooldownUpdate();
}

// function call each seconds
function actionCooldown() {
    if (window.tjs_upgrade.cooldown > 0) {
        window.tjs_upgrade.cooldown--;
    } else {
        window.tjs_upgrade.cooldown = 10;
    }
    if (window.tjs_upgrade.cooldown == 0) {
        window.tjs_upgrade.points++;
    }
    if (actionCooldownUpdate())
        setTimeout(actionCooldown, 1000);
}

actionCooldownUpdate();
actionCooldown();

function doRotation() {
    window.tjs_phi = Math.max(0.1, Math.min(Math.PI - 0.1, window.tjs_phi));

    // calculate new camera position
    window.tjs_camera.position.x = window.tjs_radius * Math.sin(window.tjs_phi) * Math.sin(window.tjs_theta) + tjs_camera_offset_x;
    window.tjs_camera.position.z = window.tjs_radius * Math.sin(window.tjs_phi) * Math.cos(window.tjs_theta) + tjs_camera_offset_z;
    window.tjs_camera.position.y = window.tjs_radius * Math.cos(window.tjs_phi);

    window.tjs_camera.lookAt(tjs_camera_offset_x, 0, tjs_camera_offset_z);
}

function actionRestViewUP() {
    window.tjs_radius = 60;
    window.tjs_theta  = 0;   // horizontal angle
    window.tjs_phi    = 0;   // vertical angle
    doRotation();
}

function actionRestViewFPS() {
    window.tjs_radius = 90;
    window.tjs_theta  = Math.PI / 2;    // horizontal angle
    window.tjs_phi    = 1.3;            // vertical angle
    doRotation();
}

window.tjs_isDragging = false;
window.tjs_previous_mouse = { x: 0, y: 0 };

window.tjs_radius = window.tjs_radius || 50;

window.tjs_theta = window.tjs_theta || 0;   // horizontal angle
window.tjs_phi   = window.tjs_phi   || 0;   // vertical angle

window.tjs_container.onmousedown = function (e) {
    window.tjs_isDragging = true;
    window.tjs_previous_mouse = { x: e.clientX, y: e.clientY };
};

window.tjs_container.onmouseup = function () {
    window.tjs_isDragging = false;
};

window.tjs_container.onmousemove = function (e) {
    if (!window.tjs_isDragging)
        return;

    let sensitivity = 0.005;

    // update angles based on mouse movement
    window.tjs_theta -= (e.clientX - window.tjs_previous_mouse.x) * sensitivity;
    window.tjs_phi   -= (e.clientY - window.tjs_previous_mouse.y) * sensitivity;

    doRotation();

    // update previous mouse position
    window.tjs_previous_mouse = { x: e.clientX, y: e.clientY };
};

// if mouse is inside the container and scrolling
window.tjs_container.onwheel = function (e) {
    window.tjs_radius -= e.deltaY * 0.1;
    window.tjs_radius = Math.max(10, Math.min(500, window.tjs_radius));

    window.tjs_camera.position.x = window.tjs_radius * Math.sin(window.tjs_phi) * Math.sin(window.tjs_theta) + tjs_camera_offset_x;
    window.tjs_camera.position.z = window.tjs_radius * Math.sin(window.tjs_phi) * Math.cos(window.tjs_theta) + tjs_camera_offset_z;
    window.tjs_camera.position.y = window.tjs_radius * Math.cos(window.tjs_phi);

    window.tjs_camera.lookAt(tjs_camera_offset_x, 0, tjs_camera_offset_z);
};

window.tjs_container.addEventListener('wheel', function (event) {
    event.preventDefault();
}, { passive: false });

window.tjs_container.addEventListener('touchmove', function (event) {
    event.preventDefault();
}, { passive: false });

// resize canvas on window resize
window.addEventListener('resize', function () {
    window.tjs_renderer.setSize(window.tjs_container.clientWidth, window.tjs_container.clientHeight);
    window.tjs_camera.aspect = window.tjs_container.clientWidth / window.tjs_container.clientHeight;
    window.tjs_camera.updateProjectionMatrix();
});

function animate() {
    window.pong3DAnim = requestAnimationFrame(animate);

    window.tjs_ball.rotation.z += 0.1;

    window.tjs_renderer.render(window.tjs_scene, window.tjs_camera);
}

var tjs_camera_offset_x = 50;
var tjs_camera_offset_z = 30;

actionRestViewUP();
animate();

function setCommands3D(socket, socket2) {
    const keysPressed = {}; // Stocker les touches enfoncées
    let animationFrameId = null; // Stocke l'ID du requestAnimationFrame

    function sendCommands3D() {
        if (socket.readyState === WebSocket.OPEN) {
            if (keysPressed["ArrowUp"]) {
                socket.send(JSON.stringify({ action: 'move', dir: 'up' }));
            }
            if (keysPressed["ArrowDown"]) {
                socket.send(JSON.stringify({ action: 'move', dir: 'down' }));
            }
        }

        if (socket2 && socket2.readyState === WebSocket.OPEN) {
            is_towplayer = true;

            if (keysPressed["+"]) {
                socket2.send(JSON.stringify({ action: 'move', dir: 'up' }));
            }
            if (keysPressed["Enter"]) {
                socket2.send(JSON.stringify({ action: 'move', dir: 'down' }));
            }
        }

        animationFrameId = requestAnimationFrame(sendCommands3D); // Appelle la fonction en boucle
    }

    function handleKeyDown(event) {
        event.preventDefault();

        // Empêche d'ajouter plusieurs fois la même touche
        if (!keysPressed[event.key]) {
            keysPressed[event.key] = true;
        }

        // Démarre l'animation seulement si elle n'est pas déjà en cours
        if (!animationFrameId) {
            animationFrameId = requestAnimationFrame(sendCommands3D);
        }
    }

    // Ajoute l'écouteur d'événement
    document.addEventListener("keydown", handleKeyDown);
    tjs_keydown = handleKeyDown;

    function handleKeyUp(event) {
        // Supprime la touche du tableau
        delete keysPressed[event.key];

        // Si plus aucune touche n'est pressée, on stoppe l'animation
        if (Object.keys(keysPressed).length === 0) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    }

    // Ajoute l'écouteur d'événement
    document.addEventListener("keyup", handleKeyUp);
    tjs_keyup = handleKeyUp;
}

function startCountdown3D(delay)
{
    const countdownEl = document.getElementById("countdown3d");
    const countdownEndsAt = window.gameStartTimestamp * 1000 + delay * 1000;

	function updateCountdown3D() {
        const now = Date.now();
        const remaining = Math.ceil((countdownEndsAt - now) / 1000);

        if (remaining > 0) {
            countdownEl.textContent = remaining;
            requestAnimationFrame(updateCountdown3D);
        } else if (remaining > -1) {
            countdownEl.textContent = "GO!";
            requestAnimationFrame(updateCountdown3D);
        } else {
            countdownEl.textContent = "";
            window.gameStartTimestamp = undefined;
        }
    }

	updateCountdown3D();
}

function displayPlayersInfos3D(data, score_div)
{
	if (!data.names)
		return;
    score_div.innerText = data.score[0] + " | " + data.score[1];
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

function onMatchWsMessage3D(
    event, score_div, [waiting, endCont, end, spec], waitingState) {
    const data = JSON.parse(event.data);
    startDelay3D(data);
    displayPlayersInfos3D(data, score_div);
    setEnd3D(data, endCont, end, spec);
    setWaiting3D(data, waiting, waitingState);
	
    if (data.yp1 !== undefined && data.yp2 !== undefined) {
        window.tjs_r1.position.z = (60 / 100) * (data.yp1);
        window.tjs_r2.position.z = (60 / 100) * (data.yp2);

        window.tjs_ball.position.x = (100 / 100) * (data.ball[0] - 1);
        window.tjs_ball.position.z = (60 / 100) * (data.ball[1] - 1);
    }
}

function startDelay3D(data)
{
	if (data.timestamp && !data.state)
	{
		if (window.gameStartTimestamp === undefined)
		{
			window.gameStartTimestamp = data.timestamp;           
			console.log("✅ Premier timestamp enregistré:", data.timestamp);	
            startCountdown3D(data.delay);
		}
		else 
			console.log("⏩ Timestamp déjà reçu, ignoré.");		
		return;
	}
}

function setEnd3D(data, endCont, end, spec)
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

function setWaiting3D(data, waiting, waitingState)
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

function setSpec3D(spec)
{
	if (spec)
	{
		if (window.selfMatchId != window.matchId)
			spec.style.display = "block";
		else
			spec.style.display = "none";
	}
}

function sequelInitMatchWs3D(socket) {
    const [waiting, endCont, end] = [
		document.getElementById("waiting"),
        document.getElementById("end-cont"),
        document.getElementById("end")
    ];
	let waitingState = ["waiting"];
    const score_div = document.getElementById("score");
    const spec = document.getElementById("spec")
    setSpec3D(spec);
    socket.onmessage = event => onMatchWsMessage3D(
        event, score_div, [waiting, endCont, end, spec], waitingState);
    if (window.player2Id != 0)
		initSecPlayer3D();	
    setCommands3D(socket, window.matchSocket2);
}

function initSecPlayer3D() {

    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
        window.pidom = "localhost:8443";
	else
		window.pidom = window.location.hostname + ":8443";

    window.matchSocket2 = new WebSocket(
        `wss://${window.pidom}/ws/match/${window.matchId}/` +
        `?playerId=${window.player2Id}`);
	window.matchSocket2.onopen = () => {
		console.log("Connexion Match établie 2nd Player😊");
	};
	window.matchSocket2.onclose = (event) => {
		console.log("Connexion Match disconnected 😈 2nd Player");
	};
}

function initMatchWs3D() {
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
    if (window.matchSocket2 && window.antiLoop)
		return window.matchSocket2.close();
    // if (window.matchSocket)
    //     window.matchSocket.close();
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
            initMatchWs3D();
        }
        else
            console.log("code42");
        window.stopFlag = false;
    };
    sequelInitMatchWs3D(window.matchSocket);
}

initMatchWs3D();
