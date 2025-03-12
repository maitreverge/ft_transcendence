import pyotp
import qrcode
import io
import base64

# import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TwoFaForm
from user_management_app.models import Player
from django.contrib.auth import login


# @login_required
def check_2fa(request):
    # Get user from session
    user_id = request.session.get("user_id_for_2fa")

    if not user_id:
        print("No user_id_for_2fa in session", flush=True)
        return redirect("login")

    # Get user from database - add debug output
    try:
        print(f"Looking for user with ID: {user_id}", flush=True)
        user = Player.objects.filter(id=user_id).first()

        if not user:
            print(f"User with ID {user_id} not found", flush=True)
            return redirect("login")

        print(f"Found user: {user.username}", flush=True)
    except Exception as e:
        print(f"Error retrieving user: {str(e)}", flush=True)
        return redirect("login")

    # Rest of the code remains the same...
    # # this blocks redirects when trying to register a new player

    if request.method == "POST":
        form = TwoFaForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["token"]

            # Get the user's secret and verify the token
            secret = user._two_fa_secret
            totp = pyotp.TOTP(secret)

            if totp.verify(str(token)):
                # Clear the 2FA session and log in the user
                if "user_id_for_2fa" in request.session:
                    del request.session["user_id_for_2fa"]
                login(request, user)
                return redirect("auth_index")
            else:
                form.add_error("token", "Invalid token. Please try again.")
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

    # Always generate a new secret when setting up 2FA
    secret = pyotp.random_base32()
    user._two_fa_secret = secret
    user.two_fa_enabled = True  # Make sure 2FA is enabled
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
