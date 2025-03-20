# import time
# from playwright.sync_api import Playwright, sync_playwright

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    base_url = "http://localhost:8000"
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    visited_urls = []

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

    #test du toggle du dheckout_modal
    def check_checkout_modal_Toggle():
        logoutModal = page.locator("#youpiBanane")
        assert "show" not in (logoutModal.get_attribute("class") or "")
        logoutModal.click()
        assert "show" in (logoutModal.get_attribute("class") or "")
        logoutModal.click()
        assert "show" not in (logoutModal.get_attribute("class") or "")

    #test du bouton logout
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

    urls = [ 
            f"{base_url}/home/", 
            f"{base_url}/user/profile/", 
            f"{base_url}/user/stats/",
            f"{base_url}/tournament/simple-match/",
            f"{base_url}/tournament/tournament/"
            ]     

    for url in urls:
        test_page(url)
    
    for url in urls:
        navigate(url)

    for url in reversed(urls):
        while True:
            if page.url == url:
                test_js()
                page.wait_for_timeout(500)
                break
            else:
                page.evaluate("window.history.back()")
                page.wait_for_timeout(500)  # Laisse un peu de temps pour le back
                visited_urls.remove(url)
                

    # Vérification de la navigation via le sidebar menu
    navigate(f"{base_url}/home/")

    page.locator("#nav-tournoi").click()
    expect(page).to_have_url(f"{base_url}/tournament/tournament/")

    page.locator("#nav-profile").click()
    expect(page).to_have_url(f"{base_url}/user/profile/")

    page.locator("#nav-stats").click()
    expect(page).to_have_url(f"{base_url}/user/stats/")

    page.locator("#nav-match").click()
    expect(page).to_have_url(f"{base_url}/tournament/simple-match/")

    # Vérification de la navigation via le topbar menu

    page.locator("#side-tournoi").click()
    expect(page).to_have_url(f"{base_url}/tournament/tournament/")

    page.locator("#side-profile").click()
    expect(page).to_have_url(f"{base_url}/user/profile/")

    page.locator("#side-stats").click()
    expect(page).to_have_url(f"{base_url}/user/stats/")

    page.locator("#side-match").click()
    expect(page).to_have_url(f"{base_url}/tournament/simple-match/")

    # Vérification des boutons sur la page home

    navigate(f"{base_url}/home/")
    page.locator("#field-tournoi").click()
    expect(page).to_have_url(f"{base_url}/tournament/tournament/")

    navigate(f"{base_url}/home/")
    page.locator("#field-match").click()
    expect(page).to_have_url(f"{base_url}/tournament/simple-match/")

    navigate(f"{base_url}/home/")
    page.locator("#field-profile").click()
    expect(page).to_have_url(f"{base_url}/user/profile/")

    navigate(f"{base_url}/home/")
    page.locator("#field-stats").click()
    expect(page).to_have_url(f"{base_url}/user/stats/")

    # test 404
    

    # Fermeture
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/")
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/home/")
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/user/profile/")
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/user/stats/")
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/tournament/simple-match/")
#     time.sleep(0.4)
#     page.locator("#nav-home").click()
#     time.sleep(0.4)
#     page.locator("#nav-tournament").click()
#     time.sleep(0.4)
#     page.locator("#nav-profile").click()
#     time.sleep(0.4)
#     page.locator("#nav-stats").click()
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/home/")
#     page.locator("#field-tournament").click()
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/home/")
#     page.locator("#field-profile").click()
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/home/")
#     page.locator("#field-stats").click()
#     time.sleep(0.4)

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)


# # import re
# from playwright.sync_api import Playwright, sync_playwright  # , expect

# import time


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()

#     # Loguer toutes les requêtes effectuées
#     def handle_request(request):
#         print(f"➡️ Requête envoyée : {request.url}")

#     # Loguer toutes les réponses reçues
#     def handle_response(response):
#         print(f"⬅️ Réponse reçue : {response.url} - Statut: {response.status}")
#         if response.status == 404:
#             print(f"❌ Erreur 404 détectée pour : {response.url}")

#     page.on("request", handle_request)
#     page.on("response", handle_response)

#     page.on("response", handle_response)

#     page.goto("http://localhost:8000/")
#     time.sleep(0.4)
#     page.get_by_role("textbox", name="Entrez votre nom").click()
#     time.sleep(0.4)
#     page.get_by_role("textbox", name="Entrez votre nom").fill("kapouet")
#     time.sleep(0.4)
#     page.get_by_role("button", name="Connexion").click()
#     time.sleep(0.4)
#     page.get_by_role("button", name="Tournament").click()
#     time.sleep(0.4)
#     page.get_by_role("button", name="Close").click()
#     time.sleep(0.4)
#     page.get_by_role("button", name="Simple Match").click()
#     time.sleep(0.4)
#     page.get_by_role("button", name="Close").click()
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/test/")
#     time.sleep(0.4)
#     page.goto("http://localhost:8000/match/")

#     # TEST FLO
#     time.sleep(1)
#     page.goto("http://localhost:8000/user/")
#     time.sleep(1)
#     # TEST FLO
#     websocket_connected = False
#     time.sleep(0.4)

#     def handle_websocket(ws):
#         nonlocal websocket_connected
#         websocket_connected = True
#         print(f"🔌 WebSocket connectée à : {ws.url}")

#     page.on("websocket", handle_websocket)
#     page.goto("http://localhost:8000/match/")
#     try:
#         if websocket_connected:
#             print("✅ La connexion WebSocket est réussie.")
#         else:
#             raise ValueError("❌ La connexion WebSocket a échoué.")
#     except ValueError as e:
#         print(e)

#     # ---------------------
#     context.close()
#     browser.close()


# with sync_playwright() as playwright:
#     run(playwright)
