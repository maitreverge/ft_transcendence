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
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Get user from database API
        user = await manage_user_data.get_user_info_w_username(username)
        if not user:
            context["error"] = "We couldn't find a user with the provided information. Please check your credentials and try again."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        context["user"] = user
        
       

    except Exception as e:
        context["error"] = "Something went wrong during 2FA setup. Please try again later."
        return render(request, "partials/security/twofa/error_2fa.html", context), True
    
@require_http_methods(["GET"])
async def game_stats_view(request):
    """Main view function that routes requests based on method."""
    context = await manage_user_data.build_context(request)
    try:
        response, is_error_page = await handle_get_game_stats(request, context["username"], context)
        is_success_page = False
        
        
        if request.headers.get("HX-Request"):
            return (response)
        
        
        if is_error_page:
            context["page"] = "partials/security/twofa/error_2fa.html"
        elif is_success_page:
            context["page"] = "partials/security/twofa/success_2fa.html"
        else:
            context["page"] = "partials/security/twofa/verify_2fa.html"        
        return render(request, "layouts/account.html", context)
    except Exception as e:
        print(f"\n❌ Exception in verify_2fa_view: {e}\n", flush=True)
        if request.headers.get("HX-Request"):
            return render(request, "partials/security/twofa/error_2fa.html", context)
        context["page"] = "partials/security/twofa/error_2fa.html"
        return render(request, "layouts/account.html", context)



@require_http_methods(["GET"])
async def game_stats_view(request: HttpRequest):
    
    context = await manage_user_data.build_context(request)
    username = context["username"]
    if username:
        user = await manage_user_data.get_user_info_w_username(username)
        if user:
            context["user"] = user

    if request.headers.get("HX-Request"):
        if request.headers.get("HX-Target") == "account-content":
            return render(request, "partials/game_stats/game_stats.html", context)
    context["page"] =  "partials/game_stats/game_stats.html"
    return render(request, "layouts/account.html", context)
    
