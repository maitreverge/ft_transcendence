from django.http import HttpResponse
def verify_2fa(request):
    pass

def enable_2fa(request):
    return HttpResponse("This is the 2FA setup page")