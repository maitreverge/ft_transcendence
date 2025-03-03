import pyotp
import qrcode
import io
import base64
# import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TwoFaForm
from user_management_app.models import Player


@login_required
def check_2fa(request):
    if request.method == "POST":
        form = TwoFaForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            user = request.user
            
            # Get the user's secret and verify the token
            secret = user._two_fa_secret
            totp = pyotp.TOTP(secret)
            
            if totp.verify(str(token)):
                return redirect('auth_index')
            else:
                form.add_error('token', 'Invalid token. Please try again.')
    else:
        form = TwoFaForm()
    
    
    return render(
        request,
        "auth_app/check_2fa.html",
        {"title": "Check Two-Factor Authentication", "form": form},
    )


@login_required
def setup_2fa(request):

    user = request.user

    # secret = pyotp.random_base32()

    # Save secret in database (this prevents overwriting an existing one)
    if not user._two_fa_secret:
        # Generate a new secret key
        secret = pyotp.random_base32()
        user._two_fa_secret = secret  # Encrypt the secret before saving
        user.save()
    else:
        secret = user._two_fa_secret  # Decrypt the secret before using

        # Generate QR Code URI
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.username, issuer_name="TryHardTeam Inc."
    )

    # Generate QR code image
    temp_qr_code = qrcode.make(otp_uri)
    img_io = io.BytesIO()
    temp_qr_code.save(img_io, format="PNG")
    img_io.seek(0)

    # Convert QR Code to Base64
    qr_code = base64.b64encode(img_io.getvalue()).decode("utf-8")

    return render(
        request,
        "auth_app/setup_2fa.html",
        {
            "title": "Set Up Two-Factor Authentication",
            "secret": secret,
            "qr_code": qr_code,
        },
    )
