import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8080/")
    page.get_by_role("textbox", name="Entrez votre nom").click()
    page.get_by_role("textbox", name="Entrez votre nom").fill("kapouet")
    page.get_by_role("button", name="Connexion").click()
    page.get_by_role("button", name="Tournament").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="Simple Match").click()
    page.get_by_role("button", name="Close").click()
    page.goto("http://localhost:8080/match/")
    
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)