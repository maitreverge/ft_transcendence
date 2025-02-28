import pyotp
import qrcode
import io
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_management_app.models import Player
from django.http import HttpResponse


def verify_2fa(request):
    pass


@login_required
def setup_2fa(request):

    user = request.user

    # Generate a new secret key
    secret = pyotp.random_base32()

    # Save secret in database (this prevents overwriting an existing one)
    if user.two_fa_enabled:
        user.two_fa_secret = secret
        user.save()
    
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




