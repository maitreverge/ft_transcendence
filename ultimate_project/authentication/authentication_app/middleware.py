import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Public paths that don't require authentication
        exempt_paths = ['/auth/login/', '/auth/refresh-token/', '/static/']
        
        # Check if the current path is exempt
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)
            
        # Get the token from cookie
        token = request.COOKIES.get('access_token')
        
        if not token:
            return redirect('login')
            
        try:
            # Verify the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Add user info to the request
            request.user_id = payload.get('user_id')
            request.username = payload.get('username')
            
            # Continue to the view
            return self.get_response(request)
            
        except jwt.ExpiredSignatureError:
            # Try to use refresh token (automatic redirection)
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                # You could automatically refresh here or redirect to refresh endpoint
                return redirect('refresh_token')
            return redirect('login')
            
        except jwt.InvalidTokenError:
            # Invalid token, clear cookies and redirect to login
            response = redirect('login')
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response