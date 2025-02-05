from django.shortcuts import render
import os

def match(request):
    return render(request, "match.html", {"truc": "trouffion du bidule", "rasp":os.getenv("rasp", "false")})
