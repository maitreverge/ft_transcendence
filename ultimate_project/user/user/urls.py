from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
import user_app.views as views
import twofa_app.views as twofa_views
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async, async_to_sync
from django.views.decorators.http import require_http_methods, require_POST, require_GET


# Create a view that doesn't get logged
@csrf_exempt
def health_check(request):
    return HttpResponse(status=200)


# Debug view for headers
@csrf_exempt
def debug_headers(request):
    headers = {key: value for key, value in request.headers.items()}
    post_data = {key: value for key, value in request.POST.items()}

    response_data = {
        "headers": headers,
        "post_data": post_data,
        "method": request.method,
    }

    return JsonResponse(response_data)


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("debug-headers/", debug_headers, name="debug_headers"),
    path("user/", include("user_management_app.urls")),
    path("user/profile/", views.profile),
    path("user/stats/", views.stats),
    path("user/setup-2fa/", async_to_sync(twofa_views.setup_2fa)),
    path("user/verify-2fa/", async_to_sync(twofa_views.verify_2fa)),
    path("user/disable-2fa/", csrf_exempt(async_to_sync(twofa_views.disable_2fa))),
]
