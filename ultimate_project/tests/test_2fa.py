from playwright.sync_api import Playwright, sync_playwright, expect, Page
import time
import pyotp
import traceback

# test_2fa user secret
LOGIN_SECRET = "S3EF2KESUQR45MRTL7MXDSJVI6JQDG4R"
BASE_URL = "https://localhost:8443"
USERNAME = "test_all_2fa"
EMAIL = "test_all_2fa@test.com"
PASSWORD = "password"

totp = pyotp.TOTP(LOGIN_SECRET)

def get_ordinal_suffix(num):
        if num == 1:
            return "st"
        elif num == 2:
            return "nd"
        elif num == 3:
            return "rd"
        else:
            return "th"

def setup_playwright(playwright: Playwright):
    try:
        print("🔄 Starting get page process...", flush=True)
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        print("✅ Successfully initialized the page.", flush=True)
        return page, context, browser
    except Exception as e:
        print(f"❌ An error occurred while initializing the page: {str(e)}", flush=True)
        return None
    
def close_playwright(context, browser):
    try:
        print("🔄 Starting the process to close Playwright...", flush=True)
        context.close()
        browser.close()
        print("✅ Successfully closed Playwright context and browser.", flush=True)
    except Exception as e:
        print(f"❌ An error occurred while closing Playwright: {str(e)}", flush=True)

def test_delete_user(page: Page, has_2fa, password):
    try:
        print(f"🔄 Starting process to delete user - is using 2fa {has_2fa}...", flush=True)
        expect(page).to_have_url(f"{BASE_URL}/home/", timeout=1000)
    except Exception as e:
        print(f"❌ Failed to confirm landing on the Home page: {str(e)}", flush=True)
    if has_2fa:
        for _ in range(3):
            try:
                page.locator("#otp_input").fill(totp.now())
                page.locator("#otp_verify").click()
                expect(page).to_have_url(f"{BASE_URL}/home/", timeout=2000)
                print(f"✅ 2FA login success on attempt {_ + 1}", flush=True)
                break
            except Exception as e:
                print(f"❌ 2FA login failed on attempt {_ + 1}: {str(e)}", flush=True)
    try:
        expect(page).to_have_url(f"{BASE_URL}/home/", timeout=2000)
        print("✅ Landed on Home page after login", flush=True)
        page.locator("#nav-profile").click()
        expect(page).to_have_url(f"{BASE_URL}/account/profile/", timeout=2000)
        print("✅ Navigated to profile page", flush=True)
    except Exception as e:
        print(f"❌ Failed during navigation or setup to delete profile: {str(e)}", flush=True)

    try:
        delete_button = page.locator("#delete_profile")
        expect(page).to_have_url(f"{BASE_URL}/user/delete-profile/", timeout=2000)
    except Exception as e:
        print(f"❌ Failed during navigation or setup to delete profile: {str(e)}", flush=True)

    print(f"🔄 CASE 1: INVALID PASSWORD (W OR NOT OTP) ...", flush=True)
    if has_2fa:
        for _ in range(3):
            try:
                password_field.fill("nope_false_password")
                otp_field = page.locator("#otp-code")
                otp_field.fill(totp.now())
                delete_button.click()
                expect(page).to_have_url(f"{BASE_URL}/account/profile/", timeout=2000)
                error_field = page.locator("#error_delete_user").text_content()
                assert error_field == "Invalid password"
                print("✅ Correctly handled invalid password with 2FA", flush=True)
                break
            except Exception as e:
                print(f"❌ Incorrect password with 2FA attempt {_ + 1} failed: {str(e)}", flush=True)
    else:
        try:
            password_field.fill("nope_false_password")
            delete_button.click()
            expect(page).to_have_url(f"{BASE_URL}/account/profile/", timeout=2000)
            error_field = page.locator("#error_delete_user").text_content()
            assert error_field == "Invalid password"
            print("✅ Correctly handled invalid password (no 2FA)", flush=True)
        except Exception as e:
            print(f"❌ Incorrect password (no 2FA) test failed: {str(e)}", flush=True)

    print(f"🔄 CASE 2: Valid PASSWORD (W OR NOT INVALID OTP) ...", flush=True)
    if has_2fa:
        try:
            password_field = page.locator("#password")
            password_field.fill(password)
            otp_field = page.locator("#otp-code")
            otp_field.fill("000000")
            delete_button.click()
            expect(page).to_have_url(f"{BASE_URL}/account/profile/", timeout=2000)
            time.sleep(3)
            error_field = page.locator("#error_delete_user").text_content()
            assert error_field == "Invalid 2FA code"
            print("✅ Correctly handled invalid 2FA code", flush=True)
        except Exception as e:
            print(f"❌ Invalid OTP test failed: {str(e)}", flush=True)

    print(f"🔄 CASE 3: CORRECT PASSWORD + OTP ...", flush=True)
    if has_2fa:
        for _ in range(3):
            current_code = totp.now()
            try:
                password_field.fill(password)
                otp_field = page.locator("#otp-code")
                otp_field.fill(current_code)
                delete_button.click()
                expect(page).to_have_url(f"{BASE_URL}/register/", timeout=2000)
                print(f"✅ User with 2FA deleted successfully on attempt {_ + 1}", flush=True)
                break
            except Exception as e:
                print(f"❌ Happy path 2FA delete attempt {_ + 1} failed: {str(e)}", flush=True)
    else:
        try:
            password_field.fill(PASSWORD)
            delete_button.click()
            expect(page).to_have_url(f"{BASE_URL}/register/")
            print("✅ User without 2FA deleted successfully", flush=True)
        except Exception as e:
            print(f"❌ Failed to delete user without 2FA: {str(e)}", flush=True)

