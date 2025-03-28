import os
from django.shortcuts import render
from match_app.services.pong import Pong
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, JsonResponse

pongs = []


def new_match(request: HttpRequest):
    pong = Pong(int(request.GET.get("p1")), int(request.GET.get("p2")))
    pongs.append(pong)
    return JsonResponse({"matchId": pong.id}, status=201)


def enter_match(    : HttpRequest):

    return render(
        request,
        "pong.html",
        {
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8443"),
            "matchId": int(request.GET.get("matchId", "0")),
            "playerId": int(request.GET.get("playerId", "0")),
        },
    )


def enter_match3d(request: HttpRequest):

    return render(
        request,
        "pong3d.html",
        {
            "rasp": os.getenv("rasp", "false"),
            "pidom": os.getenv("pi_domain", "localhost:8443"),
            "matchId": int(request.GET.get("matchId", "0")),
            "playerId": int(request.GET.get("playerId", "0")),
        },
    )


async def stop_match(request: HttpRequest, playerId, matchId):

    for p in pongs:
        if p.id == matchId:
            if await p.stop(playerId):
                return JsonResponse({"status": "succes"})
            else:
                return JsonResponse({"status": "fail"}, status=200)
    return JsonResponse({"status": "not authorized"}, status=200)


def del_pong(pong_id):
    print("DEL PONG {pong_id}", flush=True)
    print(pongs, flush=True)
    pongs[:] = [p for p in pongs if p.id != pong_id]
    print(pongs, flush=True)
