import pyotp
import qrcode
import io
import base64
import os
from cryptography.fernet import Fernet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from user_management_app.models import Player
from django.http import HttpResponse
from django.conf import settings

# Generate a secret key (only do this once, then store it securely)
# FERNET_KEY = os.getenv("2FA_KEY")
FERNET_KEY = getattr(settings, "FERNET_SECRET_KEY", None)

if not FERNET_KEY:
    raise ValueError("FERNET_SECRET_KEY is missing from settings!")

cipher = Fernet(FERNET_KEY.encode())

# Encrypts the 2FA secret key.
def encrypt_2fa_secret(secret):
    return cipher.encrypt(secret.encode()).decode()

# Decrypts the 2FA secret key.
def decrypt_2fa_secret(encrypted_secret):
    return cipher.decrypt(encrypted_secret.encode()).decode()


@login_required
def verify_2fa(request):
    pass


@login_required
def setup_2fa(request):

    user = request.user

    # secret = pyotp.random_base32()

    # Save secret in database (this prevents overwriting an existing one)
    if not user.two_fa_secret:
        # Generate a new secret key
        secret = pyotp.random_base32()
        user.two_fa_secret = secret # Encrypt the secret before saving
        user.save()
    else:
        secret = user.two_fa_secret # Decrypt the secret before using
    
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