def logout(page: Page) -> None:
    try:
        print("🔄 Starting logout process...", flush=True)
        if page.content().strip() == "":
            print("❌ The page is empty. Unable to proceed with logout.", flush=True)
            return
        time.sleep(1)
        youpiBanane = page.locator("#youpiBanane")
        logoutButton = page.locator("#logoutButton")
        modalLogoutButton = page.locator("#modalLogoutButton")
        assert "show" not in (youpiBanane.get_attribute("class") or "")
        youpiBanane.click()
        logoutButton.click()
        modalLogoutButton.click()
        expect(page).to_have_url(f"{BASE_URL}/login/", timeout=2000)
        print("✅ Successfully logged out and redirected to login page.", flush=True)
    except Exception as e:
        print(f"❌ An error occurred during logout: {str(e)}", flush=True)

def test_login_w_check_failed(page: Page, username, password):
    try:
        print("🔄 Starting the process of filling and submitting the login form with 1 wrong attempt...", flush=True)
        expect(page).to_have_url(f"{BASE_URL}/login/", timeout=2000)
        if page.content().strip() == "":
            print("❌ The page is empty. Unable to proceed with logout.", flush=True)
            return
        # Fill in the login form with invalid credentials
        page.locator("#username").fill(username)
        page.locator("#password").fill(password)
        page.locator("#loginButton").click()
        error_message = page.locator("#login-form")
        expect(error_message).to_have_text("Invalid credentials", timeout=2000)
        expect(page).to_have_url(f"{BASE_URL}/login/", timeout=2000)
        print("✅ Login failed as expected with the correct error message.", flush=True)
        # Optionally, check that the URL is still the login page after the failed login
        page.locator("#username").fill(username)
        page.locator("#password").fill(password)
        page.locator("#loginButton").click()
        print("✅ Login successful as expected.", flush=True)
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}", flush=True)

def test_login(page: Page, username, password):
    try:
        print("🔄 Starting the process of filling and submitting the login form...", flush=True)
        page.goto(f"{BASE_URL}/login/")
        expect(page).to_have_url(f"{BASE_URL}/login/", timeout=2000)
        if page.content().strip() == "":
            print("❌ The page is empty. Unable to proceed with logout.", flush=True)
            return
        # Fill in the login form with invalid credentials
        page.locator("#username").fill(username)
        page.locator("#password").fill(password)
        page.locator("#loginButton").click()
        expect(page).to_have_url(f"{BASE_URL}/home/", timeout=2000)
        print("✅ Login successful as expected.", flush=True)
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}", flush=True)

def test_login_w_2fa(page: Page, username, input_secret) -> None:
    try:
        print("⚙️ Starting 2FA login test...", flush=True)
        totp = pyotp.TOTP(input_secret)
        page.goto(f"{BASE_URL}/login/")
        try:
            test_login(page, username, PASSWORD)
            expect(page).to_have_url(f"{BASE_URL}/two-factor-auth/", timeout=2000)
            print("✅ Login successful, on 2FA page.", flush=True)
        except Exception as e:
            print(f"❌ Login failed before 2FA: {str(e)}", flush=True)
            return
        try:
            page.locator("#otp_input").fill("000000")
            page.locator("#otp_verify").click()
            expect(page).to_have_url(f"{BASE_URL}/two-factor-auth/", timeout=2000)
            error_message = page.locator("#login_error")
            expect(error_message).to_have_text("Invalid 2FA code", timeout=2000)
            print("✅ Error message correctly shown for invalid 2FA code.", flush=True)
        except Exception as e:
            print(f"❌ Invalid 2FA code test failed: {str(e)}", flush=True)
            return
        try:
            page.locator("#cancel_button").click()
            expect(page).to_have_url(f"{BASE_URL}/login/", timeout=2000)
            print("✅ Navigated back to login after invalid 2FA.", flush=True)
        except Exception as e:
            print(f"❌ Failed to return to login page after cancel: {str(e)}", flush=True)
            return
        try:
            test_login(page, username, PASSWORD)
            expect(page).to_have_url(f"{BASE_URL}/two-factor-auth/", timeout=1000)
            print("✅ Re-login successful, back on 2FA page.", flush=True)
        except Exception as e:
            print(f"❌ Re-login failed: {str(e)}", flush=True)
            return
        for attempt in range(3):
            current_code = totp.now()
            try:
                page.locator("#otp_input").fill(current_code)
                page.locator("#otp_verify").click()
                expect(page).to_have_url(f"{BASE_URL}/home/", timeout=1000)
                print(f"✅ 2FA succeeded on attempt {attempt + 1}{get_ordinal_suffix(attempt + 1)}.", flush=True)
                break
            except Exception as e:
                print(f"💀 2FA attempt {attempt + 1} failed, retrying...", flush=True)

    except Exception as e:
        print(f"❌ Unexpected error during 2FA login test: {str(e)}", flush=True)
    else:
        print("✅ 2FA login test completed successfully.", flush=True)

