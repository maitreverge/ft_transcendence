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
        window.currentNav = item.querySelector('a'); // on garde une référence au lien entier
        window.applyBackground(bg);

    });
    item.addEventListener('mouseleave', () => {
        setFirstBgImage();
      });
});

function setFirstBgImage()
{
    window.currentBg = 'https://images.unsplash.com/photo-1501720804996-ae418d1ba820?q=80&w=3864&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D';
    window.applyBackground(window.currentBg);

}
window.addEventListener('DOMContentLoaded', () => {
    // console.log("%%%%%%%% func onload executed %%%%%%%%");
    setFirstBgImage();
    
});

document.body.addEventListener('htmx:afterSwap', () => {
    console.log("%%%%%%%% HTMX content swapped %%%%%%%%");
    if (!window.currentBg)
        setFirstBgImage();
    else {
        // Attendre un court instant avant d'appliquer l'image de fond
        setTimeout(() => {
            window.applyBackground(window.currentBg); // Réappliquer l'image de fond
        }, 100); // Attendre 100ms avant d'appliquer l'image de fond
    }
});

if (typeof window.currentBg == 'undefined')
{
    setFirstBgImage();
    window.applyBackground(window.currentBg);
}



