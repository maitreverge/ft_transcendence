from fastapi import Request
import os
import jwt
import datetime
import requests

SECRET_JWT_KEY = os.getenv("JWT_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# ! ALL DEPENDENCIES ARE IN THE AUTHENTICATION.PY FILE


# Function to verify JWT token
def verify_jwt(token):
    """
    Verify a JWT token and return the payload if valid.

    Args:
        token (str): The JWT token to verify

    Returns:
        dict: The decoded token payload if valid, None otherwise
    """
    try:
        # Verify the token with our secret key
        payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


# Function to generate a new access token using a valid refresh token
def refresh_access_token(refresh_payload):
    """
    Generate a new access token from a valid refresh token payload.

    Args:
        refresh_payload (dict): The decoded refresh token payload

    Returns:
        str: The newly generated access token
    """
    # Create a new access token with the same user info
    user_id = refresh_payload.get("user_id")
    username = refresh_payload.get("username")  # Extract username from refresh token

    # Get the current UUID for this user
    try:
        response = requests.get(f"http://databaseapi:8007/api/player/{user_id}/uuid")
        uuid_value = None
        if response.status_code == 200:
            session_data = response.json()
            uuid_value = session_data.get("uuid")
    except Exception as e:
        print(f"⚠️ Error retrieving UUID during refresh: {str(e)}", flush=True)
        uuid_value = None

    # Set expiration for new access token
    expire_access = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Create payload for new access token
    access_payload = {
        "user_id": user_id,
        "username": username,
        "uuid": uuid_value,
        "exp": expire_access,
    }

    # Generate and return the new access token
    new_access_token = jwt.encode(access_payload, SECRET_JWT_KEY, algorithm="HS256")
    print(f"🔄 Generated new access token: {new_access_token[:20]}...", flush=True)

    return new_access_token


# Function to check if a user is authenticated based on cookies
def is_authenticated(request: Request):
    """
    Check if the request contains valid authentication cookies.

    Args:
        request (Request): The FastAPI request object

    Returns:
        tuple: (is_authenticated, user_info)
    """

    # Get the access token from cookies
    access_token = request.cookies.get("access_token")
    if not access_token:
        return False, None

    # Verify the token
    payload = verify_jwt(access_token)
    if not payload:
        # If access token is invalid, check refresh token
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return False, None

        refresh_payload = verify_jwt(refresh_token)
        if not refresh_payload:
            return False, None

        # Implement token refresh
        new_access_token = refresh_access_token(refresh_payload)

        # Set new access token in the response
        # Since this is middleware and not a full response handler,
        # we'll need to return a signal to set a new cookie
        return True, {
            "user_id": refresh_payload.get("user_id"),
            "username": refresh_payload.get("username"),
            "refresh_needed": True,
            "new_access_token": new_access_token,
        }

    # Get the user ID and UUID from the token
    user_id = payload.get("user_id")
    token_uuid = payload.get("uuid")

    # Verify this is the active session for the user
    if token_uuid:
        try:
            # Check if this session is still valid
            response = requests.get(
                f"http://databaseapi:8007/api/player/{user_id}/uuid"
            )
            if response.status_code == 200:
                current_data = response.json()
                current_uuid = current_data.get("uuid")

                # If the UUIDs don't match, this token is from an old session
                if current_uuid and current_uuid != token_uuid:
                    print(
                        f"⚠️ UUID mismatch. Token: {token_uuid}, DB: {current_uuid}",
                        flush=True,
                    )
                    return False, None
        except Exception as e:
            print(f"⚠️ Error checking UUID: {str(e)}", flush=True)
            # Continue with authentication if we can't check the UUID
            # This is a failsafe to prevent lockouts if the database API is down

    # Return authentication status and user info from the valid access token
    return True, {
        "user_id": payload.get("user_id"),
        "username": payload.get("username"),
    }
