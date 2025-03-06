import os
from django.shortcuts import render
from match_app.services.pong import Pong
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, JsonResponse

pongs = []

def new_match(request : HttpRequest):
	pong = Pong(int(request.GET.get("p1")), int(request.GET.get("p2")))
	pongs.append(pong)
	return JsonResponse({"matchId": pong.id}, status=201)

def start_match(request : HttpRequest):

	return render(
		request,
		"pong.html",
		{           
			"rasp": os.getenv("rasp", "false"),
			"pidom": os.getenv("pi_domain", "localhost:8000"),
			"matchId": int(request.GET.get("matchId", "0")),           
			"playerId": int(request.GET.get("playerId", "0"))
		},
	)

async def stop_match(request : HttpRequest, playerId, matchId): 

	for p in pongs:
		if p.id == matchId:
			if await p.stop(playerId):  
				return JsonResponse({"status": "succes"})
			else:
				return JsonResponse({"status": "fail"}, status=500)
	return JsonResponse({"status": "not authorized"}, status=403)

def del_pong(pong_id):
	print(pongs, flush=True)
	pongs[:] = [p for p in pongs if p.id != pong_id]
	print(pongs, flush=True)
