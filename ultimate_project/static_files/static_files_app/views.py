from django.shortcuts import render


def index(request):
    arg = "toto"
    return render(request, "index.html", {'arg':arg}) 
