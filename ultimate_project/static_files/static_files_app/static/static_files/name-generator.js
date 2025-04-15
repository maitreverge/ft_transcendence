if (!window.nameGeneratorLoaded) {
    window.nameGeneratorLoaded = true;

    window.usedNames = window.usedNames || new Set();

    function generateRandomName() {
    const names = [
    'Neo',
    'Trinity',
    'Link',
    'Mario',
    'Cortana',
    'Ada',
    'Bilbo',
    'Gandalf',
    'Tux',
    'Woz',
    'Jedi',
    'Spock',
    'R2D2',
    'Yoshi',
    'Lain',
    ];    const availableNames = names.filter(name => !window.usedNames.has(name));

        if (availableNames.length === 0) {
            return 'Player' + Math.floor(Math.random() * 1000); // fallback si tous les noms sont pris
        }

        const index = Math.floor(Math.random() * availableNames.length);
        return availableNames[index];
    }


    function prefillName() {
        const input = document.getElementById('player-name');
        if (input)
            input.value = generateRandomName();
    }

    window.addEventListener('DOMContentLoaded', () => {
        document.body.addEventListener('htmx:afterSwap', (e) => {
            // Si le champ #player-name est dans la réponse HTMX, on préremplit
            if (document.getElementById('player-name')) {
                prefillName();
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });

        prefillName();
    });



    const observer = new MutationObserver((mutationsList) => {
        for (const mutation of mutationsList) {
            for (const node of mutation.addedNodes) {
                if (
                    node.nodeType === 1 &&
                    node.classList.contains('swal2-container') &&
                    node.textContent.includes('won the tournament!')
                ) {
                    console.log('Tournoi terminé, reset des noms...');
                    window.usedNames.clear();
                }
            }
        }
    });

}