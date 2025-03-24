from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pyotp

# test_2fa user secret
secret = "S3EF2KESUQR45MRTL7MXDSJVI6JQDG4R"

# Create a TOTP object
totp = pyotp.TOTP(secret)

# ! =============== TESTING 2FA ===============

base_url = "http://localhost:8000"

def test_login_2fa(playwright: Playwright):
    # Starting a new window
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{base_url}/login/")

    # ! ============= LOGIN PAGE =============
    # Fill in the username and password
    expect(page).to_have_url(f"{base_url}/login/")
    page.locator("#username").fill("test_2fa")
    page.locator("#password").fill("password")
    page.locator("#loginButton").click()


    # ! ============= TWO-FA PAGE =============
    expect(page).to_have_url(f"{base_url}/two-factor-auth/")
    
    # Fill with a wrong code
    page.locator("#otp_input").fill("000000")
    page.locator("#otp_verify").click()
    expect(page).to_have_url(f"{base_url}/two-factor-auth/")
    error_message = page.locator("#login_error")
    expect(error_message).to_have_text("Invalid 2FA code")

    # Click on the cancel button
    page.locator("#cancel_button").click()

    # ! ============= LOGIN PAGE =============
    expect(page).to_have_url(f"{base_url}/login/")

    # Fill in the username and password
    page.locator("#username").fill("test_2fa")
    page.locator("#password").fill("password")
    page.locator("#loginButton").click()

    # ! ============= TWO-FA PAGE =============
    expect(page).to_have_url(f"{base_url}/two-factor-auth/")

    # Get the current code
    current_code = totp.now()

    # Fill with a correct code
    page.locator("#otp_input").fill(current_code)
    page.locator("#otp_verify").click()

    expect(page).to_have_url(f"{base_url}/home/")

    context.close()
    browser.close()
