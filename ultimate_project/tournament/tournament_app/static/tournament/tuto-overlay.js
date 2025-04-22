window.addEventListener("DOMContentLoaded", () => {
    let lastVisitedPage = history.state?.lastVisitedPage || sessionStorage.getItem("lastVisitedPage");

    console.log("Dernière page visitée:", lastVisitedPage);
    console.log("Page actuelle:", window.location.href);

    // Vérifie si une page précédente existe et si l'URL actuelle n'est pas celle de la page d'erreur
    if (lastVisitedPage && window.location.href === lastVisitedPage && !sessionStorage.getItem("redirected")) {
        console.log("Redirection vers la dernière page visitée :", lastVisitedPage);
        
        // Marque que la redirection a eu lieu pour éviter la boucle infinie
        sessionStorage.setItem("redirected", "true");

    } else {
        sessionStorage.removeItem("redirected");
        console.log("Aucune page précédente trouvée ou déjà sur la page visitée.");
    }
});

function replayTuto() {
    const overlay = document.getElementById('tuto-overlay');
    console.log("enter replay tuto func");
    if (!overlay) return;
    console.log("overlay found");

    overlay.style.display = 'flex';
    localStorage.removeItem('tutoSimpleMatchSeen');
}

function showTutoOverlayIfFirstTime() {
    const overlay = document.getElementById('tuto-overlay');
    if (!overlay) return;

    const matchAlreadySeen = localStorage.getItem('tutoSimpleMatchSeen');
    const TournamentAlreadySeen = localStorage.getItem('tutoTournamentSeen');
    
    if (!matchAlreadySeen && window.location.href.includes('simple-match')) {
    // if (matchAlreadySeen && window.location.href.includes('simple-match')) {
        overlay.style.display = 'flex';

        overlay.addEventListener('click', () => {
            overlay.style.display = 'none';
            localStorage.setItem('tutoSimpleMatchSeen', 'true');
        });
    }
    if (!TournamentAlreadySeen && window.location.href.includes('tournament/tournament')) {
    // if (TournamentAlreadySeen && window.location.href.includes('tournament/tournament')) {
        overlay.style.display = 'flex';

        overlay.addEventListener('click', () => {
            overlay.style.display = 'none';
            localStorage.setItem('tutoTournamentSeen', 'true');
        });
    }


}

showTutoOverlayIfFirstTime();