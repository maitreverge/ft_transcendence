# import re
from playwright.sync_api import Playwright, sync_playwright  # , expect

# import time


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Loguer toutes les requêtes effectuées
    def handle_request(request):
        print(f"➡️ Requête envoyée : {request.url}")

    # Loguer toutes les réponses reçues
    def handle_response(response):
        print(f"⬅️ Réponse reçue : {response.url} - Statut: {response.status}")
        if response.status == 404:
            print(f"❌ Erreur 404 détectée pour : {response.url}")

    page.on("request", handle_request)
    page.on("response", handle_response)

    # def handle_response(response):
    #     if response.status == 404:
    #         print(f"Erreur 404 détectée pour : {response.url}")
    #         raise Exception(f"Erreur 404 sur la ressource: {response.url}")

    page.on("response", handle_response)

    page.goto("https://1140-46-193-66-225.ngrok-free.app/")
    page.get_by_role("textbox", name="Entrez votre nom").click()
    page.get_by_role("textbox", name="Entrez votre nom").fill("kapouet")
    page.get_by_role("button", name="Connexion").click()
    page.get_by_role("button", name="Tournament").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="Simple Match").click()
    page.get_by_role("button", name="Close").click()
    page.goto("https://1140-46-193-66-225.ngrok-free.app/test/")
    page.goto("https://1140-46-193-66-225.ngrok-free.app/match/")
    websocket_connected = False

    def handle_websocket(ws):
        nonlocal websocket_connected
        websocket_connected = True
        print(f"🔌 WebSocket connectée à : {ws.url}")

    page.on("websocket", handle_websocket)
    page.goto("http://1140-46-193-66-225.ngrok-free.app/match/")
    try:
        if not websocket_connected:
            raise ValueError("❌ La connexion WebSocket a échoué.")
        else:
            print("✅ La connexion WebSocket est réussie.")
    except ValueError as e:
        print(e)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
