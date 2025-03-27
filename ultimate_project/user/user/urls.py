from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse

import user_app.views as user_views
import twofa_app.views as twofa_views
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async, async_to_sync
from django.views.decorators.http import require_http_methods, require_POST, require_GET


# Create a view that doesn't get logged
@csrf_exempt
def health_check(request):
    return HttpResponse(status=200)


# # Debug view for headers
# @csrf_exempt
# def debug_headers(request):
#     headers = {key: value for key, value in request.headers.items()}
#     post_data = {key: value for key, value in request.POST.items()}

#     response_data = {
#         "headers": headers,
#         "post_data": post_data,
#         "method": request.method,
#     }

#     return JsonResponse(response_data)


urlpatterns = [
    # path("admin/", admin.site.urls),
    path("health/", health_check, name="health_check"),
    # path("debug-headers/", debug_headers, name="debug_headers"),
   
   
    # TO DO
    # for matchign url to the management app url if any
    #pth("user/", include("user_management_app.urls")),
    
    path("user/account/", user_views.profile),
    path("user/stats/", user_views.stats),
    path("user/setup-2fa/", async_to_sync(twofa_views.setup_2fa)),
    path("user/verify-2fa/", async_to_sync(twofa_views.verify_2fa)),
    path("user/disable-2fa/", async_to_sync(twofa_views.disable_2fa)),
    
    
    # base url when going into your account
    path("user/account/profile/", async_to_sync(user_views.profile_tmp)),
    path("user/account/game-stats/", user_views.stats),
    
    
    
    
    
    #Preparing urls for account manager
    # 1 -  account info / 2 - Security / 
    # 3 - game stat
    # 4 - Confidentialité (show if connected or not / accept firend request or not
    # delete account)
    
    # display as a grid
    # 1 - 2 
    # 3 - 4
    # (1) path("user/account/account-information/", views.profile),
    # (2) path("user/account/security-settings/", async_to_sync(twofa_views.setup_2fa)),
    # (3) path("user/account/game_stats/", async_to_sync(twofa_views.setup_2fa)),
    # (4) path("user/account/security-settings/", async_to_sync(twofa_views.setup_2fa)),
 
    #path("user/account/setup-2fa/", async_to_sync(twofa_views.setup_2fa)),
    #path("user/account/verify-2fa/", async_to_sync(twofa_views.verify_2fa)),
    #path("user/account/disable-2fa/", async_to_sync(twofa_views.disable_2fa)),
    
    
    
   
]
