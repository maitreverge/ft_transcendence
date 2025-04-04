from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
import pyotp
import qrcode
import io
import base64
import httpx
import os
from utils import manage_user_data
from user_account_app.forms import custom_form

# === ⭐ Verifying 2FA for user 🔍 ===

async def handle_post_verify(request, username, context):
    """Handles POST request for verifying 2FA token."""
    form = custom_form.TwoFaForm(request.POST)
    if not username:
        context["error"] = "User not authenticated"
        return render(request, "partials/security/twofa/error_2fa.html", context), True, False
    user = await manage_user_data.get_user_info_w_username(username)
    if not user:
        context["error"] = "We couldn't find a user with the provided information."
        return render(request, "partials/security/twofa/error_2fa.html", context), True, False
    if form.is_valid():
        token = request.POST.get("token")
        secret = user.get("_two_fa_secret")
        if not secret:
            context["error"] = "Two-Factor Authentication secret is missing from your account data."
            return render(request, "partials/security/twofa/error_2fa.html", context), True, False
        totp = pyotp.TOTP(secret)
        if totp.verify(token):
            update_data = {"two_fa_enabled": True}
            update_result = await manage_user_data.update_user_w_user_id(user["id"], update_data)
            if not update_result:
                context["error"] = "Failed to update 2FA settings. Please check your input or try again later."
                return render(request, "partials/security/twofa/error_2fa.html", context), True, False
            context["message"] = "Two-Factor Authentication (2FA) has been successfully verified!"
            return render(request, "partials/security/twofa/success_2fa.html", context), False, True 
        else:
            form.add_error("token", "The token is invalid. Please check and try again.")
    context["form"] = form
    return render(request, "partials/security/twofa/verify_2fa.html", context), False, False


async def handle_get_verify(request, username, context):
    
    try:
        form = custom_form.TwoFaForm()
        context["form"] = form
        # THIS WILL NEED TO BE DELETE BECAUSE NEED A GLOBAL AUTH HANDLER !!!!!!!!!
        if not username:
            context["error"] = "You must be logged in to perform this action. Please log in and try again."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Get user from database API
        user = await manage_user_data.get_user_info_w_username(username)
        print(f"User data retrieved: {user}", flush=True)
        if not user:
            context["error"] = "We couldn't find a user with the provided information. Please check your credentials and try again."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
            # Check if 2FA is already verified
        if user.get("two_fa_enabled"):
            context["error"] = "2FA is already enabled for this account. You can disable it before making changes."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        if request.headers.get("HX-Request"):
                if request.headers.get("X-Inner-Content") == "true":
                    return render(request, "partials/security/twofa/verify_2fa.html", context)
        context["page"] = "partials/security/twofa/verify_2fa.html"
        return render(request, "layouts/account.html", context)
    except Exception as e:
        context["error"] = "Something went wrong during 2FA setup. Please try again later."
        return render(request, "partials/security/twofa/error_2fa.html", context), True
    


@require_http_methods(["GET", "POST"])
async def verify_2fa_view(request):
    """Main view function that routes requests based on method."""
    username = request.headers.get("X-Username")
    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }
    if username:
            context["username"] = username
    try:
        if request.method == "POST":
            response, is_error_page, is_success_page = await handle_post_verify(request, username, context)
        else:
            response, is_error_page = await handle_get_verify(request, username, context)
            is_success_page = False
        if request.headers.get("HX-Request"):
            if request.headers.get("X-Inner-Content") == "true":
                return (response)
        if is_error_page:
            context["page"] = "partials/security/twofa/error_2fa.html"
        elif is_success_page:
            context["page"] = "partials/security/twofa/success_2fa.html"
        else:
            context["page"] = "partials/security/twofa/verify_2fa.html"        
        return render(request, "layouts/account.html", context)
    except Exception as e:
        print(f"\n❌ Exception in verify_2fa_view: {e}\n", flush=True)
        if request.headers.get("HX-Request"):
                if request.headers.get("X-Inner-Content") == "true":
                    return render(request, "partials/security/twofa/error_2fa.html", context)
        context["page"] = "partials/security/twofa/error_2fa.html"
        return render(request, "layouts/account.html", context)


