from django.shortcuts import render


# Create your views here.
def index(request):
    return render(
        request,
        "user_management_app/index.html",
        {
            "title": "User Management Page",
        },
    )
