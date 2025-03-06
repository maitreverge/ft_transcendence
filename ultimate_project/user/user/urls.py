from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import user_app.views as views
from django.views.decorators.csrf import csrf_exempt

# Create a view that doesn't get logged
@csrf_exempt
def health_check(request):
    return HttpResponse(status=200)


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("user/", include("user_management_app.urls")),
    path("user/profile/", views.profile),
    path("user/stats/", views.stats),
]
