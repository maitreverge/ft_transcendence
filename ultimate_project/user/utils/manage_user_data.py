import httpx
from django.http import HttpRequest
import os
from typing import Tuple, Dict
from django.http import JsonResponse

async def get_user_info_w_username(username):
    """
    Get user information by username from the database API
    """
    try:
        async with httpx.AsyncClient() as client:
            
            response = await client.get(
                f"http://databaseapi:8007/api/player/?username={username}"
            )

            response_text = response.text  # For plain text responses
            print("\n get_user_info_w_username response: ", response_text, "\n", flush=True) #rm

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0]
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

async def update_user_w_user_id(user_id, data):
    """
    Update user information in the database API
    """
    try:
        print(f"Updating user {user_id} with data: {data}", flush=True)
        async with httpx.AsyncClient() as client:
            # Set content-type header to application/json
            headers = {"Content-Type": "application/json"}
            # Make the PATCH request
            # NEED MOD THIS GO THROUGH FAST API
            response = await client.patch(
                f"http://databaseapi:8007/api/player/{user_id}/",
                json=data,
                headers=headers,
            )
            print(f"Update response status: {response.status_code}", flush=True)
            print(f"Update response content: {response.text}", flush=True)

            if response.status_code == 200:
                # Try to parse JSON response if available
                try:
                    result = response.json()
                    print(f"User updated successfully: {result}", flush=True)
                    return result
                except ValueError:
                    # If response is not JSON, return True to indicate success
                    print("User updated successfully (non-JSON response)", flush=True)
                    return {"success": True}
            print(
                f"Error updating user: HTTP {response.status_code} - {response.text}",
                flush=True,
            )
            return None
    except Exception as e:
        print(f"Exception in update_user: {str(e)}", flush=True)
        return None

async def get_if_user_credentials_valid(username, password):
    """
    Check if the user's credentials are valid using the database API.
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Content-Type": "application/json"}
            data = {
                "username": username,
                "password": password
            }
            response = await client.post(
                "http://databaseapi:8007/api/verify-credentials/",
                headers=headers,
                json=data,
            )
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"User credentials retrieved successfully.", flush=True)
                    return result
                except ValueError:
                    print("User credentials retrieved successfully (non-JSON response)", flush=True)
                    return {"success": True}
            print(f"Error retrieving user credentials: HTTP {response.status_code} - {response.text}",
                flush=True,)
            return None
    except Exception as e:
        print(f"Exception in get_if_user_credentials_valid: {str(e)}", flush=True)
        return None

async def delete_user_w_user_id(user_id):
    """
    Check if the user's credentials are valid using the database API.
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Content-Type": "application/json"}
            response = await client.delete(
                f"http://databaseapi:8007/api/player/{user_id}/",
                headers=headers,   
            )
            if response.status_code == 204:
                try:
                    result = response.json()
                    print(f"User deleted successfully.", flush=True)
                    return result
                except ValueError:
                    print("User deleted successfully (non-JSON response)", flush=True)
                    return {"success": True}
            print(f"Error retrieving user credentials: HTTP {response.status_code} - {response.text}",
                flush=True,)
            return None
    except Exception as e:
        print(f"Exception in get_if_user_credentials_valid: {str(e)}", flush=True)
        return None

async def delete_user_cookies_from_fast_api(request):
    if request.method == "POST":
        fastapi_url = "http://localhost:8005/auth/logout/"
        headers = {'Content-Type': 'application/json'}
        async with httpx.AsyncClient() as client:
            response = await client.post(fastapi_url)
        if response.status_code == 200:
            return JsonResponse({"message": "Successfully logged out from FastAPI."})
        else:
            return JsonResponse({"error": "Failed to log out from FastAPI."}, status=response.status_code)
    return JsonResponse({"error": "Only POST method is allowed."}, status=405)

async def build_context(request: HttpRequest) -> Dict:
    """Build the base context with username from Request if found"""
    username = request.headers.get("X-Username")
    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }
    if username:
        context["username"] = username
    else:
        context["username"] = None
    return context
