from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_credentials(request):
    """
    Verify username and password without creating a session.
    Returns user info and token on success.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # This uses Django's authentication system to verify credentials
    user = authenticate(username=username, password=password)

    # OLD SHIT FROM 
    # user = authenticate(request, username=username, password=password)

    
    if user:
        # Generate or get existing token
        # token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'success': True,
            'user_id': user.id,
            'username': user.first_name,
        })
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
