function applyTranslations(translations) {
    console.log("applyTranslations called");
    // console.log("Translations dans applyTranslations:", translations);
    // console.log("Translations:", translations); // Log les traductions
    // console.log("Type de translations:", Array.isArray(translations) ? "Tableau" : "Objet");
    // console.log("Premier élément si c'est un tableau:", translations[0]);
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        // console.log(`Clé recherchée: ${key}`); // Log la clé recherchée
        // console.log(`|${key}|`); // Encadre la clé avec des |
        // console.log(`|${Object.keys(translations).join('|')}|`); // Liste des clés existantes

        if (translations[key]) {
            // console.log(`Traduction trouvée pour ${key}: ${translations[key]}`); // Log la traduction
            element.innerText = translations[key];  // Applique la traduction
        } else {
            // console.log("Translations AGAIN:", translations); // Log les traductions
            // console.log(`Pas de traduction trouvée pour ${key}`);
        }
    });
}


// Fonction de gestion du changement de langue
function changeLanguage(event) {
    // console.log("changeLanguage called");
    const lang = event.target.value;
    localStorage.setItem('preferred_language', lang);
    loadTranslations(lang);
}

window.onload = function() {
    const lang = localStorage.getItem('preferred_language') || 'en';
    document.getElementById('language-selector').value = lang;
    loadTranslations(lang);
};

async function loadTranslations(lang) {
    try {
        console.log(    "loadTranslations called");
        const response = await fetch(`/translations/${lang}.json`);
        let translations = await response.json();
        // console.log("Type de translations:", typeof translations);
        // console.log("Valeur brute de translations:", translations);
        console.log("before try catch");

        try {
            translations = JSON.parse(translations);
            // console.log("Après parse:", translations);
        } catch (error) {
            console.error("Erreur JSON.parse:", error);
        }
        console.log("after try catch");

        // console.log("Translations:", translations); // Log les traductions
        // console.log(translations["welcome"]); // Devrait afficher "Welcome"
        // console.log(translations.welcome);
        applyTranslations(translations);
    } catch (error) {
        // console.error("Erreur lors du chargement des traductions:", error);
    }
}
