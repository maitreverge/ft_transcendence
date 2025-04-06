import os
from django.http import HttpRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from utils import manage_user_data


#because we will have the update profile in the same view
#@ensure_csrf_cookie
# will see where to handle the post

@require_http_methods(["GET"])
async def profile_view(request: HttpRequest):
    
    context = await manage_user_data.build_context(request)
    username = context["username"]
    if username:
        user = await manage_user_data.get_user_info_w_username(username)
        if user:
            context["user"] = user

     
    #if htmx request with inner content no need to resent the account html 
    if request.headers.get("HX-Request"):
        if request.headers.get("X-Inner-Content-Account") == "true": # we know we are on the account page
            return render(request, "partials/profile/profile.html", context)
    # If it's a full page loading
    context["page"] = "partials/profile/profile.html"
    print(f"RENDER FULL PAGE RELOAD username: {username}\n", flush=True)
    return render(request, "layouts/account.html", context)
