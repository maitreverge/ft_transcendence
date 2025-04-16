document.addEventListener("DOMContentLoaded", function () {
	initializeCharts();
});

document.body.addEventListener("htmx:afterSwap", function () {
  initializeCharts();
});

document.body.addEventListener("htmx:load", function () {
  initializeCharts();
});

// Helper function to initialize charts
function initializeCharts() {
    const gamesPie = document.getElementById("gamesPie")?.getContext("2d");
    const pointsPie = document.getElementById("pointsPie")?.getContext("2d");

    // Get the data from the JSON script
    const mainStats = JSON.parse(
      document.getElementById("mainStats").textContent
    );

    if (gamesPie && pointsPie) {
      const gamesPlayed = mainStats.games_played;
      const gamesWon = mainStats.games_won;
      const gamesLost = mainStats.games_lost;
      const winRate = mainStats.win_rate;
      const averageScore = mainStats.average_score;
      const pointsScored = mainStats.points_scored;
      const pointsConceded = mainStats.points_conceded;

      function addDummyIfZero(data, labels) {
        if (data.every((value) => value === 0)) {
          data.push(1); // dummy value to ensure doughnut doesn't collapse
          labels.push("No Data"); // dummy label for the dummy value
        }
      }

      // Games Won/Lost Data
      const gamesData = [gamesWon, gamesLost];
      const gamesLabels = ["Games Won", "Games Lost"];
      addDummyIfZero(gamesData, gamesLabels);

      // Points Scored/Conceded Data
      const pointsData = [pointsScored, pointsConceded];
      const pointsLabels = ["Points Scored", "Points Conceded"];
      addDummyIfZero(pointsData, pointsLabels);

      // Options for the charts
      const chartOptions = {
        maintainAspectRatio: false,
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          borderColor: "#5a5c69",
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          caretPadding: 10,
          filter: function (item, chart) {
            return chart.labels[item.index] !== "No Data";
          },
        },
        legend: {
          display: false,
          labels: {
            filter: (item) =>
              item.text !== undefined && item.text !== "No Data",
          },
        },
        cutoutPercentage: 80,
        animation: {
          animateScale: true,
          animateRotate: true,
        },
        responsive: true,
      };

      // Create the Games Won/Lost Pie Chart
      new Chart(gamesPie, {
        type: "doughnut",
        data: {
          labels: gamesLabels,
          datasets: [
            {
              data: gamesData,
              backgroundColor: ["#007bff", "#ff4d4d"],
              hoverBorderColor: "#5a5c69",
              borderColor: "#5a5c69",
              borderWidth: 2,
            },
          ],
        },
        options: chartOptions,
      });

      // Create the Points Scored/Conceded Pie Chart
      new Chart(pointsPie, {
        type: "doughnut",
        data: {
          labels: pointsLabels,
          datasets: [
            {
              data: pointsData,
              backgroundColor: ["#007bff", "#ff4d4d"],
              hoverBorderColor: "#5a5c69",
              borderColor: "#5a5c69",
              borderWidth: 2,
            },
          ],
        },
        options: chartOptions,
      });
    }
}

window.initializeCharts = initializeCharts;