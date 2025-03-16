/**
 * Consolidated Authentication Script
 * Handles both login and register page functionality
 */

// Initialize the auth script when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('Auth script loaded, initializing...');
  initializeAuth();
});

// Also initialize on htmx content swaps
document.addEventListener('htmx:afterSwap', function(event) {
  console.log('HTMX Content Swap: Page content swapped to:', window.location.pathname);
  // Small delay to ensure DOM is ready
  setTimeout(initializeAuth, 50);
});

/**
 * Main initialization function that determines which page we're on
 * and sets up the appropriate functionality
 */
function initializeAuth() {
  // Get the page type from the data attribute
  const container = document.querySelector('.container[data-page-type]');
  
  if (!container) {
    console.log('No auth container found, skipping auth initialization');
    return;
  }
  
  const pageType = container.getAttribute('data-page-type');
  console.log(`Detected page type: ${pageType}`);
  
  // Initialize based on page type
  if (pageType === 'login') {
    initializeLoginPage();
  } else if (pageType === 'register') {
    initializeRegisterPage();
  } else {
    console.warn(`Unknown page type: ${pageType}`);
  }
  
  // Set up common HTMX configuration
  setupHtmxConfiguration();
}

/**
 * Set up common HTMX configuration
 */
function setupHtmxConfiguration() {
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
}

/**
 * Common function to handle successful authentication
 */
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

/**
 * Common function to handle authentication errors
 */
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

/************************************
 * LOGIN PAGE SPECIFIC FUNCTIONALITY
 ************************************/
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

/***************************************
 * REGISTER PAGE SPECIFIC FUNCTIONALITY
 ***************************************/
