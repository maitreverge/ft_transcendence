function logoutUser() {
    // Create a fetch request to logout endpoint
    fetch("/auth/logout/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin", // Important for cookies
    }).then((response) => {
      htmx
        .ajax("GET", "/login/", {
          target: "body",
          swap: "outerHTML",
          headers: { "HX-Login-Success": "true" },
        })
        .then(function () {
          history.pushState(null, "", "/login/");
        });
    });
  }