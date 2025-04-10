from playwright.sync_api import Playwright, sync_playwright, expect
import time
import os
import pyotp


# USERS
USER_2 = "user2"
USER_3 = "user3"
PASSWORD = "password"

SIMULTANEOUS_USERS = 2

BASE_URL = "https://localhost:8443"

def run(playwright: Playwright) -> None:

    def get_screen_size():
        # This is a simple approach that works on many Linux systems
        # For more accurate results across all setups, consider a library like PyAutoGUI
        try:
            cmd = "xrandr | grep '*' | awk '{print $1}'"
            output = os.popen(cmd).read().strip().split("x")
            if len(output) == 2:
                return int(output[0]), int(output[1])
        except:
            pass
        # Fallback to common resolution
        return 1920, 1080

    def login(page, login, twofa = None):
        expect(page).to_have_url(f"{BASE_URL}/login/")

        # Fill in the username and password
        page.locator("#username").fill(login)
        page.locator("#password").fill(PASSWORD)
        page.locator("#loginButton").click()

        time.sleep(2)

        # ! 2FA CONNEXION BLOCK
        # if twofa:
        #     totp = pyotp.TOTP(SECRET_2FA)
        #     expect(page).to_have_url(f"{BASE_URL}/two-factor-auth/")

        #     # Fill with a correct code
        #     for _ in range(3):
        #         current_code = totp.now()
        #         try:
        #             page.locator("#otp_input").fill(current_code)
        #             page.locator("#otp_verify").click()
        #             expect(page).to_have_url(f"{BASE_URL}/home/")
        #             print(
        #                 f"✅ 2FA connexion succed on {_ + 1}{get_ordinal_suffix(_ + 1)} try ✅",
        #                 flush=True,
        #             )
        #             break
        #         except Exception as e:
        #             print(f"💀 2FA connexion failed {_ + 1} times, retrying 💀", flush=True)


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

    def init_win(browsers, contexts, pages, positions, window_sizes):
        for _ in range(SIMULTANEOUS_USERS):
            # Launch browser without specific size/position first
            browsers.append(
                playwright.chromium.launch(
                    headless=False,
                    args=[
                        f"--window-position={positions[_][0]},{positions[_][1]}",
                        f"--window-size={window_sizes[_][0]},{window_sizes[_][1]}",
                    ],
                )
            )

            # Create context with viewport size matching our target window size
            contexts.append(
                browsers[_].new_context(
                    ignore_https_errors=True,
                    viewport={
                        "width": window_sizes[_][0],
                        "height": window_sizes[_][1],
                    },
                )
            )

            pages.append(contexts[_].new_page())

            # Also set position via JavaScript to ensure it takes effect
            pages[_].evaluate(
                f"window.moveTo({positions[_][0]}, {positions[_][1]}); window.resizeTo({window_sizes[_][0]}, {window_sizes[_][1]});"
            )

    def destroy_obj(browsers, contexts):
        for context in contexts:
            context.close()
        for browser in browsers:
            browser.close()


    def test_remote_simple_match(browsers, contexts, pages, positions, window_sizes):

        for _ in range(SIMULTANEOUS_USERS):
            pages[_].goto(f"{BASE_URL}/login/")
        
        page1 = pages[0]
        page2 = pages[1]

        # Login both pages regular users
        login(page1, USER_2)
        login(page2, USER_3)

        # Go to match simple
        page1.goto(f"{BASE_URL}/tournament/simple-match/")
        page2.goto(f"{BASE_URL}/tournament/simple-match/")
        
        # !!!!!!!!!! 🪡🪡🪡🪡 WORK NEEDLE

        # Page 1 => user 2 / 3
        
        
        
        time.sleep(10)
        
        logout(page1)
        logout(page2)
        
        # page1.locator("#big-tournament").click()
        # expect(page1).to_have_url(f"{BASE_URL}/tournament/tournament/")


        # # Page 2 login after
        # page2.locator("#big-tournament").click()
        # expect(page
        # expect(page2).to_have_url(f"{BASE_URL}/tournament/tournament/")2).to_have_url(f"{BASE_URL}/tournament/tournament/")

        
        # # Page 1 tries to navigate afterwards, and is no longer auth
        # page1.locator("#side-match").click()
        # expect(page1).to_have_url(f"{BASE_URL}/register/")
        # page1.goto(f"{BASE_URL}/home/")
        # expect(page1).to_have_url(f"{BASE_URL}/register/")



        # time.sleep(10)

    # ! =============== INIT WINDOWS SIZES ===============
    browsers = []
    contexts = []
    pages = []
    

    screen_width, screen_height = get_screen_size()

    # Make windows narrow but tall (vertical shape)
    window_width = int(screen_width * 0.35)
    window_height = int(screen_height * 0.9)

    # Position one window at far left, one at far right
    left_position = 0
    right_position = screen_width - window_width

    # Position windows at left and right edges with different Y positions
    positions = [(left_position, 20), (right_position, 20)]

    # Set each window to be the same size
    window_sizes = [(window_width, window_height), (window_width, window_height)]

    # ! =============== KICKSTART TESTER HERE ===============
    test_remote_simple_match(browsers, contexts, pages, positions, window_sizes)


    print(f"✅ GAME TESTS ✅")

    destroy_obj(browsers, contexts)
    
    
    # context.close()
    # browser.close()

    """
    DAN, PUT WHAT TO TEST HERE

    - TEST MATCH SIMPLE
    - PREMIER TEST: test 1v1 solo
    - Navigate to page Match simple

    - START ROUTINE1 click sur l'element ayant les classes "user self-player"
    - dans l'input avec l'id="match-player-name", entre le nom "bobby"
    - click ENCORE sur le meme elment qu'avant 
    
    
    - START ROUTINE 2 click sur l'element avec les classes "match self-match"    - 
    - l'élément avec la class "loader" doit avoir style="opacity: 1;"
    - attendre 4 secondes
    - l'élément avec la class "loader" doit avoir style="opacity: 0;"
    - 
    - DEUXIEME TEST:  test 1v1 solo part 2
    - cliquer sur l'élément avec id="acc-profile" (on va devoir changer cet id, c'ets le template de thomas :)
    - cliquer sur l'élément avec id="acc-profile" (on revient sur la page via une htmx)
    - On rebalance le test a partir de START ROUTINE1

    - TEST TROIS: test 1v1 remote
    - on ouvre deux sessions avec deux user differents
    - un des deux users acced a la page match simple par un click sur l'élément avec id="acc-profile" 
    - l'autre navigue directement à la page 
    - joueur A clique sur l'élément avec la classe "user" (et UNIQUEMENT la classe user)
    - joueur B clique sur l'élément avec les classe "swal2-cancel swal2-styled"
    - l'autre A clique sur l'élément avec les classes "swal2-confirm swal2-styled"
    - joueur B clique sur l'élément avec la classe "user" (et UNIQUEMENT la classe user)
    - joueur A clique sur l'élément avec les classes "swal2-confirm swal2-styled"
    - joueur A et joueur B excuent la routine 2
    
    - TEST QUATRE: test 
    -
    -
    -
    -
    -
    -
    -
    -
    -

    
    """

with sync_playwright() as playwright:
    run(playwright)
