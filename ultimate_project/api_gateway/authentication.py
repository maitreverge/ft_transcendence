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
            raise HTTPException(status_code=401, detail=error_message)

        # 🔹 L'authentification est réussie, récupérer les données utilisateur
        auth_data = db_response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Database API error: {str(e)}")

    # 🔹 Générer les tokens JWT
    expire_access = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_refresh = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_payload = {
        "user_id": auth_data.get("user_id", 0),
        "username": username,
        "exp": expire_access,
    }
    refresh_payload = {
        "user_id": auth_data.get("user_id", 0),
        "exp": expire_refresh,
    }

    access_token = jwt.encode(access_payload, SECRET_JWT_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, SECRET_JWT_KEY, algorithm="HS256")

    # 🔹 Stocker les tokens dans des cookies HTTP sécurisés
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Empêche l’accès via JavaScript (protection XSS)
        secure=False,  # Doit être True en production avec HTTPS
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 6,  # Expire en 6 heures
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Doit être True en production avec HTTPS
        samesite="Lax",
        path="/",
        max_age=60 * 60 * 24 * 7,  # Expire en 7 jours
    )

    # 🔹 Log pour debug
    print(f"Access Token: {access_token[:20]}...", flush=True)
    print(f"Refresh Token: {refresh_token[:20]}...", flush=True)

    # 🔹 Indiquer à HTMX de rediriger l'utilisateur
    response.headers["HX-Redirect"] = "/home"

    return JSONResponse(content={"success": True, "message": "Connexion réussie"})
