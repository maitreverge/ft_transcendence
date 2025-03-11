import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # Disable CSRF protection for the login view
def login_view(request):
    if request.method == "POST":
        cur_username = request.POST.get("username")
        cur_password = request.POST.get("password")

        logger.info("============== Login Attempt ==============")

        # Call the database API to verify credentials
        try:
            response = requests.post(
                "http://databaseapi:8007/api/verify-credentials/",
                data={"username": cur_username, "password": cur_password},
            )

            if response.status_code == 200:
                logger.info("============== Successful Login ==============")
                # Authentication successful
                auth_data = response.json()

                # Generate access token (short-lived)
                access_payload = {
                    "user_id": auth_data.get("user_id", 0),
                    "username": cur_username,
                    "exp": datetime.utcnow() + timedelta(minutes=15),  # 15 min expiry
                }
                access_token = jwt.encode(
                    access_payload, settings.SECRET_JWT_KEY, algorithm="HS256"
                )

                # Generate refresh token (longer-lived)
                refresh_payload = {
                    "user_id": auth_data.get("user_id", 0),
                    "exp": datetime.utcnow() + timedelta(days=7),  # 7 days expiry
                }
                refresh_token = jwt.encode(
                    refresh_payload, settings.SECRET_JWT_KEY, algorithm="HS256"
                )

                # Return JSON response instead of redirect
                logger.info(
                    "============== Successful Login - JWT Tokens Created =============="
                )
                response = JsonResponse(
                    {
                        "success": True,
                        "redirect_to": "/home/",
                        "user": {
                            "id": auth_data.get("user_id", 0),
                            "username": cur_username,
                        },
                    }
                )

                # Set cookies with appropriate attributes for cross-service sharing
                response.set_cookie(
                    "access_token",
                    access_token,
                    httponly=True,
                    secure=False,  # Set to True in production with HTTPS
                    samesite="Lax",  # Use 'None' with secure=True in production
                    path="/",  # Make cookie available across all paths
                    max_age=15 * 60,
                    domain=None,  # Use None to allow the browser to set the cookie domain automatically
                )

                response.set_cookie(
                    "refresh_token",
                    refresh_token,
                    httponly=True,
                    secure=False,  # Set to True in production with HTTPS
                    samesite="Lax",  # Use 'None' with secure=True in production
                    path="/",  # Make cookie available across all paths
                    max_age=7 * 24 * 60 * 60,
                    domain=None,  # Use None to allow the browser to set the cookie domain automatically
                )

                # Log token information for debugging
                logger.info(f"Access Token (first 20 chars): {access_token[:20]}...")
                logger.info(f"Refresh Token (first 20 chars): {refresh_token[:20]}...")
                logger.info(f"Response Headers: {dict(response.headers)}")

                return response
            else:
                # Authentication failed - return JSON error
                error_message = response.json().get("error", "Authentication failed")
                return JsonResponse(
                    {"success": False, "error": error_message}, status=401
                )
        except requests.exceptions.RequestException as e:
            # Handle connection errors - return JSON error
            return JsonResponse(
                {"success": False, "error": f"Connection error: {str(e)}"}, status=500
            )

    # For GET requests, show the login form
    return redirect("/auth/login/")


@csrf_exempt
def refresh_token_view(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        return JsonResponse({"error": "Refresh token required"}, status=401)

    try:
        # Verify the refresh token
        payload = jwt.decode(
            refresh_token, settings.SECRET_JWT_KEY, algorithms=["HS256"]
        )

        # Extract user information
        user_id = payload.get("user_id")

        # Generate a new access token
        new_access_payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=15),
        }

        new_access_token = jwt.encode(
            new_access_payload, settings.SECRET_JWT_KEY, algorithm="HS256"
        )

        # Return the new access token
        response = JsonResponse({"message": "Token refreshed successfully"})
        response.set_cookie(
            "access_token",
            new_access_token,
            httponly=True,
            samesite="Lax",  # Add SameSite attribute
            secure=False,  # Set to False during development
            path="/",  # Make cookie available across all paths
            max_age=15 * 60,  # 15 minutes
        )

        return response

    except jwt.ExpiredSignatureError:
        return JsonResponse({"error": "Refresh token expired"}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({"error": "Invalid refresh token"}, status=401)
