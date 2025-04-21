  // this function is part of the history logic
  window.addEventListener("beforeunload", () => {
    // console.log("URL sauvegardée avec history.state et sessionStorage");
    stopMatchHtmx();
    let currentURL = window.location.href;
    history.replaceState({ lastVisitedPage: currentURL }, "");
    sessionStorage.setItem("lastVisitedPage", currentURL);
  });

  function stopMatchHtmx() {
    fetch(`/match/stop-match/${window.selfId}/${window.selfMatchId}/`)
      .then(response => {
        if (!response.ok)
          throw new Error(`Error HTTP! Status: ${response.status}`);
        return response.text();
      })
      // .then(data => console.log(data))
      .catch(error => console.log(error))
  }

  function closeWebsockets() {

    // console.log("########### closing websockets #######");
    if (typeof closeSimpleMatchSocket === "function") closeSimpleMatchSocket();
    if (typeof closeTournamentSocket === "function") closeTournamentSocket();
    
  }

  closeWebsockets();
  function interceptUrlChanges() {
    const originalReplaceState = history.replaceState;

    history.replaceState = function (state, title, url) {
      originalReplaceState.apply(history, arguments);
      closeWebsockets();
    };
  }

  interceptUrlChanges();

  function handleNavigation(event) {
    alert("truc: " + JSON.stringify(event));
    console.log('***************************** Navigation event *************************');
  }
  
  // Se déclenche sur back/forward
  window.addEventListener('popstate', handleNavigation);
  
  // Se déclenche au rechargement initial
  window.addEventListener('DOMContentLoaded', handleNavigation);
