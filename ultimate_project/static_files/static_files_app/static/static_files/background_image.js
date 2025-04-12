document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
        const bg = item.getAttribute('data-bg');
        const main = document.getElementById('main_content');
        main.style.backgroundImage = `url(${bg})`;
        main.style.backgroundSize = 'cover';
        main.style.backgroundPosition = 'center';
        main.style.transition = 'background-image 0.3s ease';
    });
});