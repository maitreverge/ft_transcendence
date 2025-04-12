document.querySelectorAll('.side-nav').forEach(item => {
    item.addEventListener('mouseenter', () => {
        const bg = item.getAttribute('data-bg');
        console.log("bg 1: ", bg)

        const main = document.getElementById('main_content');
        main.style.backgroundImage = `url(${bg})`;
        main.style.backgroundSize = 'cover';
        main.style.backgroundPosition = 'center';
        main.style.transition = 'background-image 0.3s ease';
    });
});

window.addEventListener('DOMContentLoaded', () => {
    console.log("%%%%%%%% func onload executed %%%%%%%%");
    const firstItem = document.querySelector('.side-nav');
    console.log("first item: ", firstItem);
    
    if (firstItem) {
        console.log("%%%%%%%% first item found %%%%%%%%");

        const bg = firstItem.getAttribute('data-bg');
        console.log("bg 2: ", bg)
        const main = document.getElementById('main_content');
        main.style.backgroundImage = `url(${bg})`;
        main.style.backgroundSize = 'cover';
        main.style.backgroundPosition = 'center';
        main.style.transition = 'background-image 0.3s ease';
    }
});

document.body.addEventListener('htmx:afterSwap', () => {
    console.log("%%%%%%%% HTMX content swapped %%%%%%%%");
    // Si tu as des styles CSS spécifiques qui ne sont pas appliqués, tu peux les réinitialiser ici
});