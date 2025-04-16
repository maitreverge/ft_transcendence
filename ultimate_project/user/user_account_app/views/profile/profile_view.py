import os
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from utils import manage_user_data


@require_http_methods(["GET"])
async def profile_view(request: HttpRequest):
    
    context = await manage_user_data.build_context(request)
    username = context["username"]
    if username:
        user = await manage_user_data.get_user_info_w_username(username)
        if user:
            context["user"] = user
    if request.headers.get("HX-Request"):
        if request.headers.get("HX-Target") == "account-content":
            return render(request, "partials/profile/profile.html", context)
    context["page"] = "partials/profile/profile.html"
    return render(request, "layouts/account.html", context)
