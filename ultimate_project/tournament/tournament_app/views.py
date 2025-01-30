from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def start_tournament(request):
    return HttpResponse("<h1>Tournament houla la</h1>")
