import os
from django.shortcuts import render
from django.http import HttpRequest
from django.template.loader import render_to_string


import httpx



async def get_user_by_username(username):
    """
    Get user information by username from the database API
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://databaseapi:8007/api/player/?username={username}"
            )

            if response.status_code == 200:
                data = response.json()

                # Check if response is a list (direct array)
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
                # Check if response has 'results' field (paginated)
                elif (
                    isinstance(data, dict)
                    and data.get("results")
                    and len(data["results"]) > 0
                ):
                    return data["results"][0]

            return None
    except Exception as e:
        print(f"Error getting user by username: {str(e)}", flush=True)
        return None


async def profile(request: HttpRequest):
    # Get username from the JWT header
    username = request.headers.get("X-Username")

    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }

    if username:
        user = await get_user_by_username(username)
        if user:
            context["user"] = user

    return render(
        request,
        "profile.html",
        context,
    )
 
 
 
   
async def account_information(request: HttpRequest):
    # Get username from the JWT header
    username = request.headers.get("X-Username")

    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }

    if username:
        user = await get_user_by_username(username)
        if user:
            context["user"] = user

    return render(
        request,
        "account_information.html",
        context,
    )

def stats(request: HttpRequest):
    return render(
        request,
        "stats.html",
        {
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8443"),
        },
    )




async def profile_tmp(request: HttpRequest):
    # Get username from the JWT header
    username = request.headers.get("X-Username")

    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }

    if username:
        user = await get_user_by_username(username)
        if user:
            context["user"] = user
   
    """ if user:
        context.update({
            "user": user,
            
        }) """
  
    """ "user_id": user.id,
    "email": user.email,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "is_active": user.is_active,
    "is_staff": user.is_staff,
    "two_fa_enabled": user.two_fa_enabled, """

   
    return render(
        request,
        "account.html",  # Render the account.html template directly
        {
            "username": username,
            "page": "profile.html",  # This could be the path to the profile template
            **context  # Pass user-related context (such as user data)
        },
    )


def game_stats(request: HttpRequest):
    return render(
        request,
        "stats.html",
        {
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8443"),
        },
    )