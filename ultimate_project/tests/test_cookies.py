from playwright.sync_api import Playwright, sync_playwright, expect
import time
from test_2fa import test_login_2fa, test_register_2fa

def run(playwright: Playwright) -> None:
    base_url = "https://localhost:8443"
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        ignore_https_errors=True
    )
    page = context.new_page()

    # ! =============== KICKSTART TESTER HERE ===============
    
    # Those tests create, test and close their own browsers
    register_from_login()
    register_after_login()
    test_login_2fa(playwright)
    # test_register_2fa(playwright) # ! NOT YET READY

    # ? =============== START REGULAR TESTS ===============
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        ignore_https_errors=True
    )
    page = context.new_page()
    page.goto(f"{base_url}/register/")
    
    # Regular register + login tests which links to Dan tests after getting proprely logged-in
    test_register(base_url, page)
    test_login(base_url, page)

with sync_playwright() as playwright:
    run(playwright)
