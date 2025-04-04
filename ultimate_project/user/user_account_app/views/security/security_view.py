import os
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from utils import manage_user_data

async def security_view(request: HttpRequest):
    username = request.headers.get("X-Username")
    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }
    # Fetch user data
    if username:
        context["username"] = username
        user = await manage_user_data.get_user_info_w_username(username)
        if user:
            context["user"] = user
    # Handle HTMX requests dynamically
    if request.headers.get("HX-Request"):
        if request.headers.get("X-Inner-Content") == "true":
            return render(request, "partials/security/security.html", context)
    # Default full-page load with security page included
    context["page"] = "partials/security/security.html"
    return render(request, "layouts/account.html", context)


