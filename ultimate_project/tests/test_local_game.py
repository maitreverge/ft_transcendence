from playwright.sync_api import Playwright, sync_playwright, expect
from collections import Counter
import time

# USERS
LOGIN = "user2"
PASSWORD = "password"

BASE_URL = "https://localhost:8443"


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    def login():
        expect(page).to_have_url(f"{BASE_URL}/login/")

        # Fill in the username and password
        page.locator("#username").fill(LOGIN)
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

    def test_local_match():

        page.goto(f"{BASE_URL}/login/")

        login()

        expect(page).to_have_url(f"{BASE_URL}/home/")
        
        page.goto(f"{BASE_URL}/tournament/simple-match/")
        
        # This block is registered by auto-playright
        page.get_by_text("user2", exact=True).click()
        page.get_by_role("textbox", name="enter a name").click()
        page.get_by_role("textbox", name="enter a name").fill("test_player")
        page.get_by_text("user2", exact=True).click()
        page.get_by_text("match:").click()
        page.locator(".circle").click()

        time.sleep(10)


        logout()

    # ! =============== KICKSTART TESTER HERE ===============

    test_local_match()

    print(f"✅ LOCAL GAMES TEST OKAY ✅")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
