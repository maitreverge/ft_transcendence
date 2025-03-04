import os
from django.shortcuts import render
from match_app.services.pong import Pong
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, JsonResponse

pongs = []

def new_match(request : HttpRequest):
    print("********************* NEW MATCH *********************", flush=True)
    pong = Pong(request.GET.get("p1"), request.GET.get("p2"))
    pongs.append(pong)
    return JsonResponse({"matchId":f"{pong.id}"}, status=201)

def start_match(request : HttpRequest):
    print("********************* START MATCH *********************", flush=True)
    matchId = request.GET.get("matchId", "0")
    playerId = request.GET.get("playerId", "0")
    print("matchId: ", matchId, flush=True)
    print("playerId: ", playerId, flush=True)
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

async def stop_match(request : HttpRequest, playerId, matchId): 
	print(f"je suis ds stop match et l'id est: {matchId} typ: {type(matchId)} et playerId est : {playerId} typ: {type(playerId)}", flush=True)
	for p in pongs:
		if p.id == matchId:
			if await p.stop(playerId):  
				return JsonResponse({"status": "succes"})
			else:
				return JsonResponse({"status": "fail"}, status=500) 
	print(f"je suis ds stop match et l'id est: {matchId}", flush=True)
	return JsonResponse({"status": "not authorized"}, status=504)

# def stop_match(request: HttpRequest, playerId, matchId): 
#     print(f"je suis ds stop match et l'id est: {matchId} typ: {type(matchId)} et playerId est : {playerId} typ: {type(playerId)}", flush=True)
    
#     for p in pongs:
#         print(f"Checking p.id: {p.id} typ: {type(p.id)}", flush=True)  # Debug

#         if p.id == matchId:
#             print(f"Match trouvé ! ID: {p.id}", flush=True)
#             if p.stop(playerId):  
#                 return JsonResponse({"status": "succes"})
#             else:
#                 return JsonResponse({"status": "fail"}, status=500) 
    
#     print(f"Aucun match trouvé pour matchId: {matchId}", flush=True)
#     return JsonResponse({"status": "not authorized"}, status=504)