# === ⭐ Setting up 2FA for user ⭐ ===

async def handle_get_setup(request, username, context):
    try:
        print(f"Setting up 2FA for user: {username}", flush=True)
        if not username:
            context["error"] = "You must be logged in to perform this action. Please log in and try again."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Get user from database API
        user = await manage_user_data.get_user_info_w_username(username)
        print(f"User data retrieved: {user}", flush=True)
        if not user:
            context["error"] = "We couldn't find a user with the provided information. Please check your credentials and try again."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Check if 2FA is already verified
        if user.get("two_fa_enabled"):
            context["error"] = "2FA is already enabled for this account. You can disable it before making changes."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Generate a new secret for 2FA
        secret = pyotp.random_base32()
        print(f"Generated new 2FA secret: {secret}", flush=True)
        # Save the secret to the user via API
        update_data = {"_two_fa_secret": secret}
        update_result = await manage_user_data.update_user_w_user_id(user["id"], update_data)
        if not update_result:
            context["error"] = "Failed to update 2FA settings. Please check your input or try again later."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Generate QR Code URI
        try:
            otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=username, issuer_name="Transcendence")
            print(f"Generated OTP URI: {otp_uri}", flush=True)
            # Generate QR code image
            qr = qrcode.make(otp_uri)
            img_io = io.BytesIO()
            qr.save(img_io, format="PNG")
            img_io.seek(0)
            # Convert to base64 for embedding in HTML
            qr_code_data = base64.b64encode(img_io.getvalue()).decode("utf-8")
            qr_code_img = f"data:image/png;base64,{qr_code_data}"
            print("QR code image generated successfully", flush=True)
            context["qr_code"] = qr_code_img
            context["secret"] = secret
            return render(request, "partials/security/twofa/setup_2fa.html", context), False
        except Exception as e:
            context["error"] = "An error occurred while generating 2FA credentials. Please try again later."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
    except Exception as e:
        context["error"] = "Something went wrong during 2FA setup. Please try again later."
        return render(request, "partials/security/twofa/error_2fa.html", context), True
    
@require_http_methods(["GET"])
async def setup_2fa_view(request):
    username = request.headers.get("X-Username")
    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }
    if username:
        context["username"] = username
    try:
        response, is_error_page = await handle_get_setup(request, username, context)
        if request.headers.get("HX-Request"):
            if request.headers.get("X-Inner-Content") == "true":
                return (response)
        if is_error_page:
            context["page"] = "partials/security/twofa/error_2fa.html"
        else:
            context["page"] = "partials/security/twofa/setup_2fa.html"
        return render(request, "layouts/account.html", context)
    except Exception as e:
        print(f"\n❌ Exception in setup_2fa_view: {e}\n", flush=True)
        if request.headers.get("HX-Request"):
            return render(request, "partials/security/twofa/error_2fa.html", context)
        context["page"] = "partials/security/twofa/error_2fa.html"
        return render(request, "layouts/account.html", context)

# === ⭐ Disabling 2FA for user 🔒 ===

async def handle_get_disable(request, username, context):
    try:
        print(f"Setting up 2FA for user: {username}", flush=True)
        if not username:
            context["error"] = "You must be logged in to perform this action. Please log in and try again."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Get user from database API
        user = await manage_user_data.get_user_info_w_username(username)
        print(f"User data retrieved: {user}", flush=True)
        if not user:
            context["error"] = "We couldn't find a user with the provided information. Please check your credentials and try again."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        # Check if 2FA is already verified
        if not user.get("two_fa_enabled"):
            context["error"] = "2FA is already disabled for this account. You can enable it before making changes."
            return render(request, "partials/security/twofa/error_2fa.html", context), True
        if request.headers.get("HX-Request"):
                if request.headers.get("X-Inner-Content") == "true":
                    return render(request, "partials/security/twofa/disable_2fa.html", context)
        context["page"] = "partials/security/twofa/disable_2fa.html"
        return render(request, "layouts/account.html", context), False
    except Exception as e:
        context["error"] = "Something went wrong during 2FA setup. Please try again later."
        return render(request, "partials/security/twofa/error_2fa.html", context), True
    