def test_register(page: Page, username, email, password):
    try:
        print("⚙️ Register user with valid credentials ...", flush=True)
        page.goto(f"{BASE_URL}/register/")
        expect(page).to_have_url(f"{BASE_URL}/register/", timeout=1000)
        page.locator("#first_name").fill("test")
        page.locator("#last_name").fill("test")
        page.locator("#username").fill(username)
        page.locator("#email").fill(email)
        page.locator("#password").fill(password)
        page.locator("#repeat_password").fill(password)
        page.locator("#register-button").click()
        expect(page).to_have_url(f"{BASE_URL}/home/", timeout=1000)
        print("✅ Successfully registered and landed on Home page", flush=True)
        return True
    except Exception as e:
        print(f"❌ Failed during registration: {str(e)}", flush=True)
        return False

def test_setup_2fa_account(page: Page) -> None:

    try:
        print("⚙️ Setup 2FA on the account page ...", flush=True)
        expect(page).to_have_url(f"{BASE_URL}/home/")
        print("✅ On Home page", flush=True)
        for _ in range(2):
            try:
                page.locator("#nav-profile").click()
                expect(page).to_have_url(f"{BASE_URL}/account/profile/")
                print("✅ Navigated to account profile settings", flush=True)
                break
            except Exception as e:
                print(f"❌ Failed to access account profile settings: {str(e)}", flush=True)
        # Check 2FA not already enabled
        expect(page.locator("#disable_2fa")).to_be_hidden()
        expect(page.locator("#setup_2fa")).to_be_visible()
        print("✅ 2FA is currently disabled", flush=True)
        # Start 2FA setup
        page.locator("#setup_2fa").click()
        expect(page).to_have_url(f"{BASE_URL}/account/security/setup-2fa/")
        print("✅ Reached setup-2FA page", flush=True)
        # Get the secret and create TOTP generator
        extracted_secret = page.locator("#secret_key").text_content()
        print(f"✅ Extracted 2FA secret: {extracted_secret}", flush=True)
        register_totp = pyotp.TOTP(extracted_secret)
        # Try verifying the TOTP
        for attempt in range(3):
            try:
                otp_input = page.locator("#otp_input")
                otp_input.fill(register_totp.now())
                verify_button = page.locator("#otp_verify")
                verify_button.click()
                success_message = page.locator("#twofa_success_message")
                success_message.wait_for(state="visible", timeout=4000)
                expect(success_message).to_have_text("2FA Action Complete")
                log_message = page.locator("#log_message")
                log_message.wait_for(state="visible", timeout=4000)
                expect(log_message).to_have_text(
                    "Your account is now protected with two-factor authentication."
                )
                print(f"✅ 2FA setup successful on attempt {attempt + 1}", flush=True)
                page.locator("#nav-profile").click()
                expect(page).to_have_url(f"{BASE_URL}/home/")
                break
            except Exception as e:
                print(f"❌ 2FA setup failed on attempt {attempt + 1}: {str(e)}", flush=True)
        print("✅ Test completed: 2FA setup successful", flush=True)
    except Exception as e:
        print(f"❌ Test failed: {str(e)}", flush=True)

def run(playwright: Playwright) -> None:

    print("===================== 🧪 START: Setup 2FA for Account =====================", flush=True)    
    page, context, browser  = setup_playwright(playwright)
    #test_delete_user(page, True, PASSWORD)
    if not test_register(page, USERNAME, EMAIL, PASSWORD):
        print("⚙️ Retrying to regsiter user ...", flush=True)
        test_login(page, USERNAME, PASSWORD)
        test_delete_user(page, True, PASSWORD)
        test_register(page, USERNAME, EMAIL, PASSWORD)
    test_setup_2fa_account(page)
    logout(page)
    test_login_w_2fa(page, USERNAME, LOGIN_SECRET)
    close_playwright(context, browser)
    test_delete_user(page, PASSWORD, True)
    print("===================== ✅ END: Setup 2FA for Account Test Completed =====================", flush=True)

with sync_playwright() as playwright:
    run(playwright)
