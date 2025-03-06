from django.urls import path
from django.urls import path, include
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create a view that doesn't get logged
@csrf_exempt
def health_check(request):
    return HttpResponse(status=200)


urlpatterns = [
    path("health/", health_check, name="health_check"),
]





