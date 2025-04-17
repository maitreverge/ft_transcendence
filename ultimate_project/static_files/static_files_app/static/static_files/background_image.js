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
    const text = document.querySelector('.myText');
    console.log("FUNC CALLED");
    console.log(text);

    item.addEventListener('mouseenter', () => {
        if (text) text.style.opacity = '0';
        const bg = item.getAttribute('data-bg');
        // console.log("bg 1: ", bg)
        window.currentBg = bg;
        window.currentNav = item.querySelector('a');
        window.applyBackground(bg);

    });
    item.addEventListener('mouseleave', () => {
        if (text) text.style.opacity = '1';
        setFirstBgImage();
      });
});

function setFirstBgImage()
{
    window.currentBg = 'https://dansylvain.github.io/pictures/marvin_warm.png';
    window.applyBackground(window.currentBg);

}
window.addEventListener('DOMContentLoaded', () => {
    // console.log("%%%%%%%% func onload executed %%%%%%%%");
    setFirstBgImage();
    
});

document.body.addEventListener('htmx:afterSwap', () => {
    // console.log("%%%%%%%% HTMX content swapped %%%%%%%%");
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



