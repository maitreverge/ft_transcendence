const socket = new WebSocket("ws://localhost:8080/ws/somepath/");  // Établit la connexion websocket

socket.onopen = () => {
  console.log("Connexion établie 😊");
};

socket.onmessage = (event) => {
  console.log("Message reçu :", event.data);
};
