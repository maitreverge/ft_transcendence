import pyotp
import qrcode
import io
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_management_app.models import Player
from django.http import HttpResponse


def verify_2fa(request):
    pass


@login_required
def enable_2fa(request):
    
    # Generate a new secret key
    secret = pyotp.random_base32()

    

    return render(request, "auth_app/enable_2fa.html", {
        "title": "This is 2FA setup",
        "secret": secret,
    })
