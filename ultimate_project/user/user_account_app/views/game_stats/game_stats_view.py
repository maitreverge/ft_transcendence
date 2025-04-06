import os
import httpx
import pyotp
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.cache import cache_control

from django.views.decorators.http import require_http_methods

# Custom import
from utils import manage_user_data

#view hope the access will be handle above :)

@require_http_methods(["GET"])
async def game_stats_view(request: HttpRequest):
    
    context = await manage_user_data.build_context(request)
    username = context["username"]
    if username:
        user = await manage_user_data.get_user_info_w_username(username)
        if user:
            context["user"] = user
    if request.headers.get("HX-Request"):
        if request.headers.get("X-Inner-Content-Account") == "true":
                return render(request, "partials/game_stats/game_stats.html", context)
    context["page"] =  "partials/game_stats/game_stats.html"
    return render(request, "layouts/account.html", context)
    
