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


async def handle_get_game_stats(request, username, context):
    
    try:
        if not username:
            context["error"] = "You must be logged in to perform this action. Please log in and try again."
            return render(request, "partials/game_stats/error_stats.html", context), True
        # Get user from database API
        user = await manage_user_data.get_user_info_w_username(username)
        if not user:
            context["error"] = "We couldn't find a user with the provided information. Please check your credentials and try again."
            return render(request, "partials/game_stats/error_stats.html", context), True
        context["user"] = user
        data = await manage_user_data.get_user_match_stats(username, user["id"])
        

        return render(request, "partials/game_stats/game_stats.html", context), False
    except Exception as e:
        context["error"] = "Something went wrong during 2FA setup. Please try again later."
        return render(request, "partials/game_stats/error_stats.html", context), True
    


@require_http_methods(["GET"])
async def game_stats_view(request: HttpRequest):
    
    try:
        context = await manage_user_data.build_context(request)
        username = context["username"]
        if request.method == "GET":
            response, is_error_page = await handle_get_game_stats(request, username, context)
    
        if request.headers.get("HX-Request"):
              return (response)
        if is_error_page:
            context["page"] = "partials/game_stats/error_stats.html"
        else:
            context["page"] = "partials/game_stats/game_stats.html"
        return render(request, "layouts/account.html", context)
    except Exception as e:
        print(f"\n❌ Exception in disable_2fa_view: {e}\n", flush=True)
        if request.headers.get("HX-Request"):
            if request.headers.get("HX-Target") == "account-content":
                return render(request, "partials/game_stats/error_stats.html", context)
        context["page"] = "partials/game_stats/error_stats.html"
        return render(request, "layouts/account.html", context)