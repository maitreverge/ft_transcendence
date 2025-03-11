import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Public paths that don't require authentication
        exempt_paths = ["/auth/login/", "/auth/refresh-token/", "/static/"]

        # Check if the current path is exempt
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)

        # Debug cookies
        logger.info(f"Cookies in middleware: {request.COOKIES}")

        # Get the token from cookie
        token = request.COOKIES.get("access_token")

        if not token:
            # logger.warning("No access token found in cookies")
            if request.headers.get("Accept") == "application/json":
                return JsonResponse({"error": "Authentication required"}, status=401)
            return redirect("login")

        try:
            # Verify the token using the correct secret key
            payload = jwt.decode(token, settings.SECRET_JWT_KEY, algorithms=["HS256"])

            # Add user info to the request
            request.user_id = payload.get("user_id")
            request.username = payload.get("username")

            logger.info(f"Successfully authenticated user: {request.username}")

            # Continue to the view
            return self.get_response(request)

        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            # Try to use refresh token (automatic redirection)
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                # You could automatically refresh here or redirect to refresh endpoint
                if request.headers.get("Accept") == "application/json":
                    return JsonResponse(
                        {"error": "Token expired", "redirect": "/auth/refresh-token/"},
                        status=401,
                    )
                return redirect("refresh_token")

            if request.headers.get("Accept") == "application/json":
                return JsonResponse({"error": "Authentication required"}, status=401)
            return redirect("login")

        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            # Invalid token, clear cookies and redirect to login
            if request.headers.get("Accept") == "application/json":
                response = JsonResponse(
                    {"error": "Invalid authentication token"}, status=401
                )
            else:
                response = redirect("login")

            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
