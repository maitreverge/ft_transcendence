import os
from django.shortcuts import render
from match_app.services.pong import Pong
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, JsonResponse

def newMatch(request):
    pong = Pong(request.GET.get("p1"), request.GET.get("p2"))
    return JsonResponse({"matchId":f"{pong.id}"}, status=201)

def startMatch(request : HttpRequest):
    return render(
        request,
        "pong.html",
        {           
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8000"),
            "matchId": request.GET.get("matchId", "0"),           
            "playerId": request.GET.get("playerId", "0")
        },
    )

    