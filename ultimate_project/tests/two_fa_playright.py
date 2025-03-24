from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pyotp

# test_2fa user secret
test_2fa_secret = "S3EF2KESUQR45MRTL7MXDSJVI6JQDG4R"


register_2fa_test_username = "register-2fa-test"
register_2fa_test_email = "register-2fa-test@test.com"
register_2fa_test_password = "password"

# ! =============== TESTING 2FA ===============

base_url = "http://localhost:8000"


def test_login_2fa(playwright: Playwright):
    # Create a TOTP object
    totp = pyotp.TOTP(test_2fa_secret)

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


def test_register_2fa(playwright: Playwright):
    # Starting a new window
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{base_url}/register/")

    # ! ============= REGISTER PAGE =============
    expect(page).to_have_url(f"{base_url}/register/")

    # Fill in the username and password
    page.locator("#first_name").fill("test")
    page.locator("#last_name").fill("test")
    page.locator("#username").fill(register_2fa_test_username)
    page.locator("#email").fill(register_2fa_test_email)
    page.locator("#password").fill(register_2fa_test_password)
    page.locator("#repeat_password").fill(register_2fa_test_password)

    page.locator("#register-button").click()

    # ! ============= HOME PAGE =============
    expect(page).to_have_url(f"{base_url}/home/")

    # Go to profile page
    page.locator("#nav-profile").click()

    # ! ============= PROFILE PAGE =============
    expect(page).to_have_url(f"{base_url}/user/profile/")

    # Check is 2FA is not enabled
    expect(page.locator("#disable_2fa")).to_be_hidden()
    expect(page.locator("#setup_2fa")).to_be_visible()

    # Click on setup 2FA
    page.locator("#setup_2fa").click()

    # ! ============= TWO-FA PAGE =============

    extracted_secret = page.locator("#secret_key").text_content()
    print(extracted_secret, flush=True)
    totp = pyotp.TOTP(extracted_secret)

    # Wait for the input field to be visible and fill it
    otp_input = page.locator("#otp_input")
    # otp_input.wait_for(state="visible", timeout=5000)
    otp_input.fill(totp.now())

    # Wait for the verify button to be visible and clickable
    verify_button = page.locator("#otp_verify")
    # verify_button.wait_for(state="visible", timeout=5000)
    # verify_button.wait_for(state="enabled", timeout=5000)
    verify_button.click()

    # Wait for success message to be visible
    success_message = page.locator("#twofa_success_message")
    success_message.wait_for(state="visible", timeout=5000)
    expect(success_message).to_have_text("2FA Action Complete")

    # Wait for log message to be visible
    log_message = page.locator("#log_message")
    log_message.wait_for(state="visible", timeout=5000)
    expect(log_message).to_have_text(
        "Your account is now protected with two-factor authentication."
    )

    # # Click on disable 2FA
    # page.locator("#disable_2fa").click()

    # page.locator("#otp_input").fill(totp.now())
    # page.locator("#otp_verify").click()

    # expect(page.locator("#success_message")).to_have_text("Two-factor authentication has been disabled for your account.")

    # expect(page).to_have_url(f"{base_url}/user/profile/")

    context.close()
    browser.close()
