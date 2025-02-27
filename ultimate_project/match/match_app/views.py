import os
from django.shortcuts import render
from match_app.services.pong import Pong
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, JsonResponse

pongs = []

def new_match(request : HttpRequest):
    pong = Pong(request.GET.get("p1"), request.GET.get("p2"))
    pongs.append(pong)
    return JsonResponse({"matchId":f"{pong.id}"}, status=201)

def start_match(request : HttpRequest):
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

def stop_match(request : HttpRequest, matchId): 
    for p in pongs:
        if p.id == matchId:
            p.stop()   
    print(f"je suis ds stop match et l'id est: {matchId}", flush=True)
    return JsonResponse({"status": "succes"})