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

window.addEventListener('DOMContentLoaded', () => {

    const url = window.location.pathname;

        console.log ("HOLLLY shit! there is no navbar!");
        htmx.ajax('GET', url, {
        target: 'body',
        pushURL: url,
        headers: {
            'HX-Login-Success': 'true'
          }
        });
    

    // history.pushState(null, '', window.location.href);
    // handleNavigation();
    // history.replaceState(null, '', window.location.href);
 
  })
