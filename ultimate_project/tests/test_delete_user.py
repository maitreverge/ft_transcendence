from playwright.sync_api import Playwright, sync_playwright, expect
from collections import Counter
import pyotp

LOGIN_REGULAR = "test"
PASSWORD = "password"

LOGIN_2FA = "delete_2fa"
OPT_KEY = "S3EF2KESUQR45MRTL7MXDSJVI6JQDG42"

BASE_URL = "https://localhost:8443"

totp = pyotp.TOTP(OPT_KEY)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        ignore_https_errors=True
    )
    page = context.new_page()

    def login(user):
        page.goto(f"{BASE_URL}/login/")
        
        if user == "regular":
            page.locator("#username").fill(LOGIN_REGULAR)
            page.locator("#password").fill(PASSWORD)
            page.locator("#loginButton").click()
        else:
            page.locator("#username").fill(LOGIN_2FA)
            page.locator("#password").fill(PASSWORD)
            page.locator("#loginButton").click()
        

    def logout():
        youpiBanane = page.locator("#youpiBanane")
        logoutButton = page.locator("#logoutButton")
        modalLogoutButton = page.locator("#modalLogoutButton")
        assert "show" not in (youpiBanane.get_attribute("class") or "")
        youpiBanane.click()
        logoutButton.click()
        modalLogoutButton.click()
        expect(page).to_have_url(f"{BASE_URL}/login/")

    
    # LOGIN

    def delete_user(user):
        login(user)
        
        # Connect to 2fa
        if user == "2fa":
            for _ in range(3):
                try:
                    page.locator("#otp_input").fill(totp.now())
                    page.locator("#otp_verify").click()
                    expect(page).to_have_url(f"{BASE_URL}/home/")
                    break
                except Exception as e:
                    print(f"💀 2FA connexion failed {_ + 1} times 💀", flush=True)

        expect(page).to_have_url(f"{BASE_URL}/home/")

        page.locator("#nav-profile").click()
        expect(page).to_have_url(f"{BASE_URL}/user/profile/")

        page.locator("#delete_profile").click()

        # ! We're on the delete-profile.html

        final_delete_button = page.locator("#delete_profile")
        password_field = page.locator("#password")

        # ! CASE 1 BOTH EMPTY
        final_delete_button.click()
        expect(page).to_have_url(f"{BASE_URL}/user/profile/")
        
        error_field = page.locator("#error_delete_user")
        # expect(error_field).to_have_text("Password is required")




        # password_field.fill("nope")

        # if user == "2fa":
        #     twofa_field = page.locator("#otp-code")
        #     twofa_field.fill(totp.now())
        





        logout()

    # ! =============== KICKSTART TESTER HERE ===============
    delete_user("regular")
    delete_user("2fa")


    print(f"✅ DELETE USER TEST ✅")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
