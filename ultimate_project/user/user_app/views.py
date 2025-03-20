import os
from django.shortcuts import render, redirect
from django.http import HttpRequest
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
        "pidom": os.getenv("pi_domain", "localhost:8000"),
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


def stats(request: HttpRequest):
    return render(
        request,
        "stats.html",
        {
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
        },
    )


async def upload_profile_picture(request: HttpRequest):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        # Get username from the JWT header
        username = request.headers.get("X-Username")

        if not username:
            return redirect("profile")

        # Get the uploaded file
        uploaded_file = request.FILES["profile_picture"]

        # Upload the file to the database API
        try:
            async with httpx.AsyncClient() as client:
                # First get the user to get their ID
                user_response = await client.get(
                    f"http://databaseapi:8007/api/player/?username={username}"
                )

                if user_response.status_code != 200:
                    return redirect("profile")

                user_data = user_response.json()

                # Check if we got a user
                if isinstance(user_data, list) and len(user_data) > 0:
                    user_id = user_data[0]["id"]
                elif (
                    isinstance(user_data, dict)
                    and user_data.get("results")
                    and len(user_data["results"]) > 0
                ):
                    user_id = user_data["results"][0]["id"]
                else:
                    return redirect("profile")

                # Prepare multipart form data
                files = {
                    "profile_picture": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.content_type,
                    )
                }

                # Update the user with the new profile picture
                update_response = await client.patch(
                    f"http://databaseapi:8007/api/player/{user_id}/", files=files
                )

                if update_response.status_code not in [200, 201, 204]:
                    print(
                        f"Error updating profile picture: {update_response.text}",
                        flush=True,
                    )
                else:
                    # If successful, get the updated user data
                    user_response = await client.get(
                        f"http://databaseapi:8007/api/player/{user_id}/"
                    )
                    if user_response.status_code == 200:
                        user = user_response.json()
                        # Render only the form part for HTMX response
                        return render(
                            request, "profile_picture_form.html", {"user": user}
                        )

        except Exception as e:
            print(f"Error uploading profile picture: {str(e)}", flush=True)

    # If anything fails, redirect to the profile page
    return redirect("profile")
