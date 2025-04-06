from playwright.sync_api import Playwright, sync_playwright, expect
import time

LOGIN = "user2"
PASSWORD = "password"


def run(playwright: Playwright) -> None:
    base_url = "https://localhost:8443"
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    visited_urls = []
    page.set_default_timeout(6000)  # Timeout of 6 seconds for each click

    # Fonction de navigation avec attente
    def navigate(url: str):
        page.goto(url)
        page.wait_for_load_state("networkidle")
        visited_urls.append(url)

    # test du toggle de la sidebar
    def check_sidebar_Toggle():
        sidebar = page.locator("#accordionSidebar")
        toggle_button = page.locator("#sidebarToggle")
        if not toggle_button.is_visible():
            return
        assert "toggled" not in (sidebar.get_attribute("class") or "")
        toggle_button.click()
        assert "toggled" in (sidebar.get_attribute("class") or "")
        toggle_button.click()
        assert "toggled" not in (sidebar.get_attribute("class") or "")

    # test du toggle du dheckout_modal
    def check_checkout_modal_Toggle():
        logoutModal = page.locator("#youpiBanane")
        assert "show" not in (logoutModal.get_attribute("class") or "")
        logoutModal.click()
        assert "show" in (logoutModal.get_attribute("class") or "")
        logoutModal.click()
        assert "show" not in (logoutModal.get_attribute("class") or "")

    # test du bouton logout
    def check_checkout_button():
        youpiBanane = page.locator("#youpiBanane")
        logoutButton = page.locator("#logoutButton")
        modalLogoutButton = page.locator("#modalLogoutButton")
        assert "show" not in (youpiBanane.get_attribute("class") or "")
        youpiBanane.click()
        logoutButton.click()
        modalLogoutButton.click()
        expect(page).to_have_url(f"{base_url}/login/")

        # expect(page).to_have_url(f"{base_url}/login/")

    def test_js():
        check_sidebar_Toggle()
        check_checkout_modal_Toggle()
        check_checkout_button()

    def test_page(url: str):
        if url:
            navigate(url)
            visited_urls.append(url)  # Enregistre l'URL après chaque navigation
        test_js()

    def test_single_page(url: str):
        # Navigate to the URL and test it
        current_url = page.url
        navigate(f"{base_url}{url}")

        # Check if we got redirected to register (protected route)
        if (
            page.url == f"{base_url}/register/"
            and current_url != f"{base_url}/register/"
        ):
            print(f"✓ Protected route {url} correctly redirected to register")
            return

        # Return to previous page only if we successfully navigated
        if page.url != current_url:
            page.evaluate("window.history.back()")
            page.wait_for_timeout(500)  # Laisse un peu de temps pour le back

        # Test the current page (either we returned or we couldn't navigate due to auth)
        test_page(page.url)

    def login():
        page.goto(f"{base_url}/login/")

        page.locator("#username").fill(LOGIN)
        page.locator("#password").fill(PASSWORD)
        page.locator("#loginButton").click()
        expect(page).to_have_url(f"{base_url}/home/")

    def logout():
        youpiBanane = page.locator("#youpiBanane")
        logoutButton = page.locator("#logoutButton")
        modalLogoutButton = page.locator("#modalLogoutButton")
        assert "show" not in (youpiBanane.get_attribute("class") or "")
        youpiBanane.click()
        logoutButton.click()
        modalLogoutButton.click()
        expect(page).to_have_url(f"{base_url}/login/")

    # Function to test redirection to register when accessing protected routes
    def test_auth_redirection(url: str):
        # Try to access protected URL while logged out
        navigate(url)
        # Expect redirection to register page
        expect(page).to_have_url(f"{base_url}/register/")
        print(
            f"✓ Protected route {url} correctly redirects to register when not authenticated"
        )

    urls = [
        f"{base_url}/home/",
        f"{base_url}/user/profile/",
        f"{base_url}/user/stats/",
        f"{base_url}/tournament/simple-match/",
        f"{base_url}/tournament/tournament/",
    ]

    # ! =============== KICKSTART TESTER HERE ===============
    for url in urls:
        login()
        test_page(url)

    print("⭐ 1st BLOCK PASSED  ⭐")

    for url in urls:
        login()
        navigate(url)
        logout()
    print("⭐ 2nd BLOCK PASSED  ⭐")

    # ? ================== WORK NEEDLE ======================
    # Test logout from each page and then try to access protected URL (should redirect to register)
    for url in reversed(urls):
        # First login and navigate to URL
        login()
        navigate(url)

        # Then logout and try to access the same URL
        logout()
        navigate(url)

        # We should be redirected to register page
        expect(page).to_have_url(f"{base_url}/register/")
        print(f"✓ After logout, access to {url} correctly redirects to register")

    print("⭐ 3rd BLOCK PASSED  ⭐")

    # Vérification de la navigation via le sidebar menu
    def test_navigation(locator, expected_url):
        locator.click()
        expect(page).to_have_url(expected_url)
    print("⭐ 4th BLOCK PASSED  ⭐")

    # Liste des tests à effectuer
    navigation_tests = [
        ("#nav-tournoi", f"{base_url}/tournament/tournament/"),
        ("#nav-profile", f"{base_url}/user/profile/"),
        ("#nav-stats", f"{base_url}/user/stats/"),
        ("#nav-match", f"{base_url}/tournament/simple-match/"),
        ("#side-tournoi", f"{base_url}/tournament/tournament/"),
        ("#side-profile", f"{base_url}/user/profile/"),
        ("#side-stats", f"{base_url}/user/stats/"),
        ("#side-match", f"{base_url}/tournament/simple-match/"),
        ("#field-tournoi", f"{base_url}/tournament/tournament/"),
        ("#field-match", f"{base_url}/tournament/simple-match/"),
        ("#field-profile", f"{base_url}/user/profile/"),
        ("#field-stats", f"{base_url}/user/stats/"),
    ]

    # Vérification de la navigation via le menu topbar
    login()  # Ensure we're authenticated
    navigate(f"{base_url}/home/")
    for locator, expected_url in navigation_tests[
        :4
    ]:  # Pour les éléments du menu topbar
        test_navigation(page.locator(locator), expected_url)
    print("⭐ 5th BLOCK PASSED  ⭐")

    # Vérification de la navigation via le menu latéral
    login()  # Re-authenticate to ensure session is valid
    navigate(f"{base_url}/home/")
    for locator, expected_url in navigation_tests[
        4:8
    ]:  # Pour les éléments du menu latéral
        test_navigation(page.locator(locator), expected_url)
    print("⭐ 6th BLOCK PASSED  ⭐")

    # Vérification de la navigation via les boutons sur la page home
    login()  # Re-authenticate to ensure session is valid
    for locator, expected_url in navigation_tests[
        8:
    ]:  # Pour les éléments de la page home
        navigate(f"{base_url}/home/")
        test_navigation(page.locator(locator), expected_url)
    print("⭐ 7th BLOCK PASSED  ⭐")

    # test 404
    login()  # Ensure we're authenticated for protected routes
    test_single_page("/home/sylvain_duriff/")
    print("⭐ 8th BLOCK PASSED  ⭐")

    # Test unauthenticated routes - first logout
    logout()
    test_single_page("/register/")
    test_single_page("/login/")
    print("⭐ 9th BLOCK PASSED  ⭐")

    # Test protected routes redirection when logged out
    print("Testing protected routes redirection when logged out...")
    for url in urls:
        test_auth_redirection(url)
    print("⭐ 10th BLOCK PASSED  ⭐")

    # Login again before closing
    login()
    navigate(f"{base_url}/home/")
    print("⭐ 11th BLOCK PASSED  ⭐")

    # Fermeture
    context.close()
    browser.close()

    print(f"✅ NAVIGATION TEST ✅")


with sync_playwright() as playwright:
    run(playwright)
