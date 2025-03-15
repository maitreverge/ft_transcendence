/**
 * Common authentication functionality shared between login and register pages
 */

// Global flags to track script initialization
window.loginInitialized = false;
window.registerInitialized = false;

// HTMX event handling for page transitions - this is the key event for HTMX navigation
document.addEventListener('htmx:afterSwap', function(event) {
  console.log('HTMX Content Swap: Page content swapped to:', window.location.pathname);
  
  // Determine which page we're on after the swap and initialize appropriate scripts
  setTimeout(function() {
    initializePageScripts();
  }, 50); // Small delay to ensure DOM is ready
});

// Also initialize on DOMContentLoaded for initial page load
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOMContentLoaded: Initial page load of:', window.location.pathname);
  initializePageScripts();
});

// Function to initialize scripts based on current page
function initializePageScripts() {
  const path = window.location.pathname;
  
  // First check if we're on the login page
  if (path.includes('login')) {
    // Reset register initialization
    window.registerInitialized = false;
    
    // Initialize login page if not already initialized
    if (!window.loginInitialized && typeof initializeLoginPage === 'function') {
      console.log('Initializing login page scripts');
      window.loginInitialized = true;
      initializeLoginPage();
    }
  }
  
  // Check if we're on the register page
  else if (path.includes('register') || document.getElementById('first_name')) {
    // Reset login initialization
    window.loginInitialized = false;
    
    // Initialize register page if not already initialized
    if (!window.registerInitialized && typeof initializeRegisterPage === 'function') {
      console.log('Initializing register page scripts');
      window.registerInitialized = true;
      initializeRegisterPage();
    }
  }
  
  // For any other page, reset both
  else {
    window.loginInitialized = false;
    window.registerInitialized = false;
  }
}

// HTMX configuration to properly handle page transitions
htmx.config.historyEnabled = true;
htmx.config.defaultSwapStyle = 'outerHTML';
htmx.config.includeIndicatorStyles = true;

// Set up event listeners for various HTMX events for debugging
document.addEventListener('htmx:beforeSwap', function(evt) {
  console.log('htmx:beforeSwap triggered for target:', evt.detail.target);
});

document.addEventListener('htmx:afterRequest', function(evt) {
  console.log('htmx:afterRequest triggered for URL:', evt.detail.pathInfo.requestPath);
});

// Helper function to handle successful authentication
function handleAuthSuccess() {
  // Redirect to home on successful login/registration
  htmx.ajax("GET", "/home/", {
    target: "body",
    swap: "outerHTML",
    headers: { "HX-Login-Success": "true" },
  }).then(function () {
    history.pushState(null, "", "/home/");
  });
}

// Helper function to handle authentication errors
function handleAuthError(message, context) {
  let errorMessage = message || "An error occurred. Please try again.";
  
  // Format based on context if provided
  if (context === 'login') {
    errorMessage = "Login failed: Incorrect username or password.";
  } else if (context === 'register') {
    errorMessage = "Registration error: " + errorMessage;
  }
  
  // Show the alert
  alert(errorMessage);
} 