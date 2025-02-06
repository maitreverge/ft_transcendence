
// const socket = new WebSocket("ws://localhost:8000/ws/somepath/");
// const socket = new WebSocket( window.rasp + "/ws/somepath/");

if (window.rasp == "true")
	socket = new WebSocket(`wss://${window.pidom}/ws/somepath/`);
else
	socket = new WebSocket("ws://localhost:8000/ws/somepath/");

socket.onopen = () => {
  console.log("Connexion établie 😊");
};

socket.onmessage = (event) => {
  console.log("Message reçu :", event.data);
};