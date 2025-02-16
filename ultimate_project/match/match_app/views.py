from django.shortcuts import render
import os
from match_app.services.pong import Pong
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, JsonResponse

def newMatch(request):
    pong = Pong()
    return JsonResponse({"id":f"{pong.id}"}, status=201)

def startMatch(request : HttpRequest):
    # return HttpResponse("<h1>TEST</h1>")
    return render(
        request,
        "pong.html",
        {           
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            "matchId": request.GET.get("matchId", "0")
        },
    )

    