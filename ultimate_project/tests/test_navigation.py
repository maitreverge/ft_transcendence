# import re
from playwright.sync_api import Playwright, sync_playwright  # , expect

# import time


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
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

    page.goto("http://localhost:8000/")
    page.get_by_role("textbox", name="Entrez votre nom").click()
    page.get_by_role("textbox", name="Entrez votre nom").fill("kapouet")
    page.get_by_role("button", name="Connexion").click()
    page.get_by_role("button", name="Tournament").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="Simple Match").click()
    page.get_by_role("button", name="Close").click()
    page.goto("http://localhost:8000/match/")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