async def handle_post_disable(request, username, context):
    print(f"🔐 Disabling 2FA for: {username}", flush=True)
    form = custom_form.TwoFaForm(request.POST)

    if not username:
        context["error"] = "User not authenticated"
        return render(request, "partials/security/twofa/error_2fa.html", context), True, False
    
    user = await manage_user_data.get_user_info_w_username(username)
    if not user:
        context["error"] = "We couldn't find a user with the provided information."
        return render(request, "partials/security/twofa/error_2fa.html", context),  True, False
    
    context["user"] = user
    if not form.is_valid():
        context["error"] = "Oops! Looks like something’s missing or incorrect in the form."
        return render(request, "partials/security/twofa/disable_2fa.html", context) , False, False
    
    token = request.POST.get("token")
    if not token:
        context["error"] = "You need to provide your 2FA code from your authenticator app."
        return render(request, "partials/security/twofa/disable_2fa.html", context) , False, False
        
    if not token.isdigit() or len(token) != 6:
        context["error"] = "The code you entered is not valid. Please try again."
        return render(request, "partials/security/twofa/disable_2fa.html", context) , False, False

    secret = user.get("_two_fa_secret")
    if not secret:
        context["error"] = "Two-Factor Authentication secret is missing from your account data."
        return render(request, "partials/security/twofa/disable_2fa.html", context) , False, False
    
    totp = pyotp.TOTP(secret)
    if not totp.verify(token):
        context["error"] = "Invalid 2FA code."
        return render(request, "partials/security/twofa/disable_2fa.html", context) , False, False
    
    update_data = {"two_fa_enabled": False, "_two_fa_secret": None}
    update_result = await manage_user_data.update_user_w_user_id(user["id"], update_data)
    if not update_result:
        context["error"] = "Failed to update 2FA settings. Please check your input or try again later."
        return render(request, "partials/security/twofa/disable_2fa.html", context) , False, False

    print("✅ 2FA disabled successfully", flush=True)
    context["message"] = "Two-Factor Authentication has been disabled successfully."
    return render(request, "partials/security/twofa/success_2fa.html", context) , False, True
    

@require_http_methods(["GET", "POST"])
async def disable_2fa_view(request):
    """Route disable 2FA view based on request method."""
    username = request.headers.get("X-Username")
    context = {
        "rasp": os.getenv("rasp", "false"),
        "pidom": os.getenv("pi_domain", "localhost:8443"),
    }
    if username:
            context["username"] = username
    try:
        if request.method == "POST":
            response, is_error_page, is_success_page = await handle_post_disable(request, username, context)
        else:
            response, is_error_page = await handle_get_disable(request, username, context)
            is_success_page = False
        if request.headers.get("HX-Request"):
            if request.headers.get("X-Inner-Content") == "true":
                return (response)
        if is_error_page:
            context["page"] = "partials/security/twofa/error_2fa.html"
        elif is_success_page:
            context["page"] = "partials/security/twofa/success_2fa.html"
        else:
            context["page"] = "partials/security/twofa/disable_2fa.html"
        return render(request, "layouts/account.html", context)
    except Exception as e:
        print(f"\n❌ Exception in disable_2fa_view: {e}\n", flush=True)
        if request.headers.get("HX-Request"):
            
            return render(request, "partials/security/twofa/error_2fa.html", context)
        context["page"] = "partials/security/twofa/error_2fa.html"
        return render(request, "layouts/account.html", context)

