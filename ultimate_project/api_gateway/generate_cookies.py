from csrf_tokens import generate_csrf_token

def generate_cookies(json_response, access_token, refresh_token):
        # Access token
    json_response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        path="/",
        max_age=60 * 2,  # TEST 2 MN
    )
# 
    # Refresh token
    json_response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 7,  # 7 days
    )
# 
    # Generate and set CSRF token
    json_response.set_cookie(
        key="csrftoken",
        value=generate_csrf_token(),
        httponly=True,
        secure=True,
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 21,  # 21 days => gets logged out after 21 days
    )