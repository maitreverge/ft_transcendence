import os
import httpx
import pyotp
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.cache import cache_control

# Custom import
from utils import manage_user_data


async def handle_get_game_stats(request, username, context):
    
    try:
        if not username:
            context["error"] = "You must be logged in to perform this action. Please log in and try again."
            return render(request, "partials/game_stats/error_stats.html", context), True
        user = await manage_user_data.get_user_info_w_username(username)
        if not user:
            context["error"] = "We couldn't find a user with the provided information. Please check your credentials and try again."
            return render(request, "partials/game_stats/error_stats.html", context), True
        context["user"] = user
        main_stats, stats_history = await manage_user_data.get_user_match_stats(username, user["id"])        
        if (main_stats == None or stats_history == None):
            context["error"] = "No player statistics found. Please try again later."
            return render(request, "partials/game_stats/error_stats.html", context), True
        context['main_stats'] = main_stats
        context['stats_history'] = stats_history
        
        
        return render_to_string("partials/game_stats/stats/overview.html", context,  request=request), False
    except Exception as e:
        print(f"ERROR CAUGHT: {e}", flush=True) #rm
        context["error"] = "An error occurred while retrieving player statistics. Please try again later."
        return render(request, "partials/game_stats/error_stats.html", context), True
    

@require_http_methods(["GET"])
async def game_stats_overview(request: HttpRequest):
    
    try:
        context = await manage_user_data.build_context(request)
        username = context["username"]
        if request.method == "GET":
            response, is_error_page = await handle_get_game_stats(request, username, context)
        
        if request.headers.get("HX-Request"):
            header = request.headers.get("HX-Target")
            if header == "account-content":
                if is_error_page:
                    return (response)
                # first load case when we click on side bar  button
                context["page_stats"] = response # will be rendered html
                return render(request, "partials/game_stats/game_stats.html", context)
            elif header == "stats-content":
                # case when we click on page button juts reload inner content
                if is_error_page: # error page are not render to string but render direcly
                    return (response)
                else:
                    # because response is str html for just inner overview or match history
                    return HttpResponse(response)

        if is_error_page:
            context["page"] = "partials/game_stats/error_stats.html"
        else:
            context["page_stats"] = response
            context["page"] = render_to_string("partials/game_stats/game_stats.html", context, request=request)
        return render(request, "layouts/account.html", context)
    except Exception as e:
        print(f"\n❌ Exception in game_stats_overview: {e}\n", flush=True)
        if request.headers.get("HX-Request"):
            if request.headers.get("HX-Target") == "account-content":
                return render(request, "partials/game_stats/error_stats.html", context)
        context["page"] = "partials/game_stats/error_stats.html"
        return render(request, "layouts/account.html", context)