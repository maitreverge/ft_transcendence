window.currentBg = null; // Variable pour stocker l'image de fond actuelle

// Applique l'image de fond et les styles au chargement ou après un swap HTMX
if (typeof window.applyBackground === 'undefined') {
    // Fonction pour appliquer l'image de fond
    window.applyBackground = (bg) => {
        const main = document.getElementById('main_content');
        if (main && bg) {
            main.style.backgroundImage = `url(${bg})`;
            main.style.backgroundSize = 'cover';
            main.style.backgroundPosition = 'center';
            main.style.transition = 'background-image 0.3s ease';
        }
    };
}


document.querySelectorAll('.side-nav').forEach(item => {
    item.addEventListener('mouseenter', () => {
        const bg = item.getAttribute('data-bg');
        // console.log("bg 1: ", bg)
        window.currentBg = bg;
        const main = document.getElementById('main_content');
        main.style.backgroundImage = `url(${bg})`;
        main.style.backgroundSize = 'cover';
        main.style.backgroundPosition = 'center';
        main.style.transition = 'background-image 0.3s ease';
    });
});

window.addEventListener('DOMContentLoaded', () => {
    // console.log("%%%%%%%% func onload executed %%%%%%%%");
    const firstItem = document.querySelector('.side-nav');
    // console.log("first item: ", firstItem);
    
    if (firstItem) {
        // console.log("%%%%%%%% first item found %%%%%%%%");

        const bg = firstItem.getAttribute('data-bg');
        window.currentBg = bg;
        // console.log("bg 2: ", bg)
        const main = document.getElementById('main_content');
        main.style.backgroundImage = `url(${bg})`;
        main.style.backgroundSize = 'cover';
        main.style.backgroundPosition = 'center';
        main.style.transition = 'background-image 0.3s ease';
    }
});

document.body.addEventListener('htmx:afterSwap', () => {
    // console.log("%%%%%%%% HTMX content swapped %%%%%%%%");
    if (currentBg) {
        applyBackground(window.currentBg);
     } // Réapplique l'image de fond stockée
    // Si tu as des styles CSS spécifiques qui ne sont pas appliqués, tu peux les réinitialiser ici
});