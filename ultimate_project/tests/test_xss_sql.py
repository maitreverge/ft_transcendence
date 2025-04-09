from playwright.sync_api import Playwright, sync_playwright, expect
from collections import Counter
import time

LOGIN = "user2"
PASSWORD = "password"
BASE_URL = "https://localhost:8443"

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        ignore_https_errors=True
    )
    page = context.new_page()

    def login(username):
        page.locator("#username").fill(username)
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

    # ! =============== KICKSTART TESTER HERE ===============
    
    page.goto(f"{BASE_URL}/login/")

    SQL = {
        "username: ' OR '1'='1",
        "admin' --",
        "' UNION SELECT null, 'hacked', null --",
        "' OR IF(1=1, SLEEP(5), 0) --",
    }

    XSS = {
        "<script>alert('XSS')</script>",
        "<p>You searched for: <script>alert('XSS')</script></p>",
        "<a href=\"javascript:alert('XSS')\">Click me</a>",
        "<div onclick=\"alert('XSS')\">Click here</div>",
        "<input value=\"<?php echo $_GET['name']; ?>\">",
        "\" onfocus=\"alert('XSS')",
    }

    for sql in SQL:
        login(sql)
        time.sleep(0.5)
        error_message = page.locator("#login-form")
        expect(error_message).to_have_text("Invalid credentials")
        
    for xss in XSS:
        login(xss)
        time.sleep(0.5)
        error_message = page.locator("#login-form")
        expect(error_message).to_have_text("Invalid credentials")
    
    login(LOGIN, 1)



    # logout()

    print(f"✅ SQL / XSS PASSED ✅")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
