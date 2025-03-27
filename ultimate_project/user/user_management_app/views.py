from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import httpx
import json
from django.conf import settings
import pyotp


# Create your views here.
def index(request):
    return render(
        request,
        "user_management_app/index.html",
        {
            "title": "User Management Page",
        },
    )


@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
async def delete_profile(request):
    if request.method == "GET":
        return render(request, "user_management_app/delete-profile.html")
    else:
        try:
            # Get username from headers
            username = request.headers.get("X-Username")
            if not username:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            # Get form data
            password = request.POST.get("password")
            token = request.POST.get("token")

            if not password:
                return JsonResponse({"error": "Password is required"}, status=400)

            # Get user data from database API
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://databaseapi:8007/api/player/?username={username}"
                )
                # ! Should not happen once the route will be locked
                if response.status_code != 200:
                    return JsonResponse({"error": "User not found"}, status=404)

                # Checking if the user data is a list or a dictionary
                user_data = response.json()
                if isinstance(user_data, list):
                    user = user_data[0]
                elif isinstance(user_data, dict) and "results" in user_data:
                    user = user_data["results"][0]
                else:
                    return JsonResponse({"error": "Invalid user data"}, status=500)

                # Check if 2FA is enabled
                if user.get("two_fa_enabled"):
                    if not token:
                        return JsonResponse(
                            {"error": "2FA code is required"}, status=400
                        )

                    # Verify 2FA code
                    secret = user.get("_two_fa_secret")
                    if not secret:
                        return JsonResponse(
                            {"error": "2FA not properly configured"}, status=500
                        )

                    totp = pyotp.TOTP(secret)
                    if not totp.verify(token):
                        return JsonResponse({"error": "Invalid 2FA code"}, status=400)

                # Verify password
                verify_response = await client.post(
                    "http://databaseapi:8007/api/check-2fa/",
                    json={"username": username, "password": password},
                )

                if verify_response.status_code != 200:
                    return JsonResponse({"error": "Invalid password"}, status=400)

                # Delete user
                delete_response = await client.delete(
                    f"http://databaseapi:8007/api/player/{user['id']}/"
                )

                if delete_response.status_code != 204:
                    return JsonResponse({"error": "Failed to delete user"}, status=500)

                # Return success response with redirect URL
                return JsonResponse({"success": True, "redirect_url": "/register/"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
