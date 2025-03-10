import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    print("============== PRINT REQUEST ==============", flush=True)
    print("Request Method:", request.method, flush=True)
    print("Request Headers:", request.headers, flush=True)
    print("Request Body:", request.body, flush=True)
    print("============== PRINT REQUEST ==============", flush=True)
    
    
    if request.method == "POST":
        cur_username = request.POST.get('username')
        cur_password = request.POST.get('password')

        # print("============== PRINT POST ==============", flush=True)
        # print("Username:", cur_username, flush=True)
        # print("Password:", cur_password, flush=True)
        # print("============== PRINT POST ==============", flush=True)
        
        # Call the database API to verify credentials
        try:
            response = requests.post(
                'http://databaseapi:8007/api/verify-credentials/',
                data={'username': cur_username, 'password': cur_password}
            )
            
            if response.status_code == 200:
                # Authentication successful
                # auth_data = response.json()
                
                # # Store auth token in session or cookie
                # request.session['auth_token'] = auth_data['token']
                # request.session['user_id'] = auth_data['user_id']
                # request.session['username'] = auth_data['username']
                
                # Redirect to home or dashboard
                print("============== Successfull Login ==============", flush=True)
                print("============== Successfull Login ==============", flush=True)
                print("============== Successfull Login ==============", flush=True)
                # return redirect('home')
            else:
                # Authentication failed
                error_message = response.json().get('error', 'Authentication failed')
                messages.error(request, error_message)
        except requests.exceptions.RequestException as e:
            # Handle connection errors
            messages.error(request, f"Connection error: {str(e)}")
    
    # For GET requests or failed POST, show the login form
    # return render(request, 'authentication_app/login.html')