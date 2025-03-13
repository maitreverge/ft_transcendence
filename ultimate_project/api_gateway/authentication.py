from fastapi import APIRouter, Request, Response, HTTPException, Form
from fastapi.responses import JSONResponse
import requests
import jwt
import datetime
import os

router = APIRouter()

# Clé secrète pour signer les JWT
SECRET_JWT_KEY = os.getenv("JWT_KEY")

# Configuration des durées des tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# URL de l'API qui gère la vérification des identifiants
DATABASE_API_URL = "http://databaseapi:8007/api/verify-credentials/"


# @router.post("/auth/login/")
async def login_fastAPI(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Vérifie les identifiants via `databaseAPI`, puis génère un JWT stocké en cookie.
    """

    print(f"🔐 Tentative de connexion pour {username}", flush=True)

    # Vérifier les identifiants en appelant `databaseAPI`
    try:
        db_response = requests.post(
            DATABASE_API_URL,
            data={"username": username, "password": password},
        )

        if db_response.status_code != 200:
            error_message = db_response.json().get("error", "Authentication failed")
            # Return error message to be displayed in the login-result div
            return JSONResponse(
                content={"success": False, "message": error_message}, status_code=401
            )

        # 🔹 L'authentification est réussie, récupérer les données utilisateur
        auth_data = db_response.json()

    except requests.exceptions.RequestException as e:
        # Return error message for connection issues
        return JSONResponse(
            content={"success": False, "message": f"Service unavailable: {str(e)}"},
            status_code=500,
        )

    # 🔹 Générer les tokens JWT
    expire_access = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    expire_refresh = datetime.datetime.utcnow() + datetime.timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    access_payload = {
        "user_id": auth_data.get("user_id", 0),
        "username": username,
        "exp": expire_access,
    }
    refresh_payload = {
        "user_id": auth_data.get("user_id", 0),
        "username": username,  # Include username in refresh token too
        "exp": expire_refresh,
    }

    access_token = jwt.encode(access_payload, SECRET_JWT_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, SECRET_JWT_KEY, algorithm="HS256")

    # 🔹 Log pour debug
    print(f"Access Token: {access_token[:20]}...", flush=True)
    print(f"Refresh Token: {refresh_token[:20]}...", flush=True)

    # 🔹 Indiquer à HTMX de rediriger l'utilisateur
    response.headers["HX-Redirect"] = "/home"

    # Create a JSONResponse with success message
    json_response = JSONResponse(
        content={"success": True, "message": "Connexion réussie"}
    )

    # Copy the headers from our response to the JSONResponse
    for key, value in response.headers.items():
        json_response.headers[key] = value

    # Make sure the cookies are also set on the JSONResponse
    # Access token
    json_response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 6,
    )

    # Refresh token
    json_response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 7,
    )

    # Debug log for headers
    print(f"🔒 Response headers: {dict(json_response.headers)}", flush=True)

    return json_response


# Function to verify JWT token
def verify_jwt(token):
    """
    Verify a JWT token and return the payload if valid.

    Args:
        token (str): The JWT token to verify

    Returns:
        dict: The decoded token payload if valid, None otherwise
    """
    try:
        # Verify the token with our secret key
        payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


# Function to generate a new access token using a valid refresh token
def refresh_access_token(refresh_payload):
    """
    Generate a new access token from a valid refresh token payload.

    Args:
        refresh_payload (dict): The decoded refresh token payload

    Returns:
        str: The newly generated access token
    """
    # Create a new access token with the same user info
    user_id = refresh_payload.get("user_id")
    username = refresh_payload.get("username")  # Extract username from refresh token

    # Set expiration for new access token
    expire_access = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Create payload for new access token
    access_payload = {
        "user_id": user_id,
        "username": username,  # Include username in new access token
        "exp": expire_access,
    }

    # Generate and return the new access token
    new_access_token = jwt.encode(access_payload, SECRET_JWT_KEY, algorithm="HS256")
    print(f"🔄 Generated new access token: {new_access_token[:20]}...", flush=True)

    return new_access_token


# Function to check if a user is authenticated based on cookies
def is_authenticated(request: Request):
    """
    Check if the request contains valid authentication cookies.

    Args:
        request (Request): The FastAPI request object

    Returns:
        tuple: (is_authenticated, user_info)
    """
    # Get the access token from cookies
    access_token = request.cookies.get("access_token")
    if not access_token:
        return False, None

    # Verify the token
    payload = verify_jwt(access_token)
    if not payload:
        # If access token is invalid, check refresh token
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return False, None

        refresh_payload = verify_jwt(refresh_token)
        if not refresh_payload:
            return False, None

        # Implement token refresh
        new_access_token = refresh_access_token(refresh_payload)

        # Set new access token in the response
        # Since this is middleware and not a full response handler,
        # we'll need to return a signal to set a new cookie
        return True, {
            "user_id": refresh_payload.get("user_id"),
            "username": refresh_payload.get(
                "username"
            ),  # Include username from refresh token
            "refresh_needed": True,
            "new_access_token": new_access_token,
        }

    # Return authentication status and user info from the valid access token
    return True, {
        "user_id": payload.get("user_id"),
        "username": payload.get("username"),
    }


# Function to handle user logout
async def logout_fastAPI(request: Request):
    """
    Logout a user by clearing their JWT cookies.

    Args:
        request (Request): The FastAPI request object

    Returns:
        JSONResponse with cleared cookies and redirect header
    """
    print("🚪 Logout requested", flush=True)

    # Create response
    response = JSONResponse(content={"success": True, "message": "Déconnexion réussie"})

    # Clear cookies by setting them with empty values and making them expire immediately
    response.delete_cookie(
        key="access_token",
        path="/",  # Must match how it was set
        httponly=True,  # Must match how it was set
        samesite="Lax",  # Must match how it was set
    )

    response.delete_cookie(
        key="refresh_token",
        path="/",  # Must match how it was set
        httponly=True,  # Must match how it was set
        samesite="Lax",  # Must match how it was set
    )

    # Add a header for HTMX to redirect to login page
    response.headers["HX-Redirect"] = "/login"

    # Log for debugging
    print("🔑 JWT Cookies cleared", flush=True)

    return response
