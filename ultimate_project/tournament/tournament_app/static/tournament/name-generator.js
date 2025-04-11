        // Liste de prénoms
        const names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ian", "Jack"];

        // Fonction pour générer un prénom aléatoire
        function getRandomName() {
            const randomIndex = Math.floor(Math.random() * names.length);
            return names[randomIndex];
        }

        // Fonction d'initialisation au chargement de la page
        window.onload = function() {
            // Remplir le champ d'input avec un prénom aléatoire au chargement
            document.getElementById('player-name').value = getRandomName();
        };

        // Fonction appelée lors du clic sur le bouton
        function newPlayer(socket) {
            // Remplir le champ d'input avec un prénom aléatoire à chaque clic
            document.getElementById('player-name').value = getRandomName();
            
            // Ton code pour ajouter un joueur...
            console.log("Ajout d'un joueur via socket:", socket);
        }