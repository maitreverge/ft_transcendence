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

    const alreadySeen = localStorage.getItem('tutoSimpleMatchSeen');
    //! if (!alreadySeen) { exchange the two lines to activate tutorial
    if (alreadySeen) {
        overlay.style.display = 'flex';

        overlay.addEventListener('click', () => {
            overlay.style.display = 'none';
            localStorage.setItem('tutoSimpleMatchSeen', 'true');
        });
    }
}

showTutoOverlayIfFirstTime();


document.addEventListener("DOMContentLoaded", () => {
    const switcherElementContainer = document.getElementById('side-nav-2d3d');
    const mainContentContainer = document.getElementById('mainContentContainer');
    const switcherElement = document.getElementById('switch2d3d');
    
    function moveSideNavElement() {
        const windowWidth = window.innerWidth; // Obtenir la largeur du viewport

        // Si la largeur est <= 576px, déplace l'élément dans le main container
        if (windowWidth <= 576) {
            if (!mainContentContainer.contains(switcherElement)) {
                mainContentContainer.appendChild(switcherElement); // Déplacer l'élément vers le main container
            }
        } else { 
            // Si la largeur est > 576px, déplace l'élément dans la sidebar
            if (!switcherElementContainer.contains(switcherElement)) {
                switcherElementContainer.appendChild(switcherElement); // Déplacer l'élément vers la sidebar
            }
        }
    }

    // Vérifier la position initiale et la déplacer en fonction de la taille de l'écran
    moveSideNavElement();

    // Ajouter un écouteur d'événements pour surveiller le redimensionnement de la fenêtre
    window.addEventListener('resize', moveSideNavElement);
});