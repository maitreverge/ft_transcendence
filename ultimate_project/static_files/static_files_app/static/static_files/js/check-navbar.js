document.body.addEventListener("htmx:afterSettle", () => {
    const navbarAbsent = !document.getElementById("navbar");
    const isHomeUrl = window.location.pathname === "/home/";

    if (navbarAbsent && isHomeUrl) {
        // console.log ("HOLLLY shit! there is no navbar!");
        htmx.ajax('GET', '/home/', {
        target: 'body',
        pushURL: '/home/',
        headers: {
            'HX-Login-Success': 'true'
          }
        });
    }
});