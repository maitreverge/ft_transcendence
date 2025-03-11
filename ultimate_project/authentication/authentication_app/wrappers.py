import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps


def block_authenticated_users(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get("access_token")

        if access_token:
            try:
                payload = jwt.decode(
                    access_token, settings.SECRET_JWT_KEY, algorithms=["HS256"]
                )
                return JsonResponse({"detail": "Already authenticated"}, status=403)
            except jwt.ExpiredSignatureError:
                pass  # Token expired, allow login
            except jwt.InvalidTokenError:
                pass  # Invalid token, allow login

        return view_func(request, *args, **kwargs)

    return _wrapped_view
