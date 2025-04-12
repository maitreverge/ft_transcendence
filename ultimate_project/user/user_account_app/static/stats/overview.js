/* JS for the overview page */
document.addEventListener("DOMContentLoaded", function () {
	const gamesPie = document.getElementById("gamesPie")?.getContext("2d");
	const pointsPie = document.getElementById("pointsPie")?.getContext("2d");
  
	if (gamesPie && pointsPie && window.stats) {
	  new Chart(gamesPie, {
		type: "doughnut",
		data: {
		  labels: ["Games Won", "Games Lost"],
		  datasets: [{
			data: [window.stats.gamesWon, window.stats.gamesPlayed - window.stats.gamesWon],
			backgroundColor: ["#28a745", "#e0e0e0"],
			borderWidth: 0
		  }]
		},
		options: {
		  cutout: "70%",
		  plugins: { legend: { display: false } }
		}
	  });
  
	  new Chart(pointsPie, {
		type: "doughnut",
		data: {
		  labels: ["Points Scored", "Points Conceded"],
		  datasets: [{
			data: [window.stats.pointsScored, window.stats.pointsConceded],
			backgroundColor: ["#007bff", "#ffc107"],
			borderWidth: 0
		  }]
		},
		options: {
		  cutout: "70%",
		  plugins: { legend: { display: false } }
		}
	  });
	}
  });
  

