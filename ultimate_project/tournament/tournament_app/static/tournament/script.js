
document.getElementById("new-match").addEventListener("click", function(event) {
	event.preventDefault();
	console.log("ta bien clique man");
	fetch('http://localhost:8000/match/new-match/').then(response => response.json()).then(data => console.log(data)).catch(error => console.error(error))
});