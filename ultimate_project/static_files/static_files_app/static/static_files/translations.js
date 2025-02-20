function applyTranslations(translations) {
    const lang = localStorage.getItem("preferred_language") || "en";
    document.documentElement.lang = lang;
    
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[key]) {
            console.log("content:" + element.innerText);
            element.innerText = translations[key];
        }
    });
}


function changeLanguage(event) {
    const lang = event.target.value;
    localStorage.setItem('preferred_language', lang);
    loadTranslations(lang);
}

function observeDOMChanges() {
    const observer = new MutationObserver((mutationsList) => {
        for (const mutation of mutationsList) {
            if (mutation.type === "childList" || mutation.type === "subtree") {
                console.log("Changement détecté dans le DOM, application des traductions...");
                console.log("type:", typeof window.currentTranslations);
                
                const lang = localStorage.getItem('preferred_language') || 'en';

                if (window.currentTranslations) {
                    observer.disconnect(); // Désactiver temporairement l'observer pour éviter la boucle
                    applyTranslations(window.currentTranslations);
                    observer.observe(document.body, { childList: true, subtree: true }); // Réactiver après modif
                }
            }
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
}


window.onload = function() {
    console.log("onload called");
    const lang = localStorage.getItem('preferred_language') || 'en';
    document.getElementById('language-selector').value = lang;
    loadTranslations(lang);
    observeDOMChanges();
};

async function loadTranslations(lang) {
    try {
        const response = await fetch(`/translations/${lang}.json`);
        let translations = await response.json();
        try {
            translations = JSON.parse(translations);
        } catch (error) {
            console.error("Error JSON.parse:", error);
        }
        window.currentTranslations = translations;
        applyTranslations(translations);
    } catch (error) {
        console.error("Error while loading translation:", error);
    }
}
