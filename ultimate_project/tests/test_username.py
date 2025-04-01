from playwright.sync_api import Playwright, sync_playwright, expect
from collections import Counter
import time
import os

# USERS
# LOGIN_REG = "same_auth"
# LOGIN_2FA = "same_auth_2fa"
# PASSWORD = "password"
# SECRET_2FA = "9JUF2KESUQR45MRTL7MXDSJVI6JQDG42"

SIMULTANEOUS_USERS = 2

BASE_URL = "https://localhost:8443"


def run(playwright: Playwright) -> None:
    # browser = playwright.chromium.launch(headless=False)
    # context = browser.new_context(
    #     ignore_https_errors=True
    # )
    # page = context.new_page()

    def login(page, login):
        expect(page).to_have_url(f"{BASE_URL}/login/")

        # Fill in the username and password
        page.locator("#username").fill(login)
        page.locator("#password").fill(PASSWORD)
        page.locator("#loginButton").click()

        # ! ============= TWO-FA PAGE =============
        expect(page).to_have_url(f"{BASE_URL}/home/")

    def logout(page):
        youpiBanane = page.locator("#youpiBanane")
        logoutButton = page.locator("#logoutButton")
        modalLogoutButton = page.locator("#modalLogoutButton")
        assert "show" not in (youpiBanane.get_attribute("class") or "")
        youpiBanane.click()
        logoutButton.click()
        modalLogoutButton.click()
        expect(page).to_have_url(f"{BASE_URL}/login/")


    # ! =============== KICKSTART TESTER HERE ===============
    browsers = []
    contexts = []
    pages = []
    

    screen_width, screen_height = get_screen_size()

    # Make windows narrow but tall (vertical shape)
    window_width = int(screen_width * 0.35)  # 35% of screen width
    window_height = int(screen_height * 0.9)  # 90% of screen height

    # Position one window at far left, one at far right
    left_position = 0
    right_position = screen_width - window_width

    # Position windows at left and right edges with different Y positions
    positions = [(left_position, 20), (right_position, 20)]

    # Better debugging to check what's happening
    print(f"Screen dimensions: {screen_width}x{screen_height}")
    print(f"Window size: {window_width}x{window_height}")
    print(f"Left window position: ({left_position}, 20)")
    print(f"Right window position: ({right_position}, 20)")

    # Set each window to be the same size
    window_sizes = [(window_width, window_height), (window_width, window_height)]

    test_reg_users(browsers, contexts, pages, positions, window_sizes)

    test_2fa_users()

    print(f"✅ SAMETIME AUTH PASSED ✅")

    # context.close()
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)
