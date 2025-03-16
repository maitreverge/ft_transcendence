/**
 * Login page functionality
 */

// Main initialization function that will be called by auth-common.js
function initializeLoginPage() {
  console.log("Login page initialization starting");
  
  // Set up event listener for form submission response
  document.addEventListener("htmx:beforeSwap", function handleLoginResponse(evt) {
    if (evt.detail.target.id === "register-form") {
      try {
        console.log("Processing login response:", evt.detail.xhr.responseText);
        const response = JSON.parse(evt.detail.xhr.responseText);

        if (response.success) {
          evt.detail.shouldSwap = false;
          // Use common function for successful authentication
          handleAuthSuccess();
        } else {
          // Use common function for authentication errors
          handleAuthError(response.message, 'login');
          
          // Return false to prevent the default swap
          evt.detail.shouldSwap = false;
        }
      } catch (e) {
        console.error("Error processing login response:", e);
      }
    }
  });
  
  console.log("Login page initialization complete");
}

// Legacy DOMContentLoaded handler - forwards to the new initialization function
document.addEventListener("DOMContentLoaded", function() {
  // We'll use this as a backup, but the main initialization should come through auth-common.js
  if (window.location.pathname.includes('login') && !window.loginInitialized) {
    initializeLoginPage();
    window.loginInitialized = true;
  }
}); 