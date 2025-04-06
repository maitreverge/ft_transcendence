from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from utils import manage_user_data
from django.http import HttpRequest

@require_http_methods(["GET"])
async def conf_view(request: HttpRequest):
    context = await manage_user_data.build_context(request)
    if request.headers.get("HX-Request"):
        if request.headers.get("X-Inner-Content-Account") == "true": # so we know we are on the accoutn page
            return render(request, "partials/confidentiality/conf.html", context)
    # Default full-page load with security page included
    context["page"] = "partials/confidentiality/conf.html"
    return render(request, "layouts/account.html", context)