function initializeRegisterPage() {
  console.log("Register page initialization starting");
  
  // Check if we're actually on the register page
  if (!document.getElementById("first_name") && 
      !document.getElementById("password-strength-bar")) {
    console.log("Required register page elements not found, skipping initialization");
    return;
  }

  // Get all form elements
  const firstNameInput = document.getElementById("first_name");
  const lastNameInput = document.getElementById("last_name");
  const usernameInput = document.getElementById("username");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const repeatPasswordInput = document.getElementById("repeat_password");
  const emailError = document.getElementById("email-error");
  const passwordError = document.getElementById("password-error");
  const registerButton = document.getElementById("register-button");
  const form = document.querySelector("form.user");

  console.log("Register page elements:", {
    firstNameInput: !!firstNameInput,
    lastNameInput: !!lastNameInput,
    usernameInput: !!usernameInput,
    emailInput: !!emailInput,
    passwordInput: !!passwordInput,
    repeatPasswordInput: !!repeatPasswordInput,
    emailError: !!emailError,
    passwordError: !!passwordError,
    registerButton: !!registerButton,
    form: !!form
  });

  // Initialize password strength indicator if exists
  if (document.getElementById("password-strength-bar")) {
    updatePasswordStrengthIndicator(0);
  }

  // Email validation function
  function validateEmail(email) {
    const re =
      /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  }

  // Password strength calculation function
  function checkPasswordStrength(password) {
    if (!password) {
      return 0; // Empty password
    }
    
    let strength = 0;
    
    // Length check with adjusted thresholds (maximum 50 points)
    if (password.length > 12) {
      strength += 50; // Strong length (13+ chars)
    } else if (password.length >= 6) {
      strength += 30; // Medium length (6-12 chars)
    } else {
      strength += 10; // Weak length (1-5 chars)
    }
    
    // Character variety checks
    let varieties = 0;
    
    // Check for lowercase letters
    if (/[a-z]/.test(password)) {
      varieties++;
      strength += 10;
    }
    
    // Check for uppercase letters
    if (/[A-Z]/.test(password)) {
      varieties++;
      strength += 10;
    }
    
    // Check for numbers
    if (/\d/.test(password)) {
      varieties++;
      strength += 10;
    }
    
    // Check for special characters
    if (/[^A-Za-z0-9]/.test(password)) {
      varieties++;
      strength += 10;
    }
    
    // Bonus for variety (up to 10 points extra)
    if (varieties > 2) {
      strength += (varieties - 2) * 5;
    }
    
    // Cap at 100
    return Math.min(strength, 100);
  }
  
  // Update the password strength visual indicator
  function updatePasswordStrengthIndicator(strength) {
    const strengthBar = document.getElementById('password-strength-bar');
    const strengthText = document.getElementById('password-strength-text');
    
    if (!strengthBar || !strengthText) {
      console.log("Password strength indicators not found");
      return;
    }
    
    console.log("Updating password strength to:", strength);
    
    // Update progress bar width
    strengthBar.style.width = strength + '%';
    strengthBar.setAttribute('aria-valuenow', strength);
    
    // Update text and color based on strength
    if (strength === 0) {
      strengthBar.className = 'progress-bar';
      strengthText.textContent = 'Password strength: Not entered';
      strengthText.style.color = '#6c757d'; // Gray
    } else if (strength < 40) {
      strengthBar.className = 'progress-bar bg-danger';
      strengthText.textContent = 'Password strength: Weak';
      strengthText.style.color = '#dc3545'; // Red
    } else if (strength < 70) {
      strengthBar.className = 'progress-bar bg-warning';
      strengthText.textContent = 'Password strength: Moderate';
      strengthText.style.color = '#ffc107'; // Orange/Yellow
    } else {
      strengthBar.className = 'progress-bar bg-success';
      strengthText.textContent = 'Password strength: Strong';
      strengthText.style.color = '#28a745'; // Green
    }
  }

  // If email input exists, add event listener
  if (emailInput) {
    // Check email format
    emailInput.addEventListener("blur", function () {
      if (emailInput.value && !validateEmail(emailInput.value)) {
        emailError.style.display = "block";
      } else {
        emailError.style.display = "none";
      }
      validateForm();
    });
  }

  // Improved password check function
  function checkPasswords() {
    if (!passwordInput || !repeatPasswordInput || !passwordError) return true;

    // Both fields have values - check if they match
    if (passwordInput.value || repeatPasswordInput.value) {
      // At least one password field has a value
      if (passwordInput.value !== repeatPasswordInput.value) {
        // Passwords don't match - show error
        passwordError.style.display = "block";
        repeatPasswordInput.classList.add("is-invalid");
        return false;
      } else {
        // Passwords match - clear error
        passwordError.style.display = "none";
        repeatPasswordInput.classList.remove("is-invalid");
        return true;
      }
    } else {
      // Both fields are empty - no error but not valid
      passwordError.style.display = "none";
      repeatPasswordInput.classList.remove("is-invalid");
      return false;
    }
  }

  // Add password field event listeners if they exist
  if (repeatPasswordInput) {
    repeatPasswordInput.addEventListener("input", function () {
      checkPasswords();
      validateForm();
    });

    repeatPasswordInput.addEventListener("blur", function () {
      if (repeatPasswordInput.value) {
        checkPasswords();
        validateForm();
      }
    });
  }

  if (passwordInput) {
    passwordInput.addEventListener("input", function () {
      // First check password strength
      const password = passwordInput.value;
      const strength = checkPasswordStrength(password);
      console.log("Password strength:", strength);
      updatePasswordStrengthIndicator(strength);
      
      // Then check password match
      const passwordsMatch = checkPasswords();
      console.log("Passwords match:", passwordsMatch);
      
      // Finally validate the form
      validateForm();
    });

    passwordInput.addEventListener("blur", function () {
      // Update strength indicator
      const strength = checkPasswordStrength(passwordInput.value);
      updatePasswordStrengthIndicator(strength);
      
      // Check password match if both fields have values
      if (passwordInput.value || (repeatPasswordInput && repeatPasswordInput.value)) {
        checkPasswords();
      }
      
      validateForm();
    });
  }

  // Add input event listeners to all required fields
  if (firstNameInput) firstNameInput.addEventListener("input", validateForm);
  if (lastNameInput) lastNameInput.addEventListener("input", validateForm);
  if (usernameInput) usernameInput.addEventListener("input", validateForm);
  if (emailInput) emailInput.addEventListener("input", validateForm);

  // Validate the entire form and enable/disable the register button
  function validateForm() {
    if (!registerButton) return;

    const isFirstNameValid = !firstNameInput || firstNameInput.value.trim() !== "";
    const isLastNameValid = !lastNameInput || lastNameInput.value.trim() !== "";
    const isUsernameValid = !usernameInput || usernameInput.value.trim() !== "";
    const isEmailValid = !emailInput || (emailInput.value && validateEmail(emailInput.value));
    const isPasswordValid = !passwordInput || passwordInput.value.trim() !== "";
    const doPasswordsMatch = checkPasswords();

    // Apply visual indicators for validation status
    if (emailInput && !isEmailValid && emailInput.value) {
      emailInput.classList.add("is-invalid");
    } else if (emailInput) {
      emailInput.classList.remove("is-invalid");
    }

    // Password must be valid and match the confirmation
    const passwordValidAndMatching = isPasswordValid && doPasswordsMatch;
    
    // Only validate repeat password if the main password has a value
    if (passwordInput && repeatPasswordInput && passwordInput.value && !doPasswordsMatch) {
      repeatPasswordInput.classList.add("is-invalid");
    } else if (repeatPasswordInput) {
      repeatPasswordInput.classList.remove("is-invalid");
    }

    const isFormValid =
      isFirstNameValid &&
      isLastNameValid &&
      isUsernameValid &&
      isEmailValid &&
      passwordValidAndMatching;

    // Update button state
    registerButton.disabled = !isFormValid;

    return isFormValid;
  }

  // Form submission validation for registration
  if (form) {
    console.log("Setting up form submission handler");
    form.addEventListener("htmx:beforeSwap", function handleRegisterResponse(evt) {
      console.log("htmx:beforeSwap event triggered (register form)");
      if (evt.detail.target.id === "register-form") {
        try {
          console.log("Processing register response:", evt.detail.xhr.responseText);
          const response = JSON.parse(evt.detail.xhr.responseText);

          if (response.success) {
            evt.detail.shouldSwap = false;
            // Use common function for successful authentication
            handleAuthSuccess();
          } else {
            // Use common function for authentication errors
            handleAuthError(response.message, 'register');
            
            // Return false to prevent the default swap
            evt.detail.shouldSwap = false;
          }
        } catch (e) {
          console.error("Error processing register response:", e);
        }
      }
    });
  }
  
  console.log("Register page initialization complete");
}
