window.addEventListener("DOMContentLoaded", () => {
    let lastVisitedPage = history.state?.lastVisitedPage || sessionStorage.getItem("lastVisitedPage");

    console.log("Dernière page visitée:", lastVisitedPage);
    console.log("Page actuelle:", window.location.href);

    if (lastVisitedPage && window.location.href === lastVisitedPage && !sessionStorage.getItem("redirected")) {
        console.log("Redirection vers la dernière page visitée :", lastVisitedPage);
        
        sessionStorage.setItem("redirected", "true");

    } else {
        sessionStorage.removeItem("redirected");
        console.log("Aucune page précédente trouvée ou déjà sur la page visitée.");
    }
});

function replayTuto() {
    const steps = [
    {
            title: '🎮 MATCH TUTORIAL 🎮',
            html: "<p data-translate=\"tuto_match_1\">In the next steps, you\'ll learn how to play Simple Matches.</p>",
            // text: 'In the next steps, you\'ll learn how to play Simple Matches',
            imageUrl: 'https://dansylvain.github.io/pictures/tuto.webp',
            imageWidth: 800,
        },
        {
            title: 'STEP 1',
            html: "<p data-translate=\"tuto_match_2\">Enter a name for your local opponant.</p>",
            // text: 'Enter a name for your local opponant',
            imageUrl: 'https://dansylvain.github.io/pictures/match_1.png',
            imageWidth: 1200,
        },
        {
            title: 'STEP 2',
            html: "<p data-translate=\"tuto_match_3\">Add the player, which launches a local match.</p>",
            // text: 'Add the player, which launches a local match.',
            imageUrl: 'https://dansylvain.github.io/pictures/match_2.png',
            imageWidth: 1200,
        },
        {
            title: 'STEP 3',
            html: "<p data-translate=\"tuto_match_4\">Click on your local match to fight!</p>",
            // text: 'Click on your local match to fight!',
            imageUrl: 'https://dansylvain.github.io/pictures/match_3.png',
            imageWidth: 1200,
        }

        // Add more steps here if needed!
    ];

    let currentStep = 0;

    const showStep = (index) => {
        const step = steps[index];
        const swalConfig = {
            title: step.title,
            imageUrl: step.imageUrl,
            imageWidth: step.imageWidth,
            imageHeight: step.imageHeight,
            width: 'auto',         // Let popup size adjust to content
            heightAuto: true,
    
            // ✅ Always show Cancel button except on the first step
            showCancelButton: index > 0,
    
            // ✅ Only show Confirm button if not on the last step
            showConfirmButton: index < steps.length - 1,
            confirmButtonText: 'Next →',
            cancelButtonText: '← Back',
    
            // ✅ Show a "Finish" button if on last step
            footer: index === steps.length - 1 ? '<button class="swal2-confirm swal2-styled" onclick="Swal.close()">Finish</button>' : ''
        };
    
        // Use html if available, otherwise use text
        if (step.html) {
            swalConfig.html = step.html;
        } else {
            swalConfig.text = step.text;
        }
    
        Swal.fire(swalConfig).then((result) => {
            if (result.isConfirmed && index < steps.length - 1) {
                showStep(index + 1);
            } else if (result.dismiss === Swal.DismissReason.cancel && index > 0) {
                showStep(index - 1);
            }
        });
    };
    showStep(currentStep);
}

if (!localStorage.getItem("tuto_completed_match")) {
    replayTuto();
    localStorage.setItem("tuto_completed_match", "true");
}
